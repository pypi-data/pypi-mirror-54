# import pyarrow as pa
import pandas as pd
from .Table import Table


class MultiYearTable:
    _entities: list = []

    def __init__(self, code: str, uttag: str, year_codes: list):
        self.code = code
        self.uttag = uttag
        self.year_codes = year_codes

    @property
    def entities(self) -> list:
        if len(self._entities) > 0:
            return self._entities
        self._entities = Table(self.code, self.uttag, self.year_codes[0]).entities
        return self._entities

    @property
    def data(self) -> pd.DataFrame:
        tables = [Table(self.code, self.uttag, y) for y in self.year_codes]
        tables = [t.data for t in tables if not t.data.empty]
        if not tables:
            return pd.DataFrame()
        return pd.concat(tables, sort=True)

    def __repr__(self) -> str:
        return f'<MultiYearTable code="{self.code}" years={str(self.year_codes)}>'

    def __str__(self) -> str:
        return f'<MultiYearTable code="{self.code}" years={str(self.year_codes)}>'
