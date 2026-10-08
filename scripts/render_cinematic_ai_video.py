import asyncio
import os
import pathlib
import subprocess
import urllib.request
import urllib.parse
import edge_tts
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

ROOT_DIR = pathlib.Path(__file__).parent.parent
OUTPUT_DIR = ROOT_DIR / "studio_output"
OUTPUT_DIR.mkdir(exist_ok=True)
TEMP_DIR = OUTPUT_DIR / "cinematic_temp"
TEMP_DIR.mkdir(exist_ok=True)

FINAL_MP4 = OUTPUT_DIR / "imperial_debt_trap_cinematic_1080p.mp4"
FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()

SCENES = [
    {
        "scene_num": 1,
        "title": "THE CYCLE OF DEBASEMENT: ROME, BRITAIN & AMERICA",
        "prompt": "Cinematic 4K archival shot of ancient Roman silver coins denarius melting into gold bullion and paper currency, dark chiaroscuro lighting, epic historical documentary style, 16:9",
        "line1": "In the third century, Roman emperors clipped silver from the denarius.",
        "line2": "Today, United States national debt has breached $35 Trillion ($1T every 100 days).",
        "speech": "In the third century, Roman emperors clipped the silver from the denarius. In the twentieth century, Britain liquidated its gold to finance world wars. Today, the United States national debt has breached thirty-five trillion dollars — expanding by one trillion every one hundred days."
    },
    {
        "scene_num": 2,
        "title": "FISCAL DOMINANCE: THE $1.1 TRILLION TRAP",
        "prompt": "Dramatic night view of US Capitol building with red glowing parabolic debt charts and financial telemetry lines in the sky, cinematic 4K, 16:9",
        "line1": "Net interest on US debt exceeds $1.1 Trillion per year.",
        "line2": "The interest bill alone is now larger than the entire $850B Pentagon defense budget.",
        "speech": "This is not just another political budget debate. Annual net interest on US sovereign debt has officially crossed one point one trillion dollars. That single interest bill is now larger than the entire eight-hundred-and-fifty-billion-dollar Pentagon defense budget, creating inescapable Fiscal Dominance."
    },
    {
        "scene_num": 3,
        "title": "THE CANTILLON EFFECT & FIAT EROSION",
        "prompt": "Cinematic abstract close up of high speed fiat currency printing press with green blur and shadows of Wall Street skyscrapers, dark dramatic lighting, 16:9",
        "line1": "New money printing inflates financial assets for those closest to the press.",
        "line2": "Real purchasing power and middle-class wages get silently devalued.",
        "speech": "Economists call this the Cantillon Effect. When new money is printed to absorb sovereign deficits, those closest to the financial printing press acquire assets first, driving stock markets to nominal highs while real purchasing power is quietly crushed."
    },
    {
        "scene_num": 4,
        "title": "EURASIAN MONETARY REALIGNMENT: GOLD REPATRIATION",
        "prompt": "Massive central bank vault lined with stacked high-purity golden bullion ingots, dramatic golden reflections, cinematic lighting, 16:9",
        "line1": "China and Russia aggressively liquidating US Treasuries.",
        "line2": "Eurasian central banks accumulating record physical gold inside domestic vaults.",
        "speech": "Across the Pacific and Eurasia, rival powers recognized the danger. Central banks in China and Russia have been dumping US Treasuries for over a decade, aggressively accumulating physical gold bullion inside their own domestic vaults."
    },
    {
        "scene_num": 5,
        "title": "STRATEGIC RETREAT & WESTERN AUSTERITY",
        "prompt": "Silhouetted crowds of teachers and citizens in foggy European city streets with classical stone government buildings in background, somber cinematic atmosphere, 16:9",
        "line1": "Washington demands allies finance their own defense burdens.",
        "line2": "Mounting economic stagnation and public spending cuts trigger severe civil friction.",
        "speech": "As imperial fiscal strength erodes, strategic retrenchment inevitably follows. Washington is demanding that allies carry their own defense burdens, while mounting economic stagnation and public spending cuts spark severe civil friction across Europe."
    },
    {
        "scene_num": 6,
        "title": "BHARAT'S SOVEREIGN DEFENSE: ~25,000 TONNES OF GOLD",
        "prompt": "Radiant Indian temple treasury with 24k gold sacred jewelry, bullion coins on deep red silk, golden sunlight streaming through stone carvings, 16:9",
        "line1": "Private household gold is the world's largest decentralized sovereign hedge.",
        "line2": "RBI actively repatriating sovereign bullion from London back to Indian soil.",
        "speech": "Where does Bharat stand in this unraveling order? India possesses an unprecedented civilizational hedge: over twenty-five thousand metric tonnes of privately held domestic gold, alongside proactive central bank bullion repatriation, providing an unshakeable sovereign balance sheet."
    },
    {
        "scene_num": 7,
        "title": "CRITICAL SOVEREIGN CHOKEPOINTS: HARD REALISM",
        "prompt": "Cinematic shot of giant crude oil tanker navigating narrow maritime strait at sunset with industrial radar overlays, 16:9",
        "line1": "Energy Chokepoint: Over 85% import dependency on crude oil.",
        "line2": "Caloric & Medical: Reliance on imported fertilizers and Chinese active pharmaceutical ingredients.",
        "speech": "However, strategic realism demands an honest look at Bharat's severe material vulnerabilities. India still imports over eighty-five percent of its crude oil, relies heavily on imported potash and phosphate fertilizers, and remains critically dependent on Chinese active pharmaceutical ingredients."
    },
    {
        "scene_num": 8,
        "title": "THE SOVEREIGN INVESTOR PLAYBOOK: TANGIBLE VALUE",
        "prompt": "Epic cinematic globe showing golden trade routes illuminating Eurasia and the Indian Ocean at dawn, hyper-detailed, 16:9",
        "line1": "Over-indebted governments pay paper claims with devalued money.",
        "line2": "Lasting sovereignty lies in productive real assets, energy, and industrial self-reliance.",
        "speech": "For investors and citizens, the lesson of the imperial debt trap is straightforward: paper claims on over-indebted governments will be paid in devalued money. Real security lies in productive physical assets, critical infrastructure, and domestic industrial self-reliance."
    }
]

