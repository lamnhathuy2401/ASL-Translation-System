import React, { useState, useEffect } from 'react';
import axios from 'axios';


// --- COMPONENT 1: HIỂN THỊ VIDEO MOCK ---
const MockAvatarPlayer = ({ gloss }) => {
  const [videoQueue, setVideoQueue] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  
  // THÊM BIẾN NÀY: Để đếm số lần phát lại, ép React render lại video
  const [replayCount, setReplayCount] = useState(0);

  useEffect(() => {
    if (gloss) {
      const words = gloss.toLowerCase().trim().split(/\s+/);
      setVideoQueue(words);
      setCurrentIndex(0);
      setReplayCount(0); // Reset bộ đếm khi có câu mới
    }
  }, [gloss]);

  const handleVideoEnd = () => {
    if (currentIndex < videoQueue.length - 1) {
      setCurrentIndex(prev => prev + 1);
    }
  };

  const handleVideoError = () => {
    console.warn(`Thiếu video cho từ: ${videoQueue[currentIndex]}. Tự động bỏ qua.`);
    handleVideoEnd();
  };

  // THÊM HÀM NÀY: Xử lý sự kiện nhấn nút Phát lại
  const handleReplay = () => {
    if (videoQueue.length > 0) {
      setCurrentIndex(0); // Quay về từ đầu tiên
      setReplayCount(prev => prev + 1); // Đổi key để ép video chạy lại
    }
  };

  return (
    <div className="video-player-wrapper">
      {videoQueue.length > 0 ? (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          <video
            // BÍ QUYẾT: Nối thêm replayCount vào key
            key={`${replayCount}-${currentIndex}-${videoQueue[currentIndex]}`} 
            src={`/sign_videos/${videoQueue[currentIndex]}.mp4`}
            autoPlay
            onEnded={handleVideoEnd}
            onError={handleVideoError}
            className="video-element"
          />
          
          <div className="video-controls" style={{ display: 'flex', alignItems: 'center', gap: '15px', marginTop: '16px' }}>
            <p className="video-status" style={{ margin: 0 }}>
              Đang ký hiệu: <strong style={{color: '#111827'}}>{videoQueue[currentIndex].toUpperCase()}</strong>
            </p>
            
            {/* THÊM NÚT PHÁT LẠI */}
            <button className="btn-replay" onClick={handleReplay} title="Phát lại toàn bộ">
              🔄 Replay
            </button>
          </div>
        </div>
      ) : (
        <div className="video-empty">
          <span className="skeleton-icon">🎬</span>
          <span>Chưa có dữ liệu video</span>
        </div>
      )}
    </div>
  );
};


// --- COMPONENT 2: GIAO DIỆN CHÍNH (APP) ---
function App() {
  const [data, setData] = useState({ original_text: "", gloss: "" });
  const [inputText, setInputText] = useState("");
  const [recording, setRecording] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState(null);

  // 1. Xử lý Ghi âm
  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);
      let chunks = [];

      recorder.ondataavailable = (e) => chunks.push(e.data);
      recorder.onstop = async () => {
        const blob = new Blob(chunks, { type: "audio/wav" });
        const formData = new FormData();
        formData.append("file", blob, "speech.wav");

        try {
          const response = await axios.post("http://localhost:8000/translate/speech", formData);
          setData(response.data);
        } catch (err) {
          alert("Lỗi kết nối Backend (Speech)");
        }
      };

      recorder.start();
      setMediaRecorder(recorder);
      setRecording(true);
    } catch (err) {
      alert("Hãy cấp quyền Microphone!");
    }
  };

  const stopRecording = () => {
    if (mediaRecorder) {
      mediaRecorder.stop();
      setRecording(false);
    }
  };

  // 2. Xử lý Nhập Văn bản
  const handleTextTranslate = async () => {
    if (!inputText.trim()) return;
    try {
      const response = await axios.post("http://localhost:8000/translate/text", { text: inputText });
      setData(response.data);
    } catch (err) {
      alert("Lỗi kết nối Backend (Text)");
    }
  };

  return (
  <div className="app-container">
    <h1>ASL TRANSLATION SYSTEM</h1>
    
    <div className="input-section">
      {/* Group Nhập liệu */}
      <div className="input-group">
        <input 
          type="text" 
          placeholder="🔍 Nhập câu tiếng Anh..."
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          onKeyDown={(e) => {
          if (e.key === 'Enter') {
            handleTextTranslate();
            }
          }}
        />
        <button className="btn btn-primary" onClick={handleTextTranslate}>
          Dịch
        </button>
      </div>

      <p className="divider">HOẶC</p>

      {/* Nút Micro (Secondary Style) */}
      <button 
        className={`btn btn-secondary ${recording ? 'recording' : ''}`}
        onClick={recording ? stopRecording : startRecording}
      >
        {recording ? "🛑 Đang xử lý âm thanh..." : "🎤 Nói bằng Micro"}
      </button>
    </div>

    {/* Kết quả 2 cột */}
    <div className="results-grid">
      <div className="result-card">
        <h3 className="section-title">📄 Kết quả xử lý</h3>
        
        <div className="result-row">
          <span className="label">Văn bản gốc:</span>
          <span className="value-text">{data.original_text || "Đang chờ dữ liệu..."}</span>
        </div>
        
        <div className="result-row">
          <span className="label">Mã Gloss ASL:</span>
          <span className="gloss-highlight">{data.gloss || "..."}</span>
        </div>
      </div>
      
      <MockAvatarPlayer gloss={data.gloss} />
    </div>
  </div>
);
}

export default App;