from __future__ import annotations

import argparse
from dataclasses import asdict
import json
from pathlib import Path

from oddsharvester.predict.backtest import build_calibration_map
from oddsharvester.predict.engine import PredictionEngine
from oddsharvester.predict.io import export_predictions, load_events


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate predictions from OddsHarvester JSON exports.")
    parser.add_argument("--input", required=True, help="Upcoming JSON export path")
    parser.add_argument("--calibration-input", help="Historic JSON export path used for calibration")
    parser.add_argument(
        "--markets",
        default="1x2,double_chance,over_1_5,over_2_5,under_3_5,btts",
        help="Comma-separated markets to evaluate",
    )
    parser.add_argument("--top", type=int, default=25, help="Maximum number of rows to keep")
    parser.add_argument("--min-confidence", type=float, default=60.0, help="Minimum confidence 0-100")
    parser.add_argument("--bankroll", type=float, default=0.0, help="Optional bankroll for Kelly stake suggestions")
    parser.add_argument("--kelly-fraction", type=float, default=0.25, help="Fractional Kelly multiplier")
    parser.add_argument("--output", default="predictions.json", help="Output file path")
    parser.add_argument("--output-format", choices=["json", "csv"], default="json", help="Output format")
    args = parser.parse_args()

    events = load_events(Path(args.input))
    calibration_map = None
    if args.calibration_input:
        calibration_map = build_calibration_map(load_events(Path(args.calibration_input)))

    engine = PredictionEngine(calibration_map=calibration_map)
    predictions = engine.predict_many(
        events=events,
        markets=[m.strip() for m in args.markets.split(",") if m.strip()],
        top=args.top,
        min_confidence=args.min_confidence,
        bankroll=args.bankroll,
        kelly_fraction=args.kelly_fraction,
    )
    export_predictions(predictions, Path(args.output), args.output_format)
    print(json.dumps([asdict(p) for p in predictions[: min(5, len(predictions))]], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
