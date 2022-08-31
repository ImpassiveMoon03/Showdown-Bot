import json

with open("./types.json", "r") as f:
    types = json.load(f)

def get_weaknesses(typess: []):
    tp = {}
    weak = {}
    res = {}
    if len(typess) == 1:
        tp = types[typess[0]]
        for i in tp.keys():
            if tp[i] > 1:
                weak[i] = tp[i]
            elif tp[i] < 1:
                res[i] = tp[i]
    
    else:
        for i in types[typess[0]].keys():
            tp[i] = types[typess[0]][i] * types[typess[1]][i]
            for i in tp.keys():
                if tp[i] > 1:
                    weak[i] = tp[i]
                elif tp[i] < 1:
                    res[i] = tp[i]
    
    return {
        "weaknesses": weak,
        "resistances": res
    }