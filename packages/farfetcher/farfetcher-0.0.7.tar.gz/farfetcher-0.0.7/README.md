# fmarket
API built to extract product data from Farfetch. Farfetch is a luxury fashion e-commerce website.

Full code from Medium post 'Scraping 180K Luxury Fashion Products with PYthon"
https://medium.com/swlh/scraping-180k-luxury-fashion-products-with-python-ba42fdd831d8


# Usage

```python
>>> from farfetcher import Farfetcher
>>> ff = Farfetcher()
>>> ff.listings()
```

# CLI

```
$ farfetcher crawl --help
Usage: farfetcher crawl [OPTIONS]

Options:
  -n, --num-pages INTEGER  No. of pages to crawl.
  -o, --output-to TEXT     Filename to save the dataframe.
  -h, --help               Show this message and exit.

$ farfetcher crawl -n 5
100%|██████████████████████████████████████████████| 5/5 [00:04<00:00,  1.20it/s]
TSV file saved to farfetch-2019-10-18.tsv
```


# To read the tsv file.

```python
import pandas as pd

df = pd.read_csv('farfetch-2019-10-18.tsv', sep='\t')
```
