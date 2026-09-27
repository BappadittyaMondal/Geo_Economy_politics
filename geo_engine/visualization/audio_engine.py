"""
Multilingual Audio Narration Engine (Phase 76).
Generates structured, natural-sounding audio briefing scripts in English, Hindi, and Bengali
for client-side browser speech synthesis (HTML5 Web Speech API) and offline audio rendering.
"""

from typing import Dict, List, Optional
from .adapter import UniversalReportPayload


class AudioNarrationEngine:
    """Generates synchronized multilingual narration scripts from UniversalReportPayload."""

    @classmethod
    def generate_multilingual_scripts(
        cls,
        payload: UniversalReportPayload
    ) -> Dict[str, str]:
        """
        Produces three concise, speech-optimized narration scripts:
        - 'en': English executive brief
        - 'hi': Devanagari Hindi executive brief
        - 'bn': Bengali executive brief
        """
        title = payload.metadata.title
        conf = payload.metadata.overall_confidence_pct
        verdict = payload.metadata.epistemic_classification

        kpi_summaries = []
        for k in payload.kpis[:3]:
            kpi_summaries.append(f"{k.label}: {k.value} {k.unit}".strip())
        kpis_str = ", ".join(kpi_summaries)

        # 1. English Script
        en_script = (
            f"Executive Intelligence Briefing for {title}. "
            f"Epistemic evaluation confirms overall confidence at {conf} percent. "
            f"Key metrics: {kpis_str}. "
            f"Final strategic verdict is classified as {verdict}. "
            f"Analysis deconstructs ceremonial rhetoric into verified physical and financial ground reality."
        )

        # 2. Hindi Script (Devanagari)
        hi_script = (
            f"{title} की आधिकारिक रणनीतिक समीक्षा। "
            f"प्रमाणिक मूल्यांकन में सत्यता का स्तर {conf} प्रतिशत निर्धारित किया गया है। "
            f"प्रमुख आंकड़े: {kpis_str}। "
            f"अंतिम निर्णय {verdict} के रूप में प्रमाणित है। "
            f"यह विश्लेषण कूटनीतिक दिखावे को हटाकर वास्तविक भौतिक और वित्तीय स्थिति को उजागर करता है।"
        )

        # 3. Bengali Script (বাংলা)
        bn_script = (
            f"{title} এর কার্যনির্বাহী গোয়েন্দা পর্যালোচনা। "
            f"বিশ্লেষণে সার্বিক নির্ভরযোগ্যতার মাত্রা {conf} শতাংশ নির্ধারিত হয়েছে। "
            f"প্রধান পরিমাপক: {kpis_str}। "
            f"চূড়ান্ত সিদ্ধান্ত {verdict} হিসাবে প্রত্যয়িত। "
            f"এই মূল্যায়ন আনুষ্ঠানিক প্রচারের আড়ালে থাকা প্রকৃত অর্থনৈতিক এবং ভূরাজনৈতিক সত্য প্রকাশ করে।"
        )

        return {
            "en": en_script,
            "hi": hi_script,
            "bn": bn_script
        }


__all__ = ["AudioNarrationEngine"]
