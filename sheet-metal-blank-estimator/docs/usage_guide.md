# Usage Guide — Sheet Metal Blank Estimator

## Quick Start

```bash
python code/blank_estimator.py --demo
```

## Input Parameters

| Parameter | Description | Example |
|---|---|---|
| material | Material name from database | "304 SS" |
| thickness_mm | Sheet thickness in mm | 1.626 |
| folded_l | Folded part length (outer) | 200 |
| folded_w | Folded part width (outer) | 150 |
| bends_l | Bend list for length direction | [{angle:90, ir:3.2}] |
| bends_w | Bend list for width direction | [{angle:90, ir:3.2}] |
| sheet_l | Stock sheet length | 1000 |
| sheet_w | Stock sheet width | 2000 |

## Bend Dictionary Format

```python
bend = {
    "angle":    90,        # Bend angle in degrees
    "ir":       3.2,       # Inner radius in mm
    "t":        1.626,     # Thickness (optional, uses part thickness if omitted)
    "material": "304 SS",  # Material (for K-factor lookup)
    "k":        0.44,      # Explicit K-factor (overrides material lookup)
}
```

## Gauge Lookup

```python
from code.gauge_table import gauge_to_mm, mm_to_nearest_gauge

t = gauge_to_mm(16, "USS")          # → 1.519 mm
ga, t = mm_to_nearest_gauge(1.626)  # → (16, 1.519)
```

## Common Stock Sheet Sizes
| Sheet Size (mm) | Common Use |
|---|---|
| 1000 × 2000 | Standard metric sheet |
| 1219 × 2438 | 4' × 8' imperial |
| 1219 × 3048 | 4' × 10' imperial |
| 1524 × 3048 | 5' × 10' imperial |

## Interpreting Results

**Developed dimensions** = actual flat blank size to cut/shear from stock.

**K-factor** = neutral axis location (auto-looked-up from material + ir/t ratio).

**Sheet utilization** = fraction of stock sheet used by parts (rectangular nesting only — actual nesting software may achieve higher utilization with rotation/mirroring).

**Scrap %** = 100 − utilization %. Includes edge trim, gap between parts, and leftover strips.
