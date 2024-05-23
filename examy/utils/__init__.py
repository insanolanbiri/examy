class TurkishStr:
    REPLACED_CHARS: dict[str, dict[str, str]] = {
        "upper": {"i": "İ", "ı": "I"},
        "lower": {"I": "ı", "İ": "i"},
    }

    @classmethod
    def upper(cls, string: str) -> str:
        for old, new in cls.REPLACED_CHARS["upper"].items():
            string = string.replace(old, new)
        return string.upper()

    @classmethod
    def lower(cls, string: str) -> str:
        for old, new in cls.REPLACED_CHARS["lower"].items():
            string = string.replace(old, new)
        return string.lower()


def turkish_str_to_float(text: str) -> float:
    return float(text.replace(",", "."))
