"""A Van Gogh "Starry Night" theme for pandaviz: textured sky, impasto brushstrokes."""
import numpy as np
import pandas as pd
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch

# Series hues chosen to glow against a deep night sky (chrome yellow, cobalt, ...).
PALETTE = ["#f4d35e", "#8ecae6", "#a7c957", "#e07a5f",
           "#c8b6e2", "#e5989b", "#e9c46a", "#83c5be"]
SKY_BOT, SKY_TOP, SWIRL, STAR = "#0b1d33", "#2a5583", "#5b8fbf", "#f4d35e"
CREAM, GOLD, HAZE = "#efe6c8", "#f4d35e", "#8fa9c4"
_AVAIL = {f.name for f in font_manager.fontManager.ttflist}
FONT = next((f for f in ("Segoe Print", "Bradley Hand", "Chalkboard", "Comic Sans MS",
                         "DejaVu Sans") if f in _AVAIL), "sans-serif")


def _rgb(c):
    return np.array(mcolors.to_rgb(c))


def _mix(c1, c2, t):
    return _rgb(c1) * (1 - t) + _rgb(c2) * t


def _blur(a, k):
    for _ in range(k):
        a = (a + np.roll(a, 1, 0) + np.roll(a, -1, 0)
             + np.roll(a, 1, 1) + np.roll(a, -1, 1)) / 5
    return a


def _new_ax(ax, figsize):
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig = ax.figure
    fig.patch.set_facecolor(SKY_BOT)
    ax.set_facecolor(SKY_BOT)
    return fig, ax


def _swirl(ax, cx, cy, fx, fy, color, rng, zorder=1):
    """A faint logarithmic-spiral brushstroke, à la the sky of Starry Night."""
    th = np.linspace(0, rng.uniform(3.5, 5) * np.pi, 220)
    r = th / th[-1]
    ph = rng.uniform(0, 6.28)
    x = cx + fx * r * np.cos(th + ph)
    y = cy + fy * r * np.sin(th + ph)
    for lw, a in ((5, 0.12), (2.4, 0.22)):
        ax.plot(x, y, color=color, lw=lw, alpha=a, solid_capstyle="round", zorder=zorder)


