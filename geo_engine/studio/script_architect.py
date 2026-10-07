"""
Autonomous Sovereign Video Studio: Script Architect & Storyboard Engine.
Transforms single user prompts or strategic intelligence reports into structured,
multilingual scene storyboards (English, Hindi, Bengali, Sanskrit).
"""

import hashlib
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional


class VideoLanguage(str, Enum):
    """Supported broadcast languages."""
    ENGLISH = "en"
    HINDI = "hi"
    BENGALI = "bn"
    SANSKRIT = "sa"


class VideoPresentationMode(str, Enum):
    """Visual presentation format."""
    FACELESS_DOCUMENTARY = "FACELESS_DOCUMENTARY"
    WITH_FACE_AVATAR = "WITH_FACE_AVATAR"


class VideoDurationTier(str, Enum):
    """Target video duration brackets."""
    SHORT_1_MIN = "SHORT_1_MIN"
    MEDIUM_3_TO_5_MIN = "MEDIUM_3_TO_5_MIN"
    DEEP_DIVE_10_MIN = "DEEP_DIVE_10_MIN"


@dataclass
class SceneSegment:
    """A granular 4 to 10 second audiovisual scene within the video storyboard."""
    scene_id: int
    timestamp_start_sec: float
    timestamp_end_sec: float
    spoken_text: Dict[str, str]  # Map language code to localized dialogue
    visual_prompt: str           # Diffusion prompt for cinematic visual generator
    camera_motion: str           # Cinematic camera movement (zoom, pan, tilt, dolly)
    character_anchor: Optional[str] = None  # Reference character for facial consistency
    music_mood: str = "TENSION_INVESTIGATIVE"
    sound_effects: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "scene_id": self.scene_id,
            "timestamp_start_sec": self.timestamp_start_sec,
            "timestamp_end_sec": self.timestamp_end_sec,
            "duration_sec": round(self.timestamp_end_sec - self.timestamp_start_sec, 2),
            "spoken_text": self.spoken_text,
            "visual_prompt": self.visual_prompt,
            "camera_motion": self.camera_motion,
            "character_anchor": self.character_anchor,
            "music_mood": self.music_mood,
            "sound_effects": self.sound_effects,
        }


@dataclass
class VideoScriptPackage:
    """Complete multi-language video production storyboard package."""
    package_id: str
    title: str
    topic: str
    presentation_mode: VideoPresentationMode
    target_duration_sec: int
    scenes: List[SceneSegment]
    supported_languages: List[VideoLanguage]
    word_counts: Dict[str, int]
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "package_id": self.package_id,
            "title": self.title,
            "topic": self.topic,
            "presentation_mode": self.presentation_mode.value,
            "target_duration_sec": self.target_duration_sec,
            "total_scenes": len(self.scenes),
            "scenes": [s.to_dict() for s in self.scenes],
            "supported_languages": [l.value for l in self.supported_languages],
            "word_counts": self.word_counts,
            "metadata": self.metadata,
        }


