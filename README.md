# pandaviz

Better-looking bar, line, and histogram charts on top of pandas — a small,
opinionated styling layer so your plots look clean without fussing over
matplotlib defaults.

## Install

```bash
pip install -e .
```

> **Dependencies:** `pandas` for data and `matplotlib` for rendering. Charts are
> drawn on a matplotlib `Axes`, so you can keep customizing after the fact.

## Usage

```python
import pandas as pd
import pandaviz as pv

df = pd.DataFrame({
    "category": ["Alpha", "Beta", "Gamma", "Delta"],
    "sales":    [420, 310, 260, 190],
    "costs":    [200, 220, 180, 140],
})

# Single-series bar (with direct value labels)
pv.bar(df, "category", "sales", title="Sales by Category")

# Grouped bars
pv.bar(df, "category", ["sales", "costs"], title="Sales vs Costs")

# Line chart with one or more series
pv.line(df, ["sales", "costs"], x="category", title="Trend")

# Histogram from a Series or a DataFrame column
pv.hist(df, "sales", bins=20, title="Distribution of Sales")
```

Every function returns the matplotlib `Axes`, so you can tweak it or save it:

```python
ax = pv.bar(df, "category", "sales", title="Sales")
ax.figure.savefig("sales.png", dpi=150)
```

## API

| Function | Purpose |
|----------|---------|
| `bar(df, x, y, ...)`   | Vertical or `horizontal=True` bars; `y` can be a list for grouped bars. |
| `line(df, y, x=None, ...)` | One or more overlaid line series. |
| `hist(data, column=None, ...)` | Distribution of a Series or a DataFrame column. |

Common keyword arguments: `title`, `xlabel`, `ylabel`, `color`, `figsize`, and
`ax` (to draw into an existing subplot).

## Styling

Charts use a fixed, colorblind-safe categorical palette, hairline gridlines,
no top/right borders, and a legend only when there is more than one series —
so a set of charts reads as one consistent system.
