import random
import argparse
import threading
import time

INF = 16

tables = {}
neighbors = {}
changed = False
lock = threading.Lock()
barrier = None
stop = False

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
    result = {r: [] for r in routers}

    for a, b in links:
        result[a].append(b)
        result[b].append(a)

    return result

def make_start_tables(routers):
    result = {}

    for r in routers:
        result[r] = {}
        result[r][r] = (r, 0)

        for nb in neighbors[r]:
            result[r][nb] = (nb, 1)

    return result

def print_table(title, router, table):
    print(title)
    print(f"{'[Source IP]':<18}{'[Destination IP]':<20}{'[Next Hop]':<18}{'[Metric]':>8}")

    for dest in table:
        if dest != router:
            next_hop, metric = table[dest]
            print(f"{router:<18}{dest:<20}{next_hop:<18}{metric:>8}")

    print()

def router_work(router):
    global changed
    global stop

    while True:
        barrier.wait()

        if stop:
            break

        with lock:
            old_tables = {}
            for r in tables:
                old_tables[r] = tables[r].copy()

        local_changed = False

        for nb in neighbors[router]:
            for dest in old_tables[nb]:
                if dest == router:
                    continue

                new_metric = old_tables[nb][dest][1] + 1

                if new_metric >= INF:
                    continue

                with lock:
                    if dest not in tables[router] or new_metric < tables[router][dest][1]:
                        tables[router][dest] = (nb, new_metric)
                        local_changed = True

        if local_changed:
            with lock:
                changed = True

        barrier.wait()

def main():
    global tables
    global neighbors
    global changed
    global barrier
    global stop

    parser = argparse.ArgumentParser()
    parser.add_argument("--routers", type=int, default=5)
    parser.add_argument("--extra-links", type=int, default=1)
    parser.add_argument("--seed", type=int, default=1)
    args = parser.parse_args()

    random.seed(args.seed)

    routers, links = make_network(args.routers, args.extra_links)
    neighbors = make_neighbors(routers, links)
    tables = make_start_tables(routers)

    barrier = threading.Barrier(len(routers) + 1)

    threads = []
    for r in routers:
        t = threading.Thread(target=router_work, args=(r,))
        threads.append(t)
        t.start()

    print("Routers:")
    for r in routers:
        print(r)

    print("\nLinks:")
    for a, b in links:
        print(a, "<->", b)

    print()

    step = 0

    while True:
        step += 1
        changed = False

        barrier.wait()
        barrier.wait()

        print(f"Simulation step {step}")

        with lock:
            for r in routers:
                print_table(f"Current table of router {r}", r, tables[r])

        if not changed:
            print("Protocol converged.")
            break

        time.sleep(0.3)

    stop = True
    barrier.wait()

    for t in threads:
        t.join()

    print("Final tables:")
    for r in routers:
        print_table(f"Final state of router {r} table:", r, tables[r])

if __name__ == "__main__":
    main()