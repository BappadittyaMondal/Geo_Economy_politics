@echo off
chcp 65001 > nul
echo ===================================================================
echo SOVEREIGN VIDEO STUDIO: RENDERING MNF-633960d159
echo ===================================================================

echo [1/5] Synthesizing English neural voiceover via Edge-TTS...
edge-tts --voice en-IN-PrabhatNeural --file script_en.txt --write-media audio_en.mp3

echo [2/5] Synthesizing Hindi neural voiceover via Edge-TTS...
edge-tts --voice hi-IN-MadhurNeural --file script_hi.txt --write-media audio_hi.mp3

echo [3/5] Synthesizing Bengali neural voiceover via Edge-TTS...
edge-tts --voice bn-IN-BashkarNeural --file script_bn.txt --write-media audio_bn.mp3

echo [4/5] Synthesizing Sanskrit neural voiceover via Edge-TTS...
edge-tts --voice hi-IN-MadhurNeural --rate=-8% --file script_sa.txt --write-media audio_sa.mp3

echo [5/5] Executing multi-track audio multiplexing with FFmpeg...
ffmpeg -y -i video_base.mp4 -i audio_en.mp3 -i audio_hi.mp3 -i audio_bn.mp3 -i audio_sa.mp3 -map 0:v -map 1:a -map 2:a -map 3:a -map 4:a -c:v copy -c:a aac -metadata:s:a:0 language=en -metadata:s:a:0 title="EN" -metadata:s:a:1 language=hi -metadata:s:a:1 title="HI" -metadata:s:a:2 language=bn -metadata:s:a:2 title="BN" -metadata:s:a:3 language=sa -metadata:s:a:3 title="SA" output_multiaudio_MNF-633960d159.mp4

echo [SUCCESS] Video render completed: output_multiaudio_MNF-633960d159.mp4