def fetch_or_create_image(scene, out_path):
    if out_path.exists() and out_path.stat().st_size > 5000:
        return
    encoded = urllib.parse.quote(scene["prompt"])
    url = f"https://image.pollinations.ai/prompt/{encoded}?width=1920&height=1080&nologo=true"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=35) as resp:
            data = resp.read()
            if len(data) > 5000:
                out_path.write_bytes(data)
                return
    except Exception as e:
        print(f"[WARN] Image download fallback for scene {scene['scene_num']}: {e}")

    # Fallback to rich geometric slide if network fails
    img = Image.new("RGB", (1920, 1080), (15, 23, 42))
    img.save(str(out_path))

def render_cinematic_slide(scene, raw_img_path, out_slide_path):
    # 1. Base Image
    base_img = Image.open(raw_img_path).convert("RGB")
    base_img = base_img.resize((1920, 1080), Image.Resampling.LANCZOS)

    # 2. Dark Vignette & Gradient Overlay (bottom 380px)
    overlay = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    draw_ov = ImageDraw.Draw(overlay)
    for y in range(700, 1080):
        alpha = int(230 * ((y - 700) / 380.0))
        draw_ov.line([(0, y), (1920, y)], fill=(10, 15, 28, alpha))
    base_img.paste(overlay, (0, 0), overlay)

    # 3. Typography
    draw = ImageDraw.Draw(base_img)
    font_badge = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 22)
    font_title = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 44)
    font_text = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 30)

    # Amber Badge
    draw.rectangle([70, 50, 420, 92], fill=(217, 119, 6))
    draw.text((85, 58), "GEO-ECONOMIC FORENSICS", font=font_badge, fill=(255, 255, 255))
    draw.text((1920 - 320, 58), f"SCENE 0{scene['scene_num']} / 0{len(SCENES)}", font=font_badge, fill=(203, 213, 225))

    # Title & Text
    draw.text((70, 770), scene["title"], font=font_title, fill=(245, 158, 11))
    draw.text((70, 850), f">  {scene['line1']}", font=font_text, fill=(255, 255, 255))
    draw.text((70, 905), f">  {scene['line2']}", font=font_text, fill=(226, 232, 240))

    # Watermark
    draw.line([(70, 980), (1850, 980)], fill=(71, 85, 105), width=1)
    draw.text((70, 995), "GEO_ENGINE SOVEREIGN INTELLIGENCE | 1080p BROADCAST MASTER", font=font_badge, fill=(148, 163, 184))

    base_img.save(str(out_slide_path))

async def produce_cinematic_video():
    print(f"[STUDIO] Starting Photorealistic AI Video Generation ({len(SCENES)} Scenes)...")
    clip_files = []

    for scene in SCENES:
        s_num = scene["scene_num"]
        print(f"[STUDIO] Generating Scene {s_num}: {scene['title']}...")

        # 1. Generate Voiceover MP3
        audio_file = TEMP_DIR / f"audio_{s_num}.mp3"
        if not audio_file.exists() or audio_file.stat().st_size < 1000:
            comm = edge_tts.Communicate(scene["speech"], "en-IN-PrabhatNeural")
            await comm.save(str(audio_file))

        # 2. Fetch AI Photorealistic Background Image
        raw_img = TEMP_DIR / f"raw_image_{s_num}.jpg"
        fetch_or_create_image(scene, raw_img)

        # 3. Create Styled 1080p Broadcast Slide
        styled_slide = TEMP_DIR / f"cinematic_slide_{s_num}.png"
        render_cinematic_slide(scene, raw_img, styled_slide)

        # 4. Render Scene Video Clip with FFmpeg
        clip_file = TEMP_DIR / f"clip_{s_num}.mp4"
        cmd = [
            FFMPEG_EXE,
            "-y",
            "-loop", "1",
            "-i", str(styled_slide),
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
            print(f"[ERROR] Failed clip {s_num}: {res.stderr}")
            return
        clip_files.append(clip_file)

    # 5. Concatenate All Scene Clips
    concat_list = TEMP_DIR / "concat_list.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        for c in clip_files:
            f.write(f"file '{c.name}'\n")

    print("[STUDIO] Muxing all scenes into Final Master Video...")
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
        print(f"[SUCCESS] CINEMATIC VIDEO COMPLETE: {FINAL_MP4} ({size_mb:.2f} MB)")
    else:
        print(f"[ERROR] Failed final muxing: {res.stderr}")

if __name__ == "__main__":
    asyncio.run(produce_cinematic_video())
