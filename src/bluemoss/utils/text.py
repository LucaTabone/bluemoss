from __future__ import annotations
from lxml.html import HtmlElement


def get_infix(text: str, prefix: str, suffix: str) -> str | None:
    """
    Compute the first string-infix in @param text that sits between @param prefix and @param suffix.
    If either one of @param prefix and @param suffix is not found in the text, return None.
    If both @param prefix and @param suffix are present in @param text, the returned string-infix would start
    with the first character after @param prefix ends and ends with the first character before @param suffix starts.

    Example 1: get_infix(text='Hello World!', prefix='ll', suffix='ld') returns 'o Wor'
    Example 2: get_infix(text='Hello World!', prefix='Hey', suffix='World!') returns None
    Example 3: get_infix(text='Hello World!', prefix='Hello', suffix='Darling') returns None

    :param text: String to be searched
    :param prefix: Prefix to be searched
    :param suffix: Suffix to be searched
    :rtype: str | None
    :return: First string-infix in @param text that sits between @param prefix and @param suffix.
    """
    if not text:
        return None
    idx: int = text.find(prefix)
    if idx == -1:
        return None
    res: str = text[idx + len(prefix) :]
    idx = res.find(suffix)
    if idx == -1:
        return None
    return res[:idx]


def clean_text(text: str) -> str:
    """
    Edit the given @param text by
        - removing leading and trailing spaces
        - replacing multiple spaces with just one space
        - replacing any linebreaks + leading space with a linebreak
        - replacing any linebreaks + trailing space with a linebreak
        - replacing multiple newlines with just one newline

    :param text: Text to be edited.
    :rtype: str | None
    :return: The updated text.
    """
    if not text:
        return ''
    text = text.strip()
    while '  ' in text:
        text = text.replace('  ', ' ')
    while '\n ' in text:
        text = text.strip().replace('\n ', '\n')
    while ' \n' in text:
        text = text.strip().replace(' \n', '\n')
    while '\n\n\n' in text:
        text = text.strip().replace('\n\n\n', '\n\n')
    return text


def lxml_etree_text_content(tag: HtmlElement) -> str:
    return clean_text(tag.xpath('string(.)'))


__all__ = ['get_infix', 'clean_text', 'lxml_etree_text_content']
