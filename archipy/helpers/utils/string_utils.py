import re
from re import compile

from archipy.helpers.utils.string_utils_constants import StringUtilsConstants


class StringUtils(StringUtilsConstants):
    """String utilities for text normalization and cleaning."""

    @classmethod
    def remove_arabic_vowels(cls, text: str) -> str:
        """Remove Arabic vowels from text."""
        return text.translate(cls.arabic_vowel_translate_table)

    @classmethod
    def normalize_persian_chars(cls, text: str) -> str:
        """Normalize Persian characters."""
        text = text.translate(cls.alphabet_akoolad_alef_translate_table)
        text = text.translate(cls.alphabet_alef_translate_table)
        text = text.translate(cls.alphabet_be_translate_table)
        text = text.translate(cls.alphabet_pe_translate_table)
        text = text.translate(cls.alphabet_te_translate_table)
        text = text.translate(cls.alphabet_se_translate_table)
        text = text.translate(cls.alphabet_jim_translate_table)
        text = text.translate(cls.alphabet_che_translate_table)
        text = text.translate(cls.alphabet_he_translate_table)
        text = text.translate(cls.alphabet_khe_translate_table)
        text = text.translate(cls.alphabet_dal_translate_table)
        text = text.translate(cls.alphabet_zal_translate_table)
        text = text.translate(cls.alphabet_re_translate_table)
        text = text.translate(cls.alphabet_ze_translate_table)
        text = text.translate(cls.alphabet_zhe_translate_table)
        text = text.translate(cls.alphabet_sin_translate_table)
        text = text.translate(cls.alphabet_shin_translate_table)
        text = text.translate(cls.alphabet_sad_translate_table)
        text = text.translate(cls.alphabet_zad_translate_table)
        text = text.translate(cls.alphabet_ta_translate_table)
        text = text.translate(cls.alphabet_za_translate_table)
        text = text.translate(cls.alphabet_eyn_translate_table)
        text = text.translate(cls.alphabet_gheyn_translate_table)
        text = text.translate(cls.alphabet_fe_translate_table)
        text = text.translate(cls.alphabet_ghaf_translate_table)
        text = text.translate(cls.alphabet_kaf_translate_table)
        text = text.translate(cls.alphabet_gaf_translate_table)
        text = text.translate(cls.alphabet_lam_translate_table)
        text = text.translate(cls.alphabet_mim_translate_table)
        text = text.translate(cls.alphabet_nun_translate_table)
        text = text.translate(cls.alphabet_vav_translate_table)
        text = text.translate(cls.alphabet_ha_translate_table)
        text = text.translate(cls.alphabet_ye_translate_table)
        return text

    @classmethod
    def normalize_punctuation(cls, text: str) -> str:
        """Normalize punctuation marks."""
        text = text.translate(cls.punctuation_translate_table1)
        text = text.translate(cls.punctuation_translate_table2)
        text = text.translate(cls.punctuation_translate_table3)
        text = text.translate(cls.punctuation_translate_table4)
        text = text.translate(cls.punctuation_translate_table5)
        text = text.translate(cls.punctuation_translate_table6)
        text = text.translate(cls.punctuation_translate_table7)
        text = text.translate(cls.punctuation_translate_table8)
        text = text.translate(cls.punctuation_translate_table9)
        text = text.translate(cls.punctuation_translate_table10)
        text = text.translate(cls.punctuation_translate_table11)
        text = text.translate(cls.punctuation_translate_table12)
        text = text.translate(cls.punctuation_translate_table13)
        return text

    @classmethod
    def normalize_numbers(cls, text: str) -> str:
        """Normalize numbers to English format."""
        text = text.translate(cls.number_zero_translate_table)
        text = text.translate(cls.number_one_translate_table)
        text = text.translate(cls.number_two_translate_table)
        text = text.translate(cls.number_three_translate_table)
        text = text.translate(cls.number_four_translate_table)
        text = text.translate(cls.number_five_translate_table)
        text = text.translate(cls.number_six_translate_table)
        text = text.translate(cls.number_seven_translate_table)
        text = text.translate(cls.number_eight_translate_table)
        return text.translate(cls.number_nine_translate_table)

    @classmethod
    def clean_spacing(cls, text: str) -> str:
        """Clean up spacing issues in text."""
        text = text.replace('\u200c', ' ')  # ZWNJ
        text = text.replace('\xa0', ' ')  # NBSP

        for pattern, repl in cls.character_refinement_patterns:
            text = pattern.sub(repl, text)

        return text

    @classmethod
    def normalize_punctuation_spacing(cls, text: str) -> str:
        """Apply proper spacing around punctuation marks."""
        for pattern, repl in cls.punctuation_spacing_patterns:
            text = pattern.sub(repl, text)
        return text

    @classmethod
    def remove_punctuation_marks(cls, text: str) -> str:
        """Remove punctuation marks from text."""
        return text.translate(cls.punctuation_persian_marks_to_space_translate_table)

    @classmethod
    def mask_urls(cls, text: str, mask: str | None = None) -> str:
        """Mask URLs in text."""
        mask = mask or "MASK_URL"
        return compile(r'https?://\S+|www\.\S+').sub(f' {mask} ', text)

    @classmethod
    def mask_emails(cls, text: str, mask: str | None = None) -> str:
        """Mask email addresses in text."""
        mask = mask or "MASK_EMAIL"
        return compile(r'\S+@\S+\.\S+').sub(f' {mask} ', text)

    @classmethod
    def mask_phones(cls, text: str, mask: str | None = None) -> str:
        """Mask phone numbers in text."""
        mask = mask or "MASK_PHONE"
        return compile(r'(?:\+98|0)?(?:\d{3}\s*?\d{3}\s*?\d{4})').sub(f' {mask} ', text)

    @classmethod
    def convert_english_number_to_persian(cls, text: str) -> str:
        """Convert English numbers to Persian numbers."""
        table = {
            48: 1776,  # 0
            49: 1777,  # 1
            50: 1778,  # 2
            51: 1779,  # 3
            52: 1780,  # 4
            53: 1781,  # 5
            54: 1782,  # 6
            55: 1783,  # 7
            56: 1784,  # 8
            57: 1785,  # 9
            44: 1548,  # ,
        }
        return text.translate(table)

    @classmethod
    def convert_numbers_to_english(cls, text: str) -> str:
        """Convert Persian/Arabic numbers to English numbers."""
        table = {
            1776: 48,  # 0
            1777: 49,  # 1
            1778: 50,  # 2
            1779: 51,  # 3
            1780: 52,  # 4
            1781: 53,  # 5
            1782: 54,  # 6
            1783: 55,  # 7
            1784: 56,  # 8
            1785: 57,  # 9
            1632: 48,  # 0
            1633: 49,  # 1
            1634: 50,  # 2
            1635: 51,  # 3
            1636: 52,  # 4
            1637: 53,  # 5
            1638: 54,  # 6
            1639: 55,  # 7
            1640: 56,  # 8
            1641: 57,  # 9
        }
        return text.translate(table)

    @classmethod
    def convert_add_3digit_delimiter(cls, value: int) -> str:
        """Add a thousand separators to numbers."""
        return f"{value:,}" if isinstance(value, int) else value

    @classmethod
    def remove_emoji(cls, text: str) -> str:
        """Remove emoji characters from text."""
        emoji_pattern = compile(
            pattern="["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F1E0-\U0001F1FF"  # flags (iOS)
            "\U00002702-\U000027B0"
            "\U000024C2-\U0001F251"
            "\U0001f926-\U0001f937"
            "\U00010000-\U0010ffff"
            "\u2640-\u2642"
            "\u2600-\u2B55"
            "\u23cf\u23e9\u231a\u3030\ufe0f\u2069\u2066\u2068\u2067"
            "]+",
            flags=re.UNICODE,
        )
        return emoji_pattern.sub(r"", text)

    @classmethod
    def replace_currencies_with_mask(cls, text: str, mask: str | None = None) -> str:
        mask = mask or "MASK_CURRENCIES"
        """Mask currency symbols and amounts."""
        currency_pattern = compile(r"(\\|zł|£|\$|₡|₦|¥|₩|₪|₫|€|₱|₲|₴|₹|﷼)+")
        return currency_pattern.sub(f" {mask} ", text)

    @classmethod
    def replace_numbers_with_mask(cls, text: str, mask: str | None = None) -> str:
        """Mask numbers in text."""
        mask = mask or "MASK_NUMBERS"
        numbers = re.findall("[0-9]+", text)
        for number in sorted(numbers, key=len, reverse=True):
            text = text.replace(number, f" {mask} ")
        return text

    @classmethod
    def is_string_none_or_empty(cls, text: str) -> bool:
        """Check if string is None or empty."""
        return text is None or isinstance(text, str) and not text.strip()

    @classmethod
    def normalize_persian_text(
        cls,
        text: str,
        *,
        remove_vowels: bool = True,
        normalize_punctuation: bool = True,
        normalize_numbers: bool = True,
        normalize_persian_chars: bool = True,
        mask_urls: bool = False,
        mask_emails: bool = False,
        mask_phones: bool = False,
        mask_currencies: bool = False,
        mask_all_numbers: bool = False,
        remove_emojis: bool = False,
        url_mask: str | None = None,
        email_mask: str | None = None,
        phone_mask: str | None = None,
        currency_mask: str | None = None,
        number_mask: str | None = None,
        clean_spacing: bool = True,
        remove_punctuation: bool = False,
        normalize_punctuation_spacing: bool = False,
    ) -> str:
        """Normalize text with configurable options."""
        if not text:
            return text

        # Remove emojis if requested
        if remove_emojis:
            text = cls.remove_emoji(text)

        # Apply normalizations
        if remove_vowels:
            text = cls.remove_arabic_vowels(text)
        if normalize_persian_chars:
            text = cls.normalize_persian_chars(text)
        if normalize_punctuation:
            text = cls.normalize_punctuation(text)
        if remove_punctuation:
            text = cls.remove_punctuation_marks(text)
        if normalize_numbers:
            text = cls.normalize_numbers(text)

        # Apply masking
        if mask_urls:
            text = cls.mask_urls(text, mask=url_mask)
        if mask_emails:
            text = cls.mask_emails(text, mask=email_mask)
        if mask_phones:
            text = cls.mask_phones(text, mask=phone_mask)
        if mask_currencies:
            text = cls.replace_currencies_with_mask(text, mask=currency_mask)
        if mask_all_numbers:
            text = cls.replace_numbers_with_mask(text, mask=number_mask)

        if clean_spacing:
            text = cls.clean_spacing(text)
        if normalize_punctuation_spacing:
            text = cls.normalize_punctuation_spacing(text)

        return text.strip()
