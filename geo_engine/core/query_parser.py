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
            speaker_profiles=resolved_profiles,
            confidence_threshold=0.80
        )


