# ProfAll

ProfAll is a global Python profiler via `.pth` hooks. It intercepts Python executions automatically to record execution runtimes and can optionally run a `cProfile` dump for every Python execution on a machine. Data is seamlessly reported to an InfluxDB v2 server.

## Overview

The `profall` package installs a global `.pth` hook directly into your Python environment's site-packages. This means any Python script run with that interpreter will execute the ProfAll hook logic.

Since this affects the global execution path, ProfAll strives to have effectively *zero* startup overhead until explicitly enabled via environment variables.

## Requirements

- Python 3.12+
- InfluxDB v2 server

## Installation & Setup

1. Install the package via pip:
   ```bash
   pip install profall
   ```
1. Inject the hook into your environment:
   ```bash
   profall install
   ```
1. Set your InfluxDB connection environment variables:
   - `PROFALL_INFLUXDB_URL` (default: `http://localhost:8086`)
   - `PROFALL_INFLUXDB_TOKEN` (default: `my-token`)
   - `PROFALL_INFLUXDB_ORG` (default: `my-org`)
   - `PROFALL_INFLUXDB_BUCKET` (default: `ProfAll`)
1. Enable the profiler by setting the `PROFALL` environment variable.

See the [User Guide](USER_GUIDE.md) for more usage examples and instructions.

## Development

See the [Developer Guide](DEVELOPER_GUIDE.md) for instructions on local development, testing, and contribution rules.
