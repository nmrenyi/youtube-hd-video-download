# YouTube Download and Combine
The video downloaded by `pytube` with default parameters is not in highest resolution (like 1080p), but in 720p. If we specify the `itag` for the 1080p video, however, the video comes without audio.

To solve this problem in a simple way, we can download the video and audio separately and combine them with `ffmpeg`. That's what repository is for.

Referring to [pytube](https://pytube.io/en/latest/index.html)
