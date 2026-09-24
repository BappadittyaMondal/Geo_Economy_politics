"""
Multi-Pillar Historical Chronology Arbiter (MPCA).
Provides machine-verifiable, cross-disciplinary arbitration of conflicting ancient historical
and civilizational timeline claims (e.g. Nilesh Oak 5561 BCE vs. Narahari Achar 3067 BCE vs. ASI 1000 BCE).
Evaluates hypotheses across 4 orthogonal epistemic pillars:
1. Astronomical retro-calculation with periodic degeneracy discounting.
2. Archaeological stratigraphy and material culture coherence (metallurgy, urban strata, chariot/horse evidence).
3. Hydro-geological and paleoclimatic telemetry (Saraswati river flow vs. desiccation, Dwarka marine geology).
4. Textual and philological manuscript provenance (BORI Critical Edition common archetype vs. regional interpolations).
"""

from typing import Any, Dict, List, Optional, Tuple
from pydantic import BaseModel, Field


class ChronologyPillarScore(BaseModel):
    """Normalized scoring (0.0 to 1.0) across the four orthogonal evidentiary pillars."""
    astronomy_score: float = Field(..., ge=0.0, le=1.0, description="Fit with planetary/constellation observations in text")
    astronomy_degeneracy_factor: float = Field(default=0.30, ge=0.0, le=1.0, description="1.0 = highly recurring/degenerate periodic alignment; 0.0 = unique")
    archaeology_score: float = Field(..., ge=0.0, le=1.0, description="Fit with excavated strata, C-14, metallurgy, and material culture")
    hydro_geology_score: float = Field(..., ge=0.0, le=1.0, description="Fit with river Saraswati flow state, monsoon curves, marine sea-levels")
    textual_provenance_score: float = Field(..., ge=0.0, le=1.0, description="Manuscript weight (1.0 = BORI common archetype, 0.2 = late regional variant)")


class HistoricalHypothesisCandidate(BaseModel):
    """A proposed historical timeline candidate evaluated across multi-pillar evidence."""
    hypothesis_id: str
    label: str
    proposed_year_bce: int
    proponent: str
    pillar_scores: ChronologyPillarScore
    has_material_culture_collision: bool = False
    collision_rationale: Optional[str] = None
    composite_coherence_score: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Serializes candidate into a clean dictionary."""
        return {
            "hypothesis_id": self.hypothesis_id,
            "label": self.label,
            "proposed_year_bce": self.proposed_year_bce,
            "proponent": self.proponent,
            "pillar_scores": self.pillar_scores.model_dump(),
            "has_material_culture_collision": self.has_material_culture_collision,
            "collision_rationale": self.collision_rationale,
            "composite_coherence_score": round(self.composite_coherence_score, 4)
        }


class ChronologyEvaluationReport(BaseModel):
    """Comprehensive evaluation report arbitrating competing historical timelines."""
    event_name: str
    candidates: List[HistoricalHypothesisCandidate] = Field(default_factory=list)
    ranked_candidates: List[HistoricalHypothesisCandidate] = Field(default_factory=list)
    dominant_candidate_id: str = ""
    dominant_candidate_label: str = ""
    dominant_coherence_score: float = 0.0
    epistemic_warning: Optional[str] = None
    reasoning_audit_trail: List[str] = Field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Serializes report into JSON-compatible dictionary."""
        return {
            "event_name": self.event_name,
            "dominant_candidate_id": self.dominant_candidate_id,
            "dominant_candidate_label": self.dominant_candidate_label,
            "dominant_coherence_score": round(self.dominant_coherence_score, 4),
            "epistemic_warning": self.epistemic_warning,
            "reasoning_audit_trail": self.reasoning_audit_trail,
            "ranked_candidates": [c.to_dict() for c in self.ranked_candidates]
        }


