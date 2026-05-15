🤟 Hệ thống Dịch thuật Ngôn ngữ Ký hiệu Mỹ (ASL) Thời gian thực

(Real-time Text/Speech to American Sign Language Translation System)

📖 Tổng quan dự án

Đây là hệ thống phần mềm nền Web ứng dụng Trí tuệ nhân tạo (AI) giúp phiên dịch trực tiếp từ Giọng nói hoặc Văn bản tiếng Anh sang Ngôn ngữ Ký hiệu Mỹ (ASL).

Hệ thống được thiết kế để giải quyết triệt để bài toán thiếu hụt từ vựng (Out-Of-Vocabulary - OOV) bằng kiến trúc "Phễu lọc NLP 4 tầng", kết hợp mô hình không gian Vector (Word Embeddings) để tự động suy luận từ đồng nghĩa và cơ chế đánh vần (Fingerspelling) làm chốt chặn an toàn dự phòng.

(Lưu ý: Dự án ban đầu có định hướng sử dụng công nghệ Generative 3D Avatar rendering, tuy nhiên để tối ưu hóa hiệu năng, tính chân thực và tài nguyên máy tính, phiên bản hiện tại đã chuyển sang kiến trúc Video Dictionary Mapping thông minh).

🚀 Các tính năng nổi bật

Đầu vào đa phương thức: Hỗ trợ nhập liệu bằng Text qua bàn phím hoặc Speech (Bóc băng âm thanh thời gian thực bằng mô hình học sâu OpenAI Whisper).

Chuẩn hóa cú pháp tự động: Loại bỏ các từ chức năng (to-be, mạo từ, giới từ) để ép cấu trúc câu tiếng Anh về chuẩn ngữ pháp rút gọn của ASL.

Tìm kiếm ngữ nghĩa (Semantic Search): Hệ thống không dùng cơ chế so khớp từ khóa cứng nhắc. Nếu người dùng nhập "joyful", AI sẽ tự động tính toán Cosine Similarity và gọi video "happy" thay thế.

Trực quan hóa liền mạch: Quản lý hàng đợi video (Video Queue) bằng React Hooks và Virtual DOM, chuyển cảnh mượt mà, không giật lag.

Tự động nạp dữ liệu (Auto Ingestion): Khối Backend có khả năng tự động nhận diện từ vựng mới khi dán file .mp4 vào thư mục lưu trữ tĩnh mà không cần sửa đổi mã nguồn.

📂 Cấu trúc thư mục hệ thống

Cấu trúc dự án được phân tách hoàn toàn (Decoupled) thành Backend và Frontend:

DOAN/
├── BE/ # Phân hệ Backend (Máy chủ AI - FastAPI)
│ ├── pipeline/ # Gói (Package) chứa các module AI cốt lõi
│ │ ├── asr.py # Module xử lý Nhận dạng giọng nói với Whisper
│ │ └── text2gloss.py # Module Phễu lọc NLP 4 tầng & Semantic Search
│ ├── data/ # Thư mục lưu trữ các file dữ liệu cấu hình
│ ├── main.py # Gateway & Khai báo RESTful API chính
│ └── temp\_{file.filename} # Tệp tạm lưu trữ audio upload từ Client
│
├── FE/ # Phân hệ Frontend (Giao diện người dùng - ReactJS/Vite)
│ ├── public/ # Không gian tĩnh
│ │ └── sign_videos/ # ⚠️ NƠI LƯU TRỮ TỆP VIDEO VẬT LÝ (.mp4)
│ ├── src/ # Mã nguồn React
│ │ ├── App.jsx # Component gốc điều hướng giao diện chính
│ │ ├── main.jsx # Entry point của React
│ │ └── index.css # Tệp CSS định dạng toàn cục
│ ├── index.html # Tệp HTML khởi tạo
│ ├── package.json # Cấu hình môi trường Node.js
│ └── README.md # Tài liệu hướng dẫn sử dụng này
│
└── logs/ # Thư mục lưu trữ nhật ký hệ thống (System logs)

