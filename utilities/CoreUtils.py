import json

def openfile(filename) -> list:
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def append_file(filename, to_append) -> None:
    data = openfile(filename)
    data.append(to_append)
    with open(filename, "w")as outfile:
        json.dump(data, outfile)

def parse_commands(cmd, l):
    ch = []
    for c in l:
        ch.clear()
        ch.append(c["Name"])
        for a in c["Aliases"]:
            ch.append(a)
        for k in ch:
            if cmd == k:
                return str(c["Response"])
    return None

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