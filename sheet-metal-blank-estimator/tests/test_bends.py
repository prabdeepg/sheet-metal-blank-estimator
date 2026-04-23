"""
Tests for bend allowance and blank estimator.
Run: python -m pytest tests/ -v
"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))
from bend_allowance import bend_allowance, get_k_factor, developed_length, bend_deduction
from gauge_table import gauge_to_mm, mm_to_nearest_gauge

def test_k_factor_increases_with_ir_ratio():
    k1 = get_k_factor("304 SS", 1.0, 1.0)   # ir/t = 1
    k2 = get_k_factor("304 SS", 8.0, 1.0)   # ir/t = 8
    assert k2 > k1, "K-factor should increase with ir/t"

def test_k_factor_below_0_5():
    k = get_k_factor("mild_steel", 10.0, 1.0)
    assert k <= 0.5, "K-factor should not exceed 0.5"

def test_ba_positive():
    ba = bend_allowance(90, 3.0, 1.5, material="304 SS")
    assert ba > 0

def test_ba_increases_with_angle():
    ba45 = bend_allowance(45, 3.0, 1.5, material="1018 CRS")
    ba90 = bend_allowance(90, 3.0, 1.5, material="1018 CRS")
    assert ba90 > ba45

def test_ba_explicit_k():
    ba = bend_allowance(90, 3.0, 1.5, k=0.44)
    expected = (math.pi/2) * (3.0 + 0.44*1.5)
    assert abs(ba - expected) < 1e-6

def test_developed_length_two_bends():
    legs = [50, 200, 50]
    bends = [{"angle":90,"ir":3.2,"t":1.626,"material":"304 SS"},
             {"angle":90,"ir":3.2,"t":1.626,"material":"304 SS"}]
    dl = developed_length(legs, bends)
    ba_each = bend_allowance(90, 3.2, 1.626, material="304 SS")
    expected = sum(legs) + 2*ba_each
    assert abs(dl - expected) < 0.01

def test_gauge_lookup_16():
    t = gauge_to_mm(16, "USS")
    assert abs(t - 1.519) < 0.01

def test_nearest_gauge():
    ga, t = mm_to_nearest_gauge(1.626, "USS")
    assert ga in [15, 16]

print("Tests defined. Run: python -m pytest tests/ -v")
