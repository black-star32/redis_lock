# -*- coding: UTF-8 -*-
import functools
import time
import uuid

KEY_PREFIX = 'LOCK_'
def redis_lock(redis, key_name, wait_time=60, wait_msg=None):
    """
    :param redis: redis client
    :param key_name: key 名称
    :param wait_time: 锁定时间
    :param wait_msg: 等待信息
    :return:
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(**kwargs):
            lock_key = KEY_PREFIX + key_name.format(**kwargs)
            with RedisLock(redis, lock_key, wait_time, wait_msg):
                return func(**kwargs)

        return wrapper

    return decorator

class RedisLock(object):

    def __init__(self, redis, name, wait_time, wait_msg):
        """
        :param redis:
        :param name:
        :param wait_time:
        :param wait_msg:
        """
        self.redis = redis
        self.name = name
        self.wait_time = wait_time
        self.wait_msg = wait_msg or u"发送频率过高，请稍后再试"

    def __enter__(self):
        # force blocking, as otherwise the user would have to check whether
        # the lock was actually acquired or not.
        self.acquire()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass
        # self.release()

    def acquire(self):
        while 1:
            if self.do_acquire(self.name):
                return True
            else:
                time.sleep(10)

    def do_acquire(self, name):
        result = self.redis.exists('name')
        if not result:
            self.redis.set('name', 'mail_lock')
            self.redis.expire('name', 60)
            return True
        return False

    def release(self):
        expected_key = self.name
        self.name = None
        self.do_release(expected_key)

    def do_release(self, expected_key):
        lock_value = self.redis.get(expected_key)
        self.redis.delete(expected_key)

class LockError(ValueError):
    """
    Errors acquiring or releasing a lock
    """
    pass

class BlockingTimeOutException(LockError):
    pass

class Dummy(object):
    """
    Instances of this class can be used as an attribute container.
    """
    pass
