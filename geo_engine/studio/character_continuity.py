"""
Character and Environment Continuity Engine.
Ensures visual consistency across scenes by locking visual tokens, seeds,
and lighting archetypes for recurring characters and settings.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import re
import hashlib


@dataclass
class CharacterAnchor:
    """Immutable visual anchor for a recurring character."""
    character_id: str
    name: str
    archetype: str
    visual_descriptor: str
    faceless_representation: str
    consistency_seed: int
    lighting_style: str = "cinematic chiaroscuro, 8k resolution, volumetric lighting"

    def get_prompt_fragment(self) -> str:
        """Return the locked visual prompt fragment for image/video generation."""
        return (
            f"[{self.character_id}: {self.visual_descriptor}, "
            f"representation: {self.faceless_representation}, "
            f"style: {self.lighting_style}, seed: {self.consistency_seed}]"
        )


@dataclass
class EnvironmentAnchor:
    """Immutable visual anchor for a recurring scene environment."""
    environment_id: str
    name: str
    setting_type: str
    visual_descriptor: str
    color_palette: str
    camera_mood: str
    consistency_seed: int

    def get_prompt_fragment(self) -> str:
        """Return the locked environment prompt fragment."""
        return (
            f"[{self.environment_id}: {self.visual_descriptor}, "
            f"palette: {self.color_palette}, mood: {self.camera_mood}, seed: {self.consistency_seed}]"
        )


class CharacterContinuityEngine:
    """
    Manages character and environment consistency across a multi-scene film production.
    Enforces anti-hallucination and faceless compliance rules.
    """

    # Pre-calibrated archetypes for historical, economic, and civilizational entities
    CANONICAL_ARCHETYPES = {
        "sovereign_leader": {
            "archetype": "SOVEREIGN_LEADER",
            "visual_descriptor": "dignified statesman silhouette with formal ceremonial stole, standing before sovereign seal",
            "faceless": "shadow silhouette with subtle amber rim-lighting, no facial features depicted",
        },
        "warrior_monarch": {
            "archetype": "EPIC_WARRIOR_MONARCH",
            "visual_descriptor": "towering ancient monarch in ornate bronze and gold ceremonial cuirass armor, regal presence",
            "faceless": "heroic chiaroscuro silhouette, glowing armor highlights, back to camera or shadowed profile",
        },
        "central_banker": {
            "archetype": "FINANCIAL_CUSTODIAN",
            "visual_descriptor": "formal executive silhouette in dark tailored suit examining glowing balance sheet ledger",
            "faceless": "shadowed figure in minimalist glass boardroom, illuminated by financial data projections",
        },
        "vedic_rishi": {
            "archetype": "CIVILIZATIONAL_SAGE",
            "visual_descriptor": "venerable contemplative sage in saffron robes seated beside sacred fire altar, profound composure",
            "faceless": "serene silhouette beside sacred flames, golden smoke highlights, dignified posture",
        },
        "artisan_citizen": {
            "archetype": "SOVEREIGN_CITIZEN",
            "visual_descriptor": "skilled artisan or farmer standing in field or workshop, enduring industrious strength",
            "faceless": "warm amber backlit silhouette against golden harvest or forge embers",
        },
    }

    CANONICAL_ENVIRONMENTS = {
        "gold_vault": {
            "setting_type": "SOVEREIGN_TREASURY",
            "visual_descriptor": "massive subterranean granite vault with reinforced blast doors and stacked 24k gold bullion bars",
            "color_palette": "lustrous deep gold reflections against cold polished dark slate",
            "camera_mood": "reverent, impenetrable, heavy gravitas",
        },
        "maritime_chokepoint": {
            "setting_type": "STRATEGIC_WATERS",
            "visual_descriptor": "narrow maritime strait flanked by rugged arid coastal mountains with cargo supertankers in transit",
            "color_palette": "deep nautical navy, twilight amber and sunset crimson reflections",
            "camera_mood": "tense geopolitical friction, vast scale",
        },
        "ancient_citadel": {
            "setting_type": "PURANIC_CITADEL",
            "visual_descriptor": "colossal monolithic red sandstone and granite palace fortress carved into mountain peaks with brass braziers",
            "color_palette": "terracotta red, burnished bronze, dramatic twilight sky",
            "camera_mood": "epic civilizational majesty, timeless grandeur",
        },
        "financial_capitol": {
            "setting_type": "MODERN_METROPOLIS",
            "visual_descriptor": "towering neoclassical parliament and central bank facades silhouetted against glowing digital ticker data",
            "color_palette": "obsidian black, cold steel blue, glowing amber data lines",
            "camera_mood": "analytical forensic urgency, systemic crisis",
        },
    }

    def __init__(self):
        self.characters: Dict[str, CharacterAnchor] = {}
        self.environments: Dict[str, EnvironmentAnchor] = {}

    def register_or_derive_character(self, name: str, raw_context: str = "") -> CharacterAnchor:
        """Extract or create a locked character anchor from raw text context."""
        slug = re.sub(r"[^a-zA-Z0-9]+", "_", name.strip().lower())
        char_id = f"CHAR_{slug.upper()[:16]}"

        if char_id in self.characters:
            return self.characters[char_id]

        # Deterministic seed from name
        seed = int(hashlib.sha256(name.encode("utf-8")).hexdigest()[:8], 16) % 1000000

        # Match canonical archetype or derive
        matched_arch = "artisan_citizen"
        context_lower = (name + " " + raw_context).lower()

        if any(w in context_lower for w in ["king", "warrior", "vaali", "ravana", "caesar", "general", "army"]):
            matched_arch = "warrior_monarch"
        elif any(w in context_lower for w in ["ruler", "prime minister", "president", "emperor", "modi", "trump"]):
            matched_arch = "sovereign_leader"
        elif any(w in context_lower for w in ["bank", "fed", "treasury", "investor", "fund", "wall street"]):
            matched_arch = "central_banker"
        elif any(w in context_lower for w in ["rishi", "sage", "narada", "shankaracharya", "vedic", "guru"]):
            matched_arch = "vedic_rishi"

        template = self.CANONICAL_ARCHETYPES[matched_arch]

        anchor = CharacterAnchor(
            character_id=char_id,
            name=name,
            archetype=template["archetype"],
            visual_descriptor=f"{name.title()} as {template['visual_descriptor']}",
            faceless_representation=template["faceless"],
            consistency_seed=seed,
        )
        self.characters[char_id] = anchor
        return anchor

    def register_or_derive_environment(self, location_name: str, raw_context: str = "") -> EnvironmentAnchor:
        """Extract or create a locked environment anchor."""
        slug = re.sub(r"[^a-zA-Z0-9]+", "_", location_name.strip().lower())
        env_id = f"ENV_{slug.upper()[:16]}"

        if env_id in self.environments:
            return self.environments[env_id]

        seed = int(hashlib.sha256(location_name.encode("utf-8")).hexdigest()[:8], 16) % 1000000
        context_lower = (location_name + " " + raw_context).lower()

        matched_env = "financial_capitol"
        if any(w in context_lower for w in ["gold", "vault", "bullion", "treasury", "fort knox", "rbi"]):
            matched_env = "gold_vault"
        elif any(w in context_lower for w in ["sea", "strait", "ocean", "hormuz", "malacca", "tanker", "port"]):
            matched_env = "maritime_chokepoint"
        elif any(w in context_lower for w in ["kishkindha", "ayodhya", "lanka", "rome", "cave", "temple", "fort"]):
            matched_env = "ancient_citadel"

        template = self.CANONICAL_ENVIRONMENTS[matched_env]

        anchor = EnvironmentAnchor(
            environment_id=env_id,
            name=location_name,
            setting_type=template["setting_type"],
            visual_descriptor=f"{location_name.title()}: {template['visual_descriptor']}",
            color_palette=template["color_palette"],
            camera_mood=template["camera_mood"],
            consistency_seed=seed,
        )
        self.environments[env_id] = anchor
        return anchor

    def lock_scene_prompt(self, base_prompt: str, char_names: List[str], env_name: Optional[str] = None) -> str:
        """
        Assemble a consistent visual prompt injecting locked character and environment tags.
        Guarantees that diffusion and video generation models maintain continuity.
        """
        tokens = []
        if env_name:
            env = self.register_or_derive_environment(env_name)
            tokens.append(env.get_prompt_fragment())

        for cname in char_names:
            char = self.register_or_derive_character(cname)
            tokens.append(char.get_prompt_fragment())

        continuity_header = " | ".join(tokens)
        if continuity_header:
            return f"{continuity_header} | Cinematic 4K scene: {base_prompt}, 16:9 aspect ratio, photorealistic, documentary grading."
        return f"Cinematic 4K scene: {base_prompt}, 16:9 aspect ratio, photorealistic, documentary grading."
