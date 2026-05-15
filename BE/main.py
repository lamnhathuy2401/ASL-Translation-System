import os
# Ép Python đưa thư mục FFmpeg lên đầu danh sách tìm kiếm lệnh
os.environ["PATH"] = r"E:\ffmpeg\bin" + os.pathsep + os.environ.get("PATH", "")

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
# ... các code còn lại của bạn giữ nguyên ...
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware # Quan trọng nhất
from pipeline.asr import SpeechToText
from pipeline.text2gloss import text_to_gloss
import shutil

app = FastAPI()


# --- CẤU HÌNH CORS ĐỂ KẾT NỐI VỚI REACT ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép tất cả các nguồn (hoặc ["http://localhost:5173"])
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép POST, GET, v.v.
    allow_headers=["*"],
)

asr_tool = SpeechToText()

@app.get("/")
async def root():
    return {"message": "ASL Backend is running!"}

@app.post("/translate/speech")
async def translate_speech(file: UploadFile = File(...)):
    # 1. Lưu file tạm
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # 2. Chuyển Speech -> Text
    raw_text = asr_tool.transcribe(temp_path)
    
    # 3. Chuyển Text -> Gloss
    gloss = text_to_gloss(raw_text)
    
    return {
        "original_text": raw_text,
        "gloss": gloss
    }

@app.post("/translate/text")
async def translate_text(request: dict):
    text = request.get("text", "")
    gloss = text_to_gloss(text)
    return {
        "original_text": text,
        "gloss": gloss
    }