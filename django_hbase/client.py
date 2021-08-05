import happybase
from django.conf import settings


class HBaseClient:
    conn = None

    @classmethod
    def get_connection(cls):
        if cls.conn:
            return cls.conn
        cls.conn = happybase.Connection(settings.HBASE_HOST)
        return cls.conn
