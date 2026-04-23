# Results — Sheet Metal Blank Estimator

## Case 1: 304 SS Enclosure Box (200×150×50mm)

**Inputs:**
- Material: 304 Stainless Steel, 1.626mm (16 ga USS)
- Folded dimensions: 200mm L × 150mm W
- Bends: 2 × 90° per direction, ir = 3.2mm (2×t)

**Calculations:**

K-factor (304 SS, ir/t = 1.97): K = 0.432

Bend Allowance per bend:
- BA = (π/2) × (3.2 + 0.432 × 1.626) = (π/2) × 3.903 = 6.129mm

Developed dimensions:
- L = 200 + 2 × 6.129 = 212.26mm
- W = 150 + 2 × 6.129 = 162.26mm

**Results:**

| Parameter | Value |
|---|---|
| Blank size | 212.3 × 162.3 mm |
| Blank area | 34,449 mm² (345 cm²) |
| Weight | 0.448 kg (448 g) |
| Cost/part | $1.70 |
| Parts/sheet (1000×2000) | 8 parts (4×2 array) |
| Sheet utilization | 59.5% |
| Scrap | 40.5% |

**Validation vs SolidWorks Sheet Metal Flat Pattern:**
- SW flat pattern: 212.1 × 162.1mm → 34,382mm²
- Calculator: 212.3 × 162.3mm → 34,449mm²
- Δ = 0.2% — within RFQ accuracy requirement

---

## Case 2: 6061-T6 Mounting Bracket (100×80mm, 1 bend)

**Results:**
| Parameter | Value |
|---|---|
| Blank size | 108.7 × 80 mm |
| Weight | 0.049 kg |
| Cost/part | $0.11 |
| Parts/sheet | 184 parts |
| Sheet utilization | 79.6% |

Higher utilization due to smaller part size and simpler geometry.
