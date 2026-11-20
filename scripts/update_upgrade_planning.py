# scripts/update_upgrade_planning.py
import re

phase_446_content = """
## Phase 446: SupranationalOligarchyAndDeepStateSubversionSieve
- **Subsystem / Parent Lens:** `geo_engine/lenses/institutional_lawfare.py`
- **Primary Metric / Channel:** `supranational_deep_state_subversion_risk`
- **Empirical Drivers:** The 5 Structural Pillars of Supranational Oligarchy (Defense-Industrial Complex, Big Pharma, Petrochemical cartels, Wall Street/Debt rollover, Big Tech/Enterprise OS surveillance), WEF Davos technocratic mandates, programmable digital rationing (CBDC freezes, carbon footprint quotas), and intelligence/judicial lawfare resistance to sovereign bilateral treaties (*The Alternate Media* / Gayatri Mishra & Girdhar Mamidipudi, `1C-Mps-LwXI`).
- **Mathematical Formulation:**
  $$\\\\text{DeepStateSubversionIndex} = \\\\text{Norm}\\\\left(0.35 \\\\cdot W_{\\\\text{WEFGlobalistPushback}} + 0.30 \\\\cdot J_{\\\\text{JudicialIntelligenceLawfare}} + 0.20 \\\\cdot M_{\\\\text{TechMonopolyChokepoint}} + 0.15 \\\\cdot R_{\\\\text{RatingCartelSqueeze}}\\\\right) \\\\cdot (1.0 - 0.40 \\\\cdot \\\\text{SovereignAutonomy})$$
  $$\\\\text{InstitutionalResilienceMoat} = \\\\sigma\\\\left(2.2 \\\\cdot D_{\\\\text{IndigenousDPI}} + 1.8 \\\\cdot P_{\\\\text{DomesticManufacturingCapEx}} - 2.0 \\\\cdot \\\\text{DeepStateSubversionIndex}\\\\right)$$
- **Expected Integration:** Expands `SummitSynthesizer.strategic_resilience_matrix` by 1 live float channel.

## Summary of Architectural Impact
- **Total New Sieves / Tensors:** 6 (Phases 441–446)
- **Projected Resilience Channels:** 245 -> 251
- **Projected Lens Symbols:** 256 -> 262
- **Status:** Staged in `UPGRADE_PLANING` for future execution when authorized.
"""

def update_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Update title
    content = content.replace("PHASES 441–445", "PHASES 441–446")
    
    # Remove old summary
    old_summary_pos = content.find("## Summary of Architectural Impact")
    if old_summary_pos != -1:
        base_content = content[:old_summary_pos].rstrip()
    else:
        base_content = content.rstrip()

    new_content = base_content + "\n" + phase_446_content.lstrip()
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Updated {filepath}")

update_file("UPGRADE_PLANING")
update_file("UPGRADE_PLANING.md")
