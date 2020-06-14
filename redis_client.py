import redis

class RedisClient(object):
    """
    Redis客户端
    """
    _CLIENT = None

    @classmethod
    def get_client(cls):
        """
        获取客户端
        :return:
        """
        if cls._CLIENT:
            return cls._CLIENT

        pool = redis.ConnectionPool(host='localhost', port=6379, db=0)

        cls._CLIENT = redis.StrictRedis(connection_pool=pool)
        return cls._CLIENT