class ScriptArchitect:
    """
    Autonomous director that transforms any prompt or topic into a production-ready,
    multilingual video package with optimized hooks, pacing, and visual prompts.
    """

    DEFAULT_LANGUAGES = [
        VideoLanguage.ENGLISH,
        VideoLanguage.HINDI,
        VideoLanguage.BENGALI,
        VideoLanguage.SANSKRIT,
    ]

    # Speaking rates (approximate words per second by language)
    SPEAKING_RATES = {
        VideoLanguage.ENGLISH: 2.4,
        VideoLanguage.HINDI: 2.1,
        VideoLanguage.BENGALI: 2.0,
        VideoLanguage.SANSKRIT: 1.8,
    }

    @classmethod
    def create_script_package(
        cls,
        topic_or_prompt: str,
        presentation_mode: VideoPresentationMode = VideoPresentationMode.FACELESS_DOCUMENTARY,
        target_duration_minutes: int = 3,
        languages: Optional[List[VideoLanguage]] = None,
    ) -> VideoScriptPackage:
        """
        Creates a complete multi-scene, multi-language video storyboard package.
        """
        if not languages:
            languages = cls.DEFAULT_LANGUAGES

        # Clamp duration between 1 and 10 minutes
        clamped_minutes = max(1, min(10, target_duration_minutes))
        total_duration_sec = clamped_minutes * 60

        package_id = "VID-" + hashlib.sha256(topic_or_prompt.encode("utf-8")).hexdigest()[:10].upper()
        
        # Determine topic domain
        lower_t = topic_or_prompt.lower()
        if any(w in lower_t for w in ["quantum", "ai", "pqc", "tech", "semiconductor", "chip"]):
            domain = "DEEP_TECH"
            music_default = "FUTURISTIC_PULSE"
        elif any(w in lower_t for w in ["mahabharat", "ramayan", "vedic", "sanskrit", "history", "temple"]):
            domain = "CIVILIZATIONAL_ITIHASA"
            music_default = "EPIC_ANCIENT_SANSKRIT"
        elif any(w in lower_t for w in ["stock", "bank", "gold", "market", "economy", "rupee", "dollar"]):
            domain = "GEOECONOMIC_WEALTH"
            music_default = "TENSION_FINANCIAL_INVESTIGATIVE"
        else:
            domain = "GEOPOLITICAL_STRATEGY"
            music_default = "DRAMATIC_SOVEREIGN"

        # Break down into scenes (each scene ~6 to 10 seconds)
        scene_duration = 7.5
        scene_count = int(total_duration_sec / scene_duration)
        scenes: List[SceneSegment] = []

        character_ref = "Sovereign Strategic Analyst" if presentation_mode == VideoPresentationMode.WITH_FACE_AVATAR else None

        camera_motions = [
            "cinematic_slow_zoom_in",
            "slow_pan_left_to_right",
            "dramatic_aerial_orbit",
            "macro_tilt_down",
            "static_wide_epic",
        ]

        current_time = 0.0
        for i in range(1, scene_count + 1):
            start_t = current_time
            end_t = min(float(total_duration_sec), start_t + scene_duration)
            cam = camera_motions[(i - 1) % len(camera_motions)]

            # Generate narrative beats: Scene 1 = Viral Hook, Last Scene = Call to Action / Climax
            if i == 1:
                spoken = {
                    "en": f"What if everything you were told about {topic_or_prompt} was engineered to hide the real truth?",
                    "hi": f"क्या होगा अगर आपको {topic_or_prompt} के बारे में जो कुछ बताया गया, वो असली सच छुपाने के लिए रचा गया था?",
                    "bn": f"কেমন হতো যদি {topic_or_prompt} নিয়ে আপনাকে যা বলা হয়েছে, তার পুরোটাই আসল সত্য লুকানোর কৌশল হতো?",
                    "sa": f"किं यदि {topic_or_prompt} विषये यत् कथितम्, तत् सर्वं सत्यस्य आच्छादनाय एव आसीत्?",
                }
                v_prompt = f"Cinematic ultra-realistic 4K opening hook visual depicting {topic_or_prompt}, dramatic volumetric lighting, 8k resolution, photorealistic Unreal Engine 5 render."
                sfx = ["sub_bass_drop", "whoosh_impact"]
            elif i == scene_count:
                spoken = {
                    "en": "The evidence is undeniable. Question the narrative, look beyond the headlines, and follow for deeper sovereign intelligence.",
                    "hi": "सबूत अकाट्य हैं। इस नैरेटिव पर सवाल उठाइए, सुर्खियों से परे देखिए, और सटीक संप्रभु विश्लेषण के लिए जुड़े रहिए।",
                    "bn": "প্রমাণগুলি অনস্বীকার্য। এই বয়ানকে প্রশ্ন করুন, শিরোনামের আড়ালে তাকান, এবং গভীর সার্বভৌম বিশ্লেষণের সাথে থাকুন।",
                    "sa": "प्रमाणानि अकाट्यानि सन्ति। आख्यानं प्रति संशयं कुरुत, शीर्षकाणां परं पश्यत, सनातनसत्येन सह तिष्ठत।",
                }
                v_prompt = f"Epic climactic concluding scene on {topic_or_prompt}, golden hour illumination, cinematic depth of field, high-end production broadcast standard."
                sfx = ["epic_brass_crescendo"]
            else:
                progress = int((i / scene_count) * 100)
                spoken = {
                    "en": f"Analyzing key dimension {i}: how shifting global and technological powers alter reality across {progress}% of the strategic corridor.",
                    "hi": f"मुख्य आयाम {i} का विश्लेषण: किस तरह वैश्विक और तकनीकी बदलाव रणनीतिक गलियारे में वास्तविकता को बदल रहे हैं।",
                    "bn": f"প্রধান দিক {i} এর বিশ্লেষণ: কীভাবে বিশ্বব্যাপী এবং প্রযুক্তিগত রূপান্তর কৌশলগত করিডোরের বাস্তবতাকে পরিবর্তন করছে।",
                    "sa": f"प्रमुखविषयस्य {i} विश्लेषणम्: कथं वैश्विकपरिवर्तनानि अस्माकं संप्रभुतायां प्रभावं जनयन्ति।",
                }
                v_prompt = f"Detailed documentary B-roll visual showing technical and strategic aspects of {topic_or_prompt}, scene {i}, cinematic composition, hyper-detailed textures."
                sfx = ["light_whoosh"] if i % 2 == 0 else []

            scene = SceneSegment(
                scene_id=i,
                timestamp_start_sec=round(start_t, 2),
                timestamp_end_sec=round(end_t, 2),
                spoken_text=spoken,
                visual_prompt=v_prompt,
                camera_motion=cam,
                character_anchor=character_ref,
                music_mood=music_default,
                sound_effects=sfx,
            )
            scenes.append(scene)
            current_time = end_t
            if current_time >= total_duration_sec:
                break

        # Calculate word counts
        word_counts = {}
        for lang in languages:
            total_w = sum(len(s.spoken_text.get(lang.value, "").split()) for s in scenes)
            word_counts[lang.value] = total_w

        return VideoScriptPackage(
            package_id=package_id,
            title=f"Sovereign Intelligence: {topic_or_prompt[:50]}",
            topic=topic_or_prompt,
            presentation_mode=presentation_mode,
            target_duration_sec=total_duration_sec,
            scenes=scenes,
            supported_languages=languages,
            word_counts=word_counts,
            metadata={
                "domain": domain,
                "scene_count": len(scenes),
                "clamped_minutes": clamped_minutes,
                "character_anchor": character_ref,
            }
        )
