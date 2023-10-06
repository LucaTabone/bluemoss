from urllib.parse import urlparse


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
    return urlparse(url).path if url else None


def get_query(url: str | None) -> str | None:
    return urlparse(url).query if url else None


def get_endpoint_with_query(url: str | None) -> str | None:
    if not (endpoint := get_endpoint(url)):
        return
    if not (query := get_query(url)):
        return endpoint
    return f"{endpoint}?{query}"
