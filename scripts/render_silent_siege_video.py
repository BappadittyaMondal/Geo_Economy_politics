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
TEMP_DIR = OUTPUT_DIR / "silent_siege_temp"
TEMP_DIR.mkdir(exist_ok=True)

FINAL_MP4 = OUTPUT_DIR / "the_silent_siege_cinematic_1080p.mp4"
FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()

SCENES = [
    {
        "scene_num": 1,
        "title": "THE CELLULAR ILLUSION: 2018-2024",
        "prompt": "Dark tactical surveillance operations room with green glowing radio spectrum monitors and military maps of Kashmir mountain ridges, cinematic 4K, 16:9",
        "line1": "For two decades, counter-terror relied on tracking mobile towers.",
        "line2": "In J&K, proxies quietly abandoned cellular networks altogether.",
        "speech": "For over two decades, counter-terrorism operations relied on cellular dominance. The assumption was simple: if an operative uses a smartphone, military signals intelligence intercepts the tower within minutes. But between 2019 and 2024, terror handlers quietly abandoned cellular networks entirely."
    },
    {
        "scene_num": 2,
        "title": "THE CLOUD TRAP: FOREIGN HYPERSCALER RISK",
        "prompt": "Massive server farm corridor in blue fluorescent light with digital fiber optic cables stretching across a world map with security lock icons, 16:9",
        "line1": "Hyperscalers (AWS, Azure, GCP) subject to US CLOUD Act jurisdiction.",
        "line2": "Cloud dependence exposes national defense assets to remote kill-switches.",
        "speech": "Simultaneously, the modern world moved defense data onto commercial clouds. But under the US CLOUD Act, foreign hyperscalers can be legally compelled to audit, throttle, or freeze offshore systems. If sovereign defense drones and targeting rely on foreign servers, national security becomes a paid subscription that can be revoked overnight."
    },
    {
        "scene_num": 3,
        "title": "TACTICAL EW: THE OFF-GRID LoRa DISCOVERY",
        "prompt": "Cinematic close-up of tactical radio circuit board with small whip antenna in dense misty Himalayan pine forest at dawn, 16:9",
        "line1": "Terrorist proxies shifted to unlicensed ISM band (865-867 MHz) LoRa radios.",
        "line2": "Chirp Spread Spectrum operates below 100mW, bypassing mobile phone taps.",
        "speech": "In the rugged mountains of Rajouri and Poonch, the Indian Army uncovered the new tactical reality: twenty-dollar commercial LoRa transceivers operating on unlicensed 865 megahertz frequencies. Using Chirp Spread Spectrum, encrypted coordinates hop ridge-to-ridge over fifteen kilometers without SIM cards or towers, requiring portable military spectrum analyzers to hunt sub-milliwatt whispers in the dark."
    },
    {
        "scene_num": 4,
        "title": "ZERO CLOUD, ZERO INTERNET: TATVA & SANJAY",
        "prompt": "Ultra-modern cleanroom laboratory with high-tech military drone payload and glowing microprocessor chip on circuit board, 16:9",
        "line1": "Indigenous tactical edge AI embedded directly on UAV and sensor microchips.",
        "line2": "Autonomous target recognition and navigation in complete GPS-jammed silence.",
        "speech": "Bharat's strategic counter-response was the deployment of sovereign, air-gapped edge AI. Models like Tatva, Sanjay, and Drishta run on local embedded microprocessors aboard UAVs and satellites with zero internet and zero cloud exposure. Even during total electronic blackouts and GPS denial, autonomous mission kill-chains execute without transmitting a single byte abroad."
    },
    {
        "scene_num": 5,
        "title": "PRE-ELECTORAL LAWFARE: ARTICLE 324 SIEGE",
        "prompt": "Dramatic split composition showing stone classical pillars of justice on one side and flashing police lights with barricades on other side, 16:9",
        "line1": "Targeted protests at Nirvachan Sadan and Jantar Mantar against CEC Gyanesh Kumar.",
        "line2": "Pre-emptive delegitimization of the umpire to establish post-poll alibis.",
        "speech": "On the political front, hybrid warfare targets constitutional arbiters. Under Article 324, the Election Commission possesses independent superintendence over polls. Coordinated street protests and 47-judge public petitions targeting Chief Election Commissioner Gyanesh Kumar represent pre-electoral lawfare: delegitimizing the referee before the match to build ready-made excuses for electoral defeat."
    },
    {
        "scene_num": 6,
        "title": "THE OUTRAGE ECONOMY: ALGORITHMIC AD CASH",
        "prompt": "Dark room illuminated by glowing smartphone screens and abstract glowing digital network nodes with cash flow graph graphics, 16:9",
        "line1": "Meta & YouTube recommendation algorithms mathematically favor high-friction outrage.",
        "line2": "Automated ad monetization and viral clicks convert digital anger into street cash.",
        "speech": "Where does the funding come from? Following strict FCRA crackdowns on foreign NGOs, agitation finance evolved. Big Tech recommendation algorithms prioritize high-friction political outrage. Sponsored reels and viral sensationalism generate continuous ad payouts and UPI crowdfunding, converting algorithmic anger into physical street mobilization."
    },
    {
        "scene_num": 7,
        "title": "DEMOGRAPHIC SOVEREIGNTY: BORDER REALISM",
        "prompt": "Cinematic wide angle shot of military transport aircraft on dark tarmac at night with security personnel in silhouette, dramatic lighting, 16:9",
        "line1": "8,100+ illegal foreign infiltrators identified and repatriated under Foreigners Act.",
        "line2": "National survival explicitly supersedes un-elected multilateral vetoes.",
        "speech": "In border enforcement, the doctrine is clear. The Indian Air Force airlifted over eight thousand illegal foreign infiltrators from sensitive Jammu military zones under the Foreigners Act. Despite international human rights pushback, Bharat established a precedent: national demographic survival and border integrity strictly supersede un-elected multilateral vetoes."
    },
    {
        "scene_num": 8,
        "title": "THE HORIZON: ETERNAL VIGILANCE (2026-2030)",
        "prompt": "Epic sunrise over majestic government architecture in New Delhi with high tech telemetry grid in the sky, cinematic 4K, 16:9",
        "line1": "Dominating the radio spectrum, owning sovereign silicon, shielding institutions.",
        "line2": "An awake, forensically informed citizenry is the ultimate national defense.",
        "speech": "The next decade will not see wars declared with formal manifestos. They will arrive disguised as viral trends, PIL blitzes, and twenty-dollar radio chips. By dominating the radio spectrum, building sovereign offline silicon, and upholding constitutional institutions with calm fortitude, Bharat secures its civilizational future. Eternal vigilance remains the true price of sovereignty."
    }
]

