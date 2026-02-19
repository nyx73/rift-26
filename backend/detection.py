from collections import defaultdict
import numpy as np



def build_graph(transactions):

    graph = defaultdict(dict)

    for tx in transactions:

        s = tx["sender_id"]
        r = tx["receiver_id"]
        amt = tx["amount"]

        graph[s][r] = graph[s].get(r, 0) + amt

    return graph


def compute_flow_metrics(transactions):

    incoming = defaultdict(float)
    outgoing = defaultdict(float)
    count = defaultdict(int)

    for tx in transactions:

        s = tx["sender_id"]
        r = tx["receiver_id"]
        amt = tx["amount"]

        outgoing[s] += amt
        incoming[r] += amt

        count[s] += 1
        count[r] += 1


    metrics = {}

    for acc in set(list(incoming) + list(outgoing)):

        metrics[acc] = {

            "incoming_total": incoming[acc],

            "outgoing_total": outgoing[acc],

            "net_flow":
                incoming[acc] - outgoing[acc],

            "transaction_count": count[acc]
        }

    return metrics


# FAST cycle detection (bounded)

def detect_cycles(graph, min_len=3, max_len=5):

    cycles = []

    def dfs(start, node, path):

        if len(path) > max_len:
            return

        for neighbor in graph.get(node, {}):

            if neighbor == start and len(path) >= min_len:

                cycles.append(path.copy())

            elif neighbor not in path:

                dfs(start, neighbor, path + [neighbor])


    for node in graph:

        dfs(node, node, [node])

    return cycles


def detect_smurfing(transactions):

    recv = defaultdict(set)
    send = defaultdict(set)

    for tx in transactions:

        recv[tx["receiver_id"]].add(tx["sender_id"])
        send[tx["sender_id"]].add(tx["receiver_id"])


    return {

        "fan_in":

            [k for k, v in recv.items()
             if len(v) >= 10],

        "fan_out":

            [k for k, v in send.items()
             if len(v) >= 10]
    }


def detect_shell_accounts(transactions):

    incoming = defaultdict(int)
    outgoing = defaultdict(int)

    for tx in transactions:

        incoming[tx["receiver_id"]] += 1
        outgoing[tx["sender_id"]] += 1


    return [

        acc

        for acc in set(list(incoming) + list(outgoing))

        if incoming[acc] > 0
        and outgoing[acc] > 0
        and incoming[acc] + outgoing[acc] <= 3
    ]


def detect_high_velocity(transactions):

    count = defaultdict(int)

    for tx in transactions:

        count[tx["sender_id"]] += 1


    return [

        acc for acc, c in count.items()

        if c >= 4
    ]


def detect_amount_anomalies(transactions):

    amounts = [tx["amount"] for tx in transactions]

    mean = np.mean(amounts)
    std = np.std(amounts)

    return [

        tx["sender_id"]

        for tx in transactions

        if (tx["amount"] - mean) / std >= 2
    ]


# FAST pagerank approximation

def compute_pagerank(graph):

    score = defaultdict(float)

    for node in graph:

        score[node] = len(graph[node])

    return score
