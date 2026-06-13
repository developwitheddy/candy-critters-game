# Printable Wall Art — 100-Piece Collection

A collection of **100 original, royalty-free vector posters** ready to print and
frame. Every piece is a pure **SVG**, so it scales to any size without ever going
blurry — print it at postcard size or as a big poster and the lines stay crisp.

All art is sized in a **4:5 ratio**, the most popular framing ratio for wall
prints. That means it drops straight into standard frames:

| Frame size | Notes |
|------------|-------|
| 8 × 10 in  | desk / gallery wall |
| 11 × 14 in | most common frame |
| 16 × 20 in | statement piece |
| 18 × 22.5 in | large poster |
| A-series   | scales cleanly too |

## How to use it

1. **Browse:** open [`index.html`](index.html) in any web browser. You get a
   filterable gallery of all 100 pieces grouped by style.
2. **Pick one:** click a piece to open the full-size SVG, or use the **Download**
   link on each card.
3. **Print:** open the `.svg` in a browser and `Ctrl/Cmd + P`, or import it into
   Word / Canva / a print shop. Choose **borderless** or "fit to page" and print
   on matte or heavyweight paper for the best look. Because it's vector, set any
   size you like and it stays sharp.

The individual files live in [`art/prints/`](art/prints/), named
`001-…` through `100-…`.

## What's inside

The 100 pieces span 13 styles, so there's something for any room:

- **Geometric** — mandalas, spirographs, harmonographs
- **Landscape** — layered mountain ranges, city skylines
- **Mid-Century** — sunbursts, rising-sun motifs
- **Modernist** — Bauhaus grids, Albers-style nested squares
- **Abstract** — sound waves, concentric arcs, gradient dawns
- **Pattern** — seigaiha waves, terrazzo, halftone dot matrices
- **Celestial** — moon phases, constellations
- **Generative** — circle packing, low-poly facets, flow fields
- **Op-Art** — optic rings, warped checkers, spinning squares
- **Botanical / Organic** — leafy sprigs, tree rings
- **Typography** — minimalist quote posters
- **Candy Critters** — a cute set of characters that nods to this repo's name 🍬

## Regenerating

Everything is produced by one script with no third-party dependencies:

```bash
python3 art/generate.py
```

This regenerates `art/prints/*.svg`, `art/manifest.json`, and `index.html`.
Tweak the palettes or the family `plan` near the bottom of `generate.py` to
change the mix.

## License

These works are generated programmatically and are free for personal and
commercial use — print them, frame them, gift them. No attribution required.
