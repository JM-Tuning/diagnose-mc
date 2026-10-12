# Limtubeholder

Holder for en limtube (korken ned i holderen). Rotasjonskropp med kuppelformet
fot og sylindrisk hals. I halsen er det en boring med en kant (avsats) nederst
som korken på tuben hviler på, og en liten lomme under kanten.

| Mål                       | mm   | Kilde                         |
|---------------------------|------|-------------------------------|
| Diameter fot              | 50,0 | målt med skyvelær             |
| Total høyde               | 54,0 | målt med skyvelær             |
| Høyde kuppel / hals       | 34 / 20 | fra sidebilde              |
| Ytre diameter hals        | 28,7 | målt med skyvelær             |
| Boring i hals             | 24,5 | målt med skyvelær             |
| Dybde ned til kanten      | 23,7 | målt med dybdemål             |
| Hull gjennom kanten       | 14,0 | valgt (korken er Ø18,7)       |
| Lomme under kanten        | 6,0  | valgt                         |
| Fas rundt bunnkanten      | 1,0  | valgt (printvennlig)          |

Filer:

- `limtubeholder.stl` – klar til slicing (mm, 256 segmenter, vanntett).
- `limtubeholder.scad` – samme form som OpenSCAD-fil.
- `limtubeholder.png` – illustrasjon med mål.
- `generate_limtubeholder.py` – lager alle filene. Alle mål står øverst i
  skriptet; endre f.eks. `D_BORE` til 20 for en strammere boring rundt korken.

Printes stående på foten, ingen overheng som trenger støtte.
