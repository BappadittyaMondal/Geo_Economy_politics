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
        elif any(w in lower_t for w in ["mahabharat", "ramayan", "vedic", "sanskrit", "history", "temple", "sinauli", "rakhigarhi"]):
            domain = "CIVILIZATIONAL_ITIHASA"
            music_default = "EPIC_ANCIENT_SANSKRIT"
        elif any(w in lower_t for w in ["fz1073", "aviation", "flight", "pilot", "sabotage", "cockpit", "terror"]):
            domain = "AVIATION_SECURITY"
            music_default = "TENSION_INVESTIGATIVE"
        elif any(w in lower_t for w in ["stock", "bank", "gold", "market", "economy", "rupee", "dollar", "svb", "repatriation", "700"]):
            domain = "GEOECONOMIC_WEALTH"
            music_default = "TENSION_FINANCIAL_INVESTIGATIVE"
        else:
            domain = "GEOPOLITICAL_STRATEGY"
            music_default = "DRAMATIC_SOVEREIGN"

        # Break down into scenes (each scene ~7.5 seconds)
        scene_duration = 7.5
        scene_count = max(4, int(total_duration_sec / scene_duration))
        scenes: List[SceneSegment] = []

        character_ref = "Sovereign Strategic Analyst" if presentation_mode == VideoPresentationMode.WITH_FACE_AVATAR else None

        camera_motions = [
            "cinematic_slow_zoom_in",
            "slow_pan_left_to_right",
            "dramatic_aerial_orbit",
            "macro_tilt_down",
            "static_wide_epic",
        ]

        beats = cls._build_thematic_story_beats(domain, topic_or_prompt, scene_count)

        current_time = 0.0
        for i in range(1, scene_count + 1):
            start_t = current_time
            end_t = min(float(total_duration_sec), start_t + scene_duration)
            cam = camera_motions[(i - 1) % len(camera_motions)]
            beat = beats[i - 1]

            scene = SceneSegment(
                scene_id=i,
                timestamp_start_sec=round(start_t, 2),
                timestamp_end_sec=round(end_t, 2),
                spoken_text=beat["spoken"],
                visual_prompt=beat["visual_prompt"],
                camera_motion=cam,
                character_anchor=character_ref,
                music_mood=beat.get("music_mood", music_default),
                sound_effects=beat.get("sound_effects", []),
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

    @classmethod
    def _get_localized_topic_label(cls, topic: str, domain: str, lang: VideoLanguage) -> str:
        """Returns idiomatic localized label for broadcast dialogue."""
        if lang == VideoLanguage.ENGLISH:
            return topic
        elif lang == VideoLanguage.HINDI:
            if domain == "GEOECONOMIC_WEALTH":
                return "अमेरिकी बैंकिंग संकट और संप्रभु स्वर्ण की वापसी"
            elif domain == "DEEP_TECH":
                return "पोस्ट-क्वांटम सुरक्षा और डिजिटल संप्रभुता"
            elif domain == "AVIATION_SECURITY":
                return "वाणिज्यिक विमानन सुरक्षा और कॉकपिट काउंटर-टेररिज्म"
            elif domain == "CIVILIZATIONAL_ITIHASA":
                return "सनातन इतिहास और पुरातात्विक सत्य"
            return "वैश्विक भू-राजनीतिक वास्तविकताओं"
        elif lang == VideoLanguage.BENGALI:
            if domain == "GEOECONOMIC_WEALTH":
                return "ব্যাংকিং ব্যবস্থার সংকট ও সার্বভৌম স্বর্ণ প্রত্যাবর্তন"
            elif domain == "DEEP_TECH":
                return "পোস্ট-কোয়ান্টাম সাইবার নিরাপত্তা ও প্রযুক্তিগত সার্বভৌমত্ব"
            elif domain == "AVIATION_SECURITY":
                return "বাণিজ্যিক বিমান নিরাপত্তা ও সন্ত্রাসবিরোধী প্রোটোকল"
            elif domain == "CIVILIZATIONAL_ITIHASA":
                return "সনাতন ইতিহাস ও প্রত্নতাত্ত্বিক প্রমাণ"
            return "বৈশ্বিক ভূ-রাজনৈতিক বাস্তবতা"
        elif lang == VideoLanguage.SANSKRIT:
            if domain == "GEOECONOMIC_WEALTH":
                return "कोषागारसङ्कटं संप्रभुस्वर्णप्रत्यावर्तनं च"
            elif domain == "DEEP_TECH":
                return "क्वांटम-सुरक्षा डिजिटल-संप्रभुता च"
            elif domain == "AVIATION_SECURITY":
                return "विमानसुरक्षा संप्रभुसंरक्षणं च"
            elif domain == "CIVILIZATIONAL_ITIHASA":
                return "सनातन-इतिहासः पुरातात्त्विक-सत्यं च"
            return "वैश्विक-सामरिक-सत्यम्"
        return topic

    @classmethod
    def _build_thematic_story_beats(cls, domain: str, topic: str, count: int) -> List[Dict[str, Any]]:
        """Constructs an ordered sequence of rich forensic narrative beats."""
        hi_label = cls._get_localized_topic_label(topic, domain, VideoLanguage.HINDI)
        bn_label = cls._get_localized_topic_label(topic, domain, VideoLanguage.BENGALI)
        sa_label = cls._get_localized_topic_label(topic, domain, VideoLanguage.SANSKRIT)

        if domain == "GEOECONOMIC_WEALTH":
            base_beats = [
                {
                    "spoken": {
                        "en": f"Behind the calm exterior of financial media, a seismic balance-sheet fracture is widening across the banking system.",
                        "hi": f"{hi_label} के पीछे की सच्चाई यह है कि वित्तीय प्रणाली में एक गहरा संतुलन-पत्र संकट आकार ले रहा है।",
                        "bn": f"{bn_label} এর আড়ালে বৈশ্বিক ব্যাংকিং ব্যবস্থায় এক মারাত্মক ব্যালেন্স শিট সংকট ঘনীভূত হচ্ছে।",
                        "sa": f"{sa_label} विषये वित्तीयविपण्याः शान्तेः पृष्ठतः, पाश्चात्यकोषागारेषु गभीरं तुलनपत्रसङ्कटं समुत्पद्यते।",
                    },
                    "visual_prompt": "Cinematic 4K hyper-realistic macro tracking shot across Wall Street trading floor with red downward telemetry overlays, moody volumetric lighting, Unreal Engine 5 broadcast quality.",
                    "sfx": ["sub_bass_drop", "ticker_tape_flutter"],
                    "music_mood": "TENSION_FINANCIAL_INVESTIGATIVE"
                },
                {
                    "spoken": {
                        "en": "The core trigger: the Federal Reserve's fastest rate hiking cycle in 40 years, from 0 to over 5.25 percent, decimating held-to-maturity Treasury portfolios.",
                        "hi": "मुख्य कारण: पिछले 40 वर्षों में फेडरल रिजर्व की सबसे आक्रामक ब्याज दर वृद्धि, जिसने बैंकों के दीर्घकालिक बॉन्ड पोर्टफोलियो का बाजार मूल्य गिरा दिया।",
                        "bn": "মূল কারণ: গত ৪০ বছরে ফেডারেল রিজার্ভের সবচেয়ে দ্রুত সুদের হার বৃদ্ধি, যা ব্যাংকগুলির দীর্ঘমেয়াদী বন্ড পোর্টফোলিওর বাজারমূল্য ধ্বংস করেছে।",
                        "sa": "मूलकारणं तु: चत्वारिंशद्वर्षेषु तीव्रतमं व्याजदरवर्धनम्, येन दीर्घकालिकऋणपत्राणां विपण्मूल्यं क्षीणं जातम्।",
                    },
                    "visual_prompt": "Technical financial forensic visualization showing US Treasury bond yield curve inversion and steep unrealized loss curves, clean holographic data graph.",
                    "sfx": ["digital_data_blip"],
                    "music_mood": "TENSION_FINANCIAL_INVESTIGATIVE"
                },
                {
                    "spoken": {
                        "en": "Over 700 regional banks are now trapped with massive unrealized bond losses, compounded by a looming Commercial Real Estate refinancing cliff.",
                        "hi": "700 से अधिक अमेरिकी क्षेत्रीय बैंक अब हेल्ड-टू-मैच्योरिटी परिसंपत्तियों पर भारी अवास्तविक घाटे और वाणिज्यिक रियल एस्टेट कर्ज संकट में फंसे हैं।",
                        "bn": "৭০০টিরও বেশি আঞ্চলিক ব্যাংক এখন বিশাল অবাস্তবায়িত লোকসান এবং বাণিজ্যিক রিয়েল এস্টেট ঋণের মেয়াদপূর্তির ফাঁদে আটকা পড়েছে।",
                        "sa": "सप्तशताधिकाः प्रादेशिककोषागाराः अवास्तविकहानिग्रस्ताः सन्ति, वाणिज्यिकभूमिसंकटेन च संपीडिताः।",
                    },
                    "visual_prompt": "Dramatic aerial establishing shot of American regional bank branches in dusk light, cinematic anamorphic lens, high contrast shadows.",
                    "sfx": ["low_drone"],
                    "music_mood": "TENSION_FINANCIAL_INVESTIGATIVE"
                },
                {
                    "spoken": {
                        "en": "Simultaneously, the geopolitical weaponization of dollar clearing and reserve asset freezes has driven sovereign nations to seek un-cancellable monetary alternatives.",
                        "hi": "साथ ही, डॉलर निपटान के भू-राजनीतिक शस्त्रीकरण और विदेशी मुद्रा भंडारों की जब्ती ने संप्रभु राष्ट्रों को सुरक्षित विकल्पों की ओर मोड़ दिया है।",
                        "bn": "একই সাথে, ডলারের ভূ-রাজনৈতিক অস্ত্রায়ন এবং রিজার্ভ জব্দকরণের ফলে সার্বভৌম দেশগুলি নির্ভরযোগ্য বিকল্পের দিকে ঝুঁকছে।",
                        "sa": "युगपदेव, मुद्रायाः शस्त्रीकरणेन संप्रभुराष्ट्राणि सुरक्षितविकल्पान् अन्वेष्टुं प्रवृत्तानि सन्ति।",
                    },
                    "visual_prompt": "Global map showing non-dollar bilateral settlement corridors between New Delhi, Moscow, Riyadh, and Abu Dhabi with glowing trade vectors.",
                    "sfx": ["whoosh_impact"],
                    "music_mood": "STRATEGIC_MOMENTUM"
                },
                {
                    "spoken": {
                        "en": "Central banks responded by accumulating physical gold at a 55-year record pace, physically repatriating thousands of metric tonnes from London vaults directly to domestic soil.",
                        "hi": "केंद्रीय बैंकों ने 55 वर्षों के रिकॉर्ड स्तर पर भौतिक सोना खरीदकर जवाब दिया, और लंदन की तिजोरियों से हजारों टन स्वर्ण अपने घरेलू कोषों में वापस मंगाया।",
                        "bn": "কেন্দ্রীয় ব্যাংকগুলি ৫৫ বছরের রেকর্ড গতিতে সোনা সংগ্রহ করে এবং লন্ডনের ভল্ট থেকে হাজার হাজার টন স্বর্ণ নিজ দেশে ফিরিয়ে এনে জবাব দিয়েছে।",
                        "sa": "केंद्रीयकोषागाराः पञ्चपञ्चाशद्वर्षेषु सर्वाधिकं भौतिकस्वर्णं संगृह्य, लण्डनकोषागारात् स्वभूभौ प्रत्यावर्तितवन्तः।",
                    },
                    "visual_prompt": "Cinematic close-up of solid 99.99% pure 24-carat gold bullion bars stamped with sovereign seals in an ultra-secure vault, dramatic rim lighting.",
                    "sfx": ["vault_lock_clank", "metallic_ring"],
                    "music_mood": "EPIC_SOVEREIGN_RESOLVE"
                },
                {
                    "spoken": {
                        "en": "Under the Dr. Ankit Shah macro-monetary lens, paper debt promises are losing supremacy to sovereign balance-sheet reality: physical gold carries zero counterparty default risk.",
                        "hi": "डॉ. अंकित शाह के मौद्रिक विश्लेषण के अनुसार, कागजी कर्ज वादों की प्रधानता समाप्त हो रही है: भौतिक स्वर्ण में शून्य प्रतिपक्ष जोखिम होता है।",
                        "bn": "ড. অঙ্কিত শাহের সামষ্টিক মুদ্রানীতি বিশ্লেষণ অনুযায়ী, কাগজের ঋণের দাপট শেষ হচ্ছে: নিখাদ শারীরিক স্বর্ণে কোনো কাউন্টারপার্টি ঝুঁকি থাকে না।",
                        "sa": "अंकित-शाह-वित्तीयदृष्ट्या, पत्रऋणस्य प्राधान्यं नश्यति: भौतिकस्वर्णस्य प्रत्यर्थिजोखिमः शून्यः भवति।",
                    },
                    "visual_prompt": "Forensic balance sheet comparison showing depreciating paper fiat currencies versus an ascending physical gold reserve bar, 4K motion graphics.",
                    "sfx": ["deep_hit"],
                    "music_mood": "FORENSIC_TRIUMPH"
                },
                {
                    "spoken": {
                        "en": "India's Reserve Bank led by example, repatriating over 100 tonnes of physical gold to secure the rupee against external debt contagion and currency blackmail.",
                        "hi": "भारतीय रिज़र्व बैंक ने अनुकरणीय नेतृत्व करते हुए 100 टन से अधिक सोना स्वदेश लाकर बाहरी कर्ज संकट और मुद्रा ब्लैकमेल से रुपये को सुरक्षित किया।",
                        "bn": "ভারতের রিজার্ভ ব্যাংক দৃষ্টান্ত স্থাপন করে ১০০ টনেরও বেশি স্বর্ণ দেশে ফিরিয়ে এনে বাহ্যিক আর্থিক আক্রমণ থেকে রুপিয়াকে সুরক্ষিত করেছে।",
                        "sa": "भारतीय-रिजर्व-बैंक-संस्थया शतटनाधिकं स्वर्णं स्वदेशं समानीय, बाह्यसंकटात् संप्रभुमुद्रा रक्षिता।",
                    },
                    "visual_prompt": "High-security RBI convoy carrying armored sovereign gold bullion crates in Mumbai, cinematic golden hour lighting, photorealistic.",
                    "sfx": ["engine_hum", "brass_crescendo"],
                    "music_mood": "EPIC_NATIONAL_PRIDE"
                },
                {
                    "spoken": {
                        "en": "The lesson is clear: when banking illusions dissolve, tangible sovereign reserves endure. Scrutinize the numbers, protect sovereign assets, and subscribe for deeper strategic intelligence.",
                        "hi": "सबक स्पष्ट है: जब वित्तीय भ्रम टूटते हैं, तो केवल ठोस संप्रभु संपत्तियां ही टिकती हैं। आंकड़ों की पड़ताल करें और सटीक संप्रभु विश्लेषण के लिए जुड़े रहें।",
                        "bn": "শিক্ষাটি স্পষ্ট: যখন ব্যাংকিং বিভ্রম ভেঙে পড়ে, তখন কেবল বাস্তব সার্বভৌম সম্পদই টিকে থাকে। তথ্যের বিশ্লেষণ করুন এবং গভীর সার্বভৌম বুদ্ধিমত্তার সাথে থাকুন।",
                        "sa": "शिक्षा स्पष्टा: यदा वित्तीयभ्रमाः नश्यन्ति, तदा भौतिकसंप्रभुसंपदः एव तिष्ठन्ति। सत्यं परीक्षत, संप्रभुबुद्ध्या सह तिष्ठत।",
                    },
                    "visual_prompt": "Majestic concluding panoramic vista of the Indian Parliament and Reserve Bank headquarters under sunrise skies, epic 8K broadcast cinematography.",
                    "sfx": ["epic_brass_crescendo"],
                    "music_mood": "DRAMATIC_SOVEREIGN"
                },
            ]
        elif domain == "DEEP_TECH":
            base_beats = [
                {
                    "spoken": {
                        "en": f"A silent cryptographic revolution is underway, threatening to dissolve modern public-key encryption across banking and national defense.",
                        "hi": f"{hi_label} के अंतर्गत आधुनिक बैंकिंग और राष्ट्रीय सुरक्षा को सुरक्षित रखने वाली एन्क्रिप्शन प्रणाली पर बड़ा संकट आ चुका है।",
                        "bn": f"{bn_label} এর ক্ষেত্রে আধুনিক ব্যাংকিং ও জাতীয় সুরক্ষার ক্রিপ্টোগ্রাফিক ব্যবস্থা এক নীরব বিপ্লবের মুখোমুখি।",
                        "sa": f"{sa_label} विषये आधुनिक-गूढलेखन-प्रणाल्याः उपरि गभीरः संशयः समुत्पन्नः अस्ति।",
                    },
                    "visual_prompt": "Futuristic high-tech visualization of quantum superposition qubits interacting with classical binary encryption keys, neon cyan and deep amber lighting, 8K resolution.",
                    "sfx": ["quantum_hum", "data_stream"],
                    "music_mood": "FUTURISTIC_PULSE"
                },
                {
                    "spoken": {
                        "en": "Shor's algorithm executed on fault-tolerant quantum hardware can theoretically crack RSA and elliptic curve protocols within minutes, enabling Harvest Now, Decrypt Later espionage.",
                        "hi": "शोर का एल्गोरिदम भविष्य के क्वांटम कंप्यूटरों पर आरएसए और एलिप्टिक कर्व एन्क्रिप्शन को मिनटों में तोड़ सकता है, जिससे पहले डेटा चुराकर बाद में डिक्रिप्ट करने का खतरा बढ़ गया है।",
                        "bn": "শোরের অ্যালগরিদম কোয়ান্টাম কম্পিউটারে আরএসএ এবং উপবৃত্তাকার কার্ভ এনক্রিপশন কয়েক মিনিটের মধ্যে ভেঙে ফেলতে পারে।",
                        "sa": "शोर-विधिः क्वांटम-संगणके प्रचलितः सन् क्षणाभ्यन्तरे पुरातन-गूढलेखनं भङ्क्तुं शक्नोति।",
                    },
                    "visual_prompt": "Forensic cybersecurity visualization showing high-speed cryptographic key factorisation in holographic 3D, matrix data streams.",
                    "sfx": ["matrix_beep"],
                    "music_mood": "FUTURISTIC_PULSE"
                },
                {
                    "spoken": {
                        "en": "Simultaneously, extreme ultraviolet lithography bottlenecks concentrate advanced sub-2 nanometer fabrication into a fragile handful of geographical nodes.",
                        "hi": "इसके साथ ही, अत्यधिक पराबैंगनी लिथोग्राफी तकनीक ने उन्नत सब-2 नैनोमीटर चिप निर्माण को कुछ सीमित भौगोलिक केंद्रों तक समेट दिया है।",
                        "bn": "একই সাথে, চরম অতিবেগুনি লিথোগ্রাফির সীমাবদ্ধতা উন্নত সেমিকন্ডাক্টর উৎপাদনকে কয়েকটি নির্দিষ্ট ভৌগোলিক কেন্দ্রে কেন্দ্রীভূত করেছে।",
                        "sa": "युगपदेव, सूक्ष्मतम-सिलिकॉन-निर्माणं कतिपयेषु एव वैश्विक-केन्द्रेषु संकुचितं जातम्।",
                    },
                    "visual_prompt": "Cleanroom photolithography machine inside a semiconductor mega-fab with robotic arms manipulating silicon wafers under yellow cleanroom illumination.",
                    "sfx": ["robotic_servo", "air_filter_hum"],
                    "music_mood": "TENSION_INVESTIGATIVE"
                },
                {
                    "spoken": {
                        "en": "Sovereign nations are accelerating deployment of lattice-based post-quantum cryptographic standards like ML-KEM and ML-DSA to shield central banking networks.",
                        "hi": "संप्रभु राष्ट्र अपने केंद्रीय बैंकिंग नेटवर्क की रक्षा के लिए लैटिस-आधारित पोस्ट-क्वांटम मानकों जैसे एमएल-केईएम और एमएल-डीएसए को तेजी से लागू कर रहे हैं।",
                        "bn": "সার্বভৌম রাষ্ট্রগুলি তাদের ব্যাংকিং নেটওয়ার্ক সুরক্ষায় ল্যাটিস-ভিত্তিক পোস্ট-কোয়ান্টাম ক্রিপ্টোগ্রাফি দ্রুত মোতায়েন করছে।",
                        "sa": "संप्रभुराष्ट्राणि केंद्रीयकोषागारसंरक्षणाय नूतन-क्वांटम-सुरक्षा-प्रणालीं त्वरया प्रवर्तयन्ति।",
                    },
                    "visual_prompt": "Multi-layered cryptographic lattice geometric structure forming an impenetrable shield over sovereign data servers, cinematic 4K render.",
                    "sfx": ["shield_activation"],
                    "music_mood": "STRATEGIC_MOMENTUM"
                },
                {
                    "spoken": {
                        "en": "Technological sovereignty requires full-stack control: from domestic instruction set architectures to proprietary hardware security modules and secure subsea landing stations.",
                        "hi": "प्रौद्योगिक संप्रभुता के लिए संपूर्ण स्टैक पर नियंत्रण आवश्यक है: घरेलू प्रोसेसर आर्किटेक्चर से लेकर स्वदेशी सुरक्षा मॉड्यूल और सबसी केबल लैंडिंग स्टेशनों तक।",
                        "bn": "প্রযুক্তিগত সার্বভৌমত্বের জন্য সম্পূর্ণ স্তরে নিয়ন্ত্রণ প্রয়োজন: নিজস্ব প্রসেসর আর্কিটেকচার থেকে সুরক্ষিত সাবসি কেবল ল্যান্ডিং স্টেশন পর্যন্ত।",
                        "sa": "प्रौद्योगिकसंप्रभुतायै समग्रनियन्त्रणं आवश्यकम्: स्वदेशी-संसाधकेभ्यः आरभ्य सागरकेबलस्थानपर्यन्तम्।",
                    },
                    "visual_prompt": "High-tech map of India showing semiconductor fab corridors, quantum communication links, and subsea fiber landing hubs glowing in electric blue.",
                    "sfx": ["pulse_sweep"],
                    "music_mood": "EPIC_SOVEREIGN_RESOLVE"
                },
                {
                    "spoken": {
                        "en": "The final verdict: in an age of quantum intelligence, dependence on foreign cryptographic stacks is equivalent to voluntary strategic surrender.",
                        "hi": "अंतिम निष्कर्ष: क्वांटम युग में विदेशी तकनीक और एन्क्रिप्शन पर निर्भरता रणनीतिक आत्मसमर्पण के समान है। संप्रभु तकनीकी सुरक्षा ही वास्तविक स्वतंत्रता है।",
                        "bn": "চূড়ান্ত সিদ্ধান্ত: কোয়ান্টাম বুদ্ধিমত্তার যুগে বিদেশি এনক্রিপশনের ওপর নির্ভরতা কৌশলগত আত্মসমর্পণের সমান। সার্বভৌম প্রযুক্তির সাথেই থাকুন।",
                        "sa": "अन्तिमनिर्णयः: क्वांटम-युगे वैदेशिक-प्रौद्योगिकी-निर्भरता सामरिक-समर्पण-समाना भवति। संप्रभुज्ञानमेव परमरक्षा।",
                    },
                    "visual_prompt": "Epic sovereign tech command center with analysts monitoring real-time quantum network integrity against a panoramic cityscape backdrop.",
                    "sfx": ["epic_brass_crescendo"],
                    "music_mood": "DRAMATIC_SOVEREIGN"
                },
            ]
        elif domain == "AVIATION_SECURITY":
            base_beats = [
                {
                    "spoken": {
                        "en": f"Commercial flight decks represent vital sovereign corridors, where a single breach can rapidly escalate into a national security crisis.",
                        "hi": f"{hi_label} यह दर्शाता है कि वाणिज्यिक कॉकपिट देश की संप्रभु सीमाएं हैं, जहां एक भी चूक गंभीर सुरक्षा संकट बन सकती है।",
                        "bn": f"{bn_label} প্রমাণ করে যে বাণিজ্যিক বিমান করিডোরগুলি অত্যন্ত সংবেদনশীল জাতীয় সুরক্ষার অংশ।",
                        "sa": f"{sa_label} इत्यनेन स्पष्टं भवति यत् वाणिज्यिकविमानकक्षाः राष्ट्रिय-संप्रभुतायाः संवेदनशीलाः विभागाः सन्ति।",
                    },
                    "visual_prompt": "Dramatic night cockpit POV showing heads-up display instruments, runway approach lights through rain-streaked windshield, ultra-photorealistic.",
                    "sfx": ["cockpit_avionics_chime", "engine_thrust"],
                    "music_mood": "TENSION_INVESTIGATIVE"
                },
                {
                    "spoken": {
                        "en": "The harrowing incident on FlyDubai Flight FZ1073 demonstrated the lethal peril of insider cockpit assault and the irreplaceable value of pilot composure under duress.",
                        "hi": "फ्लाईदुबई उड़ान एफजेड1073 की घटना ने कॉकपिट के भीतर अचानक हमले के घातक खतरे और पायलट के असाधारण धैर्य के महत्व को साबित किया।",
                        "bn": "ফ্লাইদুবাই ফ্লাইট এফজেড১০৭৩ এর ঘটনাটি ককপিটের ভেতরে আকস্মিক হামলার মারাত্মক ঝুঁকিকে স্পষ্ট করে তুলেছে।",
                        "sa": "फ्लाईदुबई-विमानघटनायां कॉकपिट-मध्ये आकस्मिक-आक्रमणस्य भयानकता स्पष्टीकृता, वैमानिकस्य धैर्यं च प्रशंसितम्।",
                    },
                    "visual_prompt": "Tense cinematic reconstruction of an airline cockpit interior at 35,000 feet, low key lighting, high tension atmosphere.",
                    "sfx": ["alarm_whoop", "radio_static"],
                    "music_mood": "TENSION_INVESTIGATIVE"
                },
                {
                    "spoken": {
                        "en": "Captain Smit Machchhar's rapid reaction neutralized an attempted suicide dive, preventing catastrophic disaster and prompting worldwide re-evaluations of cockpit crash-axe protocols.",
                        "hi": "कैप्टन स्मित मछार के त्वरित साहस ने आत्मघाती हमले को विफल किया और दुनिया भर में कॉकपिट क्रैश-कुल्हाड़ी सुरक्षा नियमों की तत्काल समीक्षा कराई।",
                        "bn": "ক্যাপ্টেন স্মিত মচ্ছারের সময়োপযোগী সাহসিকতা আত্মঘাতী হামলা ব্যর্থ করে দেয় এবং বিশ্বব্যাপী ককপিট সুরক্ষা বিধির পুনর্মূল্যায়ন ঘটায়।",
                        "sa": "कॅप्टन स्मित महोदयेन त्वरितसाहसेन आत्मघाती-प्रयासः विफलीकृतः, वैश्विकसुरक्षानियमानां च पुनरीक्षणं कारितम्।",
                    },
                    "visual_prompt": "Commercial airliner stabilizing in stormy skies, regaining smooth level flight above dramatic cloud layers, cinematic lighting.",
                    "sfx": ["level_off_chime", "sub_bass_relief"],
                    "music_mood": "STRATEGIC_MOMENTUM"
                },
                {
                    "spoken": {
                        "en": "Coupled with cyber-spoofing of ADS-B transponders and dual-use biosecurity protocols, aviation counter-terrorism demands proactive sovereign surveillance.",
                        "hi": "जीपीएस स्पूफिंग और ट्रांसपोंडर साइबर हमलों के साथ, विमानन काउंटर-टेररिज्म के लिए पूर्ण संप्रभु निगरानी प्रणाली की आवश्यकता है।",
                        "bn": "জিপিএস স্পুফিং এবং ট্রান্সপন্ডার সাইবার ঝুঁকির প্রেক্ষাপটে বিমান চলাচলে সার্বভৌম নজরদারি আরও জরুরি হয়ে উঠেছে।",
                        "sa": "सायबर-आक्रमणानां रडार-व्याघातानां च मध्ये विमानसुरक्षायै संप्रभुसतर्कता अत्यावश्यकी अस्ति।",
                    },
                    "visual_prompt": "Air traffic control radar screen showing encrypted aircraft flight tracks across international airspace boundaries, crisp UI vectors.",
                    "sfx": ["radar_sweep"],
                    "music_mood": "TENSION_INVESTIGATIVE"
                },
                {
                    "spoken": {
                        "en": "The Ajit Doval doctrine dictates defensive-offensive preparedness: sovereign boundaries extend to every passenger manifest and every kilowatt of avionics telecommand.",
                        "hi": "अजीत डोभाल का सुरक्षा सिद्धांत स्पष्ट है: राष्ट्रीय सुरक्षा कॉकपिट के हर स्विच और यात्री मैनिफेस्ट तक विस्तृत होती है। किसी भी ढिलाई की कोई गुंजाइश नहीं है।",
                        "bn": "অজিত ডোভালের সুরক্ষা নীতি নির্দেশ করে: আকাশসীমার প্রতিটি করিডোরে কোনো অসাবধানতার স্থান নেই।",
                        "sa": "अजीत-डोभाल-नीतिः कथयति: संप्रभुसीमाः विमानस्य प्रत्येकस्मिन् भागे वर्तन्ते, प्रमादाय अवकाशः नास्ति।",
                    },
                    "visual_prompt": "Indian Air Force Su-30MKI fighter jet escorting an airliner at golden hour, powerful contrails, stunning cinematic depth.",
                    "sfx": ["jet_flyby", "brass_fanfare"],
                    "music_mood": "EPIC_SOVEREIGN_RESOLVE"
                },
                {
                    "spoken": {
                        "en": "Sovereignty requires zero-compromise vigilance. Respect the unsung guardians of the skies, question bureaucratic complacency, and stay tuned for deep forensic insights.",
                        "hi": "संप्रभुता का अर्थ है शून्य-समझौता सतर्कता। आसमान के मौन रक्षकों का सम्मान करें और सटीक संप्रभु विश्लेषण के लिए जुड़े रहें।",
                        "bn": "সার্বভৌমত্ব মানে আপসহীন সতর্কতা। আকাশের নিঃশব্দ প্রহরীদের সম্মান জানান এবং গভীর সুরক্ষামূলক বিশ্লেষণের সাথে থাকুন।",
                        "sa": "संप्रभुता नाम असंशयसतर्कता। आकाशस्य मौनरक्षकान् नमस्कृत्य, सनातनसत्येन सह तिष्ठत।",
                    },
                    "visual_prompt": "Majestic airport runway at dawn with silhouette of pilots and an airliner taxiing beneath golden sunrise clouds.",
                    "sfx": ["epic_brass_crescendo"],
                    "music_mood": "DRAMATIC_SOVEREIGN"
                },
            ]
        elif domain == "CIVILIZATIONAL_ITIHASA":
            base_beats = [
                {
                    "spoken": {
                        "en": f"Colonial historiography sought to sever Bharat from its millennial roots, yet incontrovertible ground excavations are restoring the unbroken timeline.",
                        "hi": f"{hi_label} के पुरातात्विक साक्ष्य यह सिद्ध करते हैं कि औपनिवेशिक इतिहासकारों द्वारा गढ़े गए नैरेटिव पूरी तरह ध्वस्त हो चुके हैं।",
                        "bn": f"{bn_label} এর প্রত্নতাত্ত্বিক প্রমাণগুলি ঔপনিবেশিক ইতিহাসবিদদের চাপিয়ে দেওয়া মিথ্যা বয়ানকে সম্পূর্ণ ভেঙে চুরমার করেছে।",
                        "sa": f"{sa_label} विषये पुरातात्त्विक-प्रमाणानि औपनिवेशिक-मिथ्याख्यानं पूर्णतया खण्डयन्ति।",
                    },
                    "visual_prompt": "Cinematic aerial tracking shot over ancient archaeological dig at Sanauli, revealing royal burial chambers and copper antennae swords under golden light.",
                    "sfx": ["wind_chime", "distant_conch"],
                    "music_mood": "EPIC_ANCIENT_SANSKRIT"
                },
                {
                    "spoken": {
                        "en": "The sensational discovery of solid-disk wheel chariots at Sinauli dating to 2000 BCE shattered the Aryan Invasion theory with tangible kinetic bronze engineering.",
                        "hi": "सनौली में 2000 ईसा पूर्व के ठोस पहियों वाले युद्ध-रथों की खोज ने विदेशी आक्रमण के सिद्धांत को हमेशा के लिए दफन कर दिया।",
                        "bn": "সনৌলিতে ২০০০ খ্রিস্টপূর্বাব্দের ব্রোঞ্জ যুগের যুদ্ধের রথ আবিষ্কার আর্য আগ্রাসন তত্ত্বকে সরাসরি নস্যাৎ করে দিয়েছে।",
                        "sa": "सनौली-क्षेत्रे द्वि-सहस्र-वर्ष-पुरातनानां रथानां प्राप्तिः वैदेशिक-आक्रमण-वादं समूलं उन्मूलयति।",
                    },
                    "visual_prompt": "Ultra-detailed 3D photorealistic reconstruction of a Sanauli Bronze Age warrior chariot with copper repousse ornamentation, 8K Unreal Engine 5 render.",
                    "sfx": ["bronze_strike", "chariot_rumble"],
                    "music_mood": "EPIC_ANCIENT_SANSKRIT"
                },
                {
                    "spoken": {
                        "en": "Rakhigarhi paleogenomic DNA studies confirmed genetic continuity across thousands of years, proving our civilizational roots are indigenous and indivisible.",
                        "hi": "राखीगढ़ी के प्राचीन डीएनए अध्ययनों ने साबित कर दिया है कि हमारी आनुवंशिक और सांस्कृतिक निरंतरता पूरी तरह स्वदेशी और अटूट है।",
                        "bn": "রাখিগড়ির প্রাচীন ডিএনএ গবেষণা প্রমাণ করেছে যে আমাদের বংশগত এবং সাংস্কৃতিক ধারা সম্পূর্ণ আদিবাসী এবং অবিভাজ্য।",
                        "sa": "राखीगढ़ी-डीएनए-परीक्षणैः सिद्धं यत् अस्माकं सभ्यतायाः मूलानि स्वदेशीयानि निरन्तराणि च सन्ति।",
                    },
                    "visual_prompt": "Scientific paleogenomic laboratory showing DNA double helix morphing into ancient Indus-Saraswati geometric seals, clean holographic visuals.",
                    "sfx": ["dna_chime"],
                    "music_mood": "EPIC_ANCIENT_SANSKRIT"
                },
                {
                    "spoken": {
                        "en": "Rigorous archaeoastronomy corroborates the astronomical observations embedded within the Valmiki Ramayana and Vyasa Mahabharata with mathematical precision.",
                        "hi": "वाल्मीकि रामायण और व्यास महाभारत में वर्णित खगोलीय ग्रहों की स्थितियों को आधुनिक खगोल विज्ञान ने गणितीय रूप से सत्यापित किया है।",
                        "bn": "রামায়ণ এবং মহাভারতে উল্লিখিত গ্রহ-নক্ষত্রের অবস্থান আধুনিক জ্যোতির্বিজ্ঞানের সাহায্যে গাণিতিকভাবে নির্ভুল প্রমাণিত হয়েছে।",
                        "sa": "रामायण-महाभारतयोः वर्णितानि खगोलीय-दृश्यानि आधुनिक-ज्योतिर्विज्ञानेन पूर्णतया सत्यानि सिद्धानानि।",
                    },
                    "visual_prompt": "Magnificent planetarium night sky rendering showing the exact planetary alignments described in ancient texts above a temple silhouette.",
                    "sfx": ["celestial_shimmer"],
                    "music_mood": "EPIC_ANCIENT_SANSKRIT"
                },
                {
                    "spoken": {
                        "en": "From Kautilya's Arthashastra to the sacred architecture of our grand temples, Sanatan statecraft harmonizes ethical Rajdharma with uncompromising national defense.",
                        "hi": "कौटिल्य के अर्थशास्त्र से लेकर हमारे भव्य मंदिरों की वास्तुकला तक, सनातन राजधर्म नैतिक मूल्यों और सशक्त राष्ट्रीय सुरक्षा का अद्भुत संगम है।",
                        "bn": "কৌটিল্যের অর্থশাস্ত্র থেকে শুরু করে সনাতন দেবালয় পর্যন্ত, আমাদের সভ্যতা নৈতিক রাজধর্ম এবং অপ্রতিরোধ্য সুরক্ষার মেলবন্ধন।",
                        "sa": "कौटिलीय-अर्थशास्त्रात् आरभ्य भव्यमन्दिराणि यावत्, सनातन-राजधर्मः नैतिकतायाः दृढसुरक्षायाः च अद्वितीयः सङ्गमः।",
                    },
                    "visual_prompt": "Majestic drone orbit of the illuminated Brihadisvara Temple gopuram with ancient Sanskrit inscriptions glowing in golden light.",
                    "sfx": ["temple_bell_ring"],
                    "music_mood": "EPIC_ANCIENT_SANSKRIT"
                },
                {
                    "spoken": {
                        "en": "A nation that reclaims its memory cannot be subjugated by cognitive warfare. Stand firm in civilizational truth, and follow for deeper historical forensics.",
                        "hi": "जो राष्ट्र अपने वास्तविक इतिहास को पहचान लेता है, उसे मानसिक रूप से कभी गुलाम नहीं बनाया जा सकता। सनातन सत्य के साथ खड़े रहें।",
                        "bn": "যে জাতি নিজের আসল ইতিহাস চিনে নেয়, তাকে কোনো মনস্তাত্ত্বিক যুদ্ধে পরাজিত করা যায় না। ঐতিহাসিক সত্যের সাথে থাকুন।",
                        "sa": "यत् राष्ट्रं स्व-इतिहासम् अभिजानाति, तत् कदापि पराजितं न भवति। सनातनसत्येन सह तिष्ठत।",
                    },
                    "visual_prompt": "Epic grand vista of the rising sun over the Himalayas with ancient Vedic scholars and modern scientists standing together in harmony.",
                    "sfx": ["epic_brass_crescendo", "resonant_conch"],
                    "music_mood": "DRAMATIC_SOVEREIGN"
                },
            ]
        else:  # GEOPOLITICAL_STRATEGY
            base_beats = [
                {
                    "spoken": {
                        "en": f"Beneath choreographed diplomatic photocalls, raw sovereign interests and kinetic realities dictate the true balance of power.",
                        "hi": f"{hi_label} की औपचारिक वार्ताओं के पीछे, असली शक्ति संतुलन जमीनी और सामरिक वास्तविकताओं से तय होता है।",
                        "bn": f"{bn_label} এর কূটনৈতিক হাসিমুখের আড়ালে আসল ক্ষমতার ভারসাম্য নির্ধারিত হয় ভূ-রাজনৈতিক বাস্তবতায়।",
                        "sa": f"{sa_label} विषये राजनयिक-वार्तानां पृष्ठतः, वास्तविकं शक्तिसन्तुलनं सामरिक-सत्येन एव निर्णीयते।",
                    },
                    "visual_prompt": "Cinematic establishing shot of a high-level geopolitical summit hall with red carpet, international flags, and tense diplomatic delegates in conversation.",
                    "sfx": ["sub_bass_drop", "camera_flash_clicks"],
                    "music_mood": "DRAMATIC_SOVEREIGN"
                },
                {
                    "spoken": {
                        "en": "Epistemic Tier 1 reality supersedes rhetoric: troop deployments, perimeter fortifications, and satellite verified logistics reveal what communiqués conceal.",
                        "hi": "कथनी से बड़ी करनी होती है: वास्तविक सीमा पर सेना की तैनाती, बंकर और उपग्रह द्वारा जांची गई रसद ही असल स्थिति बताती है।",
                        "bn": "কথার চেয়ে কাজের গুরুত্ব বেশি: সীমান্তে সেনার অবস্থান এবং উপগ্রহের ছবি যা প্রকাশ করে, তা কোনো যৌথ বিবৃতিতে থাকে না।",
                        "sa": "प्रत्यक्षप्रमाणं सर्वोपरि: सीमासु सैन्यविन्यासः उपग्रहचित्राणि च सत्यं प्रकाशयन्ति।",
                    },
                    "visual_prompt": "Split screen showing high-resolution satellite imagery of strategic border infrastructure and troop logistical corridors with digital coordinate grids.",
                    "sfx": ["satellite_uplink"],
                    "music_mood": "TENSION_INVESTIGATIVE"
                },
                {
                    "spoken": {
                        "en": "Financial forensics unmask unfinanced MOUs: real sovereignty is measured by executed capital expenditure and resilient cross-border settlement channels.",
                        "hi": "वित्तीय वास्तविकता दिखावटी समझौतों की पोल खोल देती है: वास्तविक संप्रभुता वास्तविक पूंजी निवेश और सुरक्षित व्यापारिक गलियारों से मापी जाती है।",
                        "bn": "আর্থিক বিশ্লেষণ মৌখিক চুক্তির ফাঁকফোকর ফাঁস করে দেয়: প্রকৃত সার্বভৌমত্ব পরিমাপ করা হয় কার্যকরী বিনিয়োগের মাধ্যমে।",
                        "sa": "वित्तीयसत्यं केवलं पत्राचारं खण्डयति: वास्तविकं संप्रभुत्वं निवेशेन व्यापारसुरक्षया च ज्ञायते।",
                    },
                    "visual_prompt": "Forensic data flow graphic tracing real trade settlement volumes versus inflated ceremonial press releases, clean modern financial charts.",
                    "sfx": ["data_stream"],
                    "music_mood": "TENSION_FINANCIAL_INVESTIGATIVE"
                },
                {
                    "spoken": {
                        "en": "Through the strategic lens of S. Jaishankar, multi-alignment is not neutrality; it is the agile pursuit of national interest in a fragmented world.",
                        "hi": "डॉ. एस. जयशंकर के रणनीतिक दृष्टिकोण के अनुसार, बहु-संरेखण तटस्थता नहीं है, बल्कि बदलते विश्व में राष्ट्रीय हितों की निर्भीक साधना है।",
                        "bn": "ড. এস. জয়শঙ্করের কূটনীতির মূল কথা: বহুমুখী মিত্রতা কোনো নিষ্ক্রিয়তা নয়, বরং নির্দ্বিধায় জাতীয় স্বার্থের সুরক্ষা।",
                        "sa": "जयशंकर-सामरिकदृष्ट्या, बहुपक्षीयता न तु निष्पक्षता, अपितु राष्ट्रहितस्य निर्भीका साधना एव।",
                    },
                    "visual_prompt": "Global maritime trade routes connecting the Indian Ocean, Arabian Sea, and Malacca Strait with glowing sovereign naval escort vectors.",
                    "sfx": ["whoosh_impact"],
                    "music_mood": "STRATEGIC_MOMENTUM"
                },
                {
                    "spoken": {
                        "en": "Combined with Ajit Doval's doctrine of hard deterrence, defensive-offensive readiness guarantees that sovereign redlines remain inviolable.",
                        "hi": "अजीत डोभाल के कठोर सुरक्षा सिद्धांत के साथ, आक्रामक-रक्षात्मक तत्परता यह सुनिश्चित करती है कि देश की लक्ष्मण रेखाएं कभी न लांघी जाएं।",
                        "bn": "অজিত ডোভালের কঠোর নিরাপত্তা নীতি নিশ্চিত করে যে দেশের সার্বভৌম লাল রেখা কোনোভাবেই লঙ্ঘন করা যাবে না।",
                        "sa": "अजीत-डोभाल-नीत्या सह, आक्रामक-रक्षा-सन्नाहः संप्रभुसीमारेखां सदैव सुरक्षितां करोति।",
                    },
                    "visual_prompt": "Stealth frontline defense radars scanning perimeter airspace against mountain silhouettes, powerful cinematic mood.",
                    "sfx": ["radar_sweep", "deep_hit"],
                    "music_mood": "EPIC_SOVEREIGN_RESOLVE"
                },
                {
                    "spoken": {
                        "en": "True autonomy belongs to nations that see through the fog of narrative warfare. Examine the evidence, demand rigor, and follow for unapologetic sovereign analysis.",
                        "hi": "सच्ची स्वायत्तता उन्हीं की होती है जो नैरेटिव के भ्रमजाल को चीरकर सच देखते हैं। साक्ष्यों की जांच करें और सटीक संप्रभु विश्लेषण के लिए जुड़े रहें।",
                        "bn": "প্রকৃত স্বাধীনতা তাদেরই যারা প্রচারণার কুয়াশা ভেদ করে সত্য দেখতে পায়। তথ্যের বিশ্লেষণ করুন এবং গভীর সার্বভৌম বুদ্ধিমত্তার সাথে থাকুন।",
                        "sa": "सत्या स्वायत्तता तेषामेव भवति ये प्रचारजालं भित्त्वा सत्यं पश्यन्ति। सत्यं परीक्षत, संप्रभुबुद्ध्या सह तिष्ठत।",
                    },
                    "visual_prompt": "Dramatic sunset view of the Indian coastline with modern naval frigates patrolling under soaring sovereign tricolor, 8K cinema quality.",
                    "sfx": ["epic_brass_crescendo"],
                    "music_mood": "DRAMATIC_SOVEREIGN"
                },
            ]

        # Expand beats with progressive forensic depth if scene_count exceeds length of base_beats
        beats: List[Dict[str, Any]] = []
        for i in range(count):
            base_idx = i % len(base_beats)
            b = dict(base_beats[base_idx])
            cycle = (i // len(base_beats)) + 1
            if cycle == 2:
                # Cycle 2: Forensic Telemetry & Mechanistic Deep-Dive
                b["spoken"] = {
                    "en": f"Forensic telemetry examination: {b['spoken']['en']}",
                    "hi": f"विस्तृत साक्ष्य विश्लेषण: {b['spoken']['hi']}",
                    "bn": f"বিশদ তথ্য প্রমাণ বিশ্লেষণ: {b['spoken']['bn']}",
                    "sa": f"गहन-साक्ष्य-परीक्षणम्: {b['spoken']['sa']}",
                }
                b["visual_prompt"] = f"{b['visual_prompt']}, forensic data overlay, macro telemetry indicators, sequence phase 2."
            elif cycle >= 3:
                # Cycle 3+: Strategic Counter-Measure & Sovereign Synthesis
                b["spoken"] = {
                    "en": f"Strategic sovereign counter-measure: {b['spoken']['en']}",
                    "hi": f"संप्रभु रणनीतिक प्रतिकार: {b['spoken']['hi']}",
                    "bn": f"সার্বভৌম কৌশলগত প্রতিরক্ষা: {b['spoken']['bn']}",
                    "sa": f"संप्रभु-सामरिक-प्रतीकारः: {b['spoken']['sa']}",
                }
                b["visual_prompt"] = f"{b['visual_prompt']}, panoramic geopolitical command visualization, sequence phase 3."
            beats.append(b)
        return beats

