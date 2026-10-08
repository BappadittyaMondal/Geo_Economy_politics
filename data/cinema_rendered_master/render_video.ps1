$OutputEncoding = [Console]::OutputEncoding = [Text.Encoding]::UTF8
Write-Host '== SOVEREIGN VIDEO STUDIO: RENDERING MNF-633960d159 ==' -ForegroundColor Cyan

if (-not (Test-Path 'video_base.mp4')) {
    Write-Host '[0/5] Compiling visual scene plates and video_base.mp4 via Geo Engine...' -ForegroundColor Cyan
    py -3.14 -m geo_engine.cli studio script_en.txt --cinema --render --output-dir .
}

Write-Host '[1/5] Synthesizing English neural audio...' -ForegroundColor Yellow
edge-tts --voice en-IN-PrabhatNeural --file script_en.txt --write-media audio_en.mp3

Write-Host '[2/5] Synthesizing Hindi neural audio...' -ForegroundColor Yellow
edge-tts --voice hi-IN-MadhurNeural --file script_hi.txt --write-media audio_hi.mp3

Write-Host '[3/5] Synthesizing Bengali neural audio...' -ForegroundColor Yellow
edge-tts --voice bn-IN-BashkarNeural --file script_bn.txt --write-media audio_bn.mp3

Write-Host '[4/5] Synthesizing Sanskrit neural audio...' -ForegroundColor Yellow
edge-tts --voice hi-IN-MadhurNeural --rate='-8%' --file script_sa.txt --write-media audio_sa.mp3

Write-Host '[5/5] Multiplexing multi-language audio with FFmpeg...' -ForegroundColor Yellow
ffmpeg -y -i video_base.mp4 -i audio_en.mp3 -i audio_hi.mp3 -i audio_bn.mp3 -i audio_sa.mp3 -map 0:v -map 1:a -map 2:a -map 3:a -map 4:a -c:v copy -c:a aac -metadata:s:a:0 language=en -metadata:s:a:0 title="EN" -metadata:s:a:1 language=hi -metadata:s:a:1 title="HI" -metadata:s:a:2 language=bn -metadata:s:a:2 title="BN" -metadata:s:a:3 language=sa -metadata:s:a:3 title="SA" output_multiaudio_MNF-633960d159.mp4

Write-Host '[SUCCESS] Broadcast package ready!' -ForegroundColor Green