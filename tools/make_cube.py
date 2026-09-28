#!/usr/bin/env python3
"""Write assets/teal-orange.cube: shadows toward teal, skin and highlights toward orange.

    python3 tools/make_cube.py > assets/teal-orange.cube
"""
N = 17


def grade(r, g, b):
    luma = 0.2126 * r + 0.7152 * g + 0.0722 * b
    # a gentle S-curve on luma, then split-tone: teal below the middle, orange above
    s = luma + 0.12 * (luma - 0.5) * (1 - abs(2 * luma - 1))
    t = max(0.0, 0.5 - s) * 2          # 0..1 in the shadows
    o = max(0.0, s - 0.5) * 2          # 0..1 in the highlights
    r, g, b = r + (s - luma), g + (s - luma), b + (s - luma)
    r += 0.10 * o - 0.08 * t
    g += 0.03 * o + 0.02 * t
    b += -0.08 * o + 0.07 * t
    return tuple(min(1.0, max(0.0, v)) for v in (r, g, b))


print('TITLE "teal-orange"')
print(f"LUT_3D_SIZE {N}")
for bi in range(N):
    for gi in range(N):
        for ri in range(N):
            print("%.6f %.6f %.6f" % grade(ri / (N - 1), gi / (N - 1), bi / (N - 1)))
