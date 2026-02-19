from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

import time
import csv
import io

from concurrent.futures import ThreadPoolExecutor

from detection import (
    build_graph,
    compute_flow_metrics,
    detect_cycles,
    detect_smurfing,
    detect_shell_accounts,
    detect_high_velocity,
    detect_amount_anomalies,
    compute_pagerank
)

from scoring import generate_scores


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def load_transactions(contents):

    transactions = []

    reader = csv.DictReader(io.StringIO(contents.decode()))

    for row in reader:

        transactions.append({
            "transaction_id": row["transaction_id"],
            "sender_id": row["sender_id"],
            "receiver_id": row["receiver_id"],
            "amount": float(row["amount"]),
            "timestamp": row["timestamp"]
        })

    return transactions


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):

    start_time = time.time()

    contents = await file.read()

    transactions = load_transactions(contents)

    graph = build_graph(transactions)


    with ThreadPoolExecutor() as executor:

        future_cycles = executor.submit(detect_cycles, graph)
        future_smurf = executor.submit(detect_smurfing, transactions)
        future_shells = executor.submit(detect_shell_accounts, transactions)
        future_velocity = executor.submit(detect_high_velocity, transactions)
        future_anomaly = executor.submit(detect_amount_anomalies, transactions)
        future_pr = executor.submit(compute_pagerank, graph)
        future_flow = executor.submit(compute_flow_metrics, transactions)

        cycles = future_cycles.result()
        smurf = future_smurf.result()
        shells = future_shells.result()
        velocity = future_velocity.result()
        anomaly = future_anomaly.result()
        pagerank = future_pr.result()
        flow = future_flow.result()


    suspicious_accounts, fraud_rings = generate_scores(
        cycles,
        smurf,
        shells,
        velocity,
        anomaly,
        pagerank,
        flow
    )


    graph_edges = [

        {
            "source": s,
            "target": r,
            "weight": w
        }

        for s in graph
        for r, w in graph[s].items()

    ]


    return {

        "suspicious_accounts": suspicious_accounts,

        "fraud_rings": fraud_rings,

        "graph_edges": graph_edges,

        "summary": {

            "total_accounts_analyzed": len(graph),

            "suspicious_accounts_flagged": len(suspicious_accounts),

            "fraud_rings_detected": len(fraud_rings),

            "processing_time_seconds":
                round(time.time() - start_time, 2)
        }
    }
