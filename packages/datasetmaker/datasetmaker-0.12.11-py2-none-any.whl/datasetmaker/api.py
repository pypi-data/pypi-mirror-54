from datasetmaker import clients
from datasetmaker.models import Client


def create_client(source: str) -> Client:
    """
    Create a new client instance.

    Parameters
    ----------
    source
        Name of source.
    """
    return clients.available[source]()  # type: ignore
