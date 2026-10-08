import asyncio
import os
import pathlib
import subprocess
import edge_tts
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

# Paths
ROOT_DIR = pathlib.Path(__file__).parent.parent
OUTPUT_DIR = ROOT_DIR / "studio_output"
OUTPUT_DIR.mkdir(exist_ok=True)
TEMP_DIR = OUTPUT_DIR / "temp_render"
TEMP_DIR.mkdir(exist_ok=True)

FINAL_MP4 = OUTPUT_DIR / "imperial_debt_trap_1080p.mp4"
FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()

# Scene definitions
SCENES = [
    {
        "scene_num": 1,
        "title": "THE CYCLE OF DEBASEMENT: ROME, BRITAIN & AMERICA",
        "bullets": [
            "Rome clipped silver from the denarius (95% -> <5%).",
            "Britain liquidated gold reserves during two world wars.",
            "US national debt has breached $35 Trillion ($1T every 100 days)."
        ],
        "speech": "In the third century, Roman emperors clipped the silver from the denarius. In the twentieth century, Britain liquidated its gold to finance world wars. Today, the United States national debt has breached thirty-five trillion dollars — expanding by one trillion every one hundred days."
    },
    {
        "scene_num": 2,
        "title": "FISCAL DOMINANCE: THE MATHEMATICAL TRAP",
        "bullets": [
            "Net interest on US debt exceeds $1.1 Trillion per year.",
            "Interest expense now eclipses the entire $850B Pentagon defense budget.",
            "Central banks cannot hike rates without accelerating sovereign insolvency."
        ],
        "speech": "This is not just another political budget debate. Annual net interest on US sovereign debt has officially crossed one point one trillion dollars. That single interest bill is now larger than the entire eight-hundred-and-fifty-billion-dollar Pentagon defense budget, creating inescapable Fiscal Dominance."
    },
    {
        "scene_num": 3,
        "title": "THE CANTILLON EFFECT & FIAT EROSION",
        "bullets": [
            "New money printing inflates financial asset prices nominally.",
            "Real purchasing power and middle-class wages get silently devalued.",
            "Paper wealth surges while physical caloric and industrial output lags."
        ],
        "speech": "Economists call this the Cantillon Effect. When new money is printed to absorb sovereign deficits, those closest to the financial printing press acquire assets first, driving stock markets to nominal highs while real purchasing power is quietly crushed."
    },
    {
        "scene_num": 4,
        "title": "EURASIAN MONETARY REALIGNMENT: GOLD REPATRIATION",
        "bullets": [
            "China and Russia aggressively liquidating US Treasuries.",
            "PBOC accumulating physical gold bullion for consecutive quarters.",
            "Bilateral local-currency invoicing bypassing SWIFT settlement."
        ],
        "speech": "Across the Pacific and Eurasia, rival powers recognized the danger. Central banks in China and Russia have been dumping US Treasuries for over a decade, aggressively accumulating physical gold bullion inside their own domestic vaults."
    },
    {
        "scene_num": 5,
        "title": "STRATEGIC RETREAT & WESTERN AUSTERITY",
        "bullets": [
            "Washington demands NATO and Gulf allies finance their own defense.",
            "European social welfare model pressured by de-industrialization.",
            "Municipal strikes conflated with civilizational culture wars."
        ],
        "speech": "As imperial fiscal strength erodes, strategic retrenchment inevitably follows. Washington is demanding that allies carry their own defense burdens, while mounting economic stagnation and public spending cuts spark severe civil friction across Europe."
    },
    {
        "scene_num": 6,
        "title": "BHARAT'S SOVEREIGN DEFENSE: ~25,000 TONNES OF GOLD",
        "bullets": [
            "Private household gold is the world's largest decentralized hedge.",
            "RBI actively repatriating sovereign bullion from London vaults.",
            "Intergenerational tangible wealth immune to Western bank freezes."
        ],
        "speech": "Where does Bharat stand in this unraveling order? India possesses an unprecedented civilizational hedge: over twenty-five thousand metric tonnes of privately held domestic gold, alongside proactive central bank bullion repatriation, providing an unshakeable sovereign balance sheet."
    },
    {
        "scene_num": 7,
        "title": "CRITICAL SOVEREIGN CHOKEPOINTS: HARD REALISM",
        "bullets": [
            "Energy: >85% import dependency on crude oil (Hormuz/Malacca risk).",
            "Caloric: Potash (MOP) and Phosphate (DAP) fertilizer import exposure.",
            "Medicine: >68% active pharmaceutical ingredient (API) reliance on China."
        ],
        "speech": "However, strategic realism demands an honest look at Bharat's severe material vulnerabilities. India still imports over eighty-five percent of its crude oil, relies heavily on imported potash and phosphate fertilizers, and remains critically dependent on Chinese active pharmaceutical ingredients."
    },
    {
        "scene_num": 8,
        "title": "THE SOVEREIGN INVESTOR PLAYBOOK: TANGIBLE VALUE",
        "bullets": [
            "Over-indebted governments pay paper claims with devalued currency.",
            "Capital reallocation toward productive real assets and energy.",
            "National security demands hard infrastructure and self-reliance."
        ],
        "speech": "For investors and citizens, the lesson of the imperial debt trap is straightforward: paper claims on over-indebted governments will be paid in devalued money. Real security lies in productive physical assets, critical infrastructure, and domestic industrial self-reliance."
    }
]