def _sky(ax, seed, stars=True):
    """Paint a swirling, star-flecked night sky across the current axes limits."""
    (x0, x1), (y0, y1) = ax.get_xlim(), ax.get_ylim()
    H, W = 300, 450
    rng = np.random.default_rng(seed)
    t = np.linspace(0, 1, H)[:, None]
    base = _rgb(SKY_BOT)[None, None] * (1 - t)[..., None] + _rgb(SKY_TOP)[None, None] * t[..., None]
    img = np.repeat(base, W, axis=1)
    low = rng.normal(0, 1, (6, 9))
    tex = _blur(np.kron(low, np.ones((H // 6 + 1, W // 9 + 1)))[:H, :W], 22)
    tex = (tex - tex.min()) / (np.ptp(tex) + 1e-9)
    img = img * (1 - 0.4 * tex[..., None]) + _rgb(SWIRL)[None, None] * (0.4 * tex[..., None])
    ax.imshow(np.clip(img, 0, 1), extent=[x0, x1, y0, y1], origin="lower",
              aspect="auto", zorder=0, interpolation="bilinear")
    dx, dy = x1 - x0, y1 - y0
    for _ in range(3):
        _swirl(ax, rng.uniform(x0 + 0.1 * dx, x1 - 0.1 * dx),
               rng.uniform(y0 + 0.55 * dy, y1 - 0.05 * dy),
               rng.uniform(0.06, 0.13) * dx, rng.uniform(0.06, 0.13) * dy,
               STAR if rng.random() > 0.5 else "#cfe0f0", rng)
    if stars:
        sx = rng.uniform(x0, x1, 30)
        sy = rng.uniform(y0 + dy * 0.5, y1, 30)
        ax.scatter(sx, sy, s=rng.uniform(6, 45, 30), c=STAR, alpha=0.5,
                   edgecolors="none", zorder=1, marker="*")
    ax.set_xlim(x0, x1); ax.set_ylim(y0, y1)


def _style(ax, xlabel, ylabel):
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(HAZE)
    ax.spines["bottom"].set_alpha(0.6)
    ax.tick_params(colors=CREAM, labelsize=9.5, length=0, pad=6)
    for lbl in ax.get_xticklabels() + ax.get_yticklabels():
        lbl.set_fontfamily(FONT)
    ax.set_axisbelow(True)
    ax.grid(True, color=HAZE, linewidth=0.7, alpha=0.18)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=11, color=CREAM, labelpad=8,
                      fontfamily=FONT, fontstyle="italic")
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=11, color=CREAM, labelpad=8,
                      fontfamily=FONT, fontstyle="italic")


def _finish(fig, ax, title, subtitle, caption, labels):
    n = len(labels)
    top = 0.99 - 0.058 * (bool(title) + bool(subtitle)) - (0.05 if n > 1 else 0)
    fig.subplots_adjust(left=0.10, right=0.965, top=top,
                        bottom=0.16 if caption else 0.12)
    pos = ax.get_position()
    if n > 1:
        handles, lbls = ax.get_legend_handles_labels()
        leg = ax.legend(handles, lbls, loc="lower left", bbox_to_anchor=(0, 1.01),
                        ncol=min(n, 4), frameon=False, fontsize=10,
                        handlelength=1.1, handletextpad=0.5, columnspacing=1.5,
                        borderaxespad=0, labelcolor=CREAM)
        for txt in leg.get_texts():
            txt.set_fontfamily(FONT)
    if title:
        fig.text(pos.x0, 0.965, title, ha="left", va="top", fontsize=17,
                 fontweight="bold", color=GOLD, fontfamily=FONT)
    if subtitle:
        fig.text(pos.x0, 0.965 - (0.06 if title else 0), subtitle, ha="left",
                 va="top", fontsize=11, color=CREAM, fontfamily=FONT, fontstyle="italic")
    if caption:
        fig.text(pos.x0, 0.035, caption, ha="left", va="bottom", fontsize=9,
                 color=HAZE, fontfamily=FONT, fontstyle="italic")


def _impasto(ax, xs, ys, color, seed, zbase=3):
    """A wobbling, multi-layer brushstroke: shadow, body, and a bright highlight."""
    xs, ys = np.asarray(xs, float), np.asarray(ys, float)
    tt, dense = np.linspace(0, 1, len(xs)), np.linspace(0, 1, len(xs) * 24)
    xd, yd = np.interp(dense, tt, xs), np.interp(dense, tt, ys)
    rng = np.random.default_rng(seed)
    amp = (np.ptp(ys) + 1e-9) * 0.015
    wob = _blur(rng.normal(0, 1, (1, xd.size)), 9)[0]
    yd = yd + wob / (np.abs(wob).max() + 1e-9) * amp
    ax.plot(xd, yd, color=_mix(color, "#000000", 0.45), lw=8, alpha=0.45,
            solid_capstyle="round", solid_joinstyle="round", zorder=zbase)
    ax.plot(xd, yd, color=color, lw=4.5, solid_capstyle="round",
            solid_joinstyle="round", zorder=zbase + 1)
    ax.plot(xd, yd + amp * 0.7, color=_mix(color, "#ffffff", 0.5), lw=1.6,
            alpha=0.85, solid_capstyle="round", zorder=zbase + 2)


def _paint_bar(ax, x0, width, height, color, seed, radius=0.05):
    """A rounded bar filled with vertical impasto streaks and an edge highlight."""
    patch = FancyBboxPatch((x0, 0), width, height, mutation_aspect=1,
                           boxstyle=f"round,pad=0,rounding_size={min(radius, width/2)}",
                           fc=color, ec=_mix(color, "#000000", 0.3), lw=1.2, zorder=3)
    ax.add_patch(patch)
    rng = np.random.default_rng(seed)
    for cx in np.linspace(x0 + width * 0.12, x0 + width * 0.88, 9):
        shade = _mix(color, "#ffffff" if rng.random() > 0.5 else "#000000",
                     rng.uniform(0.1, 0.4))
        seg = ax.plot([cx, cx + rng.normal(0, width * 0.02)],
                      [height * rng.uniform(0.02, 0.12), height * rng.uniform(0.75, 0.99)],
                      color=shade, lw=2.4, alpha=0.5, solid_capstyle="round", zorder=4)[0]
        seg.set_clip_path(patch)
    return patch


def bar(df, x, y, *, ax=None, title=None, subtitle=None, caption=None,
        xlabel=None, ylabel=None, figsize=(8.5, 5.2)):
    """Van Gogh bar chart. `y` may be a single column or a list for grouped bars."""
    cols = [y] if isinstance(y, str) else list(y)
    fig, ax = _new_ax(ax, figsize)
    n, width = len(df), 0.78 / len(cols)
    vmax = max(df[c].max() for c in cols)
    ax.set_xlim(-0.6, n - 0.4); ax.set_ylim(0, vmax * 1.18)
    _sky(ax, seed=3)
    for i, col in enumerate(cols):
        c = PALETTE[i % len(PALETTE)]
        for p in range(n):
            xc = p + (i - (len(cols) - 1) / 2) * width
            _paint_bar(ax, xc - width * 0.46, width * 0.92, df[col].iloc[p],
                       c, seed=100 * i + p, radius=vmax * 0.04)
        ax.plot([], [], color=c, lw=6, label=col)
    ax.set_xticks(range(n)); ax.set_xticklabels(df[x].astype(str).tolist())
    _style(ax, xlabel or x, ylabel or (cols[0] if len(cols) == 1 else None))
    _finish(fig, ax, title, subtitle, caption, cols)
    return ax


def line(df, y, x=None, *, ax=None, title=None, subtitle=None, caption=None,
         xlabel=None, ylabel=None, figsize=(8.5, 5.2)):
    """Van Gogh line chart with undulating impasto strokes."""
    cols = [y] if isinstance(y, str) else list(y)
    fig, ax = _new_ax(ax, figsize)
    xpos, n = list(range(len(df))), len(df)
    vmin = min(df[c].min() for c in cols)
    vmax = max(df[c].max() for c in cols)
    pad = (vmax - vmin) * 0.12 + 1e-9
    ax.set_xlim(-0.4, n - 0.6); ax.set_ylim(vmin - pad, vmax + pad)
    _sky(ax, seed=5)
    for i, col in enumerate(cols):
        c = PALETTE[i % len(PALETTE)]
        _impasto(ax, xpos, df[col].values, c, seed=17 + i)
        if n <= 30:
            ax.scatter(xpos, df[col], s=40, c=c, edgecolors=CREAM,
                       linewidths=1.2, zorder=7)
        ax.plot([], [], color=c, lw=6, label=col)
    ax.set_xticks(xpos)
    labels = (df[x].astype(str).tolist() if x else [str(v) for v in df.index])
    ax.set_xticklabels(labels, rotation=30 if n > 8 else 0,
                       ha="right" if n > 8 else "center")
    _style(ax, xlabel or (x or ""), ylabel or (cols[0] if len(cols) == 1 else None))
    _finish(fig, ax, title, subtitle, caption, cols)
    return ax


def hist(data, column=None, *, bins=30, ax=None, title=None, subtitle=None,
         caption=None, xlabel=None, ylabel="Frequency", color=None, figsize=(8.5, 5.2)):
    """Van Gogh histogram: painted bars over a night sky, with a mean brushstroke."""
    values = (data[column] if isinstance(data, pd.DataFrame) else data).dropna()
    fig, ax = _new_ax(ax, figsize)
    c = color or PALETTE[0]
    counts, edges = np.histogram(values, bins=bins)
    ax.set_xlim(edges[0], edges[-1]); ax.set_ylim(0, counts.max() * 1.15)
    _sky(ax, seed=8, stars=False)
    for j in range(len(counts)):
        w = (edges[j + 1] - edges[j]) * 0.94
        _paint_bar(ax, edges[j] + (edges[j + 1] - edges[j]) * 0.03, w,
                   counts[j], c, seed=j, radius=(edges[1] - edges[0]) * 0.25)
    m = values.mean()
    ax.axvline(m, color=GOLD, linewidth=2, dashes=(4, 3), zorder=6)
    ax.text(m, counts.max() * 1.15, f" mean {m:,.1f}", va="top", ha="left",
            fontsize=10, color=GOLD, fontfamily=FONT, fontstyle="italic")
    _style(ax, xlabel or column or values.name, ylabel)
    _finish(fig, ax, title, subtitle, caption, [column or values.name or ""])
    return ax
