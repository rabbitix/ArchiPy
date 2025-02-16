# src/helpers/password_helper.py
import hashlib
import hmac
import os
import random
import string
from base64 import b64decode, b64encode

from archipy.configs.base_config import BaseConfig
from archipy.configs.config_template import AuthConfig


class PasswordUtils:

    @staticmethod
    def hash_password(password: str, auth_config: AuthConfig | None = None) -> str:
        """
        Hash a password using PBKDF2 with SHA256
        Returns: base64 encoded string of "salt:hash"
        """

        configs = BaseConfig.global_config().AUTH if auth_config is None else auth_config
        salt = os.urandom(configs.SALT_LENGTH)
        pw_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, configs.HASH_ITERATIONS)

        # Combine salt and hash, encode in base64
        combined = b64encode(salt + pw_hash).decode('utf-8')
        return combined

    @staticmethod
    def verify_password(password: str, stored_password: str, auth_config: AuthConfig | None = None) -> bool:
        """
        Verify a password against a stored hash
        """
        try:
            configs = BaseConfig.global_config().AUTH if auth_config is None else auth_config

            # Decode the stored password
            decoded = b64decode(stored_password.encode('utf-8'))
            salt = decoded[: configs.SALT_LENGTH]
            stored_hash = decoded[configs.SALT_LENGTH :]

            # Hash the provided password with the same salt
            pw_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, configs.HASH_ITERATIONS)

            # Compare in constant time to prevent timing attacks
            return hmac.compare_digest(pw_hash, stored_hash)
        except Exception:
            return False

    @staticmethod
    def validate_password(password: str, auth_config: AuthConfig | None = None) -> None:
        """
        Validate a password against the password policy.

        Args:
            password: Password to validate
            auth_config: Password policy configuration

        Returns:
            None
        """
        configs = BaseConfig.global_config().AUTH if auth_config is None else auth_config
        errors = []

        if len(password) < configs.MIN_LENGTH:
            errors.append(f'Password must be at least {configs.MIN_LENGTH} characters long.')

        if configs.REQUIRE_DIGIT and not any(char.isdigit() for char in password):
            errors.append('Password must contain at least one digit.')

        if configs.REQUIRE_LOWERCASE and not any(char.islower() for char in password):
            errors.append('Password must contain at least one lowercase letter.')

        if configs.REQUIRE_UPPERCASE and not any(char.isupper() for char in password):
            errors.append('Password must contain at least one uppercase letter.')

        if configs.REQUIRE_SPECIAL and not any(char in configs.SPECIAL_CHARACTERS for char in password):
            errors.append(f'Password must contain at least one special character: {configs.SPECIAL_CHARACTERS}')

        if errors:
            raise ValueError('; '.join(errors))

    @staticmethod
    def generate_password(auth_config: AuthConfig | None = None) -> str:
        """
        Generate a random password that meets the policy requirements.

        Args:
            auth_config: Password policy configuration

        Returns:
            str: Generated password
        """
        configs = BaseConfig.global_config().AUTH if auth_config is None else auth_config

        lowercase_chars = string.ascii_lowercase
        uppercase_chars = string.ascii_uppercase
        digit_chars = string.digits
        special_chars = ''.join(configs.SPECIAL_CHARACTERS)

        # Initialize with required characters
        password_chars = []
        if configs.REQUIRE_LOWERCASE:
            password_chars.append(random.choice(lowercase_chars))
        if configs.REQUIRE_UPPERCASE:
            password_chars.append(random.choice(uppercase_chars))
        if configs.REQUIRE_DIGIT:
            password_chars.append(random.choice(digit_chars))
        if configs.REQUIRE_SPECIAL:
            password_chars.append(random.choice(special_chars))

        # Calculate remaining length
        remaining_length = max(0, configs.MIN_LENGTH - len(password_chars))

        # Add random characters to meet minimum length
        all_chars = lowercase_chars + uppercase_chars + digit_chars + special_chars
        password_chars.extend(random.choices(all_chars, k=remaining_length))

        # Shuffle the password characters
        random.shuffle(password_chars)

        return ''.join(password_chars)

    @classmethod
    def validate_password_history(
        cls,
        new_password: str,
        password_history: list[str],
        auth_config: AuthConfig | None = None,
    ) -> None:
        """
        Validate a new password against password history.

        Args:
            new_password: New password to validate
            password_history: List of previous password hashes
            auth_config: Auth configuration

        Returns:
            None
        """
        configs = BaseConfig.global_config().AUTH if auth_config is None else auth_config
        errors = []
        # First validate against password policy
        cls.validate_password(new_password, configs)

        # Check password history
        if any(
            cls.verify_password(new_password, old_password, configs)
            for old_password in password_history[-configs.PASSWORD_HISTORY_SIZE :]
        ):
            errors.append("Password has been used recently")

        if errors:
            raise ValueError('; '.join(errors))
