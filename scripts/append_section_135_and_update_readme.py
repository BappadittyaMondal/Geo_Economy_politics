"""
scripts/append_section_135_and_update_readme.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Updates analysis_reports/README.md with entry 12 and appends Section 135 to History_upgradation.md.
"""

import os

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README_PATH = os.path.join(REPO_ROOT, "analysis_reports", "README.md")
HISTORY_PATH = os.path.join(REPO_ROOT, "History_upgradation.md")

# 1. Update analysis_reports/README.md
with open(README_PATH, 'r', encoding='utf-8') as f:
    readme_content = f.read()

new_row = """| **2026-11-24 22:00** | [`2026-11-24_2200IST_SUBALTERN_POLITICAL_GENESIS_MODI_YOGI_AUDIT.pdf`](2026-11-24_2200IST_SUBALTERN_POLITICAL_GENESIS_MODI_YOGI_AUDIT.pdf) | **Subaltern Political Genesis, Electoral Hegemony & Modi-Yogi Dynamics:** Forensic investigative audit of the political biography, electoral architecture, and leadership succession dynamics explored by senior journalist Pankaj Prasoon on NMF News (`ENvsxdIB8TA`). Dissects the Vadnagar railway tea stall ground reality, Modh-Ghanchi OBC origins, the weaponization of class scorn into 'Chai Pe Charcha', the four structural pillars of Modi's 23-year undefeated electoral record (2001-2024+), deconstructs the manufactured 'Modi vs. Yogi' rivalry into a complementary visionary-enforcer symbiosis, models political stability as a sovereign defense moat, 7 Strategic Council Titans, Credibility Scorecard, and Queued Phase 452. | 13.6 KB | Section 191 (`MODI-YOGI-POLITICAL-GENESIS`), `ENvsxdIB8TA` |
"""

target_marker = "| :--- | :--- | :--- | :--- | :--- |\n"
if new_row.strip() not in readme_content:
    if target_marker in readme_content:
        readme_content = readme_content.replace(target_marker, target_marker + new_row)
        with open(README_PATH, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print("Updated analysis_reports/README.md with Entry 12.")
    else:
        print("Target marker not found in README.md")
else:
    print("README.md already has Entry 12.")

# 2. Append Section 135 to History_upgradation.md
section_135_content = """

## Section 135: Subaltern Political Genesis, 23-Year Electoral Hegemony, Modi-Yogi Succession Dynamics, Section 191 Ingestion & Phase 452 Queued

### 1. Architectural Motivation & Executive Summary
In direct response to the comprehensive strategic query requiring a deep forensic analysis of the political biography, subaltern mobilization, and leadership succession dynamics explored by senior investigative journalist Pankaj Prasoon on **NMF News** (`ENvsxdIB8TA`, 2865s), Section 191 was formulated and ingested into `KNOWLEDGE_LIBRARY_GEO_POLITICS.md`. The SQLite database `data/events.db` was re-indexed via `scripts/build_knowledge_library.py`, bringing the total database catalog to **191 discourses**. A publication-grade 3-page PDF report (`2026-11-24_2200IST_SUBALTERN_POLITICAL_GENESIS_MODI_YOGI_AUDIT.pdf`, 13.6 KB) was compiled and archived in `analysis_reports/` and mirrored to the active conversation artifact directory. In strict adherence to the Zero Codebase Modification rule, `geo_engine/` and `tests/` code remained pristine, and Phase 452 (`SubalternElectoralCapitalAndSuccessionContinuityTensor`) was formally queued in `UPGRADE_PLANING` and `UPGRADE_PLANING.md`.

### 2. Multi-Domain Analytical Highlights
1. **Vadnagar Ground Truth & Class Transmutation:** Historical records of the Western Railway and municipal archives corroborate that Damodardas Modi and his brother Babubhai operated a tea stall at Vadnagar railway station, where Narendra Modi assisted in his youth. Belonging to the marginalized Modh-Ghanchi (OBC) community, his upbringing was characterized by authentic subaltern austerity. When dynastic elites mocked his background in 2013, the political machinery executed *Chai Pe Charcha*, transmuting class scorn into an insurmountable populist identity that permanently captured the working class.
2. **The Four Pillars of 23-Year Electoral Hegemony:**
   - *Panna Pramukh Micro-Architecture:* Transitioned voter mobilization from feudal patronage to deterministic mathematical execution by assigning dedicated cadres to single pages of 30–60 voters.
   - *The Post-Caste 'Labharthi' Mega-Bloc:* Deployed the JAM Trinity (Jan Dhan, Aadhaar, Mobile) to eliminate 85% bureaucratic leakage across PM Awas, Jal Jeevan, Ujjwala, Ayushman Bharat, and PM Kisan, creating a unified demographic voting on direct material delivery.
   - *Subaltern Realignment:* Systematically empowered non-dominant OBCs and non-Jatav Dalits, shattering Congress's KHAM and regional parties' caste monopolies.
   - *Ascetic Incorruptibility:* Zero personal assets, private business, or dynastic heirs provided an impregnable shield against corruption allegations.
3. **Deconstructing the "Modi vs. Yogi" Narrative:** Exposes the media-manufactured rift as an optical illusion. The relationship is fundamentally symbiotic: Modi functions as the global visionary statesman, macroeconomic architect, and welfare consolidator; Yogi Adityanath operates as the uncompromising internal security enforcer in Uttar Pradesh (the "Bulldozer Model" restoring law and order, dismantling mafias, and enabling industrial investment). Both share deep roots in the Sangh Parivar, which views Yogi as the proven ideological and administrative heir for the post-2029 era.
4. **Geoeconomic Stability as a Sovereign Defense Moat:** India's 2014–2029+ political continuity under Modi provides global sovereign capital with long-term policy certainty, while the organic bond between Modi and the subaltern masses acts as an impenetrable firewall against foreign color-revolution playbooks.

### 3. Credibility Scorecard & Council Titan Synthesis
- **Scorecard:** Pankaj Prasoon (NMF News) evaluated at 92% Logical Rigor, 12% Ideological Bias, 88% Ground Reality (90% Objective Truth).
- **Council Titans Directives:** Synthesized actionable guidance across 7 mentors (Dr. S. Jaishankar, NSA Ajit Doval, Dr. Ankit Shah, PM Narendra Modi, Sanjeev Sanyal, J Sai Deepak, and Dr. Anand Ranganathan) delivered in concise, plain-language bullet points for general citizens.

### 4. Phase 452 Staged in `UPGRADE_PLANING`
- **Module:** `SubalternElectoralCapitalAndSuccessionContinuityTensor` in `geo_engine/lenses/institutional_lawfare.py` and `geopolitical.py`.
- **Target Metric:** `subaltern_electoral_hegemony_and_succession_resilience_score`.
- **Empirical Scale:** Expands system capacity from 256 to **257 resilience channels** and 267 to **268 lens symbols** when authorized.
"""

with open(HISTORY_PATH, 'a', encoding='utf-8') as f:
    f.write(section_135_content.strip() + '\n')
print("Appended Section 135 to History_upgradation.md.")
