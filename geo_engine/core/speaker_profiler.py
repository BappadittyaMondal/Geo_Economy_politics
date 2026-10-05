"""
Epistemic Speaker Archetype Registry & Profiling Engine.
Maps prominent political, civilizational, economic, and strategic thinkers
to structured cognitive persona profiles that track baseline priors,
epistemic strengths, characteristic blind spots, and discourse vectors.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional
import re


class SpeakerArchetype(str, Enum):
    """Canonical intellectual and statecraft archetypes."""
    TRADITIONALIST_MERITOCRACY = "TRADITIONALIST_MERITOCRACY"
    INDIC_DECOLONIAL_JURISPRUDENCE = "INDIC_DECOLONIAL_JURISPRUDENCE"
    DEEP_TECH_NATIONALISM = "DEEP_TECH_NATIONALISM"
    SUBALTERN_CONSTITUTIONALISM = "SUBALTERN_CONSTITUTIONALISM"
    BUREAUCRATIC_INSTITUTIONALISM = "BUREAUCRATIC_INSTITUTIONALISM"
    PRAGMATIC_SOVEREIGN_STATECRAFT = "PRAGMATIC_SOVEREIGN_STATECRAFT"
    SCIENTIFIC_EMPIRICISM = "SCIENTIFIC_EMPIRICISM"
    GEOECONOMIC_TIMELINE_MAPPING = "GEOECONOMIC_TIMELINE_MAPPING"
    INDIC_CULTURAL_RHETORIC = "INDIC_CULTURAL_RHETORIC"
    VEDIC_SCIENTIFIC_NATIONALISM = "VEDIC_SCIENTIFIC_NATIONALISM"
    INDEPENDENT_ANALYST = "INDEPENDENT_ANALYST"


@dataclass(frozen=True)
class SpeakerProfile:
    """Immutable cognitive and epistemic profile for a strategic commentator or leader."""
    name: str
    canonical_id: str
    archetype: SpeakerArchetype
    core_frameworks: List[str] = field(default_factory=list)
    characteristic_strengths: List[str] = field(default_factory=list)
    primary_blind_spots: List[str] = field(default_factory=list)
    frequent_thematic_tokens: List[str] = field(default_factory=list)
    baseline_reliability_weight: float = 0.85

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "canonical_id": self.canonical_id,
            "archetype": self.archetype.value,
            "core_frameworks": list(self.core_frameworks),
            "characteristic_strengths": list(self.characteristic_strengths),
            "primary_blind_spots": list(self.primary_blind_spots),
            "frequent_thematic_tokens": list(self.frequent_thematic_tokens),
            "baseline_reliability_weight": self.baseline_reliability_weight,
        }


class EpistemicSpeakerProfiler:
    """Registry and resolver for speaker epistemic profiles."""

    _REGISTRY: Dict[str, SpeakerProfile] = {}

    @classmethod
    def register_profile(cls, profile: SpeakerProfile) -> None:
        """Registers or updates a speaker profile in the registry."""
        cls._REGISTRY[profile.canonical_id.lower()] = profile
        cls._REGISTRY[profile.name.lower()] = profile

    @classmethod
    def get_profile(cls, name_or_id: str) -> Optional[SpeakerProfile]:
        """Looks up a speaker profile by name or canonical ID."""
        if not name_or_id:
            return None
        key = name_or_id.strip().lower()
        if key in cls._REGISTRY:
            return cls._REGISTRY[key]
        for p in cls._REGISTRY.values():
            if key in p.name.lower() or p.name.lower() in key:
                return p
        return None

    @classmethod
    def resolve_from_text(cls, text: str) -> List[SpeakerProfile]:
        """Scans arbitrary text for mentions of registered speaker profiles."""
        if not text:
            return []
        text_lower = text.lower()
        matched: List[SpeakerProfile] = []
        seen = set()

        for p in cls._REGISTRY.values():
            if p.canonical_id in seen:
                continue
            # Regex word boundary check for name
            escaped_name = re.escape(p.name.lower())
            if re.search(r"(?<!\w)" + escaped_name + r"(?!\w)", text_lower):
                matched.append(p)
                seen.add(p.canonical_id)
                continue
            # Check frequent thematic tokens if 2 or more appear together
            token_matches = [t for t in p.frequent_thematic_tokens if re.search(r"(?<!\w)" + re.escape(t.lower()) + r"(?!\w)", text_lower)]
            if len(token_matches) >= 2:
                matched.append(p)
                seen.add(p.canonical_id)

        return matched

    @classmethod
    def list_profiles(cls) -> List[SpeakerProfile]:
        """Returns all uniquely registered speaker profiles."""
        unique = {}
        for p in cls._REGISTRY.values():
            unique[p.canonical_id] = p
        return list(unique.values())


# ---------------------------------------------------------------------------
# Canonical Pre-Seeded Speaker Profiles (The 7-Master Council & Key Thinkers)
# ---------------------------------------------------------------------------

_CANONICAL_PROFILES = [
    SpeakerProfile(
        name="Neeraj Atri",
        canonical_id="PROF-NEERAJ-ATRI",
        archetype=SpeakerArchetype.TRADITIONALIST_MERITOCRACY,
        core_frameworks=[
            "Traditionalist Savarna meritocracy",
            "NCERT textbook & historical distortion critique",
            "Anti-welfarism & middle-class direct tax burden",
            "SC/ST Act due process & Section 18A critique",
        ],
        characteristic_strengths=[
            "High forensic rigor on educational syllabus distortions",
            "Sharp identification of statutory asymmetries and presumption of guilt",
            "Direct exposure of middle-class fiscal exploitation without social safety nets",
            "Unflinching critique of ruling establishment's failure to build independent intellectual ecosystems",
        ],
        primary_blind_spots=[
            "Underestimates macro-geopolitical necessity of social welfarism as a stability floor",
            "Downplays historical subaltern socio-economic exclusion and need for integration",
            "Conflates pragmatic electoral de-escalation with civilizational cowardice",
        ],
        frequent_thematic_tokens=["neeraj atri", "blunder called modi", "sc st act", "section 18a", "kashinath mahajan", "jizya", "middle class tax"],
        baseline_reliability_weight=0.88,
    ),
    SpeakerProfile(
        name="J. Sai Deepak",
        canonical_id="PROF-J-SAI-DEEPAK",
        archetype=SpeakerArchetype.INDIC_DECOLONIAL_JURISPRUDENCE,
        core_frameworks=[
            "Indic decoloniality & civilizational constitutionalism",
            "Temple autonomy & HRCE statutory dismantling",
            "Statutory double-standards (Places of Worship Act, Waqf Act Section 40)",
            "Epistemic decolonization of Indian jurisprudence",
        ],
        characteristic_strengths=[
            "Exhaustive legal and constitutional analysis of colonial continuities",
            "Deep textual and historical grounding in Indic jurisprudence and Sanatan traditions",
            "Rigorous courtroom advocacy for institutional autonomy of Hindu institutions",
        ],
        primary_blind_spots=[
            "Over-reliance on legal and constitutional remedies for deep socioeconomic fractures",
            "Less emphasis on industrial manufacturing, defense technology, and kinetic deterrence",
        ],
        frequent_thematic_tokens=["j. sai deepak", "sai deepak", "india that is bharat", "india bharat and pakistan", "temple autonomy", "places of worship act", "waqf act"],
        baseline_reliability_weight=0.92,
    ),
    SpeakerProfile(
        name="Srijan Pal Singh",
        canonical_id="PROF-SRIJAN-PAL-SINGH",
        archetype=SpeakerArchetype.DEEP_TECH_NATIONALISM,
        core_frameworks=[
            "Dr. A.P.J. Abdul Kalam techno-nationalist vision",
            "Indigenous defense R&D CapEx & semiconductor roadmaps",
            "Youth demographic dividend mobilization",
            "Aerospace, avionics & high-tech supply chain sovereignty",
        ],
        characteristic_strengths=[
            "Data-driven focus on science, technology, engineering, and mathematics (STEM)",
            "Clear articulation of deep-tech industrial autonomy and defense manufacturing",
            "Optimistic, forward-looking youth and educational mobilization frameworks",
        ],
        primary_blind_spots=[
            "Technocratic optimism that may underestimate entrenched bureaucratic inertia",
            "Less emphasis on domestic socio-legal fault lines and ideological warfare",
        ],
        frequent_thematic_tokens=["srijan pal singh", "srijan", "kalam", "semi-conductor", "defense r&d", "deep tech", "demographic dividend"],
        baseline_reliability_weight=0.90,
    ),
    SpeakerProfile(
        name="B.R. Ambedkar",
        canonical_id="PROF-BR-AMBEDKAR",
        archetype=SpeakerArchetype.SUBALTERN_CONSTITUTIONALISM,
        core_frameworks=[
            "Annihilation of caste & subaltern emancipation",
            "Constitutional democracy as a moral framework",
            "Critique of communist totalitarianism and uncritical political Bhakti",
            "Economic self-reliance and monetary reform (Problem of the Rupee)",
        ],
        characteristic_strengths=[
            "Uncompromising defense of individual dignity and institutional equality",
            "Prescient warning against hero-worship in politics eroding constitutional democracy",
            "Rigorous economic understanding of currency, taxation, and labor rights",
            "Explicit rejection of violent Marxism and communal factionalism",
        ],
        primary_blind_spots=[
            "Modern political misappropriation that reduces his comprehensive philosophy to perpetual reservation politics",
        ],
        frequent_thematic_tokens=["b.r. ambedkar", "ambedkar", "babasaheb", "annihilation of caste", "rajya sabha 1953", "hero worship", "constitutional morality"],
        baseline_reliability_weight=0.96,
    ),
    SpeakerProfile(
        name="Hamid Ansari",
        canonical_id="PROF-HAMID-ANSARI",
        archetype=SpeakerArchetype.BUREAUCRATIC_INSTITUTIONALISM,
        core_frameworks=[
            "Nehruvian diplomatic institutionalism",
            "West Asian diplomatic equilibrium & Non-Alignment (NAM)",
            "Minority protection within constitutional secularism",
            "Protocol-driven multilateral engagement",
        ],
        characteristic_strengths=[
            "Decades of institutional diplomatic experience across West Asia and the UN",
            "Strict adherence to diplomatic protocol and institutional proceduralism",
        ],
        primary_blind_spots=[
            "Severe vulnerability to covert intelligence asset compromises (e.g. 1992 Tehran RAW network)",
            "Reluctance to deploy hard sovereign power or asymmetric kinetic deterrence",
            "Detachment from indigenous civilizational consciousness",
        ],
        frequent_thematic_tokens=["hamid ansari", "ansari", "tehran embassy", "nehruvian diplomacy", "institutional secularism"],
        baseline_reliability_weight=0.78,
    ),
    SpeakerProfile(
        name="Narendra Modi",
        canonical_id="PROF-NARENDRA-MODI",
        archetype=SpeakerArchetype.PRAGMATIC_SOVEREIGN_STATECRAFT,
        core_frameworks=[
            "Saturation DBT welfarism & subaltern electoral consolidation",
            "Civilizational revivalism (Kashi, Ayodhya, Ujjain, Sengol)",
            "Mass physical infrastructure CapEx (highways, ports, railway freight, DPI)",
            "Pragmatic strategic autonomy & kinetic deterrence (Balakot, Article 370)",
        ],
        characteristic_strengths=[
            "Unmatched electoral mobilization and subaltern demographic consolidation",
            "Decisive execution of long-pending constitutional changes (Article 370, CAA)",
            "Building high-velocity digital public infrastructure and macroeconomic social safety floor",
            "Assertive non-aligned foreign policy resisting Western moral pressure",
        ],
        primary_blind_spots=[
            "Prone to high-decibel PR theatrics that outpace structural ground reforms",
            "Persistent fiscal squeeze on salaried middle-class taxpayers",
            "Vulnerability to street vetoes causing sudden strategic policy retreats (Farm Laws)",
            "Neglect of independent intellectual and academic ecosystem building",
        ],
        frequent_thematic_tokens=["narendra modi", "modi", "vishwa bandhu", "viksit bharat", "dbt", "swachh bharat", "temple of democracy"],
        baseline_reliability_weight=0.92,
    ),
    SpeakerProfile(
        name="Ajit Doval",
        canonical_id="PROF-AJIT-DOVAL",
        archetype=SpeakerArchetype.PRAGMATIC_SOVEREIGN_STATECRAFT,
        core_frameworks=[
            "Defensive-offense doctrine & cross-domain deterrence",
            "Nexus between internal security subversion and external sovereignty",
            "Cyber-kinetic and intelligence synergy",
            "Border infrastructure hardening & non-kinetic retaliation",
        ],
        characteristic_strengths=[
            "Operational mastery of counter-terrorism and covert intelligence operations",
            "Clear strategic doctrine linking domestic stability to external deterrence",
            "Rapid tactical crisis management across volatile borders (Doklam, Galwan)",
        ],
        primary_blind_spots=[
            "High concentration of strategic decision-making within small executive cabals",
            "Less focus on macroeconomic fiscal policies and global trade architecture",
        ],
        frequent_thematic_tokens=["ajit doval", "doval", "defensive offense", "doval doctrine", "internal external security", "kinetic deterrence"],
        baseline_reliability_weight=0.94,
    ),
    SpeakerProfile(
        name="S. Jaishankar",
        canonical_id="PROF-S-JAISHANKAR",
        archetype=SpeakerArchetype.PRAGMATIC_SOVEREIGN_STATECRAFT,
        core_frameworks=[
            "The India Way & strategic multi-alignment",
            "Mahabharata ethical statecraft (Artha and Dharma equilibrium)",
            "Weaponized interdependence & critical supply chain hedging",
            "Rejection of Western moral lecturing & diplomatic realism",
        ],
        characteristic_strengths=[
            "Razor-sharp articulation of Indian strategic interests on global stages",
            "Skillful maneuvering between Quad, BRICS, and Russian hydrocarbon supplies",
            "Deep comprehension of China's revisionist strategy along the Himalayan frontier",
        ],
        primary_blind_spots=[
            "Diplomatic success occasionally masks deep underlying domestic manufacturing bottlenecks",
            "Vulnerability of overseas Indian diaspora communities to host-nation lawfare and nativism",
        ],
        frequent_thematic_tokens=["s. jaishankar", "jaishankar", "india way", "strategic autonomy", "multi-alignment", "mahabharata statecraft"],
        baseline_reliability_weight=0.95,
    ),
    SpeakerProfile(
        name="Sanjeev Sanyal",
        canonical_id="PROF-SANJEEV-SANYAL",
        archetype=SpeakerArchetype.PRAGMATIC_SOVEREIGN_STATECRAFT,
        core_frameworks=[
            "Complex Adaptive Systems (CAS) & agile policy formulation",
            "Indian Ocean maritime trade history & naval civilizational heritage",
            "Supply-side economic CapEx over demand-side populist stimulus",
            "Judicial, administrative, and legal system deregulation",
        ],
        characteristic_strengths=[
            "Sophisticated application of complexity theory and feedback loops to macroeconomics",
            "Rigorous debunking of colonial and Eurocentric maritime historical narratives",
            "Data-driven focus on logistics friction, court delays, and process simplification",
        ],
        primary_blind_spots=[
            "May underestimate political survival imperatives that compel governments to prioritize populist welfarism",
        ],
        frequent_thematic_tokens=["sanjeev sanyal", "sanyal", "complex adaptive systems", "ocean of churn", "maritime history", "supply side"],
        baseline_reliability_weight=0.93,
    ),
    SpeakerProfile(
        name="Anand Ranganathan",
        canonical_id="PROF-ANAND-RANGANATHAN",
        archetype=SpeakerArchetype.SCIENTIFIC_EMPIRICISM,
        core_frameworks=[
            "Scientific empiricism & evidentiary rigor",
            "Absolute free speech defense & anti-censorship advocacy",
            "Relentless exposure of statutory double-standards and appeasement",
            "Separation of state and religious institutions",
        ],
        characteristic_strengths=[
            "Methodical, data-backed confrontation of political and religious hypocrisy across all parties",
            "Fearless defense of freedom of expression against statutory blasphemy and speech codes",
            "Clear empirical exposure of state-enforced religious asymmetries",
        ],
        primary_blind_spots=[
            "Purity of principle occasionally conflicts with messy realpolitik compromises needed to govern a 1.4B diverse society",
        ],
        frequent_thematic_tokens=["anand ranganathan", "ranganathan", "hindus in hindu rashtra", "free speech", "statutory double standards", "scientific empiricism"],
        baseline_reliability_weight=0.91,
    ),
    SpeakerProfile(
        name="Ankit Shah",
        canonical_id="PROF-ANKIT-SHAH",
        archetype=SpeakerArchetype.GEOECONOMIC_TIMELINE_MAPPING,
        core_frameworks=[
            "Global geoeconomic timeline mapping & dedollarization cycles",
            "Western sovereign debt saturation & US Treasury weaponization",
            "Bilateral currency settlement & commodity-backed reserves",
            "Geopolitical inflection points (2019-2029-2039 financial warfare)",
        ],
        characteristic_strengths=[
            "Macro-level integration of financial flows, sovereign debt traps, and currency warfare",
            "Longitudinal perspective connecting historical monetary agreements to current supply chain ruptures",
        ],
        primary_blind_spots=[
            "Timeline projections can be overly deterministic regarding exact dates of global financial collapses",
        ],
        frequent_thematic_tokens=["ankit shah", "dedollarization", "currency war", "brics currency", "sovereign debt", "geoeconomic timeline"],
        baseline_reliability_weight=0.87,
    ),
    SpeakerProfile(
        name="Kumar Vishwas",
        canonical_id="PROF-KUMAR-VISHWAS",
        archetype=SpeakerArchetype.INDIC_CULTURAL_RHETORIC,
        core_frameworks=[
            "Apne Apne Ram civilizational synthesis",
            "Poetic cultural mobilization & mass Hindi-Awadhi resonance",
            "Ramcharitmanas ethical statecraft (Ramrajya ideal)",
            "Subaltern cultural bridging & anti-hypocrisy political satire",
        ],
        characteristic_strengths=[
            "Unrivaled oratorical, literary, and poetic mass engagement across demographics",
            "De-hyphenating classical Indic traditions from sectarian dogma into accessible cultural pride",
            "Deep textual mastery of Tulsidas, Valmiki, Nirala, Dinkar, and Bharti",
            "Effective use of humor and satire to dismantle moral sanctimony in contemporary politics",
        ],
        primary_blind_spots=[
            "Literary and poetic romanticism that can understate hard macroeconomic fiscal constraints",
            "Less emphasis on kinetic military technicalities, global supply chains, and industrial manufacturing",
        ],
        frequent_thematic_tokens=[
            "kumar vishwas", "dr kumar vishwas", "apne apne ram", "ramcharitmanas",
            "kavi sammelan", "tulsidas", "koi deewana kehta hai", "ram katha",
        ],
        baseline_reliability_weight=0.89,
    ),
    SpeakerProfile(
        name="Sudhanshu Trivedi",
        canonical_id="PROF-SUDHANSHU-TRIVEDI",
        archetype=SpeakerArchetype.VEDIC_SCIENTIFIC_NATIONALISM,
        core_frameworks=[
            "Vedic scientific-astronomical correlation & historical chronology",
            "Parliamentary dialectics & forensic political debate",
            "Rebuttal of Marxist, Eurocentric, and colonial historiography",
            "Civilizational constitutionalism & Sanatan philosophical defense",
        ],
        characteristic_strengths=[
            "Encyclopedic recall of Sanskrit scriptures, Vedic astronomy, and Indian political history",
            "Mechanical engineering analytical background applied to scriptural and scientific validation",
            "Razor-sharp parliamentary and televised debate forensic rebuttal",
            "Articulate deconstruction of linguistic and historical distortions in national discourse",
        ],
        primary_blind_spots=[
            "Party-line organizational defense that can lead to defensiveness on government economic lapses",
            "Tendency to deflect administrative friction into broad historical and civilizational polemics",
        ],
        frequent_thematic_tokens=[
            "sudhanshu trivedi", "dr sudhanshu trivedi", "vedic science", "rajya sabha",
            "sanatan parampara", "bjp spokesperson", "kalpa", "yuga chronology", "shastra",
        ],
        baseline_reliability_weight=0.91,
    ),
    SpeakerProfile(
        name="Pushpendra Kulshrestha",
        canonical_id="PROF-PUSHPENDRA-KULSHRESTHA",
        archetype=SpeakerArchetype.INDIC_CULTURAL_RHETORIC,
        core_frameworks=[
            "Civilizational nationalism & Hindutva historical reinterpretation",
            "Counter-narrative journalism against alleged media bias & colonial liberal historiography",
            "Grassroots Hindu awakening & Sanatan cultural mobilization",
            "Deconstruction of political-media nexus & dominant narrative fraud",
        ],
        characteristic_strengths=[
            "Mass grassroots reach on digital platforms (Instagram, Facebook, YouTube) with high emotional resonance",
            "High-energy populist framing making complex civilizational history accessible to non-academic audiences",
            "Persistent counter-programmatic journalism targeting dominant media narratives",
            "Rapid mobilization of civilizational pride as a unifying emotional force",
        ],
        primary_blind_spots=[
            "High ideological intensity may reduce factual granularity and nuance in contested historical claims",
            "Populist emotional packaging can amplify partially verified or single-source claims",
            "Limited engagement with cross-ideological empirical counter-evidence or comparative historical data",
        ],
        frequent_thematic_tokens=[
            "pushpendra kulshrestha", "pushpendra", "kulshrestha",
            "sanatan dharma", "hindutva", "media bias", "hindu jagriti",
            "sansad tv", "cultural nationalism", "bharat mata",
        ],
        baseline_reliability_weight=0.82,
    ),
]

for _prof in _CANONICAL_PROFILES:
    EpistemicSpeakerProfiler.register_profile(_prof)
