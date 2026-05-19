from collections import deque

INF = 10 ** 9

class Network:
    def __init__(self):
        self.graph = {}
        self.tables = {}
        self.received = {}
        self.queue = deque()

    def add_node(self, node):
        if node not in self.graph:
            self.graph[node] = {}
            self.tables[node] = {node: (0, node)}
            self.received[node] = {}

    def add_link(self, a, b, cost):
        self.add_node(a)
        self.add_node(b)

        self.graph[a][b] = cost
        self.graph[b][a] = cost

        self.recalculate(a)
        self.recalculate(b)

    def get_vector(self, node):
        result = {}

        for dest, route in self.tables[node].items():
            cost, next_hop = route
            result[dest] = cost

        return result

    def send_vector(self, node):
        vector = self.get_vector(node)

        for neighbor in self.graph[node]:
            self.queue.append((node, neighbor, vector.copy()))

    def send_all_vectors(self):
        for node in self.graph:
            self.send_vector(node)

    def recalculate(self, node):
        old_table = self.tables[node]

        destinations = {node}

        for neighbor in self.graph[node]:
            destinations.add(neighbor)

        for vector in self.received[node].values():
            for dest in vector:
                destinations.add(dest)

        new_table = {node: (0, node)}

        for dest in destinations:
            if dest == node:
                continue

            best_cost = INF
            best_next_hop = None

            for neighbor, link_cost in self.graph[node].items():
                if dest == neighbor:
                    neighbor_cost = 0
                else:
                    neighbor_vector = self.received[node].get(neighbor, {})
                    neighbor_cost = neighbor_vector.get(dest, INF)

                total_cost = link_cost + neighbor_cost

                if total_cost < best_cost:
                    best_cost = total_cost
                    best_next_hop = neighbor

            if best_next_hop is not None and best_cost < INF:
                new_table[dest] = (best_cost, best_next_hop)

        self.tables[node] = new_table

        return old_table != new_table

    def run(self):
        while self.queue:
            from_node, to_node, vector = self.queue.popleft()

            self.received[to_node][from_node] = vector

            changed = self.recalculate(to_node)

            if changed:
                self.send_vector(to_node)

    def change_link(self, a, b, new_cost):
        self.graph[a][b] = new_cost
        self.graph[b][a] = new_cost

        self.recalculate(a)
        self.recalculate(b)

        self.send_vector(a)
        self.send_vector(b)

        self.run()

    def get_costs(self):
        result = {}

        for node in self.tables:
            result[node] = {}

            for dest, route in self.tables[node].items():
                cost, next_hop = route
                result[node][dest] = cost

        return result

def create_network():
    network = Network()

    network.add_link(0, 1, 1)
    network.add_link(1, 2, 1)
    network.add_link(2, 3, 2)
    network.add_link(0, 3, 7)
    network.add_link(0, 2, 3)

    return network

def test_task_a():
    network = create_network()

    network.send_all_vectors()
    network.run()

    expected = {
        0: {0: 0, 1: 1, 2: 2, 3: 4},
        1: {0: 1, 1: 0, 2: 1, 3: 3},
        2: {0: 2, 1: 1, 2: 0, 3: 2},
        3: {0: 4, 1: 3, 2: 2, 3: 0},
    }

    assert network.get_costs() == expected

def test_task_b():
    network = create_network()

    network.send_all_vectors()
    network.run()

    network.change_link(0, 3, 1)

    expected = {
        0: {0: 0, 1: 1, 2: 2, 3: 1},
        1: {0: 1, 1: 0, 2: 1, 3: 2},
        2: {0: 2, 1: 1, 2: 0, 3: 2},
        3: {0: 1, 1: 2, 2: 2, 3: 0},
    }

    assert network.get_costs() == expected

def main():
    test_task_a()
    print("Задание A: OK")

    test_task_b()
    print("Задание B: OK")

if __name__ == "__main__":
    main()