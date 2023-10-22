def get_infix(text: str, prefix: str, suffix: str) -> str | None:
    """ @return an infix within @param text given a specific prefix and a specific suffix. """
    if not text:
        return
    idx: int = text.find(prefix)
    if idx == -1:
        return
    res: str = text[idx+len(prefix):]
    if not suffix:
        return res
    idx = res.find(suffix)
    if idx == -1:
        return
    return res[:idx]


def clean_text(text: str | None) -> str | None:
    if text is None:
        return
    text = text.strip()
    while "  " in text:
        text = text.replace("  ", " ")
    while "\n " in text:
        text = text.strip().replace("\n ", "\n")
    while " \n" in text:
        text = text.strip().replace(" \n", "\n")
    while "\n\n" in text:
        text = text.strip().replace("\n\n", "\n")
    return text


__all__ = [
    "get_infix",
    "clean_text"
]
