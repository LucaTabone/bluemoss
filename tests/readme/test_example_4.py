from src.bluemoss import Node, Range, Ex, scrape
from ..constants import README_EXAMPLE_HTML as HTML


def get_company_id(hrefs: list[str]) -> list[str]:
    return [href.split('=')[-1] for href in hrefs]


for node in [
    Node('a', filter=Range(1), extract=Ex.HREF, transform=get_company_id),
    Node('a', filter=Range(1), extract='href', transform=get_company_id),
    Node('a/@href', filter=Range(1), transform=get_company_id),
]:
    assert scrape(node, HTML) == ['google', 'tesla', 'deepmind']
