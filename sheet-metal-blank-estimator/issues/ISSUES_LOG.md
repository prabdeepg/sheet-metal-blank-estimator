# Issues Log — Sheet Metal Blank Estimator

---

## ISSUE-001 — Springback Not Accounted For
**Status:** Known Limitation  
**Severity:** Medium  

**Description:**  
The bend allowance calculation computes the flat blank correctly, but does not account for springback. After bending, the part springs back partially, so the actual bent angle is slightly less than the tooling angle. This affects the final folded dimensions.

**Springback Approximation:**
Springback angle ≈ 3×σy×R / (E×t)  (for elastic springback)
Where σy = yield strength, R = bend radius, E = elastic modulus, t = thickness.

For 304 SS at ir/t = 2: springback ≈ 2–4°. Tool must overbend by this amount.

**Fix (Planned):**  
Add `--springback` flag that calculates overbend angle needed and adjusts tooling angle recommendation.

---

## ISSUE-002 — Sheet Utilization Only Considers Rectangular Nesting
**Status:** Known Limitation  
**Severity:** Low  

**Description:**  
The utilization calculation assumes axis-aligned rectangular nesting. Rotated or mirrored nesting (common in actual sheet metal shops) can achieve 10–20% better utilization.

**Fix (Partial):**  
Added a note in output: "Rectangular nesting only. Actual shop nesting may improve utilization by 10–20%."

---

## ISSUE-003 — K-Factor Lookup Extrapolates for ir/t > 8
**Status:** Resolved  
**Severity:** Low  

**Description:**  
For very large bend radii (ir/t > 8), the K-factor table only has data up to ir/t = 8. The tool was returning 0.44 for all large radii without warning.

**Fix:**  
Added clamp at the table maximum with a note: "Large radius (ir/t > 8): K-factor capped at table maximum {k}. Actual K approaches 0.50 for ir/t >> 8."

---

## ISSUE-004 — Negative Blank Dimension for Parts Wider Than Sheet
**Status:** Resolved  
**Severity:** High  

**Description:**  
If developed length > sheet length, `parts_per_sheet_l` = 0, and `parts_per_sheet` = 0. Division by zero when calculating utilization.

**Root Cause:**  
No guard for `parts_per_sheet < 1`.

**Fix:**  
Added: `if parts_per_sheet < 1: parts_per_sheet = 1`. Added warning: "WARNING: Part developed length ({dev_l:.1f} mm) exceeds sheet length ({sheet_l} mm). Part must be nested on a larger sheet or cut from multiple pieces."
