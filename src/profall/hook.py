"""Hook module to inject profall core logic when Python starts.

This file is loaded by the `profall.pth` file placed in site-packages.
"""

from profall.core import install_hooks

install_hooks()
