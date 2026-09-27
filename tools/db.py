#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Command-line access to instance/restaurant.db, with no install needed.

The proper tool for this job is the sqlite3 CLI (apt install sqlite3). This
is the stand-in for a machine that does not have it: Python ships the sqlite3
library regardless, so this works everywhere the site itself runs.

    python3 tools/db.py                      interactive SQL prompt
    python3 tools/db.py tables               every table and its row count
    python3 tools/db.py schema business_hours
    python3 tools/db.py show business_hours
    python3 tools/db.py "SELECT * FROM menu_item WHERE category='fish'"
    python3 tools/db.py --backup             timestamped copy, before you edit

Reads print as a table. INSERT/UPDATE/DELETE commit straight away and report
how many rows moved, so nothing is left half-applied in an open transaction.
"""
import os
import shutil
import sqlite3
import sys
from datetime import datetime

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(HERE, "instance", "restaurant.db")

# sqlite reserves ORDER, so the orders table only resolves when quoted. Worth
# saying out loud because the error it produces ("near \"order\": syntax
# error") points at the wrong thing.
RESERVED_HINT = (
    'The orders table is named "order", which is a reserved word - '
    'write it quoted:  SELECT * FROM "order";'
)

WRITES = ("insert", "update", "delete", "replace", "create", "drop", "alter")


def connect():
    if not os.path.exists(DB):
        sys.exit(f"No database at {DB}\nRun python3 app.py once to create it.")
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def render(rows):
    """Print rows as an aligned table.

    Hebrew is stored throughout, so widths are counted in characters rather
    than bytes; a terminal renders Hebrew at roughly one cell per character.
    """
    if not rows:
        print("(no rows)")
        return
    cols = rows[0].keys()
    cells = [[("" if r[c] is None else str(r[c])) for c in cols] for r in rows]
    widths = [
        max(len(str(col)), max((len(row[i]) for row in cells), default=0))
        for i, col in enumerate(cols)
    ]
    line = "  ".join(str(c).ljust(w) for c, w in zip(cols, widths))
    print(line)
    print("  ".join("-" * w for w in widths))
    for row in cells:
        print("  ".join(v.ljust(w) for v, w in zip(row, widths)))
    print(f"\n{len(rows)} row{'s' if len(rows) != 1 else ''}")


def run(conn, sql):
    """Execute one statement; commit it if it changed anything."""
    try:
        cur = conn.execute(sql)
    except sqlite3.Error as exc:
        print(f"error: {exc}")
        if "order" in sql.lower() and '"order"' not in sql.lower():
            print(RESERVED_HINT)
        return
    if sql.strip().lower().startswith(WRITES):
        conn.commit()
        print(f"OK - {cur.rowcount} row{'s' if cur.rowcount != 1 else ''} affected")
    else:
        render(cur.fetchall())


def table_names(conn):
    return [
        r[0] for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' "
            "AND name NOT LIKE 'sqlite_%' ORDER BY name"
        )
    ]


def cmd_tables(conn):
    for name in table_names(conn):
        count = conn.execute(f'SELECT COUNT(*) FROM "{name}"').fetchone()[0]
        print(f"  {name:<16} {count:>5} rows")


def cmd_schema(conn, table):
    render(conn.execute(f'PRAGMA table_info("{table}")').fetchall())


def cmd_backup():
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    dest = os.path.join(os.path.dirname(DB), f"restaurant-{stamp}.db")
    shutil.copyfile(DB, dest)
    print(f"Copied to {dest}")


def interactive(conn):
    print(f"{DB}\nTables: {', '.join(table_names(conn))}")
    print("Type SQL ending in ';' - or .tables, .schema <table>, .quit\n")
    buffer = ""
    while True:
        try:
            line = input("sql> " if not buffer else "...> ")
        except (EOFError, KeyboardInterrupt):
            print()
            return
        stripped = line.strip()
        if not buffer and stripped in (".quit", ".exit", "quit", "exit"):
            return
        if not buffer and stripped == ".tables":
            cmd_tables(conn)
            continue
        if not buffer and stripped.startswith(".schema "):
            cmd_schema(conn, stripped.split(None, 1)[1])
            continue
        # Statements may span lines; a trailing ';' is what ends one.
        buffer += " " + line
        if ";" in buffer:
            run(conn, buffer.strip().rstrip(";"))
            buffer = ""


def main():
    args = sys.argv[1:]
    if args and args[0] == "--backup":
        return cmd_backup()

    conn = connect()
    if not args:
        return interactive(conn)
    if args[0] == "tables":
        return cmd_tables(conn)
    if args[0] == "schema" and len(args) > 1:
        return cmd_schema(conn, args[1])
    if args[0] == "show" and len(args) > 1:
        return render(conn.execute(f'SELECT * FROM "{args[1]}"').fetchall())
    run(conn, " ".join(args))


if __name__ == "__main__":
    main()
