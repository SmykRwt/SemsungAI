import moviepy.config as mpy_config
mpy_config.change_settings({"IMAGEMAGICK_BINARY": "C:\\Program Files\\ImageMagick-7.1.2-Q16-HDRI\\magick.exe"})  # Use your actual path

from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip
import os

def combine_audio_with_video(audio_path, video_path, output_path="static/final_output/final_video.mp4", subtitle_text=None):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)

    # Trim video to audio duration (to avoid access errors)
    duration = min(video.duration, audio.duration)
    video = video.subclip(0, duration)
    audio = audio.subclip(0, duration)

    video = video.set_audio(audio)

    if subtitle_text:
        subtitle = TextClip(
            subtitle_text,
            fontsize=32,
            font='Arial-Bold',
            color='white',
            bg_color='black',
            method='caption',
            size=(video.w, None)
        )
        subtitle = subtitle.set_duration(duration).set_position(("center", "bottom"))
        video = CompositeVideoClip([video, subtitle])

    video.write_videofile(output_path, codec="libx264", audio_codec="aac")
    return output_path
