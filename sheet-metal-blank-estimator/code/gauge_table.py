"""
Gauge number to thickness lookup tables.
US Standard (USS) and Manufacturers' Standard (MSG) gauges.
All thicknesses in mm.
Source: ASTM A480, Machinery's Handbook 30th Ed.
"""

# US Standard Gauge (Steel)
USS_GAUGE_MM = {
    7:  4.763,
    8:  4.166,
    9:  3.759,
    10: 3.416,
    11: 3.038,
    12: 2.657,
    13: 2.278,
    14: 1.994,
    15: 1.709,
    16: 1.519,
    17: 1.367,
    18: 1.214,
    19: 1.062,
    20: 0.912,
    21: 0.836,
    22: 0.759,
    23: 0.683,
    24: 0.607,
    25: 0.531,
    26: 0.455,
    28: 0.378,
    30: 0.302,
}

# Manufacturers' Standard Gauge (Steel sheets)
MSG_GAUGE_MM = {
    7:  4.554,
    8:  4.175,
    9:  3.797,
    10: 3.416,
    11: 3.038,
    12: 2.657,
    13: 2.278,
    14: 1.994,
    15: 1.709,
    16: 1.519,
    17: 1.367,
    18: 1.214,
    19: 1.062,
    20: 0.912,
    22: 0.759,
    24: 0.607,
    26: 0.455,
    28: 0.378,
}

# Aluminum gauge (AWG / Aluminum Association)
AL_GAUGE_MM = {
    7:  3.665,
    8:  3.264,
    9:  2.906,
    10: 2.588,
    11: 2.305,
    12: 2.053,
    13: 1.828,
    14: 1.628,
    15: 1.450,
    16: 1.290,
    18: 1.024,
    20: 0.813,
    22: 0.644,
    24: 0.511,
    26: 0.405,
}


def gauge_to_mm(gauge, standard="USS"):
    """Convert gauge number to thickness in mm."""
    tables = {"USS": USS_GAUGE_MM, "MSG": MSG_GAUGE_MM, "AL": AL_GAUGE_MM}
    tbl = tables.get(standard.upper())
    if tbl is None:
        raise ValueError(f"Unknown standard '{standard}'. Options: USS, MSG, AL")
    if gauge not in tbl:
        raise ValueError(f"Gauge {gauge} not in {standard} table. Available: {sorted(tbl.keys())}")
    return tbl[gauge]


def mm_to_nearest_gauge(t_mm, standard="USS"):
    """Find the nearest gauge for a given thickness."""
    tables = {"USS": USS_GAUGE_MM, "MSG": MSG_GAUGE_MM, "AL": AL_GAUGE_MM}
    tbl = tables.get(standard.upper(), USS_GAUGE_MM)
    return min(tbl.items(), key=lambda x: abs(x[1] - t_mm))
