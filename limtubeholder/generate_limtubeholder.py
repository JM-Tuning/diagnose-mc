#!/usr/bin/env python3
"""Limtubeholder – genererer STL, OpenSCAD-fil og illustrasjon.

Holderen er en rotasjonskropp: kuppelformet fot med en sylindrisk hals.
Øverst er det en boring Ø24,5 ned til en kant (avsats). Under kanten går
et hull på korkens bredde nesten helt ned til bunnen (bare 2-3 lag igjen),
med flat bunn.

Kjør:  python3 generate_limtubeholder.py
"""
import math
import struct
import numpy as np

# ----------------------------------------------------------------- mål (mm)
D_BASE = 50.0        # diameter fot (målt 50,0)
H_TOTAL = 54.0       # total høyde (målt 54,0)
H_DOME = 34.0        # høyde kuppel (fra sidebilde: hals ≈ 20 mm)
D_NECK = 28.7        # ytre diameter hals (målt 28,7)
D_BORE = 25.5        # boring i halsen (24,5 og 25,0 var for trangt for tuben)
BORE_DEPTH = 23.7    # dybde fra toppen ned til kanten (målt 23,7)
D_CAP = 18.5         # korken på limtuben (målt 18,5)
CLEARANCE = 0.4      # klaring så korken går ned i hullet etter printing
D_HOLE = D_CAP + CLEARANCE  # hull under kanten, går nesten helt ned
FLOOR = 0.6          # bunn under hullet: 3 lag à 0,2 mm (flat, ingen forhøyning)
CHAMFER_BASE = 1.0   # 45° fas rundt bunnkanten
CHAMFER_TOP_OUT = 0.4
CHAMFER_TOP_IN = 0.6 # fas i toppen av boringen (lettere å sette tuben i)
DOME_EXP = 2.6       # formen på kuppelen: r(z) = R - k*z^DOME_EXP

SEGMENTS = 256       # oppløsning rundt aksen (STL)


def dome_radius(z):
    """Kuppelprofil: r=R_base ved z=0, r=R_neck ved z=H_DOME."""
    r_base, r_neck = D_BASE / 2, D_NECK / 2
    k = (r_base - r_neck) / H_DOME ** DOME_EXP
    return r_base - k * z ** DOME_EXP


def profile(n_dome=120):
    """Lukket polygon (r, z) i halvplanet r >= 0, mot klokka."""
    r_neck, r_bore, r_hole = D_NECK / 2, D_BORE / 2, D_HOLE / 2
    z_ledge = H_TOTAL - BORE_DEPTH
    z_pocket = FLOOR
    pts = [(0.0, 0.0), (D_BASE / 2 - CHAMFER_BASE, 0.0)]
    # kuppel: tettere punkter mot toppen der krumningen er størst
    for i in range(n_dome + 1):
        t = i / n_dome
        z = CHAMFER_BASE + (H_DOME - CHAMFER_BASE) * (t ** 0.8)
        pts.append((dome_radius(z), z))
    pts += [
        (r_neck, H_TOTAL - CHAMFER_TOP_OUT),
        (r_neck - CHAMFER_TOP_OUT, H_TOTAL),
        (r_bore + CHAMFER_TOP_IN, H_TOTAL),
        (r_bore, H_TOTAL - CHAMFER_TOP_IN),
        (r_bore, z_ledge),
        (r_hole, z_ledge),
        (r_hole, z_pocket),
        (0.0, z_pocket),
    ]
    # fjern eventuelle påfølgende like punkter (gir ellers degenererte trekanter)
    clean = [pts[0]]
    for q in pts[1:]:
        if abs(q[0] - clean[-1][0]) > 1e-9 or abs(q[1] - clean[-1][1]) > 1e-9:
            clean.append(q)
    return np.array(clean)


def revolve(poly, segments):
    """Roterer en lukket (r,z)-polygon om z-aksen -> (N,3,3) trekanter."""
    theta = np.linspace(0, 2 * math.pi, segments, endpoint=False)
    cos, sin = np.cos(theta), np.sin(theta)
    tris = []
    n = len(poly)
    for i in range(n):
        r0, z0 = poly[i]
        r1, z1 = poly[(i + 1) % n]
        if r0 == 0 and r1 == 0:
            continue  # kant langs aksen – ingen flate
        a = np.stack([r0 * cos, r0 * sin, np.full_like(cos, z0)], axis=1)
        b = np.stack([r1 * cos, r1 * sin, np.full_like(cos, z1)], axis=1)
        a2, b2 = np.roll(a, -1, axis=0), np.roll(b, -1, axis=0)
        if r1 > 0:
            tris.append(np.stack([a, b, b2], axis=1))
        if r0 > 0:
            tris.append(np.stack([a, b2, a2], axis=1))
    tris = np.concatenate(tris)
    # sørg for at normalene peker utover (positivt volum)
    if signed_volume(tris) < 0:
        tris = tris[:, ::-1, :]
    return tris


