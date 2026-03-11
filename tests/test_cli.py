"""Tests for ProfAll CLI commands.

Uses pytest to assert that install and uninstall correctly modify the .pth file.
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

from click.testing import CliRunner
from profall.cli import cli, get_site_packages_dir


def test_get_site_packages_dir() -> None:
    """Test getting the site-packages directory."""
    dir_path = get_site_packages_dir()
    assert isinstance(dir_path, Path)


@patch("profall.cli.get_site_packages_dir")
def test_install_success(mock_get_dir: MagicMock, tmp_path: Path) -> None:
    """Test successful installation of the .pth hook."""
    mock_get_dir.return_value = tmp_path

    runner = CliRunner()
    result = runner.invoke(cli, ["install"])

    assert result.exit_code == 0
    assert "Successfully installed hook" in result.output

    pth_file = tmp_path / "profall.pth"
    assert pth_file.exists()
    assert pth_file.read_text() == "import profall.hook\n"


@patch("profall.cli.get_site_packages_dir")
def test_install_permission_error(mock_get_dir: MagicMock, tmp_path: Path) -> None:
    """Test handling of permission error during install."""
    mock_get_dir.return_value = tmp_path

    with patch("pathlib.Path.write_text", side_effect=PermissionError):
        runner = CliRunner()
        result = runner.invoke(cli, ["install"])

        assert result.exit_code == 1
        assert "Permission denied" in result.output


@patch("profall.cli.get_site_packages_dir")
def test_uninstall_success(mock_get_dir: MagicMock, tmp_path: Path) -> None:
    """Test successful uninstallation of the .pth hook."""
    mock_get_dir.return_value = tmp_path
    pth_file = tmp_path / "profall.pth"
    pth_file.write_text("import profall.hook\n")

    runner = CliRunner()
    result = runner.invoke(cli, ["uninstall"])

    assert result.exit_code == 0
    assert "Successfully removed hook" in result.output
    assert not pth_file.exists()


@patch("profall.cli.get_site_packages_dir")
def test_uninstall_not_found(mock_get_dir: MagicMock, tmp_path: Path) -> None:
    """Test uninstallation when the .pth hook does not exist."""
    mock_get_dir.return_value = tmp_path

    runner = CliRunner()
    result = runner.invoke(cli, ["uninstall"])

    assert result.exit_code == 0
    assert "Hook not found" in result.output


@patch("profall.cli.get_site_packages_dir")
def test_uninstall_permission_error(mock_get_dir: MagicMock, tmp_path: Path) -> None:
    """Test handling of permission error during uninstall."""
    mock_get_dir.return_value = tmp_path
    pth_file = tmp_path / "profall.pth"
    pth_file.write_text("import profall.hook\n")

    with patch("pathlib.Path.unlink", side_effect=PermissionError):
        runner = CliRunner()
        result = runner.invoke(cli, ["uninstall"])

        assert result.exit_code == 1
        assert "Permission denied" in result.output
