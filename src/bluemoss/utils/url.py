from __future__ import annotations
from urllib.parse import urlparse, parse_qs


def get_base_domain(url: str | None) -> str | None:
    """
    Returns the base domain of the given @param url.
    Example:
        1) get_base_domain("https://www.google.com?search=python") -> "google.com"
        2) get_base_domain("https://www.products.apple.com?p=iphone") -> "apple.com"
        3) get_base_domain("https://www.sub1.sub2.example.com/about/team?type=engineer") -> "example.com"
        4) get_base_domain(None) -> None

    :rtype: str | None
    :return: The base-domain of the given @param url.
    """
    domain: str | None = get_domain(url)
    return '.'.join(domain.split('.')[-2:]) if domain else None


def get_domain(url: str | None) -> str | None:
    """
    Returns the full domain of the given @param url.
    Example:
        1) get_domain("https://www.google.com?search=python") -> "google.com"
        2) get_domain("https://www.products.apple.com?p=iphone") -> "products.apple.com"
        3) get_domain("https://www.sub1.sub2.example.com/about/team?type=engineer") -> "sub1.sub2.example.com"
        4) get_domain(None) -> None

    :rtype: str | None
    :return: The full domain of @param url.
    """
    url = url.strip() if url else None
    if not url:
        return None
    domain = urlparse(url).netloc
    return domain.replace('www.', '', 1)


def get_endpoint(url: str | None) -> str | None:
    """
    Returns the endpoint @param url.
    Example:
        1) get_endpoint("https://www.google.com?search=python") -> None
        2) get_endpoint("https://www.products.apple.com?p=iphone") -> None
        3) get_endpoint("https://www.sub1.sub2.example.com/about/team?type=engineer") -> "/about/team"
        4) get_endpoint(None) -> None

    :param url: The url to extract the base-domain from.
    :rtype: str | None
    :return: The endpoint of @param url.
    """
    url = url.strip() if url else None
    if not url:
        return None
    endpoint: str | None = urlparse(url).path if url else None
    if endpoint and endpoint.endswith('/'):
        endpoint = endpoint[:-1]
    return endpoint if endpoint else None


def get_url_query(url: str | None) -> str | None:
    """
    Returns the query-string of @param url.
    Example:
        1) get_url_query("https://www.google.com?search=python") -> "search=python"
        2) get_url_query("https://www.products.apple.com?p=iphone") -> "p=iphone"
        3) get_url_query("https://www.sub1.sub2.example.com/about/team?type=engineer") -> "type=engineer"
        4) get_url_query(None) -> None

    :rtype: str | None
    :return: The url-query-string of @param url.
    """
    url = url.strip() if url else None
    if not url:
        return None
    query: str = urlparse(url).query
    return query if query else None


def get_endpoint_with_query(url: str | None) -> str | None:
    """
    Returns the endpoint including query-string of @param url.
    Example:
        1) get_endpoint_with_query("https://www.google.com?search=python") -> "?search=python"
        2) get_endpoint_with_query("https://www.products.apple.com?p=iphone") -> "?p=iphone"
        3) get_endpoint_with_query("https://www.sub1.sub2.example.com/about/team?type=engineer")
                -> "/about/team?type=engineer"
        4) get_endpoint_with_query(None) -> None
        5) get_endpoint_with_query(

    :rtype: str | None
    :return: endpoint + query of @param url.
    """
    if not (endpoint := get_endpoint(url)):
        endpoint = ''
    if not (query := get_url_query(url)):
        query = ''
    if not endpoint and not query:
        return None
    if not query:
        return endpoint
    return f'{endpoint}?{query}'


def get_url_query_params(url: str | None) -> dict[str, list[str]]:
    """
    Returns the query-parameters of @param url as a dict.
    Example:
        1) get_endpoint_with_query("https://www.google.com?search=python") -> {"search": "python"}
        2) get_endpoint_with_query("https://www.products.apple.com?p=iphone") -> {"p": "iphone"}
        3) get_endpoint_with_query("https://www.example.com/team?type=engineer&page=2&type=manager")
                -> {"page": ["2"], "type": ["engineer", "manager"]}
        4) get_endpoint_with_query(None) -> None

    :rtype: dict
    :return: The query-parameters of @param url.
    """
    return parse_qs(urlparse(url).query) if url else {}


__all__ = [
    'get_base_domain',
    'get_domain',
    'get_endpoint',
    'get_url_query',
    'get_endpoint_with_query',
    'get_url_query_params',
]
