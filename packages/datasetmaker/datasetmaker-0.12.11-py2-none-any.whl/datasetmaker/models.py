from pathlib import Path
from typing import Union, Any
import pandas as pd


class Client:
    """Base class for clients."""

    def get(self, **kwargs: Any) -> Union[list, pd.DataFrame]:
        """Get data from remote resource."""
        raise NotImplementedError

    def save(self, path: Union[Path, str], **kwargs: Any) -> None:
        """Save data to disk."""
        raise NotImplementedError
