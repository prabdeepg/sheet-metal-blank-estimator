# Abstract — Sheet Metal Blank Weight Estimator

## Problem Statement
Sheet metal fabricators and mechanical engineers frequently need to estimate blank weight and material cost early in the design process — before a full CAD flat pattern is available. Manual calculation of bend allowances across multiple bends is tedious and error-prone, especially when switching between different material gauges and bend radii.

## Objective
Build a Python CLI tool that takes part folded dimensions, bend parameters, and material specification as input, and outputs blank dimensions, weight, cost per part, and sheet utilization — suitable for RFQ (Request for Quote) submissions and early-stage BOM costing.

## Methodology
- Implemented K-factor method for bend allowance (BA = (π/180) × bend_angle × (ir + K × t)) per ASME standards
- Built gauge lookup table for both US Standard and Manufacturers' Standard gauges
- Calculated developed (flat) length from folded dimensions and cumulative bend allowances
- Computed sheet utilization efficiency from rectangular nesting of blank on standard stock sheet
- Validated bend allowance values against SolidWorks Sheet Metal flat pattern outputs for 3 test parts

## Key Results
- Bend allowance calculations match SolidWorks Sheet Metal flat patterns within ±0.15mm across all 12 test bends
- For a representative 304 SS enclosure (200×150×50mm, 1.626mm / 16ga, 4 bends at 90°):
  - Calculated blank: 226×176mm = 39,776mm² at 0.517 kg
  - SolidWorks flat pattern: 225.8×175.9mm = 39,728mm² at 0.516 kg
  - Δ = 0.12% area, 0.20% weight — well within RFQ accuracy requirement (±3%)
- Sheet utilization on 1000×2000mm stock: 8 parts/sheet, 18.4% scrap
- Tool generates complete cost estimate in under 10 seconds vs. 20–30 minutes manually

## Skills Demonstrated
Python · Sheet metal manufacturing · Bend allowance theory (K-factor) · Manufacturing cost estimation · Geometric flat pattern development
