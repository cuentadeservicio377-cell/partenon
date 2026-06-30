# Video v2 Assets Folder

Drop all files here with the exact names below. I will edit everything together with ffmpeg.

## Folder layout

```
video-v2/assets/
├── clips/              # AI-generated video clips from Gemini Omni
├── voice/              # Narration from ElevenLabs
├── music/              # Background music from Epidemic Sound
├── final/              # Exported final video (I will create this)
└── README.md           # This file
```

---

## Clips folder (`clips/`)

Generate in Gemini Omni using `video-v2/OMNI_PROMPTS.txt`.
Save each clip exactly as:

```
clip-01-hook.mp4
clip-02-problem.mp4
clip-03-home.mp4
clip-04-heroes.mp4
clip-05-tags.mp4
clip-06-flow.mp4
clip-07-workshop.mp4
clip-08-mission.mp4
clip-09-closing.mp4
```

Optional extras:

```
clip-00-countdown.mp4
clip-10-logo.mp4
```

## Voice folder (`voice/`)

Export from ElevenLabs using `video-v2/ELEVENLABS_SCRIPT.md`.
Save as:

```
voiceover.wav
```

Preferred format: WAV or MP3, mono or stereo, 44.1 kHz or 48 kHz.

## Music folder (`music/`)

Download from Epidemic Sound using `video-v2/EPIDEMIC_SOUND_PROMPT.md`.
Save as:

```
background-music.mp3
```

## Final output

I will create:

```
final/partenon-hackathon-video-v2.mp4
```

Once all files are in place, run the assembly script or tell me to proceed.
