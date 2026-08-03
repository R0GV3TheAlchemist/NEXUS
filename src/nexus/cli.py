"""NEXUS CLI.

Copyright (c) 2026 Kyle Alexander Steen.
"""

from .version import __author__, __version__


def version_text() -> str:
    return f"NEXUS {__version__} by {__author__}"
