# Vietlot
auto crawl lottery data from [vietlott](https://vietlott.vn) daily, and predict tickets - it's a copy from [here](https://github.com/vietvudanh/vietlott-data)
## Predictions (just for testing, not a financial advice)
### random 10 tickets of power 6/55

strategy 1:
| date       | result                  | predicted               |
|:-----------|:------------------------|:------------------------|
| 2025-09-13 | [2, 7, 15, 18, 24, 27]  | [7, 45, 27, 18, 35, 15] |
| 2024-02-03 | [4, 6, 7, 13, 18, 26]   | [49, 6, 26, 7, 3, 4]    |
| 2019-04-06 | [1, 20, 30, 41, 46, 50] | [50, 30, 46, 41, 18, 1] |

strategy 2:
|   # | Tickets                  |
|----:|:-------------------------|
|   1 | [34, 39, 40, 42, 54, 55] |
|   2 | [12, 17, 21, 25, 33, 40] |

strategy 3:
|   # | Tickets                  |
|----:|:-------------------------|
|   1 | [5, 21, 25, 41, 50, 53]  |
|   2 | [4, 9, 14, 29, 34, 43]   |
|   3 | [4, 33, 39, 43, 50, 53]  |
|   4 | [13, 24, 31, 35, 41, 44] |
|   5 | [16, 20, 25, 29, 32, 42] |
|   6 | [17, 24, 31, 36, 40, 50] |
|   7 | [2, 8, 31, 42, 48, 53]   |
|   8 | [10, 15, 40, 44, 48, 52] |
|   9 | [15, 19, 31, 42, 50, 53] |
|  10 | [10, 17, 22, 40, 48, 52] |

## top 20 details power 6/55
| date       |    id | result                   |
|:-----------|------:|:-------------------------|
| 2026-04-07 | 01329 | [1, 13, 23, 31, 44, 53]  |
| 2026-04-04 | 01328 | [5, 7, 10, 23, 30, 54]   |
| 2026-04-02 | 01327 | [9, 21, 32, 34, 52, 53]  |
| 2026-03-31 | 01326 | [15, 16, 22, 38, 43, 48] |
| 2026-03-28 | 01325 | [7, 13, 21, 30, 33, 42]  |
| 2026-03-26 | 01324 | [3, 9, 10, 34, 38, 44]   |
| 2026-03-24 | 01323 | [12, 19, 25, 26, 32, 45] |
| 2026-03-21 | 01322 | [1, 6, 40, 43, 47, 53]   |
| 2026-03-19 | 01321 | [7, 9, 17, 31, 34, 36]   |
| 2026-03-17 | 01320 | [12, 26, 28, 43, 50, 54] |
| 2026-03-14 | 01319 | [7, 16, 27, 29, 47, 52]  |
| 2026-03-12 | 01318 | [12, 28, 36, 40, 53, 55] |
| 2026-03-10 | 01317 | [3, 26, 31, 39, 47, 54]  |
| 2026-03-07 | 01316 | [4, 32, 41, 45, 50, 52]  |
| 2026-03-05 | 01315 | [14, 16, 35, 38, 43, 51] |
| 2026-03-03 | 01314 | [7, 13, 27, 29, 43, 50]  |
| 2026-02-28 | 01313 | [22, 25, 31, 44, 51, 54] |
| 2026-02-26 | 01312 | [1, 7, 10, 21, 44, 51]   |
| 2026-02-24 | 01311 | [5, 8, 18, 30, 39, 54]   |
| 2026-02-21 | 01310 | [5, 7, 26, 30, 41, 45]   |

### random 10 tickets of power 6/45

strategy 1:
|   # | Tickets                  |
|----:|:-------------------------|
|   1 | [6, 14, 15, 24, 26, 39]  |
|   2 | [17, 18, 19, 33, 35, 37] |

strategy 2:
|   # | Tickets                  |
|----:|:-------------------------|
|   1 | [4, 26, 33, 36, 39, 43]  |
|   2 | [11, 20, 25, 28, 35, 42] |
|   3 | [17, 21, 24, 34, 42, 44] |
|   4 | [3, 11, 14, 17, 40, 43]  |
|   5 | [5, 22, 30, 36, 39, 43]  |
|   6 | [3, 13, 23, 27, 34, 43]  |
|   7 | [2, 30, 36, 39, 43, 44]  |
|   8 | [3, 7, 31, 34, 41, 44]   |
|   9 | [6, 12, 19, 23, 39, 43]  |
|  10 | [11, 17, 20, 27, 33, 42] |

## top 20 details power 6/45
| date       |    id | result                   |
|:-----------|------:|:-------------------------|
| 2026-04-08 | 01494 | [5, 8, 23, 26, 38, 41]   |
| 2026-04-05 | 01493 | [2, 9, 23, 30, 32, 42]   |
| 2026-04-03 | 01492 | [2, 4, 23, 24, 35, 41]   |
| 2026-04-01 | 01491 | [6, 30, 34, 36, 37, 44]  |
| 2026-03-29 | 01490 | [5, 8, 18, 30, 37, 45]   |
| 2026-03-27 | 01489 | [5, 7, 13, 19, 38, 45]   |
| 2026-03-25 | 01488 | [16, 22, 24, 29, 35, 36] |
| 2026-03-22 | 01487 | [5, 10, 22, 26, 31, 36]  |
| 2026-03-20 | 01486 | [8, 11, 22, 23, 38, 43]  |
| 2026-03-18 | 01485 | [14, 20, 33, 35, 36, 44] |
| 2026-03-15 | 01484 | [4, 7, 11, 26, 42, 44]   |
| 2026-03-13 | 01483 | [11, 12, 20, 22, 31, 33] |
| 2026-03-11 | 01482 | [16, 18, 19, 28, 31, 44] |
| 2026-03-08 | 01481 | [6, 12, 13, 25, 31, 32]  |
| 2026-03-06 | 01480 | [2, 10, 12, 21, 32, 37]  |
| 2026-03-04 | 01479 | [1, 4, 6, 9, 13, 44]     |
| 2026-03-01 | 01478 | [16, 22, 23, 35, 44, 45] |
| 2026-02-27 | 01477 | [2, 4, 8, 15, 17, 28]    |
| 2026-02-25 | 01476 | [4, 13, 20, 22, 23, 29]  |
| 2026-02-22 | 01475 | [7, 23, 24, 36, 38, 40]  |

<!---
stats 6/55 all time - stats.to_markdown(index=False)
stats 6/55 -15d - stats_15d.to_markdown(index=False)
stats 6/55 -30d - stats_30d.to_markdown(index=False)
stats 6/55 -60d - stats_60d.to_markdown(index=False)
stats 6/55 -90d - stats_90d.to_markdown(index=False)
-->

# Install
 
## run locally

```shell
# add PATH C:\Users\win\.pyenv\pyenv-win\versions\3.11.4\Scripts\
$ pip install -r requirements.txt
$ python src/vietlott/cli/crawl.py power_655
$ python src/vietlott/cli/missing.py power_655
$ python src/render_readme.py
$ python src/vietlott/predictor/predictor.py
$ python src/vietlott/predictor/predictor2.py
```
 
## via pip

```shell
pip install -i https://test.pypi.org/simple/ vietlott-data==0.1.2
```

## cli
project provides two cli

### crawl
```shell
Usage: vietlott-crawl [OPTIONS] PRODUCT

  crawl a product with a given run date or from/to index page :param ctx:
  :param product: :param run_date: :param index_from: :param index_to:
  :return:

Options:
  --run-date TEXT
  --index_from INTEGER  page index from run since we crawl by pagination the
                        pages
  --index_to INTEGER    page index from run since we crawl by pagination the
                        pages
  --help                Show this message and exit.
```

### Backfill missing data

```shell
Usage: vietlott-missing [OPTIONS] PRODUCT

  detect_missing_data and run if needed :param ctx: context :param product:
  product to run :param limit: number of pages to run :return:

Options:
  --limit INTEGER
  --help           Show this message and exit.
```

