from enum import Enum

from luffy.api.src.common.constants.aws_constants import AwsConstants
from luffy.api.src.common.utils.decoder_util import decode_val


class AwsEnum(Enum):
    ACCESS_KEY_ID = decode_val(AwsConstants.aws_access_key_id)
    ACCESS_KEY = decode_val(AwsConstants.aws_secret_access_key)
