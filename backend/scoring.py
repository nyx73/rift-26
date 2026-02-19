def generate_scores(

    cycles,
    smurf,
    shells,
    velocity,
    anomaly,
    pagerank,
    flow

):

    suspicious = {}
    rings = []
    acc_ring = {}


    ring_id = 1


    for cycle in cycles:

        rid = f"RING_{ring_id:03d}"

        rings.append({

            "ring_id": rid,

            "member_accounts": cycle,

            "pattern_type": "cycle",

            "risk_score": 90
        })


        for acc in cycle:

            acc_ring[acc] = rid

        ring_id += 1


    def get(acc):

        if acc not in suspicious:

            suspicious[acc] = {

                "account_id": acc,

                "suspicion_score": 0,

                "detected_patterns": [],

                "ring_id": acc_ring.get(acc, "")
            }

        return suspicious[acc]


    for acc in acc_ring:

        get(acc)["suspicion_score"] += 50


    for acc in smurf["fan_in"]:

        get(acc)["suspicion_score"] += 25


    for acc in smurf["fan_out"]:

        get(acc)["suspicion_score"] += 20


    for acc in shells:

        get(acc)["suspicion_score"] += 15


    for acc in velocity:

        get(acc)["suspicion_score"] += 25


    for acc in anomaly:

        get(acc)["suspicion_score"] += 10


    for acc in suspicious:

        suspicious[acc]["suspicion_score"] += pagerank.get(acc, 0)


    result = list(suspicious.values())

    result.sort(
        key=lambda x: x["suspicion_score"],
        reverse=True
    )

    return result, rings
