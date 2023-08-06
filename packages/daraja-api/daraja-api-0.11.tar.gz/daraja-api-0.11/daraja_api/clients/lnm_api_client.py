import abc, json, base64, requests
from datetime import datetime
from daraja_api.auth import generate_token
from daraja_api.conf import AbstractConfig
from daraja_api.clients.abstract_api_client import AbstractApiClient
from daraja_api.exceptions import DarajaException
from daraja_api.utils import format_phone_number, base_url

class AbstractLNMApiClient(AbstractApiClient):

    @abc.abstractmethod
    def __init__(self, config:AbstractConfig):
        raise NotImplementedError('Not Implemented')

    @abc.abstractmethod
    def stk_push(self, phone_number, amount, account_reference, transaction_desc, callback_url):
        raise NotImplementedError('Not Implemented')

    @abc.abstractmethod
    def parse_stk_callback_response(self,body):
        raise NotImplementedError('Not Implemented')


class LNMApiClient(AbstractLNMApiClient):

    def __init__(self, conf:AbstractConfig):
        self.config=conf

    def stk_push(self, phone_number:str, amount:int,callback_url:str,
        account_reference:str="account", transaction_desc:str="desc",):

        if str(account_reference).strip() == '':
            raise DarajaException('Account reference cannot be blank')

        if str(transaction_desc).strip() == '':
            raise DarajaException('Transaction description cannot be blank')

        if not isinstance(amount, int):
            raise DarajaException('Amount must be an integer')

        if self.config.get_environment() == 'sandbox':
            business_short_code = self.config.get_express_shortcode()
        else:
            business_short_code = self.config.get_shortcode()
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        passkey = self.config.get_passkey()
        _p = (business_short_code + passkey + timestamp).encode()
        password =  base64.b64encode(_p).decode('utf-8')
        phone_number = format_phone_number(phone_number)
        party_a = phone_number
        party_b = business_short_code
        url = base_url(self.config) + '/mpesa/stkpush/v1/processrequest'
        data = {
            'BusinessShortCode': business_short_code,
            'Password': password,
            'Timestamp': timestamp,
            'TransactionType': 'CustomerPayBillOnline',
            'Amount': amount,
            'PartyA': party_a,
            'PartyB': party_b,
            'PhoneNumber': phone_number,
            'CallBackURL': callback_url,
            'AccountReference': account_reference,
            'TransactionDesc': transaction_desc
        }
        token = generate_token(self.config)
        headers = {
            'Authorization': 'Bearer ' + token,
            'Content-type': 'application/json'
        }
        r = requests.post(url, json=data, headers=headers)
        if r.status_code != 200:
            try:
                e = json.loads(r.text)
                errorMessage = e["errorMessage"]
                raise DarajaException("STK push failed: %s"%errorMessage)
            except json.decoder.JSONDecodeError:
                pass
            raise DarajaException('STK push failed, status_code: %s'%str(r.status_code))
        data = r.json()
        return data

    def parse_stk_callback_response(self, body):
        if type(body)==str:
            try:
                body = json.loads(body)
            except json.decoder.JSONDecodeError:
                raise DarajaException('Invalid Response body, unable to parse json')
        elif type(body) != dict:
            raise DarajaException('Response body must be json or a dict')
        data = {}
        stkCallback = body['Body']['stkCallback']
        data['ResultCode'] = stkCallback['ResultCode']
        data['ResultDesc'] = stkCallback['ResultDesc']
        data['MerchantRequestID'] = stkCallback['MerchantRequestID']
        data['CheckoutRequestID'] = stkCallback['CheckoutRequestID']
        data['meta']={}
        meta = stkCallback.get('CallbackMetadata')
        if meta:
            meta_items = meta.get('Item')
            for item in meta_items:
                data['meta'][item['Name']] = item.get('Value')
        return data
