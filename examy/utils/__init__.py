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

province_codes = {
    'ADANA': '1',
    'ADIYAMAN': '2',
    'AFYONKARAHİSAR': '3',
    'AĞRI': '4',
    'AMASYA': '5',
    'ANKARA': '6',
    'ANTALYA': '7',
    'ARTVİN': '8',
    'AYDIN': '9',
    'BALIKESİR': '10',
    'BİLECİK': '11',
    'BİNGÖL': '12',
    'BİTLİS': '13',
    'BOLU': '14',
    'BURDUR': '15',
    'BURSA': '16',
    'ÇANAKKALE': '17',
    'ÇANKIRI': '18',
    'ÇORUM': '19',
    'DENİZLİ': '20',
    'DIYARBAKIR': '21',
    'EDİRNE': '22',
    'ELAZIĞ': '23',
    'ERZİNCAN': '24',
    'ERZURUM': '25',
    'ESKİŞEHİR': '26',
    'GAZİANTEP': '27',
    'GIRESUN': '28',
    'GÜMÜŞHANE': '29',
    'HAKKARİ': '30',
    'HATAY': '31',
    'ISPARTA': '32',
    'MERSİN': '33',
    'İSTANBUL': '34',
    'İZMİR': '35',
    'KARS': '36',
    'KASTAMONU': '37',
    'KAYSERİ': '38',
    'KIRKLARELI': '39',
    'KIRŞEHİR': '40',
    'KOCAELİ': '41',
    'KONYA': '42',
    'KÜTAHYA': '43',
    'MALATYA': '44',
    'MANİSA': '45',
    'KAHRAMANMARAŞ': '46',
    'MARDİN': '47',
    'MUĞLA': '48',
    'MUŞ': '49',
    'NEVŞEHİR': '50',
    'NİĞDE': '51',
    'ORDU': '52',
    'RİZE': '53',
    'SAKARYA': '54',
    'SAMSUN': '55',
    'SİİRT': '56',
    'SİNOP': '57',
    'SİVAS': '58',
    'TEKİRDAĞ': '59',
    'TOKAT': '60',
    'TRABZON': '61',
    'TUNCELİ': '62',
    'ŞANLIURFA': '63',
    'UŞAK': '64',
    'VAN': '65',
    'YOZGAT': '66',
    'ZONGULDAK': '67',
    'AKSARAY': '68',
    'BAYBURT': '69',
    'KARAMAN': '70',
    'KIRIKKALE': '71',
    'BATMAN': '72',
    'ŞIRNAK': '73',
    'BARTIN': '74',
    'ARDAHAN': '75',
    'IĞDIR': '76',
    'YALOVA': '77',
    'KARABÜK': '78',
    'KİLİS': '79',
    'OSMANİYE': '80',
    'DÜZCE': '81'
}
