
def get_route_table() -> str:
    f = open("/proc/net/route")
    lines = f.readlines()
    f.close()

    keys = ["Iface", "Destination", "Gateway"]

    # cleanup data
    lines = [[j.strip() for j in i.strip().split("\t")] for i in lines]

    # create dict from table data
    data = [{lines[0][i]: lines[j][i] for i in range(len(lines[1]))} for j in range(1, len(lines))]

    # generate HTMl table

    # header
    values = ""
    for key in keys:
        values += f"<td>{key}</td>"

    rows = f"\t<tr>{values}</tr>\n"

    # data
    for line in data:
        values = ""
        for key in keys:
            values += f"<td>{line[key]}</td>"
        rows += f"\t<tr>{values}</tr>\n"
    
    table = f"<table border=\"black 1px\">\n{rows}</table>\n"

    return table


if __name__ == "__main__":
    print(get_route_table())