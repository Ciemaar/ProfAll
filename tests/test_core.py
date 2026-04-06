"""Tests for core telemetry recording and profiling logic."""

import datetime
import os
from unittest.mock import MagicMock, patch

import pytest
from profall.core import end_profile, install_hooks, record_execution, write_measurement


@pytest.fixture
def mock_influx() -> MagicMock:
    """Fixture providing a mocked InfluxDB client and APIs."""
    with patch("influxdb_client.client.influxdb_client.InfluxDBClient") as MockClient:
        mock_client_inst = MagicMock()
        mock_write_api = MagicMock()

        mock_client_inst.__enter__.return_value = mock_client_inst
        mock_client_inst.write_api.return_value = mock_write_api
        MockClient.return_value = mock_client_inst

        yield mock_write_api


def test_write_measurement_success(mock_influx: MagicMock) -> None:
    """Test successful write to InfluxDB."""
    write_measurement("test_metric", {"test_field": 1.0})
    assert mock_influx.write.called
    args, kwargs = mock_influx.write.call_args
    assert kwargs["bucket"] == "ProfAll"
    assert kwargs["org"] == "my-org"
    assert kwargs["record"]._name == "test_metric"


def test_write_measurement_import_error() -> None:
    """Test behavior when influxdb-client is missing."""
    with patch.dict("sys.modules", {"influxdb_client.client.influxdb_client": None}):
        with patch("sys.stderr.write") as mock_stderr:
            write_measurement("test_metric", {"test_field": 1.0})
            mock_stderr.assert_called_with("profall: influxdb-client not installed. Skipping measurement write.\n")


def test_write_measurement_write_exception(mock_influx: MagicMock) -> None:
    """Test handling of write exception to InfluxDB."""
    mock_influx.write.side_effect = Exception("Connection Failed")
    with patch("sys.stderr.write") as mock_stderr:
        write_measurement("test_metric", {"test_field": 1.0})
        mock_stderr.assert_called_with("profall: Write to influxdb failed: Connection Failed\n")


@patch("profall.core.write_measurement")
def test_record_execution(mock_write: MagicMock) -> None:
    """Test that execution duration is correctly recorded."""
    start_time = datetime.datetime.now() - datetime.timedelta(seconds=5)
    record_execution(start_time)

    assert mock_write.called
    args, kwargs = mock_write.call_args
    assert args[0] == "runtime"
    assert "runtime" in args[1]
    assert args[1]["runtime"] >= 5.0


@patch("profall.core.write_measurement")
def test_end_profile(mock_write: MagicMock) -> None:
    """Test that ending a profile writes data and dumps stats."""
    mock_pr = MagicMock()
    start_time = datetime.datetime.now() - datetime.timedelta(seconds=2)

    end_profile(mock_pr, start_time)

    assert mock_pr.disable.called
    assert mock_pr.dump_stats.called
    assert mock_write.called

    args, kwargs = mock_write.call_args
    assert args[0] == "profile"
    assert "profile" in args[1]
    assert "runtime" in args[1]
    assert args[1]["runtime"] >= 2.0


@patch("atexit.register")
@patch.dict(os.environ, {"PROFALL": "OFF"})
def test_install_hooks_off(mock_atexit: MagicMock) -> None:
    """Test that hooks are not installed when PROFALL=OFF."""
    install_hooks()
    assert not mock_atexit.called


@patch("atexit.register")
@patch.dict(os.environ, clear=True)
def test_install_hooks_unset(mock_atexit: MagicMock) -> None:
    """Test that hooks are not installed when PROFALL is unset."""
    install_hooks()
    assert not mock_atexit.called


@patch("atexit.register")
@patch.dict(os.environ, {"PROFALL": "ON"})
def test_install_hooks_on(mock_atexit: MagicMock) -> None:
    """Test that only record_execution is registered when PROFALL=ON."""
    install_hooks()
    assert mock_atexit.called
    assert mock_atexit.call_args[0][0] == record_execution


@patch("atexit.register")
@patch("cProfile.Profile")
@patch.dict(os.environ, {"PROFALL": "PROFILE"})
def test_install_hooks_profile(mock_profile: MagicMock, mock_atexit: MagicMock) -> None:
    """Test that end_profile is registered and enabled when PROFALL=PROFILE."""
    mock_pr_inst = MagicMock()
    mock_profile.return_value = mock_pr_inst

    install_hooks()

    assert mock_pr_inst.enable.called
    assert mock_atexit.called
    assert mock_atexit.call_args[0][0] == end_profile
    assert mock_atexit.call_args[0][1] == mock_pr_inst
