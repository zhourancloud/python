import time
import redis


class ActionControl:
    """
    指定用户 user_id 的某个行为 action 在特定时间内 period 只允许发生做多的次数 max_count
    """
    def __init__(self, **conf):
        self._redis_client = redis.Redis(host=conf['host'],
                                         port=conf['port'],
                                         password=conf['password'],
                                         db=conf['db'])

    def is_action_allow(self, user_id, action, period, max_count):
        key = "action_control:{}:{}".format(user_id, action)
        now_ts = int(time.time()*1000)
        with self._redis_client.pipeline() as pipe:
            pipe.zadd(key, now_ts, now_ts)
            pipe.zremrangebyscore(key, 0, now_ts - period * 1000)
            pipe.zcard(key)
            pipe.expire(key, period + 1)
            _, _, current_count, _ = pipe.execute()
            print("current_count:{}".format(current_count))
        return current_count <= max_count


if __name__ == "__main__":
    action_control = ActionControl(**{'host': '120.78.127.165', 'port': 6379, 'password': '123456', 'db': 0})
    do_replay = action_control.is_action_allow('1111', 'block_ip', 60, 3)
    print("do_replay:{}".format(do_replay))

    do_replay = action_control.is_action_allow('1111', 'block_ip', 60, 3)
    print("do_replay:{}".format(do_replay))

    do_replay = action_control.is_action_allow('1111', 'block_ip', 60, 3)
    print("do_replay:{}".format(do_replay))

    do_replay = action_control.is_action_allow('1111', 'block_ip', 60, 3)
    print("do_replay:{}".format(do_replay))

