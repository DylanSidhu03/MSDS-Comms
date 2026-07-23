"""Better-looking bar, line, and histogram charts built on pandas + matplotlib."""
import pandas as pd
import matplotlib.pyplot as plt

PALETTE = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100",
           "#e87ba4", "#008300", "#4a3aa7", "#e34948"]
INK, INK_MUTED, GRID, SURFACE = "#0b0b0b", "#52514e", "#e1e0d9", "#fcfcfb"


def _new_ax(ax, figsize):
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig = ax.figure
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)
    return fig, ax


def _style_ax(ax, title, xlabel, ylabel, grid_axis="y"):
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(GRID)
    ax.tick_params(colors=INK_MUTED, labelsize=9, length=0)
    ax.set_axisbelow(True)
    if grid_axis == "y":
        ax.yaxis.grid(True, color=GRID, linewidth=0.8)
    elif grid_axis == "x":
        ax.xaxis.grid(True, color=GRID, linewidth=0.8)
    if title:
        ax.set_title(title, fontsize=13, fontweight="bold", color=INK, loc="left", pad=12)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=10, color=INK_MUTED)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=10, color=INK_MUTED)


def _legend(ax, n_series):
    if n_series > 1:
        ax.legend(frameon=False, fontsize=9, labelcolor=INK,
                   loc="upper left", bbox_to_anchor=(1.0, 1.0))


def bar(df, x, y, *, ax=None, title=None, xlabel=None, ylabel=None, color=None,
         horizontal=False, value_labels=True, figsize=(8, 5)):
    """Bar chart. `y` may be a single column name or a list for grouped bars."""
    cols = [y] if isinstance(y, str) else list(y)
    fig, ax = _new_ax(ax, figsize)
    n = len(df)
    width = 0.8 / len(cols)
    labels = df[x].astype(str).tolist()
    for i, col in enumerate(cols):
        offset = (i - (len(cols) - 1) / 2) * width
        pos = [p + offset for p in range(n)]
        c = color if (color and len(cols) == 1) else PALETTE[i % len(PALETTE)]
        plot_fn = ax.barh if horizontal else ax.bar
        size_kw = {"height": width * 0.9} if horizontal else {"width": width * 0.9}
        bars = plot_fn(pos, df[col], color=c, label=col, zorder=3, **size_kw)
        if value_labels and len(cols) == 1:
            for rect in bars:
                if horizontal:
                    w = rect.get_width()
                    ax.text(w, rect.get_y() + rect.get_height() / 2, f" {w:,.0f}",
                            va="center", ha="left", fontsize=9, color=INK)
                else:
                    h = rect.get_height()
                    ax.text(rect.get_x() + rect.get_width() / 2, h, f"{h:,.0f} ",
                            va="bottom", ha="center", fontsize=9, color=INK)
    if horizontal:
        ax.set_yticks(range(n))
        ax.set_yticklabels(labels)
        _style_ax(ax, title, xlabel or (cols[0] if len(cols) == 1 else None), ylabel or x, "x")
    else:
        ax.set_xticks(range(n))
        rot, ha = (45, "right") if n > 8 else (0, "center")
        ax.set_xticklabels(labels, rotation=rot, ha=ha)
        _style_ax(ax, title, xlabel or x, ylabel or (cols[0] if len(cols) == 1 else None))
    _legend(ax, len(cols))
    fig.tight_layout()
    return ax


def line(df, y, x=None, *, ax=None, title=None, xlabel=None, ylabel=None,
          markers=True, figsize=(8, 5)):
    """Line chart. `y` may be a single column name or a list of columns to overlay."""
    cols = [y] if isinstance(y, str) else list(y)
    fig, ax = _new_ax(ax, figsize)
    xvals = df[x] if x else df.index
    for i, col in enumerate(cols):
        ax.plot(xvals, df[col], color=PALETTE[i % len(PALETTE)], linewidth=2,
                 marker="o" if markers else None, markersize=5, label=col, zorder=3)
    _style_ax(ax, title, xlabel or x, ylabel or (cols[0] if len(cols) == 1 else None))
    _legend(ax, len(cols))
    fig.tight_layout()
    return ax


def hist(data, column=None, *, bins=30, ax=None, title=None, xlabel=None,
          ylabel="Frequency", color=None, figsize=(8, 5)):
    """Histogram over a Series, or a DataFrame + `column`."""
    values = data[column] if isinstance(data, pd.DataFrame) else data
    fig, ax = _new_ax(ax, figsize)
    ax.hist(values.dropna(), bins=bins, color=color or PALETTE[0],
             edgecolor=SURFACE, linewidth=0.5, zorder=3)
    _style_ax(ax, title, xlabel or column or values.name, ylabel)
    fig.tight_layout()
    return ax
