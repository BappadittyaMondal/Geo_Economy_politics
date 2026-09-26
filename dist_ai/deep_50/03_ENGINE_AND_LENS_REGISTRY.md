<!-- RAG_CONTEXT_HEADER
BUNDLE: Geo_Engine_Core_5
MODULE: 03_ENGINE_AND_LENS_REGISTRY.md
CANONICAL_COMMIT: 2d4a9e1
CANONICAL_REPO: https://github.com/BappadittyaMondal/Geo_Economy_politics.git
-->

# 03 ENGINE AND LENS REGISTRY
**Document Reference:** `LENS-REGISTRY-R20`  
**System Identity:** Geo-Economic & Geopolitical Intelligence Engine (`Geo_Economy_politics`)  
**Canonical Matrix Count:** **20 Analytical Lenses**  

---

## THE 20-LENS ANALYTICAL MATRIX SPECIFICATION

| ID | Analytical Lens Name | Tier | Primary Domain |
| :--- | :--- | :--- | :--- |
| L01 | Deep-Tech & Bayesian Confidence | Tier 1 | Bayesian NLP |
| L02 | World & Indian Diplomatic History | Tier 3 | Treaties & NAM |
| L03 | Civilizational Statecraft & Mandala | Tier 3 | Arthashastra |
| L04 | Geo-Economic Realism & Mundell-Fleming | Tier 2 | Macro-Currency |
| L05 | Geopolitical Realism & Multi-Alignment | Tier 3 | Balance of Power |
| L06 | Protocol-Subtracted Kinesics | Tier 4 | Proxemics/Photos |
| L07 | Real Cash Flow & 85% Haircut Rule | Tier 2 | Forensic CapEx |
| L08 | Propaganda & Narrative Warfare | Tier 5 | Media Spin |
| L09 | Petro-Logistics & Chokepoints | Tier 1 | Crude & Straits |
| L10 | Bureaucratic Inertia & Two-Level Games | Tier 3 | Permanent Civil |
| L11 | Digital Sovereignty & Compute Stack | Tier 1 | Silicon & NavIC |
| L12 | Hybrid & Covert Levers (Lawfare) | Tier 3 | FATF & Sub-Conv |
| L13 | India Strategic Timelines & Frontiers | Tier 3 | Himalayan LAC |
| L14 | Demographic Infiltration & Corridors | Tier 1 | Migration Arms |
| L15 | Critical Minerals & Refining Monopolies | Tier 1 | HREE & Precursor |
| L16 | Institutional Lawfare & OFAC Sanctions | Tier 2 | Asset Freezes |
| L17 | Food Security & Caloric Sovereignty | Tier 1 | Fertilizer & FCI |
| L18 | Military Readiness, ORBAT & Deterrence | Tier 1 | WWR Ammunition |
| L19 | Subsea Cables & Hydro-Spatial Sovereignty | Tier 1 | Subsea & Mining |
| L20 | Astro-Politics & Counter-Space Deterrence | Tier 1 | LEO & Kinetic ASAT |

---

## DETAILED LENS SPECIFICATIONS

### L01: Deep-Tech & Bayesian Confidence Lens
- **Purpose:** Entity resolution, Bayesian confidence scoring, and sentiment-reality delta audit.
- **Inputs:** `SummitEvent`, `claims: Optional[List[ClaimItem]]`.
- **Metrics:** `entity_resolution_score`, `bayesian_confidence_discount`, `sentiment_reality_delta`.

### L02: World & Indian Diplomatic History Lens
- **Purpose:** Audits events against long-cycle diplomatic precedents (Bandung 1955, NAM, 1971 Indo-Soviet Treaty).
- **Inputs:** `SummitEvent`.
- **Metrics:** `historical_precedent_index`, `non_alignment_continuity_score`.

### L03: Civilizational Statecraft & Mandala Lens
- **Purpose:** Evaluates statecraft through Kautilya’s *Arthashastra*, the *Raja Mandala* (Ari, Mitra, Madhyama, Udasina), *Rajdharma*, and *Yogakshema*.
- **Metrics:** `kautilyan_mandala_balance`, `civilizational_cohesion_score`.

### L04: Geo-Economic Realism & Mundell-Fleming Lens
- **Purpose:** Audits de-dollarization and currency proposals against the Mundell-Fleming Trilemma.
- **Metrics:** `trilemma_violation_flag`, `de_dollarization_level_feasibility`.

### L05: Geopolitical Realism & Multi-Alignment Lens
- **Purpose:** Audits strategic autonomy, multi-alignment hedging, and intra-bloc zero-sum rivalries.
- **Metrics:** `strategic_autonomy_index`, `intra_bloc_friction_score`.

### L06: Protocol-Subtracted Kinesics Lens
- **Purpose:** Strips away staged photoshoot bonhomie; calculates genuine bilateral warmth.
- **Safeguard:** Text claims lacking visual vectors enter `TIER_0_INSUFFICIENT_EVIDENCE`.
- **Metrics:** `protocol_subtracted_warmth`, `micro_tension_index`.

