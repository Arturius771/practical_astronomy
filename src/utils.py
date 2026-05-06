import math

from astronomy_types import DecimalTime, Hour, Minute, Second, Time


def time_to_decimal_time(time: Time) -> DecimalTime:
    unsigned_decimal = (
        int(time.hour) + int(time.minute) / 60 + float(time.second) / 3600
    )

    return DecimalTime(unsigned_decimal)


def decimal_time_to_time(decimal_value: DecimalTime) -> Time:
    unsigned_decimal = abs(float(decimal_value))

    total_seconds = unsigned_decimal * 3600
    rounded_seconds = round(total_seconds % 60, 2)

    seconds = 0 if rounded_seconds == 60 else rounded_seconds
    remainder = total_seconds + 60 if rounded_seconds == 60 else total_seconds

    minutes = math.floor(remainder / 60) % 60
    hours = math.floor(remainder / 3600)

    return Time(
        hour=Hour(hours),
        minute=Minute(minutes),
        second=Second(seconds),
    )