def signed_volume(tris):
    a, b, c = tris[:, 0], tris[:, 1], tris[:, 2]
    return float(np.einsum("ij,ij->i", a, np.cross(b, c)).sum() / 6.0)


def check_watertight(tris):
    """Hver kant skal deles av nøyaktig to trekanter (motsatt retning)."""
    v = tris.reshape(-1, 3)
    uniq, inv = np.unique(np.round(v, 6), axis=0, return_inverse=True)
    f = inv.reshape(-1, 3)
    edges = np.concatenate([f[:, [0, 1]], f[:, [1, 2]], f[:, [2, 0]]])
    directed, cnt = np.unique(edges, axis=0, return_counts=True)
    if cnt.max() != 1:
        return False, "duplisert rettet kant"
    rev = {(b, a) for a, b in map(tuple, directed)}
    missing = sum(1 for e in map(tuple, directed) if e not in rev)
    return missing == 0, f"{missing} kanter uten makker"


def write_stl(path, tris, name=b"limtubeholder"):
    n = len(tris)
    normals = np.cross(tris[:, 1] - tris[:, 0], tris[:, 2] - tris[:, 0])
    normals /= np.maximum(np.linalg.norm(normals, axis=1, keepdims=True), 1e-12)
    data = np.zeros(n, dtype=[("n", "<f4", 3), ("v", "<f4", (3, 3)), ("attr", "<u2")])
    data["n"], data["v"] = normals, tris
    with open(path, "wb") as fh:
        fh.write(name.ljust(80, b"\0"))
        fh.write(struct.pack("<I", n))
        fh.write(data.tobytes())


def write_scad(path):
    poly = profile(60)
    pts = ",\n    ".join(f"[{r:.3f}, {z:.3f}]" for r, z in poly)
    with open(path, "w") as fh:
        fh.write(
            "// Limtubeholder – generert av generate_limtubeholder.py\n"
            f"// Fot Ø{D_BASE}, høyde {H_TOTAL}, hals Ø{D_NECK}, boring Ø{D_BORE} "
            f"x {BORE_DEPTH} dyp, kant, hull Ø{D_HOLE:.1f} ned til {FLOOR} mm bunn\n"
            "$fn = 256;\n"
            "rotate_extrude() polygon([\n    " + pts + "\n]);\n"
        )