def fetch_or_create_image(scene, out_path):
    if out_path.exists() and out_path.stat().st_size > 5000:
        return
    encoded = urllib.parse.quote(scene["prompt"])
    url = f"https://image.pollinations.ai/prompt/{encoded}?width=1920&height=1080&nologo=true"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
            if len(data) > 5000:
                out_path.write_bytes(data)
                return
    except Exception as e:
        print(f"[WARN] Fallback for scene {scene['scene_num']}: {e}")

    # Fallback image
    img = Image.new("RGB", (1920, 1080), (15, 23, 42))
    img.save(str(out_path))

def render_cinematic_slide(scene, raw_img_path, out_slide_path):
    base_img = Image.open(raw_img_path).convert("RGB")
    base_img = base_img.resize((1920, 1080), Image.Resampling.LANCZOS)

    # Dark Vignette & Gradient Overlay (bottom 380px)
    overlay = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    draw_ov = ImageDraw.Draw(overlay)
    for y in range(700, 1080):
        alpha = int(230 * ((y - 700) / 380.0))
        draw_ov.line([(0, y), (1920, y)], fill=(10, 15, 28, alpha))
    base_img.paste(overlay, (0, 0), overlay)

    # Typography
    draw = ImageDraw.Draw(base_img)
    font_badge = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 22)
    font_title = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 44)
    font_text = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 30)

    # Amber Badge
    draw.rectangle([70, 50, 480, 92], fill=(217, 119, 6))
    draw.text((85, 58), "FORENSIC GEOPOLITICAL AUDIT", font=font_badge, fill=(255, 255, 255))
    draw.text((1920 - 320, 58), f"SCENE 0{scene['scene_num']} / 0{len(SCENES)}", font=font_badge, fill=(203, 213, 225))

    # Title & Text
    draw.text((70, 770), scene["title"], font=font_title, fill=(245, 158, 11))
    draw.text((70, 850), f">  {scene['line1']}", font=font_text, fill=(255, 255, 255))
    draw.text((70, 905), f">  {scene['line2']}", font=font_text, fill=(226, 232, 240))

    # Watermark
    draw.line([(70, 980), (1850, 980)], fill=(71, 85, 105), width=1)
    draw.text((70, 995), "OPERATION CHRONOS // BHARAT SOVEREIGN INTELLIGENCE | 1080p BROADCAST MASTER", font=font_badge, fill=(148, 163, 184))

    base_img.save(str(out_slide_path))

async def produce_cinematic_video():
    print(f"[STUDIO] Starting Silent Siege AI Video Generation ({len(SCENES)} Scenes)...")
    clip_files = []

    for scene in SCENES:
        s_num = scene["scene_num"]
        print(f"[STUDIO] Rendering Scene {s_num}: {scene['title']}...")

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
