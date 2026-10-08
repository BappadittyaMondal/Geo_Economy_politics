"""
Local Frame Renderer & Visual Plate Generator.
Renders broadcast-quality 1080p cinematic slides with telemetry typography,
dark gradient overlays, domain badges, and character/environment anchors.
Operates 100% offline with zero external network dependencies to eliminate black screens.
"""

import os
import pathlib
from typing import Optional, Dict, Any, List
from PIL import Image, ImageDraw, ImageFont

from .script_architect import SceneSegment


class LocalFrameRenderer:
    """
    Synthesizes crisp, high-contrast, broadcast-ready 1080p/9:16 visual plates
    for scene segments using Pillow without requiring remote diffusion APIs.
    """

    @classmethod
    def get_system_font(cls, size: int, bold: bool = False) -> ImageFont.ImageFont:
        """Loads system TrueType font or falls back gracefully to default PIL font."""
        font_paths = [
            "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/segoeui.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ]
        for p in font_paths:
            if os.path.exists(p):
                try:
                    return ImageFont.truetype(p, size)
                except Exception:
                    pass
        return ImageFont.load_default()

    @classmethod
    def render_scene_slide(
        cls,
        scene: SceneSegment,
        scene_idx: int,
        total_scenes: int,
        out_path: str,
        topic: str = "SOVEREIGN INTELLIGENCE",
        aspect_ratio: str = "16:9",
        bg_image_path: Optional[str] = None,
    ) -> str:
        """
        Renders a cinematic graphic plate for a single scene.
        """
        width, height = (1920, 1080) if aspect_ratio == "16:9" else (1080, 1920)

        # 1. Base Canvas
        if bg_image_path and os.path.exists(bg_image_path):
            try:
                base = Image.open(bg_image_path).convert("RGB")
                base = base.resize((width, height), Image.Resampling.LANCZOS)
            except Exception:
                base = Image.new("RGB", (width, height), (15, 23, 42))
        else:
            base = Image.new("RGB", (width, height), (10, 15, 28))

        # 2. Add subtle horizontal gradient/vignette
        gradient = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw_grad = ImageDraw.Draw(gradient)
        vignette_start = int(height * 0.55)
        for y in range(vignette_start, height):
            alpha = int(245 * ((y - vignette_start) / float(height - vignette_start)))
            draw_grad.line([(0, y), (width, y)], fill=(8, 12, 22, alpha))
        base.paste(gradient, (0, 0), gradient)

        # 3. Typography & Graphics
        draw = ImageDraw.Draw(base)
        font_badge = cls.get_system_font(20, bold=True)
        font_title = cls.get_system_font(38, bold=True)
        font_text = cls.get_system_font(26, bold=False)
        font_mono = cls.get_system_font(18, bold=True)

        margin_x = 70
        badge_top = 50

        # Domain / Category Amber Badge
        badge_w = 420
        badge_h = 42
        draw.rectangle([margin_x, badge_top, margin_x + badge_w, badge_top + badge_h], fill=(217, 119, 6))
        draw.text((margin_x + 18, badge_top + 8), "GEO-ECONOMIC & CIVILIZATIONAL", font=font_badge, fill=(255, 255, 255))

        # Scene Counter (Top Right)
        counter_str = f"SCENE {scene_idx:02d} / {total_scenes:02d}"
        draw.text((width - margin_x - 220, badge_top + 8), counter_str, font=font_badge, fill=(203, 213, 225))

        # Character/Environment Anchor Tags if present
        if scene.character_anchor:
            anchor_badge = f"ANCHOR: {scene.character_anchor.upper()}"
            draw.rectangle([margin_x + badge_w + 20, badge_top, margin_x + badge_w + 320, badge_top + badge_h], fill=(30, 41, 59))
            draw.text((margin_x + badge_w + 35, badge_top + 10), anchor_badge, font=font_mono, fill=(56, 189, 248))

        # Camera Motion Indicator (Top Right sub-badge)
        cam_text = f"MOTION: {scene.camera_motion.upper()}"
        draw.text((width - margin_x - 220, badge_top + 50), cam_text, font=font_mono, fill=(148, 163, 184))

        # Scene Visual Prompt Brief
        y_cursor = height - 340
        draw.text((margin_x, y_cursor), f"TOPIC: {topic[:65].upper()}", font=font_title, fill=(245, 158, 11))

        # Scene Dialogue (English & Hindi/Bengali preview)
        en_text = scene.spoken_text.get("en", scene.spoken_text.get("english", ""))
        if en_text:
            en_lines = cls._wrap_text(en_text, max_chars=80)
            y_cursor += 60
            for line in en_lines[:2]:
                draw.text((margin_x, y_cursor), f"> {line}", font=font_text, fill=(255, 255, 255))
                y_cursor += 36

        hi_text = scene.spoken_text.get("hi", scene.spoken_text.get("sa", ""))
        if hi_text:
            y_cursor += 10
            draw.text((margin_x, y_cursor), f">> {hi_text[:90]}...", font=font_text, fill=(226, 232, 240))

        # Bottom Sovereign Intelligence Watermark
        draw.line([(margin_x, height - 70), (width - margin_x, height - 70)], fill=(71, 85, 105), width=1)
        draw.text(
            (margin_x, height - 55),
            "GEO_ENGINE SOVEREIGN STUDIO | BROADCAST MASTER 1080p | ZERO-HALLUCINATION",
            font=font_mono,
            fill=(148, 163, 184),
        )

        os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
        base.save(out_path)
        return out_path

    @classmethod
    def _wrap_text(cls, text: str, max_chars: int = 80) -> List[str]:
        """Simple word-wrap helper."""
        words = text.split()
        lines = []
        current_line = []
        current_len = 0
        for w in words:
            if current_len + len(w) + 1 <= max_chars:
                current_line.append(w)
                current_len += len(w) + 1
            else:
                if current_line:
                    lines.append(" ".join(current_line))
                current_line = [w]
                current_len = len(w)
        if current_line:
            lines.append(" ".join(current_line))
        return lines
