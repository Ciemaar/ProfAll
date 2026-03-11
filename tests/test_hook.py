"""Tests for the hook module.

Ensures that the hook runs correctly on import.
"""

from unittest.mock import patch


def test_hook_import() -> None:
    """Test that importing the hook module calls install_hooks."""
    with patch("profall.core.install_hooks") as mock_install:
        # We need to reload the module since it might be cached by pytest
        import importlib

        import profall.hook

        importlib.reload(profall.hook)

        assert mock_install.called
