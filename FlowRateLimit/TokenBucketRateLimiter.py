
import time


class TokenBucketRateLimiter:

    def __init__(self, capacity, rate):
        self.__capacity = capacity
        self.__current_capacity = 0
        self.__rate = rate
        self.__last_consume_time = int(time.time())

    def consume(self, token_count):
        """
        :param token_count: 发送数据需要的令牌数
        :return:
        """
        now_time = int(time.time())
        increment = (now_time - self.__last_consume_time) * self.__rate
        self.__current_capacity = min(increment + self.__current_capacity, self.__capacity)

        if token_count > self.__current_capacity:
            return False

        self.__last_consume_time = now_time
        self.__current_capacity -= token_count
        return True


if __name__ == "__main__":
    worker = TokenBucketRateLimiter(10, 1)
    time.sleep(1)
    time.sleep(1)
    time.sleep(1)

    for i in range(20):
        print(worker.consume(1))
        time.sleep(0.5)
