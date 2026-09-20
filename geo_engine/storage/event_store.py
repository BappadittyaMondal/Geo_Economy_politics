"""
Local SQLite Event Knowledge Base and Treaty Archive.
Provides zero-dependency persistent storage for historical events, bilateral treaties,
border agreements, and multilateral baseline communique clauses for negative-space diffing.
"""

import os
import sqlite3
from typing import Any, Dict, List, Optional


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
        else:
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
            conn.commit()

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
        conn = sqlite3.connect(self.db_path, timeout=10.0)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("PRAGMA journal_mode;")
        current_mode = cursor.fetchone()
        if current_mode and current_mode[0].lower() != "wal":
            conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA busy_timeout=5000;")
        return conn

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
                )
            ]

            cursor.executemany("""
                INSERT OR IGNORE INTO historical_anniversaries
                (anniversary_id, month, day, year, event_title, region, historical_summary, strategic_mirror_significance)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, anniversaries_seed)

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


