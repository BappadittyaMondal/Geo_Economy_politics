"""scripts/append_section_138_and_update_readme.py
Updates analysis_reports/README.md with Entry 14 and appends Section 138 to History_upgradation.md.
"""

import os

README_PATH = "analysis_reports/README.md"
HISTORY_PATH = "History_upgradation.md"

ENTRY_14_ROW = """| **2026-11-24 23:00** | [`2026-11-24_2300IST_CHINESE_MSS_COVERT_WARFARE_AND_INDIAN_SOVEREIGNTY_AUDIT.pdf`](2026-11-24_2300IST_CHINESE_MSS_COVERT_WARFARE_AND_INDIAN_SOVEREIGNTY_AUDIT.pdf) | **Chinese MSS Covert Warfare, Asymmetric Commercial Cyber-Espionage & Cognitive Perception Subversion:** Forensic investigative audit of Gaurav Thakur's documentary (`MkrfVSVO5m0`). Deconstructs the Guoanbu (MSS) architecture, Xi's 16-domain National Security Concept, the i-Soon commercial APT data leaks targeting Indian PMO/MHA/MEA/Reliance/Air India, the Dhaka-as-Delhi geo-spoofed cognitive perception laundering campaign, McLeodganj infiltration & Dalai Lama succession vector, the entomological ant colony chemical recognition metaphor for diaspora subversion, AMSC/GE industrial IP theft, Credibility Scorecard, Council Titans Directives, and Queued Phase 455 in UPGRADE_PLANING. | 10.3 KB | Section 193 (`CHINESE-MSS-COVERT-WARFARE`), `MkrfVSVO5m0` |
"""

SECTION_138_TEXT = """
## Section 138: Forensic Audit of Chinese MSS Asymmetric Warfare, i-Soon Commercial Cyber-Leaks, Cognitive Perception Laundering, Section 193 Ingestion & Phase 455 Queued

### 1. Architectural Motivation & Executive Summary
In direct response to the comprehensive strategic query requiring a microscopic DNA/RNA-level forensic analysis of the investigative documentary by Gaurav Thakur (*GetsetflySCIENCE*, `MkrfVSVO5m0`, 2049s), Section 193 was authored and ingested into `KNOWLEDGE_LIBRARY_GEO_POLITICS.md`. Re-indexing `data/events.db` via `scripts/build_knowledge_library.py` expanded the SQLite knowledge library to **193 discourses**. A publication-grade PDF dossier (`2026-11-24_2300IST_CHINESE_MSS_COVERT_WARFARE_AND_INDIAN_SOVEREIGNTY_AUDIT.pdf`, 10.3 KB) was compiled in `analysis_reports/` and mirrored to the conversation artifact directory. In strict adherence to the Zero Codebase Modification rule, `geo_engine/` and `tests/` code remained untouched, all previous upgrade phases (Phases 451–454) were preserved, and Phase 455 (`AsymmetricCommercialHackingAndPerceptionDistortionTensor`) was formally queued in `UPGRADE_PLANING` and `UPGRADE_PLANING.md`.

### 2. Multi-Domain Analytical Highlights
1. **Totalitarian Intelligence Architecture of the Guoanbu (MSS):** Unlike Western statutory models separating foreign human espionage (CIA) from domestic counter-intelligence (FBI), the MSS operates as an omnipotent secret service combining foreign espionage, domestic secret police, counter-intelligence, and ideological enforcement. Under Xi Jinping’s "Comprehensive National Security Concept" (总体国家安全观), national security spans 16 non-military domains (ideology, culture, technology, finance, and biology). Under Minister Chen Yixin, the MSS has launched public WeChat informant channels and enforced extraterritorial coercion.
2. **The i-Soon Data Leaks (Commercial APT Hacking):** The February 2024 GitHub leak of internal contractor records from i-Soon (Anxun Information Technology) exposed that China utilizes a commercial capitalist-bounty model, paying private hacking firms to breach foreign sovereign entities. The files proved successful intrusions into India's PMO, MHA, MEA, Ministry of Finance, Air India passenger manifests, Reliance telecom/energy infrastructure, and CRPF troop rotation registries in J&K and the North-East.
3. **Cognitive Perception Laundering (The "Dhaka-as-Delhi" Operation):** In late 2026, over 150 Chinese livestreamers operated out of Dhaka, Bangladesh, broadcasting urban squalor and open sewers while using VPN geo-spoofing and hashtags falsely claiming they were broadcasting live from "New Delhi, India". India's MEA officially called out this cognitive warfare operation, designed to damage India's international image and depress inbound tourism and FDI.
4. **The Entomological Metaphor (Chemical Scent Manipulation):** Gaurav Thakur leverages biological research (Boulay et al. 2004, Vásquez et al. 2008) showing that ants recognize nestmates by chemical cuticular scents; isolating an ant for 20 days shifts its scent, causing its own nestmates to execute it upon return. The MSS applies this to human intelligence by isolating diaspora scholars and dissidents from native support networks, altering their cognitive alignment, or using Operation Fox Hunt and illegal overseas police stations (102 worldwide) to coerce compliance.
5. **McLeodganj Infiltration & Tibetan Succession:** Persistent surveillance and illegal presence of Chinese police operatives near the Dalai Lama's residence in Dharamshala, aimed at manipulating the succession of the 15th Dalai Lama.
6. **Industrial IP Siphoning:** High-profile industrial espionage cases including the destruction of American Superconductor (AMSC) via Sinovel's code theft, GE Aviation composite blade theft by Yanjun Xu, and academic penetration via the Thousand Talents Plan (e.g., Charles Lieber).

### 3. Credibility Scorecard & Council Titan Synthesis
- **Scorecard:** Gaurav Thakur evaluated at 94% Logical Rigor, 8% Ideological Bias, 95% Ground Reality Alignment, and **94% Overall Objective Truth Score**.
- **Council Titans Directives:** Synthesized unified operational guidance across Dr. S. Jaishankar, NSA Ajit Doval, Dr. Ankit Shah, PM Narendra Modi, Sanjeev Sanyal, J Sai Deepak, and Dr. Anand Ranganathan in concise bullet points for ordinary citizens.

### 4. Phase 455 Staged in `UPGRADE_PLANING`
- **Module:** `AsymmetricCommercialHackingAndPerceptionDistortionTensor` in `geo_engine/lenses/deep_tech.py`, `institutional_lawfare.py`, and `geopolitical.py`.
- **Target Metric:** `asymmetric_cyber_commercial_and_perception_defense_score`.
- **Empirical Scale:** Expands system capacity from 255 to **260 resilience channels** across **271 lens symbols** upon future authorized execution.
"""

def update_readme():
    with open(README_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    
    table_header_marker = "| :--- | :--- | :--- | :--- | :--- |\n"
    if table_header_marker in content:
        parts = content.split(table_header_marker, 1)
        new_content = parts[0] + table_header_marker + ENTRY_14_ROW + parts[1]
        with open(README_PATH, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"[OK] Inserted Entry 14 into {README_PATH}")
    else:
        print("[WARN] Table header marker not found in README.md")

def update_history():
    with open(HISTORY_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = content.rstrip() + "\n\n" + SECTION_138_TEXT.strip() + "\n"
    with open(HISTORY_PATH, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"[OK] Appended Section 138 to {HISTORY_PATH}")

if __name__ == '__main__':
    update_readme()
    update_history()
