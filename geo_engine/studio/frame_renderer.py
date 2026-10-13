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
    def get_system_font(cls, size: int, bold: bool = False, is_indic: bool = False) -> ImageFont.ImageFont:
        """Loads system TrueType font or falls back gracefully to default PIL font."""
        if is_indic:
            indic_paths = [
                "C:/Windows/Fonts/NirmalaB.ttf" if bold else "C:/Windows/Fonts/Nirmala.ttf",
                "C:/Windows/Fonts/mangal.ttf",
                "C:/Windows/Fonts/vrinda.ttf",
                "/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf" if bold else "/usr/share/fonts/truetype/freefont/FreeSerif.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            ]
            for p in indic_paths:
                if os.path.exists(p):
                    try:
                        return ImageFont.truetype(p, size)
                    except Exception:
                        pass

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

        hi_text = scene.spoken_text.get("hi", scene.spoken_text.get("bn", scene.spoken_text.get("sa", "")))
        if hi_text:
            font_indic = cls.get_system_font(24, bold=False, is_indic=True)
            y_cursor += 10
            draw.text((margin_x, y_cursor), f">> {hi_text[:90]}...", font=font_indic, fill=(226, 232, 240))

        # 4. Optional Native Telemetry Infographic Overlay (Phase 153)
        telemetry = getattr(scene, "telemetry_data", None) or (bg_image_path if isinstance(bg_image_path, dict) else None)
        if isinstance(telemetry, dict) and aspect_ratio == "16:9":
            info_x = width - margin_x - 500
            info_y = 120
            if "gauges" in telemetry and isinstance(telemetry["gauges"], list):
                for g in telemetry["gauges"][:3]:
                    cls.render_horizontal_bar_gauge(
                        draw,
                        x=info_x,
                        y=info_y,
                        width=480,
                        height=28,
                        label=g.get("label", "METRIC"),
                        value=float(g.get("value", 0.0)),
                        max_value=float(g.get("max_value", 100.0)),
                        unit=g.get("unit", ""),
                        color=g.get("color", (245, 158, 11))
                    )
                    info_y += 68
            elif "balance_sheet" in telemetry and isinstance(telemetry["balance_sheet"], dict):
                bs = telemetry["balance_sheet"]
                cls.render_balance_sheet_metric_panel(
                    draw,
                    x=info_x,
                    y=info_y,
                    width=480,
                    height=160,
                    announced_usd_b=float(bs.get("announced", 10.0)),
                    realized_usd_b=float(bs.get("realized", 1.5)),
                    haircut_pct=float(bs.get("haircut", 85.0))
                )
            elif "escalation" in telemetry and isinstance(telemetry["escalation"], dict):
                esc = telemetry["escalation"]
                cls.render_escalation_meter(
                    draw,
                    x=info_x,
                    y=info_y,
                    width=480,
                    height=45,
                    provocation_index=float(esc.get("provocation_index", 0.5)),
                    threat_tier=str(esc.get("threat_tier", "ELEVATED"))
                )

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
    def render_horizontal_bar_gauge(
        cls,
        draw: ImageDraw.ImageDraw,
        x: int,
        y: int,
        width: int,
        height: int,
        label: str,
        value: float,
        max_value: float,
        unit: str = "",
        color: tuple = (245, 158, 11),
        bg_color: tuple = (30, 41, 59)
    ) -> None:
        """Renders a procedural horizontal progress gauge with label and percentage/value text."""
        font_label = cls.get_system_font(16, bold=True)
        font_val = cls.get_system_font(16, bold=True)

        ratio = max(0.0, min(1.0, value / max_value if max_value > 0 else 0.0))
        fill_w = int(width * ratio)

        # Draw Label & Metric Header
        unit_str = f" {unit}" if unit else ""
        metric_str = f"{value:.1f}/{max_value:.1f}{unit_str} ({int(ratio * 100)}%)"
        draw.text((x, y - 22), label.upper(), font=font_label, fill=(203, 213, 225))
        draw.text((x + width - 140, y - 22), metric_str, font=font_val, fill=(245, 158, 11))

        # Background Track
        draw.rectangle([x, y, x + width, y + height], fill=bg_color)
        # Active Progress Fill
        if fill_w > 0:
            draw.rectangle([x, y, x + fill_w, y + height], fill=color)
        # Border
        draw.rectangle([x, y, x + width, y + height], outline=(71, 85, 105), width=1)

    @classmethod
    def render_balance_sheet_metric_panel(
        cls,
        draw: ImageDraw.ImageDraw,
        x: int,
        y: int,
        width: int,
        height: int,
        announced_usd_b: float,
        realized_usd_b: float,
        haircut_pct: float = 85.0
    ) -> None:
        """Renders an epistemic balance sheet panel contrasting announced vs realized CapEx."""
        font_hdr = cls.get_system_font(18, bold=True)
        font_metric = cls.get_system_font(24, bold=True)
        font_sub = cls.get_system_font(14, bold=False)

        # Panel Background
        draw.rectangle([x, y, x + width, y + height], fill=(15, 23, 42), outline=(71, 85, 105), width=1)
        # Header
        draw.rectangle([x, y, x + width, y + 36], fill=(30, 41, 59))
        draw.text((x + 16, y + 8), "FORENSIC BALANCE SHEET HAIRCUT AUDIT", font=font_hdr, fill=(56, 189, 248))

        # Announced Column
        draw.text((x + 20, y + 50), "ANNOUNCED MOU", font=font_sub, fill=(148, 163, 184))
        draw.text((x + 20, y + 74), f"${announced_usd_b:.1f}B", font=font_metric, fill=(239, 68, 68))

        # Realized Column
        draw.text((x + 260, y + 50), f"REALIZED ({100-haircut_pct:.0f}% CAPEX)", font=font_sub, fill=(148, 163, 184))
        draw.text((x + 260, y + 74), f"${realized_usd_b:.1f}B", font=font_metric, fill=(34, 197, 94))

        # Bottom Haircut Status Tag
        draw.line([(x + 16, y + 118), (x + width - 16, y + 118)], fill=(51, 65, 85), width=1)
        draw.text(
            (x + 20, y + 128),
            f"EPISTEMIC RULE: {haircut_pct:.0f}% HAIRCUT APPLIED ON UNFINANCED PR MOUs",
            font=font_sub,
            fill=(245, 158, 11)
        )

    @classmethod
    def render_escalation_meter(
        cls,
        draw: ImageDraw.ImageDraw,
        x: int,
        y: int,
        width: int,
        height: int,
        provocation_index: float,
        threat_tier: str
    ) -> None:
        """Renders a multi-segmented visual threat and escalation index meter."""
        font_lbl = cls.get_system_font(16, bold=True)
        draw.text((x, y - 22), f"ESCALATION INDEX: {provocation_index:.2f} [{threat_tier}]", font=font_lbl, fill=(239, 68, 68))

        # 4 Color Segments
        seg_w = width // 4
        colors = [(34, 197, 94), (234, 179, 8), (249, 115, 22), (239, 68, 68)]
        for i, col in enumerate(colors):
            draw.rectangle([x + i * seg_w, y, x + (i + 1) * seg_w - 4, y + height], fill=(30, 41, 59), outline=(71, 85, 105))
            if provocation_index >= (i + 1) * 0.25:
                draw.rectangle([x + i * seg_w, y, x + (i + 1) * seg_w - 4, y + height], fill=col)
            elif provocation_index > i * 0.25:
                part_ratio = (provocation_index - i * 0.25) / 0.25
                draw.rectangle([x + i * seg_w, y, x + i * seg_w + int((seg_w - 4) * part_ratio), y + height], fill=col)

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
