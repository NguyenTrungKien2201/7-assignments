"""
Lesson 11 - Parse extra GPS data from NMEA sentences.

This parser extracts latitude, longitude, altitude, speed, date/time, satellite
count, and fix quality from common GGA/RMC sentences.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Optional


@dataclass
class GpsTelemetry:
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    altitude_m: Optional[float] = None
    speed_kmh: Optional[float] = None
    gps_time_utc: Optional[str] = None
    satellites: Optional[int] = None
    fix_quality: Optional[int] = None


def nmea_coord_to_decimal(value: str, hemisphere: str) -> Optional[float]:
    if not value or not hemisphere:
        return None

    # Latitude format: ddmm.mmmm. Longitude format: dddmm.mmmm.
    dot_index = value.find(".")
    degree_digits = dot_index - 2
    degrees = float(value[:degree_digits])
    minutes = float(value[degree_digits:])
    decimal = degrees + minutes / 60.0

    if hemisphere in ("S", "W"):
        decimal *= -1
    return round(decimal, 7)


def parse_gga(parts: list[str], telemetry: GpsTelemetry) -> None:
    # $GPGGA,time,lat,N,lon,E,fix_quality,num_satellites,hdop,altitude,M,...
    telemetry.latitude = nmea_coord_to_decimal(parts[2], parts[3])
    telemetry.longitude = nmea_coord_to_decimal(parts[4], parts[5])
    telemetry.fix_quality = int(parts[6]) if parts[6] else None
    telemetry.satellites = int(parts[7]) if parts[7] else None
    telemetry.altitude_m = float(parts[9]) if parts[9] else None


def parse_rmc(parts: list[str], telemetry: GpsTelemetry) -> None:
    # $GPRMC,time,status,lat,N,lon,E,speed_knots,course,date,...
    telemetry.latitude = nmea_coord_to_decimal(parts[3], parts[4]) or telemetry.latitude
    telemetry.longitude = nmea_coord_to_decimal(parts[5], parts[6]) or telemetry.longitude

    if parts[7]:
        speed_knots = float(parts[7])
        telemetry.speed_kmh = round(speed_knots * 1.852, 2)

    raw_time = parts[1]
    raw_date = parts[9]
    if raw_time and raw_date:
        # Date: ddmmyy. Time: hhmmss.sss
        dt = datetime(
            year=2000 + int(raw_date[4:6]),
            month=int(raw_date[2:4]),
            day=int(raw_date[0:2]),
            hour=int(raw_time[0:2]),
            minute=int(raw_time[2:4]),
            second=int(float(raw_time[4:])),
            tzinfo=timezone.utc,
        )
        telemetry.gps_time_utc = dt.isoformat().replace("+00:00", "Z")


def parse_nmea_sentences(sentences: list[str]) -> GpsTelemetry:
    telemetry = GpsTelemetry()

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence.startswith("$"):
            continue

        # Remove checksum if present.
        sentence_without_checksum = sentence.split("*")[0]
        parts = sentence_without_checksum.split(",")
        sentence_type = parts[0][-3:]

        try:
            if sentence_type == "GGA":
                parse_gga(parts, telemetry)
            elif sentence_type == "RMC":
                parse_rmc(parts, telemetry)
        except (ValueError, IndexError):
            continue

    return telemetry


if __name__ == "__main__":
    sample_sentences = [
        "$GPGGA,091520.00,1046.6140,N,10642.0540,E,1,08,0.9,12.4,M,0.0,M,,*47",
        "$GPRMC,091520.00,A,1046.6140,N,10642.0540,E,22.84,84.4,030526,,,A*68",
    ]
    result = parse_nmea_sentences(sample_sentences)
    print(asdict(result))
