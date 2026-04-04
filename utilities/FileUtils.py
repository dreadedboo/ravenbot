import json

def openfile(filename) -> dict:
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

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