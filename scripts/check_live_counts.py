"""scripts/check_live_counts.py"""
import re
import sys
sys.path.insert(0, ".")

with open("History_upgradation.md", "r", encoding="utf-8") as f:
    htxt = f.read()
hsecs = re.findall(r"^##\s+([^\n]+)", htxt, re.MULTILINE)
print("Last 10 History headings:")
for s in hsecs[-10:]:
    print(" ", s)

with open("KNOWLEDGE_LIBRARY_GEO_POLITICS.md", "r", encoding="utf-8") as f:
    ktxt = f.read()
ksecs = re.findall(r"^##\s+([^\n]+)", ktxt, re.MULTILINE)
print(f"\nTotal KNOWLEDGE_LIBRARY headers: {len(ksecs)}")
for s in ksecs[-6:]:
    print(" ", s)

with open("geo_engine/arbitration/synthesizer.py", "r", encoding="utf-8") as f:
    stxt = f.read()
m = re.search(r"strategic_resilience_matrix\s*=\s*\{(.*?)\n        \}", stxt, re.DOTALL)
if m:
    keys = re.findall(r'"([^"]+)"\s*:', m.group(1))
    print(f"\nLive SRM channel keys: {len(keys)}")
    print("Last 6 keys:", keys[-6:])

import geo_engine.lenses as lmod
print("Lenses __all__ count:", len(getattr(lmod, "__all__", [])))
print("Last 5 symbols:", getattr(lmod, "__all__", [])[-5:])
