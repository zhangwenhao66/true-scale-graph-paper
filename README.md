# true-scale-graph-paper

A single-file Python script (no dependencies) that writes vector graph paper PDFs whose squares measure exactly what they say when printed at 100%.

```
python3 graphpaper.py --square 0.25in --paper letter --major 4 -o quarter-inch-letter.pdf
python3 graphpaper.py --square 5mm --paper a4 --major 2 -o 5mm-a4.pdf
python3 graphpaper.py --square 1cm --paper letter -o 1cm-letter.pdf
```

Ready-made files are in [`examples/`](examples).

## Why squares come out the wrong size

1. **Fit to page.** Most print dialogs default to shrinking the page so it fits the printable area. A 1/4 in grid printed that way comes out a few percent small, which is enough for a ruler or a scale drawing to disagree with the grid. Print at **100% / Actual size**. The PDFs here also set `/PrintScaling /None`, which asks viewers that honour it to default to 100%.
2. **Raster grids.** A grid saved as a PNG or JPEG is tied to a pixel density; a 150 dpi image printed at 300 dpi halves. Lines drawn as vectors in PDF points (72 pt = 1 in, 1 mm = 72 / 25.4 pt) have no pixel size to get wrong.
3. **Partial squares.** If the grid is just clipped by the margin, the edge squares are cut. The script fits a whole number of squares inside the margin and centres the grid, so every square is full size.

## How it works

- Paper sizes in points: Letter 612 × 792, A4 595.276 × 841.89, Legal 612 × 1008.
- Columns = floor((page width − 2 × margin) ÷ square), same for rows.
- Minor lines 0.5 pt at 60% grey; optional major lines every N squares at 0.9 pt, 35% grey.
- The PDF is four objects (catalog, pages, page, content stream) written by hand, so the file for a full page of 1/4 in grid is about 3 KB.

After printing, measure ten squares with a ruler: ten 1/4 in squares should be 2.5 in, ten 5 mm squares 50 mm.

If you'd rather not run a script, https://paper-generator.com/ makes the same kind of true-scale PDFs (graph and lined paper on Letter, A4 or Legal) in the browser.

License: MIT.
