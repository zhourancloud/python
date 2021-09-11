import time


class SnowflakeUtils:
    """
    使用雪花算法生成分布式唯一ID
    64bit划分
    1. 符号位，占用1位。
    2. 时间戳，占用41位，可以支持69年的时间跨度。
    3. 机器ID，占用10位。
    4. 序列号，占用12位。一毫秒可以生成4095个ID。
    |1位符合位|41位时间戳|3位机房位+7位机器位|12位序列号|
    """
    # 机房区域ID占用bit数
    DATA_CENTER_ID_BITS = 3
    # 机器ID占用bit数
    WORKER_ID_BITS = 7
    # 序列号占用bit数
    SEQUENCE_ID_BITS = 12

    # 位移偏移量
    WORKER_ID_SHIFT = SEQUENCE_ID_BITS
    DATA_CENTER_ID_SHIFT = SEQUENCE_ID_BITS + WORKER_ID_BITS
    TIMESTAMP_SHIFT = SEQUENCE_ID_BITS + WORKER_ID_BITS + DATA_CENTER_ID_BITS

    # Twitter元年时间戳
    START_TIME = 1288834974657

    SEQ_MAX_NUM = ~(-1 << SEQUENCE_ID_BITS)

    def __init__(self):
        self.__last_timestamp = -1
        self.__sequence = 0

        self.__data_center_id = 1
        self.__worker_id = 1

    def GenerateId(self):
        timestamp = int(time.time() * 1000)

        # 时钟回拨
        if timestamp < self.__last_timestamp:
            raise None

        if timestamp == self.__last_timestamp:
            self.__sequence = (self.__sequence + 1) & self.SEQ_MAX_NUM
            if self.__sequence == 0:
                timestamp = self.__next_millimeter()
        else:
            self.__sequence = 0

        self.__last_timestamp = timestamp

        new_id = ((timestamp - self.START_TIME) << self.TIMESTAMP_SHIFT) | \
                 (self.__data_center_id << self.DATA_CENTER_ID_SHIFT) | \
                 (self.__worker_id << self.WORKER_ID_SHIFT) | self.__sequence

        return new_id

    def __next_millimeter(self):
        timestamp = int(time.time() * 1000)
        while timestamp <= self.__last_timestamp:
            timestamp = int(time.time() * 1000)
        return timestamp


if __name__ == "__main__":
    worker = SnowflakeUtils()

    result = worker.GenerateId()
    print("result:{}".format(result))

    result = worker.GenerateId()
    print("result:{}".format(result))

    result = worker.GenerateId()
    print("result:{}".format(result))

