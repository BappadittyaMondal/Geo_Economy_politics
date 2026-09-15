# 01 SYSTEM ARCHITECTURE
**Document Reference:** `SYSTEM-ARCH-V3.0`  
**System Identity:** Geo-Economic & Geopolitical Intelligence Engine (`Geo_Economy_politics`)  
**Canonical Repository:** `https://github.com/BappadittyaMondal/Geo_Economy_politics.git` (Branch: `main`)  

---

## 1. END-TO-END DATA PIPELINE TOPOLOGY

The engine transforms raw, unverified natural language text and ingested open-source feeds into arbitrated, mathematically grounded strategic intelligence through an unbroken execution pipeline:

```
[USER QUERY / INGESTED OPEN-SOURCE TELEMETRY]
                       │
                       ▼
          1. Dynamic Query Parser (QueryParser)
             - 5000-char input envelope cap
             - Disambiguates SUMMIT vs BORDER_MILITARY vs BORDER_SECURITY vs CIVILIZATIONAL_CRISIS
                       │
                       ▼
          2. Stage 0 Ingestion Normalizer (IngestionNormalizer)
             - SHA-256 wire deduplication across syndicated stories
             - Multi-currency extraction (€, £, ₹, $) normalized to USD
             - Extracts ClaimItem records with target_lenses routing
                       │
                       ▼
          3. Local Knowledge Base & Treaty Archive (EventStore / events.db)
             - SQLite with PRAGMA journal_mode=WAL; and busy_timeout=5000
             - Mandatory baseline clauses for negative space diffing
             - Historical turning points & anniversaries (711, 1492, 1971, 1993, 2024)
                       │
                       ▼
          4. Epistemic Arbitration Engine (EpistemicArbitrator)
             - Deterministic 5-Tier Truth Priority (Tier 1 Physical > Tier 5 Communique)
             - Enforces 85% MOU haircut on unfinanced declarations
             - Enforces text-only safeguard on kinesic claims (TIER_0)
                       │
                       ▼
          5. The 18-Lens Analytical Matrix (LENS_REGISTRY)
             - Evaluates physical, financial, sovereign, and narrative layers
             - Dynamic signature inspect.signature parameter claim injection
             - Outputs LensEvaluation objects with confidence & hard metrics
                       │
                       ▼
          6. Negative Space Diff Engine (NegativeSpaceDiffEngine)
             - Diff against baseline clauses (UNSC seats, currency, terror, UNCLOS)
             - Categorizes clauses into omitted, diluted, or retained
                       │
                       ▼
          7. Master Multi-Tier Synthesizer (SummitSynthesizer)
             - Epistemic Tier-Weighted Confidence Calculation
             - Decoupled Dynamic Country Ledgers (10-country sovereign audits)
             - Strategic Resilience Matrix (caloric, military, mineral, lawfare)
             - Civilizational & Kautilyan Inner Meaning Synthesis
                       │
                       ▼
          8. Persona Archetype Projection Layer (PersonaNarrator)
             - Projects arbitrated truth through 5 distinct doctrinal traditions
             - Sanyal, Jaishankar, Shah, Doval, Ranganathan with legal disclaimers
                       │
                       ▼
          9. Calibrated Forecasting Engine (ForecastingEngine)
             - Reliability-weighted Bayesian scenario probability updating
             - MECE scenario branches summing strictly to 1.0
             - Deterministic SHA-256 forecast IDs (FCST-{year}-{hash[:8]})
                       │
                       ▼
          10. Rich Terminal CLI / Publisher (cli.py & morning_digest/)
             - Windows UTF-8 console safe rendering
             - 5-tier rich tables, resilience matrix panel, persona profile
             - Token-sanitized Telegram broadcast daemon
```

---

## 2. SUBSYSTEM BOUNDARIES & INTERACTION CONTRACTS

1. **Ingestion $\rightarrow$ Arbitration Boundary:** Raw text claims are normalized into immutable `ClaimItem` records. Unverified wire reports receive `reliability_weight = 0.0`.
2. **Arbitration $\rightarrow$ Lenses Boundary:** Claims are filtered via `ClaimItem.target_lenses` so each lens receives only relevant empirical assertions.
3. **Lenses $\rightarrow$ Synthesizer Boundary:** All 18 lenses output `LensEvaluation` records. The synthesizer calculates composite confidence using epistemic tier weights, preventing narrative PR lenses from dragging down verified physical data.
4. **Synthesizer $\rightarrow$ Forecasting Boundary:** Scenarios are updated via reliability-weighted Bayesian updating; claims with zero reliability cause zero probability shift.
5. **Synthesizer $\rightarrow$ Presentation Boundary:** Persona narration applies prioritized lens multipliers without modifying the underlying factual arbitration log.

---

## 3. TEMPORAL GUARDRAIL & HORIZON CLASSIFICATION

Every analyzed event is classified into one of three temporal modes:
1. `EMPIRICAL_HISTORICAL`: Past verified events with full archival data.
2. `LIVE_VERIFIED`: Ongoing events with real-time ingested feeds.
3. `PROSPECTIVE_SCENARIO`: Horizon events (e.g., 2026) modeled game-theoretically. All prospective statements are tagged `[PROSPECTIVE_SCENARIO]` to prevent future-data hallucinations.
