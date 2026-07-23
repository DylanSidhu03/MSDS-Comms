"""pandaviz — better-looking bar, line, and histogram charts on top of pandas."""
from .core import bar, line, hist, PALETTE
from . import vangogh

__all__ = ["bar", "line", "hist", "PALETTE", "vangogh"]
__version__ = "0.2.0"
