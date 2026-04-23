# Bend Theory — K-Factor, Bend Allowance, Developed Length

## 1. The Neutral Axis and K-Factor

When sheet metal is bent, the outer surface stretches and the inner surface compresses. Somewhere between them lies the **neutral axis** — the theoretical surface where no strain occurs. Material on the neutral axis neither stretches nor compresses.

The **K-factor** defines the location of the neutral axis as a fraction of the material thickness measured from the inner bend surface:

```
neutral axis location = K × t  (from inner surface)
```

For a sharp bend (ir/t → 0): K ≈ 0.33 (neutral axis at 1/3 of thickness)
For a large radius bend (ir/t > 8): K → 0.50 (neutral axis at midpoint)

Typical K-factors:
| Material | ir/t = 0 | ir/t = 1 | ir/t = 4 |
|---|---|---|---|
| Soft aluminum (5052) | 0.33 | 0.38 | 0.42 |
| Hard aluminum (6061) | 0.38 | 0.41 | 0.45 |
| Mild steel | 0.33 | 0.38 | 0.44 |
| Stainless steel | 0.38 | 0.42 | 0.46 |

---

## 2. Bend Allowance (BA)

The bend allowance is the arc length along the neutral axis through the bend:

```
BA = (π/180) × θ × (ir + K × t)
```

Where:
- θ = bend angle (degrees) — the INCLUDED angle (90° for a 90° bend)
- ir = inner bend radius [mm]
- K = K-factor
- t = material thickness [mm]

**Example:** 90° bend, 304 SS, t = 1.626mm, ir = 3.2mm, K = 0.44

```
BA = (π/180) × 90 × (3.2 + 0.44 × 1.626)
   = (π/2) × (3.2 + 0.715)
   = 1.5708 × 3.915
   = 6.148 mm
```

---

## 3. Outside SetBack (OSSB)

The setback is the distance from the apex of the bend to the tangent point (mold line):

```
OSSB = tan(θ/2) × (ir + t)
```

For 90°: OSSB = tan(45°) × (ir + t) = 1.000 × (ir + t)

---

## 4. Bend Deduction (BD)

Bend deduction relates the flat blank dimension to the folded dimension:

```
BD = 2 × OSSB − BA
```

Flat blank leg = folded leg − BD/2  (per leg)

Or equivalently:
Developed length = sum of flat legs + sum of BAs (per bend)

---

## 5. Developed Length Derivation

For a part with flat legs [L1, L2, L3] and bends [B1, B2]:

```
DL = L1 + BA₁ + L2 + BA₂ + L3
```

Each bend contributes its bend allowance to the total flat length.

**Example:** Simple U-channel, 200mm wide × 50mm flanges, 304 SS 1.626mm, 90° bends
- L1 = 50mm, L2 = 200mm, L3 = 50mm
- BA per bend = 6.148mm
- DL = 50 + 6.148 + 200 + 6.148 + 50 = **312.3 mm**
