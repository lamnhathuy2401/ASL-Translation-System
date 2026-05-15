import os
import imageio_ffmpeg

os.environ["PATH"] += os.pathsep + os.path.dirname(imageio_ffmpeg.get_ffmpeg_exe())

import whisper

class SpeechToText:
    def __init__(self, model_size="base"):
        # Model 'base' cân bằng tốt giữa tốc độ và độ chính xác
        self.model = whisper.load_model(model_size)

    def transcribe(self, audio_path):
        if not os.path.exists(audio_path):
            return "File không tồn tại"
        
        result = self.model.transcribe(audio_path)
        return result['text'].strip()

