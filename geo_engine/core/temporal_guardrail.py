"""
Temporal Guardrail to prevent future-data hallucinations and temporal conflation.
Enforces strict boundaries between verified empirical archives, live data,
and prospective/horizon (e.g., 2026) game-theoretic projections.
"""

from datetime import datetime
from typing import Tuple
from .models import TemporalMode, SummitEvent, get_system_reference_date


class TemporalGuardrail:
    """
    Validates the temporal frame of an analysis request.
    Prevents confusing retrospective reporting with prospective scenario projections.
    """

    REFERENCE_DATE = get_system_reference_date()

    CONSTITUTIONAL_TENURE_REGISTRY = {
        "gyanesh_kumar": [
            {
                "office": "Chief Election Commissioner",
                "start_date": "2025-02-19",
                "end_date": "2029-01-26",
                "predecessor": "Rajiv Kumar"
            },
            {
                "office": "Election Commissioner",
                "start_date": "2024-03-15",
                "end_date": "2025-02-18",
                "predecessor": "Anup Chandra Pandey"
            },
            {
                "office": "Secretary, Ministry of Cooperation",
                "start_date": "2022-05-01",
                "end_date": "2024-01-31",
                "predecessor": "Devendra Kumar Singh"
            }
        ],
        "rajiv_kumar": [
            {
                "office": "Chief Election Commissioner",
                "start_date": "2022-05-15",
                "end_date": "2025-02-18",
                "predecessor": "Sushil Chandra"
            }
        ],
        "sukhbir_singh_sandhu": [
            {
                "office": "Election Commissioner",
                "start_date": "2024-03-15",
                "end_date": "2029-02-01",
                "predecessor": "Arun Goel"
            }
        ]
    }

    @classmethod
    def verify_chronological_feasibility(
        cls,
        person_key: str,
        office_keyword: str,
        event_date_str: str
    ) -> dict:
        """
        Level-0 Atomic Epistemic Gate:
        Mathematically asserts whether a constitutional officer was legally in office on event_date.
        Prevents anachronistic fabrications from entering macro-analytic evaluation.
        """
        normalized_key = person_key.lower().strip().replace(" ", "_")
        tenures = cls.CONSTITUTIONAL_TENURE_REGISTRY.get(normalized_key, [])

        if not tenures:
            return {
                "is_chronologically_feasible": True,
                "verified": False,
                "message": f"Officer '{person_key}' not in static gazette registry; defaulting to open verification."
            }

        # Match office
        office_match = None
        for t in tenures:
            if office_keyword.lower() in t["office"].lower():
                office_match = t
                break

        if not office_match:
            return {
                "is_chronologically_feasible": False,
                "verified": True,
                "classification": "ANACHRONISTIC_OFFICE_MISMATCH",
                "message": f"'{person_key}' never held office matching '{office_keyword}'."
            }

        start = office_match["start_date"]
        end = office_match["end_date"]
        event_clean = event_date_str.strip()[:10]

        if event_clean < start:
            predecessor = office_match.get("predecessor", "Predecessor")
            return {
                "is_chronologically_feasible": False,
                "verified": True,
                "classification": "ANACHRONISTIC_FABRICATION",
                "message": (
                    f"Chronologically impossible: '{person_key}' did not assume office as '{office_match['office']}' "
                    f"until {start}. Event occurred on {event_date_str} under predecessor '{predecessor}'."
                )
            }
        elif event_clean > end:
            return {
                "is_chronologically_feasible": False,
                "verified": True,
                "classification": "ANACHRONISTIC_FABRICATION",
                "message": (
                    f"Chronologically impossible: '{person_key}' demitted office as '{office_match['office']}' "
                    f"on {end}. Event occurred on {event_date_str}."
                )
            }

        return {
            "is_chronologically_feasible": True,
            "verified": True,
            "classification": "CHRONOLOGICALLY_VERIFIED",
            "message": f"Verified: '{person_key}' was incumbent in '{office_match['office']}' on {event_date_str}."
        }

    @classmethod
    def get_reference_date(cls) -> datetime:
        """Returns the centralized runtime reference date."""
        return get_system_reference_date()

    @classmethod
    def evaluate_event_mode(cls, summit: SummitEvent) -> Tuple[TemporalMode, str]:
        """
        Determines the epistemic temporal mode of the summit.
        """
        current_year = get_system_reference_date().year
        if summit.year < current_year:
            mode = TemporalMode.EMPIRICAL_HISTORICAL
            guidance = (
                f"Summit year {summit.year} is in the historical past. "
                "Analysis must be grounded in ratified communiques and empirical balance-of-payments archives."
            )
        elif summit.year == current_year:
            mode = TemporalMode.PROSPECTIVE_SCENARIO
            guidance = (
                f"Summit year {summit.year} is current/horizon. "
                "Analysis must be strictly partitioned into: "
                "(1) Verified institutional trajectory & established national redlines, and "
                "(2) Game-theoretic payoff matrix projections. "
                "Zero hallucinated treaties permitted."
            )
        else:
            mode = TemporalMode.PROSPECTIVE_SCENARIO
            guidance = (
                f"Summit year {summit.year} is in the prospective future. "
                "All outputs must be branded as [PROSPECTIVE_GAME_THEORETIC_MODELING]."
            )
        return mode, guidance

    @classmethod
    def enforce_prospective_tagging(cls, text: str, mode: TemporalMode) -> str:
        """
        Ensures prospective projections are explicitly tagged so user interfaces
        do not present future simulations as historical facts.
        """
        if mode == TemporalMode.PROSPECTIVE_SCENARIO and not text.startswith("[PROSPECTIVE_MODEL]"):
            return f"[PROSPECTIVE_MODEL] {text}"
        return text
