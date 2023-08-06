import os
import logging
import socket
from typing import Union, Any, Optional
from pathlib import Path
from ddf_utils import package
from ddf_utils.io import dump_json
import requests
import pandas as pd
from datasetmaker.models import Client
from datasetmaker.datapackage import DataPackage
from datasetmaker.validate import validate_package
from datasetmaker.onto.manager import read_entity
from datasetmaker.utils import concurrent_requests


log = logging.getLogger(__name__)
pd.options.mode.chained_assignment = None


class WAQIClient(Client):
    _base_url = 'http://api.waqi.info'

    def get(self, **kwargs: Any) -> list:
        if not os.environ.get("WAQI_TOKEN"):
            raise KeyError('WAQI_TOKEN not found. Aborting.')

        stations = read_entity('waqi_station')
        self.stations = stations
        records: Union[pd.DataFrame, list] = []

        urls = [f'{self._base_url}/feed/@{x}/?token={os.environ.get("WAQI_TOKEN")}'
                for x in stations.waqi_station]

        records = concurrent_requests(self.get_station_data, urls, max_workers=100)
        records = [x for x in records if x is not None]
        records = pd.io.json.json_normalize(records)
        records = records.drop(['attributions',
                                'city.geo',
                                'city.name',
                                'city.url',
                                'iaqi.p.v',
                                'iaqi.w.v',
                                'iaqi.wg.v',
                                'time.v',
                                'debug.sync',
                                'iaqi.t.v',
                                'iaqi.h.v',
                                'iaqi.dew.v',
                                'dominentpol'], axis=1, errors='ignore')

        # Drop/fix some erroneous rows
        records = records.dropna(subset=['time.s'])
        records = records[records['time.s'] != '']
        records['time.tz'] = records['time.tz'].str.replace('America/New_York\t', '-05:00')

        records['datetime'] = records['time.s'] + records['time.tz']
        records['datetime'] = pd.to_datetime(records.datetime, utc=True)
        records = records.drop(['time.s', 'time.tz'], axis=1)

        records = records.rename(columns={
            'aqi': 'waqi_aqi',
            'idx': 'waqi_station',
            'iaqi.no2.v': 'waqi_no2',
            'iaqi.o3.v': 'waqi_o3',
            'iaqi.co.v': 'waqi_co',
            'iaqi.so2.v': 'waqi_so2',
            'iaqi.pm10.v': 'waqi_pm10',
            'iaqi.pm25.v': 'waqi_pm25',
        })

        records = records[['waqi_aqi', 'waqi_station', 'waqi_no2', 'waqi_o3',
                           'waqi_co', 'waqi_so2', 'waqi_pm10', 'waqi_pm25', 'datetime']]
        records = records.sort_values('waqi_station')
        records = records.merge(stations[['waqi_station', 'country']],
                                on='waqi_station', how='left')

        measures = ['waqi_aqi', 'waqi_no2', 'waqi_o3', 'waqi_pm25',
                    'waqi_co', 'waqi_so2', 'waqi_pm10']

        for measure in measures:
            if measure not in records:
                continue
            records.ddf.register_datapoints(measures=measure, keys=['waqi_station', 'datetime'])

        records.ddf.register_entity('waqi_station')
        records.ddf.register_entity('country')

        self.data = records
        return self.data

    def get_station_data(self, url: str) -> Optional[dict]:
        try:
            r = requests.get(url, timeout=10)
        except socket.timeout:
            log.error(f'URL {url} timed out')
        except socket.gaierror:
            log.error(f'URL {url} raised gaiaerror')

        if r.status_code == 200:
            data = r.json()
            if data['status'] == 'nope':
                log.warn(f'Skipped URL {url}, got "nope" from API')
                return None
            else:
                return data.get('data')
        else:
            log.warn(f'Skipped URL {url} with status code {r.status_code}')
            return None

    def save(self, path: Union[Path, str], **kwargs: Any) -> None:
        kwargs.update({
            'author': 'Datastory',
            'default_measure': 'waqi_pm25',
            'default_primary_key': ['waqi_station', 'datetime'],
            'name': 'waqi',
            'source': 'World Air Quality Index',
            'status': 'draft',
            'title': 'World Air Quality Index',
            'topics': ['environment'],
        })

        path = Path(path)
        if path.exists() and kwargs.get('append', False) is True:
            measures = ['waqi_aqi', 'waqi_no2', 'waqi_o3', 'waqi_pm25',
                        'waqi_co', 'waqi_so2', 'waqi_pm10']
            for measure in measures:
                fname = path / f'ddf--datapoints--{measure}--by--waqi_station--datetime.csv'
                if fname.exists() and measure in self.data:
                    df = pd.read_csv(fname)
                    df['datetime'] = pd.to_datetime(df.datetime, utc=True)
                    df = pd.concat(
                        [df, self.data[[measure, 'waqi_station', 'datetime']]], sort=True)
                    offsets = (pd.Timestamp.utcnow() - df.datetime).dt.days
                    df = df[offsets == 0]
                    df = df.drop_duplicates(subset=['waqi_station', 'datetime'])
                    df.to_csv(fname, index=False)
                elif measure in self.data:
                    self.data[[measure, 'waqi_station', 'datetime']].to_csv(fname, index=False)
            self.stations.to_csv(path / 'ddf--entities--waqi_station.csv', index=False)
            meta = package.create_datapackage(path, **kwargs)
            dump_json(path / 'datapackage.json', meta)

            log.info('Validating package on disk')
            validate_package(path)

            return

        new_package = DataPackage(data=self.data)
        new_package.save(path)
