"""Better-looking bar, line, and histogram charts built on pandas + matplotlib."""
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch
from matplotlib.ticker import FuncFormatter

# Earthy "Sage, Stone & Clay" palette: the three mains are a sage green, a light
# washed brown, and a slate grey, backed by deeper green/brown/grey earth tones.
PALETTE = ["#5e8f77", "#c8b79f", "#5c6b6a", "#2f5147",
           "#9c8468", "#bcc4c2", "#8a9e95", "#ded3c2"]
INK, SECONDARY, MUTED = "#363330", "#6b655c", "#a09a8f"
GRID, BASELINE, SURFACE, PAGE = "#eae7e0", "#d4cfc4", "#fcfbf8", "#f1eee7"
_AVAIL = {f.name for f in font_manager.fontManager.ttflist}
FONT = next((f for f in ("Inter", "Helvetica Neue", "Helvetica", "Arial",
                         "Segoe UI", "DejaVu Sans") if f in _AVAIL), "sans-serif")


def _fmt(v):
    """Compact, thousands-separated tick/label formatting."""
    if abs(v) >= 1000 and v == int(v):
        return f"{int(v):,}"
    if v == int(v):
        return f"{int(v)}"
    return f"{v:,.2f}".rstrip("0").rstrip(".")


def _new_ax(ax, figsize):
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig = ax.figure
    fig.patch.set_facecolor(PAGE)
    ax.set_facecolor(SURFACE)
    return fig, ax


def _style_ax(ax, xlabel, ylabel, grid_axis="y", fmt_axis="y"):
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(BASELINE)
    ax.spines["bottom"].set_linewidth(1.2)
    ax.tick_params(colors=MUTED, labelsize=9.5, length=0, pad=6)
    for lbl in ax.get_xticklabels() + ax.get_yticklabels():
        lbl.set_fontfamily(FONT)
    ax.set_axisbelow(True)
    grid = getattr(ax, f"{grid_axis}axis")
    grid.grid(True, color=GRID, linewidth=1.0)
    getattr(ax, f"{fmt_axis}axis").set_major_formatter(FuncFormatter(lambda v, _: _fmt(v)))
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=10.5, color=SECONDARY, labelpad=8, fontfamily=FONT)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=10.5, color=SECONDARY, labelpad=8, fontfamily=FONT)


def _round_bars(ax, bars, horizontal, radius_px=6):
    """Replace rectangular bars with softly rounded ones (equal pixel radius)."""
    fig = ax.figure
    fig.canvas.draw()
    ext = ax.get_window_extent()
    (x0, x1), (y0, y1) = ax.get_xlim(), ax.get_ylim()
    xppx, yppx = (x1 - x0) / ext.width, (y1 - y0) / ext.height
    rsize, aspect = radius_px * xppx, yppx / xppx
    for rect in bars:
        (bx, by), bw, bh = rect.get_xy(), rect.get_width(), rect.get_height()
        fc = rect.get_facecolor()
        rect.set_visible(False)
        span = abs(bh) if horizontal else abs(bw)
        r = min(rsize, span / 2)
        ax.add_patch(FancyBboxPatch(
            (bx, by), bw, bh, boxstyle=f"round,pad=0,rounding_size={r}",
            mutation_aspect=aspect, fc=fc, ec="none", zorder=rect.get_zorder(),
            clip_on=False))


def _finish(fig, ax, title, subtitle, caption, labels):
    """Titles, caption, and a top-left horizontal legend, cleanly spaced."""
    n = len(labels)
    top = 0.99 - 0.055 * (bool(title) + bool(subtitle)) - (0.05 if n > 1 else 0)
    fig.subplots_adjust(left=0.10, right=0.965, top=top,
                        bottom=0.16 if caption else 0.12)
    pos = ax.get_position()
    if n > 1:
        leg = ax.legend(labels, loc="lower left", bbox_to_anchor=(0, 1.01),
                        ncol=min(n, 4), frameon=False, fontsize=9.5,
                        handlelength=1.1, handletextpad=0.5, columnspacing=1.5,
                        borderaxespad=0, labelcolor=INK)
        for t in leg.get_texts():
            t.set_fontfamily(FONT)
    if title:
        fig.text(pos.x0, 0.965, title, ha="left", va="top", fontsize=15.5,
                 fontweight="bold", color=INK, fontfamily=FONT)
    if subtitle:
        fig.text(pos.x0, 0.965 - (0.058 if title else 0), subtitle, ha="left",
                 va="top", fontsize=10.5, color=SECONDARY, fontfamily=FONT)
    if caption:
        fig.text(pos.x0, 0.035, caption, ha="left", va="bottom", fontsize=8.5,
                 color=MUTED, fontfamily=FONT)


