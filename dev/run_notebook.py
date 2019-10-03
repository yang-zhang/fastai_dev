#!/usr/bin/env python

# TODO: parallel

from pathlib import Path
from local.script import *
from local.notebook.test import test_nb

def get_fns(path,max_num,fn):
    path = Path(path)
    if fn: return path.glob(fn)
    fns = list(path.glob("*.ipynb"))
    return [f for f in fns if f.name<max_num and not f.name.startswith('_')]

@call_parse
def main(path:Param("Path to notebooks",str)=".", max_num:Param("Max numbered notebook to run",str)=999,
         fn:Param("Filename glob",str)=None, cuda:Param("Run tests that require a GPU", bool)=False,
         slow:Param("Run slow tests", bool)=False, cpp:Param("Run tests that require c++ extensions", bool)=False):
    "Tests notebooks in `path` and shows any exceptions."
    fns = get_fns(path,max_num,fn)
    flags = ["cuda"] if cuda else []
    if slow: flags.append("slow")
    if cpp:  flags.append("cpp")
    for f in sorted(fns): test_nb(f, flags=flags)