def create_scene_slide(scene, out_path):
    width, height = 1920, 1080
    img = Image.new("RGB", (width, height), color=(11, 19, 43)) # Deep cinematic obsidian-navy
    draw = ImageDraw.Draw(img)

    # Decorative Border
    draw.rectangle([50, 50, width - 50, height - 50], outline=(217, 119, 6), width=4) # Amber gold
    draw.rectangle([58, 58, width - 58, height - 58], outline=(51, 65, 85), width=2) # Slate border

    # Header Badges
    draw.rectangle([90, 85, 380, 130], fill=(217, 119, 6))
    draw.text((105, 95), "GEO-ECONOMIC FORENSICS", fill=(255, 255, 255))

    draw.text((width - 450, 95), f"SCENE 0{scene['scene_num']} / 0{len(SCENES)}", fill=(148, 163, 184))

    # Title
    draw.text((90, 180), scene["title"], fill=(245, 158, 11))

    # Divider line
    draw.line([(90, 240), (width - 90, 240)], fill=(71, 85, 105), width=2)

    # Bullet Points
    y_pos = 320
    for bullet in scene["bullets"]:
        draw.text((120, y_pos), ">", fill=(245, 158, 11))
        draw.text((160, y_pos), bullet, fill=(241, 245, 249))
        y_pos += 120

    # Footer Watermark & Compliance
    draw.line([(90, 940), (width - 90, 940)], fill=(51, 65, 85), width=1)
    draw.text((90, 960), "GEO_ENGINE SOVEREIGN INTELLIGENCE PLATFORM | 1080p BROADCAST MASTER", fill=(100, 116, 139))
    draw.text((width - 620, 960), "BOUNDARIES & DATA REPRESENTATIONAL FOR EDUCATION", fill=(100, 116, 139))

    img.save(str(out_path))

async def synthesize_all():
    print(f"[STUDIO] Initiating Master Video Render: {len(SCENES)} Scenes...")
    clip_files = []

    for idx, scene in enumerate(SCENES):
        s_num = scene["scene_num"]
        print(f"[STUDIO] Processing Scene {s_num}: {scene['title']}...")

        # 1. Generate Voiceover MP3
        audio_file = TEMP_DIR / f"audio_{s_num}.mp3"
        comm = edge_tts.Communicate(scene["speech"], "en-IN-PrabhatNeural")
        await comm.save(str(audio_file))

        # 2. Generate 1080p Slide PNG
        slide_file = TEMP_DIR / f"slide_{s_num}.png"
        create_scene_slide(scene, slide_file)

        # 3. Render Individual Scene Clip with FFmpeg
        clip_file = TEMP_DIR / f"clip_{s_num}.mp4"
        cmd = [
            FFMPEG_EXE,
            "-y",
            "-loop", "1",
            "-i", str(slide_file),
            "-i", str(audio_file),
            "-c:v", "libx264",
            "-tune", "stillimage",
            "-c:a", "aac",
            "-b:a", "192k",
            "-pix_fmt", "yuv420p",
            "-shortest",
            str(clip_file)
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"[ERROR] Failed to render clip {s_num}: {res.stderr}")
            return
        clip_files.append(clip_file)

    # 4. Concatenate All Scene Clips into Master MP4
    concat_list = TEMP_DIR / "concat_list.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        for c in clip_files:
            f.write(f"file '{c.name}'\n")

    print("[STUDIO] Muxing all scenes into Master Video...")
    final_cmd = [
        FFMPEG_EXE,
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy",
        str(FINAL_MP4)
    ]
    res = subprocess.run(final_cmd, capture_output=True, text=True, cwd=str(TEMP_DIR))
    if res.returncode == 0 and FINAL_MP4.exists():
        size_mb = FINAL_MP4.stat().st_size / (1024 * 1024)
        print(f"[SUCCESS] Broadcast-Ready Video Rendered Successfully!")
        print(f"[EXPORT_PATH] {FINAL_MP4} ({size_mb:.2f} MB)")
    else:
        print(f"[ERROR] Final concatenation failed: {res.stderr}")

if __name__ == "__main__":
    asyncio.run(synthesize_all())
