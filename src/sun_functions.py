import math

from coordinate_functions import ecliptic_to_equatorial_coordinates
from time_functions import (
    greenwich_to_julian_date,
    local_civil_to_universal_time,
)
from astronomy_types import (
    Date,
    Day,
    EclipticCoordinates,
    EquatorialCoordinates,
    FullDate,
    Latitude,
    Longitude,
    Month,
    Radians,
    Year,
    radians,
)


def sun_longitude(
    local_date: FullDate,
    daylight_savings_correction: int,
    timezone_correction: int,
) -> Longitude:
    def sun_mean_anomaly_2010(degrees: float) -> float:
        ecliptic_longitude = 279.557208
        ecliptic_longitude_of_perigee = 283.112438

        return degrees + ecliptic_longitude - ecliptic_longitude_of_perigee

    def sun_true_anomaly_2010(mean_anomaly_degrees: float) -> float:
        eccentricity = 0.016705

        return mean_anomaly_degrees + (
            (360 / math.pi) * eccentricity * math.sin(radians(mean_anomaly_degrees))
        )

    def sun_longitude_2010(true_anomaly_degrees: float) -> float:
        ecliptic_longitude_of_perigee = 283.112438

        return true_anomaly_degrees + ecliptic_longitude_of_perigee

    greenwich_date = local_civil_to_universal_time(
        local_date,
        daylight_savings_correction,
        timezone_correction,
    ).date

    julian_date = greenwich_to_julian_date(greenwich_date)

    epoch_date = greenwich_to_julian_date(
        Date(
            year=Year(2010),
            month=Month(1),
            day=Day(0),
        )
    )

    days_since_epoch = julian_date - epoch_date

    mean_longitude_degrees = 360 * days_since_epoch / 365.242191

    mean_anomaly = sun_mean_anomaly_2010(mean_longitude_degrees)
    mean_anomaly_corrected = mean_anomaly % 360

    true_anomaly = sun_true_anomaly_2010(mean_anomaly_corrected)

    longitude_degrees = sun_longitude_2010(true_anomaly)
    longitude_degrees_corrected = longitude_degrees % 360

    return Longitude(Radians(radians(longitude_degrees_corrected)))


def sun_position_approximate(
    local_date: FullDate,
    daylight_savings_correction: int,
    timezone_correction: int,
) -> EquatorialCoordinates:
    greenwich_date = local_civil_to_universal_time(
        local_date,
        daylight_savings_correction,
        timezone_correction,
    ).date

    longitude = sun_longitude(
        local_date,
        daylight_savings_correction,
        timezone_correction,
    )

    return ecliptic_to_equatorial_coordinates(
        EclipticCoordinates(
            latitude=Latitude(Radians(0.0)),
            longitude=longitude,
        ),
        greenwich_date,
    )
