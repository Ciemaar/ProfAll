"""Command-line interface for managing ProfAll.

This module provides a CLI using `click` to easily install or remove
the `profall.pth` hook file into the Python environment's site-packages.
"""

import site
import sys
from pathlib import Path

import click


def get_site_packages_dir() -> Path:
    """Gets the primary site-packages directory.

    Returns:
        The Path to the primary site-packages directory.
    """
    if getattr(site, "ENABLE_USER_SITE", False):
        return Path(site.getusersitepackages())
    return Path(site.getsitepackages()[0])


@click.group()
def cli() -> None:
    """Manage the ProfAll global profiler."""
    pass


@cli.command()
def install() -> None:
    """Install the profall.pth hook into the Python environment."""
    sp_dir = get_site_packages_dir()
    pth_file = sp_dir / "profall.pth"

    try:
        # Write the hook logic directly to the .pth file.
        # This tells python to import the hook module when starting up.
        pth_file.write_text("import profall.hook\n")
        click.echo(f"Successfully installed hook to {pth_file}")
    except PermissionError:
        click.echo(
            f"Permission denied. Cannot write to {sp_dir}. " "Try running with sudo or as administrator.",
            err=True,
        )
        sys.exit(1)
    except Exception as e:
        click.echo(f"Failed to install hook: {e}", err=True)
        sys.exit(1)


@cli.command()
def uninstall() -> None:
    """Remove the profall.pth hook from the Python environment."""
    sp_dir = get_site_packages_dir()
    pth_file = sp_dir / "profall.pth"

    if not pth_file.exists():
        click.echo(f"Hook not found at {pth_file}. Nothing to remove.")
        return

    try:
        pth_file.unlink()
        click.echo(f"Successfully removed hook from {pth_file}")
    except PermissionError:
        click.echo(
            f"Permission denied. Cannot remove {pth_file}. " "Try running with sudo or as administrator.",
            err=True,
        )
        sys.exit(1)
    except Exception as e:
        click.echo(f"Failed to remove hook: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    cli()
