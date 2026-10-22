"""
Automated Prospective Forecast Resolution Daemon.
Monitors the persistent forecast ledger in EventStore, evaluates elapsed forecasts
against empirical ground truth, and computes calibrated Brier scores deterministically.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from ..core.models import get_system_reference_date
from ..storage.event_store import EventStore


class ForecastResolutionDaemon:
    """
    Autonomous evaluation engine for forward-looking probabilistic projections.
    Scans active forecast entries, evaluates target dates against system clocks,
    and resolves outcomes with rigorous Brier calibration.
    """

    @classmethod
    def get_reference_date_str(cls, override_date: Optional[str] = None) -> str:
        """Resolves the active reference date string (YYYY-MM-DD)."""
        if override_date:
            return str(override_date).strip()[:10]
        ref = get_system_reference_date()
        if isinstance(ref, datetime):
            return ref.strftime("%Y-%m-%d")
        return str(ref)[:10]

    @classmethod
    def check_elapsed_forecasts(
        cls,
        store: EventStore,
        current_date: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieves all ACTIVE forecast records whose target_date has arrived or passed.
        """
        ref_date = cls.get_reference_date_str(current_date)
        active_forecasts = store.get_forecast_ledger(status="ACTIVE")
        elapsed = []

        for fc in active_forecasts:
            target_str = str(fc.get("target_date", "")).strip()[:10]
            if target_str and target_str <= ref_date:
                elapsed.append(fc)

        return elapsed

    @classmethod
    def auto_resolve_elapsed(
        cls,
        store: EventStore,
        ground_truth_map: Optional[Dict[str, int]] = None,
        current_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Resolves elapsed forecasts matching provided ground truth binary outcomes (0 or 1).
        Updates database status to 'RESOLVED' and computes Brier score (predicted - actual)^2.
        """
        gt_map = ground_truth_map or {}
        elapsed = cls.check_elapsed_forecasts(store, current_date=current_date)
        resolved_records = []
        brier_scores = []
        unresolved = []

        for fc in elapsed:
            fid = fc["forecast_id"]
            if fid in gt_map:
                outcome = int(gt_map[fid])
                if outcome not in (0, 1):
                    outcome = 1 if outcome > 0 else 0
                brier = store.resolve_forecast(fid, outcome)
                brier_scores.append(brier)
                resolved_records.append({
                    "forecast_id": fid,
                    "event_name": fc.get("event_name", ""),
                    "hypothesis": fc.get("hypothesis", ""),
                    "predicted_probability": fc.get("predicted_probability", 0.5),
                    "actual_outcome": outcome,
                    "brier_score": brier
                })
            else:
                unresolved.append(fid)

        mean_brier = round(sum(brier_scores) / len(brier_scores), 4) if brier_scores else None

        return {
            "elapsed_count": len(elapsed),
            "resolved_count": len(resolved_records),
            "unresolved_count": len(unresolved),
            "resolved_records": resolved_records,
            "mean_brier_score": mean_brier,
            "unresolved_forecast_ids": unresolved
        }

    @classmethod
    def get_ledger_calibration_summary(cls, store: EventStore) -> Dict[str, Any]:
        """
        Computes aggregate statistical calibration metrics across all records in the ledger.
        """
        all_records = store.get_forecast_ledger()
        total_count = len(all_records)
        active_count = sum(1 for r in all_records if r.get("status") == "ACTIVE")
        resolved_records = [r for r in all_records if r.get("status") == "RESOLVED" and r.get("brier_score") is not None]
        resolved_count = len(resolved_records)

        if not resolved_records:
            return {
                "total_forecasts": total_count,
                "active_forecasts": active_count,
                "resolved_forecasts": 0,
                "mean_brier_score": None,
                "calibration_grade": "INSUFFICIENT_RESOLVED_DATA",
                "best_forecast": None,
                "worst_forecast": None
            }

        brier_values = [float(r["brier_score"]) for r in resolved_records]
        mean_brier = round(sum(brier_values) / len(brier_values), 4)

        # Grade calibration: 0.0 - 0.10: Exceptional, 0.10 - 0.20: Strong, 0.20 - 0.25: Neutral, > 0.25: Degraded
        if mean_brier <= 0.10:
            grade = "EXCEPTIONAL_CALIBRATION"
        elif mean_brier <= 0.20:
            grade = "STRONG_PREDICTIVE_CALIBRATION"
        elif mean_brier <= 0.25:
            grade = "BASELINE_RANDOM_BOUNDARY"
        else:
            grade = "SUB_OPTIMAL_CALIBRATION"

        sorted_records = sorted(resolved_records, key=lambda x: float(x["brier_score"]))
        best_fc = sorted_records[0]
        worst_fc = sorted_records[-1]

        return {
            "total_forecasts": total_count,
            "active_forecasts": active_count,
            "resolved_forecasts": resolved_count,
            "mean_brier_score": mean_brier,
            "calibration_grade": grade,
            "best_forecast": {
                "forecast_id": best_fc["forecast_id"],
                "hypothesis": best_fc["hypothesis"],
                "brier_score": best_fc["brier_score"]
            },
            "worst_forecast": {
                "forecast_id": worst_fc["forecast_id"],
                "hypothesis": worst_fc["hypothesis"],
                "brier_score": worst_fc["brier_score"]
            }
        }
