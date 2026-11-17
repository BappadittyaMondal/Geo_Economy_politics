"""
scripts/build_knowledge_library.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Automated Modularization, SQLite Ingestion & Two-Tier Canonical Compiler
for the Bharat-Centric Sovereign Knowledge Matrix (BSKM).

Ensures:
1. Zero test regressions: Root KNOWLEDGE_LIBRARY_GEO_POLITICS.md is preserved.
2. Lightweight modular files in knowledge_library/ for fast AI & human editing.
3. Master Index & Router with Video IDs and Council Mentor cross-referencing.
4. SQLite knowledge_discourses indexing in data/events.db for instant CLI retrieval.
"""

import os
import re
import sys
from typing import Dict, List, Tuple, Optional

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from geo_engine.storage.event_store import EventStore

ROOT_LIB = os.path.join(REPO_ROOT, "KNOWLEDGE_LIBRARY_GEO_POLITICS.md")
KNOW_DIR = os.path.join(REPO_ROOT, "knowledge_library")

DOMAIN_FILES = {
    "01_SANATAN_CIVILIZATIONAL_EPISTEMOLOGY.md": "Vedic & Sanatan Civilizational Epistemology, Shastras & Historiography",
    "02_INVISIBLE_CASH_FLOW_AND_GEO_ECONOMICS.md": "Invisible Cash Flow, Shadow Banking, Bullion & Geo-Economic Realism",
    "03_GEOPOLITICAL_REALPOLITIK_AND_DEFENSE.md": "Geopolitical Realpolitik, Border Defense, Multipolar Balance & ORBAT",
    "04_HYBRID_WARFARE_AND_COVERT_SUBVERSION.md": "Hybrid Warfare, Deep State Subversion, Honeytraps & Mobocracy",
    "05_DEEP_TECH_AND_DIGITAL_SOVEREIGNTY.md": "Deep-Tech Sovereignty, Compute, Semiconductors & Critical Minerals",
    "06_COGNITIVE_WARFARE_AND_LAWFARE.md": "Cognitive Warfare, Media Deconstruction, Edutainment & Institutional Lawfare",
}

COUNCIL_MENTORS = [
    "Ajit Doval", "Dr. S. Jaishankar", "Dr. Ankit Shah", "Sanjeev Sanyal", 
    "J. Sai Deepak", "Dr. Anand Ranganathan", "PM Narendra Modi", "Vikram Singh",
    "Ami Ganatra", "Neeraj Atri", "Meenakshi Jain", "Sadhguru", "Abhijit Chavda",
    "Major Gaurav Arya", "Brahma Chellaney", "Kapil Komireddi", "Rishabh Bidhuri"
]

def classify_section(title: str, body: str) -> str:
    t = (title + " " + body[:600]).lower()
    if any(k in t for k in [
        "purusha sukta", "vyadha gita", "vedanta", "prasthanatrayi", "ramayana",
        "shankaracharya", "mandana", "shastrartha", "varna", "manusmriti",
        "agnihotra", "sandhyavandanam", "spiritual diplomacy", "ayodhya",
        "temple", "epigraphy", "sanatan", "dharmashastra", "odisha", "garuda purana"
    ]):
        return "01_SANATAN_CIVILIZATIONAL_EPISTEMOLOGY.md"
    if any(k in t for k in [
        "cash flow", "debt", "bank", "bis", "swap", "fiat", "blackrock", "aladdin",
        "vanguard", "rwa", "tokenization", "pboc", "lgfv", "gold", "bullion",
        "currency", "msme", "gdp", "informal economy", "tax haven", "p-note",
        "pnote", "capex", "turkey", "fund freeze", "housing", "balance-sheet"
    ]):
        return "02_INVISIBLE_CASH_FLOW_AND_GEO_ECONOMICS.md"
    if any(k in t for k in [
        "lac", "border", "aksai chin", "nyoma", "yalta", "condominium", "military",
        "iaf", "radar", "navy", "pns hunain", "air defense", "patriot", "drone",
        "scramjet", "hypersonic", "nuclear", "air india one", "deterrence", "orbat",
        "taiwan", "escort", "missile", "subsea", "chokepoint", "strait", "cbrn"
    ]):
        return "03_GEOPOLITICAL_REALPOLITIK_AND_DEFENSE.md"
    if any(k in t for k in [
        "mk-ultra", "cia", "isi", "honeytrap", "kamopadha", "mobocracy", "street veto",
        "granovetter", "color revolution", "subversion", "khalistan", "doval", "covert",
        "espionage", "infiltration", "sanctuary", "regime change", "astroturfing",
        "netaji bose", "crime-terror", "d-company"
    ]):
        return "04_HYBRID_WARFARE_AND_COVERT_SUBVERSION.md"
    if any(k in t for k in [
        "deep-tech", "semiconductor", "jio", "volte", "grok", "ai algorithmic",
        "server water", "crowdstrike", "cloud", "quantum", "scada", "microcode",
        "uranium", "darpa", "microprocessor", "rare earth", "gallium", "lithium", "isro"
    ]):
        return "05_DEEP_TECH_AND_DIGITAL_SOVEREIGNTY.md"
    return "06_COGNITIVE_WARFARE_AND_LAWFARE.md"


