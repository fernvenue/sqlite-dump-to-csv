#! /usr/bin/env python3
import codecs
import os
import sqlite3
import csv


def main(db_file, output_dir):
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tabs = cur.fetchall()
    for tab in tabs:
        tab = tab[0]
        cols = []
        try:
            cols = cur.execute("PRAGMA table_info('%s')" % tab).fetchall()
        except:
            cols = []
        if len(cols) > 0:
            fname = tab + '.csv'
            print('Output: ' + fname)
            path_fname = os.path.join(output_dir, fname)
            f = codecs.open(path_fname, 'w', encoding='utf-8')
            writer = csv.writer(f, dialect=csv.excel, quoting=csv.QUOTE_ALL)
            field_name_row = []
            for col in cols:
                col_name = col[1]
                field_name_row.append(col_name)
            writer.writerow(field_name_row)
            cur.execute("SELECT * FROM " + f"`{tab}`" + ";")
            rows = cur.fetchall()
            for row in rows:
               writer.writerow(row)
            f.closed
    print("Done! " + output_dir)

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
