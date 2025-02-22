import os
import whisper
import ffmpeg
import srt
from datetime import timedelta

def extract_audio(video_path, audio_path="temp_audio.mp3"):
    """使用 ffmpeg 從影片中提取音訊"""
    ffmpeg.input(video_path).output(audio_path, acodec="mp3").run(overwrite_output=True)
    return audio_path

def transcribe_audio(audio_path):
    """使用 OpenAI Whisper 轉錄音訊"""
    model = whisper.load_model("base")  # 可選 tiny, base, small, medium, large
    result = model.transcribe(audio_path,language='ko')
    return result["segments"]  # 取得逐段文字與時間戳

def write_srt(transcription, srt_path="output.srt"):
    """將 Whisper 的轉錄結果轉換為 SRT 格式"""
    subtitles = []
    for i, segment in enumerate(transcription):
        start_time = timedelta(seconds=segment["start"])
        end_time = timedelta(seconds=segment["end"])
        text = segment["text"]
        subtitles.append(srt.Subtitle(index=i + 1, start=start_time, end=end_time, content=text))

    with open(srt_path, "w", encoding="utf-8") as f:
        f.write(srt.compose(subtitles))
    
    print(f"SRT 字幕已儲存至 {srt_path}")

def main(video_path):
    """主流程"""
    audio_path = extract_audio(video_path)
    transcription = transcribe_audio(audio_path)
    write_srt(transcription)

# 使用範例
video_file = "Snapinst.app_video_AQNwq_gXP2g3PWyw3u9U3JZ8tcEBdZkbEfxTTJK116CnehDKVvrFXHXlsb7BsPd0AuL0VPQVSMXogtJF_SOQR-DR9o3I4DQyt4hMVtg.mp4"  # 替換為你的影片檔案
main(video_file)
