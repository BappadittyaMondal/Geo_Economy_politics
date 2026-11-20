from youtube_transcript_api import YouTubeTranscriptApi

api = YouTubeTranscriptApi()
video_id = 'PdDa0pCmsrY'

try:
    transcript_list = api.list(video_id)
    print("Available transcripts:", [t.language_code for t in transcript_list])
    
    for t in transcript_list:
        data = t.fetch()
        text = ' '.join([x.text for x in data])
        print(f"Transcript language: {t.language_code}, length: {len(text)} characters")
        with open(f"scripts/transcript_{video_id}_{t.language_code}.txt", "w", encoding="utf-8") as f:
            f.write(text)
        print("Sample:", text[:400])
        break
except Exception as e:
    print("Transcript fetch error:", e)
