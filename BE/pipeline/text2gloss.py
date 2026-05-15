import spacy
import string
import os

try:
    nlp = spacy.load("en_core_web_md")
except OSError:
    os.system("python -m spacy download en_core_web_md")
    nlp = spacy.load("en_core_web_md")

# --- ĐƯỜNG DẪN TỚI THƯ MỤC CHỨA VIDEO ---
VIDEO_DIR = r"E:\CDIO3\doan\FE\public\sign_videos" 

# --- KHỞI TẠO RỖNG TOÀN BỘ ---
AVAILABLE_VIDEOS = []
WORD_MAP = {}
PHRASES_MAP = {} # Không gõ tay nữa!

if os.path.exists(VIDEO_DIR):
    for filename in os.listdir(VIDEO_DIR):
        if filename.endswith(".mp4"):
            base_name = filename.replace(".mp4", "").lower()
            
            # 1. Nhận diện cụm từ (Tầng 1)
            if "_" in base_name:
                phrase_key = base_name.replace("_", " ")
                PHRASES_MAP[phrase_key] = base_name.upper()
                
            # 2. BẢN VÁ LỖI (BUG FIX): Nhận diện video Bảng chữ cái
            elif len(base_name) == 1:
                # Nếu là chữ cái (a-z), CHỈ thêm vào WORD_MAP để phục vụ Tầng 4 (Đánh vần)
                # TUYỆT ĐỐI KHÔNG đưa vào AVAILABLE_VIDEOS để tránh Semantic Search (Tầng 3) nhận nhầm Slang
                WORD_MAP[base_name] = base_name.upper()
                
            # 3. Từ đơn bình thường (Tầng 2 & 3)
            else:
                AVAILABLE_VIDEOS.append(base_name)
                WORD_MAP[base_name] = base_name.upper()


# Bổ sung một vài từ lóng/viết tắt nếu muốn (Tùy chọn)
WORD_MAP.update({
    "hi": "HELLO",
    "hey": "HELLO"
})

IGNORE_POS = ['DET', 'AUX', 'PART', 'PUNCT', 'ADP']



# Hàm tính toán độ tương đồng (Semantic Search)
def get_semantic_match(target_lemma, threshold=0.60):
    target_token = nlp(target_lemma)[0]
    
    # Nếu từ này không có vector trong từ điển AI thì bỏ qua
    if not target_token.has_vector:
        return None
        
    best_score = 0
    best_match = None
    
    for video_word in AVAILABLE_VIDEOS:
        video_token = nlp(video_word)[0]
        # Tính điểm Cosine Similarity (từ 0.0 đến 1.0)
        score = target_token.similarity(video_token)
        
        if score > best_score:
            best_score = score
            best_match = video_word
            
    # Nếu điểm giống nhau vượt qua ngưỡng cho phép
    if best_score >= threshold:
        return best_match.upper()
    return None

def text_to_gloss(text):
    if not text:
        return ""
        
    text_clean = text.lower().translate(str.maketrans('', '', string.punctuation)).strip()
    
    # 1. BẮT CỤM TỪ
    for phrase, gloss_code in PHRASES_MAP.items():
        if phrase in text_clean:
            text_clean = text_clean.replace(phrase, gloss_code)
            
    doc = nlp(text_clean)
    gloss_tokens = []
    
    for token in doc:
        word = token.text
        
        # Bỏ qua cụm từ đã đóng gói
        if word.isupper() and "_" in word:
            gloss_tokens.append(word)
            continue
            
        if token.pos_ in IGNORE_POS:
            continue
            
        lemma = token.lemma_.lower()
        
        # 2. KHỚP TỪ ĐIỂN CHÍNH XÁC
        if lemma in WORD_MAP:
            gloss_tokens.append(WORD_MAP[lemma])
        # 3. TÌM KIẾM NGỮ NGHĨA (SEMANTIC SEARCH)
        else:
            semantic_result = get_semantic_match(lemma)
            if semantic_result:
                gloss_tokens.append(semantic_result)
            # 4. ĐÁNH VẦN (Fallback)
            else:
                for char in lemma.upper():
                    if char.isalpha():
                        gloss_tokens.append(char)
                    
    return " ".join(gloss_tokens)

# --- KHU VỰC TEST SỰ THÔNG MINH CỦA AI ---
if __name__ == "__main__":
    print("Test 1 - Từ đồng nghĩa:")
    # "joyful" sẽ tự suy luận ra "HAPPY" (vì điểm similarity > 0.75)
    print("Câu gốc: I am joyful")
    print("Gloss:  ", text_to_gloss("I am joyful")) 
    print("điểm tương đồng joyful:", nlp("joyful")[0].similarity(nlp("happy")[0]))
    
    print("\nTest 2 - Từ đồng nghĩa 2:")
    # "beverage" sẽ tự suy luận ra "DRINK"
    print("Câu gốc: I need a beverage")
    print("Gloss:  ", text_to_gloss("I need a beverage"))
    
    print("\nTest 3 - Từ mới tinh (Đánh vần):")
    # "DTU" không giống bất kỳ từ nào trong kho -> Đánh vần
    print("Câu gốc: I study at DTU")
    print("Gloss:  ", text_to_gloss("I study at DTU"))
    #"Hello, I meet a friend"
    print("câu gốc: Hello, I meet a friend")
    print("Gloss:  ", text_to_gloss("Hello, I meet a friend"))