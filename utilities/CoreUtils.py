# common functions used across multiple files

import json
import logging


def logger(name: str) -> logging.Logger:
    return logging.getLogger(name)


LOGGER = logger("CoreUtils")


# open a file to read
def openfile(filename) -> list:
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


# write data to a file
def writefile(data, filename) -> None:
    with open(filename, "w") as outfile:
        json.dump(data, outfile)


# add an entry to a file
def append_file(filename, to_append) -> None:
    data = openfile(filename)
    data.append(to_append)
    writefile(data, filename)


# remove an entry from a file
def remove_from_file(filename, to_remove) -> None:
    data = openfile(filename)
    data.remove(to_remove)
    writefile(data, filename)


# parse list of commands for a specific command, returns none if command not found
def parse_commands(cmd, l) -> dict | None:
    ch = []
    for c in l:
        ch.clear()
        ch.append(c["Name"])
        for a in c["Aliases"]:
            ch.append(a)
        for k in ch:
            if cmd == k:
                return c
    return None


# get a single string from command arguments
def concat_string_from_args(t: tuple) -> str:
    s = ""
    c = 0
    for a in t:
        if c == len(t) - 1:
            s += a
        else:
            c += 1
            s += (a + " ")
    return s
