class TurkishStr:
    """Handle string upper/lower conversions in Turkish.

    I/i conversions is the key point of this class.
    """
    REPLACED_CHARS: dict[str, dict[str, str]] = {
        "upper": {"i": "İ", "ı": "I"},
        "lower": {"I": "ı", "İ": "i"},
    }

    @classmethod
    def upper(cls, string: str) -> str:
        """Convert a string to uppercase, in a Turkish way.

        Args:
            string: The string to convert.

        Returns:
            The converted string.
        """
        for old, new in cls.REPLACED_CHARS["upper"].items():
            string = string.replace(old, new)
        return string.upper()

    @classmethod
    def lower(cls, string: str) -> str:
        """Convert a string to lowercase, in a Turkish way.

        Args:
            string: The string to convert.

        Returns:
            The converted string.
        """
        for old, new in cls.REPLACED_CHARS["lower"].items():
            string = string.replace(old, new)
        return string.lower()


def turkish_str_to_float(text: str) -> float:
    """Convert a turkish float string to float.

    In Turkish, the floating point seperator is a comma, instead of a dot.
    This function handles the conversion such strings to float.

    Args:
        text: A turkish float string.

    Returns:
        A floating point value, the one represented in the `text` argument.
    """
    return float(text.replace(",", "."))