### L07: Real Cash Flow & 85% Haircut Rule Lens
- **Purpose:** Enforces 85% haircut on unfinanced MOUs and sanctions risk discount.
- **Mathematical Clamping Gate:** $\min(1.0, 0.15 + 0.85 \times \text{CapEx Ratio})$.
- **Metrics:** `total_nominal_announced_usd`, `total_effective_capex_usd`, `aggregate_haircut_percentage`.

### L08: Propaganda & Narrative Warfare Lens
- **Purpose:** Deconstructs communiqués across domestic audiences (Beijing, Moscow, New Delhi, Washington).
- **Metrics:** `domestic_narrative_divergence_score`, `media_coordination_index`.

### L09: Petro-Logistics & Chokepoints Lens
- **Purpose:** Evaluates physical crude diversions, shadow tanker fleets, and maritime straits (Hormuz, Malacca).
- **Metrics:** `physical_crude_diversion_bpd`, `shadow_tanker_dependence_pct`, `western_pi_insurance_choke_pct`.

### L10: Bureaucratic Inertia & Two-Level Games Lens
- **Purpose:** Models Putnam’s Two-Level Game and permanent civil service filters (Press Note 3, MEA, NDRC).
- **Metrics:** `two_level_ratification_feasibility`, `bureaucratic_drag_score`.

### L11: Digital Sovereignty & Compute Stack Lens
- **Purpose:** Audits semiconductor supply chains, telecom clean-core bans (Huawei ban), and NavIC satellite positioning.
- **Metrics:** `compute_sovereignty_index`, `telecom_clean_core_compliance`.

### L12: Hybrid & Covert Levers (Lawfare) Lens
- **Purpose:** Audits FATF mutual evaluations, extraterritorial intelligence shielding, and non-kinetic leverage.
- **Metrics:** `fatf_regulatory_exposure_score`, `asymmetric_leverage_index`.

### L13: India Strategic Timelines & Frontiers Lens
- **Purpose:** Tracks post-1947 Himalayan boundary trajectories, 1993/1996 LAC CBMs, and neighborhood corridors.
- **Metrics:** `boundary_protocol_compliance_score`, `neighborhood_first_alignment_score`.

### L14: Demographic Infiltration & Migration Corridors Lens
- **Purpose:** Evaluates engineered migration, transit bridges, and strategic corridor vulnerabilities (Siliguri neck, Ceuta).
- **Metrics:** `border_transit_vulnerability_score`, `demographic_leverage_index`.

### L15: Critical Minerals & Refining Monopolies Lens
- **Purpose:** Evaluates Heavy Rare Earth Elements (HREE) refining monopolies, lithium processing, and export controls on Gallium/Germanium/Antimony.
- **Metrics:** `hree_refining_concentration_pct`, `semiconductor_precursor_vulnerability`, `material_sovereignty_index`.

### L16: Institutional Lawfare & OFAC Sanctions Lens
- **Purpose:** Deconstructs FATF grey-listing timing, OFAC secondary sanctions, and sovereign reserve confiscation risk.
- **Metrics:** `ofac_secondary_sanctions_risk_score`, `sovereign_asset_confiscation_risk`.

### L17: Food Security & Caloric Sovereignty Lens
- **Purpose:** Evaluates fertilizer import dependencies (MOP 100%, DAP ~60%, Urea), FCI grain buffer stock ratios ($1.82\times$), and caloric welfare commitments.
- **Metrics:** `caloric_sovereignty_index`, `strategic_grain_buffer_ratio`, `mop_potash_import_dependency_pct`.

### L18: Military Readiness, ORBAT & Deterrence Lens
- **Purpose:** Audits dual-front ORBAT posture, War Wastage Reserves (WWR) ammunition stocking depth (21.5 days), defense indigenization, and S-400/IADS air defense saturation.
- **Metrics:** `two_front_deterrence_posture_score`, `wwr_ammunition_reserve_days`, `iads_air_defense_coverage_index`.

### L19: Subsea Cables & Hydro-Spatial Sovereignty Lens
- **Purpose:** Audits deep-sea fiber-optic cable landing stations (Mumbai, Chennai), seabed mining of polymetallic nodules, and hydrophone choke monitoring in the Indian Ocean / Andaman Sea.
- **Metrics:** `subsea_bandwidth_dependency_pct`, `hydro_spatial_sovereignty_score`, `seabed_mining_concession_status`.

### L20: Astro-Politics & Counter-Space Deterrence Lens
- **Purpose:** Audits Low Earth Orbit (LEO) mega-constellations, sovereign PNT autonomy (NavIC vs. GPS denial), space domain awareness (NETRA), and kinetic/non-kinetic ASAT deterrence.
- **Metrics:** `satcom_sovereignty_coverage_pct`, `orbital_sovereignty_index`, `counter_space_deterrence_posture`.
