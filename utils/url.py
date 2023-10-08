
from functools import cache
from urllib.parse import urlparse, parse_qs


def get_base_domain(url: str | None) -> str | None:
    """ @return: the top-level-domain of the given @param url. """
    domain: str | None = get_domain(url)
    return ".".join(domain.split(".")[-2:]) if domain else None


def get_domain(url: str | None) -> str | None:
    """ @return: the full domain of the given @param url. """
    if not url:
        return
    domain = urlparse(url).netloc
    return domain.replace("www.", "", 1)


def get_endpoint(url: str | None) -> str | None:
    """ @return: the endpoint of the given @param url ."""
    endpoint: str | None = urlparse(url).path if url else None
    if endpoint and endpoint.endswith("/"):
        return endpoint[:-1]
    return endpoint


def get_query(url: str | None) -> str | None:
    return urlparse(url).query if url else None


def get_endpoint_with_query(url: str | None) -> str | None:
    if not (endpoint := get_endpoint(url)):
        return
    if not (query := get_query(url)):
        return endpoint
    return f"{endpoint}?{query}"


@cache
def get_query_params(url: str | None, only_initial_values: bool = True) -> dict:
    params: dict = parse_qs(urlparse(url).query) if url else None
    if not params:
        return {}
    if not only_initial_values:
        return params
    return {k: v[0] for k, v in params.items()}
