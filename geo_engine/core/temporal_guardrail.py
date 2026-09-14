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
