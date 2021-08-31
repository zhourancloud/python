import redis
import uuid
import json
import time

"""
http://www.360doc.com/content/16/0923/15/4958641_732609265.shtml
"""

class DelayQueue:
    QUEUE_KEY = 'delay_queue'
    DATA_PREFIX = 'delay_queue_data'

    def __init__(self, conf):
        self._redis_client = redis.Redis(host=conf['host'],
                                         port=conf['port'],
                                         db=conf['db'])

    def push(self, msg):
        task_id = str(uuid.uuid4())
        key = '{}_{}'.format(self.DATA_PREFIX, task_id)
        self._redis_client.set(key, json.dumps(msg))
        self._redis_client.zadd(self.QUEUE_KEY, key, int(time.time()))

    def pop(self, num, previous):
        """
        :param num: pop 多少条数据
        :param previous: 获取多少秒前的数据
        :return:
        """
        pre_times = int(time.time()) - previous
        task_list = self._redis_client.zrangebyscore(self.QUEUE_KEY, 0, pre_times, start=0, num=num)
        if not task_list:
            return []
        pipe = self._redis_client.pipeline()
        for task_id in task_list:
            pipe.zrem(self.QUEUE_KEY, task_id)
        data_keys = [
            key
            for key, flag in zip(task_list, pipe.execute())
            if flag
        ]
        if not data_keys:
            return []

        data = [
            json.loads(item) for item in self._redis_client.mget(data_keys)
        ]

        self._redis_client.delete(*data_keys)
        return data


if __name__ == "__main__":
    queue = DelayQueue({'host': '120.78.127.165', 'port': 6379, 'db': 0})
    for i in range(20):
        item = {
            'user': 'user-{}'.format(i)
        }
        queue.push(item)

    data = queue.pop(num=10)
    assert len(data) == 0

    time.sleep(10)
    data = queue.pop(num=10)
    assert len(data) == 10

    data = queue.pop(num=10, previous=5)
    assert len(data) == 10
