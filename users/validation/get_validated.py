from logMaker.log import logger
from users.models import Accounts
from datetime import timedelta, datetime
from users.constants import CommonConstants
from common_utilities.aes_encryption import AESCipher


class Validator:
    @classmethod
    def validate_login(cls, request):
        valid_flag = False
        message = ""
        cookie = ""
        try:
            request_json = request.data
            user_data = Accounts.objects.filter(email_id=request_json["email"])
            for user in user_data:
                try:
                    decrypted_password = AESCipher(key="I Seek Vengeance").decrypt(user.password)
                    if decrypted_password == request_json[CommonConstants.password]:
                        valid_flag = True
                        cookie = cls.create_cookie(email_id=user.email_id)
                    else:
                        message = "password_mismatch"
                except Exception as e:
                    logger.error("Failed to login : {}".format(str(e)))

        except Exception as e:
            logger.exception(f"Exception when logging in {e}")
        return valid_flag, message, cookie

    @staticmethod
    def create_cookie(email_id):
        key = "VU5BVVRIT1JJWkVEQUNDRVNTREVOSUVE"
        valid_till = (datetime.now() + timedelta(minutes=30)).strftime("%d_%m_%Y_%H_%M")
        cookie_str = email_id + "^" + valid_till
        return AESCipher(key).encrypt(cookie_str)

    @staticmethod
    def decode_cookie(encoded_str):
        key = "VU5BVVRIT1JJWkVEQUNDRVNTREVOSUVE"
        return AESCipher(key).decrypt(encoded_str)

    @classmethod
    def cookie_validator(cls, encoded_string):
        flag = False
        email_id = ""
        decoded_string = cls.decode_cookie(encoded_string)
        decoded_string = decoded_string.split("^")
        if decoded_string:
            minutes_difference = int(round((datetime.strptime(decoded_string[1], "%d_%m_%Y_%H_%M") - datetime.now()).total_seconds() / 60))
            if 0 < minutes_difference <= 30:
                email_id = decoded_string[0]
                flag = True
        return flag, email_id