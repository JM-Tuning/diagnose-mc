# EGR og DPF på Mitsubishi 4N14 (2,2 DI-D)

Referanse for **TL 26689** — Mitsubishi Outlander II, chassiskode `CW1W`
(VIN `JMBXJCW1WBZ000670`), første gang registrert 09.03.2011, motorkode **4N14**,
2 268 cm³, 103 kW / 138 hk, manuell, Euro 5.

Tegninger: [`4n14-egr-dpf-plassering.svg`](4n14-egr-dpf-plassering.svg) (sett fra siden)
og [`4n14-egr-dpf-gassvei.svg`](4n14-egr-dpf-gassvei.svg) (gassvei og sensorer).
Samlet side: [`4n14-egr-dpf.html`](4n14-egr-dpf.html).

## Kort

| | |
|---|---|
| **EGR-type** | Høytrykks, kjølt. Tappet fra eksosmanifolden før turbinen. |
| **EGR-kjøler** | Vannkjølt, på baksiden av motoren mot spjeldveggen. |
| **EGR-ventil** | Elektrisk, i EGR-røret etter kjøleren. Røret bolter seg til baksiden av innsugsmanifolden (2 bolter oppe, 2 muttere nede, 10 mm). |
| **DOC + DPF** | Én kanne rett etter turboutløpet, bak/under motoren. Deretter flexrør og potter bakover under gulvet. |
| **Regenerering** | Etterinnsprøytning i sylinder. Ingen Eolys-additiv og ingen additivtank. |
| **Sensorer** | Differansetrykksensor med to slanger over filteret, eksostemperatursensor foran filteret. |

`Partikkelfilter: ---` i vognkortet betyr bare at feltet ikke er utfylt. Euro 5-dieselen
har filter fra fabrikk. 4N14 kom i Outlander fra juli 2010 og avløste den PSA-baserte
2.2-en, som brukte additivbasert FAP — derfor er det verdt å slå fast motorkoden før
man leter etter additivtank som ikke finnes.

## Delenumre

| Del | Nummer | Merknad |
|---|---|---|
| EGR-ventil | `1582A554` | Erstatter `1582A260` / `K5T74091`; også `1582A440`, `1582A476` |
| EGR-kjøler | `1582A212` | Deles med 4N13 (1.8) |
| Eksosmanifold | `1555A958` | Støpejern, kjent for sprekker |
| Turbo | `1515A238`, `49335-0112x` | TF035, variabel geometri |
| Differansetrykksensor | `1865A210` / `1865A176` | |
| Partikkelfilter | `1584A672` | Vanligste OE-nummer i 4N14-familien — kontrolleres mot VIN |

Numrene er hentet fra delekataloger, ikke fra Mitsubishis eget system for denne VIN-en.

## Kjente feil

- **EGR-kjøler lekker** — kjølevæsketap uten synlig lekkasje, hvit røyk. Trykktest kjølesystemet.
- **Soting i EGR-rør og innsugsmanifold** — ujevn tomgang, effekttap, EGR-feilkoder.
- **Sprukket eksosmanifold** — tikking kald, eksoslukt, dårlig ladetrykk.
- **Avbrutt regenerering** — diesel i oljen, stigende oljenivå. Skift olje, ikke etterfyll.
- **Differansetrykksensor / slanger** — hindrer regen, gir `P1498` og `P2463`.
- **VGT-aktuator setter seg** — sot binder skovlene, manglende trekk.

## Bildekilder

Egress-proxyen i utviklingsmiljøet blokkerer bildenedlasting, så foto er lenket, ikke innebygd.

**Video i motorrommet**

- [Rens av innsugsmanifold på 4N14](https://www.youtube.com/watch?v=BgmDQ2uoTgw) — hele EGR-veien synlig
- [4N13/4N14 EGR-ventil ut og inn](https://www.youtube.com/shorts/MFTvuNRRwi4)
- [Outlander DI-D MIVEC — rens av EGR-ventil](https://www.youtube.com/watch?v=Ijk4GzCVL94)
- [Outlander/ASX — sjekk av DPF-system (P1498, P2463)](https://www.youtube.com/watch?v=xwvb-OkVsHc)
- [Outlander 2.2 — DPF-rens](https://www.youtube.com/watch?v=K9SO9BIDpnQ)
- [ASX/Outlander — tvungen regenerering](https://www.youtube.com/watch?v=TP9aGL3Q1hU)

**Foto av delene**

- [EGR-kjøler 1582A212 fra ASX 2.2 DI-D 4N14 (ProxyParts)](https://www.proxyparts.com/car-parts-stock/information/part-number/1582a212/part/egr-cooler/partid/14900962/)
- [EGR-ventil 1582A554](https://www.ebay.com/itm/318408684854)
- [EGR-kjøler 1582A212, flere vinkler](https://www.ebay.com/itm/185660868864)
- [Eksosmanifold 1555A958](https://u2autoparts.com/en/1555a958-mitsubishi-asx-1-8-2-2-outlander-2-2-2-3-4n13-4n14-exhaust-manifold/)
- [Turbo 49335-01122](https://www.ebay.co.uk/itm/176389418977)
- [Partikkelfilter ASX/Outlander 2.2 DI-D](https://www.ebay.com/itm/388660670361)
- [Komplett 4N14-motor fotografert fra flere sider](https://www.proxyparts.com/car-parts-stock/information/engine-code/4n14/part/engine/partid/9888336/)

**Delekatalog med sprengskisser**

- [Amayama — original delekatalog (søk chassiskode CW1W, gruppene «EGR system» og «exhaust pipe»)](https://www.amayama.com/en/catalogs/mitsubishi/outlander)
- [Finndel.no — EGR-ventil, motorkode 4N14](https://finndel.no/delinfo.aspx?f=761&dnr=380305)
- [Autodoc Club — bytte av EGR-ventil, steg for steg](https://club.autodoc.co.no/manuals/motor/egr-ventil/mitsubishi/outlander)

## Forbehold

Tegningene er laget ut fra hvordan 4N14 er bygget, ikke kopiert fra verkstedhåndboka —
den lot seg ikke åpne fra dette miljøet. Nøyaktig brakettplassering og slangeføring bør
kontrolleres mot bilen eller mot MUT-III / verkstedhåndboka for CW1W.
