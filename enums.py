import datetime
import enum
from typing import List


class DateString(str):
    pass


class DatetimeLinting(datetime.datetime):
    """
    It is used to create a new instance of the class.
    We override it to make sure that the value is a string in specific format.
    """

    def __new__(cls, value: DateString, format: "%Y/%m/%d, %H:%M:%S"):
        return datetime.datetime.strptime(value, format)


class Fields(enum.Enum):
    """
    Enum class for the fields in the data.json file.
    """
    x: DatetimeLinting = 'x'
    uniques: List[int] = 'uniques'
    visits: List[int] = 'visits'
    sdur: List[int] = 'sdur'


class TimeMetrics(enum.Enum):
    """
    Enum class for the time metrics, we want to predict the specific metric for the next 1, 3, 7, 14, 30, 90, 180, 365d.
    """
    ONE_DAY = 1
    THREE_DAYS = 3
    ONE_WEEK = 7
    TWO_WEEKS = 14
    ONE_MONTH = 30
    THREE_MONTHS = 90
    SIX_MONTHS = 180
    ONE_YEAR = 365
