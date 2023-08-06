"""
Date Math
"""

import calendar
import datetime
from typing import Optional, Tuple

from .weekdays import DayOfWeek
from .months import MonthOfYear
from .daterules import BusinessDayConvention
from .calendars import SimpleCalendar, AbstractCalendar

_MONTH_DAYS = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)

WEEKEND_CALENDAR = SimpleCalendar([DayOfWeek.SATURDAY, DayOfWeek.SUNDAY], [])


def days_in_month(year: int, month: int) -> int:
    """Returns the number of days in the month.

    :param year: The year
    :type year: int
    :param month: The month
    :type month: int
    :return: The number of days in the month
    :rtype: int
    """
    return 29 if calendar.isleap(year) and month == 2 else _MONTH_DAYS[month - 1]


def days_in_year(year: int) -> int:
    """Returns the number of days in the year.

    :param year: The year
    :type year: int
    :return: The number of days in the year
    :rtype: int
    """
    return 366 if calendar.isleap(year) else 365


def is_end_of_month(date: datetime.date) -> bool:
    """Returns true if the given date is the last day of the month.

    :param date: The date
    :type date: date.datetime
    :return: True if the given date is the last day of the month
    :rtype: bool
    """
    return date.day == days_in_month(date.year, date.month)


def add_months(date: datetime.date, months: int, eom: bool = False) -> datetime.date:
    """
    Adds months to the date. If the end of month anchor is true, keep to the
    end of the month is the given date was at the end of the month.
    """

    month = date.month - 1 + months
    year = date.year + month // 12
    month = month % 12 + 1
    if eom and date == end_of_month(date.year, date.month):
        day = days_in_month(year, month)
    else:
        day = min(date.day, days_in_month(year, month))
    return datetime.date(year, month, day)


def nearest_business_day(
        date: datetime.date,
        prefer_forward: bool = True,
        cal: AbstractCalendar = WEEKEND_CALENDAR
) -> datetime.date:
    """
    Find the nearest business day to a given date.
    """
    if cal.is_business_day(date):
        return date

    one_day = datetime.timedelta(1)
    forward_date = date + one_day
    backward_date = date - one_day

    while True:
        is_forward_ok = cal.is_business_day(forward_date)
        is_backward_ok = cal.is_business_day(backward_date)
        if is_forward_ok and (prefer_forward or not is_backward_ok):
            return forward_date
        elif is_backward_ok:
            return backward_date
        forward_date += one_day
        backward_date -= one_day


def add_business_days(
        date: datetime.date,
        count: int,
        cal: AbstractCalendar = WEEKEND_CALENDAR
) -> datetime.date:
    """Adds business days to a date

    :param date: The target date
    :type date: date
    :param count: The number of days
    :type count: int
    :param cal: The calendar, defaults to WEEKEND_CALENDAR
    :type cal: AbstractCalendar, optional
    :return: The new date
    :rtype: date
    """

    sign = 1 if count > 0 else -1
    signed_day = datetime.timedelta(sign)

    while count != 0:
        date += signed_day
        count -= sign

        while not cal.is_business_day(date):
            date += signed_day

    return date


def adjust(
        date: datetime.date,
        convention: BusinessDayConvention = BusinessDayConvention.FOLLOWING,
        prefer_forward: bool = True,
        cal: AbstractCalendar = WEEKEND_CALENDAR
) -> datetime.date:
    """
    Adjusts a non-business day to the appropriate near business day
    with respect to the given convention.
    """

    if convention == BusinessDayConvention.NONE or cal.is_business_day(date):
        return date
    elif convention == BusinessDayConvention.NEAREST:
        return nearest_business_day(date, prefer_forward, cal)
    elif convention == BusinessDayConvention.FOLLOWING:
        return add_business_days(date, 1, cal)
    elif convention == BusinessDayConvention.PRECEDING:
        return add_business_days(date, -1, cal)
    elif convention == BusinessDayConvention.MODIFIED_FOLLOWING:
        adjusted_date = add_business_days(date, 1, cal)

        if adjusted_date.month == date.month:
            return adjusted_date
        else:
            return add_business_days(date, -1, cal)
    elif convention == BusinessDayConvention.MODIFIED_PRECEDING:
        adjusted_date = add_business_days(date, -1, cal)

        if adjusted_date.month == date.month:
            return adjusted_date
        else:
            return add_business_days(date, 1, cal)
    else:
        raise ValueError("Invalid business day convention")


def advance(
        date: datetime.date,
        days: Optional[int] = None,
        weeks: Optional[int] = None,
        months: Optional[int] = None,
        years: Optional[int] = None,
        convention: BusinessDayConvention = BusinessDayConvention.FOLLOWING,
        eom: bool = False,
        cal: AbstractCalendar = WEEKEND_CALENDAR
) -> datetime.date:
    """
    Advances the given date of the given number of business days and
    returns the result.
    Note: The input date is not modified.
    """

    if not (days or weeks or months or years):
        return adjust(date, convention, cal=cal)

    if years:
        date = adjust(add_months(
            date, 12 * years, eom), convention, cal=cal)

    if months:
        date = adjust(add_months(
            date, months, eom), convention, cal=cal)

    if weeks:
        date = adjust(
            date + datetime.timedelta(days=7 * weeks), convention)

    if days:
        date = add_business_days(date, days, cal)

    return date


