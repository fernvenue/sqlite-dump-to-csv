# SQLite Dump to CSV

[![sqlite-dump-to-csv](https://img.shields.io/badge/LICENSE-MIT%20Liscense-blue?style=flat-square)](./LICENSE)
[![sqlite-dump-to-csv](https://img.shields.io/badge/GitHub-SQLite%20Dump%20to%20CSV-blueviolet?style=flat-square&logo=github)](https://github.com/fernvenue/sqlite-dump-to-csv)

Simple Python 3 script to dump a SQLite database to a set of CSV files.

## Features

- [x] Dumps all tables in a SQLite database to individual CSV files;
- [x] Rich logging for better tracking of the process;
- [x] Set logging level (DEBUG, INFO, WARNING, ERROR);

## Usage

```bash
python3 sqlite_dump.py --db mydb.sqlite --output ./csv_output/
```