def modularize_and_index_library(store: Optional[EventStore] = None):
    """Parses root canonical library, writes topic dossiers and indexes discourses into SQLite."""
    if not os.path.exists(ROOT_LIB):
        print(f"[ERROR] Cannot find root file: {ROOT_LIB}")
        return

    with open(ROOT_LIB, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    os.makedirs(KNOW_DIR, exist_ok=True)

    matches = list(re.finditer(r"^(## (?:SECTION \d+|\d+\.|\bSection \d+\b)[^\n]+)", text, re.MULTILINE))
    if not matches:
        print("[ERROR] No section headers matched in library!")
        return

    categorized: Dict[str, List[Tuple[str, str]]] = {fname: [] for fname in DOMAIN_FILES}
    video_registry = []
    indexed_count = 0

    if store is None:
        store = EventStore()

    for i in range(len(matches)):
        start = matches[i].start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        title_raw = matches[i].group(0)
        body = text[start:end].strip()

        # Section number
        sm = re.search(r'(?:SECTION|Section)\s+(\d+)|(\d+)\.', title_raw)
        sec_num = int(sm.group(1) or sm.group(2)) if sm else (i + 1)

        # Video ID if present
        v_match = re.search(r"`([A-Za-z0-9_-]{11})`", title_raw)
        vid_id = v_match.group(1) if v_match else "N/A"
        
        target_file = classify_section(title_raw, body)
        categorized[target_file].append((title_raw, body))
        video_registry.append((title_raw, vid_id, target_file))

        # Council Mentors
        detected_mentors = [
            m for m in COUNCIL_MENTORS
            if m.lower() in (title_raw + " " + body).lower()
        ]
        council_str = ", ".join(detected_mentors) if detected_mentors else "Sovereign Statecraft Council"

        # Speaker detection
        speaker = "General Epistemology"
        t_clean = re.sub(r"^##\s*(?:SECTION|Section|\d+\.)\s*\d*[:\.]?\s*", "", title_raw).strip()
        if "—" in t_clean:
            cand = t_clean.split("—")[0].strip()
            if len(cand) < 45:
                speaker = cand
        elif "-" in t_clean:
            cand = t_clean.split("-")[0].strip()
            if len(cand) < 45:
                speaker = cand
        if speaker == "General Epistemology" and detected_mentors:
            speaker = detected_mentors[0]

        # Thesis detection
        thesis_m = re.search(r'(?:Key Thesis|Core Thesis|Thesis|Main Argument):\s*([^\n]+)', body, re.IGNORECASE)
        if thesis_m:
            key_thesis = thesis_m.group(1).strip()
        else:
            prose_lines = [l.strip() for l in body.split("\n") if l.strip() and not l.startswith("#") and not l.startswith("|") and not l.startswith(">")]
            key_thesis = prose_lines[0][:280] if prose_lines else t_clean

        # Strategic doctrine detection
        doc_m = re.search(r'(?:Strategic Doctrine|Doctrine|Strategic Significance|Civilizational Significance|Geo-Economic Significance):\s*([^\n]+)', body, re.IGNORECASE)
        if doc_m:
            strategic_doctrine = doc_m.group(1).strip()
        else:
            strategic_doctrine = f"Sovereign doctrine aligned with {DOMAIN_FILES[target_file]}."

        discourse_id = f"DISCOURSE-{sec_num:03d}" if vid_id == "N/A" else f"DISCOURSE-{sec_num:03d}-{vid_id}"

        # SQLite upsert
        store.upsert_knowledge_discourse(
            discourse_id=discourse_id,
            section_number=sec_num,
            title=title_raw.replace("## ", "").strip(),
            domain_category=DOMAIN_FILES[target_file],
            council_members=council_str,
            source_speaker=speaker,
            key_thesis=key_thesis,
            strategic_doctrine=strategic_doctrine,
            content_markdown=body
        )
        indexed_count += 1

    # 1. Write each categorized domain file
    for fname, sections in categorized.items():
        fpath = os.path.join(KNOW_DIR, fname)
        desc = DOMAIN_FILES[fname]
        content = [
            f"# BSKM DOMAIN DOSSIER: {desc.upper()}",
            f"> Canonical Sub-Dossier of the Bharat-Centric Sovereign Knowledge Matrix.",
            f"> Source: `knowledge_library/{fname}` | Sections: {len(sections)}\n",
            "---\n"
        ]
        for title, body in sections:
            content.append(body)
            content.append("\n---\n")

        with open(fpath, "w", encoding="utf-8") as f_out:
            f_out.write("\n".join(content))
        print(f"[GENERATED] {fname}: {len(sections)} sections ({os.path.getsize(fpath):,} bytes)")

    # 2. Write 00_MASTER_INDEX_AND_ROUTER.md
    index_path = os.path.join(KNOW_DIR, "00_MASTER_INDEX_AND_ROUTER.md")
    index_content = [
        "# BSKM: MASTER EPISTEMIC INDEX & ROUTING MATRIX",
        "> Central Navigational Compass for the 157+ Multi-Domain Video Intelligence Dossiers.",
        f"> Total Indexed Dossiers: {len(matches)} | Domain Files: {len(DOMAIN_FILES)}\n",
        "## 1. Domain Dossier Inventory\n",
        "| File | Domain Name | Sections Covered |",
        "| :--- | :--- | :--- |"
    ]
    for fname, desc in DOMAIN_FILES.items():
        cnt = len(categorized[fname])
        index_content.append(f"| [`{fname}`]({fname}) | {desc} | {cnt} sections |")

    index_content.append("\n## 2. Complete Chronological Video & Section Registry\n")
    index_content.append("| Section Header | Video ID | Target Domain File |")
    index_content.append("| :--- | :--- | :--- |")
    for title, vid, tgt in video_registry:
        t_clean = title.replace("|", "\\|").replace("## ", "")
        index_content.append(f"| {t_clean} | `{vid}` | [`{tgt}`]({tgt}) |")

    with open(index_path, "w", encoding="utf-8") as f_idx:
        f_idx.write("\n".join(index_content))
    print(f"[GENERATED] 00_MASTER_INDEX_AND_ROUTER.md ({os.path.getsize(index_path):,} bytes)")
    print(f"[INDEXED] Successfully ingested {indexed_count} video discourses into SQLite events.db.")


def compile_root_library():
    """Verifies that the canonical root KNOWLEDGE_LIBRARY_GEO_POLITICS.md is intact."""
    if os.path.exists(ROOT_LIB):
        size = os.path.getsize(ROOT_LIB)
        print(f"[OK] Root canonical library preserved: {size:,} bytes.")


def main():
    print("[BSKM] Initializing Knowledge Library Modularization & DB Ingestion...")
    store = EventStore()
    modularize_and_index_library(store)
    compile_root_library()
    count = store.count_knowledge_discourses()
    print(f"[BSKM] Knowledge Library Ingestion Complete. Total Discourses in DB: {count}")


if __name__ == "__main__":
    main()
