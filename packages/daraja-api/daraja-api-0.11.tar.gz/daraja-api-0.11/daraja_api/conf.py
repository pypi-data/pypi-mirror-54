import abc
from daraja_api.exceptions import DarajaException

class AbstractConfig(abc.ABC):

    @abc.abstractmethod
    def get_consumer_key(self)->str:
        raise NotImplementedError('Not implemented error')

    @abc.abstractmethod
    def get_consumer_secret(self)->str:
        raise NotImplementedError('Not implemented error')

    @abc.abstractmethod
    def get_environment(self)->str:
        raise NotImplementedError('Not implemented error')

    @abc.abstractmethod
    def get_shortcode(self)->str:
        raise NotImplementedError('Not implemented error')

    @abc.abstractmethod
    def get_express_shortcode(self)->str:
        raise NotImplementedError('Not implemented error')

    @abc.abstractmethod
    def get_shortcode_type(self)->str:
        raise NotImplementedError('Not implemented error')

    @abc.abstractmethod
    def get_passkey(self)->str:
        raise NotImplementedError('Not implemented error')

class ConfigFromObject(AbstractConfig):
    
    def __init__(self,obj):
        self.obj=obj
        required_attrs=['MPESA_ENVIRONMENT','MPESA_CONSUMER_KEY','MPESA_CONSUMER_SECRET']
        for i in required_attrs:
            self.get_attr_from_obj(i)
        allowed_env = ['sandbox','production']
        env = self.obj.get('MPESA_ENVIRONMENT') if type(self.obj)==dict\
                else getattr(obj,'MPESA_ENVIRONMENT')
        if env not in allowed_env:
            raise DarajaException('Allowed environments values: '+','.join(allowed_env))
        
    def get_attr_from_obj(self, attr):
        try:
            if type(self.obj)==object:
                _v=getattr(self.obj,attr)
            elif type(self.obj)==dict:
                _v=self.obj.get(attr)
            else:
                raise DarajaException('Invalid Config Object Type')
            if _v==None:
                raise AttributeError()
            if type(_v) != str or _v=='':
                raise DarajaException('{attr} must be a string, cannot be empty'.format(attr=attr))
            return _v
        except AttributeError:
            raise DarajaException('{attr} is required'.format(attr=attr))

    def get_consumer_key(self)->str:
        return self.get_attr_from_obj('MPESA_CONSUMER_KEY')

    def get_consumer_secret(self)->str:
        return self.get_attr_from_obj('MPESA_CONSUMER_SECRET')

    def get_environment(self)->str:
        return self.get_attr_from_obj('MPESA_ENVIRONMENT')

    def get_shortcode(self)->str:
        return self.get_attr_from_obj('MPESA_SHORTCODE')

    def get_express_shortcode(self)->str:
        return self.get_attr_from_obj('MPESA_EXPRESS_SHORTCODE')

    def get_shortcode_type(self)->str:
        return self.get_attr_from_obj('MPESA_SHORTCODE_TYPE')

    def get_passkey(self)->str:
        return self.get_attr_from_obj('MPESA_PASSKEY')



