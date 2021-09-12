import time

"""
漏斗算法顾名思义采用一个漏斗来对流量进行限制。
因为漏斗下面有孔，所以会定时的漏水下去，然后我们可以将流量想象为从上边落入漏斗的水。
这样就会有两种情况，
第二种情况就是, 如果流量的注入漏斗的速度比漏斗的漏水的速度慢，漏斗就会处于一个空漏斗的状态，也就是没有超出负荷的状态。
第二种情况就是，如果流量注入漏斗的速度比漏斗快，那么漏斗就会渐渐的超出最大的容量，对于溢出的流量，漏斗会采用拒绝的方式，防止流量继续进入。

漏桶
漏桶的出水速度是恒定的，那么意味着如果瞬时大流量的话，将有大部分请求被丢弃掉（也就是所谓的溢出）。

令牌桶
生成令牌的速度是恒定的，而请求去拿令牌是没有速度限制的。这意味，面对瞬时大流量，该算法可以在短时间内请求拿到大量令牌，而且拿令牌的过程并不是消耗很大的事情。


【令牌桶】令牌桶可以用来保护自己，主要用来对调用者频率进行限流，为的是让自己不被打垮。所以如果自己本身有处理能力的时候，如果流量突发（实际消费能力强于配置的流量限制），
那么实际处理速率可以超过配置的限制。

【漏桶】，这是用来保护他人，也就是保护他所调用的系统。主要场景是，当调用的第三方系统本身没有保护机制，或者有流量限制的时候，我们的调用速度不能超过他的限制，
由于我们不能更改第三方系统，所以只有在主调方控制。这个时候，即使流量突发，也必须舍弃。因为消费能力是第三方决定的。
总结起来：如果要让自己的系统不被打垮，用令牌桶。如果保证被别人的系统不被打垮，用漏桶算法。

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
        free_capacity = int(last_ts * self.__leaking_rage)
        if free_capacity < 1:
            return

        # 将释放的空间加入到空间空间中
        self.__free_capacity += free_capacity
        self.__leaking_time = now_time

        if self.__free_capacity > self.__capacity:
            self.__free_capacity = self.__capacity


if __name__ == "__main__":
    worker = FunnelRateLimiter(5, 0.5)

    for i in range(20):
        print(worker.action_allow(1))
 #       time.sleep(1)