def render(path, poly):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Polygon as MplPolygon
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection

    def shaded(tris, base_rgb, light=(0.4, -0.6, 0.7)):
        n = np.cross(tris[:, 1] - tris[:, 0], tris[:, 2] - tris[:, 0])
        n /= np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-12)
        l = np.array(light) / np.linalg.norm(light)
        lam = np.clip(n @ l, 0, 1)
        shade = 0.35 + 0.65 * lam
        cols = np.clip(np.array(base_rgb)[None, :] * shade[:, None], 0, 1)
        return np.concatenate([cols, np.ones((len(cols), 1))], axis=1)

    def visible(tris, elev, azim):
        """Fjerner trekanter som vender bort fra kameraet (riktigere tegnerekkefølge)."""
        e, a = math.radians(elev), math.radians(azim)
        v = np.array([math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e)])
        n = np.cross(tris[:, 1] - tris[:, 0], tris[:, 2] - tris[:, 0])
        return tris[n @ v > 0]

    def setup_axes(ax, title):
        ax.set_box_aspect((1, 1, 1.1))
        lim = D_BASE / 2 + 2
        ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim); ax.set_zlim(0, H_TOTAL + 1)
        ax.set_axis_off()
        ax.set_title(title, fontsize=12)

    def subdivide(poly, max_len=2.5):
        out = []
        for i in range(len(poly)):
            a, b = poly[i], poly[(i + 1) % len(poly)]
            n = max(1, int(math.ceil(np.linalg.norm(b - a) / max_len)))
            out += [a + (b - a) * t / n for t in range(n)]
        return np.array(out)

    low = revolve(subdivide(profile(40)), 96)
    fig = plt.figure(figsize=(16, 6.2), dpi=130)
    grey = (0.32, 0.33, 0.36)

    # --- 1: hele modellen
    ax = fig.add_subplot(1, 3, 1, projection="3d")
    elev, azim = 22, -55
    # innvendige flater dypere enn ~10 mm er ikke synlige herfra; de utelates
    # fordi matplotlib ellers kan tegne dem gjennom ytterveggen
    cen = low.mean(axis=1)
    interior_deep = (np.hypot(cen[:, 0], cen[:, 1]) < D_BORE / 2 + 0.01) & (cen[:, 2] < H_TOTAL - 12)
    vis = visible(low[~interior_deep], elev, azim)
    cols = shaded(vis, grey)
    ax.add_collection3d(Poly3DCollection(vis, facecolors=cols, edgecolors=cols, linewidths=0.2))
    setup_axes(ax, "Limtubeholder")
    ax.view_init(elev=elev, azim=azim)

    # --- 2: snitt (halve modellen) som viser boring, kant og lomme
    ax = fig.add_subplot(1, 3, 2, projection="3d")
    elev, azim = 18, 90
    cen = low.mean(axis=1)
    half = visible(low[cen[:, 1] <= 1e-9], elev, azim)
    cols = shaded(half, grey, light=(0.3, 0.8, 0.6))
    ax.add_collection3d(Poly3DCollection(half, facecolors=cols, edgecolors=cols, linewidths=0.2))
    cut = (0.85, 0.55, 0.25)
    for sgn in (1, -1):
        face = np.array([(sgn * r, 0.0, z) for r, z in poly])
        ax.add_collection3d(Poly3DCollection([face], facecolors=[cut], edgecolors="k", linewidths=0.4))
    setup_axes(ax, "Snitt gjennom midten")
    ax.view_init(elev=elev, azim=azim)

    # --- 3: 2D-snitt med mål
    ax = fig.add_subplot(1, 3, 3)
    full = np.concatenate([poly, poly[::-1] * np.array([-1, 1])])
    ax.add_patch(MplPolygon(full, closed=True, facecolor=(0.82, 0.84, 0.88), edgecolor="k", lw=1.0))
    # korken på limtuben (spøkelse) som hviler på kanten
    z_ledge = H_TOTAL - BORE_DEPTH
    cap_len = 30.0
    red = (0.85, 0.2, 0.15)
    ax.add_patch(MplPolygon([(-D_CAP / 2, FLOOR), (D_CAP / 2, FLOOR),
                             (D_CAP / 2, FLOOR + cap_len), (-D_CAP / 2, FLOOR + cap_len)],
                            closed=True, facecolor="none", edgecolor=red, lw=1.2, ls="--"))
    ax.text(0, FLOOR + 20, f"kork på\nlimtuben\nØ{D_CAP:g}", ha="center", va="center",
            fontsize=8, color=red)

    def dim_h(x0, x1, y, text, dy=1.3):
        ax.annotate("", (x0, y), (x1, y), arrowprops=dict(arrowstyle="<->", lw=0.8))
        ax.text((x0 + x1) / 2, y + dy, text, ha="center", va="bottom", fontsize=8)

    def dim_v(y0, y1, x, text, dx=1.0):
        ax.annotate("", (x, y0), (x, y1), arrowprops=dict(arrowstyle="<->", lw=0.8))
        ax.text(x + dx, (y0 + y1) / 2, text, ha="left", va="center", fontsize=8, rotation=90)

    r_neck, r_bore, r_hole = D_NECK / 2, D_BORE / 2, D_HOLE / 2
    dim_h(-D_BASE / 2, D_BASE / 2, -4, f"Ø{D_BASE:g}", dy=-4.5)
    dim_h(-r_neck, r_neck, H_TOTAL + 16, f"Ø{D_NECK:g} hals")
    dim_h(-r_bore, r_bore, H_TOTAL + 9, f"Ø{D_BORE:g} boring")
    dim_h(-r_hole, r_hole, FLOOR + 3.5, f"Ø{D_HOLE:.1f} hull\n(kork {D_CAP:g} + {CLEARANCE:g} klaring)")
    dim_v(0, H_TOTAL, D_BASE / 2 + 5, f"{H_TOTAL:g}")
    dim_v(0, H_DOME, D_BASE / 2 + 11, f"{H_DOME:g}")
    dim_v(z_ledge, H_TOTAL, -(r_neck + 4), f"{BORE_DEPTH:g} dyp", dx=-3.2)
    dim_v(FLOOR, z_ledge, -(r_neck + 4), f"{z_ledge - FLOOR:.1f} dyp under kanten", dx=-3.2)
    ax.annotate(f"bunn {FLOOR:g} mm (3 lag), flat", (r_hole / 2, FLOOR / 2), (r_neck + 3, -7),
                fontsize=8, arrowprops=dict(arrowstyle="->", lw=0.8))
    ax.annotate("kant (avsats)", (r_bore - 1.5, z_ledge), (r_bore + 6, z_ledge - 9),
                fontsize=8, arrowprops=dict(arrowstyle="->", lw=0.8))
    ax.set_aspect("equal")
    ax.set_xlim(-D_BASE / 2 - 16, D_BASE / 2 + 16)
    ax.set_ylim(-11, H_TOTAL + 24)
    ax.set_axis_off()
    ax.set_title("Snitt med mål (mm)", fontsize=12)

    fig.tight_layout()
    fig.savefig(path, facecolor="white")


if __name__ == "__main__":
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    poly = profile()
    tris = revolve(poly, SEGMENTS)
    ok, msg = check_watertight(tris)
    vol = signed_volume(tris)
    print(f"trekanter: {len(tris)}  volum: {vol/1000:.1f} cm³  vanntett: {ok} ({msg})")
    print(f"PLA-vekt ved 100 % fyll: ca {vol/1000*1.24:.0f} g")
    write_stl(os.path.join(here, "limtubeholder.stl"), tris)
    write_scad(os.path.join(here, "limtubeholder.scad"))
    render(os.path.join(here, "limtubeholder.png"), poly)
    print("skrev limtubeholder.stl, limtubeholder.scad, limtubeholder.png")
