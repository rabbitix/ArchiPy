import re

from archipy.helpers.utils.datetime_utils import DatetimeUtils
from archipy.helpers.utils.exception_utils import ExceptionUtils
from archipy.helpers.utils.file_utils import FileUtils
from archipy.helpers.utils.jwt_utils import JWTUtils
from archipy.helpers.utils.password_utils import PasswordUtils
from archipy.helpers.utils.string_utils import StringUtils
from archipy.helpers.utils.totp_utils import TOTPUtils
from archipy.models.exceptions import (
    InvalidLandlineNumberException,
    InvalidNationalCodeException,
    InvalidPhoneNumberException,
)


class BaseUtils(ExceptionUtils, DatetimeUtils, PasswordUtils, JWTUtils, TOTPUtils, FileUtils, StringUtils):
    @staticmethod
    def sanitize_iranian_landline_or_phone_number(landline_or_phone_number: str) -> str:
        """Remove non-numeric characters from the phone number and handle country code."""
        # Remove non-numeric characters
        cleaned_number = re.sub(r'\D', '', landline_or_phone_number)

        # Standardize international format to local Iran format
        if cleaned_number.startswith("0098"):  # Handles "0098"
            cleaned_number = "0" + cleaned_number[4:]  # Replace "0098" with "0"
        elif cleaned_number.startswith("98"):  # Handles "+98"
            cleaned_number = "0" + cleaned_number[2:]  # Replace "98" with "0"

        # Ensure mobile numbers start with '09'
        if len(cleaned_number) == 10 and cleaned_number.startswith("9"):
            cleaned_number = "0" + cleaned_number  # Convert "9123456789" → "09123456789"

        return cleaned_number

    @classmethod
    def validate_iranian_phone_number(cls, phone_number: str) -> None:
        # Sanitize the input to remove spaces, dashes, or other non-numeric characters
        sanitized_number = cls.sanitize_iranian_landline_or_phone_number(phone_number)
        # Define the regular expression pattern for Iranian phone numbers
        iranian_mobile_pattern = re.compile(r'^09\d{9}$')  # Mobile numbers

        # Check if the phone number matches either mobile or landline pattern
        if not iranian_mobile_pattern.match(sanitized_number):
            raise InvalidPhoneNumberException(phone_number)

    @classmethod
    def validate_iranian_landline_number(cls, landline_number: str) -> None:
        # Sanitize the input to remove spaces, dashes, or other non-numeric characters
        sanitized_number = cls.sanitize_iranian_landline_or_phone_number(landline_number)
        # Landline examples: `0` + 2 to 4-digit area code + 7 to 8-digit local number
        iranian_landline_pattern = re.compile(r'^0\d{2,4}\d{7,8}$')

        if not iranian_landline_pattern.match(sanitized_number):
            raise InvalidLandlineNumberException(landline_number)

    @classmethod
    def validate_iranian_national_code_pattern(cls, national_code: str) -> str:
        """
        Validates an Iranian National ID number using the official algorithm.
        To see how the algorithm works, see http://www.aliarash.com/article/codemeli/codemeli.htm

        The algorithm works by:
        1. Checking if the ID is exactly 10 digits
        2. Multiplying each digit (except the last) by its position weight
        3. Summing these products
        4. Calculating the remainder when divided by 11
        5. Comparing the check digit based on specific rules

        Args:
            national_code: A string containing the national ID to validate

        Returns:
            The validated national ID string

        Raises:
            JibitNationalIDInvalidException: If the ID is invalid due to length or checksum
        """

        def _validate_length(national_code: str) -> None:
            if not len(national_code) == 10:
                raise InvalidNationalCodeException(national_code)

        def _calculate_weighted_sum(national_code: str) -> int:
            return sum(int(digit) * (10 - i) for i, digit in enumerate(national_code[:-1]))

        def _get_checksums(national_code: str) -> tuple[int, int]:
            weighted_sum = _calculate_weighted_sum(national_code)
            remainder = weighted_sum % 11

            calculated_checksum = remainder if remainder < 2 else 11 - remainder
            actual_checksum = int(national_code[-1])

            return calculated_checksum, actual_checksum

        _validate_length(national_code)
        calculated_checksum, actual_checksum = _get_checksums(national_code)
        if calculated_checksum != actual_checksum:
            raise InvalidNationalCodeException(national_code)
        return national_code
