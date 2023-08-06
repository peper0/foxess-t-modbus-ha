import pickle

with open("data", "rb") as f:
    data = pickle.load(f)

# print selected regs
for d in data[::]:
    print(d[0], d[10800])

# print one record as markdown table
record = data[-1]
for reg, dd in record.items():
    if isinstance(dd, list):
        for i, d in enumerate(dd):
            print(f"| {reg} | {i} | {d} |  |  |")


