"""
Dynamic Query Parser and Strategic Intent Extractor.
Parses arbitrary natural language queries into structured analytical instructions,
extracting entities (countries, leaders, summits), temporal horizons, and prioritized lens foci.
"""

import re
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field



class StrategicQuery(BaseModel):
    """Structured analytical specification derived from an arbitrary user prompt."""
    raw_prompt: str
    target_summit: str = Field(default="Multilateral Summit")
    target_event: str = Field(default="Strategic Event")
    event_type: str = Field(default="SUMMIT")
    focal_date: Optional[str] = None
    year: int = Field(default=2026)
    target_countries: List[str] = Field(default_factory=list)
    target_leaders: List[str] = Field(default_factory=list)
    prioritized_lenses: List[str] = Field(default_factory=list)
    requires_kinesics: bool = False
    requires_cash_audit: bool = False
    requires_negative_space: bool = False
    requires_civilizational_depth: bool = False
    requires_india_timeline: bool = False
    requires_demographic_audit: bool = False
    requires_minerals_audit: bool = False
    requires_lawfare_audit: bool = False
    requires_chronology_arbitration: bool = False
    requires_abyssal_sovereignty: bool = False
    requires_trophic_biosecurity: bool = False
    requires_cognitive_sovereignty: bool = False
    requires_bullion_audit: bool = False
    requires_insurgency_audit: bool = False
    requires_quantum_statecraft: bool = False
    requires_grayzone_micro_signal: bool = False
    requires_pnt_autonomy: bool = False
    requires_ai_governance: bool = False
    requires_proxy_warfare: bool = False
    requires_textual_triangulation: bool = False
    requires_media_capture: bool = False
    requires_hydro_weaponization: bool = False
    requires_antiquity_restitution: bool = False
    requires_diaspora_sanctuary: bool = False
    requires_precious_metals: bool = False
    requires_hydrocarbon_chokepoints: bool = False
    requires_cognitive_resilience: bool = False
    requires_nuclear_autonomy: bool = False
    requires_bop_shield: bool = False
    requires_electoral_polarization: bool = False
    requires_refinery_sabotage: bool = False
    requires_hnwi_capital: bool = False
    requires_gold_repatriation: bool = False
    requires_multi_agent_consensus: bool = False
    requires_paleogenomics: bool = False
    requires_epistemic_triangulation: bool = False
    requires_soil_resilience: bool = False
    requires_dharmic_sovereignty: bool = False
    requires_sectoral_rotation: bool = False
    requires_island_net_security: bool = False
    requires_cbdc_surveillance: bool = False
    requires_interagency_synergy: bool = False
    requires_bank_crar: bool = False
    requires_bureaucratic_friction: bool = False
    requires_gan_radar: bool = False
    requires_high_altitude_airlift: bool = False
    requires_bigtech_algorithmic_sovereignty: bool = False
    requires_sacred_economy: bool = False
    requires_outward_asset_capture: bool = False
    requires_archaeo_astronomy: bool = False
    requires_black_projects: bool = False
    requires_trans_himalayan_hydrology: bool = False
    requires_predatory_dumping: bool = False
    requires_apaurusheya_epistemic: bool = False
    requires_sacred_heritage_encroachment: bool = False
    requires_narrative_inversion: bool = False
    requires_malacca_chokepoint: bool = False
    requires_ritual_ecological_sovereignty: bool = False
    requires_dharmic_constitutionalism: bool = False
    requires_partition_demystification: bool = False
    requires_canonical_epic_fidelity: bool = False
    requires_theological_apostasy_velocity: bool = False
    requires_aurobindonian_integration: bool = False
    requires_shastric_dietary_plurality: bool = False
    requires_archival_primary_source: bool = False
    requires_academic_gatekeeping: bool = False
    requires_succession_continuity: bool = False
    requires_linguistic_sprachbund: bool = False
    requires_indigenous_stem: bool = False
    requires_subaltern_memory: bool = False
    requires_industrial_attrition: bool = False
    requires_imperial_debt_overreach: bool = False
    requires_colonial_drain_extraction: bool = False
    speaker_profiles: List[Dict[str, Any]] = Field(default_factory=list)
    confidence_threshold: float = Field(default=0.75, ge=0.0, le=1.0)



_COMPILED_WORD_PATTERNS: Dict[str, re.Pattern] = {}


def get_word_boundary_pattern(kw: str) -> re.Pattern:
    """Returns a compiled regex pattern matching kw at discrete word boundaries."""
    kw_key = kw.strip().lower()
    if kw_key not in _COMPILED_WORD_PATTERNS:
        escaped = re.escape(kw_key)
        pattern_str = r"(?<!\w)" + escaped + r"(?!\w)"
        _COMPILED_WORD_PATTERNS[kw_key] = re.compile(pattern_str, re.IGNORECASE)
    return _COMPILED_WORD_PATTERNS[kw_key]


