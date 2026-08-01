"""simpleviz_dgsidhu — better-looking bar, line, and histogram charts on top of pandas."""
from .core import bar, line, hist, PALETTE

__all__ = ["bar", "line", "hist", "PALETTE"]
__version__ = "0.5.0"


def _enable_notebook_display():
    """Turn on inline plotting when imported inside a Jupyter kernel, so charts
    render automatically without the caller needing `%matplotlib inline` or
    `plt.show()`. A no-op in plain scripts or the terminal."""
    try:
        from IPython import get_ipython
        ip = get_ipython()
        if ip is not None and hasattr(ip, "kernel"):  # a Jupyter/ZMQ kernel
            ip.run_line_magic("matplotlib", "inline")
    except Exception:
        pass


_enable_notebook_display()