def end_of_month(year: int, month: int) -> datetime.date:
    """
    Return the date at the last day of the month.
    """
    return datetime.date(year, month, days_in_month(year, month))


def add_nth_day_of_week(
        date: datetime.date,
        nth: int,
        dow: DayOfWeek,
        strictly_different: bool
) -> datetime.date:
    """
    Add or subtract a number of different days of the week.

    If the start date lies on the specified day of the week and the strictly
    different flag is false, the current date would be considered the first
    day of the week.
    """

    if nth == 0:
        return date

    if dow < DayOfWeek.MONDAY or dow > DayOfWeek.FRIDAY:
        return date

    diff = dow - date.weekday()

    if diff == 0 and strictly_different:
        nth += 1 if nth >= 0 else -1

    # forwards
    if nth > 0:
        # If diff = 0 below, the input date is the 1st DOW already, no adjustment
        # is required. The 'diff' is the adjustment from the input date
        # required to get to the first DOW matching the 'dow_index' given.

        if diff < 0:
            diff += 7

        adjusted_start_date = date + datetime.timedelta(diff)
        end_date = adjusted_start_date + datetime.timedelta((nth - 1) * 7)
        return end_date
    # backwards
    else:
        # If diff = 0 below, the input date is the 1st DOW already, no adjustment
        # is required. The 'diff' is the adjustment from the input date
        # required to get to the first DOW matching the 'dow_index' given.

        if diff > 0:
            diff -= 7

        adjusted_start_date = date + datetime.timedelta(diff)
        end_date = adjusted_start_date + datetime.timedelta((nth + 1) * 7)
        return end_date


def easter(year: int) -> datetime.date:
    """
    The date for Easter Sunday for the given year.
    """
    # Note: Only true for Gregorian dates

    # pylint: disable=invalid-name
    y = year
    g = (y - ((y // 19) * 19)) + 1
    c = (y // 100) + 1
    x = ((3 * c) // 4) - 12
    z = (((8 * c) + 5) // 25) - 5
    d = ((5 * y) // 4) - x - 10
    e1 = (11 * g) + 20 + z - x
    e = e1 - ((e1 // 30) * 30)

    # The value of 'e' may be negative. The case of year = 14250, e.g.,
    # produces values of g = 1, z = 40 and x = 95. The value of e1 is thus
    # -24, and the 'mod' code fails to return the proper positive result.
    # The following correction produces a positive value, mod 30, for 'e'.

    while e < 0:
        e += 30

    if ((e == 25) and (g > 11)) or (e == 24):
        e += 1

    n = 44 - e

    if n < 21:
        n += 30

    dpn = d + n
    n1 = dpn - ((dpn // 7) * 7)
    n = n + 7 - n1

    if n > 31:
        month = 4
        day = n - 31
    else:
        month = 3
        day = n

    return datetime.date(year, month, day)


def days_and_months_between(start_date: datetime.date, end_date: datetime.date) -> Tuple[int, int]:
    """
    Calculates the number of days an months between two dates.
    """
    if start_date == end_date:
        return 0, 0

    start_date1 = datetime.date(start_date.year, start_date.month, 1)
    end_date1 = datetime.date(end_date.year, end_date.month, 1)
    months = (end_date1.year - start_date1.year) * \
        12 + (end_date1.month - start_date1.month)

    if not is_end_of_month(end_date) and (
            is_end_of_month(start_date) or start_date.day > end_date.day
    ):
        months -= 1

    if start_date.day == end_date.day or (
            is_end_of_month(start_date) and is_end_of_month(end_date)
    ):
        days = 0
    elif start_date.day < end_date.day:
        days = end_date.day - start_date.day
    else:
        days = days_in_month(start_date.year, start_date.month) - \
            start_date.day + end_date.day

    return days, months


def are_in_same_quarter(first: datetime.date, second: datetime.date) -> bool:
    """
    Find out if two dates are in the same quarter.
    """
    if first > second:
        return are_in_same_quarter(second, first) # pylint: disable=arguments-out-of-order

    return first == second or (
        first.year == second.year and second.month - first.month < 4 and (
            second.month - 1) % 3 > (first.month - 1) % 3)


def quarter_of_year(date: datetime.date) -> int:
    """
    Find the quarter of the year for a given date.
    """
    if date.month in [MonthOfYear.JANUARY, MonthOfYear.FEBRUARY, MonthOfYear.MARCH]:
        return 1
    elif date.month in [MonthOfYear.APRIL, MonthOfYear.MAY, MonthOfYear.JUNE]:
        return 2
    elif date.month in [MonthOfYear.JULY, MonthOfYear.AUGUST, MonthOfYear.SEPTEMBER]:
        return 3
    else:
        return 4


def week_of_year(date: datetime.date, iso: bool = True) -> int:
    """
    Return the week of the year
    """
    if iso:
        return date.isocalendar()[1]
    else:
        return 1 + (date - datetime.date(date.year, 1, 1)).days // 7
