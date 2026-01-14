# Vietlot
auto crawl lottery data from [vietlott](https://vietlott.vn) daily, and predict tickets - it's a copy from [here](https://github.com/vietvudanh/vietlott-data)
## Predictions (just for testing, not a financial advice)
### random 10 tickets of power 6/55

strategy 1:
| date       | result                   | predicted                |
|:-----------|:-------------------------|:-------------------------|
| 2022-12-13 | [10, 22, 31, 37, 41, 52] | [37, 52, 31, 42, 22, 41] |
| 2018-11-15 | [13, 16, 21, 40, 49, 52] | [21, 49, 54, 16, 3, 52]  |

strategy 2:
|   # | Tickets                  |
|----:|:-------------------------|
|   1 | [12, 18, 20, 25, 27, 52] |
|   2 | [1, 2, 14, 32, 33, 41]   |

strategy 3:
|   # | Tickets                  |
|----:|:-------------------------|
|   1 | [4, 8, 14, 22, 27, 51]   |
|   2 | [4, 17, 25, 41, 46, 51]  |
|   3 | [4, 27, 33, 42, 49, 54]  |
|   4 | [3, 20, 33, 44, 48, 53]  |
|   5 | [4, 31, 40, 45, 50, 53]  |
|   6 | [12, 27, 39, 45, 49, 53] |
|   7 | [4, 28, 32, 35, 42, 49]  |
|   8 | [10, 24, 27, 45, 50, 53] |
|   9 | [9, 14, 32, 43, 49, 54]  |
|  10 | [3, 8, 40, 45, 50, 53]   |

## top 20 details power 6/55
| date       |    id | result                   |
|:-----------|------:|:-------------------------|
| 2026-01-13 | 01294 | [3, 12, 25, 51, 52, 55]  |
| 2026-01-10 | 01293 | [9, 16, 30, 33, 34, 38]  |
| 2026-01-08 | 01292 | [20, 22, 36, 43, 45, 50] |
| 2026-01-06 | 01291 | [22, 28, 29, 30, 34, 47] |
| 2026-01-03 | 01290 | [10, 16, 17, 23, 33, 36] |
| 2026-01-01 | 01289 | [5, 16, 29, 33, 39, 42]  |
| 2025-12-30 | 01288 | [11, 30, 35, 41, 48, 55] |
| 2025-12-27 | 01287 | [16, 21, 30, 37, 39, 40] |
| 2025-12-25 | 01286 | [4, 6, 32, 37, 40, 48]   |
| 2025-12-23 | 01285 | [2, 10, 16, 25, 32, 38]  |
| 2025-12-20 | 01284 | [22, 32, 33, 35, 40, 41] |
| 2025-12-18 | 01283 | [12, 14, 29, 30, 39, 55] |
| 2025-12-16 | 01282 | [7, 36, 37, 38, 52, 55]  |
| 2025-12-13 | 01281 | [5, 8, 12, 18, 20, 38]   |
| 2025-12-11 | 01280 | [9, 13, 21, 45, 48, 55]  |
| 2025-12-09 | 01279 | [14, 21, 26, 27, 31, 43] |
| 2025-12-06 | 01278 | [12, 26, 34, 37, 50, 52] |
| 2025-12-04 | 01277 | [10, 29, 32, 33, 44, 53] |
| 2025-12-02 | 01276 | [16, 20, 24, 36, 51, 54] |
| 2025-11-29 | 01275 | [4, 20, 24, 27, 40, 48]  |

### random 10 tickets of power 6/45

strategy 1:
|   # | Tickets                |
|----:|:-----------------------|
|   1 | [4, 8, 15, 23, 31, 40] |
|   2 | [2, 7, 13, 23, 25, 45] |

strategy 2:
|   # | Tickets                  |
|----:|:-------------------------|
|   1 | [4, 26, 32, 36, 40, 43]  |
|   2 | [5, 22, 25, 28, 31, 37]  |
|   3 | [5, 18, 23, 27, 38, 41]  |
|   4 | [3, 7, 22, 29, 38, 41]   |
|   5 | [4, 15, 24, 34, 41, 44]  |
|   6 | [4, 17, 24, 36, 40, 43]  |
|   7 | [20, 28, 33, 36, 40, 43] |
|   8 | [7, 12, 16, 28, 41, 44]  |
|   9 | [4, 10, 23, 35, 38, 42]  |
|  10 | [7, 12, 33, 38, 41, 44]  |

## top 20 details power 6/45
| date       |    id | result                   |
|:-----------|------:|:-------------------------|
| 2026-01-09 | 01456 | [8, 9, 17, 21, 36, 45]   |
| 2026-01-07 | 01455 | [1, 5, 7, 28, 31, 43]    |
| 2026-01-04 | 01454 | [2, 12, 21, 29, 35, 44]  |
| 2026-01-02 | 01453 | [7, 18, 22, 32, 37, 38]  |
| 2025-12-31 | 01452 | [1, 25, 35, 36, 37, 45]  |
| 2025-12-28 | 01451 | [1, 2, 7, 16, 31, 37]    |
| 2025-12-26 | 01450 | [4, 6, 16, 25, 27, 40]   |
| 2025-12-24 | 01449 | [15, 19, 31, 35, 43, 45] |
| 2025-12-21 | 01448 | [6, 9, 12, 18, 29, 43]   |
| 2025-12-19 | 01447 | [1, 21, 36, 42, 43, 44]  |
| 2025-12-17 | 01446 | [5, 14, 24, 38, 41, 43]  |
| 2025-12-14 | 01445 | [8, 11, 13, 16, 28, 32]  |
| 2025-12-12 | 01444 | [3, 7, 13, 17, 38, 44]   |
| 2025-12-10 | 01443 | [7, 18, 22, 29, 30, 36]  |
| 2025-12-07 | 01442 | [1, 5, 23, 28, 29, 43]   |
| 2025-12-05 | 01441 | [2, 19, 23, 37, 42, 43]  |
| 2025-12-03 | 01440 | [8, 15, 20, 23, 31, 34]  |
| 2025-11-30 | 01439 | [7, 13, 26, 30, 34, 42]  |
| 2025-11-28 | 01438 | [2, 9, 17, 23, 39, 41]   |
| 2025-11-26 | 01437 | [2, 8, 15, 19, 30, 38]   |

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

