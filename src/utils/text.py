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


def clean_text(text: str) -> str:
    text = text.strip().replace("\n", "")
    while "  " in text:
        text = text.replace("  ", " ")
    return text
