# src/utils/totp_utils.py
import base64
import hmac
import random
import struct
from datetime import datetime
from typing import Tuple
from uuid import UUID

from archipy.configs.base_config import BaseConfig
from archipy.configs.config_template import AuthConfig
from archipy.helpers.utils.datetime_utils import DatetimeUtils


class TOTPUtils:
    """Utility class for TOTP (Time-based One-Time Password) operations."""

    @classmethod
    def generate_totp(cls, secret: str | UUID, auth_config: AuthConfig | None = None) -> Tuple[str, datetime]:
        """Generate a TOTP code using HMAC-SHA1."""
        configs = BaseConfig.global_config().AUTH if auth_config is None else auth_config

        # Convert secret to bytes if it's UUID
        if isinstance(secret, UUID):
            secret = str(secret)

        # Get current timestamp and calculate time step
        current_time = DatetimeUtils.get_epoch_time_now()
        time_step_counter = int(current_time / configs.TOTP_TIME_STEP)

        # Generate HMAC-SHA1 hash
        secret_bytes = str(secret).encode('utf-8')
        time_bytes = struct.pack('>Q', time_step_counter)
        hmac_obj = hmac.new(secret_bytes, time_bytes, configs.HASH_ALGORITHM.replace('HS', 'SHA'))
        hmac_result = hmac_obj.digest()

        # Get offset and truncate
        offset = hmac_result[-1] & 0xF
        truncated_hash = (
            ((hmac_result[offset] & 0x7F) << 24)
            | ((hmac_result[offset + 1] & 0xFF) << 16)
            | ((hmac_result[offset + 2] & 0xFF) << 8)
            | (hmac_result[offset + 3] & 0xFF)
        )

        # Generate TOTP code
        totp_code = str(truncated_hash % (10**configs.TOTP_LENGTH)).zfill(configs.TOTP_LENGTH)

        # Calculate expiration time
        expires_in = DatetimeUtils.get_datetime_after_given_datetime_or_now(seconds=configs.TOTP_EXPIRES_IN)

        return totp_code, expires_in

    @classmethod
    def verify_totp(cls, secret: str | UUID, totp_code: str, auth_config: AuthConfig | None = None) -> bool:
        """Verify a TOTP code."""
        configs = BaseConfig.global_config().AUTH if auth_config is None else auth_config

        if not totp_code.isdigit():
            return False

        current_time = DatetimeUtils.get_epoch_time_now()

        # Check codes within verification window
        for i in range(-configs.TOTP_VERIFICATION_WINDOW, configs.TOTP_VERIFICATION_WINDOW + 1):
            time_step_counter = int(current_time / configs.TOTP_TIME_STEP) + i

            secret_bytes = str(secret).encode('utf-8')
            time_bytes = struct.pack('>Q', time_step_counter)
            hmac_obj = hmac.new(secret_bytes, time_bytes, configs.HASH_ALGORITHM.replace('HS', 'SHA'))
            hmac_result = hmac_obj.digest()

            offset = hmac_result[-1] & 0xF
            truncated_hash = (
                ((hmac_result[offset] & 0x7F) << 24)
                | ((hmac_result[offset + 1] & 0xFF) << 16)
                | ((hmac_result[offset + 2] & 0xFF) << 8)
                | (hmac_result[offset + 3] & 0xFF)
            )

            computed_totp = str(truncated_hash % (10 ** len(totp_code))).zfill(len(totp_code))

            if hmac.compare_digest(totp_code, computed_totp):
                return True

        return False

    @staticmethod
    def generate_secret_key_for_totp(auth_config: AuthConfig | None = None) -> str:
        """Generate a random secret key for TOTP initialization."""
        configs = BaseConfig.global_config().AUTH if auth_config is None else auth_config

        random_bytes = random.randbytes(configs.SALT_LENGTH)
        master_key = configs.TOTP_SECRET_KEY.get_secret_value().encode('utf-8')

        # Use HMAC with master key for additional security
        hmac_obj = hmac.new(master_key, random_bytes, configs.HASH_ALGORITHM.replace('HS', 'SHA'))
        return base64.b32encode(hmac_obj.digest()).decode('utf-8')
