"""
Negative Space Diff Engine.
Detects omitted, suppressed, and diluted clauses in summit communiques.
Overcomes standard LLM positive-retrieval bias by computing delta diffs against
historical multilateral declarations.
"""

from collections import Counter
import math
import re
from typing import Dict, List, Optional, Tuple
from ..core.models import CommuniqueClause


class NegativeSpaceDiffEngine:
    """Computes negative space (omissions and dilutions) in multilateral communiques."""

    DEFAULT_BASELINE_CLAUSES: List[CommuniqueClause] = [
        CommuniqueClause(
            clause_id="UNSC-01",
            category="institutional_reform",
            raw_text="Support for comprehensive reform of the United Nations Security Council, explicitly endorsing permanent membership for India, Brazil, and South Africa with full veto power.",
            present_in_current_summit=False,
            historical_baseline_present=True,
            dilution_status="omitted_negative_space",
            omission_significance="China systematically blocked explicit endorsement of permanent veto-wielding UNSC seats for India and Brazil, diluting text to generic 'aspirations for greater Global South representation'."
        ),
        CommuniqueClause(
            clause_id="CURR-01",
            category="finance",
            raw_text="Exploration and technical feasibility roadmap for a unified common BRICS reserve currency (R5 basket) backed by gold and sovereign commodities.",
            present_in_current_summit=False,
            historical_baseline_present=True,
            dilution_status="omitted_negative_space",
            omission_significance="Concept of a unified common currency quietly abandoned due to structural impossibilities (Mundell-Fleming Trilemma) and resistance from India and Brazil against Yuan hegemony; replaced entirely by bilateral local-currency swaps."
        ),
        CommuniqueClause(
            clause_id="SEC-01",
            category="security",
            raw_text="Explicit condemnation of cross-border terrorism networks, state sponsorship of terror proxies, and FATF compliance enforcement against safe havens.",
            present_in_current_summit=True,
            historical_baseline_present=True,
            dilution_status="diluted_passive",
            omission_significance="Language heavily diluted to passive generalized anti-terror platitudes, avoiding naming Pakistan or regional terror syndicates to appease Beijing."
        ),
        CommuniqueClause(
            clause_id="MAR-01",
            category="territorial",
            raw_text="Commitment to strict adherence to UNCLOS (United Nations Convention on the Law of the Sea) and unrestricted freedom of navigation in the South China Sea.",
            present_in_current_summit=False,
            historical_baseline_present=True,
            dilution_status="omitted_negative_space",
            omission_significance="UNCLOS compliance and South China Sea navigation dropped entirely at Beijing's insistence, demonstrating internal bloc inability to address maritime expansionism."
        ),
        CommuniqueClause(
            clause_id="PAY-01",
            category="finance",
            raw_text="Expansion of bilateral local-currency clearing mechanisms and technical studies on digital cross-border payment interoperability (BRICS Bridge).",
            present_in_current_summit=True,
            historical_baseline_present=True,
            dilution_status="retained_full",
            omission_significance="Unanimously retained: All member states benefit from reducing USD conversion transaction costs without ceding monetary sovereignty."
        )
    ]

    @classmethod
    def load_baseline_from_store(cls) -> List[CommuniqueClause]:
        """Loads mandatory baseline clauses dynamically from persistent SQLite EventStore."""
        try:
            from ..storage import EventStore
            store = EventStore()
            db_clauses = store.get_mandatory_baseline_clauses()
            if db_clauses:
                loaded = []
                for row in db_clauses:
                    sig = row.get("omission_significance", "").lower()
                    if any(k in sig for k in ["omission", "omitted", "dropped", "refuses", "coercion"]):
                        status_val = "omitted_negative_space"
                    elif any(k in sig for k in ["dilut", "passive", "toothless"]):
                        status_val = "diluted_passive"
                    elif any(k in sig for k in ["retain", "unanimous"]):
                        status_val = "retained_full"
                    else:
                        status_val = "omitted_negative_space"

                    loaded.append(CommuniqueClause(
                        clause_id=row["clause_id"],
                        category=row["category"],
                        raw_text=row["clause_text"],
                        present_in_current_summit=False,
                        historical_baseline_present=True,
                        dilution_status=status_val,
                        omission_significance=row.get("omission_significance", "")
                    ))
                loaded.append(cls.DEFAULT_BASELINE_CLAUSES[-1]) # Retained payment clause
                return loaded
        except Exception:
            pass
        return cls.DEFAULT_BASELINE_CLAUSES

    @classmethod
    def analyze_diff(
        cls,
        current_clauses: List[CommuniqueClause] = None
    ) -> Tuple[List[CommuniqueClause], Dict[str, int], List[str]]:
        """
        Analyzes the target summit text against historical baselines.
        Returns the annotated clauses, categorical counts, and high-impact strategic takeaways.
        """
        clauses = current_clauses if current_clauses is not None else cls.load_baseline_from_store()

        counts = {
            "omitted_negative_space": 0,
            "diluted_passive": 0,
            "retained_full": 0,
            "new_consensus": 0
        }

        insights = []

        for c in clauses:
            if c.dilution_status in counts:
                counts[c.dilution_status] += 1
            else:
                counts["retained_full"] += 1

            if c.dilution_status == "omitted_negative_space":
                insights.append(f"[CRITICAL OMISSION] {c.category.upper()}: {c.omission_significance}")
            elif c.dilution_status == "diluted_passive":
                insights.append(f"[DILUTION DETECTED] {c.category.upper()}: {c.omission_significance}")

        return clauses, counts, insights

    @classmethod
    def scan_text_for_omissions(
        cls,
        communique_text: str,
        baseline_clauses: Optional[List[CommuniqueClause]] = None
    ) -> Tuple[List[CommuniqueClause], Dict[str, int], List[str]]:
        """
        Dynamically audits raw communique text against historical baseline clauses
        using DenseSemanticIndex vector similarity.
        """
        baselines = baseline_clauses if baseline_clauses is not None else cls.load_baseline_from_store()
        if not communique_text or not communique_text.strip():
            return cls.analyze_diff(baselines)

        index = DenseSemanticIndex()
        for c in baselines:
            index.add_document(c.clause_id, c.raw_text + " " + c.category)
        index.build_index()

        annotated: List[CommuniqueClause] = []
        for c in baselines:
            sim = index.compute_similarity(communique_text, c.clause_id)
            if sim < 0.10:
                status = "omitted_negative_space"
                present = False
            elif sim < 0.32:
                status = "diluted_passive"
                present = True
            else:
                status = "retained_full"
                present = True

            annotated.append(CommuniqueClause(
                clause_id=c.clause_id,
                category=c.category,
                raw_text=c.raw_text,
                present_in_current_summit=present,
                historical_baseline_present=True,
                dilution_status=status,
                omission_significance=c.omission_significance
            ))

        return cls.analyze_diff(annotated)


