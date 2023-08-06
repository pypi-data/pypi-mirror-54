import shutil
import pathlib
from typing import Union
from pathlib import Path
import ddf_utils
import pandas as pd
from datasetmaker.datapackage import DataPackage
from datasetmaker.utils import CSV_DTYPES


def merge_packages(paths: list, dest: Union[Path, str], **kwargs: Union[str, list]) -> None:
    """
    Merge multiple DDF packages into one.

    Parameters
    ----------
    paths : list
        List of paths or in-memory packages
    dest : str
        Path to destination DDF package.
    kwargs :
        Metadata for resulting DDF package.
    """
    if isinstance(paths[0], DataPackage):
        tmp_dir = Path('.tmp_packages')
        if tmp_dir.exists():
            shutil.rmtree(tmp_dir)
        tmp_dir.mkdir()
        for i, package in enumerate(paths):
            package.save(tmp_dir / f'data_{i}')
        merge_packages([tmp_dir / f'data_{i}' for i in range(i + 1)], dest)
        shutil.rmtree(tmp_dir)
        return

    dest = pathlib.Path(dest)
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir()

    paths = [pathlib.Path(x) for x in paths]
    for path in paths:
        dst_files = [x.name for x in dest.glob('*.csv')]
        src_files = path.glob('*.csv')
        for src_file in src_files:
            if src_file.name in dst_files:
                if 'ddf--entities' in src_file.name:
                    src_df = pd.read_csv(src_file, dtype=CSV_DTYPES)
                    dst_df = pd.read_csv(dest / src_file.name, dtype=CSV_DTYPES)
                    df = pd.concat([src_df, dst_df], sort=True)
                    df = df.drop_duplicates(subset=src_file.stem.split('--')[-1])
                    df.to_csv(dest / src_file.name, index=False)
                elif 'ddf--concepts' in src_file.name:
                    src_df = pd.read_csv(src_file, dtype=CSV_DTYPES)
                    dst_df = pd.read_csv(dest / src_file.name, dtype=CSV_DTYPES)
                    df = pd.concat([src_df, dst_df], sort=True)
                    df = df.drop_duplicates(subset='concept')
                    df.to_csv(dest / src_file.name, index=False)
                else:
                    raise ValueError('Duplicate datapoints files')
            else:
                shutil.copy(src_file, dest / src_file.name)

    meta = ddf_utils.package.create_datapackage(dest, **kwargs)
    ddf_utils.io.dump_json(dest / 'datapackage.json', meta)


# def merge_packages(paths: list,
#                    dest: Union[Path, str],
#                    include: list = []) -> None:
#     collection = DDFPackageCollection(paths)
#     collection.to_package(dest, include)


def filter_items(items: Union[pd.DataFrame, list],
                 include: list) -> Union[pd.DataFrame, list]:
    """
    Filter items by include.

    Parameters
    ----------
    items : list or DataFrame, sequence to be filtered. If DataFrame,
        assumed to be a DDF concepts file filtered by concept column.
    include : sequence of labels to include in items
    """
    if not include:
        return items
    if type(items) is list:
        if '--' not in items[0]:  # not datapoints
            return filter(lambda x: x in include, items)
        out = []
        for item in items:
            name = item.split('--')[2:]
            name.pop(1)
            if all(x in include for x in name):
                out.append(item)
        return out
    # Items is dataframe
    return items[items.concept.isin(include)]  # type: ignore