⚙️ Hướng dẫn cài đặt và Khởi chạy

1. Cài đặt Backend (BE folder)

Yêu cầu máy tính cài đặt Python 3.10 trở lên. Mở Terminal, di chuyển vào thư mục BE và chạy các lệnh:

# Cài đặt các thư viện lõi của hệ thống

pip install fastapi uvicorn openai-whisper spacy python-multipart requests

# ⚠️ BẮT BUỘC: Tải mô hình không gian vector 300 chiều của thư viện spaCy

python -m spacy download en_core_web_md

# Khởi chạy Server Backend tại cổng 8000

uvicorn main:app --reload

Lưu ý: Trong lần đầu tiên gọi API nhận dạng giọng nói, hệ thống sẽ mất vài phút để tải tệp tạ (weights) của mô hình Whisper về thư mục cục bộ.

2. Cài đặt Frontend (FE folder)

Yêu cầu máy tính cài đặt Node.js (v18 trở lên). Mở một Terminal mới, di chuyển vào thư mục FE và chạy:

# Cài đặt các gói thư viện Node

npm install

# Khởi chạy giao diện Web

npm run dev

Trình duyệt sẽ tự động mở ứng dụng tại http://localhost:5173 (hoặc cổng tương ứng do Vite cấp). Đảm bảo Micro của bạn đang hoạt động để cấp quyền khi trình duyệt yêu cầu.

🛠️ Hướng dẫn quản trị dữ liệu (Tính năng Auto Ingestion)

Dự án được thiết kế theo chuẩn "Cắm là chạy" (Plug and Play). Quản trị viên không cần mở mã nguồn để khai báo biến tĩnh khi có từ vựng mới. Bạn chỉ cần thực hiện thao tác Copy-Paste tệp .mp4 vào thư mục FE/public/sign_videos/ tuân theo quy tắc sau:

> Lưu ý: Backend quét danh sách video khi `BE/pipeline/text2gloss.py` được import / khi server khởi động. Nếu bạn thêm file mới trong lúc backend đang chạy, cần khởi động lại backend để nhận diện video mới.

Từ vựng bảng chữ cái (Phục vụ Tầng 4 - Đánh vần):

Đặt tên đúng 1 ký tự: a.mp4, b.mp4, ..., z.mp4.

Từ đơn thông thường (Phục vụ Tầng 2 & 3):

Đặt tên từ tiếng Anh in thường: happy.mp4, car.mp4, study.mp4.

Cụm từ ưu tiên (Phục vụ Tầng 1):

Bắt buộc sử dụng dấu gạch dưới \_ để liên kết: thank_you.mp4, good_morning.mp4.

Thuật toán Python (text2gloss.py) sẽ tự động quét thư mục này, bóc tách dấu gạch dưới và phân loại chúng vào đúng cấu trúc WORD_MAP và PHRASES_MAP để sử dụng ngay lập tức.

🧠 Tóm tắt Thuật toán Lõi (Phễu lọc 4 tầng)

Khi người dùng nhập câu (VD: "Thank you, I am joyful DTU"), dữ liệu văn bản thô sẽ chảy qua 4 màng lọc độc quyền của hệ thống:

Tầng 1 (Phrase Matching): Nhận diện cụm "Thank you" và gom thành khối nguyên tử THANK_YOU (Bảo vệ cụm từ không bị cắt vụn).

Tầng 2 (POS Filter & Lemma): Phân tích từ loại, loại bỏ mạo từ, to-be, dấu câu. Đưa các từ còn lại về nguyên gốc.

Tầng 3 (Semantic Search): Hệ thống phát hiện không có video "joyful". AI lập tức kích hoạt Word2Vec, tính toán Cosine Similarity và ép kiểu sang từ đồng nghĩa có sẵn là HAPPY.

Tầng 4 (Fingerspelling Fallback): Hệ thống không biết "DTU" là gì. Từ này rớt xuống đáy phễu, thuật toán phân rã thành các ký tự D-T-U để gọi video múa bảng chữ cái (Chốt chặn đảm bảo hệ thống không bao giờ bị Crash).
