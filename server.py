from socket import *

def hex_to_ipv4(h: str) -> str:
    # convert to int
    val = int(h, 16)
    # separate octets
    octets = []
    for i in range(4):
        octets.append( (val >> (i * 8)) & 0xFF ) # top byte == last octet
    # convert to strings + combine
    return '.'.join([str(i) for i in octets])

def decode_flags(f: str) -> str:
    # flags from route.h (https://github.com/torvalds/linux/blob/master/include/uapi/linux/route.h)
    flags = {
        "UP": 0x0001,
        "GATEWAY": 0x0002,
        "HOST": 0x0004,
        "REINSTATE": 0x0008,
        "DYNAMIC": 0x0010,
        "MODIFIED": 0x0020,
        "MTU": 0x0040,
        "MSS": 0x0040,
        "WINDOW": 0x0080,
        "IRTT": 0x0100,
        "REJECT": 0x0200
    }

    val = int(f, 16)
    res = []
    for k in list(flags.keys()):
        if val & flags[k]: res.append(k)
    
    return ', '.join(res)


def get_route_table() -> str:
    # read table
    f = open("/proc/net/route")
    lines = f.readlines()
    f.close()

    # defined table columns to display
    keys = ["Iface", "Destination", "Mask", "Metric", "Gateway", "Flags"]
    # table columns in ipv4 addr format
    ipv4_fields = ["Mask", "Gateway", "Destination"]

    # cleanup data
    lines = [[j.strip() for j in i.strip().split("\t")] for i in lines]
    # create dict from table data (key from 1. line, values from other)
    data = [{lines[0][i]: lines[j][i] for i in range(len(lines[1]))} for j in range(1, len(lines))]

    # resolve ipv4 + flags
    for dato in data:
        # convert ipv4 to readable form
        for f in ipv4_fields:
            dato[f] = hex_to_ipv4(dato[f])
        # decode flags
        dato["Flags"] = decode_flags(dato["Flags"])

    # -- generate table --
    # table header
    values = ""
    for key in keys:
        values += f"<td>{key}</td>"

    rows = f"\t<tr>{values}</tr>\n"

    # table data
    for line in data:
        gateway = "GATEWAY" in line["Flags"] # to bold or not to bold?
        values = ""
        for key in keys:
            if gateway: 
                values += f"<td><b>{line[key]}</b></td>"
            else: 
                values += f"<td>{line[key]}</td>"
        rows += f"\t<tr>{values}</tr>\n"
    
    table = f"<html>\n<table border=\"black 1px\">\n{rows}</table>\n</html>\n"

    return table

def main():
    s= socket(AF_INET, SOCK_STREAM) 
    s.bind(('127.0.0.1', 8080))
    s.listen(1)

    while True:
        c, addr = s.accept()
        print(f"Connected to {addr}\n")

        try: 
            c.send("HTTP/1.1 200 OK\r\n\r\n".encode())
            c.send(get_route_table().encode())
            c.close()
        except IOError:
            c.send("HTTP/1.0 404 Not Found\r\n".encode());

        c.close()

if __name__ == "__main__":
    main()