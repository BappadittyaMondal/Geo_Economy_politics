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

