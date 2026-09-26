"""
Acoustic Digital Signal Processing (DSP) & Prosodic Telemetry Engine.
Zero-dependency, pure-Python / standard library acoustic analyzer for extracting
fundamental frequency (F0), cycle-to-cycle pitch jitter, Voice Activity Detection (VAD),
and prosodic pause latency from raw audio waveforms.
"""

import io
import math
import struct
import wave
from typing import Any, Dict, List, Optional, Tuple, Union


class WAVAudioReader:
    """Parses standard RIFF/WAV audio streams or raw PCM buffers."""

    @staticmethod
    def read_wav(data_or_path: Union[bytes, str]) -> Tuple[List[float], int]:
        """
        Reads a WAV file from file path or byte buffer and returns normalized samples in [-1.0, 1.0]
        and the audio sample rate.
        """
        if isinstance(data_or_path, str):
            with wave.open(data_or_path, "rb") as wf:
                return WAVAudioReader._extract_samples_from_wave(wf)
        elif isinstance(data_or_path, (bytes, bytearray)):
            try:
                with wave.open(io.BytesIO(data_or_path), "rb") as wf:
                    return WAVAudioReader._extract_samples_from_wave(wf)
            except wave.Error:
                # Fallback: Treat as raw 16-bit PCM at 16000 Hz if WAV header is absent
                return WAVAudioReader.read_raw_pcm16(data_or_path, sample_rate=16000)
        else:
            raise ValueError(f"Unsupported audio input type: {type(data_or_path)}")

    @staticmethod
    def _extract_samples_from_wave(wf: wave.Wave_read) -> Tuple[List[float], int]:
        n_channels = wf.getnchannels()
        sampwidth = wf.getsampwidth()
        framerate = wf.getframerate()
        n_frames = wf.getnframes()

        raw_frames = wf.readframes(n_frames)
        samples: List[float] = []

        if sampwidth == 2:  # 16-bit signed PCM
            total_samples = n_frames * n_channels
            fmt = f"<{total_samples}h"
            integers = struct.unpack(fmt, raw_frames[: total_samples * 2])
            if n_channels == 1:
                samples = [float(s) / 32768.0 for s in integers]
            else:
                # Downmix stereo to mono by averaging channels
                samples = [
                    (float(integers[i]) + float(integers[i + 1])) / (2.0 * 32768.0)
                    for i in range(0, len(integers), n_channels)
                ]
        elif sampwidth == 1:  # 8-bit unsigned PCM
            total_samples = n_frames * n_channels
            integers = struct.unpack(f"{total_samples}B", raw_frames[:total_samples])
            if n_channels == 1:
                samples = [(float(s) - 128.0) / 128.0 for s in integers]
            else:
                samples = [
                    ((float(integers[i]) + float(integers[i + 1])) / 2.0 - 128.0) / 128.0
                    for i in range(0, len(integers), n_channels)
                ]
        elif sampwidth == 4:  # 32-bit float or signed integer
            total_samples = n_frames * n_channels
            fmt = f"<{total_samples}i"
            integers = struct.unpack(fmt, raw_frames[: total_samples * 4])
            if n_channels == 1:
                samples = [float(s) / 2147483648.0 for s in integers]
            else:
                samples = [
                    (float(integers[i]) + float(integers[i + 1])) / (2.0 * 2147483648.0)
                    for i in range(0, len(integers), n_channels)
                ]
        else:
            raise ValueError(f"Unsupported sample width: {sampwidth} bytes")

        return samples, framerate

    @staticmethod
    def read_raw_pcm16(raw_bytes: bytes, sample_rate: int = 16000) -> Tuple[List[float], int]:
        """Parses raw headerless 16-bit signed integer PCM mono audio."""
        n_samples = len(raw_bytes) // 2
        fmt = f"<{n_samples}h"
        integers = struct.unpack(fmt, raw_bytes[: n_samples * 2])
        samples = [float(s) / 32768.0 for s in integers]
        return samples, sample_rate

    @staticmethod
    def synthesize_test_tone(
        frequency_hz: float,
        duration_s: float,
        sample_rate: int = 16000,
        amplitude: float = 0.5,
        add_jitter_ratio: float = 0.0,
        pause_duration_s: float = 0.0
    ) -> bytes:
        """Generates an in-memory synthetic 16-bit PCM WAV file for deterministic testing."""
        n_samples = int(duration_s * sample_rate)
        samples = []
        phase = 0.0
        two_pi = 2.0 * math.pi

        for i in range(n_samples):
            # Optionally modulate frequency with subtle cycle jitter
            if add_jitter_ratio > 0.0 and (i % int(sample_rate / frequency_hz)) == 0:
                freq_mod = frequency_hz * (1.0 + (math.sin(i * 0.05) * add_jitter_ratio))
            else:
                freq_mod = frequency_hz

            phase += two_pi * (freq_mod / sample_rate)
            val = amplitude * math.sin(phase)
            samples.append(val)

        # Append optional silence pause
        if pause_duration_s > 0.0:
            pause_samples = int(pause_duration_s * sample_rate)
            samples.extend([0.0] * pause_samples)
            # Add secondary tone burst after pause
            samples.extend([amplitude * math.sin(phase + two_pi * (frequency_hz / sample_rate) * j) for j in range(int(0.5 * sample_rate))])

        # Pack into WAV
        buf = io.BytesIO()
        with wave.open(buf, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            raw_pcm = b"".join(struct.pack("<h", int(max(-1.0, min(1.0, s)) * 32767.0)) for s in samples)
            wf.writeframes(raw_pcm)

        return buf.getvalue()


class AcousticDSPWorker:
    """
    On-premise Digital Signal Processing engine for extracting fundamental frequency (F0),
    cycle-to-cycle pitch perturbation (jitter), voice activity, and prosodic pause metrics.
    """

    @staticmethod
    def compute_short_term_energy(frame: List[float]) -> float:
        """Calculates short-term energy of an audio frame."""
        return sum(s * s for s in frame) / max(1, len(frame))

    @staticmethod
    def estimate_pitch_autocorrelation(
        frame: List[float],
        sample_rate: int,
        min_f0: float = 75.0,
        max_f0: float = 500.0
    ) -> Tuple[Optional[float], float]:
        """
        Estimates the fundamental frequency (F0) of a frame via Normalized Autocorrelation (NACF).
        Returns: (F0_hz, peak_confidence)
        """
        n = len(frame)
        if n < 4:
            return None, 0.0

        min_lag = int(sample_rate / max_f0)
        max_lag = int(sample_rate / min_f0)

        if max_lag >= n:
            max_lag = n - 1

        energy_0 = sum(s * s for s in frame)
        if energy_0 < 1e-6:
            return None, 0.0  # Silence / unvoiced

        best_lag = -1
        max_corr = -1.0

        for lag in range(min_lag, max_lag + 1):
            corr = 0.0
            energy_lag = 0.0
            for i in range(n - lag):
                corr += frame[i] * frame[i + lag]
                energy_lag += frame[i + lag] * frame[i + lag]

            if energy_lag > 1e-6:
                norm_corr = corr / math.sqrt(energy_0 * energy_lag)
                if norm_corr > max_corr:
                    max_corr = norm_corr
                    best_lag = lag

        # Threshold for voicing: Normalized autocorrelation peak >= 0.35
        if max_corr >= 0.35 and best_lag > 0:
            f0 = float(sample_rate) / float(best_lag)
            return round(f0, 2), round(max_corr, 3)

        return None, round(max(0.0, max_corr), 3)

    @classmethod
    def compute_pitch_and_jitter(
        cls,
        samples: List[float],
        sample_rate: int,
        frame_duration_ms: float = 30.0,
        hop_duration_ms: float = 15.0,
        min_f0: float = 75.0,
        max_f0: float = 500.0
    ) -> Dict[str, float]:
        """
        Extracts pitch contour across frames, calculating mean F0, pitch variance,
        and cycle-to-cycle local pitch jitter.
        """
        frame_len = int((frame_duration_ms / 1000.0) * sample_rate)
        hop_len = int((hop_duration_ms / 1000.0) * sample_rate)

        periods: List[float] = []
        f0_values: List[float] = []

        total_frames = max(1, (len(samples) - frame_len) // hop_len)
        for i in range(total_frames):
            start = i * hop_len
            frame = samples[start : start + frame_len]
            f0, conf = cls.estimate_pitch_autocorrelation(frame, sample_rate, min_f0, max_f0)
            if f0 is not None and conf >= 0.40:
                f0_values.append(f0)
                periods.append(1.0 / f0)

        if not f0_values:
            return {
                "mean_f0_hz": 0.0,
                "pitch_variance_hz": 0.0,
                "pitch_jitter_local": 0.0,
                "voiced_frames_count": 0
            }

        mean_f0 = sum(f0_values) / len(f0_values)
        variance = sum((f - mean_f0) ** 2 for f in f0_values) / len(f0_values)
        std_f0 = math.sqrt(variance)

        # Local pitch jitter: mean relative period-to-period difference
        if len(periods) > 1:
            period_diffs = sum(abs(periods[k] - periods[k + 1]) for k in range(len(periods) - 1))
            mean_period = sum(periods) / len(periods)
            local_jitter = (period_diffs / (len(periods) - 1)) / max(1e-6, mean_period)
        else:
            local_jitter = 0.0

        return {
            "mean_f0_hz": round(mean_f0, 2),
            "pitch_variance_hz": round(std_f0, 2),
            "pitch_jitter_local": round(min(1.0, local_jitter), 4),
            "voiced_frames_count": len(f0_values)
        }

    @classmethod
    def compute_vad_and_pauses(
        cls,
        samples: List[float],
        sample_rate: int,
        frame_duration_ms: float = 30.0,
        energy_threshold_factor: float = 0.20
    ) -> Dict[str, Any]:
        """
        Performs Voice Activity Detection (VAD) via Short-Term Energy,
        identifying continuous pause intervals and calculating mean pause duration.
        """
        frame_len = int((frame_duration_ms / 1000.0) * sample_rate)
        if frame_len == 0 or len(samples) < frame_len:
            return {
                "mean_pause_duration_seconds": 0.0,
                "max_pause_duration_seconds": 0.0,
                "total_speech_duration_seconds": 0.0,
                "total_pause_duration_seconds": 0.0,
                "pause_count": 0
            }

        energies = []
        for i in range(0, len(samples) - frame_len + 1, frame_len):
            energies.append(cls.compute_short_term_energy(samples[i : i + frame_len]))

        if not energies:
            return {"mean_pause_duration_seconds": 0.0, "pause_count": 0}

        avg_energy = sum(energies) / len(energies)
        silence_threshold = avg_energy * energy_threshold_factor

        # Detect contiguous silent frame intervals
        pause_durations: List[float] = []
        current_silent_frames = 0
        min_pause_frames = int(0.20 / (frame_duration_ms / 1000.0))  # Pauses >= 200ms

        for e in energies:
            if e <= silence_threshold:
                current_silent_frames += 1
            else:
                if current_silent_frames >= min_pause_frames:
                    pause_durations.append(current_silent_frames * (frame_duration_ms / 1000.0))
                current_silent_frames = 0

        if current_silent_frames >= min_pause_frames:
            pause_durations.append(current_silent_frames * (frame_duration_ms / 1000.0))

        mean_pause = sum(pause_durations) / len(pause_durations) if pause_durations else 0.0
        max_pause = max(pause_durations) if pause_durations else 0.0

        return {
            "mean_pause_duration_seconds": round(mean_pause, 3),
            "max_pause_duration_seconds": round(max_pause, 3),
            "pause_count": len(pause_durations),
            "pause_durations": pause_durations
        }

    @classmethod
    def analyze_audio(
        cls,
        data_or_path: Union[bytes, str],
        sample_rate: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Full-spectrum Acoustic DSP pipeline: parses audio, extracts pitch contour,
        computes local jitter, measures pause latency, and derives prosodic stress indicators.
        """
        samples, fs = WAVAudioReader.read_wav(data_or_path)
        if sample_rate and sample_rate != fs:
            # Simple decimation/sampling fallback if requested
            pass

        total_duration = len(samples) / float(fs) if fs > 0 else 0.0

        pitch_metrics = cls.compute_pitch_and_jitter(samples, fs)
        vad_metrics = cls.compute_vad_and_pauses(samples, fs)

        pause_sec = vad_metrics["mean_pause_duration_seconds"]
        pitch_jitter = pitch_metrics["pitch_jitter_local"]

        # Composite prosodic pause index (calibrated to MicroSignalExtractor)
        pause_idx = min(1.0, round((pause_sec / 2.0) * 0.7 + (pitch_jitter * 10.0) * 0.3, 3))
        high_cognitive_load = bool(pause_sec >= 1.2 or vad_metrics["max_pause_duration_seconds"] >= 1.5)

        return {
            "audio_duration_seconds": round(total_duration, 2),
            "sample_rate_hz": fs,
            "mean_f0_hz": pitch_metrics["mean_f0_hz"],
            "pitch_variance_hz": pitch_metrics["pitch_variance_hz"],
            "pitch_jitter_local": pitch_metrics["pitch_jitter_local"],
            "mean_pause_duration_seconds": pause_sec,
            "max_pause_duration_seconds": vad_metrics["max_pause_duration_seconds"],
            "pause_count": vad_metrics["pause_count"],
            "prosodic_pause_index": pause_idx,
            "high_cognitive_load": high_cognitive_load,
            "is_vocal_tremor_detected": bool(pitch_jitter >= 0.04)
        }