def bar(df, x, y, *, ax=None, title=None, subtitle=None, caption=None,
        xlabel=None, ylabel=None, color=None, horizontal=False,
        value_labels=True, rounded=True, figsize=(8.5, 5.2)):
    """Bar chart. `y` may be a single column name or a list for grouped bars."""
    cols = [y] if isinstance(y, str) else list(y)
    fig, ax = _new_ax(ax, figsize)
    n, width = len(df), 0.78 / (1 if isinstance(y, str) else len(y))
    labels = df[x].astype(str).tolist()
    vmax = max(df[c].max() for c in cols)
    for i, col in enumerate(cols):
        offset = (i - (len(cols) - 1) / 2) * width
        pos = [p + offset for p in range(n)]
        c = color if (color and len(cols) == 1) else PALETTE[i % len(PALETTE)]
        plot_fn = ax.barh if horizontal else ax.bar
        size_kw = {"height": width * 0.92} if horizontal else {"width": width * 0.92}
        bars = plot_fn(pos, df[col], color=c, label=col, zorder=3, **size_kw)
        if value_labels and len(cols) == 1:
            for rect in bars:
                v = rect.get_width() if horizontal else rect.get_height()
                if horizontal:
                    ax.text(v + vmax * 0.01, rect.get_y() + rect.get_height() / 2,
                            _fmt(v), va="center", ha="left", fontsize=9,
                            color=SECONDARY, fontfamily=FONT)
                else:
                    ax.text(rect.get_x() + rect.get_width() / 2, v + vmax * 0.02,
                            _fmt(v), va="bottom", ha="center", fontsize=9,
                            color=SECONDARY, fontfamily=FONT)
    if horizontal:
        ax.set_yticks(range(n)); ax.set_yticklabels(labels)
        ax.set_xlim(0, vmax * 1.15); ax.invert_yaxis()
        _style_ax(ax, xlabel or (cols[0] if len(cols) == 1 else None), ylabel or x,
                  grid_axis="x", fmt_axis="x")
    else:
        ax.set_xticks(range(n))
        rot, ha = (30, "right") if n > 8 else (0, "center")
        ax.set_xticklabels(labels, rotation=rot, ha=ha)
        ax.set_ylim(0, vmax * 1.18)
        _style_ax(ax, xlabel or x, ylabel or (cols[0] if len(cols) == 1 else None))
    _finish(fig, ax, title, subtitle, caption, cols)
    if rounded:
        for cont in ax.containers:
            _round_bars(ax, cont, horizontal)
    return ax


def line(df, y, x=None, *, ax=None, title=None, subtitle=None, caption=None,
         xlabel=None, ylabel=None, markers=True, area=None, figsize=(8.5, 5.2)):
    """Line chart. `y` may be a single column name or a list of columns to overlay."""
    cols = [y] if isinstance(y, str) else list(y)
    fig, ax = _new_ax(ax, figsize)
    xvals = df[x] if x else df.index
    show_markers = markers and len(df) <= 30
    for i, col in enumerate(cols):
        c = PALETTE[i % len(PALETTE)]
        ax.plot(xvals, df[col], color=c, linewidth=2.4, label=col, zorder=3,
                solid_capstyle="round", solid_joinstyle="round",
                marker="o" if show_markers else None, markersize=6,
                markeredgecolor=SURFACE, markeredgewidth=1.6)
    if (area if area is not None else len(cols) == 1):
        for i, col in enumerate(cols):
            ax.fill_between(xvals, df[col], ax.get_ylim()[0], zorder=2,
                            color=PALETTE[i % len(PALETTE)], alpha=0.10, linewidth=0)
    ax.margins(x=0.02)
    _style_ax(ax, xlabel or (x or ""), ylabel or (cols[0] if len(cols) == 1 else None))
    _finish(fig, ax, title, subtitle, caption, cols)
    return ax


def hist(data, column=None, *, bins=30, ax=None, title=None, subtitle=None,
         caption=None, xlabel=None, ylabel="Frequency", color=None,
         mean_line=True, rounded=True, figsize=(8.5, 5.2)):
    """Histogram over a Series, or a DataFrame + `column`."""
    values = (data[column] if isinstance(data, pd.DataFrame) else data).dropna()
    fig, ax = _new_ax(ax, figsize)
    c = color or PALETTE[0]
    counts, edges, patches = ax.hist(values, bins=bins, color=c, edgecolor=SURFACE,
                                     linewidth=1.2, zorder=3, rwidth=0.96)
    ax.set_ylim(0, counts.max() * 1.12)
    if mean_line:
        m = values.mean()
        ax.axvline(m, color=SECONDARY, linewidth=1.4, dashes=(4, 3), zorder=4)
        ax.text(m, counts.max() * 1.12, f" mean {_fmt(m)}", va="top", ha="left",
                fontsize=9, color=SECONDARY, fontfamily=FONT)
    _style_ax(ax, xlabel or column or values.name, ylabel)
    _finish(fig, ax, title, subtitle, caption, [column or values.name or ""])
    if rounded:
        _round_bars(ax, patches, horizontal=False, radius_px=4)
    return ax
