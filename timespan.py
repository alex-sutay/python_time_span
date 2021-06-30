# file: timespan.py
# author: Alex Sutay

from datetime import datetime
from datetime import timedelta


class timespan:
    """
    A class to represent a span of time. Includes a start date, end date, and a list of breaks, which are timespans
    Breaks are assumed not to include breaks within themselves. If you pass a timespan with a break as a break, the inner break will be ignored
    and only the overall span will be used.
    """
    def __init__(self, start, end, breaks = []):
        """
        Constructor.
        :param start: a datetime to represent the start of the span
        :param end: a datetime to represent the end of the span
        :param breaks: optional, a list of timespans representing breaks
        """
        self.start = start
        self.end = end
        self.breaks = breaks
        self.total_length = end - start
        self.length = self.total_length
        for b in breaks:
            self.length -= b.total_length
    def total_percent(self, now):
        """
        Get the percent of the way through a datetime is
        Reutrns a percent, therefore it will be between 0 and 100
        If the datetime passed in is before the start, it will return 0, if it's after, 100
        This method doesn't account for breaks. If you want to, use percent() instead
        :param now: the time you're evaluating
        """
        percent = (now - self.start) / self.total_length * 100
        return _middle(0, percent, 100)
    def percent(self, now):
        """
        Get the percent of the way through a datetime is
        Reutrns a percent, therefore it will be between 0 and 100
        If the datetime passed in is before the start, it will return 0, if it's after, 100
        This method accounts for breaks. If you don't want to, use total_percent() instead
        :param now: the time you're evaluating
        """
        passed = now - self.start
        for b in self.breaks:
            passed -= _middle(timedelta(hours=0), b.total_length, now - b.start) if now - b.start > timedelta(hours=0) else timedelta(hours=0)

        percent = passed / self.length * 100
        return _middle(0, percent, 100)


def _middle(lowerbound, value, upperbound):
    """
    A function that returns either the lowerbound, upperbound, or the value itself.
    The value itself is returned if it is between the two bounds, otherwise the bound it exceded is returned
    :param lowerbound: the minimum reutrn value
    :param value: the value being evaluated
    :param upperbound: the maximum return value
    :return: a value between lowerbound and upperbound, inclusive
    """
    if lowerbound > upperbound:
        raise ValueError("Error: lowerbound greater than upperbound")
    elif lowerbound == upperbound:
        return lowerbound
    else:
        return max(lowerbound, min(upperbound, value))


def countdown(span_tuples):
    """
    Starts printing a countdownfor a series of timespans.
    span_tuples should be a list of tuples, where the tuples are (title, span, mode) as (str, timespan, int)
    The modes are 0 for percent and 1 for total percent
    Titles have a max length of 19
    :param span_tuples: list of span tuples, including the title and timespan itself
    :return: None
    """
    titles = []
    for span_tuple in span_tuples:
        title, span, mode = span_tuple
        titles.append(title if len(title) <= 19 else title[:19])
        if mode not in [0, 1]:
            raise NotImplementedError("Provided mode invalid")
    for title in titles:
        print(title, end=" " * (20-len(title)))
    print()
    cont = True
    while cont:
        cont = False
        now = datetime.now()
        for span_tuple in span_tuples:
            title, span, mode = span_tuple
            percent = str(span.percent(now) if mode == 0 else span.total_percent(now))
            print(percent, end=" " * (20 - len(percent)), flush=True)
            cont = cont or percent != '100'
        print(end='\r', flush=True)
    print()

