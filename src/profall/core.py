"""Core logic for profiling and recording execution telemetry.

This module provides functions to record the execution time of Python scripts
and optionally profile them. Data is sent to an InfluxDB server.
"""

import atexit
import datetime
import os
import sys
from collections.abc import Mapping
from pathlib import Path


def write_measurement(measurement: str, fields: Mapping[str, float | str]) -> None:
    """Writes a measurement with fields and tags to InfluxDB.

    This function instantiates the InfluxDB client and writes the data points.
    It deliberately imports the client locally to avoid overhead unless
    profiling is active and executing.

    Args:
        measurement: The name of the measurement.
        fields: A mapping of field names to their values.
    """
    try:
        from influxdb_client import InfluxDBClient, Point
        from influxdb_client.client.write_api import SYNCHRONOUS
    except ImportError:
        sys.stderr.write("profall: influxdb-client not installed. Skipping measurement write.\n")
        return

    # Using environment variables or defaults for InfluxDB v2 connection
    url = os.environ.get("PROFALL_INFLUXDB_URL", "http://localhost:8086")
    token = os.environ.get("PROFALL_INFLUXDB_TOKEN", "my-token")
    org = os.environ.get("PROFALL_INFLUXDB_ORG", "my-org")
    bucket = os.environ.get("PROFALL_INFLUXDB_BUCKET", "ProfAll")

    tags: dict[str, str | int] = {
        "args": " ".join(sys.argv),
        "interpreter": sys.executable,
        "version": ".".join(str(x) for x in sys.version_info),
        "pid": os.getpid(),
        "ppid": os.getppid(),
    }

    point = Point(measurement)
    for k, v in tags.items():
        point = point.tag(k, str(v))
    for k, v in fields.items():
        point = point.field(k, v)

    try:
        with InfluxDBClient(url=url, token=token, org=org) as client:
            write_api = client.write_api(write_options=SYNCHRONOUS)
            write_api.write(bucket=bucket, org=org, record=point)
    except Exception as e:
        sys.stderr.write(f"profall: Write to influxdb failed: {e}\n")


def record_execution(start_time: datetime.datetime) -> None:
    """Records the total execution time of the process.

    Args:
        start_time: The timestamp when the process started.
    """
    fields: dict[str, float] = {"runtime": (datetime.datetime.now() - start_time).total_seconds()}
    write_measurement("runtime", fields)


def end_profile(pr: object, start_time: datetime.datetime) -> None:
    """Ends profiling, dumps stats to a file, and records the profile execution.

    Args:
        pr: The cProfile.Profile instance that was active.
        start_time: The timestamp when the process started.
    """
    import tempfile

    pr.disable()  # type: ignore[attr-defined]

    pid = os.getpid()
    ppid = os.getppid()
    cmd = Path(sys.argv[0]).name if sys.argv else "unknown"

    temp_dir = Path(tempfile.gettempdir())
    filename = temp_dir / f"{ppid}_{pid}_{cmd}.dmp"

    fields: dict[str, str | float] = {
        "profile": str(filename),
        "runtime": (datetime.datetime.now() - start_time).total_seconds(),
    }

    write_measurement("profile", fields)
    pr.dump_stats(str(filename))  # type: ignore[attr-defined]


def install_hooks() -> None:
    """Installs the atexit hooks based on the PROFALL environment variable."""
    mode = os.environ.get("PROFALL", "")

    if not mode or mode == "OFF":
        return

    start_time = datetime.datetime.now()

    if mode == "PROFILE":
        import cProfile

        pr = cProfile.Profile()
        pr.enable()

        atexit.register(end_profile, pr, start_time)  # type: ignore[arg-type]
    else:
        atexit.register(record_execution, start_time)


# For manual testing/execution
if __name__ == "__main__":
    start_time_main = datetime.datetime.now()
    record_execution(start_time_main)
