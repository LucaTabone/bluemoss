from urllib.parse import urlparse, parse_qs


def get_base_domain(url: str | None) -> str | None:
    """ @return: the top-level-domain of the given @param url. """
    domain: str | None = get_domain(url)
    return ".".join(domain.split(".")[-2:]) if domain else None


def get_domain(url: str | None) -> str | None:
    """ @return: the full domain of the given @param url. """
    url: str | None = url.strip() if url else None
    if not url:
        return
    domain = urlparse(url).netloc
    return domain.replace("www.", "", 1)


def get_endpoint(url: str | None) -> str | None:
    """ @return: the endpoint of the given @param url ."""
    url: str | None = url.strip() if url else None
    if not url:
        return
    endpoint: str | None = urlparse(url).path if url else None
    if endpoint and endpoint.endswith("/"):
        endpoint = endpoint[:-1]
    if endpoint:
        return endpoint


def get_url_query(url: str | None) -> str | None:
    url: str | None = url.strip() if url else None
    if not url:
        return
    query: str = urlparse(url).query
    return query if query else None


def get_endpoint_with_query(url: str | None) -> str | None:
    if not (endpoint := get_endpoint(url)):
        return
    if not (query := get_url_query(url)):
        return endpoint
    return f"{endpoint}?{query}"


def get_url_query_params(url: str | None) -> dict:
    return parse_qs(urlparse(url).query) if url else {}


__all__ = [
    "get_base_domain",
    "get_domain",
    "get_endpoint",
    "get_url_query",
    "get_endpoint_with_query",
    "get_url_query_params"
]
