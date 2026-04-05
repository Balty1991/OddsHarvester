from __future__ import annotations

from collections import defaultdict

from oddsharvester.predict.features import collect_market_consensus, derive_probabilities
from oddsharvester.predict.result_eval import evaluate_outcome


def build_calibration_map(events):
    buckets_by_key: dict[tuple[str, str, int], list[int]] = defaultdict(list)

    for event in events:
        if not event.result:
            continue
        derived = derive_probabilities(collect_market_consensus(event))
        for market, selections in derived.items():
            for selection, probability in selections.items():
                outcome = evaluate_outcome(event, market, selection)
                if outcome is None:
                    continue
                bucket = int(min(9, max(0, probability * 10)))
                buckets_by_key[(market, selection, bucket)].append(1 if outcome else 0)

    calibration_map: dict[str, dict[str, dict[str, list[dict[str, float]]]]] = defaultdict(lambda: defaultdict(dict))
    for (market, selection, bucket), results in buckets_by_key.items():
        low = bucket / 10
        high = min(0.999, (bucket + 1) / 10)
        empirical = sum(results) / len(results)
        calibration_map[market].setdefault(selection, {"buckets": []})["buckets"].append(
            {"low": low, "high": high, "empirical": round(empirical, 4), "count": len(results)}
        )

    return calibration_map
