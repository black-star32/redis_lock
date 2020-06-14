from redis_client import RedisClient
from redis_lock import redis_lock


@redis_lock(RedisClient.get_client(), "send_mail", wait_time=60, wait_msg="60秒内只能发送一次邮件")
def send_mail():
    print("sdfasd")


if __name__ == '__main__':
    for i in range(10):
        send_mail()
