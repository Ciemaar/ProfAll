# User Guide

ProfAll manages global profiling and execution time telemetry for a given Python environment via `.pth` hooks. When installed, `profall.pth` sits in your Python's site-packages and automatically evaluates minimal logic when Python starts.

## CLI Usage

The package comes with a `profall` CLI to easily inject or remove the `.pth` hook.

### Installation

To install the `.pth` hook to your site-packages:

```bash
profall install
```

This will write a file (`profall.pth`) containing `import profall.hook` directly to your global or user site-packages, allowing it to hook all Python executions. Note: If you run this in a global environment instead of a virtualenv, you may need `sudo`.

### Uninstallation

To easily remove the `.pth` hook:

```bash
profall uninstall
```

## Running the Profiler

ProfAll execution logic is controlled entirely through the `PROFALL` environment variable.

### `PROFALL=OFF` (Default)

If the environment variable is not set, or is set to `OFF`, the hook immediately returns and does not register any `atexit` functions.

### `PROFALL=ON`

When set to `ON` (or any value other than `OFF` and `PROFILE`), ProfAll records the total run duration of the Python execution and posts the telemetry to InfluxDB.

```bash
PROFALL=ON python your_script.py
```

### `PROFALL=PROFILE`

When set to `PROFILE`, ProfAll enables `cProfile` instantly. When the process finishes, ProfAll saves the cProfile dump to your `temp` directory (with the PID and command name) and records the duration plus the dump file path in InfluxDB.

```bash
PROFALL=PROFILE python your_script.py
```

## Configuring InfluxDB

ProfAll requires an InfluxDB v2 server. Ensure you have the following environment variables configured:

- `PROFALL_INFLUXDB_URL` (default: `http://localhost:8086`)
- `PROFALL_INFLUXDB_TOKEN` (default: `my-token`)
- `PROFALL_INFLUXDB_ORG` (default: `my-org`)
- `PROFALL_INFLUXDB_BUCKET` (default: `ProfAll`)
