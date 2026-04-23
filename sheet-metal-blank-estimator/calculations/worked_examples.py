"""
Worked calculation examples for sheet metal blank estimation.
"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))
from bend_allowance import bend_allowance, get_k_factor

print("=" * 60)
print("EXAMPLE 1: Single 90° Bend, 304 SS 16ga")
print("=" * 60)

t    = 1.626  # mm (16 gauge USS)
ir   = 3.2    # mm inner radius
mat  = "304 SS"
ang  = 90     # degrees

K = get_k_factor(mat, ir, t)
print(f"\nMaterial: {mat}, t = {t} mm, ir = {ir} mm")
print(f"ir/t ratio = {ir/t:.2f}")
print(f"K-factor (interpolated) = {K:.3f}")

BA = bend_allowance(ang, ir, t, material=mat)
print(f"\nBend Allowance:")
print(f"  BA = (π/180) × {ang}° × ({ir} + {K:.3f} × {t})")
print(f"  BA = {math.radians(ang):.4f} × {ir + K*t:.4f}")
print(f"  BA = {BA:.3f} mm")

OSSB = math.tan(math.radians(ang/2)) * (ir + t)
BD   = 2*OSSB - BA
print(f"\nOutside Setback: OSSB = tan(45°) × ({ir} + {t}) = {OSSB:.3f} mm")
print(f"Bend Deduction:  BD = 2×{OSSB:.3f} − {BA:.3f} = {BD:.3f} mm")

print()
print("=" * 60)
print("EXAMPLE 2: U-Channel Developed Length")
print("=" * 60)

flanges = 50  # mm
web     = 200 # mm
n_bends = 2
total_BA = n_bends * BA
dev_len  = flanges + total_BA/2 + web + total_BA/2 + flanges
# More directly:
dev_len2 = flanges + BA + web + BA + flanges
print(f"\nLeg 1 = {flanges}mm, Web = {web}mm, Leg 2 = {flanges}mm")
print(f"BA per bend = {BA:.3f} mm")
print(f"Developed Length = {flanges} + {BA:.3f} + {web} + {BA:.3f} + {flanges}")
print(f"                 = {dev_len2:.2f} mm")

# Weight check
density_gcc = 8.00  # 304 SS
width_mm = 150
area_mm2 = dev_len2 * width_mm
vol_mm3  = area_mm2 * t
weight_g = vol_mm3 * density_gcc / 1000
print(f"\nFor part width = {width_mm}mm:")
print(f"  Blank area  = {dev_len2:.2f} × {width_mm} = {area_mm2:.0f} mm²")
print(f"  Volume      = {vol_mm3:.0f} mm³")
print(f"  Weight      = {weight_g:.1f} g  ({weight_g/1000:.4f} kg)")