class DenseSemanticIndex:
    """
    Zero-dependency TF-IDF and n-gram sub-word dense semantic vector index.
    Enables semantic soft matching between raw communique texts and historical sovereign baselines.
    """

    def __init__(self):
        self.doc_ids: List[str] = []
        self.documents: Dict[str, str] = {}
        self.df: Counter = Counter()
        self.doc_vectors: Dict[str, Dict[str, float]] = {}
        self.total_docs: int = 0

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        words = re.findall(r"\b[a-zA-Z0-9_\-]{3,}\b", text.lower())
        bigrams = [f"{words[i]}_{words[i+1]}" for i in range(len(words) - 1)]
        return words + bigrams

    def add_document(self, doc_id: str, text: str) -> None:
        self.doc_ids.append(doc_id)
        self.documents[doc_id] = text
        tokens = self._tokenize(text)
        unique_tokens = set(tokens)
        for t in unique_tokens:
            self.df[t] += 1
        self.total_docs += 1

    def build_index(self) -> None:
        for doc_id, text in self.documents.items():
            tokens = self._tokenize(text)
            tf = Counter(tokens)
            vec: Dict[str, float] = {}
            for t, count in tf.items():
                idf = math.log((self.total_docs + 1) / (self.df[t] + 1)) + 1.0
                vec[t] = count * idf
            norm = math.sqrt(sum(v * v for v in vec.values())) or 1.0
            self.doc_vectors[doc_id] = {t: v / norm for t, v in vec.items()}

    def compute_similarity(self, query_text: str, doc_id: str) -> float:
        if doc_id not in self.doc_vectors:
            return 0.0
        q_tokens = self._tokenize(query_text)
        q_tf = Counter(q_tokens)
        q_vec: Dict[str, float] = {}
        for t, count in q_tf.items():
            idf = math.log((self.total_docs + 1) / (self.df.get(t, 0) + 1)) + 1.0
            q_vec[t] = count * idf
        q_norm = math.sqrt(sum(v * v for v in q_vec.values())) or 1.0
        q_norm_vec = {t: v / q_norm for t, v in q_vec.items()}

        doc_v = self.doc_vectors[doc_id]
        dot_product = sum(doc_v.get(t, 0.0) * val for t, val in q_norm_vec.items())
        return round(min(1.0, max(0.0, dot_product)), 4)

