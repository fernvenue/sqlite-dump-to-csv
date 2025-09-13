#! /usr/bin/env python3
import codecs
import csv
import logging
import os
import sqlite3

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def main(db_file, output_dir):
    logger.info(f"Connecting to database: {db_file}")
    con = sqlite3.connect(db_file)
    cur = con.cursor()

    logger.info("Retrieving database table list...")
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tabs = cur.fetchall()

    if not tabs:
        logger.warning("No tables found in database")
        return

    logger.info(f"Found {len(tabs)} tables, starting export...")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        logger.info(f"Created output directory: {output_dir}")

    exported_count = 0
    for i, tab in enumerate(tabs, 1):
        tab = tab[0]
        logger.info(f"[{i}/{len(tabs)}] Processing table: {tab}")

        cols = []
        try:
            cols = cur.execute("PRAGMA table_info('%s')" % tab).fetchall()
        except Exception as e:
            logger.warning(f"Unable to get table structure for {tab}: {e}")
            continue

        if len(cols) == 0:
            logger.warning(f"Table {tab} has no column information, skipping")
            continue

        fname = tab + '.csv'
        path_fname = os.path.join(output_dir, fname)

        try:
            with codecs.open(path_fname, 'w', encoding='utf-8') as f:
                writer = csv.writer(f, dialect=csv.excel, quoting=csv.QUOTE_ALL)

                field_name_row = [col[1] for col in cols]
                writer.writerow(field_name_row)

                cur.execute("SELECT * FROM " + f"`{tab}`" + ";")
                rows = cur.fetchall()

                for row in rows:
                    writer.writerow(row)

                logger.info(f"Export completed: {fname} ({len(rows)} records)")
                exported_count += 1

        except Exception as e:
            logger.error(f"Failed to export table {tab}: {e}")

    con.close()
    logger.info(f"Export completed! Exported {exported_count} tables to directory: {output_dir}")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        prog='sqlite_dump.py',
        description='Dump SQLite database tables to CSV files.',
        epilog='Example: python3 sqlite_dump.py --db mydb.sqlite --output ./csv_output/',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '--db',
        required=True,
        type=str,
        help='Path to the SQLite database file (e.g., mydb.sqlite)'
    )
    parser.add_argument(
        '--output',
        required=True,
        type=str,
        help='Directory to save the CSV files (will be created if it does not exist)'
    )
    args = parser.parse_args()
    main(args.db, args.output)
