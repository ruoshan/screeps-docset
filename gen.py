#!/usr/bin/env python3

import os
import sqlite3
import sys

from bs4 import BeautifulSoup

if len(sys.argv) != 2:
    print("gen.py {version}\nAvailable versions:")
    for v in os.listdir("Documents"):
        print(f"---> {v}")
    sys.exit(1)
else:
    V = sys.argv[1]

db = sqlite3.connect("./docSet.dsidx")
cur = db.cursor()

try:
    cur.execute("DROP TABLE searchIndex;")
except:
    pass

cur.execute(
    "CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, type TEXT, path TEXT);"
)
cur.execute("CREATE UNIQUE INDEX anchor ON searchIndex (name, type, path);")

docpath = f"./Documents/{V}/api.html"


def gen_index(parent_node, klass, typ):
    for e in parent_node.find_all("h2", klass):
        title = e.attrs.get("id")
        href = f"#{title}"
        cur.execute(
            "INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?);",
            (title, typ, docpath[len("./Documents/"):] + href)
        )


page = open(docpath).read()
soup = BeautifulSoup(page, features="html.parser")
gen_index(soup, "api-property--method", "Function")
gen_index(soup, "api-property--property", "Attribute")

db.commit()
db.close()
