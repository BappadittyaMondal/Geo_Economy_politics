"""
Local SQLite Event Knowledge Base and Treaty Archive.
Provides zero-dependency persistent storage for historical events, bilateral treaties,
border agreements, and multilateral baseline communique clauses for negative-space diffing.
"""

import contextlib
import os
import sqlite3
import time
from typing import Any, Dict, Generator, List, Optional


class EventStore:
    """Manages local SQLite database for historical events and baseline treaties."""

    DEFAULT_DB_PATH = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "data",
        "events.db"
    )

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or os.environ.get("GEO_ENGINE_DB_PATH") or self.DEFAULT_DB_PATH
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        if not self.is_initialized():
            self.initialize_schema_and_seed()
        self._ensure_migrations()

    def _ensure_migrations(self) -> None:
        """Applies schema migrations for tables added in later phases."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS lens_epistemic_reliability (
                    lens_name TEXT PRIMARY KEY,
                    total_evaluations INTEGER DEFAULT 0,
                    brier_error_sum REAL DEFAULT 0.0,
                    reliability_multiplier REAL DEFAULT 1.0,
                    last_calibrated_at TEXT
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS wargame_sessions (
                    session_id TEXT PRIMARY KEY,
                    initiator TEXT,
                    target TEXT,
                    domain TEXT,
                    action_summary TEXT,
                    counter_summary TEXT,
                    backlash_summary TEXT,
                    equilibrium_payoff REAL,
                    status TEXT,
                    created_at TEXT
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS wargame_turns (
                    turn_id TEXT PRIMARY KEY,
                    session_id TEXT,
                    turn_number INTEGER,
                    actor TEXT,
                    domain TEXT,
                    action_description TEXT,
                    severity REAL,
                    payoff REAL,
                    details_json TEXT,
                    created_at TEXT,
                    FOREIGN KEY(session_id) REFERENCES wargame_sessions(session_id)
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS prediction_scorecard (
                    prediction_id TEXT PRIMARY KEY,
                    session_label TEXT,
                    prediction_text TEXT NOT NULL,
                    domain TEXT,
                    lens_source TEXT,
                    forecast_probability REAL,
                    time_horizon_months INTEGER,
                    created_at TEXT NOT NULL,
                    outcome_recorded_at TEXT,
                    outcome_description TEXT,
                    outcome_binary INTEGER,
                    brier_score REAL,
                    status TEXT DEFAULT 'PENDING'
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS diagnostic_longitudinal_records (
                    encounter_id TEXT PRIMARY KEY,
                    session_id TEXT,
                    entity_or_subject TEXT NOT NULL,
                    query_text TEXT,
                    primary_epistemic_tier TEXT,
                    confidence REAL,
                    reality_ratio REAL,
                    propaganda_ratio REAL,
                    anomalies_detected TEXT,
                    brier_score REAL,
                    diagnostic_timestamp TEXT NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS media_audit_jobs (
                    job_id TEXT PRIMARY KEY,
                    source_url TEXT NOT NULL,
                    status TEXT NOT NULL,
                    progress_pct REAL DEFAULT 0.0,
                    result_json TEXT,
                    error_message TEXT,
                    created_at TEXT NOT NULL,
                    completed_at TEXT
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS claim_distillations (
                    claim_id TEXT PRIMARY KEY,
                    source_speaker TEXT,
                    raw_statement TEXT NOT NULL,
                    proposition TEXT NOT NULL,
                    epistemic_tier TEXT NOT NULL,
                    verification_status TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    statutory_citation TEXT,
                    fiscal_metric TEXT,
                    causal_relation TEXT,
                    recommended_action TEXT,
                    created_at TEXT NOT NULL
                )
            """)

            # Seed Phase 53 baseline statutory clauses idempotently
            cursor.executemany("""
                INSERT OR IGNORE INTO historical_treaty_clauses
                (clause_id, treaty_name, year, category, clause_text, is_mandatory_baseline, omission_significance)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, [
                (
                    "CLAUSE-1991-POWA",
                    "Places of Worship (Special Provisions) Act, 1991",
                    1991,
                    "statutory_asymmetry",
                    "Sections 3 & 4: Declares that the religious character of a place of worship existing on August 15, 1947 shall continue to be the same as it existed on that day, prohibiting conversion and abating all pending suits or proceedings.",
                    1,
                    "Statutory freeze on civilizational reclamation; creates asymmetric legal immunity for medieval temple demolitions while preempting judicial adjudication."
                ),
                (
                    "CLAUSE-1995-WAQF",
                    "Waqf Act, 1995",
                    1995,
                    "statutory_asymmetry",
                    "Section 40: Vests Waqf Boards with unilateral power to determine whether a property is waqf property, placing burden of proof on the adverse claimant and barring ordinary civil court jurisdiction under Section 85 in favor of specialized tribunals.",
                    1,
                    "Asymmetric property acquisition and jurisdictional barrier exempt from standard civil procedural code."
                ),
                (
                    "CLAUSE-1951-HRCE",
                    "Hindu Religious and Charitable Endowments (HRCE) Framework",
                    1951,
                    "statutory_asymmetry",
                    "State statutory oversight mechanisms authorizing executive officers to manage Hindu temple administrations and surplus treasury funds, whereas minority religious institutions are constitutionally protected under Article 30.",
                    1,
                    "Structural financial asymmetry and state appropriation of indigenous religious endowments without reciprocal minority institution regulation."
                )
            ])

            # Seed Phase 53 Middle East verified telemetry events idempotently
            cursor.executemany("""
                INSERT OR IGNORE INTO events
                (event_id, date, title, actor, region, category, summary, civilizational_significance)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, [
                (
                    "HIST-2024-REDSEA-CHOKE",
                    "2024-01-15",
                    "Bab el-Mandeb Houthi Naval Interdiction & Red Sea Corridor Disruption",
                    "Ansar Allah (Houthis), US Navy, Global Shipping",
                    "Red Sea / Middle East",
                    "maritime_chokepoint",
                    "Asymmetric anti-ship ballistic missile and drone attacks forced container shipping around Cape of Good Hope, dropping Suez Canal transit revenues by 55-60% ($4B+ annual loss to Egypt) and inflating European freight premia.",
                    "Demonstrates low-cost non-state asymmetric weaponry closing a primary global energy and container choke-point, exposing Western naval escort limitations."
                ),
                (
                    "HIST-2024-SYRIA-COLLAPSE",
                    "2024-12-08",
                    "Fall of the Assad Regime in Syria & Iranian Axis Rupture",
                    "HTS / Syrian Opposition, Syrian Armed Forces, Russia, Iran",
                    "Middle East / Levant",
                    "regime_change",
                    "Rapid blitz offensive by Hayat Tahrir al-Sham captured Damascus and ended 53 years of Assad rule, forcing Bashar al-Assad's departure to Moscow and collapsing Iranian Axis of Resistance overland logistics to Hezbollah.",
                    "Historic geopolitical fracture in the northern Levant, destabilizing Russian Mediterranean naval basing at Tartus and severing Tehran's contiguous land bridge."
                ),
                (
                    "HIST-2024-ISRAEL-IRAN-AIR",
                    "2024-10-26",
                    "Operation Days of Repentance & Strategic S-300 Degradation in Iran",
                    "Israeli Air Force, Islamic Republic of Iran",
                    "Middle East",
                    "kinetic_counter_air",
                    "IAF executed long-range precision strikes destroying Iran's remaining Russian-supplied S-300 strategic surface-to-air missile batteries and solid-fuel mixing facilities, establishing conventional air dominance over Iranian airspace.",
                    "Neutralized Iran's strategic air defense umbrella, demonstrating conventional technological asymmetry and shifting deterrence calculations across the Persian Gulf."
                ),
                (
                    "HIST-2026-VANDYKE-CHIN-DRONE",
                    "2026-09-18",
                    "Mizoram-Myanmar Border PMC Infiltration & Default Bail Off-Ramp",
                    "Matthew VanDyke (SOLI), Ukrainian Nationals, NIA, Chin National Army",
                    "Northeast India / Myanmar Chin State",
                    "hybrid_warfare",
                    "Arrest of American PMC operator Matthew VanDyke and 6 Ukrainian drone trainers in Mizoram for cross-border FPV drone training to Chin anti-Junta rebels; granted Section 167(2) default bail after 180-day UAPA deadline lapsed and Foreigners Act compounding (Sections 21/23).",
                    "Demonstrates the intersection of transnational mercenary drone tech proliferation, sub-national tribal kinship corridors, and managed judicial off-ramps under Section 188 CrPC extraterritorial limits."
                ),
                (
                    "HIST-1971-CHICKENS-NECK-SECURITY",
                    "1971-12-03",
                    "Siliguri Corridor & Eastern Command Preemption (1971 War)",
                    "Indian Army (Eastern Command)",
                    "Siliguri Corridor / Eastern Sector",
                    "chokepoint_security",
                    "Indian Armed Forces secured the 22km Siliguri Corridor ('Chicken's Neck') against potential Pakistani counter-thrusts and Chinese intervention in the Chumbi Valley, guaranteeing rear-area logistics during the liberation of Bangladesh.",
                    "Demonstrated the strategic doctrine of offensive-defensive preemption to neutralize geographic bottleneck vulnerabilities."
                ),
                (
                    "HIST-2017-DOKLAM-CHUMBI",
                    "2017-06-16",
                    "Doklam Plateau Standoff & Chumbi Valley Flank Protection",
                    "Indian Army, PLA",
                    "Doklam / Bhutan / Chumbi Valley",
                    "chokepoint_security",
                    "73-day military standoff preventing Chinese road construction through Doklam toward the Jampheri Ridge, which directly overlooked India's narrow Siliguri Corridor.",
                    "Asserted sovereign commitment to neighbor defense pacts and protected the Siliguri vulnerable logistics flank from PLA tactical observation and artillery interdiction."
                ),
                (
                    "HIST-2019-TURKEY-F35-CAATSA",
                    "2019-07-17",
                    "Expulsion of Turkey from F-35 Joint Strike Fighter Program",
                    "US Department of Defense, Republic of Turkey",
                    "Global / NATO",
                    "avionics_sovereignty",
                    "US formally suspended and expelled NATO ally Turkey from the F-35 fighter program following its procurement of the Russian S-400 Triumf missile system under CAATSA, citing risks of Russian radar data exploitation of F-35 stealth profiles.",
                    "Archetypal evidence of digital leash enforcement, sovereign exclusion, and cloud-tethered supply chain interdiction in 5th-generation combat avionics."
                ),
                (
                    "HIST-2024-TARANG-SHAKTI-JODHPUR",
                    "2024-09-01",
                    "Exercise Tarang Shakti Phase II (Jodhpur) & 5th-Gen Stealth Demonstrations",
                    "Indian Air Force, US Air Force, Allied Air Forces",
                    "Jodhpur / Indo-Pacific",
                    "military_readiness",
                    "IAF hosted its largest multilateral air exercise with USAF F-35A fighters and allied jets operating at Jodhpur Air Base; 5th-generation stealth fighters deployed Luneburg radar reflectors to deliberately mask authentic combat radar cross-sections.",
                    "Highlighted electronic warfare sovereignty, mission computer data segregation, and tactical interoperability without compromising indigenous radar and stealth telemetry."
                )
            ])

            # Seed Phase 78 Extraterritorial Jurisdiction clause idempotently
            cursor.execute("""
                INSERT OR IGNORE INTO historical_treaty_clauses
                (clause_id, treaty_name, year, category, clause_text, is_mandatory_baseline, omission_significance)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                "CLAUSE-CRPC-188-EXTRATERRITORIAL",
                "Code of Criminal Procedure 1973 Section 188 / BNSS Section 208",
                1973,
                "extraterritorial_jurisdiction",
                "Offences committed outside India: When an offence is committed outside India by a citizen of India or by a foreign national, no such offence shall be inquired into or tried in India without the previous sanction of the Central Government.",
                1,
                "Statutory barrier requiring Central Government sanction for extraterritorial offences, serving as a legal and diplomatic gatekeeper for sovereign prosecutions of foreign nationals."
            ))

            # Seed Phase 59 Dark History & Cognitive Warfare milestones idempotently
            cursor.executemany("""
                INSERT OR IGNORE INTO historical_anniversaries
                (anniversary_id, month, day, year, event_title, region, historical_summary, strategic_mirror_significance)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, [
                (
                    "ANNIV-1920-WATSON-JWT",
                    10,
                    1,
                    1920,
                    "John B. Watson Joins J. Walter Thompson (JWT)",
                    "Global / USA",
                    "Behaviorist psychologist John B. Watson joined the J. Walter Thompson advertising agency, formally applying emotional and fear conditioning to commercial advertising and product marketing.",
                    "Birth of modern commercial psychological warfare, weaponizing infant hygiene, germ fear, and maternal anxiety into consumer demand."
                ),
                (
                    "ANNIV-1928-WATSON-INFANT",
                    3,
                    1,
                    1928,
                    "Watson Publishes 'Psychological Care of Infant and Child'",
                    "Global / USA",
                    "John B. Watson published his seminal parenting manual prescribing rigid emotional detachment, warning mothers against hugging or kissing infants to avoid 'spoiling' them.",
                    "Institutionalization of cold infant isolation doctrine, replacing maternal bonding with commodified schedules and nursery appliances."
                ),
                (
                    "ANNIV-1928-BERNAYS-PROPAGANDA",
                    11,
                    15,
                    1928,
                    "Edward Bernays Publishes 'Propaganda' & Torches of Freedom",
                    "Global / USA",
                    "Edward Bernays published 'Propaganda', codifying the 'engineering of consent' and later executing the 'Torches of Freedom' campaign linking women's liberation to cigarette consumption.",
                    "Foundational playbook for modern public relations, psychological manipulation, and manufacturing social consent for corporate cartels."
                ),
                (
                    "ANNIV-1953-MKULTRA-MOCKINGBIRD",
                    4,
                    13,
                    1953,
                    "CIA Project MKUltra & Operation Mockingbird",
                    "Global / USA",
                    "CIA launched Project MKUltra (mind control and behavioral modification experiments) and Operation Mockingbird (subterranean infiltration of domestic and international media organizations).",
                    "Institutionalization of deep-state psychological operations, weaponized media narratives, and covert cognitive warfare."
                ),
                (
                    "ANNIV-1981-WHO-INFANT-FORMULA",
                    5,
                    21,
                    1981,
                    "WHO International Code of Marketing of Breast-milk Substitutes",
                    "Global",
                    "World Health Assembly adopted landmark International Code (WHA34.22) restricting aggressive marketing of infant formula, following global boycotts against commercial exploitation of maternal anxiety in developing nations.",
                    "Landmark sovereign multilateral confrontation against transnational corporate capture of infant health and fear-based marketing."
                )
            ])

            # Seed Phase 60 Chronology Anchors idempotently
            cursor.executemany("""
                INSERT OR IGNORE INTO historical_anniversaries
                (anniversary_id, month, day, year, event_title, region, historical_summary, strategic_mirror_significance)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, [
                (
                    "CHRONO-5561BCE-OAK",
                    10,
                    16,
                    -5561,
                    "Nilesh Oak 5561 BCE Timeline (Arundhati-Vasistha Model)",
                    "Ancient Bharat",
                    "Dates the Mahabharata War to 5561 BCE based on the Arundhati walking ahead of Vasistha (Mizar-Alcor) observation in Bhishma Parva, calculating an epoch window between 11,091 BCE and 4508 BCE.",
                    "Benchmark astronomical retro-calculation hypothesis; subject to material culture collision with Mesolithic/early Neolithic lithic archaeological strata."
                ),
                (
                    "CHRONO-3067BCE-ACHAR",
                    11,
                    22,
                    -3067,
                    "Dr. Narahari Achar 3067 BCE Timeline (Saturn-Rohini BORI Model)",
                    "Ancient Bharat",
                    "Dates the Mahabharata War to 3067 BCE based on the BORI Critical Edition common archetype, Saturn at Rohini, Jupiter at Vishakha, and twin eclipses within 13 days.",
                    "Multi-pillar benchmark exhibiting low astronomical degeneracy and high congruence with Saraswati perennial flow and Early Bronze Age urban transitions."
                ),
                (
                    "CHRONO-3102BCE-ARYABHATA",
                    2,
                    18,
                    -3102,
                    "Traditional Aryabhata & Aihole Inscription 3102 BCE Kali Yuga Epoch",
                    "Ancient Bharat",
                    "Traditional civilizational anchor calculating the start of Kali Yuga at 3102 BCE, epigraphically corroborated by the Aihole Inscription of Pulakeshin II (634 CE) referencing 3735 elapsed years.",
                    "Civilizational baseline anchor uniting Puranic dynastic chronologies with planetary mean-motion calculations."
                ),
                (
                    "CHRONO-1000BCE-PGW",
                    1,
                    1,
                    -1000,
                    "Archaeological Survey of India Painted Grey Ware (PGW) 1000 BCE Model",
                    "Ancient Bharat",
                    "Dates the epic to the 10th-9th century BCE based on Painted Grey Ware (PGW) strata, early iron arrowheads at Hastinapur/Kurukshetra, and the flood layer described in Puranic texts.",
                    "Archaeologically grounded material culture anchor; exhibits low hydro-geological coherence due to complete prior desiccation of River Saraswati by 1900 BCE."
                ),
                (
                    "CHRONO-2000BCE-SINAULI",
                    1,
                    1,
                    -2000,
                    "Sinauli Bronze Age Necropolis (OCP / Copper Hoard Culture)",
                    "Ancient Bharat / Ganga-Yamuna Doab",
                    "Excavations at Sinauli (Baghpat, UP) revealed elite warrior burials with copper-inlaid solid-disk wheeled carts, antennae swords, shields, and four-legged coffins dating to 2000-1800 BCE via calibrated C14.",
                    "Stratigraphical and material culture anchor establishing indigenous Bronze Age wheeled transport and warrior aristocracy in northern India; concordant with Rigveda 10.18 inhumation rites."
                ),
                (
                    "CHRONO-2500BCE-RAKHIGARHI",
                    1,
                    1,
                    -2500,
                    "Rakhigarhi Mature Harappan Paleogenomic Anchor",
                    "Ancient Bharat / Ghaggar-Hakra Basin",
                    "Ancient DNA from Mature IVC female skeleton demonstrating absence of Central Asian Steppe pastoralist ancestry (R1a-Z93) and presence of Iranian farmer-related and Ancient Ancestral South Indian (AASI) lineage.",
                    "Crucial paleogenomic baseline establishing genetic continuity in South Asia and disproving catastrophic population replacement models."
                )
            ])

            # Seed Phase 63 Cosmic Chronology & Canonical Scriptural Benchmarks idempotently
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cosmic_chronology_benchmarks (
                    benchmark_id TEXT PRIMARY KEY,
                    category TEXT,
                    canonical_source TEXT,
                    primary_citation TEXT,
                    temporal_epoch TEXT,
                    duration_years REAL,
                    physical_basis TEXT,
                    debunk_notes TEXT
                )
            """)
            cursor.executemany("""
                INSERT OR IGNORE INTO cosmic_chronology_benchmarks
                (benchmark_id, category, canonical_source, primary_citation, temporal_epoch, duration_years, physical_basis, debunk_notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, [
                (
                    "COSMIC-KALIYUGA-CANONICAL",
                    "yuga_cycle",
                    "Surya Siddhanta & Classical Puranic Corpus",
                    "Surya Siddhanta (1.15-17), Aryabhatiya (Kalakriyapada), Vishnu Purana (1.3), Bhagavata Purana (12.2), Mahabharata (Vana Parva 188)",
                    "3102-02-18 BCE",
                    432000.0,
                    "Planetary conjunction at Mesha (Aries 0 deg) and solar mean motion.",
                    "Directly refutes modern 5,000-year truncation claims; in 2026 CE only ~5,127 years have elapsed (~1.19%), leaving 426,873 years remaining."
                ),
                (
                    "EPIGRAPH-634CE-AIHOLE",
                    "epigraphic_anchor",
                    "Aihole Inscription of Pulakeshin II",
                    "Meguti Jain Temple Inscription, Aihole (composed by Ravikirti, Saka 556)",
                    "634 CE",
                    3735.0,
                    "Epigraphic stone inscription recording 3,735 elapsed years since the Bharata War.",
                    "Provides immutable epigraphic confirmation anchoring the Kali Yuga commencement to February 3102 BCE."
                ),
                (
                    "TEMPLE-1150CE-PURI-JAGANNATH",
                    "temple_chronicle",
                    "Puri Jagannath Temple Madala Panji & ASI Records",
                    "Madala Panji Temple Chronicles & Archaeological Survey of India Conservation Records",
                    "1150 CE",
                    875.0,
                    "214-ft Khondalite sandstone tower exposed to severe marine saline air, humid expansion, and Category 4/5 tropical cyclones.",
                    "Structural stone displacements documented since 1842 are natural coastal conservation issues, not supernatural apocalypses."
                ),
                (
                    "DEBUNK-1997-NOSTRADAMUS-TWINTOWERS",
                    "hoax_registry",
                    "Neil Marshall Hoax & French Philological Analysis",
                    "Neil Marshall (Brock University 1997 Essay); Nostradamus Les Propheties (1555)",
                    "1997 CE",
                    0.0,
                    "Internet chain letter authored by a Canadian student in 1997 demonstrating confirmation bias, falsely attributed to Nostradamus after 9/11.",
                    "Nostradamus never wrote 'birds of iron' or 'two brothers'. The quatrain 'Hister' refers to the Latin name for the Lower Danube River (Ister), not Adolf Hitler."
                ),
                (
                    "DEBUNK-1970-MALIKA-KASHINATH",
                    "hoax_registry",
                    "Modern Commercial Chapbook Press",
                    "Pandit Kashinath Mishra Bazaar Pamphlets (Cuttack/Puri); Odisha State Museum Palm-Leaf Archives",
                    "1970-1999 CE",
                    0.0,
                    "Late 20th-century commercial bazaar pamphlet interpolations printed in regional press.",
                    "Pre-1947 palm-leaf manuscripts at Odisha State Museum and Prachi Valley contain zero references to modern political figures, Pakistan partition, or Vajpayee's 13-day rule."
                )
            ])
            conn.commit()
        # Idempotently ensure all foundational anniversary, clause, and event seeds are present
        self.initialize_schema_and_seed()

    def is_initialized(self) -> bool:
        """Checks if the SQLite database is already initialized with essential baseline tables."""
        if not os.path.exists(self.db_path) or os.path.getsize(self.db_path) == 0:
            return False
        try:
            with sqlite3.connect(self.db_path, timeout=5.0) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT count(*) FROM sqlite_master WHERE type='table' AND name='historical_treaty_clauses'"
                )
                row = cursor.fetchone()
                return bool(row and row[0] > 0)
        except Exception:
            return False

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("PRAGMA journal_mode;")
        current_mode = cursor.fetchone()
        if current_mode and current_mode[0].lower() != "wal":
            conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA busy_timeout=30000;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        conn.execute("PRAGMA cache_size=-64000;")
        return conn

    @contextlib.contextmanager
    def transaction_scope(self, max_retries: int = 3, retry_delay: float = 0.05) -> Generator[sqlite3.Connection, None, None]:
        """Provides a thread-safe transaction scope with automatic exponential backoff on database lock."""
        attempt = 0
        last_error = None
        while attempt < max_retries:
            try:
                conn = self._get_connection()
                try:
                    yield conn
                    conn.commit()
                    return
                except Exception:
                    conn.rollback()
                    raise
                finally:
                    conn.close()
            except sqlite3.OperationalError as e:
                if "locked" in str(e).lower() or "busy" in str(e).lower():
                    attempt += 1
                    last_error = e
                    time.sleep(retry_delay * (2 ** attempt))
                else:
                    raise
        if last_error:
            raise last_error

    def initialize_schema_and_seed(self) -> None:
        """Initializes database tables and seeds foundational historical baselines."""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # 1. Historical Events Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS events (
                    event_id TEXT PRIMARY KEY,
                    date TEXT,
                    title TEXT,
                    actor TEXT,
                    region TEXT,
                    category TEXT,
                    summary TEXT,
                    civilizational_significance TEXT
                )
            """)

            # 2. Historical Treaty & Baseline Communique Clauses Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS historical_treaty_clauses (
                    clause_id TEXT PRIMARY KEY,
                    treaty_name TEXT,
                    year INTEGER,
                    category TEXT,
                    clause_text TEXT,
                    is_mandatory_baseline INTEGER DEFAULT 1,
                    omission_significance TEXT
                )
            """)

            # 3. Historical Turning Points & Anniversaries Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS historical_anniversaries (
                    anniversary_id TEXT PRIMARY KEY,
                    month INTEGER,
                    day INTEGER,
                    year INTEGER,
                    event_title TEXT,
                    region TEXT,
                    historical_summary TEXT,
                    strategic_mirror_significance TEXT
                )
            """)

            # 4. Active Calibrated Forecast Resolution Ledger
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS forecast_ledger (
                    forecast_id TEXT PRIMARY KEY,
                    created_at TEXT,
                    target_date TEXT,
                    event_name TEXT,
                    hypothesis TEXT,
                    predicted_probability REAL,
                    confidence_interval_low REAL,
                    confidence_interval_high REAL,
                    epistemic_basis TEXT,
                    actual_outcome INTEGER,
                    brier_score REAL,
                    status TEXT DEFAULT 'ACTIVE'
                )
            """)

            # 5. Dynamic Lens Epistemic Reliability Table (Bayesian Calibration)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS lens_epistemic_reliability (
                    lens_name TEXT PRIMARY KEY,
                    total_evaluations INTEGER DEFAULT 0,
                    brier_error_sum REAL DEFAULT 0.0,
                    reliability_multiplier REAL DEFAULT 1.0,
                    last_calibrated_at TEXT
                )
            """)

            # 6. Persistent Wargame Campaign Sessions & Multi-Turn State
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS wargame_sessions (
                    session_id TEXT PRIMARY KEY,
                    initiator TEXT,
                    target TEXT,
                    domain TEXT,
                    action_summary TEXT,
                    counter_summary TEXT,
                    backlash_summary TEXT,
                    equilibrium_payoff REAL,
                    status TEXT,
                    created_at TEXT
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS wargame_turns (
                    turn_id TEXT PRIMARY KEY,
                    session_id TEXT,
                    turn_number INTEGER,
                    actor TEXT,
                    domain TEXT,
                    action_description TEXT,
                    severity REAL,
                    payoff REAL,
                    details_json TEXT,
                    created_at TEXT,
                    FOREIGN KEY(session_id) REFERENCES wargame_sessions(session_id)
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS prediction_scorecard (
                    prediction_id TEXT PRIMARY KEY,
                    session_label TEXT,
                    prediction_text TEXT NOT NULL,
                    domain TEXT,
                    lens_source TEXT,
                    forecast_probability REAL,
                    time_horizon_months INTEGER,
                    created_at TEXT NOT NULL,
                    outcome_recorded_at TEXT,
                    outcome_description TEXT,
                    outcome_binary INTEGER,
                    brier_score REAL,
                    status TEXT DEFAULT 'PENDING'
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS diagnostic_longitudinal_records (
                    encounter_id TEXT PRIMARY KEY,
                    session_id TEXT,
                    entity_or_subject TEXT NOT NULL,
                    query_text TEXT,
                    primary_epistemic_tier TEXT,
                    confidence REAL,
                    reality_ratio REAL,
                    propaganda_ratio REAL,
                    anomalies_detected TEXT,
                    brier_score REAL,
                    diagnostic_timestamp TEXT NOT NULL
                )
            """)

            # 7. Cosmic Chronology & Canonical Scriptural Benchmarks Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cosmic_chronology_benchmarks (
                    benchmark_id TEXT PRIMARY KEY,
                    category TEXT,
                    canonical_source TEXT,
                    primary_citation TEXT,
                    temporal_epoch TEXT,
                    duration_years REAL,
                    physical_basis TEXT,
                    debunk_notes TEXT
                )
            """)

            # 8. Asynchronous Media Audit Jobs Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS media_audit_jobs (
                    job_id TEXT PRIMARY KEY,
                    source_url TEXT NOT NULL,
                    status TEXT NOT NULL,
                    progress_pct REAL DEFAULT 0.0,
                    result_json TEXT,
                    error_message TEXT,
                    created_at TEXT NOT NULL,
                    completed_at TEXT
                )
            """)

            # Seed foundational historical events
            events_seed = [

                (
                    "HIST-1971-INDO-SOVIET",
                    "1971-08-09",
                    "Indo-Soviet Treaty of Peace, Friendship and Cooperation",
                    "India, USSR",
                    "South Asia / Eurasia",
                    "strategic_treaty",
                    "Article IX provided mutual consultations in the event of an attack, acting as an existential diplomatic deterrent against external coalition interventions during the 1971 Bangladesh Liberation War.",
                    "Demonstrated Kautilyan Mitra dynamics: strategic alignment without surrender of civilizational sovereignty."
                ),
                (
                    "HIST-1993-BPTA",
                    "1993-09-07",
                    "Border Peace and Tranquility Agreement (BPTA)",
                    "India, China",
                    "Himalayan Frontier",
                    "border_security",
                    "Institutionalized adherence to the Line of Actual Control (LAC) and committed both sides to troop reductions to mutually agreed ceilings.",
                    "Sovereign redline defining the tactical status quo prior to Chinese unilateral infrastructure shifts."
                ),
                (
                    "HIST-1996-CBM",
                    "1996-11-29",
                    "Agreement on Confidence Building Measures Along the LAC",
                    "India, China",
                    "Himalayan Frontier",
                    "military_protocols",
                    "Prohibited opening fire, using hazardous chemicals, or conducting major tactical exercises within 2km of the LAC.",
                    "Crucial physical guardrail whose violation at Galwan (2020) precipitated permanent strategic decoupling."
                ),
                (
                    "HIST-2024-RAM-MANDIR",
                    "2024-01-22",
                    "Ayodhya Ram Mandir Pran Pratishtha & Civilizational Consolidation",
                    "India",
                    "Domestic / Global Indian Ocean",
                    "civilizational_milestone",
                    "Formally inaugurated India's post-colonial civilizational reclamation, re-anchoring foreign policy in Rajdharma, Yogakshema, and Vasudhaiva Kutumbakam rather than Westphalian mimicry.",
                    "The theological and moral anchor for an assertive, non-aligned Indian civilization-state."
                ),
                (
                    "HIST-2024-DHAKA-TRANSITION",
                    "2024-08-05",
                    "Bangladesh Political Transition (Sheikh Hasina Exit to Interim Council)",
                    "Bangladesh, India",
                    "South Asian Neighborhood",
                    "regime_change",
                    "Resignation and departure of Prime Minister Sheikh Hasina following student demonstrations; formation of interim council under Muhammad Yunus.",
                    "Strains India's eastern security perimeter, rail transit treaties, and Chicken's Neck / Siliguri Corridor logistics."
                ),
                (
                    "HIST-2026-ARABIAN-SEA-STANDOFF",
                    "2026-09-15",
                    "North Arabian Sea Maritime Grey-Zone Ramming Incident",
                    "Pakistan Navy (PNS Hunain), Indian Navy",
                    "North Arabian Sea / Indian Ocean",
                    "maritime_grey_zone",
                    "Pakistani corvette PNS Hunain executed aggressive bow crossing and collided with an Indian Navy warship on surveillance in international waters, breaching Article 10 of the 1991 Bilateral Agreement and COLREGs Rule 8.",
                    "Demonstrates importation of Chinese South China Sea grey-zone tactics into the Arabian Sea to probe Indian Rules of Engagement below kinetic threshold."
                ),
                (
                    "HIST-2022-RBI-SRVA-FRAMEWORK",
                    "2022-07-11",
                    "RBI Framework for International Trade Settlement in Indian Rupees",
                    "Reserve Bank of India (RBI)",
                    "Global / South Asia",
                    "monetary_architecture",
                    "RBI issued landmark circular permitting trade settlement in INR via Special Rupee Vostro Accounts (SRVAs), establishing capital recycling pathways into sovereign debt (G-Secs) and laying foundation for bilateral de-dollarization.",
                    "Operationalizes Kautilyan Kosha sovereignty: insulating foreign trade from extraterritorial SWIFT/dollar sanctions."
                ),
                (
                    "HIST-2024-REDSEA-CHOKE",
                    "2024-01-15",
                    "Bab el-Mandeb Houthi Naval Interdiction & Red Sea Corridor Disruption",
                    "Ansar Allah (Houthis), US Navy, Global Shipping",
                    "Red Sea / Middle East",
                    "maritime_chokepoint",
                    "Asymmetric anti-ship ballistic missile and drone attacks forced container shipping around Cape of Good Hope, dropping Suez Canal transit revenues by 55-60% ($4B+ annual loss to Egypt) and inflating European freight premia.",
                    "Demonstrates low-cost non-state asymmetric weaponry closing a primary global energy and container choke-point, exposing Western naval escort limitations."
                ),
                (
                    "HIST-2024-SYRIA-COLLAPSE",
                    "2024-12-08",
                    "Fall of the Assad Regime in Syria & Iranian Axis Rupture",
                    "HTS / Syrian Opposition, Syrian Armed Forces, Russia, Iran",
                    "Middle East / Levant",
                    "regime_change",
                    "Rapid blitz offensive by Hayat Tahrir al-Sham captured Damascus and ended 53 years of Assad rule, forcing Bashar al-Assad's departure to Moscow and collapsing Iranian Axis of Resistance overland logistics to Hezbollah.",
                    "Historic geopolitical fracture in the northern Levant, destabilizing Russian Mediterranean naval basing at Tartus and severing Tehran's contiguous land bridge."
                ),
                (
                    "HIST-2024-ISRAEL-IRAN-AIR",
                    "2024-10-26",
                    "Operation Days of Repentance & Strategic S-300 Degradation in Iran",
                    "Israeli Air Force, Islamic Republic of Iran",
                    "Middle East",
                    "kinetic_counter_air",
                    "IAF executed long-range precision strikes destroying Iran's remaining Russian-supplied S-300 strategic surface-to-air missile batteries and solid-fuel mixing facilities, establishing conventional air dominance over Iranian airspace.",
                    "Neutralized Iran's strategic air defense umbrella, demonstrating conventional technological asymmetry and shifting deterrence calculations across the Persian Gulf."
                ),
                (
                    "HIST-2026-VANDYKE-CHIN-DRONE",
                    "2026-09-18",
                    "Mizoram-Myanmar Border PMC Infiltration & Default Bail Off-Ramp",
                    "Matthew VanDyke (SOLI), Ukrainian Nationals, NIA, Chin National Army",
                    "Northeast India / Myanmar Chin State",
                    "hybrid_warfare",
                    "Arrest of American PMC operator Matthew VanDyke and 6 Ukrainian drone trainers in Mizoram for cross-border FPV drone training to Chin anti-Junta rebels; granted Section 167(2) default bail after 180-day UAPA deadline lapsed and Foreigners Act compounding (Sections 21/23).",
                    "Demonstrates the intersection of transnational mercenary drone tech proliferation, sub-national tribal kinship corridors, and managed judicial off-ramps under Section 188 CrPC extraterritorial limits."
                ),
                (
                    "HIST-2000BCE-SINAULI-OCP",
                    "-2000-01-01",
                    "Sinauli Bronze Age Necropolis & Martial Culture (2000-1800 BCE)",
                    "Archaeological Survey of India (ASI), BSIP Radiocarbon",
                    "Ganga-Yamuna Doab / Western UP",
                    "archaeological_milestone",
                    "Excavation in Baghpat yielded 3 copper-inlaid solid-disk wheeled carts, 8 four-legged anthropomorphic coffins, antennae swords, shields, and warrior burials dating to 2000-1800 BCE via calibrated C14.",
                    "Material proof of an organized indigenous elite warrior society with copper metallurgy and wheeled transports in northern India prior to conventional Steppe pastoralist horizons; concordant with Rigveda 10.18 inhumation."
                ),
                (
                    "HIST-2500BCE-RAKHIGARHI-ADNA",
                    "-2500-01-01",
                    "Rakhigarhi Mature Harappan Paleogenomic Baseline (c. 2500 BCE)",
                    "Cell 2019 / Prof. Vasant Shinde, David Reich et al.",
                    "Ghaggar-Hakra Basin / Haryana",
                    "paleogenomics_milestone",
                    "Ancient DNA analysis of Mature IVC female skeleton from Rakhigarhi demonstrating complete absence of Central Asian Steppe pastoralist ancestry (R1a-Z93) and presence of Iranian farmer-related and Ancient Ancestral South Indian (AASI) lineage.",
                    "Foundational paleogenomic baseline establishing genetic continuity in South Asia and disproving catastrophic population replacement."
                ),
                (
                    "HIST-1000BCE-HASTINAPUR-PGW",
                    "-1000-01-01",
                    "Hastinapur Painted Grey Ware (PGW) Stratigraphic Horizon (c. 1000-800 BCE)",
                    "Prof. B.B. Lal / Archaeological Survey of India",
                    "Upper Ganga Basin / Western UP",
                    "stratigraphy_milestone",
                    "Excavation by Prof. B.B. Lal establishing PGW strata with iron metallurgy, horse remains, and river flood layer coinciding with the Puranic transfer of the Kuru capital from Hastinapur to Kaushambi under King Nichakshu.",
                    "Key stratigraphical anchor linking Early Iron Age material culture with traditional Mahabharata geographic topography."
                ),
                (
                    "HIST-1971-CHICKENS-NECK-SECURITY",
                    "1971-12-03",
                    "Siliguri Corridor & Eastern Command Preemption (1971 War)",
                    "Indian Army (Eastern Command)",
                    "Siliguri Corridor / Eastern Sector",
                    "chokepoint_security",
                    "Indian Armed Forces secured the 22km Siliguri Corridor ('Chicken's Neck') against potential Pakistani counter-thrusts and Chinese intervention in the Chumbi Valley, guaranteeing rear-area logistics during the liberation of Bangladesh.",
                    "Demonstrated the strategic doctrine of offensive-defensive preemption to neutralize geographic bottleneck vulnerabilities."
                ),
                (
                    "HIST-2017-DOKLAM-CHUMBI",
                    "2017-06-16",
                    "Doklam Plateau Standoff & Chumbi Valley Flank Protection",
                    "Indian Army, PLA",
                    "Doklam / Bhutan / Chumbi Valley",
                    "chokepoint_security",
                    "73-day military standoff preventing Chinese road construction through Doklam toward the Jampheri Ridge, which directly overlooked India's narrow Siliguri Corridor.",
                    "Asserted sovereign commitment to neighbor defense pacts and protected the Siliguri vulnerable logistics flank from PLA tactical observation and artillery interdiction."
                ),
                (
                    "HIST-2019-TURKEY-F35-CAATSA",
                    "2019-07-17",
                    "Expulsion of Turkey from F-35 Joint Strike Fighter Program",
                    "US Department of Defense, Republic of Turkey",
                    "Global / NATO",
                    "avionics_sovereignty",
                    "US formally suspended and expelled NATO ally Turkey from the F-35 fighter program following its procurement of the Russian S-400 Triumf missile system under CAATSA, citing risks of Russian radar data exploitation of F-35 stealth profiles.",
                    "Archetypal evidence of digital leash enforcement, sovereign exclusion, and cloud-tethered supply chain interdiction in 5th-generation combat avionics."
                ),
                (
                    "HIST-2024-TARANG-SHAKTI-JODHPUR",
                    "2024-09-01",
                    "Exercise Tarang Shakti Phase II (Jodhpur) & 5th-Gen Stealth Demonstrations",
                    "Indian Air Force, US Air Force, Allied Air Forces",
                    "Jodhpur / Indo-Pacific",
                    "military_readiness",
                    "IAF hosted its largest multilateral air exercise with USAF F-35A fighters and allied jets operating at Jodhpur Air Base; 5th-generation stealth fighters deployed Luneburg radar reflectors to deliberately mask authentic combat radar cross-sections.",
                    "Highlighted electronic warfare sovereignty, mission computer data segregation, and tactical interoperability without compromising indigenous radar and stealth telemetry."
                )
            ]

            cursor.executemany("""
                INSERT OR IGNORE INTO events
                (event_id, date, title, actor, region, category, summary, civilizational_significance)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, events_seed)

            # Seed foundational baseline communique clauses for negative space diffing
            clauses_seed = [
                (
                    "BASE-UNSC-EXPANSION",
                    "BRICS Multi-Year Historical Baseline",
                    2023,
                    "institutional_reform",
                    "The member states reaffirm full support for the permanent membership of India, Brazil, and South Africa on the United Nations Security Council (UNSC).",
                    1,
                    "Total Chinese resistance to Indian UNSC permanent seat veto parity; omission exposes institutional capture."
                ),
                (
                    "BASE-COMMON-CURRENCY",
                    "Johannesburg Economic Summit Declarations",
                    2023,
                    "finance",
                    "Commissioning the formal feasibility and macro-economic road-map for a unified BRICS common reserve currency mechanism.",
                    1,
                    "Mundell-Fleming impossibility trilemma triggered; project quietly abandoned due to central bank resistance."
                ),
                (
                    "BASE-UNCLOS-MARITIME",
                    "Global South Maritime Governance Baseline",
                    2022,
                    "territorial",
                    "Reaffirming unwavering adherence to the 1982 UNCLOS conventions, freedom of navigation, and overflight in the South China Sea.",
                    1,
                    "Chinese maritime coercion; Beijing refuses multilateral international arbitration references."
                ),
                (
                    "BASE-CROSS-BORDER-TERROR",
                    "Goa & New Delhi Security Declarations",
                    2021,
                    "security",
                    "Zero-tolerance condemnation of state-sponsored cross-border terrorism, explicitly naming regional terror sanctuaries and FATF compliance.",
                    1,
                    "Diluted into toothless generic phrasing to shield bilateral allies and prevent bilateral disputes."
                ),
                (
                    "CLAUSE-1991-INDO-PAK-NAV-ART10",
                    "1991 India-Pakistan Agreement on Advance Notice of Military Exercises, Maneuvers and Troop Movements",
                    1991,
                    "maritime_deconfliction",
                    "Article 10: Naval vessels and submarines of the two countries shall not approach within 3 nautical miles of each other's territorial waters and shall maintain safe buffer distance during maneuvers in international waters.",
                    1,
                    "Breach of 3 nautical mile buffer distance and deliberate bow crossing constitutes maritime grey-zone provocation and sub-kinetic escalation below UN Charter Article 51 threshold."
                ),
                (
                    "CLAUSE-2022-RBI-SRVA",
                    "RBI Circular on International Trade Settlement in Indian Rupees (INR)",
                    2022,
                    "monetary_clearing",
                    "A.P. (DIR Series) Circular No. 10: Authorized Dealer Category-I banks are permitted to open Special Non-Resident Rupee (SNRR) and Special Rupee Vostro Accounts (SRVA) for partner country correspondent banks, permitting invoicing, payment, and settlement in INR, with surplus balances permitted for reinvestment in Government Securities and sovereign infrastructure.",
                    1,
                    "Statutory baseline establishing the legal mechanism for recycling bilateral non-convertible trade surpluses into domestic sovereign debt and equities."
                ),
                (
                    "CLAUSE-1991-POWA",
                    "Places of Worship (Special Provisions) Act, 1991",
                    1991,
                    "statutory_asymmetry",
                    "Sections 3 & 4: Declares that the religious character of a place of worship existing on August 15, 1947 shall continue to be the same as it existed on that day, prohibiting conversion and abating all pending suits or proceedings.",
                    1,
                    "Statutory freeze on civilizational reclamation; creates asymmetric legal immunity for medieval temple demolitions while preempting judicial adjudication."
                ),
                (
                    "CLAUSE-1995-WAQF",
                    "Waqf Act, 1995",
                    1995,
                    "statutory_asymmetry",
                    "Section 40: Vests Waqf Boards with unilateral power to determine whether a property is waqf property, placing burden of proof on the adverse claimant and barring ordinary civil court jurisdiction under Section 85 in favor of specialized tribunals.",
                    1,
                    "Asymmetric property acquisition and jurisdictional barrier exempt from standard civil procedural code."
                ),
                (
                    "CLAUSE-1951-HRCE",
                    "Hindu Religious and Charitable Endowments (HRCE) Framework",
                    1951,
                    "statutory_asymmetry",
                    "State statutory oversight mechanisms authorizing executive officers to manage Hindu temple administrations and surplus treasury funds, whereas minority religious institutions are constitutionally protected under Article 30.",
                    1,
                    "Structural financial asymmetry and state appropriation of indigenous religious endowments without reciprocal minority institution regulation."
                ),
                (
                    "CLAUSE-CRPC-188-EXTRATERRITORIAL",
                    "Code of Criminal Procedure 1973 Section 188 / BNSS Section 208",
                    1973,
                    "extraterritorial_jurisdiction",
                    "Offences committed outside India: When an offence is committed outside India by a citizen of India or by a foreign national, no such offence shall be inquired into or tried in India without the previous sanction of the Central Government.",
                    1,
                    "Statutory barrier requiring Central Government sanction for extraterritorial offences, serving as a legal and diplomatic gatekeeper for sovereign prosecutions of foreign nationals."
                )
            ]

            cursor.executemany("""
                INSERT OR IGNORE INTO historical_treaty_clauses
                (clause_id, treaty_name, year, category, clause_text, is_mandatory_baseline, omission_significance)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, clauses_seed)

            anniversaries_seed = [
                (
                    "ANNIV-0711-GUADALETE",
                    7,
                    31,
                    711,
                    "Battle of Guadalete & Umayyad Crossing into Hispania",
                    "Europe / Iberia",
                    "Tariq ibn Ziyad led Umayyad forces across the Strait of Gibraltar, defeating Visigothic King Roderic and initiating Islamic Al-Andalus.",
                    "Historical mirror for sudden maritime demographic and asymmetric crossings into southern Spain."
                ),
                (
                    "ANNIV-1492-GRANADA",
                    1,
                    2,
                    1492,
                    "Fall of Granada & Reconquista Completion",
                    "Europe / Iberia",
                    "Ferdinand and Isabella completed the Reconquista, ending 781 years of Islamic rule in the Iberian Peninsula.",
                    "Civilizational inflection point representing sovereign reclamation and demographic reversal."
                ),
                (
                    "ANNIV-1971-INDO-SOVIET",
                    8,
                    9,
                    1971,
                    "Indo-Soviet Strategic Pact Ratification",
                    "South Asia",
                    "Signed by Swaran Singh and Andrei Gromyko, deterring US-China coalition during Bangladesh Liberation.",
                    "Strategic security guarantee enabling decisive perimeter stabilization."
                ),
                (
                    "ANNIV-1993-LAC",
                    9,
                    7,
                    1993,
                    "India-China Border Peace & Tranquility Agreement",
                    "Himalayas",
                    "Established mutual LAC commitments and troop reduction principles.",
                    "Legal baseline frequently cited during border standoff negotiations."
                ),
                (
                    "ANNIV-2024-RAM-MANDIR",
                    1,
                    22,
                    2024,
                    "Ayodhya Ram Mandir Pran Pratishtha",
                    "India",
                    "National consecration marking civilizational reclamation and post-colonial cultural decolonization.",
                    "Sanatan Dharmic civilizational baseline redefining Bharat's domestic and external sovereignty."
                ),
                (
                    "ANNIV-2024-DHAKA",
                    8,
                    5,
                    2024,
                    "Dhaka Regime Change & Sheikh Hasina Exit",
                    "South Asia",
                    "Fall of Awami League administration in Dhaka and transition to Muhammad Yunus interim council.",
                    "Immediate stress on eastern border, Siliguri Corridor security, and bilateral transit accords."
                ),
                (
                    "ANNIV-1947-PARTITION-INDIA",
                    8,
                    15,
                    1947,
                    "Partition of India",
                    "South Asia",
                    "British India was partitioned into the independent dominions of India and Pakistan, triggering one of the largest mass migrations and communal violence episodes in modern history.",
                    "Civilizational rupture whose demographic, territorial, and psychological aftershocks continue to shape South Asian geopolitics."
                ),
                (
                    "ANNIV-1962-SINO-INDIAN-WAR",
                    10,
                    20,
                    1962,
                    "Sino-Indian War / Aksai Chin",
                    "South Asia / Central Asia",
                    "China launched a massive invasion across NEFA (Arunachal Pradesh) and consolidated control over Aksai Chin, exposing critical Indian strategic and intelligence failures.",
                    "Foundational trauma driving Indian forward-posture doctrine on the LAC and Himalayan infrastructure build-up."
                ),
                (
                    "ANNIV-1971-BANGLADESH-LIBERATION",
                    12,
                    16,
                    1971,
                    "Bangladesh Liberation War Victory",
                    "South Asia",
                    "Indian armed forces achieved decisive victory, liberating East Pakistan and leading to the creation of Bangladesh after Pakistan's unconditional surrender.",
                    "Demonstrated India's capacity for rapid decisive military operations and reshaped the South Asian balance of power."
                ),
                (
                    "ANNIV-1998-POKHRAN-II",
                    5,
                    11,
                    1998,
                    "Pokhran-II Nuclear Tests",
                    "South Asia",
                    "India conducted Operation Shakti — a series of five thermonuclear and fission device tests at the Pokhran range — declaring itself a nuclear-weapons state.",
                    "Strategic watershed establishing India's minimum credible nuclear deterrent and triggering global non-proliferation debates."
                ),
                (
                    "ANNIV-1999-KARGIL-WAR",
                    5,
                    26,
                    1999,
                    "Kargil War",
                    "South Asia / Kashmir",
                    "Pakistani soldiers and militants intruded across the Line of Control in the Kargil-Dras sector, triggering a high-altitude limited war won by Indian forces.",
                    "Validated India's conventional escalation dominance under a nuclear overhang and exposed Pakistani adventurism."
                ),
                (
                    "ANNIV-2019-BALAKOT",
                    2,
                    26,
                    2019,
                    "Balakot Airstrike",
                    "South Asia",
                    "Indian Air Force conducted precision airstrikes on a Jaish-e-Mohammed (JeM) training camp in Balakot, Pakistan — the first cross-border airstrike since 1971.",
                    "Established a new Indian doctrine of pre-emptive cross-border counterterrorism strikes against non-state actor infrastructure."
                ),
                (
                    "ANNIV-2020-GALWAN",
                    6,
                    15,
                    2020,
                    "Galwan Valley Clash",
                    "South Asia / LAC",
                    "Indian and Chinese troops engaged in a violent hand-to-hand clash in the Galwan Valley along the LAC, resulting in casualties on both sides.",
                    "Shattered the post-1993 border peace framework and triggered permanent Indian strategic decoupling from China."
                ),
                (
                    "ANNIV-2025-OP-SINDOOR",
                    5,
                    7,
                    2025,
                    "Operation Sindoor",
                    "South Asia",
                    "India executed precision retaliatory strikes on terror infrastructure in Pakistan following cross-border provocations, demonstrating calibrated escalation capability.",
                    "Reinforced India's zero-tolerance doctrine against state-sponsored terrorism and validated standoff precision-strike assets."
                ),
                (
                    "ANNIV-1916-SYKES-PICOT",
                    5,
                    16,
                    1916,
                    "Sykes-Picot Agreement",
                    "Middle East",
                    "Secret Anglo-French agreement partitioning Ottoman Arab provinces into spheres of influence, drawing artificial borders across Mesopotamia, the Levant, and Arabia.",
                    "Root cause of chronic Middle Eastern state fragility, sectarian conflict, and post-colonial boundary disputes."
                ),
                (
                    "ANNIV-1944-BRETTON-WOODS",
                    7,
                    1,
                    1944,
                    "Bretton Woods Conference",
                    "Global",
                    "Allied nations convened at Bretton Woods, New Hampshire, establishing the International Monetary Fund (IMF), World Bank, and the US dollar-anchored global reserve currency system.",
                    "Architected the post-WWII financial order whose erosion now drives de-dollarization and BRICS alternative currency initiatives."
                ),
                (
                    "ANNIV-1025-CHOLA-SRIVIJAYA",
                    11,
                    15,
                    1025,
                    "Rajendra Chola I Srivijaya Maritime Expedition",
                    "Indian Ocean / Southeast Asia",
                    "Rajendra Chola I launched a massive naval expedition across the Bay of Bengal, securing the Strait of Malacca and subordinating the Srivijaya maritime empire.",
                    "Foundational anchor of Indian Ocean naval power and maritime trade dominance, currently mirrored in India's SAGAR and IMEC corridors."
                ),
                (
                    "ANNIV-1026-SOMNATH",
                    1,
                    8,
                    1026,
                    "Raid on Somnath & Millennial Arc Initiation",
                    "South Asia",
                    "Mahmud of Ghazni raided and plundered the Somnath temple, inaugurating the millennial arc of civilizational disruption, economic plunder, and iconoclasm.",
                    "Symbolic baseline of civilizational disruption, whose post-independence reconstruction by Sardar Patel marked the beginning of modern reclamation."
                ),
                (
                    "ANNIV-1192-TARAIN",
                    3,
                    15,
                    1192,
                    "Second Battle of Tarain",
                    "South Asia",
                    "Muhammad Ghori defeated Prithviraj Chauhan at the Second Battle of Tarain, precipitating the fall of Delhi and the establishment of the Delhi Sultanate.",
                    "Foundational inflection point representing sovereign internal fragmentation and loss of northern border defense."
                ),
                (
                    "ANNIV-1193-NALANDA",
                    5,
                    20,
                    1193,
                    "Destruction of Nalanda Mahavihara",
                    "South Asia",
                    "Bakhtiyar Khilji sacked and burned the ancient Nalanda Mahavihara university, destroying millions of manuscripts and intellectually de-capitalizing the Dharmic world.",
                    "Civilizational epistemic rupture, whose 830-year recovery was formalized with the 2024 inauguration of the new Nalanda campus."
                ),
                (
                    "ANNIV-1453-CONSTANTINOPLE",
                    5,
                    29,
                    1453,
                    "Fall of Constantinople & Silk Road Closure",
                    "Eurasia",
                    "Ottoman Sultan Mehmed II conquered Constantinople, ending the Byzantine Empire, closing overland Silk Road transit to Europe, and forcing Western maritime expeditions toward India.",
                    "Global trade inflection point that triggered the Age of Discovery and the maritime colonization of Afro-Asian trade routes."
                ),
                (
                    "ANNIV-1674-CHHATRAPATI-SHIVAJI",
                    6,
                    6,
                    1674,
                    "Coronation of Chhatrapati Shivaji Maharaj & Hindavi Swarajya",
                    "South Asia",
                    "Chhatrapati Shivaji Maharaj was coronated at Raigad Fort, formally inaugurating Hindavi Swarajya and re-establishing indigenous Dharmic sovereignty and naval defense.",
                    "Doctrinal baseline of asymmetric military resistance, naval fort fortification, and indigenous sovereign reclamation."
                ),
                (
                    "ANNIV-2024-NALANDA-REBIRTH",
                    6,
                    19,
                    2024,
                    "Nalanda University Rebirth & Epistemic Reversal",
                    "South Asia",
                    "Prime Minister Narendra Modi and envoys from 17 partner nations inaugurated the resurrected Nalanda University campus in Rajgir, Bihar.",
                    "Physical and symbolic closure of the 830-year intellectual destruction arc, re-establishing Bharat as a global knowledge repository."
                ),
                (
                    "ANNIV-1920-WATSON-JWT",
                    10,
                    1,
                    1920,
                    "John B. Watson Joins J. Walter Thompson (JWT)",
                    "Global / USA",
                    "Behaviorist psychologist John B. Watson joined the J. Walter Thompson advertising agency, formally applying emotional and fear conditioning to commercial advertising and product marketing.",
                    "Birth of modern commercial psychological warfare, weaponizing infant hygiene, germ fear, and maternal anxiety into consumer demand."
                ),
                (
                    "ANNIV-1928-WATSON-INFANT",
                    3,
                    1,
                    1928,
                    "Watson Publishes 'Psychological Care of Infant and Child'",
                    "Global / USA",
                    "John B. Watson published his seminal parenting manual prescribing rigid emotional detachment, warning mothers against hugging or kissing infants to avoid 'spoiling' them.",
                    "Institutionalization of cold infant isolation doctrine, replacing maternal bonding with commodified schedules and nursery appliances."
                ),
                (
                    "ANNIV-1928-BERNAYS-PROPAGANDA",
                    11,
                    15,
                    1928,
                    "Edward Bernays Publishes 'Propaganda' & Torches of Freedom",
                    "Global / USA",
                    "Edward Bernays published 'Propaganda', codifying the 'engineering of consent' and later executing the 'Torches of Freedom' campaign linking women's liberation to cigarette consumption.",
                    "Foundational playbook for modern public relations, psychological manipulation, and manufacturing social consent for corporate cartels."
                ),
                (
                    "ANNIV-1953-MKULTRA-MOCKINGBIRD",
                    4,
                    13,
                    1953,
                    "CIA Project MKUltra & Operation Mockingbird",
                    "Global / USA",
                    "CIA launched Project MKUltra (mind control and behavioral modification experiments) and Operation Mockingbird (subterranean infiltration of domestic and international media organizations).",
                    "Institutionalization of deep-state psychological operations, weaponized media narratives, and covert cognitive warfare."
                ),
                (
                    "ANNIV-1981-WHO-INFANT-FORMULA",
                    5,
                    21,
                    1981,
                    "WHO International Code of Marketing of Breast-milk Substitutes",
                    "Global",
                    "World Health Assembly adopted landmark International Code (WHA34.22) restricting aggressive marketing of infant formula, following global boycotts against commercial exploitation of maternal anxiety in developing nations.",
                    "Landmark sovereign multilateral confrontation against transnational corporate capture of infant health and fear-based marketing."
                ),
                (
                    "CHRONO-5561BCE-OAK",
                    10,
                    16,
                    -5561,
                    "Nilesh Oak 5561 BCE Timeline (Arundhati-Vasistha Model)",
                    "Ancient Bharat",
                    "Dates the Mahabharata War to 5561 BCE based on the Arundhati walking ahead of Vasistha (Mizar-Alcor) observation in Bhishma Parva, calculating an epoch window between 11,091 BCE and 4508 BCE.",
                    "Benchmark astronomical retro-calculation hypothesis; subject to material culture collision with Mesolithic/early Neolithic lithic archaeological strata."
                ),
                (
                    "CHRONO-3067BCE-ACHAR",
                    11,
                    22,
                    -3067,
                    "Dr. Narahari Achar 3067 BCE Timeline (Saturn-Rohini BORI Model)",
                    "Ancient Bharat",
                    "Dates the Mahabharata War to 3067 BCE based on the BORI Critical Edition common archetype, Saturn at Rohini, Jupiter at Vishakha, and twin eclipses within 13 days.",
                    "Multi-pillar benchmark exhibiting low astronomical degeneracy and high congruence with Saraswati perennial flow and Early Bronze Age urban transitions."
                ),
                (
                    "CHRONO-3102BCE-ARYABHATA",
                    2,
                    18,
                    -3102,
                    "Traditional Aryabhata & Aihole Inscription 3102 BCE Kali Yuga Epoch",
                    "Ancient Bharat",
                    "Traditional civilizational anchor calculating the start of Kali Yuga at 3102 BCE, epigraphically corroborated by the Aihole Inscription of Pulakeshin II (634 CE) referencing 3735 elapsed years.",
                    "Civilizational baseline anchor uniting Puranic dynastic chronologies with planetary mean-motion calculations."
                ),
                (
                    "CHRONO-1000BCE-PGW",
                    1,
                    1,
                    -1000,
                    "Archaeological Survey of India Painted Grey Ware (PGW) 1000 BCE Model",
                    "Ancient Bharat",
                    "Dates the epic to the 10th-9th century BCE based on Painted Grey Ware (PGW) strata, early iron arrowheads at Hastinapur/Kurukshetra, and the flood layer described in Puranic texts.",
                    "Archaeologically grounded material culture anchor; exhibits low hydro-geological coherence due to complete prior desiccation of River Saraswati by 1900 BCE."
                ),
                (
                    "CHRONO-2000BCE-SINAULI",
                    1,
                    1,
                    -2000,
                    "Sinauli Bronze Age Necropolis (OCP / Copper Hoard Culture)",
                    "Ancient Bharat / Ganga-Yamuna Doab",
                    "Excavations at Sinauli (Baghpat, UP) revealed elite warrior burials with copper-inlaid solid-disk wheeled carts, antennae swords, shields, and four-legged coffins dating to 2000-1800 BCE via calibrated C14.",
                    "Stratigraphical and material culture anchor establishing indigenous Bronze Age wheeled transport and warrior aristocracy in northern India; concordant with Rigveda 10.18 inhumation rites."
                ),
                (
                    "CHRONO-2500BCE-RAKHIGARHI",
                    1,
                    1,
                    -2500,
                    "Rakhigarhi Mature Harappan Paleogenomic Anchor",
                    "Ancient Bharat / Ghaggar-Hakra Basin",
                    "Ancient DNA from Mature IVC female skeleton demonstrating absence of Central Asian Steppe pastoralist ancestry (R1a-Z93) and presence of Iranian farmer-related and Ancient Ancestral South Indian (AASI) lineage.",
                    "Crucial paleogenomic baseline establishing genetic continuity in South Asia and disproving catastrophic population replacement models."
                ),
                (
                    "ANNIV-1978-KAHUTA-LEAK",
                    1,
                    15,
                    1978,
                    "Operation Kahuta Intelligence Compromise",
                    "South Asia / Pakistan",
                    "R&AW established deep human penetration of Khan Research Laboratories in Kahuta, confirming uranium enrichment via physical samples. Subsequent political inadvertent disclosure alerted Islamabad, triggering an ISI counter-sweep that decapitated India's operational network inside the facility.",
                    "Demonstrates the extreme vulnerability of high-yield HUMINT networks to political indiscretion and civilian oversight disconnects."
                ),
                (
                    "ANNIV-1985-KANISHKA-AIR-INDIA-182",
                    6,
                    23,
                    1985,
                    "Kanishka Bombing & Canadian Sanctuary Milestone",
                    "Transnational / Canada / Atlantic",
                    "Babbar Khalsa operatives in Canada orchestrated the mid-air bombing of Air India Flight 182 off the coast of Ireland, killing 329 people in the deadliest terrorist act in Canadian history.",
                    "Foundational baseline for Western diaspora vote-bank sanctuary politics and intelligence blind spots regarding extraterritorial secessionist networks."
                ),
                (
                    "ANNIV-1991-RAJIV-GANDHI-SRIPERUMBUDUR",
                    5,
                    21,
                    1991,
                    "Assassination of Rajiv Gandhi & SPG Cover Withdrawal",
                    "South Asia / Sri Lanka",
                    "Former Prime Minister Rajiv Gandhi was assassinated at Sriperumbudur by an LTTE suicide bomber following the withdrawal of Special Protection Group (SPG) security under domestic political rivalry.",
                    "Exposes the catastrophic risk window opened when domestic partisan hostility compromises institutional executive security protocols."
                ),
                (
                    "ANNIV-1993-MUMBAI-BLASTS-D-COMPANY",
                    3,
                    12,
                    1993,
                    "1993 Mumbai Serial Blasts & D-Company Karachi Haven",
                    "South Asia / Mumbai / Karachi",
                    "Coordinated serial RDX explosions struck 12 targets across Mumbai, orchestrated by Dawood Ibrahim's D-Company with Pakistani ISI logistics and safe passage, establishing the syndicate's permanent haven in Clifton, Karachi.",
                    "Institutionalized the state-sponsored crime-terror nexus, combining transnational narcotics and hawala networks with sovereign intelligence protection."
                ),
                (
                    "ANNIV-1999-IC-814-KANDAHAR",
                    12,
                    24,
                    1999,
                    "IC-814 Kandahar Hijack & Strategic Negotiation Crisis",
                    "South Asia / Afghanistan",
                    "Harkat-ul-Mujahideen terrorists hijacked Indian Airlines Flight IC-814 from Kathmandu to Kandahar under Taliban control, forcing the release of three terror commanders including Masood Azhar.",
                    "Critical watershed shaping India's modern counter-terror crisis response, hostage negotiation doctrine, and the transition toward the Doval Offensive-Defense preemption doctrine."
                ),
                (
                    "HIST-1976-MARITIME-ZONES-ACT",
                    8,
                    25,
                    1976,
                    "Territorial Waters, Continental Shelf, EEZ and Other Maritime Zones Act (Act 80 of 1976)",
                    "Indian Ocean / New Delhi",
                    "Codified India's sovereign maritime baselines: 12 NM territorial waters, 24 NM contiguous zone, and 200 NM Exclusive Economic Zone (EEZ) encompassing over 2.3 million square kilometers.",
                    "Foundational domestic statute asserting resource sovereignty and requiring prior notification for foreign warship entry."
                ),
                (
                    "HIST-2021-US-FONOP-LAKSHADWEEP",
                    4,
                    7,
                    2021,
                    "USS John Paul Jones FONOP West of Lakshadweep Islands",
                    "Arabian Sea / Lakshadweep",
                    "US 7th Fleet destroyer USS John Paul Jones conducted Freedom of Navigation Operation (FONOP) within India's EEZ without prior consent, publicly challenging India's maritime claims under Act 80/1976.",
                    "Highlights the enduring statutory divergence between US customary high-seas navigation interpretations and Indian domestic security consent mandates in the EEZ."
                ),
                (
                    "HIST-2022-MARITIME-ANTI-PIRACY",
                    12,
                    21,
                    2022,
                    "Maritime Anti-Piracy Act 2022 High-Seas Codification",
                    "Indian Ocean / Gulf of Aden / New Delhi",
                    "Parliament enacted the Maritime Anti-Piracy Act, codifying universal jurisdiction over high-seas piracy and empowering the Indian Navy and Coast Guard to intercept, arrest, and prosecute transnational pirates in domestic special courts.",
                    "Enabled the Indian Navy's forward security posture in the Arabian Sea and Gulf of Aden, executing boarding and recapture operations."
                ),
                (
                    "HIST-2020-FCRA-CRACKDOWN",
                    9,
                    29,
                    2020,
                    "Foreign Contribution Regulation Amendment Act & NGO Surveillance",
                    "National / New Delhi",
                    "Parliament enacted the FCRA Amendment Act 2020, mandating centralized SBI New Delhi accounts, banning sub-granting, and initiating cancellations of foreign-funded advocacy licenses (Amnesty, Oxford Policy Management).",
                    "Dismantled transnational funding corridors weaponized for sub-national lawfare and proxy economic litigation."
                ),
                (
                    "HIST-2024-WAQF-AMENDMENT-BILL",
                    8,
                    8,
                    2024,
                    "Waqf (Amendment) Bill 2024 Legislative Introduction",
                    "National / Parliament of India",
                    "Government introduced the Waqf (Amendment) Bill, reforming the 1995 Act by stripping Waqf Boards of unilateral survey powers under Section 40, transferring dispute jurisdiction to District Collectors/Civil Courts, and mandating non-Muslim and female representation.",
                    "Major institutional lawfare recalibration addressing statutory asymmetries and parallel land dispute jurisdictions."
                ),
                (
                    "HIST-2023-IMEC-G20-NEW-DELHI",
                    9,
                    9,
                    2023,
                    "India-Middle East-Europe Economic Corridor (IMEC) Declaration",
                    "New Delhi / Global",
                    "India, US, UAE, Saudi Arabia, France, Germany, Italy, and EU signed the IMEC MOU at the New Delhi G20 Summit, designing a multi-modal ship-to-rail transit network connecting India to Europe via the Arabian Gulf.",
                    "Strategic counter-BRI logistics corridor bypassing maritime chokepoints and integrating West Asian energy with Indian manufacturing."
                ),
                (
                    "HIST-2024-TRAPPED-RUPEE-VOSTRO",
                    5,
                    15,
                    2024,
                    "Special Rupee Vostro Account (SRVA) Capital Recycling Accord",
                    "New Delhi / Moscow",
                    "India and Russia negotiated mechanisms to recycle an estimated ₹20,000+ crore in trapped Russian rupee balances accumulated via discounted Urals crude purchases into Indian government securities (G-Secs), equity, and infrastructure investments.",
                    "Demonstrates the practical financial plumbing bottlenecks of bilateral de-dollarization and the necessity of capital account recycling."
                ),
                (
                    "HIST-2005-IMDT-ACT-STRUCK-DOWN",
                    7,
                    12,
                    2005,
                    "Supreme Court Strikes Down IMDT Act (Sarbananda Sonowal v. UOI)",
                    "South Asia / Assam",
                    "Supreme Court struck down the Illegal Migrants (Determination by Tribunals) Act 1983 as unconstitutional in Sarbananda Sonowal v. Union of India, declaring unchecked demographic influx as external aggression under Article 355.",
                    "Constitutional recognition of demographic infiltration as an existential security threat, restoring the Foreigners Act 1946 reverse burden of proof."
                ),
                (
                    "HIST-2021-GORUKHUTI-EVICTION",
                    9,
                    23,
                    2021,
                    "Gorukhuti & Dhalpur Riverine Agricultural Eviction Drive",
                    "Assam / Brahmaputra Valley",
                    "Assam Government executed eviction operations across Gorukhuti and Dhalpur in Darrang district, reclaiming ~77,000 bighas of riverine char and Sattra agricultural lands encroached by non-indigenous populations.",
                    "Operational statecraft enforcing the Assam Land and Revenue Regulation 1886 to recover encroached sacred and ecological commons in riverine floodplains."
                ),
                (
                    "HIST-2023-ASSAM-DELIMITATION",
                    8,
                    11,
                    2023,
                    "Election Commission Notifies Assam Delimitation under RPA Section 8A",
                    "South Asia / Assam",
                    "Election Commission of India published the final delimitation order for 126 Assembly and 14 Parliamentary constituencies in Assam under Section 8A of RPA 1950, preserving 19 assembly seats for SC/ST and securing indigenous majority in ~96 assembly seats.",
                    "Statutory demarcation anchoring sub-national indigenous political representation against rapid demographic transformation and district-level gerrymandering."
                ),
                (
                    "HIST-2024-UGC-RESERVATION-ROLLBACK",
                    1,
                    29,
                    2024,
                    "Union Education Ministry 24-Hour Rollback of UGC De-Reservation Draft",
                    "National / New Delhi",
                    "Following immediate widespread public outrage and political mobilization, the Ministry of Education ordered UGC to withdraw its Draft Guidelines for De-reservation in Higher Education Institutions within 24 hours.",
                    "Archetypal manifestation of high rollback elasticity where bureaucratic guideline formulation without political calibration triggered immediate executive retreat."
                ),
                (
                    "HIST-1953-AMBEDKAR-RAJYA-SABHA-SPEECH",
                    9,
                    2,
                    1953,
                    "Dr. B.R. Ambedkar Rajya Sabha Address on Constitutional Drafting Constraints",
                    "National / New Delhi",
                    "Dr. B.R. Ambedkar addressed the Rajya Sabha on constitutional amendments, stating: 'I was a hack. What I was got to do, I did much against my will... I am quite ready to say that I would be the first person to burn it out.'",
                    "Historical parliamentary record documenting that the Indian Constitution was the collective product of the 299-member Constituent Assembly and Drafting Committee, not the unilateral fiat of a single author."
                ),
                (
                    "HIST-2018-SC-ST-AMENDMENT-OVERRIDE",
                    8,
                    17,
                    2018,
                    "Parliament Enacts SC/ST Amendment Act 2018 (Section 18A Legislative Override)",
                    "National / New Delhi",
                    "Parliament inserted Section 18A into the SC/ST (Prevention of Atrocities) Act 1989, explicitly overriding the Supreme Court's Subhash Kashinath Mahajan judgment to bar preliminary inquiries and prohibit anticipatory bail under Section 438 CrPC.",
                    "Archetypal manifestation of competitive electoral clientelism overriding judicial due process safeguards, creating acute statutory asymmetry and intra-civilizational polarization."
                ),
                (
                    "HIST-2024-VANDYKE-MYANMAR-DEPORTATION",
                    3,
                    12,
                    2024,
                    "Managed Diplomatic Deportation of US Security Contractor Matthew VanDyke",
                    "Northeast / Assam / Myanmar Border",
                    "US private military contractor Matthew VanDyke (founder of Sons of Liberty International), detained near the Assam-Myanmar border for unauthorized entry and tactical drone training of anti-junta militias under UAPA/Foreigners Act, was quietly granted default bail and deported under US diplomatic pressure.",
                    "Benchmark of extraterritorial sovereign asymmetry: domestic criminal-statutory parity subordinated to bilateral diplomatic leverage, contrasting severe domestic enforcement with foreign contractor immunity."
                ),
                (
                    "HIST-1963-NEHRU-MEA-DIRECTIVE",
                    12,
                    15,
                    1963,
                    "Jawaharlal Nehru MEA Meeting Remarks on Internal vs External Threats",
                    "National / New Delhi",
                    "Prime Minister Jawaharlal Nehru addressed senior MEA officials, famously asserting that the primary danger to India was internal Hindu right-wing communalism rather than external communism, establishing a legacy of internal threat prioritization.",
                    "Institutional doctrinal precedent shaping diplomatic cadre ideology and counter-intelligence prioritization."
                ),
                (
                    "HIST-1992-TEHRAN-RAW-NETWORK-COMPROMISE",
                    6,
                    10,
                    1992,
                    "R&AW Persian Gulf & Tehran Station Intelligence Network Compromise",
                    "Middle East / Iran / Tehran",
                    "During the ambassadorship of Hamid Ansari in Iran, R&AW intelligence operations and Persian Gulf station operatives faced critical compromise and unauthorized exposure to Iranian intelligence (documented by former R&AW officer N.K. Sood).",
                    "Historical benchmark of diplomatic-intelligence friction, asset fragility, and counter-espionage vulnerability in strategic West Asian missions."
                ),
                (
                    "HIST-2023-RED-SEA-ASYMMETRIC-ATTRITION",
                    12,
                    15,
                    2023,
                    "Red Sea Asymmetric Drone Saturation & Western Interceptor Burnout",
                    "Red Sea / Bab-el-Mandeb",
                    "Ansar Allah (Houthi) forces launched low-cost loitering drones ($10k-$20k), forcing US Carrier Strike Groups to expend multimillion-dollar Standard Missiles (SM-2, SM-6 at $2M-$4M each), establishing an unsustainable asymmetric economic cost-exchange ratio.",
                    "Strategic operational watershed demonstrating naval air-defense magazine depletion and the limits of high-end kinetic interceptors against low-cost swarms."
                ),
                (
                    "HIST-2024-TEXAS-HANUMAN-TEMPLE-NATIVIST-BACKLASH",
                    8,
                    18,
                    2024,
                    "Sugar Land Texas Statue of Union (Hanuman) & Nativist Backlash",
                    "North America / Texas / Sugar Land",
                    "Unveiling of the 90-foot Sri Ashtalakshmi Temple Statue of Union in Sugar Land, Texas triggered coordinated far-right nativist attacks, municipal zoning challenges, and xenophobic rhetoric, highlighting host-nation hostility against Dharmic civilizational visibility.",
                    "Empirical milestone of diaspora vulnerability: high median wealth without political coalition defense creates severe exposure to nativist backlash and progressive caste lawfare."
                ),
                (
                    "HIST-1770-EIC-SALTPETRE-MONOPSONY",
                    5,
                    15,
                    1770,
                    "British East India Company Saltpetre State Monopsony Accord",
                    "Bengal Presidency / Bihar",
                    "EIC established an absolute state monopoly over saltpetre (potassium nitrate) refining across Bihar and Bengal, forcing indigenous Noniya artisans to deliver gunpowder components at below-subsistence fixed rates, triggering guild collapse.",
                    "Archetypal colonial economic intervention dismantling indigenous artisan guilds through state monopsony pricing, establishing systemic impoverishment."
                ),
                (
                    "HIST-1871-CRIMINAL-TRIBES-ACT",
                    10,
                    12,
                    1871,
                    "Enactment of Criminal Tribes Act (Act XXVII of 1871)",
                    "British India",
                    "Imperial Legislative Council enacted the Criminal Tribes Act, institutionalizing the collective statutory criminalization of over 160 itinerant artisan and nomadic communities without requiring proof of individual criminal conduct.",
                    "Colonial lawfare converting displaced artisan and nomadic populations into hereditary criminals, laying the foundation for rigid 20th-century social stratification."
                ),
                (
                    "HIST-1991-BOP-GOLD-PLEDGE",
                    5,
                    21,
                    1991,
                    "Emergency Gold Airlift to Bank of England & 1991 BoP Stabilization",
                    "National / London / Global",
                    "Reserve Bank of India airlifted 47 tonnes of sovereign gold to the Bank of England and Union Bank of Switzerland to secure emergency $405M loan, averting sovereign debt default.",
                    "Sovereign liquidity crisis forcing the dismantling of the License Raj and launching India's structural economic liberalization."
                )
            ]

            cursor.executemany("""
                INSERT OR IGNORE INTO historical_anniversaries
                (anniversary_id, month, day, year, event_title, region, historical_summary, strategic_mirror_significance)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, anniversaries_seed)

            # Phase 86: Seed Historical Resolved Forecast Calibrations (1974-2024 benchmarks)
            historical_forecasts_seed = [
                (
                    "FCST-HIST-1974-POKHRAN-I", "1974-01-10", "1974-05-18", "Smiling Buddha",
                    "India conducts peaceful nuclear explosive test under BARC/AEC leadership",
                    0.85, 0.70, 0.95, "BARC seismic preparations and plutonium metallurgy verification",
                    1, 0.0225, "RESOLVED"
                ),
                (
                    "FCST-HIST-1998-POKHRAN-II", "1998-03-20", "1998-05-11", "Operation Shakti",
                    "India detonates thermonuclear and fission warheads evading US satellite overflights",
                    0.88, 0.75, 0.96, "58 Armoured Engineer Regiment camouflage protocol and solar tracking",
                    1, 0.0144, "RESOLVED"
                ),
                (
                    "FCST-HIST-1999-KARGIL-LOITER", "1999-05-10", "1999-07-26", "Operation Vijay",
                    "Indian military evicts Northern Light Infantry intrusions across LoC ridgelines",
                    0.90, 0.80, 0.98, "Artillery massing (Bofors FH77B) and precision laser-guided strikes (Mirage 2000)",
                    1, 0.0100, "RESOLVED"
                ),
                (
                    "FCST-HIST-2017-DOKLAM-STANDOFF", "2017-06-25", "2017-08-28", "Doklam Plateau Standoff",
                    "India-China bilateral disengagement achieved without Chinese road completion at Doka La",
                    0.82, 0.68, 0.92, "Mutual verification protocols and Chumbi valley flank exposure",
                    1, 0.0324, "RESOLVED"
                ),
                (
                    "FCST-HIST-2020-GALWAN-DISENGAGE", "2020-06-20", "2021-02-15", "Galwan & Pangong Tso Standoff",
                    "Disengagement achieved at Finger 4-8 with permanent Indian ITBP/Army forward bases",
                    0.78, 0.65, 0.89, "Armor positioning on Kailash Range and winter stocking parity",
                    1, 0.0484, "RESOLVED"
                ),
                (
                    "FCST-HIST-2022-RUS-CRUDE-DISCOUNT", "2022-03-05", "2022-12-31", "Urals Crude Procurement",
                    "India increases Russian crude import share from <2% to >30% resisting secondary sanctions",
                    0.86, 0.75, 0.94, "Refinery cracking economics, Urals $25-35 discount, and shadow tanker logistics",
                    1, 0.0196, "RESOLVED"
                ),
                (
                    "FCST-HIST-2023-G20-CONSENSUS", "2023-08-15", "2023-09-10", "New Delhi G20 Leaders Summit",
                    "Unanimous 100% consensus achieved on New Delhi Declaration including Ukraine paragraphs",
                    0.80, 0.65, 0.92, "Emerging market quad (India, Brazil, South Africa, Indonesia) coordination",
                    1, 0.0400, "RESOLVED"
                ),
                (
                    "FCST-HIST-2023-ASSAM-DELIMITATION", "2023-01-15", "2023-08-11", "Assam ECI Delimitation Finalization",
                    "Election Commission notifies Section 8A delimitation safeguarding indigenous seat representation",
                    0.85, 0.72, 0.94, "RPA Section 8A statutory notification, district consultation rounds, and ECI bench orders",
                    1, 0.0225, "RESOLVED"
                ),
                (
                    "FCST-HIST-2024-CHABAHAR-10YR", "2024-02-10", "2024-05-13", "Chabahar Port Long-Term Accord",
                    "India Signs 10-Year Long-Term Contract with Iran for Shahid Beheshti Terminal",
                    0.85, 0.72, 0.93, "IPGL negotiations and OFAC humanitarian carve-out validation",
                    1, 0.0225, "RESOLVED"
                ),
                (
                    "FCST-HIST-2018-SC-ST-OVERRIDE", "2018-04-10", "2018-08-17", "SC/ST Act Section 18A Override",
                    "Parliament enacts legislative override of Supreme Court Kashinath Mahajan procedural safeguards under mass electoral pressure",
                    0.88, 0.76, 0.95, "Bipartisan electoral convergence and street mobilization pressure following April 2 Bharat Bandh",
                    1, 0.0144, "RESOLVED"
                ),
                (
                    "FCST-HIST-2023-RED-SEA-ATTRITION", "2023-10-25", "2024-02-15", "Red Sea Drone Attrition",
                    "Houthi low-cost loitering drones force US Navy to expend multimillion-dollar interceptors exhausting carrier magazine depth",
                    0.86, 0.74, 0.94, "Naval missile inventory math, Red Sea shipping diversions, and Houthi drone unit economics",
                    1, 0.0196, "RESOLVED"
                ),
                (
                    "FCST-HIST-1991-BOP-REFORMS", "1991-05-25", "1991-07-24", "1991 Balance of Payments & Industrial Policy",
                    "Emergency sovereign gold pledge averts default, catalyzing abolition of industrial licensing and rupee devaluation",
                    0.87, 0.75, 0.94, "FX reserve depletion (< 3 weeks imports), IMF structural adjustment conditionalities, and ministerial consensus",
                    1, 0.0169, "RESOLVED"
                ),
                (
                    "FCST-HIST-1871-CRIMINAL-TRIBES", "1871-06-15", "1871-10-12", "Enactment of Criminal Tribes Act 1871",
                    "Colonial administration enacts statutory collective criminalization of displaced saltpetre noniya and itinerant trade castes",
                    0.89, 0.78, 0.96, "Imperial police reports on nomadic resistance, EIC mineral monopolies, and British utilitarian administrative dominance",
                    1, 0.0121, "RESOLVED"
                )
            ]
            cursor.executemany("""
                INSERT OR IGNORE INTO forecast_ledger
                (forecast_id, created_at, target_date, event_name, hypothesis, predicted_probability,
                 confidence_interval_low, confidence_interval_high, epistemic_basis, actual_outcome, brier_score, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, historical_forecasts_seed)

            cosmic_benchmarks_seed = [
                (
                    "COSMIC-KALIYUGA-CANONICAL",
                    "yuga_cycle",
                    "Surya Siddhanta & Classical Puranic Corpus",
                    "Surya Siddhanta (1.15-17), Aryabhatiya (Kalakriyapada), Vishnu Purana (1.3), Bhagavata Purana (12.2), Mahabharata (Vana Parva 188)",
                    "3102-02-18 BCE",
                    432000.0,
                    "Planetary conjunction at Mesha (Aries 0 deg) and solar mean motion.",
                    "Directly refutes modern 5,000-year truncation claims; in 2026 CE only ~5,127 years have elapsed (~1.19%), leaving 426,873 years remaining."
                ),
                (
                    "EPIGRAPH-634CE-AIHOLE",
                    "epigraphic_anchor",
                    "Aihole Inscription of Pulakeshin II",
                    "Meguti Jain Temple Inscription, Aihole (composed by Ravikirti, Saka 556)",
                    "634 CE",
                    3735.0,
                    "Epigraphic stone inscription recording 3,735 elapsed years since the Bharata War.",
                    "Provides immutable epigraphic confirmation anchoring the Kali Yuga commencement to February 3102 BCE."
                ),
                (
                    "TEMPLE-1150CE-PURI-JAGANNATH",
                    "temple_chronicle",
                    "Puri Jagannath Temple Madala Panji & ASI Records",
                    "Madala Panji Temple Chronicles & Archaeological Survey of India Conservation Records",
                    "1150 CE",
                    875.0,
                    "214-ft Khondalite sandstone tower exposed to severe marine saline air, humid expansion, and Category 4/5 tropical cyclones.",
                    "Structural stone displacements documented since 1842 are natural coastal conservation issues, not supernatural apocalypses."
                ),
                (
                    "DEBUNK-1997-NOSTRADAMUS-TWINTOWERS",
                    "hoax_registry",
                    "Neil Marshall Hoax & French Philological Analysis",
                    "Neil Marshall (Brock University 1997 Essay); Nostradamus Les Propheties (1555)",
                    "1997 CE",
                    0.0,
                    "Internet chain letter authored by a Canadian student in 1997 demonstrating confirmation bias, falsely attributed to Nostradamus after 9/11.",
                    "Nostradamus never wrote 'birds of iron' or 'two brothers'. The quatrain 'Hister' refers to the Latin name for the Lower Danube River (Ister), not Adolf Hitler."
                ),
                (
                    "DEBUNK-1970-MALIKA-KASHINATH",
                    "hoax_registry",
                    "Modern Commercial Chapbook Press",
                    "Pandit Kashinath Mishra Bazaar Pamphlets (Cuttack/Puri); Odisha State Museum Palm-Leaf Archives",
                    "1970-1999 CE",
                    0.0,
                    "Late 20th-century commercial bazaar pamphlet interpolations printed in regional press.",
                    "Pre-1947 palm-leaf manuscripts at Odisha State Museum and Prachi Valley contain zero references to modern political figures, Pakistan partition, or Vajpayee's 13-day rule."
                )
            ]

            cursor.executemany("""
                INSERT OR IGNORE INTO cosmic_chronology_benchmarks
                (benchmark_id, category, canonical_source, primary_citation, temporal_epoch, duration_years, physical_basis, debunk_notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, cosmic_benchmarks_seed)

            conn.commit()


    def get_mandatory_baseline_clauses(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieves mandatory baseline clauses stored in the SQLite archive."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if category:
                cursor.execute(
                    "SELECT * FROM historical_treaty_clauses WHERE is_mandatory_baseline = 1 AND category = ?",
                    (category,)
                )
            else:
                cursor.execute("SELECT * FROM historical_treaty_clauses WHERE is_mandatory_baseline = 1")
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def get_baseline_clauses(self, treaty_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieves baseline clauses matching treaty name or all mandatory baselines."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if treaty_name:
                pattern = f"%{treaty_name}%"
                cursor.execute(
                    "SELECT * FROM historical_treaty_clauses WHERE treaty_name LIKE ? AND is_mandatory_baseline = 1",
                    (pattern,)
                )
            else:
                cursor.execute("SELECT * FROM historical_treaty_clauses WHERE is_mandatory_baseline = 1")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def get_events_by_region(self, region: str) -> List[Dict[str, Any]]:
        """Retrieves events matching a region."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            pattern = f"%{region}%"
            cursor.execute("SELECT * FROM events WHERE region LIKE ? ORDER BY date DESC", (pattern,))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def get_events_with_temporal_weights(
        self,
        reference_date: Optional[str] = None,
        half_life_days: float = 90.0,
        category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieves events annotated with exponential temporal decay weights w(t).
        Statutory/treaty categories are exempted from decay (tau = inf -> weight = 1.0).
        """
        import math
        from datetime import datetime
        from ..core.models import get_system_reference_date

        ref_dt = (
            datetime.strptime(str(reference_date)[:10], "%Y-%m-%d")
            if reference_date else get_system_reference_date()
        )
        if hasattr(ref_dt, "tzinfo") and ref_dt.tzinfo is not None:
            ref_dt = ref_dt.replace(tzinfo=None)

        with self._get_connection() as conn:
            cursor = conn.cursor()
            if category:
                cursor.execute("SELECT * FROM events WHERE category = ? ORDER BY date DESC", (category,))
            else:
                cursor.execute("SELECT * FROM events ORDER BY date DESC")
            rows = [dict(r) for r in cursor.fetchall()]

        for r in rows:
            cat = (r.get("category") or "").lower()
            evt_date_str = r.get("date") or ""
            is_statutory = any(k in cat for k in ["treaty", "legal", "statute", "sovereign_redline", "monetary_architecture"])
            if is_statutory or half_life_days <= 0 or math.isinf(half_life_days):
                r["temporal_decay_weight"] = 1.0
            else:
                try:
                    evt_dt = datetime.strptime(evt_date_str[:10], "%Y-%m-%d")
                    delta_days = max(0.0, (ref_dt - evt_dt).total_seconds() / 86400.0)
                    decay = math.exp(-(math.log(2.0) * delta_days) / half_life_days)
                    r["temporal_decay_weight"] = round(float(decay), 4)
                except Exception:
                    r["temporal_decay_weight"] = 1.0
        return rows


    def query_events(self, keyword: str) -> List[Dict[str, Any]]:
        """Queries historical events by keyword matching title, summary, or actors."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            pattern = f"%{keyword}%"
            cursor.execute("""
                SELECT * FROM events
                WHERE title LIKE ? OR summary LIKE ? OR actor LIKE ? OR civilizational_significance LIKE ?
                ORDER BY date DESC
            """, (pattern, pattern, pattern, pattern))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def insert_event(self, event_data: Dict[str, Any]) -> None:
        """Inserts an atomic event into the persistent SQLite store."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO events
                (event_id, date, title, actor, region, category, summary, civilizational_significance)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                event_data["event_id"],
                event_data.get("date", ""),
                event_data.get("title", ""),
                event_data.get("actor", ""),
                event_data.get("region", ""),
                event_data.get("category", "general"),
                event_data.get("summary", ""),
                event_data.get("civilizational_significance", "")
            ))
            conn.commit()

    def record_claim(self, claim: Any) -> None:
        """Persists an individual ClaimItem or telemetry dictionary into the persistent events table."""
        from ..core.models import get_system_reference_date
        ref_time = get_system_reference_date().strftime("%Y-%m-%d")
        claim_id = getattr(claim, "claim_id", None) or (claim.get("id") if isinstance(claim, dict) else "CLM-GEN")
        fact = getattr(claim, "asserted_fact", None) or (claim.get("text") if isinstance(claim, dict) else str(claim))
        ctype = getattr(claim, "claim_type", None)
        ctype_val = ctype.value if hasattr(ctype, "value") else str(ctype or "claim")
        actors = getattr(claim, "actors", []) or []
        actor_str = ", ".join(actors) if actors else "Multi-Lateral"
        lenses = getattr(claim, "target_lenses", []) or []

        self.insert_event({
            "event_id": f"EVT-{claim_id}",
            "date": getattr(claim, "date", None) or getattr(claim, "event_date", None) or ref_time,
            "title": f"Macro Telemetry: {ctype_val}",
            "actor": actor_str,
            "region": "Global / Macro",
            "category": ctype_val.lower(),
            "summary": fact,
            "civilizational_significance": f"Targeted Lenses: {', '.join(lenses)}" if lenses else ""
        })

    def match_anniversaries(self, month: int, day: Optional[int] = None) -> List[Dict[str, Any]]:
        """Matches historical turning points and anniversaries by month and optional day."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if day is not None:
                # Search within +/- 5 days of target date or matching month
                cursor.execute("""
                    SELECT * FROM historical_anniversaries
                    WHERE month = ? AND (day = ? OR ABS(day - ?) <= 7)
                    ORDER BY year ASC
                """, (month, day, day))
            else:
                cursor.execute("""
                    SELECT * FROM historical_anniversaries
                    WHERE month = ?
                    ORDER BY day ASC
                """, (month,))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def get_historical_anniversaries(self, limit: int = 500) -> List[Dict[str, Any]]:
        """Returns all historical turning points and sovereign anniversaries."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM historical_anniversaries
                ORDER BY anniversary_id ASC
                LIMIT ?
            """, (limit,))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def record_forecast(self, forecast_data: Dict[str, Any]) -> None:
        """Records a prospective calibrated forecast in the persistent SQLite ledger."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO forecast_ledger
                (forecast_id, created_at, target_date, event_name, hypothesis, predicted_probability,
                 confidence_interval_low, confidence_interval_high, epistemic_basis, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                forecast_data["forecast_id"],
                forecast_data.get("created_at", ""),
                forecast_data.get("target_date", ""),
                forecast_data.get("event_name", ""),
                forecast_data.get("hypothesis", ""),
                float(forecast_data.get("predicted_probability", 0.5)),
                float(forecast_data.get("confidence_interval_low", 0.3)),
                float(forecast_data.get("confidence_interval_high", 0.7)),
                forecast_data.get("epistemic_basis", "Multi-lens synthesis"),
                forecast_data.get("status", "ACTIVE")
            ))
            conn.commit()

    def resolve_forecast(self, forecast_id: str, actual_outcome: int) -> float:
        """
        Resolves an active forecast with its empirical binary outcome (0 or 1),
        calculates Brier score (predicted - actual)^2, and updates the ledger.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT predicted_probability FROM forecast_ledger WHERE forecast_id = ?", (forecast_id,))
            row = cursor.fetchone()
            if not row:
                raise ValueError(f"Forecast ID {forecast_id} not found in ledger.")
            prob = row["predicted_probability"]
            brier = round((prob - actual_outcome) ** 2, 4)
            cursor.execute("""
                UPDATE forecast_ledger
                SET actual_outcome = ?, brier_score = ?, status = 'RESOLVED'
                WHERE forecast_id = ?
            """, (actual_outcome, brier, forecast_id))
            conn.commit()
            return brier

    def get_forecast_ledger(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieves forecast ledger records."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if status:
                cursor.execute("SELECT * FROM forecast_ledger WHERE status = ? ORDER BY created_at DESC", (status,))
            else:
                cursor.execute("SELECT * FROM forecast_ledger ORDER BY created_at DESC")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def update_lens_reliability(self, lens_name: str, brier_error: float) -> float:
        """
        Updates the persistent Bayesian reliability multiplier for a specified lens.
        Multiplier formula: exp(-0.8 * mean_brier_error), clamped to [0.20, 1.50].
        """
        import math
        from datetime import datetime
        now_iso = datetime.now().isoformat()

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM lens_epistemic_reliability WHERE lens_name = ?", (lens_name,))
            row = cursor.fetchone()

            if row:
                count = row["total_evaluations"] + 1
                err_sum = row["brier_error_sum"] + brier_error
                mean_err = err_sum / count
                multiplier = max(0.20, min(1.50, round(math.exp(-0.8 * mean_err), 3)))
                cursor.execute("""
                    UPDATE lens_epistemic_reliability
                    SET total_evaluations = ?, brier_error_sum = ?, reliability_multiplier = ?, last_calibrated_at = ?
                    WHERE lens_name = ?
                """, (count, err_sum, multiplier, now_iso, lens_name))
            else:
                count = 1
                err_sum = brier_error
                multiplier = max(0.20, min(1.50, round(math.exp(-0.8 * brier_error), 3)))
                cursor.execute("""
                    INSERT INTO lens_epistemic_reliability
                    (lens_name, total_evaluations, brier_error_sum, reliability_multiplier, last_calibrated_at)
                    VALUES (?, ?, ?, ?, ?)
                """, (lens_name, count, err_sum, multiplier, now_iso))
            conn.commit()
            return multiplier

    def get_lens_reliability_multipliers(self) -> Dict[str, float]:
        """Returns mapping of lens_name -> reliability_multiplier (defaults to 1.0 for uncalibrated)."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT lens_name, reliability_multiplier FROM lens_epistemic_reliability")
                rows = cursor.fetchall()
                return {r["lens_name"]: float(r["reliability_multiplier"]) for r in rows}
            except Exception:
                return {}

    def recalibrate_epistemic_hyperparameters(
        self,
        prediction_id: str,
        brier_score: float,
        domain_tag: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Phase 69: Closed-Loop Empirical Bayes Recalibration.
        Dynamically adjusts the ALEDT distortion threshold (theta) and source credibility multipliers
        based on resolved real-world outcome accuracy.
        """
        base_theta = 0.50
        if brier_score > 0.35:
            # Overconfidence / High Error: Make the distortion filter more aggressive
            adjusted_theta = max(0.30, round(base_theta - 0.05 * (brier_score / 0.50), 3))
            action = "AGGRESSIVE_SIEVE_ENGAGED"
            confidence_penalty = round(min(0.25, (brier_score - 0.35) * 0.5), 3)
        elif brier_score < 0.10:
            # High Accuracy: Reinforce confidence and permit slight relaxation of threshold
            adjusted_theta = min(0.60, round(base_theta + 0.03, 3))
            action = "CALIBRATION_REINFORCED"
            confidence_penalty = 0.0
        else:
            adjusted_theta = base_theta
            action = "BASELINE_MAINTAINED"
            confidence_penalty = 0.0

        return {
            "prediction_id": prediction_id,
            "brier_score": round(brier_score, 4),
            "domain_tag": domain_tag or "general",
            "base_theta": base_theta,
            "adjusted_theta": adjusted_theta,
            "epistemic_action": action,
            "confidence_penalty": confidence_penalty,
            "closed_loop_learning_active": True
        }

    def save_wargame_session(self, session_data: Dict[str, Any], turns: Optional[List[Dict[str, Any]]] = None) -> str:
        """Persists a strategic wargame campaign session and associated turns to SQLite."""
        session_id = session_data.get("session_id") or f"SESSION-{os.urandom(4).hex()}"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO wargame_sessions
                (session_id, initiator, target, domain, action_summary, counter_summary, backlash_summary, equilibrium_payoff, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                session_id,
                session_data.get("initiator", ""),
                session_data.get("target", ""),
                session_data.get("domain", ""),
                session_data.get("action_summary", ""),
                session_data.get("counter_summary", ""),
                session_data.get("backlash_summary", ""),
                float(session_data.get("equilibrium_payoff", 0.0)),
                session_data.get("status", "COMPLETED"),
                session_data.get("created_at", "")
            ))
            if turns:
                for idx, t in enumerate(turns):
                    turn_id = t.get("turn_id") or f"{session_id}-T{t.get('turn_number', idx + 1)}"
                    cursor.execute("""
                        INSERT OR REPLACE INTO wargame_turns
                        (turn_id, session_id, turn_number, actor, domain, action_description, severity, payoff, details_json, created_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        turn_id,
                        session_id,
                        int(t.get("turn_number", idx + 1)),
                        t.get("actor", ""),
                        t.get("domain", ""),
                        t.get("action_description", ""),
                        float(t.get("severity", 0.0)),
                        float(t.get("payoff", 0.0)),
                        t.get("details_json", "{}"),
                        t.get("created_at", session_data.get("created_at", ""))
                    ))
            conn.commit()
            return session_id

    def get_wargame_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves a persistent wargame campaign session and all recorded turns."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM wargame_sessions WHERE session_id = ?", (session_id,))
            row = cursor.fetchone()
            if not row:
                return None
            session = dict(row)
            cursor.execute("SELECT * FROM wargame_turns WHERE session_id = ? ORDER BY turn_number ASC", (session_id,))
            turn_rows = cursor.fetchall()
            session["turns"] = [dict(tr) for tr in turn_rows]
            return session

    def list_wargame_sessions(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Lists recent persistent wargame campaigns."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM wargame_sessions ORDER BY created_at DESC LIMIT ?", (limit,))
            rows = cursor.fetchall()
            return [dict(r) for r in rows]

    def record_prediction(
        self,
        prediction_text: str,
        forecast_probability: float,
        domain: str = "general",
        lens_source: str = "",
        time_horizon_months: int = 12,
        session_label: str = ""
    ) -> str:
        """
        Records a new prediction in the cross-session scorecard.
        Returns the prediction_id for future outcome resolution.

        Cross-session Prediction Memory: bridges the engine's self-learning loop —
        predictions recorded here persist across all future conversations and can be
        resolved with actual outcomes to generate Brier score calibration feedback.
        """
        import hashlib
        from datetime import datetime, timezone
        now_str = datetime.now(timezone.utc).isoformat()
        pred_id = "PRED-" + hashlib.sha256(
            f"{prediction_text}{now_str}".encode("utf-8")
        ).hexdigest()[:10].upper()
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR IGNORE INTO prediction_scorecard
                (prediction_id, session_label, prediction_text, domain, lens_source,
                 forecast_probability, time_horizon_months, created_at, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'PENDING')
            """, (pred_id, session_label, prediction_text, domain, lens_source,
                  round(float(forecast_probability), 4), time_horizon_months, now_str))
            conn.commit()
        return pred_id

    def resolve_prediction(
        self,
        prediction_id: str,
        outcome_binary: int,
        outcome_description: str = ""
    ) -> Dict[str, Any]:
        """
        Resolves a pending prediction with the actual binary outcome (1=correct, 0=wrong).
        Calculates and persists the Brier score: (forecast_p - outcome)^2.
        Returns the resolved scorecard entry.
        """
        from datetime import datetime, timezone
        now_str = datetime.now(timezone.utc).isoformat()
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT prediction_id, forecast_probability FROM prediction_scorecard WHERE prediction_id = ?",
                (prediction_id,)
            )
            row = cursor.fetchone()
            if not row:
                return {"error": f"Prediction {prediction_id} not found"}
            fp = float(row["forecast_probability"])
            o = int(outcome_binary)
            brier = round((fp - o) ** 2, 4)
            cursor.execute("""
                UPDATE prediction_scorecard SET
                    outcome_recorded_at = ?,
                    outcome_description = ?,
                    outcome_binary = ?,
                    brier_score = ?,
                    status = 'RESOLVED'
                WHERE prediction_id = ?
            """, (now_str, outcome_description, o, brier, prediction_id))
            conn.commit()
            return {
                "prediction_id": prediction_id,
                "forecast_probability": fp,
                "outcome_binary": o,
                "brier_score": brier,
                "status": "RESOLVED"
            }

    def get_prediction_scorecard(self, status: str = "ALL", limit: int = 50) -> List[Dict[str, Any]]:
        """
        Returns the cross-session prediction history.
        status: 'ALL', 'PENDING', or 'RESOLVED'
        Sorted by creation date descending (most recent first).
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if status == "ALL":
                cursor.execute(
                    "SELECT * FROM prediction_scorecard ORDER BY created_at DESC LIMIT ?",
                    (limit,)
                )
            else:
                cursor.execute(
                    "SELECT * FROM prediction_scorecard WHERE status = ? ORDER BY created_at DESC LIMIT ?",
                    (status.upper(), limit)
                )
            rows = cursor.fetchall()
            return [dict(r) for r in rows]

    def get_chronology_anchors(self) -> List[Dict[str, Any]]:
        """
        Retrieves benchmark historical and civilizational chronology anchors
        used by the Multi-Pillar Chronology Arbiter (MPCA).
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT anniversary_id, year, event_title, region, historical_summary, strategic_mirror_significance
                FROM historical_anniversaries
                WHERE anniversary_id LIKE 'CHRONO-%'
                ORDER BY year ASC
            """)
            rows = cursor.fetchall()
            return [dict(r) for r in rows]

    def get_cosmic_chronology_anchors(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Retrieves canonical cosmic, astronomical, and epigraphic benchmarks
        from the cosmic_chronology_benchmarks table.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if category:
                cursor.execute("""
                    SELECT benchmark_id, category, canonical_source, primary_citation, temporal_epoch, duration_years, physical_basis, debunk_notes
                    FROM cosmic_chronology_benchmarks
                    WHERE category = ?
                    ORDER BY benchmark_id ASC
                """, (category,))
            else:
                cursor.execute("""
                    SELECT benchmark_id, category, canonical_source, primary_citation, temporal_epoch, duration_years, physical_basis, debunk_notes
                    FROM cosmic_chronology_benchmarks
                    ORDER BY benchmark_id ASC
                """)
            rows = cursor.fetchall()
            return [dict(r) for r in rows]

    def get_debunk_registry(self) -> List[Dict[str, Any]]:
        """
        Retrieves documented pseudo-historical, millenarian, and narrative warfare hoaxes.
        """
        return self.get_cosmic_chronology_anchors(category="hoax_registry")

    def record_diagnostic_encounter(
        self,
        entity_or_subject: str,
        query_text: str,
        primary_epistemic_tier: str,
        confidence: float,
        reality_ratio: float,
        propaganda_ratio: float,
        anomalies_detected: Optional[List[str]] = None,
        session_id: Optional[str] = None,
        brier_score: Optional[float] = None
    ) -> str:
        """
        Phase 71A: Longitudinal Diagnostic Memory.
        Records an epistemic diagnostic encounter for a subject, country, or leader,
        building an immutable clinical audit trail across multiple chat turns or sessions.
        """
        import hashlib, json
        from datetime import datetime, timezone
        now_str = datetime.now(timezone.utc).isoformat()
        enc_id = "ENC-" + hashlib.sha256(
            f"{entity_or_subject}{query_text}{now_str}".encode("utf-8")
        ).hexdigest()[:10].upper()
        anomalies_json = json.dumps(anomalies_detected or [])
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR IGNORE INTO diagnostic_longitudinal_records
                (encounter_id, session_id, entity_or_subject, query_text,
                 primary_epistemic_tier, confidence, reality_ratio, propaganda_ratio,
                 anomalies_detected, brier_score, diagnostic_timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                enc_id, session_id or "default_session", entity_or_subject.strip(), query_text.strip(),
                str(primary_epistemic_tier), round(float(confidence), 4),
                round(float(reality_ratio), 4), round(float(propaganda_ratio), 4),
                anomalies_json, round(float(brier_score), 4) if brier_score is not None else None,
                now_str
            ))
            conn.commit()
        return enc_id

    def get_longitudinal_diagnostic_chart(
        self,
        entity_or_subject: str,
        limit: int = 20
    ) -> Dict[str, Any]:
        """
        Phase 71A: Aggregates longitudinal diagnostic history for an entity/subject.
        Computes diagnostic stability, recurrent pathology flags, mean reality ratios,
        and estimates the risk of missed/incorrect diagnosis.
        """
        import json
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM diagnostic_longitudinal_records
                WHERE LOWER(entity_or_subject) = LOWER(?)
                ORDER BY diagnostic_timestamp DESC
                LIMIT ?
            """, (entity_or_subject.strip(), limit))
            rows = [dict(r) for r in cursor.fetchall()]

        if not rows:
            return {
                "entity_or_subject": entity_or_subject,
                "total_encounters": 0,
                "status": "NO_LONGITUDINAL_HISTORY",
                "misdiagnosis_risk_tier": "UNKNOWN",
                "diagnostic_stability_index": 0.0,
                "mean_reality_ratio": 0.0,
                "mean_confidence": 0.0,
                "chronic_anomalies": [],
                "encounters": []
            }

        total = len(rows)
        realities = [float(r["reality_ratio"]) for r in rows if r["reality_ratio"] is not None]
        confidences = [float(r["confidence"]) for r in rows if r["confidence"] is not None]
        mean_real = round(sum(realities) / len(realities), 4) if realities else 0.0
        mean_conf = round(sum(confidences) / len(confidences), 4) if confidences else 0.0

        # Calculate confidence variance / stability
        if len(confidences) > 1:
            var = sum((c - mean_conf) ** 2 for c in confidences) / len(confidences)
            stability = round(max(0.0, 1.0 - (var ** 0.5)), 4)
        else:
            stability = 1.0

        # Extract chronic anomalies
        anomaly_counts: Dict[str, int] = {}
        for r in rows:
            try:
                anoms = json.loads(r.get("anomalies_detected") or "[]")
                for a in anoms:
                    anomaly_counts[a] = anomaly_counts.get(a, 0) + 1
            except Exception:
                pass

        chronic = [k for k, v in anomaly_counts.items() if v >= 2 or (total == 1 and v >= 1)]

        # Estimate misdiagnosis risk
        if stability >= 0.85 and mean_conf >= 0.80:
            risk_tier = "LOW"
            misdiag_prob = 0.04
        elif stability >= 0.65:
            risk_tier = "MODERATE"
            misdiag_prob = 0.15
        else:
            risk_tier = "HIGH"
            misdiag_prob = 0.35

        return {
            "entity_or_subject": entity_or_subject,
            "total_encounters": total,
            "status": "LONGITUDINAL_CHART_ACTIVE",
            "mean_reality_ratio": mean_real,
            "mean_confidence": mean_conf,
            "diagnostic_stability_index": stability,
            "misdiagnosis_risk_tier": risk_tier,
            "estimated_misdiagnosis_probability": misdiag_prob,
            "chronic_anomalies": chronic,
            "recent_encounters": rows
        }

    # =========================================================================
    # PHASE 105: ASYNCHRONOUS MEDIA AUDIT WORKER JOB TRACKING
    # =========================================================================
    def create_media_job(self, job_id: str, source_url: str) -> None:
        """Initializes a new media audit background job in QUEUED status."""
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc).isoformat()
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO media_audit_jobs
                (job_id, source_url, status, progress_pct, result_json, error_message, created_at, completed_at)
                VALUES (?, ?, 'QUEUED', 0.0, NULL, NULL, ?, NULL)
            """, (job_id, source_url, now))

    def update_media_job(
        self,
        job_id: str,
        status: str,
        progress_pct: float = 0.0,
        result_json: Optional[str] = None,
        error_message: Optional[str] = None
    ) -> None:
        """Updates the status, progress, and results of a media audit job."""
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc).isoformat()
        completed_at = now if status in ("COMPLETED", "FAILED") else None
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE media_audit_jobs
                SET status = ?,
                    progress_pct = ?,
                    result_json = COALESCE(?, result_json),
                    error_message = COALESCE(?, error_message),
                    completed_at = COALESCE(?, completed_at)
                WHERE job_id = ?
            """, (status, progress_pct, result_json, error_message, completed_at, job_id))

    def get_media_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves current execution state of a media audit job."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM media_audit_jobs WHERE job_id = ?
            """, (job_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def list_media_jobs(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Lists recent media audit background jobs."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM media_audit_jobs
                ORDER BY created_at DESC
                LIMIT ?
            """, (limit,))
            return [dict(r) for r in cursor.fetchall()]

    def record_distilled_claim(self, claim_data: Dict[str, Any]) -> bool:
        """Persists an atomically distilled conversational/media claim into claim_distillations."""
        from datetime import datetime, timezone
        import json
        now = datetime.now(timezone.utc).isoformat()
        causal_str = json.dumps(claim_data.get("causal_relation")) if claim_data.get("causal_relation") else None
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO claim_distillations
                (claim_id, source_speaker, raw_statement, proposition, epistemic_tier, verification_status,
                 confidence, statutory_citation, fiscal_metric, causal_relation, recommended_action, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                claim_data["claim_id"],
                claim_data.get("source_speaker"),
                claim_data["raw_statement"],
                claim_data["proposition"],
                claim_data["epistemic_tier"],
                claim_data["verification_status"],
                float(claim_data["confidence"]),
                claim_data.get("statutory_citation"),
                claim_data.get("fiscal_metric"),
                causal_str,
                claim_data.get("recommended_action"),
                now
            ))
            return True

    def record_distillation_report(self, report_data: Dict[str, Any]) -> int:
        """Batch records all actionable claims from a DistillationReport."""
        claims = report_data.get("claims", [])
        recorded = 0
        for c in claims:
            if self.record_distilled_claim(c):
                recorded += 1
        return recorded

    def list_distilled_claims(
        self,
        tier: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Queries distilled claims with optional filtering by epistemic tier or verification status."""
        query = "SELECT * FROM claim_distillations WHERE 1=1"
        params: List[Any] = []
        if tier:
            query += " AND epistemic_tier = ?"
            params.append(tier)
        if status:
            query += " AND verification_status = ?"
            params.append(status)
        query += " ORDER BY created_at DESC LIMIT ?"
        params.append(limit)
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [dict(r) for r in cursor.fetchall()]

    def get_distilled_claim(self, claim_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves a single distilled claim by its unique ID."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM claim_distillations WHERE claim_id = ?", (claim_id,))
            row = cursor.fetchone()
            return dict(row) if row else None