class QueryParser:
    """Extracts geopolitical entities, temporal horizons, and analytical intent from raw text."""

    @classmethod
    def matches_keyword(cls, text: str, keyword: str) -> bool:
        r"""
        Determines whether a keyword matches within text with word-boundary isolation.
        Uses regex lookbehind/lookahead `(?<!\w)pattern(?!\w)` so short tokens
        (e.g., 'ai', 'sc', 'lac') do not match within larger words ('said', 'scale', 'black').
        """
        if not keyword or not text:
            return False
        return bool(get_word_boundary_pattern(keyword).search(text))

    SUMMIT_PATTERNS: Dict[str, str] = {
        r"\bbrics\b": "BRICS Summit",
        r"\bsco\b|shanghai cooperation": "SCO Summit",
        r"\bg20\b": "G20 Summit",
        r"\bg7\b": "G7 Summit",
        r"\bquad\b": "Quad Leaders Summit",
        r"\basean\b": "ASEAN Summit",
        r"\bbimstec\b": "BIMSTEC Summit",
        r"\bsaarc\b": "SAARC Regional Forum",
        r"\bimec\b": "IMEC Corridor Forum",
        r"\bunga\b|united nations": "UN General Assembly",
    }

    COUNTRY_PATTERNS: Dict[str, str] = {
        r"\bindia\b|\bbharat\b": "India",
        r"\bchina\b|\bbeijing\b": "China",
        r"\brussia\b|\bmoscow\b": "Russia",
        r"\bbrazil\b": "Brazil",
        r"\bsouth africa\b": "South Africa",
        r"\biran\b|\btehran\b": "Iran",
        r"\bsaudi\b|\bsaudi arabia\b|\briyadh\b": "Saudi Arabia",
        r"\buae\b|\bemirates\b|\bdubai\b|\babu dhabi\b": "UAE",
        r"\begypt\b|\bcairo\b": "Egypt",
        r"\bethiopia\b|\baddis\b": "Ethiopia",
        r"\bbangladesh\b|\bdhaka\b": "Bangladesh",
        r"\bnepal\b|\bkathmandu\b": "Nepal",
        r"\bsri lanka\b|\bcolombo\b": "Sri Lanka",
        r"\bmyanmar\b|\bburma\b": "Myanmar",
        r"\bpakistan\b|\bislamabad\b": "Pakistan",
        r"\bmaldives\b|\bmale\b": "Maldives",
        r"\bbhutan\b|\bthimphu\b": "Bhutan",
        r"\bspain\b|\bspanish\b|\bmadrid\b|\bandalucia\b": "Spain",
        r"\bmorocco\b|\bmoroccan\b|\brabat\b": "Morocco",
        r"\btaiwan\b|\btaipei\b": "Taiwan",
        r"\bukraine\b|\bkyiv\b": "Ukraine",
        r"\busa\b|\bunited states\b|\bamerica\b|\bwashington\b": "USA",
    }

    LEADER_PATTERNS: Dict[str, str] = {
        r"\bmodi\b": "Narendra Modi",
        r"\bxi\b|\bxi jinping\b": "Xi Jinping",
        r"\bputin\b": "Vladimir Putin",
        r"\blula\b": "Luiz Inacio Lula da Silva",
        r"\bpezeshkian\b": "Masoud Pezeshkian",
        r"\bmbs\b|\bmohammed bin salman\b": "Mohammed bin Salman",
        r"\bmbz\b": "Mohammed bin Zayed",
        r"\bsisi\b": "Abdel Fattah el-Sisi",
        r"\bhasina\b|\bsheikh hasina\b": "Sheikh Hasina",
        r"\byunus\b|\bmuhammad yunus\b": "Muhammad Yunus",
        r"\bnetaji\b|\bsubhas\b|\bsubhas chandra bose\b": "Netaji Subhas Chandra Bose",
        r"\boli\b|\bk\.?p\.?\s*oli\b": "K.P. Sharma Oli",
        r"\bdissanayake\b|\banura\b": "Anura Kumara Dissanayake",
        r"\bmuizzu\b": "Mohamed Muizzu",
        r"\bdoval\b|\bajit doval\b": "Ajit Doval",
        r"\bhimanta\b|\bhimanta biswa sarma\b|\bhbs\b": "Himanta Biswa Sarma",
        r"\bneeraj\b|\bneeraj atri\b": "Neeraj Atri",
        r"\bambedkar\b|\bbhimrao\b|\bbabasaheb\b": "B.R. Ambedkar",
        r"\bvandyke\b|\bvan dyke\b|\bmatthew vandyke\b": "Matthew VanDyke",
        r"\bansari\b|\bhamid ansari\b": "Hamid Ansari",
        r"\bsrijan\b|\bsrijan pal singh\b": "Srijan Pal Singh",
        r"\bsai deepak\b|\bj\.?\s*sai deepak\b": "J. Sai Deepak",
    }

    MILITARY_BORDER_KEYWORDS: List[str] = [
        "lac", "loc", "troop", "troops", "deployment", "standoff", "clash", "skirmish",
        "patrol", "patrolling", "artillery", "infantry", "galwan", "doklam", "tawang", "depasang", "demchok"
    ]
    DEMOGRAPHIC_BORDER_KEYWORDS: List[str] = [
        "infiltrat", "migrant", "migration", "ceuta", "melilla", "refugee",
        "asylum", "demographic", "andalucia", "schengen", "border fence", "human trafficking"
    ]

    COLLOQUIAL_ROUTING_MAP: Dict[str, List[str]] = {
        "food_security": ["khana peena", "roti", "kisan", "annadata", "fasal", "gehun", "chawal", "anaj", "food security", "food crisis", "grain shortage", "fertilizer subsidy", "ration", "crop failure", "urea shortage", "potash supply"],
        "military_readiness": ["fauji", "sena", "goli", "barood", "hathiyar", "fouj", "topkhana", "jang", "drone burnout", "cost exchange", "sm-2", "sm-6"],
        "geo_economist": ["dhandha", "paisa", "rupaya", "kamai", "vyapar", "karz", "byaj"],
        "cash_flow": ["munafe", "kharcha", "jama", "nikasi", "hundi"],
        "propaganda": ["afwah", "dhokhadhadi", "farzi khabar", "bhatkana", "propoganda", "hisab chukta", "hisaab chukta", "hisab karega", "settle scores", "oratorical priming", "antithetical priming"],
        "institutional_lawfare": ["kacheri", "adalat", "vakil", "mudda", "chori", "dharna", "samundari kanoon", "eez kanoon", "sc st act", "section 18a", "kashinath", "general category", "ancestral sin"],
        "hybrid_covert": ["vandyke", "van dyke", "mercenary trainer", "sons of liberty", "camp victoria", "managed off-ramp", "sovereign compromise", "hamid ansari", "tehran raw", "nusrat mirza"],
        "petro_logistics": ["tel", "petrol", "diesel", "jahaz", "tatt", "samundar", "sagar"],
        "subsea_cables": ["samundari tar", "subsea tar", "sagar cable", "undersea internet", "internet cable", "cable cut", "landing station", "undersea fiber", "data corridor"],
        "astro_politics": ["antriksh", "graha", "upagraha", "space defense", "space weapon", "orbital asset", "satellite navigation", "isro mission"],
        "civilizational": ["itihaas", "purana", "puratan", "parampara", "sanskriti"],
        "demographic_infiltration": ["diaspora under siege", "texas hanuman", "sb 403", "caste lawfare"],
        "deep_tech": ["stem dilution", "grievance curricula", "lab capex"]
    }

    LENS_KEYWORDS: Dict[str, List[str]] = {
        "deep_tech": ["ai", "deep tech", "quantum", "compute", "algorithm", "frontier tech", "supercomputer", "synthetic", "biotech", "avionics", "digital leash", "odin", "alis", "mission data file", "electronic sovereignty", "stem dilution", "grievance curricula", "engineering capex", "technological dividend", "demographic dividend liability", "hard engineering", "lab capex"],
        "history": ["treaty", "precedent", "historical", "panchsheel", "1962", "1971", "1993", "cold war", "bretton woods", "bandung", "partition", "kargil", "balakot", "galwan", "pokhran", "sindoor", "sykes-picot", "1947", "1998", "1999", "somnath", "nalanda", "tarain", "chola", "srivijaya", "shivaji", "swarajya", "reversal", "millennial", "1000 year", "watson", "bernays", "mkultra", "mockingbird", "who code", "1920", "1928", "1953", "1981", "nilesh oak", "arundhati vasistha", "5561 bce", "3067 bce", "3102 bce", "bori critical edition", "sanauli chariot", "saraswati desiccation", "chronology arbitration", "historical timeline", "kahuta", "kanishka", "air india 182", "sriperumbudur", "ic 814", "kandahar hijack", "1993 mumbai blasts", "sinauli", "sanauli", "rakhigarhi", "copper hoard", "ocp", "pgw", "antennae sword", "chariot vs cart", "paleogenomics", "adna", "bsip"],
        "civilizational": ["meaning", "inner meaning", "civilization", "sanatan", "history", "kautilya", "mandala", "rajdharma", "dharmashastra", "smriti", "sadachara", "deshadharma", "kuladharma", "shankaracharya", "peetham", "matha", "parampara", "sampradaya", "dharma", "reversal", "symbolic date", "calendar", "temporal", "panchanga", "swarajya", "nalanda", "saptanga", "swami", "amatya", "janapada", "durga", "kosha", "danda", "seven limbs", "state sovereignty", "itihasa", "itihaasa", "mahabharata timeline", "ramayana timeline", "nilesh oak", "bori", "kali yuga epoch", "paradiplomacy", "sub-national paradiplomacy", "mizo-chin", "chin refugee", "yma", "soli", "sons of liberty", "faith-based contractor", "evangelical corridor", "sinauli", "sanauli", "rakhigarhi", "copper hoard", "ocp", "rigveda 10.18", "inhumation", "shmashana", "paleogenomics", "adna", "sattra", "srimanta sankardev", "batadrava", "gamusa"],
        "geo_economist": ["geo-economic", "geoeconomic", "trilemma", "mundell-fleming", "cips", "mbridge", "swift", "de-dollarization", "dedollarization", "dedollar", "vostro", "current account", "gold reserve", "central bank gold", "sovereign debt", "srva", "trapped rupee", "capital recycling", "vostro recycling", "g-sec reinvestment", "trade gap", "under-invoicing", "china deficit", "gdp discrepancy", "double deflation", "single deflation", "iebr", "fuel tax"],
        "geopolitical": ["power", "alliance", "rivalry", "border", "lac", "loc", "military", "troops", "standoff", "hedging", "security", "aukus", "imec", "i2u2", "quad", "bri", "belt and road", "game theory", "red team", "counter-move", "escalation spiral", "wargame campaign", "persistent campaign", "wargame session", "siliguri", "chicken's neck", "chickens neck", "chumbi", "doklam", "suwalki", "wakhan", "teesta", "rangpur", "pincer", "chokepoint kinetic"],
        "kinesics": ["bodylanguage", "body language", "photoshoot", "photo", "handshake", "posture", "gaze", "facial", "gamusa", "gamosa", "sartorial", "semiotic", "sartorial dissonance", "theatrical optics"],
        "cash_flow": ["cash", "investment", "fdi", "capex", "mou", "currency", "settlement", "money", "vostro", "funding", "npa write-off", "bad loan", "bank recapitalization", "haircut ratio", "ibc resolution", "write-off", "hawala", "d-company", "drone drop", "illicit finance", "crime-terror nexus", "syndicate liquidity", "asset freeze"],
        "propaganda": ["optics", "narrative", "message", "propaganda", "spin", "media", "watson", "bernays", "behavioral conditioning", "fear marketing", "anxiety capture", "torches of freedom", "mkultra", "mockingbird", "breast-milk substitutes", "teleological", "social engineering", "engineering of consent", "guilt marketing", "psychological warfare", "turn approver", "approver", "deshdrohi", "vote chori", "vote theft", "hisab chukta", "hisaab chukta", "hisab karega", "settle scores", "karega ki nahi", "antithetical priming", "oratorical priming", "grievance priming"],
        "petro_logistics": ["crude", "oil", "energy", "tanker", "chokepoint", "malacca", "hormuz"],
        "bureaucratic_inertia": ["bureaucracy", "bureaucratic", "press note 3", "veto", "ndrc", "rbi", "mea", "commerce", "regulatory delay", "inter-ministerial", "inertia", "putnam", "two-level game", "domestic backlash", "ugc rollback", "de-reservation", "draft guidelines", "policy rollback", "executive retreat", "clerical overreach", "bureaucratic disconnect"],
        "digital_sovereignty": ["digital sovereignty", "semiconductor", "lithography", "asml", "tsmc", "chip", "chips", "huawei", "5g", "6g", "telecom ban", "navic", "beidou", "gps", "data sovereignty"],
        "hybrid_covert": ["hybrid", "covert", "grey zone", "gray zone", "sabotage", "subversion", "intelligence", "proxy", "espionage", "psyop", "ramming", "shouldering", "bow crossing", "hunain", "pns", "naval standoff", "sub-kinetic", "technical error", "steering failure", "crew error", "inexperience", "diversion", "maskirovka", "competing hypotheses", "ach", "why did it happen", "asymmetric response", "sequential move", "tipping point", "unknown gunmen", "doval", "offensive-defense", "kahuta", "spg", "special protection group", "sriperumbudur", "ic 814", "kandahar", "d-company", "ripudaman", "malik", "nijjar", "sanctuary", "safe haven", "extraterritorial", "vandyke", "van dyke", "matthew vandyke", "soli", "sons of liberty", "camp victoria", "ukrainian drone", "mercenary trainer", "fpv proliferation", "chin national army", "cna", "sovereign compromise", "sovereign asymmetry", "diplomatic deportation", "quattrocchi", "warren anderson", "mercenary off-ramp", "hamid ansari", "tehran raw", "nusrat mirza", "counter-intel vetting", "diplomatic compromise", "diplomatic deep state", "station compromise", "raw network compromise"],
        "india_timeline": ["bangladesh", "hasina", "yunus", "netaji", "ram mandir", "ayodhya", "siliguri", "chicken neck", "teesta", "bimstec", "saarc", "neighborhood", "neighborhood first", "mizoram", "manipur", "chin state", "indo-myanmar", "zokhawthar", "champhai"],
        "demographic_infiltration": ["infiltrat", "migrant", "migration", "ceuta", "melilla", "refugee", "asylum", "demographic", "andalucia", "schengen", "human trafficking", "rangpur", "siliguri", "chicken's neck", "illegal infiltration", "border demographic", "rohingya", "cross-border infiltration", "demographic balance", "border census", "gorukhuti", "char land", "sonowal", "imdt", "external aggression", "batadrava", "diaspora under siege", "sb 403", "caste lawfare", "texas hanuman", "statue of union", "nativist backlash", "h-1b ban", "diaspora fragility", "diaspora backlash", "sugar land"],
        "critical_minerals": ["rare earth", "mineral", "lithium", "cobalt", "semiconductor", "gallium", "germanium", "supply chain", "refining monopoly", "ndfeb", "magnet", "processing monopoly", "rare earth processing", "midstream", "nickel", "graphite", "neodymium", "heavy rare earth", "clean energy minerals", "lithium refinery"],
        "institutional_lawfare": ["fatf", "lawfare", "icc", "icj", "sanctions", "ofac", "asset freeze", "jurisdiction", "blacklisting", "constitution", "constitutional", "article 44", "ucc", "uniform civil code", "waqf", "fcra", "sc/st", "reservation", "fundamental rights", "hrce", "temple control", "judicial activism", "1991 agreement", "colregs", "buffer distance", "maritime accord", "rpa", "representation of the people", "booth level agent", "bla", "special intensive revision", "sir", "electoral roll", "vote chori", "vote theft", "turn approver", "election commission", "election petition", "form 7", "form 8", "form 17c", "voter list", "voter deletion", "default bail", "section 167", "section 188", "foreigners act compounding", "piecemeal chargesheet", "statutory off-ramp", "managed off-ramp", "maritime zone", "act 80", "unclos", "eez", "exclusive economic zone", "contiguous zone", "innocent passage", "transit passage", "fonop", "maritime boundary", "coastal state", "anti-piracy", "sattra", "char land", "batadrava", "gorukhuti", "dhalpur", "waqf board", "section 40", "imdt", "section 8a", "sc st act", "section 18a", "kashinath mahajan", "subhash kashinath", "anticipatory bail denial", "hisab chukta", "ancestral sin", "general category", "caste faultline", "creamy layer", "due process erosion"],
        "food_security": ["food", "food security", "fertilizer", "urea", "dap", "mop", "grain", "wheat", "rice", "famine", "buffer stock", "pds", "agriculture", "export ban", "water security", "monsoon", "groundwater", "indus waters", "teesta", "brahmaputra", "potassium", "fertilizer import", "soil nutrient", "fertilizer dependency", "rice ban", "wheat ban", "onion duty", "price stabilization", "farmer income", "anti-farmer", "grain shortage", "fertilizer subsidy", "caloric intake", "food crisis"],
        "military_readiness": ["military readiness", "orbat", "order of battle", "wwr", "war wastage", "ammunition", "air defense", "s-400", "tejas", "nuclear triad", "deterrence", "escalation ladder", "mobilization", "cyber", "electronic warfare", "dca", "fifth domain", "naval", "warship", "pns", "hunain", "sea control", "sea denial", "ramming", "shouldering", "rudder failure", "hydrodynamic", "seamanship", "watchstander", "mechanical failure", "f-35", "f35", "odin", "alis", "su-57", "su57", "mrfa", "stealth fighter", "digital leash", "kill-switch", "kill switch", "luneburg", "rcs", "radar cross section", "tarang shakti", "jodhpur air base", "avionics sovereignty", "drone burnout", "cost-exchange ratio", "cost exchange", "interceptor exhaustion", "sm-2", "sm-6", "shahed drone", "houthi drone", "magazine depth", "asymmetric drone burnout"],
        "subsea_cables": ["subsea", "subsea cable", "underwater cable", "fiber optic", "submarine cable", "seabed", "seabed mining", "hydrophone", "eez", "polymetallic", "sea cable", "optic fiber", "landing station", "data traffic", "cable severed", "cable damage", "undersea data", "red sea cable", "mumbai landing", "chennai landing", "undersea internet", "subsea communications"],
        "astro_politics": ["space", "satellite", "orbital", "navic", "asat", "anti-satellite", "counter-space", "starlink", "isro", "leo constellation", "space situational awareness", "space program", "space weapon", "orbit", "orbital reconnaissance", "space debris", "project netra", "gsat", "space domain", "space defense", "satellite navigation"],
        "negative_space": ["synopsis", "omitted", "dropped", "communique", "declaration", "text", "agenda", "draft"],
    }

    @classmethod
    def parse(cls, prompt: str) -> StrategicQuery:
        """Parses an arbitrary query string into an actionable StrategicQuery."""
        if not prompt or not isinstance(prompt, str) or not prompt.strip():
            prompt = "Strategic Horizon Analysis"
        # Input envelope: truncate excessive prompt length to prevent ReDoS / memory exhaustion
        if len(prompt) > 5000:
            prompt = prompt[:5000]
        text_lower = prompt.lower()

        # 1. Extract Target Countries first to inform event titles
        matched_countries = []
        for pattern, country in cls.COUNTRY_PATTERNS.items():
            if re.search(pattern, text_lower):
                if country not in matched_countries:
                    matched_countries.append(country)

        # If user asks for "all member countries", populate full BRICS+ default roster
        if "all member" in text_lower or "all country" in text_lower or "one by one" in text_lower:
            matched_countries = [
                "India", "China", "Russia", "Brazil", "South Africa",
                "Iran", "Saudi Arabia", "UAE", "Egypt", "Ethiopia"
            ]

        # 2. Extract Year and Focal Date
        year_match = re.search(r"\b(20[2-3][0-9])\b", text_lower)
        year = int(year_match.group(1)) if year_match else 2026

        date_match = re.search(r"\b(\d{1,2}(?:st|nd|rd|th)?\s+(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?))\b", text_lower)
        if not date_match:
            date_match = re.search(r"\b((?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\s+\d{1,2}(?:st|nd|rd|th)?)\b", text_lower)
        focal_date = date_match.group(1).title() if date_match else None

        # 3. Detect Summit vs. Non-Summit Crisis Classification
        summit_name = None
        for pattern, name in cls.SUMMIT_PATTERNS.items():
            if re.search(pattern, text_lower):
                summit_name = name
                break

        if summit_name:
            event_type = "SUMMIT"
            summit_full_name = f"{summit_name.split()[0]} {year} Summit"
        elif any(cls.matches_keyword(text_lower, kw) for kw in cls.MILITARY_BORDER_KEYWORDS) or ("border" in text_lower and any(cls.matches_keyword(text_lower, kw) for kw in ["military", "troop", "troops", "army", "pla", "clash", "standoff", "patrolling", "patrol"])):
            event_type = "BORDER_MILITARY"
            c_names = " - ".join(matched_countries[:2]) if matched_countries else "Regional"
            summit_full_name = f"{c_names} Sovereign Border Military Standoff ({year})"
        elif any(cls.matches_keyword(text_lower, kw) for kw in cls.DEMOGRAPHIC_BORDER_KEYWORDS):
            event_type = "BORDER_SECURITY"
            c_name = matched_countries[0] if matched_countries else "Regional"
            summit_full_name = f"{c_name} Border Security & Infiltration Event ({year})"
        elif any(cls.matches_keyword(text_lower, kw) for kw in ["de-dollar", "dollar collapse", "vostro", "currency run", "gold bullion", "bank default"]):
            event_type = "GEO_ECONOMIC"
            summit_full_name = f"Geo-Economic Liquidity & Currency Crisis ({year})"
        elif any(cls.matches_keyword(text_lower, kw) for kw in ["feet", "touch feet", "spiritual", "shirk", "blasphemy", "civilizational crisis", "existential crisis", "famine", "food embargo"]):
            event_type = "CIVILIZATIONAL_CRISIS"
            summit_full_name = f"Civilizational Protocol & Existential Crisis ({year})"
        elif any(cls.matches_keyword(text_lower, kw) for kw in ["fatf", "lawfare", "icc", "icj", "asset freeze"]):
            event_type = "HYBRID_WARFARE"
            summit_full_name = f"Institutional Lawfare & Sanctions Escalation ({year})"
        else:
            event_type = "STRATEGIC_EVENT"
            summit_full_name = f"Strategic Event Analysis ({year})"

        # 4. Extract Target Leaders
        matched_leaders = []
        for pattern, leader in cls.LEADER_PATTERNS.items():
            if re.search(pattern, text_lower):
                if leader not in matched_leaders:
                    matched_leaders.append(leader)

        # 5. Extract Prioritized Lenses
        active_lenses = []
        for lens_name, keywords in cls.LENS_KEYWORDS.items():
            colloquial = cls.COLLOQUIAL_ROUTING_MAP.get(lens_name, [])
            all_kw = keywords + colloquial
            if any(cls.matches_keyword(text_lower, kw) for kw in all_kw):
                active_lenses.append(lens_name)

        # Boolean flags
        req_kinesics = "kinesics" in active_lenses or any(cls.matches_keyword(text_lower, kw) for kw in ["photo", "photoshoot", "bodylanguage", "body language"])
        req_cash = "cash_flow" in active_lenses or any(cls.matches_keyword(text_lower, kw) for kw in ["cash", "investment", "achieve", "achive", "yield"])
        req_neg_space = "negative_space" in active_lenses or any(cls.matches_keyword(text_lower, kw) for kw in ["synopsis", "meeting", "communique", "declaration"])
        req_civilizational = "civilizational" in active_lenses or any(cls.matches_keyword(text_lower, kw) for kw in ["meaning", "deep", "civilization", "sanatan"])
        req_timeline = "india_timeline" in active_lenses or any(cls.matches_keyword(text_lower, kw) for kw in ["bangladesh", "hasina", "netaji", "ram mandir", "siliguri"])
        req_demographic = "demographic_infiltration" in active_lenses or event_type == "BORDER_SECURITY"
        req_minerals = "critical_minerals" in active_lenses
        req_lawfare = "institutional_lawfare" in active_lenses or event_type == "HYBRID_WARFARE"
        req_chronology = (
            any(cls.matches_keyword(text_lower, kw) for kw in [
                "chronology", "timeline dispute", "nilesh oak", "5561 bce", "3067 bce",
                "3102 bce", "arundhati vasistha", "mahabharata date", "ramayana date",
                "bori critical edition", "historical timeline"
            ]) or
            ("timeline" in text_lower and any(cls.matches_keyword(text_lower, w) for w in ["mahabharat", "ramayan", "ancient", "epic", "dating", "dispute", "verdict"]))
        )

        req_abyssal = any(cls.matches_keyword(text_lower, kw) for kw in ["abyssal", "polymetallic", "matsya", "samudrayaan", "seabed", "nodule", "deep submergence"])
        req_trophic = any(cls.matches_keyword(text_lower, kw) for kw in ["trophic", "diclofenac", "vulture", "rabies", "zoonotic", "biosecurity cascade", "scavenger"])
        req_cognitive = any(cls.matches_keyword(text_lower, kw) for kw in ["cognitive enclosure", "antahkarana", "synthetic empathy", "ai colonization", "foreign model", "proprietary ai"])
        req_bullion = any(cls.matches_keyword(text_lower, kw) for kw in ["bullion", "paper gold", "comex", "lbma", "gold repatriation", "tariff arbitrage", "rbi gold", "vault drain"])
        req_insurgency = any(cls.matches_keyword(text_lower, kw) for kw in ["sub-national", "insurgency incubation", "patel vs indira", "partisan blowback", "fringe militant"])
        req_quantum = any(cls.matches_keyword(text_lower, kw) for kw in ["quantum", "superposition", "shannon alignment", "pqc", "quantum statecraft", "qubit"])
        req_grayzone_micro = any(cls.matches_keyword(text_lower, kw) for kw in ["sacred calendar", "waqf", "hr&ce", "street veto", "corridor demographic", "communal friction", "due process asymmetry"])
        req_pnt = any(cls.matches_keyword(text_lower, kw) for kw in ["pnt", "navic", "irnss", "rubidium", "clock drift", "gps denial", "missile cep", "satellite navigation"])
        req_ai_gov = any(cls.matches_keyword(text_lower, kw) for kw in ["flop", "ai safety", "ai governance", "regulatory moat", "open-source suppression", "it margin", "frontier ai"])
        req_proxy = any(cls.matches_keyword(text_lower, kw) for kw in ["operation tupac", "proxy warfare", "narco-hawala", "sleeper cell", "asymmetric attrition"])
        req_textual = any(cls.matches_keyword(text_lower, kw) for kw in ["bori", "valmiki", "vyasa", "critical edition", "textual stratigraphy", "shruti", "smriti", "pop myth", "andhe ka putra"])
        req_media = any(cls.matches_keyword(text_lower, kw) for kw in ["elite media", "underworld capital", "dopamine decay", "short-form", "media capture", "cognitive capture"])
        req_hydro = any(cls.matches_keyword(text_lower, kw) for kw in ["medog", "upper siang", "water bomb", "upstream dam", "hydro weaponization", "dam buffer", "brahmaputra flood"])
        req_antiquity = any(cls.matches_keyword(text_lower, kw) for kw in ["antiquity", "murti", "repatriation", "unesco 1970", "stolen idol", "sacred heritage", "temple plunder", "museum cartel"])
        req_diaspora = any(cls.matches_keyword(text_lower, kw) for kw in ["diaspora sanctuary", "host tolerance", "free speech pretext", "consular reciprocity", "transnational extremist", "safe haven"])
        req_pm = any(cls.matches_keyword(text_lower, kw) for kw in ["bullion", "sge", "comex", "streedhan", "gold repatriation", "physical gold", "paper derivative"])
        req_hydro_choke = any(cls.matches_keyword(text_lower, kw) for kw in ["hormuz", "brent shock", "chokepoint interdiction", "spr cover", "chabahar bypass", "tanker interdiction"])
        req_cog_res = any(cls.matches_keyword(text_lower, kw) for kw in ["cortical resilience", "dharmic stoicism", "dhriti", "viveka", "outrage-bait", "amygdala panic", "cognitive resilience"])
        req_nuc = any(cls.matches_keyword(text_lower, kw) for kw in ["fast breeder", "pfbr", "thorium cycle", "nsg cartel", "nuclear autonomy", "smr captive", "closed fuel cycle"])
        req_bop = any(cls.matches_keyword(text_lower, kw) for kw in ["bop shield", "balance of payments", "greenspan-guidotti", "dii absorption", "fii flight", "forex import cover"])
        req_elec = any(cls.matches_keyword(text_lower, kw) for kw in ["electoral polarization", "labharthi", "maryada", "caste fragmentation", "election commission neutrality", "welfare saturation"])
        req_refinery_sab = any(cls.matches_keyword(text_lower, kw) for kw in ["refinery sabotage", "ruf pit", "vizag refinery", "ot sabotage", "scada anomaly", "crack spread", "dcs anomaly"])
        req_hnwi = any(cls.matches_keyword(text_lower, kw) for kw in ["hnwi", "capital flight", "gift city", "inheritance tax", "wealth tax", "confiscation rhetoric", "onshoring"])
        req_gold_repat = any(cls.matches_keyword(text_lower, kw) for kw in ["gold repatriation", "rbi gold", "domestic vault", "bullion immunity", "counterparty default", "g7 asset freeze"])
        req_multi_agent = any(cls.matches_keyword(text_lower, kw) for kw in ["multi-agent", "agent consensus", "group chat", "agent swarm", "circular loop", "credential isolation"])
        req_paleo = any(cls.matches_keyword(text_lower, kw) for kw in ["rakhigarhi", "ancient dna", "adna", "indus periphery", "aasi", "aryan migration", "steppe pastoralist", "endogamy"])
        req_triang = any(cls.matches_keyword(text_lower, kw) for kw in ["epistemic triangulation", "archaeozoology", "harappa centenary", "faunal evidence", "zebu", "osteometry"])
        req_soil = any(cls.matches_keyword(text_lower, kw) for kw in ["soil resilience", "save soil", "soil organic carbon", "soc", "topsoil", "agroforestry", "desertification"])
        req_dharmic_sov = any(cls.matches_keyword(text_lower, kw) for kw in ["dharmic soft power", "free tn temples", "temple autonomy", "hr&ce", "cultural decolonization", "spiritual diplomacy"])
        req_sec_rot = any(cls.matches_keyword(text_lower, kw) for kw in ["sectoral rotation", "grid saturation", "data center grid", "ai capex", "index illusion", "hyperscaler capex", "sensex 2000"])
        req_island_sec = any(cls.matches_keyword(text_lower, kw) for kw in ["island net security", "eez surveillance", "agalega", "maritime bastion", "hydrographic vessel", "plan incursion", "sagar"])
        req_cbdc_surv = any(cls.matches_keyword(text_lower, kw) for kw in ["cbdc surveillance", "programmable cbdc", "monetary autonomy", "digital enclosure", "programmable money", "cash retention"])
        req_interagency = any(cls.matches_keyword(text_lower, kw) for kw in ["inter-agency synergy", "counter subversion", "nia cbi ed", "fiu-ind", "hawala crackdown", "gangster-terror", "fcra subversion"])
        req_bank_crar = any(cls.matches_keyword(text_lower, kw) for kw in ["bank crar", "asset quality", "crar ratio", "banking fortress", "net npa", "provision coverage", "treasury mtm"])
        req_bur_fric = any(cls.matches_keyword(text_lower, kw) for kw in ["bureaucratic friction", "administrative velocity", "file looping", "pil lawfare", "sub-national inertia", "statutory de-registration"])
        req_gan_radar = any(cls.matches_keyword(text_lower, kw) for kw in ["gan radar", "gallium nitride", "aesa radar", "trm density", "radar sovereignty", "indigenous aesa", "wide bandgap"])
        req_high_airlift = any(cls.matches_keyword(text_lower, kw) for kw in ["nyoma alg", "high altitude airlift", "thrust derating", "daulat beg oldi", "winter lac logistics", "heavy airlift"])
        req_algo_sov = any(cls.matches_keyword(text_lower, kw) for kw in ["algorithmic sovereignty", "big tech sovereignty", "shadow banning", "algorithmic nudging", "dpdp enforcement", "meta fir", "section 69a"])
        req_sacred_econ = any(cls.matches_keyword(text_lower, kw) for kw in ["sacred economy", "pilgrimage tourism", "ayodhya economy", "kashi corridor", "religious tourism multiplier", "temple msme"])
        req_outward_odi = any(cls.matches_keyword(text_lower, kw) for kw in ["outward direct investment", "odi asset capture", "western asset acquisition", "ip repatriation", "distressed asset capture", "corporate odi"])
        req_archaeo_astro = any(cls.matches_keyword(text_lower, kw) for kw in ["archaeo-astronomy", "planetary conjunction", "epigraphic dating", "ved veer arya", "vedic astronomy", "equinox retro-calculation", "sediment stratigraphy"])
        req_black_proj = any(cls.matches_keyword(text_lower, kw) for kw in ["black project", "special access program", "c4isr early warning", "deep state black", "nuclear alert cushion", "annie jacobsen"])
        req_trans_hydro = any(cls.matches_keyword(text_lower, kw) for kw in ["yarlung tsangpo", "upper siang", "medog dam", "trans-himalayan hydrology", "hydrological warfare", "buffer reservoir", "brahmaputra dam"])
        req_pred_dumping = any(cls.matches_keyword(text_lower, kw) for kw in ["canton fair", "predatory dumping", "overcapacity dumping", "qco enforcement", "diaper dumping", "toy dumping", "anti-dumping duty"])
        req_apaurusheya = any(cls.matches_keyword(text_lower, kw) for kw in ["apaurusheya", "apaurusheyatva", "shastric ontology", "vedic epistemology", "colonial philology", "ramnath jha", "sabda pramana"])
        req_heritage_encroach = any(cls.matches_keyword(text_lower, kw) for kw in ["heritage encroachment", "shivaji forts", "vishalgad", "lohagad", "mazar encroachment", "hilltop fort", "asi enforcement"])
        req_narr_inversion = any(cls.matches_keyword(text_lower, kw) for kw in ["narrative inversion", "ravanayana", "villain glamorization", "moral taxonomy inversion", "consumer boycott", "cinema subversion"])
        req_malacca = any(cls.matches_keyword(text_lower, kw) for kw in ["malacca strait", "great nicobar bastion", "anc strike", "malacca deterrence", "chokepoint veto", "chinese sloc"])
        req_ritual_eco = any(cls.matches_keyword(text_lower, kw) for kw in ["ritual ecological", "diwali firecrackers", "selective prohibition", "festival ban", "shastric ritual", "environmental lawfare", "firecracker ban"])
        req_dharmic_const = any(cls.matches_keyword(text_lower, kw) for kw in ["dharmic constitutionalism", "rajdharma", "decolonial jurisprudence", "borrowed constitutional dogma", "civilizational sanskriti", "decolonial law"])
        req_part_demyst = any(cls.matches_keyword(text_lower, kw) for kw in ["partition demystification", "historical sandarshan", "khilafat appeasement", "moplah atrocities", "mahatma-ism", "demystify partition", "partition causality"])
        req_epic_fidelity = any(cls.matches_keyword(text_lower, kw) for kw in ["canonical epic fidelity", "valmiki ramayana", "cinematic subversion", "adipurush", "marxist pop revisionism", "epic fidelity", "canonical fidelity"])
        req_theol_apostasy = any(cls.matches_keyword(text_lower, kw) for kw in ["theological incompatibility", "ex-muslim", "apostasy velocity", "irtidad", "surah 3:85", "sanatani muslim myth", "scriptural exclusivity"])
        req_aurobindo_integ = any(cls.matches_keyword(text_lower, kw) for kw in ["aurobindonian integration", "sri aurobindo", "spiritual integration", "shakta tantric harmony", "decentralized sanatan", "regional bastions", "integral nationalism"])
        req_shastric_diet = any(cls.matches_keyword(text_lower, kw) for kw in ["shastric dietary plurality", "dietary plurality", "shakta offering", "kamakhya dietary", "vaishnava vegetarianism", "culinary pluralism", "tantric offering"])
        req_archival_source = any(cls.matches_keyword(text_lower, kw) for kw in ["archival primary source", "primary epigraphy", "copper plate inscription", "inam register", "archival fidelity", "archival evidence"])
        req_academic_gate = any(cls.matches_keyword(text_lower, kw) for kw in ["academic gatekeeping", "literary festival gatekeeping", "foreign donor alignment", "narrative colonization", "think tank gatekeeping"])
        req_succ_cont = any(cls.matches_keyword(text_lower, kw) for kw in ["succession continuity", "leadership succession", "modi to yogi", "political transition risk", "capex statutory durability", "cadre alignment"])
        req_ling_sprach = any(cls.matches_keyword(text_lower, kw) for kw in ["linguistic sprachbund", "sprachbund convergence", "sanskrit and tamil", "proto-dravidian", "munda loanwords", "linguistic balkanization", "retroflex phonology"])
        req_indig_stem = any(cls.matches_keyword(text_lower, kw) for kw in ["indigenous stem", "wootz steel", "zawar zinc", "ancient indian metallurgy", "stem authenticity", "mathematical manuscript", "sulba sutras"])
        req_subalt_mem = any(cls.matches_keyword(text_lower, kw) for kw in ["subaltern memory", "hero stones", "viragals", "oral folk resistance", "village memorial", "subaltern history"])
        req_ind_attr = any(cls.matches_keyword(text_lower, kw) for kw in ["industrial attrition", "ammunition burn rate", "shell production surge", "drone fabrication capacity", "propellant precursor", "180-day attrition"])
        req_imp_debt = any(cls.matches_keyword(text_lower, kw) for kw in ["imperial debt overreach", "debt-to-gdp military", "basing retrenchment", "fiscal crowding out defense", "imperial overstretch"])
        req_col_drain = any(cls.matches_keyword(text_lower, kw) for kw in ["colonial drain extraction", "council bills drain", "45 trillion drain", "deindustrialization tariff", "colonial wealth drain"])

        if req_pnt and "military_readiness" not in active_lenses:
            active_lenses.append("military_readiness")
        if req_ai_gov and "deep_tech" not in active_lenses:
            active_lenses.append("deep_tech")
        if req_proxy and "hybrid_covert" not in active_lenses:
            active_lenses.append("hybrid_covert")
        if req_textual and "civilizational" not in active_lenses:
            active_lenses.append("civilizational")
        if req_media and "propaganda" not in active_lenses:
            active_lenses.append("propaganda")
        if req_hydro and "food_security" not in active_lenses:
            active_lenses.append("food_security")
        if req_antiquity and "civilizational" not in active_lenses:
            active_lenses.append("civilizational")
        if req_diaspora and "geopolitical" not in active_lenses:
            active_lenses.append("geopolitical")
        if req_pm and "cash_flow" not in active_lenses:
            active_lenses.append("cash_flow")
        if req_hydro_choke and "petro_logistics" not in active_lenses:
            active_lenses.append("petro_logistics")
        if req_cog_res and "propaganda" not in active_lenses:
            active_lenses.append("propaganda")
        if req_nuc and "deep_tech" not in active_lenses:
            active_lenses.append("deep_tech")
        if req_bop and "cash_flow" not in active_lenses:
            active_lenses.append("cash_flow")
        if req_elec and "institutional_lawfare" not in active_lenses:
            active_lenses.append("institutional_lawfare")
        if req_refinery_sab and "petro_logistics" not in active_lenses:
            active_lenses.append("petro_logistics")
        if req_hnwi and "cash_flow" not in active_lenses:
            active_lenses.append("cash_flow")
        if req_gold_repat and "cash_flow" not in active_lenses:
            active_lenses.append("cash_flow")
        if req_multi_agent and "deep_tech" not in active_lenses:
            active_lenses.append("deep_tech")
        if req_paleo and "civilizational" not in active_lenses:
            active_lenses.append("civilizational")
        if req_triang and "history" not in active_lenses:
            active_lenses.append("history")
        if req_soil and "food_security" not in active_lenses:
            active_lenses.append("food_security")
        if req_dharmic_sov and "civilizational" not in active_lenses:
            active_lenses.append("civilizational")
        if req_sec_rot and "geo_economist" not in active_lenses:
            active_lenses.append("geo_economist")
        if req_island_sec and "geopolitical" not in active_lenses:
            active_lenses.append("geopolitical")
        if req_cbdc_surv and "digital_sovereignty" not in active_lenses:
            active_lenses.append("digital_sovereignty")
        if req_interagency and "hybrid_covert" not in active_lenses:
            active_lenses.append("hybrid_covert")
        if req_bank_crar and "cash_flow" not in active_lenses:
            active_lenses.append("cash_flow")
        if req_bur_fric and "bureaucratic_inertia" not in active_lenses:
            active_lenses.append("bureaucratic_inertia")
        if req_gan_radar and "deep_tech" not in active_lenses:
            active_lenses.append("deep_tech")
        if req_high_airlift and "military_readiness" not in active_lenses:
            active_lenses.append("military_readiness")
        if req_algo_sov and "digital_sovereignty" not in active_lenses:
            active_lenses.append("digital_sovereignty")
        if req_sacred_econ and "civilizational" not in active_lenses:
            active_lenses.append("civilizational")
        if req_outward_odi and "geo_economist" not in active_lenses:
            active_lenses.append("geo_economist")
        if req_archaeo_astro and "history" not in active_lenses:
            active_lenses.append("history")
        if req_black_proj and "hybrid_covert" not in active_lenses:
            active_lenses.append("hybrid_covert")
        if req_trans_hydro and "geopolitical" not in active_lenses:
            active_lenses.append("geopolitical")
        if req_pred_dumping and "geo_economist" not in active_lenses:
            active_lenses.append("geo_economist")
        if req_apaurusheya and "civilizational" not in active_lenses:
            active_lenses.append("civilizational")
        if req_heritage_encroach and "institutional_lawfare" not in active_lenses:
            active_lenses.append("institutional_lawfare")
        if req_narr_inversion and "propaganda" not in active_lenses:
            active_lenses.append("propaganda")
        if req_malacca and "military_readiness" not in active_lenses:
            active_lenses.append("military_readiness")
        if req_ritual_eco and "institutional_lawfare" not in active_lenses:
            active_lenses.append("institutional_lawfare")
        if req_dharmic_const and "institutional_lawfare" not in active_lenses:
            active_lenses.append("institutional_lawfare")
        if req_part_demyst and "history" not in active_lenses:
            active_lenses.append("history")
        if req_epic_fidelity and "propaganda" not in active_lenses:
            active_lenses.append("propaganda")
        if req_theol_apostasy and "demographic_infiltration" not in active_lenses:
            active_lenses.append("demographic_infiltration")
        if req_aurobindo_integ and "civilizational" not in active_lenses:
            active_lenses.append("civilizational")
        if req_shastric_diet and "civilizational" not in active_lenses:
            active_lenses.append("civilizational")
        if req_archival_source and "history" not in active_lenses:
            active_lenses.append("history")
        if req_academic_gate and "propaganda" not in active_lenses:
            active_lenses.append("propaganda")
        if req_succ_cont and "geo_economist" not in active_lenses:
            active_lenses.append("geo_economist")
        if req_ling_sprach and "civilizational" not in active_lenses:
            active_lenses.append("civilizational")
        if req_indig_stem and "deep_tech" not in active_lenses:
            active_lenses.append("deep_tech")
        if req_subalt_mem and "history" not in active_lenses:
            active_lenses.append("history")
        if req_ind_attr and "military_readiness" not in active_lenses:
            active_lenses.append("military_readiness")
        if req_imp_debt and "cash_flow" not in active_lenses:
            active_lenses.append("cash_flow")
        if req_col_drain and "history" not in active_lenses:
            active_lenses.append("history")

        # Resolve speaker profiles
        from .speaker_profiler import EpistemicSpeakerProfiler
        resolved_profiles = []
        seen_profile_ids = set()
        for leader in matched_leaders:
            prof = EpistemicSpeakerProfiler.get_profile(leader)
            if prof and prof.canonical_id not in seen_profile_ids:
                resolved_profiles.append(prof.to_dict())
                seen_profile_ids.add(prof.canonical_id)
        for prof in EpistemicSpeakerProfiler.resolve_from_text(prompt):
            if prof.canonical_id not in seen_profile_ids:
                resolved_profiles.append(prof.to_dict())
                seen_profile_ids.add(prof.canonical_id)

        return StrategicQuery(
            raw_prompt=prompt,
            target_summit=summit_full_name,
            target_event=summit_full_name,
            event_type=event_type,
            focal_date=focal_date,
            year=year,
            target_countries=matched_countries,
            target_leaders=matched_leaders,
            prioritized_lenses=active_lenses,
            requires_kinesics=req_kinesics,
            requires_cash_audit=req_cash,
            requires_negative_space=req_neg_space,
            requires_civilizational_depth=req_civilizational,
            requires_india_timeline=req_timeline,
            requires_demographic_audit=req_demographic,
            requires_minerals_audit=req_minerals,
            requires_lawfare_audit=req_lawfare,
            requires_chronology_arbitration=req_chronology,
            requires_abyssal_sovereignty=req_abyssal,
            requires_trophic_biosecurity=req_trophic,
            requires_cognitive_sovereignty=req_cognitive,
            requires_bullion_audit=req_bullion,
            requires_insurgency_audit=req_insurgency,
            requires_quantum_statecraft=req_quantum,
            requires_grayzone_micro_signal=req_grayzone_micro,
            requires_pnt_autonomy=req_pnt,
            requires_ai_governance=req_ai_gov,
            requires_proxy_warfare=req_proxy,
            requires_textual_triangulation=req_textual,
            requires_media_capture=req_media,
            requires_hydro_weaponization=req_hydro,
            requires_antiquity_restitution=req_antiquity,
            requires_diaspora_sanctuary=req_diaspora,
            requires_precious_metals=req_pm,
            requires_hydrocarbon_chokepoints=req_hydro_choke,
            requires_cognitive_resilience=req_cog_res,
            requires_nuclear_autonomy=req_nuc,
            requires_bop_shield=req_bop,
            requires_electoral_polarization=req_elec,
            requires_refinery_sabotage=req_refinery_sab,
            requires_hnwi_capital=req_hnwi,
            requires_gold_repatriation=req_gold_repat,
            requires_multi_agent_consensus=req_multi_agent,
            requires_paleogenomics=req_paleo,
            requires_epistemic_triangulation=req_triang,
            requires_soil_resilience=req_soil,
            requires_dharmic_sovereignty=req_dharmic_sov,
            requires_sectoral_rotation=req_sec_rot,
            requires_island_net_security=req_island_sec,
            requires_cbdc_surveillance=req_cbdc_surv,
            requires_interagency_synergy=req_interagency,
            requires_bank_crar=req_bank_crar,
            requires_bureaucratic_friction=req_bur_fric,
            requires_gan_radar=req_gan_radar,
            requires_high_altitude_airlift=req_high_airlift,
            requires_bigtech_algorithmic_sovereignty=req_algo_sov,
            requires_sacred_economy=req_sacred_econ,
            requires_outward_asset_capture=req_outward_odi,
            requires_archaeo_astronomy=req_archaeo_astro,
            requires_black_projects=req_black_proj,
            requires_trans_himalayan_hydrology=req_trans_hydro,
            requires_predatory_dumping=req_pred_dumping,
            requires_apaurusheya_epistemic=req_apaurusheya,
            requires_sacred_heritage_encroachment=req_heritage_encroach,
            requires_narrative_inversion=req_narr_inversion,
            requires_malacca_chokepoint=req_malacca,
            requires_ritual_ecological_sovereignty=req_ritual_eco,
            requires_dharmic_constitutionalism=req_dharmic_const,
            requires_partition_demystification=req_part_demyst,
            requires_canonical_epic_fidelity=req_epic_fidelity,
            requires_theological_apostasy_velocity=req_theol_apostasy,
            requires_aurobindonian_integration=req_aurobindo_integ,
            requires_shastric_dietary_plurality=req_shastric_diet,
            requires_archival_primary_source=req_archival_source,
            requires_academic_gatekeeping=req_academic_gate,
            requires_succession_continuity=req_succ_cont,
            requires_linguistic_sprachbund=req_ling_sprach,
            requires_indigenous_stem=req_indig_stem,
            requires_subaltern_memory=req_subalt_mem,
            requires_industrial_attrition=req_ind_attr,
            requires_imperial_debt_overreach=req_imp_debt,
            requires_colonial_drain_extraction=req_col_drain,
            speaker_profiles=resolved_profiles,
            confidence_threshold=0.80
        )


