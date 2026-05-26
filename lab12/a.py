import random
import argparse

INF = 16

def make_ip(used):
    while True:
        ip = ".".join(str(random.randint(1, 254)) for _ in range(4))
        if ip not in used:
            used.add(ip)
            return ip

def make_network(n, extra_links):
    used = set()
    routers = [make_ip(used) for _ in range(n)]

    links = []

    for i in range(n - 1):
        links.append((routers[i], routers[i + 1]))

    possible = []
    for i in range(n):
        for j in range(i + 1, n):
            a, b = routers[i], routers[j]
            if (a, b) not in links and (b, a) not in links:
                possible.append((a, b))

    random.shuffle(possible)
    links += possible[:extra_links]

    return routers, links

def make_neighbors(routers, links):
    neighbors = {r: [] for r in routers}
    for a, b in links:
        neighbors[a].append(b)
        neighbors[b].append(a)
    return neighbors

def make_start_tables(routers, neighbors):
    tables = {}
    for r in routers:
        tables[r] = {}
        tables[r][r] = (r, 0)

        for nb in neighbors[r]:
            tables[r][nb] = (nb, 1)
    return tables

def rip(routers, neighbors, tables):
    changed = True

    while changed:
        changed = False

        old_tables = {}
        for r in routers:
            old_tables[r] = tables[r].copy()

        for r in routers:
            for nb in neighbors[r]:
                for dest in old_tables[nb]:
                    if dest == r:
                        continue

                    new_metric = old_tables[nb][dest][1] + 1

                    if new_metric >= INF:
                        continue

                    if dest not in tables[r] or new_metric < tables[r][dest][1]:
                        tables[r][dest] = (nb, new_metric)
                        changed = True
    return tables

def print_table(router, table):
    print(f"Final state of router {router} table:")
    print(f"{'[Source IP]':<18}{'[Destination IP]':<20}{'[Next Hop]':<18}{'[Metric]':>8}")
    for dest in table:
        if dest != router:
            next_hop, metric = table[dest]
            print(f"{router:<18}{dest:<20}{next_hop:<18}{metric:>8}")
    print()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--routers", type=int, default=5)
    parser.add_argument("--extra-links", type=int, default=1)
    parser.add_argument("--seed", type=int, default=1)
    args = parser.parse_args()

    random.seed(args.seed)

    routers, links = make_network(args.routers, args.extra_links)
    neighbors = make_neighbors(routers, links)
    tables = make_start_tables(routers, neighbors)

    print("Routers:")
    for r in routers:
        print(r)

    print("\nLinks:")
    for a, b in links:
        print(a, "<->", b)

    print()

    tables = rip(routers, neighbors, tables)

    for r in routers:
        print_table(r, tables[r])

if __name__ == "__main__":
    main()