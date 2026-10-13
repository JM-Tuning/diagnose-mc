# Limtubeholder

Holder for en limtube (korken ned i holderen). Rotasjonskropp med kuppelformet
fot og sylindrisk hals. I halsen er det en boring Ø25 ned til en kant (avsats),
og under kanten et hull på korkens bredde som går ned til en 0,6 mm flat bunn.

| Mål                       | mm   | Kilde                         |
|---------------------------|------|-------------------------------|
| Diameter fot              | 50,0 | målt med skyvelær             |
| Total høyde               | 54,0 | målt med skyvelær             |
| Høyde kuppel / hals       | 34 / 20 | fra sidebilde              |
| Ytre diameter hals        | 28,7 | målt med skyvelær             |
| Boring i hals             | 25,0 | 24,5 var for trangt for tuben |
| Dybde ned til kanten      | 23,7 | målt med dybdemål             |
| Hull under kanten         | 18,9 | kork 18,5 + 0,4 mm klaring    |
| Bunn under hullet         | 0,6  | 3 lag à 0,2 mm, flat          |
| Fas rundt bunnkanten      | 1,0  | valgt (printvennlig)          |

Filer:

- `limtubeholder.stl` – klar til slicing (mm, 256 segmenter, vanntett).
- `limtubeholder.scad` – samme form som OpenSCAD-fil.
- `limtubeholder.png` – illustrasjon med mål.
- `generate_limtubeholder.py` – lager alle filene. Alle mål står øverst i
  skriptet; endre f.eks. `CLEARANCE` hvis korken sitter for stramt eller for løst.

Printes stående på foten, ingen overheng som trenger støtte.
