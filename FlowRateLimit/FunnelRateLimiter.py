import time

"""
漏斗算法顾名思义采用一个漏斗来对流量进行限制。
因为漏斗下面有孔，所以会定时的漏水下去，然后我们可以将流量想象为从上边落入漏斗的水。
这样就会有两种情况，
第二种情况就是, 如果流量的注入漏斗的速度比漏斗的漏水的速度慢，漏斗就会处于一个空漏斗的状态，也就是没有超出负荷的状态。
第二种情况就是，如果流量注入漏斗的速度比漏斗快，那么漏斗就会渐渐的超出最大的容量，对于溢出的流量，漏斗会采用拒绝的方式，防止流量继续进入。

"""


class FunnelRateLimiter:

    """
    每次新来流量都会重新调整__free_capacity的大小，然后判断__free_capacity剩余流量是否能够容纳这些流量，
    如果能够容纳就减少__free_capacity的大小，
    如果不能容纳则拒绝，

    """
    def __init__(self, capacity, leaking_rate):
        """
        :param capacity:
        :param leaking_rate:
        """
        # 漏斗容量
        self.__capacity = capacity
        # 漏斗空余容量
        self.__free_capacity = capacity
        # 漏斗漏水流速(个/s)
        self.__leaking_rage = leaking_rate
        # 上次漏水时间
        self.__leaking_time = int(time.time())

    def action_allow(self, need_use_capacity):
        self.__make_space()
        if self.__free_capacity >= need_use_capacity:
            self.__free_capacity -= need_use_capacity
            return True
        return False

    def __make_space(self):
        now_time = int(time.time())
        # 距离上一次漏水时间差
        last_ts = now_time - self.__leaking_time

        # 可以腾空出来的空间
        free_capacity = last_ts * self.__leaking_rage
        if free_capacity < 1:
            return

        # 将释放的空间加入到空间空间中
        self.__free_capacity += free_capacity
        self.__leaking_time = now_time

        if self.__free_capacity > self.__capacity:
            self.__free_capacity = self.__capacity


if __name__ == "__main__":
    worker = FunnelRateLimiter(5, 1)

    for i in range(20):
        print(worker.action_allow(1))
        time.sleep(1)