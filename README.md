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

# Single-series bar: rounded bars + direct value labels
pv.bar(df, "category", "sales",
       title="Sales by Category",
       subtitle="Quarterly revenue across product lines",
       ylabel="USD (thousands)",
       caption="Source: internal demo data")

# Grouped bars (top-left horizontal legend), or horizontal=True
pv.bar(df, "category", ["sales", "costs"], title="Sales vs Costs")

# Line chart; single series gets a soft area fill, markers are ringed
pv.line(df, ["sales", "costs"], x="category", title="Trend")

# Histogram with an annotated mean line
pv.hist(df, "sales", bins=20, title="Distribution of Sales")
```

Every chart supports `title`, `subtitle`, and `caption` for a clean text
hierarchy, plus `xlabel`, `ylabel`, `color`, `figsize`, and `ax`.

Every function returns the matplotlib `Axes`, so you can tweak it or save it:

```python
ax = pv.bar(df, "category", "sales", title="Sales")
ax.figure.savefig("sales.png", dpi=150)
```

## API

| Function | Purpose | Notable options |
|----------|---------|-----------------|
| `bar(df, x, y, ...)`   | Vertical or horizontal bars; `y` can be a list for grouped bars. | `horizontal`, `value_labels`, `rounded` |
| `line(df, y, x=None, ...)` | One or more overlaid line series. | `markers`, `area` |
| `hist(data, column=None, ...)` | Distribution of a Series or a DataFrame column. | `bins`, `mean_line`, `rounded` |

All three also accept `title`, `subtitle`, `caption`, `xlabel`, `ylabel`,
`color`, `figsize`, and `ax` (to draw into an existing subplot).

## Styling

Charts share one deliberate, modern look so a set of them reads as a single system:

- An earthy palette whose three mains are a **sage green, a light washed brown,
  and a slate grey**, backed by deeper earth tones, applied in a set order so
  series stay distinguishable.
- **Softly rounded** bars, ringed line markers, and an optional area fill.
- A clean **title / subtitle / caption** hierarchy in a modern sans-serif.
- Hairline gridlines, a single baseline (no boxed-in axes), thousands-separated
  ticks, and a crisp white plot area on a soft cool-grey page.
- A legend only when there is more than one series.
