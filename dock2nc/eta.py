
"""Calculate Etimated Time of Arrival (estimated time of completion) for
a task."""

from __future__ import print_function, division
import time


class ETA(object):
    def __init__(self, number_of_tasks):
        self.number_of_tasks = number_of_tasks
        self.start = now()
        self.timing_data = [(0, self.start)]

    def done(self, n):
        """Indicate that `n` tasks have been completed."""
        ndone = 0
        if self.timing_data:
            ndone = self.timing_data[-1][0]
        ndone += n
        self.timing_data.append((ndone, now()))

    @property
    def elapsed(self):
        return (self.timing_data[-1][1] - self.start)

    def _calculate(self):
        """Estimate ETA using simple linear regression."""
        if len(self.timing_data) < 2:
            return 0.0
        x, y = zip(*self.timing_data)
        x = [el[0] for el in self.timing_data]
        y = [el[1] - self.start for el in self.timing_data]
        a = [xi * yi for (xi, yi) in zip(x, y)]
        b = [xi ** 2 for xi in x]
        slope = mean(a) / mean(b)
        eta = slope * self.number_of_tasks - y[-1]
        return eta

    def eta(self, fmt="%(hours)02.0f:%(minutes)02.0f:%(seconds)02.3fs"):
        """Return ETA formatted as decribed in `fmt`."""
        seconds = self._calculate()
        if (seconds < 1e-5):
            return "--:--:--"
        hours, minutes = divmod(seconds, 3600)
        minutes, seconds = divmod(minutes, 60)
        return fmt % vars()


def mean(x):
    return sum(x) / len(x)


def now():
    return time.time()


def main():
    N = 10
    eta = ETA(number_of_tasks=N)
    for i in xrange(N):
        time.sleep(1.0)
        eta.done(1)
        print eta.eta()


if __name__ == '__main__':
    main()