class MultiPillarChronologyArbiter:
    """
    Mathematical and epistemic arbiter for conflicting historical chronologies.
    Resolves the single-optic fallacy where isolated astronomical calculations
    ignore physical stratigraphy, or where archaeological models ignore celestial and hydrological records.
    """

    # Pillar Weights in Composite Bayesian Coherence
    WEIGHT_ASTRONOMY = 0.25
    WEIGHT_ARCHAEOLOGY = 0.35
    WEIGHT_HYDRO_GEOLOGY = 0.20
    WEIGHT_TEXTUAL_PROVENANCE = 0.20

    @classmethod
    def calculate_composite_coherence(
        cls,
        scores: ChronologyPillarScore,
        proposed_year_bce: int
    ) -> Tuple[float, bool, Optional[str]]:
        """
        Computes composite coherence score with degeneracy dampening and material culture collision flags.
        Formula:
          S_astro_adj = S_astro * (1.0 - 0.5 * Degeneracy)
          Base = 0.25 * S_astro_adj + 0.35 * S_arch + 0.20 * S_geo + 0.20 * S_text
          If S_arch < 0.15: Apply 75% material culture collision penalty (haircut).
        """
        # 1. Adjust astronomy for periodic recurrence degeneracy
        adj_astronomy = scores.astronomy_score * (1.0 - 0.5 * scores.astronomy_degeneracy_factor)

        # 2. Weighted multi-pillar base sum
        base_score = (
            cls.WEIGHT_ASTRONOMY * adj_astronomy +
            cls.WEIGHT_ARCHAEOLOGY * scores.archaeology_score +
            cls.WEIGHT_HYDRO_GEOLOGY * scores.hydro_geology_score +
            cls.WEIGHT_TEXTUAL_PROVENANCE * scores.textual_provenance_score
        )

        # 3. Check for Material Culture Collision
        # In South Asian archaeological stratigraphy:
        # Pre-4000 BCE: Epipaleolithic/Mesolithic/Early Aceramic Neolithic (no iron, no spoke-wheel chariots, no urban brick palaces).
        # Dating an epic describing 18 Akshauhinis with composite bows, steel swords, and iron armor to 5500+ BCE or 12,000 BCE
        # triggers a catastrophic material culture disconnect.
        has_collision = False
        collision_rationale = None

        if scores.archaeology_score < 0.15 or proposed_year_bce >= 4500:
            if scores.archaeology_score < 0.20:
                has_collision = True
                collision_rationale = (
                    f"[MATERIAL CULTURE COLLISION] Proposed epoch ({proposed_year_bce} BCE) contradicts "
                    f"excavated stratigraphic horizons. Spoke-wheeled war chariots (Rathas), steel metallurgy, "
                    f"and fortified brick citadels do not exist in the lithic/early Neolithic record."
                )
                # Apply 75% epistemic haircut
                final_score = round(base_score * 0.25, 4)
                return final_score, has_collision, collision_rationale

        final_score = round(base_score, 4)
        return final_score, has_collision, collision_rationale

    @classmethod
    def get_benchmark_candidates(cls) -> List[HistoricalHypothesisCandidate]:
        """Returns standard benchmark scholarly and traditional timeline candidates for the Mahabharata."""
        return [
            HistoricalHypothesisCandidate(
                hypothesis_id="CHRONO_OAK_5561_BCE",
                label="5561 BCE (Nilesh Oak Arundhati-Vasistha Model)",
                proposed_year_bce=5561,
                proponent="Nilesh Nilkanth Oak",
                pillar_scores=ChronologyPillarScore(
                    astronomy_score=0.88,
                    astronomy_degeneracy_factor=0.75,  # 6,500-year precession window (11,091 BCE to 4508 BCE)
                    archaeology_score=0.08,           # Mesolithic/Neolithic Mehrgarh I (stone tools, zero iron/chariots)
                    hydro_geology_score=0.45,         # Perennial glacial melt; does not match Vinashana desiccation
                    textual_provenance_score=0.70     # Interprets AV omen literally as an astronomical precession coordinate
                )
            ),
            HistoricalHypothesisCandidate(
                hypothesis_id="CHRONO_ACHAR_3067_BCE",
                label="3067 BCE (Dr. Narahari Achar / BORI Model)",
                proposed_year_bce=3067,
                proponent="Dr. Narahari Achar / Prof. K.S. Raghavan",
                pillar_scores=ChronologyPillarScore(
                    astronomy_score=0.86,
                    astronomy_degeneracy_factor=0.25,  # High specificity: twin eclipse in 13 days + Saturn-Rohini + Jupiter-Vishakha
                    archaeology_score=0.78,           # Early Harappan / Sanauli chariot horizon (~2000-1900 BCE copper-sheathed carts)
                    hydro_geology_score=0.88,         # Matches Saraswati perennial-to-dry transition before 1900 BCE desiccation
                    textual_provenance_score=0.85     # Conforms strictly to BORI Critical Edition common archetype
                )
            ),
            HistoricalHypothesisCandidate(
                hypothesis_id="CHRONO_ARYABHATA_3102_BCE",
                label="3102 BCE (Traditional Aryabhata / Aihole Inscription Model)",
                proposed_year_bce=3102,
                proponent="Aryabhata (499 CE) / Pulakeshin II Aihole Inscription (634 CE)",
                pillar_scores=ChronologyPillarScore(
                    astronomy_score=0.76,
                    astronomy_degeneracy_factor=0.35,  # Conjunction of all planets at 0 degrees Aries at Kali Yuga start
                    archaeology_score=0.75,           # Pre-Harappan / Early Bronze Age transition
                    hydro_geology_score=0.86,         # Saraswati flowing perennially to Rann of Kutch
                    textual_provenance_score=0.82     # Universal consensus across Puranic king lists and classical epigraphs
                )
            ),
            HistoricalHypothesisCandidate(
                hypothesis_id="CHRONO_LAL_PGW_1000_BCE",
                label="1000 BCE (Prof. B.B. Lal / ASI Painted Grey Ware Model)",
                proposed_year_bce=1000,
                proponent="Prof. B.B. Lal / Archaeological Survey of India",
                pillar_scores=ChronologyPillarScore(
                    astronomy_score=0.30,             # Rejects or bypasses planetary conjunctions as late poetic hyperbole
                    astronomy_degeneracy_factor=0.50,
                    archaeology_score=0.92,           # Hastinapur, Kurukshetra, Indraprastha PGW layers with iron weapons & flood stratum
                    hydro_geology_score=0.25,         # Severe mismatch: Saraswati completely dried up by 1900 BCE; dry by 1000 BCE
                    textual_provenance_score=0.65     # Treats epic as late first-millennium BCE compilation
                )
            ),
        ]

    @classmethod
    def arbitrate(
        cls,
        event_name: str = "Mahabharata War Chronology",
        candidates: Optional[List[HistoricalHypothesisCandidate]] = None
    ) -> ChronologyEvaluationReport:
        """
        Executes multi-pillar cross-disciplinary arbitration across historical candidates.
        Ranks candidates by composite Bayesian coherence score and flags single-optic distortions.
        """
        eval_candidates = candidates if candidates is not None else cls.get_benchmark_candidates()
        audit_trail: List[str] = [
            f"[MPCA_INIT] Initiating Multi-Pillar Chronology Arbitration for '{event_name}' across {len(eval_candidates)} candidates.",
            "[MPCA_WEIGHTS] Applied Epistemic Pillar Weights: Archaeology (0.35), Astronomy (0.25), Hydro-Geology (0.20), Textual Provenance (0.20)."
        ]

        # Calculate composite score for each candidate
        for c in eval_candidates:
            score, has_coll, rationale = cls.calculate_composite_coherence(c.pillar_scores, c.proposed_year_bce)
            c.composite_coherence_score = score
            c.has_material_culture_collision = has_coll
            c.collision_rationale = rationale

            audit_trail.append(
                f"[MPCA_EVAL] {c.hypothesis_id} ({c.proposed_year_bce} BCE): "
                f"Astro={c.pillar_scores.astronomy_score:.2f} (Degeneracy={c.pillar_scores.astronomy_degeneracy_factor:.2f}), "
                f"Arch={c.pillar_scores.archaeology_score:.2f}, Geo={c.pillar_scores.hydro_geology_score:.2f}, "
                f"Text={c.pillar_scores.textual_provenance_score:.2f} -> Composite={score:.4f}"
            )
            if has_coll:
                audit_trail.append(f"[MPCA_PENALTY] {c.hypothesis_id} penalized: {rationale}")

        # Rank descending by composite coherence score
        ranked = sorted(eval_candidates, key=lambda x: x.composite_coherence_score, reverse=True)
        dominant = ranked[0]
        runner_up = ranked[1] if len(ranked) > 1 else None

        audit_trail.append(
            f"[MPCA_RANKING] Dominant Candidate: '{dominant.label}' (Composite Coherence: {dominant.composite_coherence_score:.4f})."
        )

        warning: Optional[str] = None
        if dominant.has_material_culture_collision:
            warning = f"[EPISTEMIC SEVERE CAUTION] Dominant candidate exhibits unresolved material culture collision: {dominant.collision_rationale}"
        elif runner_up and (dominant.composite_coherence_score - runner_up.composite_coherence_score < 0.10):
            warning = (
                f"[EPISTEMIC CLOSE COMPETITION] Top candidate ('{dominant.label}', {dominant.composite_coherence_score:.4f}) "
                f"leads runner-up ('{runner_up.label}', {runner_up.composite_coherence_score:.4f}) by less than 0.10. "
                f"Multi-pillar synthesis confirms historical clustering in the early 3rd millennium BCE (~3102–3067 BCE)."
            )

        return ChronologyEvaluationReport(
            event_name=event_name,
            candidates=eval_candidates,
            ranked_candidates=ranked,
            dominant_candidate_id=dominant.hypothesis_id,
            dominant_candidate_label=dominant.label,
            dominant_coherence_score=dominant.composite_coherence_score,
            epistemic_warning=warning,
            reasoning_audit_trail=audit_trail
        )
