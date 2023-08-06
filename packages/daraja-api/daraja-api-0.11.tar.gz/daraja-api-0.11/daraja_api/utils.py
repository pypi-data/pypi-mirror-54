import phonenumbers
from daraja_api.conf import AbstractConfig
from daraja_api.exceptions import DarajaException

def format_phone_number(phone_number:str, format='E164'):
        try:
            phone_number = phonenumbers.parse(phone_number,"KE")            
            if not phonenumbers.is_valid_number(phone_number):
                raise DarajaException("Invalid Phone Number: "+phone_number)

        except Exception as e:
            raise DarajaException(str(e))
        if format=="E164":
            p = phonenumbers.format_number(phone_number, 
                phonenumbers.PhoneNumberFormat.E164)
            return p[1:]
        elif format=="national":
            return phonenumbers.format_number(phone_number,
            phonenumbers.PhoneNumberFormat.national)

def base_url(config:AbstractConfig):
    environment = config.get_environment()
    urls = {"sandbox":"https://sandbox.safaricom.co.ke",
        "production":"https://api.safaricom.co.ke"}
    return urls[environment]

