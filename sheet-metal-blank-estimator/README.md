# Sheet Metal Blank Weight Estimator

A Python tool that calculates the flat blank dimensions, weight, material cost, and sheet utilization efficiency for sheet metal parts. Given a part's folded geometry or flat pattern dimensions, the tool outputs everything needed for quoting and procurement.

## Features
- Bend allowance calculation (K-factor method, ASME/SMA)
- Developed length from bend angle, radius, and material thickness
- Flat pattern bounding box dimensions
- Blank weight from density and calculated volume
- Material cost per part (stock sheet size + scrap fraction)
- Sheet utilization % for nested layout (rows × columns)
- Supports 10 common sheet metal materials
- Supports gauge number → thickness lookup (US Standard & Manufacturers' Standard)

## Quick Start
```bash
python code/blank_estimator.py
```

## Example Output
```
══════════════════════════════════════════════════════
  SHEET METAL BLANK ESTIMATOR
══════════════════════════════════════════════════════
  Material       : 304 Stainless Steel
  Thickness      : 1.626 mm  (16 ga)
  Part dims      : 200 mm × 150 mm  (folded)
  Bends          : 2 × 90°  R=3.2mm  K=0.44
──────────────────────────────────────────────────────
  Bend Allowance : 3.84 mm per bend
  Developed L    : 210.68 mm
  Developed W    : 160.68 mm
  Blank Area     : 33,834 mm²  (339 cm²)
  Blank Weight   : 0.440 kg
  Material Cost  : $1.67/part  (at $3.80/kg)
  Scrap %        : 18.4 %  on 1000×2000mm sheet
  Sheet Yield    : 8 parts/sheet
══════════════════════════════════════════════════════
```

## Repository Structure
```
sheet-metal-blank-estimator/
├── code/
│   ├── blank_estimator.py       # Main estimator
│   ├── bend_allowance.py        # Bend calc library
│   └── gauge_table.py           # Gauge → thickness lookup
├── calculations/
│   ├── bend_theory.md           # K-factor, BA, OSSB derivations
│   └── worked_examples.py       # Step-by-step examples
├── bom/
│   ├── BOM.md
│   └── bom.csv
├── docs/
│   ├── usage_guide.md
│   └── material_properties.md
├── issues/
│   └── ISSUES_LOG.md
├── results/
│   └── RESULTS.md
└── tests/
    └── test_bends.py
```

## Supported Materials
6061-T6 Al, 5052-H32 Al, 304 SS, 316 SS, 1018 CRS, Galvanized Steel, C260 Brass, C110 Copper, Titanium Gr2, Mild Steel HR

## Author
Prabdeep Singh Ghatora | [github.com/prabdeepg](https://github.com/prabdeepg)
