# -*- coding: utf-8 -*-
import streamlit as st
import requests
import json
import os
from datetime import datetime

# ==============================================================================
# ĐỀ LUYỆN HSK4 - STREAMLIT APP OFFICIAL
# ==============================================================================

st.set_page_config(
    page_title="ĐỀ LUYỆN HSK4",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS CAO CẤP: PHỐI MÀU PASTEL ĐA SẮC TƯƠI SÁNG, FORCE LIGHT MODE, CHỮ BÓNG ĐẬM ---
st.markdown("""
<style>
    /* Nền trang nhã pastel */
    .stApp {
        background-color: #F8FAFC !important;
    }
    
    /* Ép phông chữ màu đen / xám đậm sắc nét (Bold 700) */
    html, body, p, span, label, li, h1, h2, h3, h4, h5, h6, 
    .stMarkdown, .stWidgetLabel, .stMarkdownContainer p,
    div[data-testid="stMarkdownContainer"] p,
    div[role="radiogroup"] label, div[role="radiogroup"] p,
    div[data-testid="stNotification"] p, div[data-testid="stNotification"] div {
        color: #0F172A !important;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif !important;
        font-weight: 700 !important;
    }
    
    /* Tiêu đề chính */
    h1 {
        color: #1E3A8A !important;
        font-size: 2.3rem !important;
        font-weight: 800 !important;
        text-align: center !important;
        margin-bottom: 4px !important;
    }
    
    .subtitle {
        text-align: center !important;
        font-size: 18px !important;
        color: #2563EB !important;
        font-weight: 700 !important;
        margin-bottom: 22px !important;
    }

    /* Khung hiển thị câu hỏi pastel bo tròn viền đa sắc */
    .question-card {
        background-color: #FFFFFF !important;
        padding: 18px 22px !important;
        border-radius: 16px !important;
        border-left: 6px solid #3B82F6 !important;
        border-top: 1.5px solid #E2E8F0 !important;
        border-right: 1.5px solid #E2E8F0 !important;
        border-bottom: 1.5px solid #E2E8F0 !important;
        margin-bottom: 18px !important;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.05) !important;
    }
    
    .card-blue { border-left-color: #3B82F6 !important; }
    .card-pink { border-left-color: #EC4899 !important; }
    .card-purple { border-left-color: #8B5CF6 !important; }
    .card-orange { border-left-color: #F97316 !important; }
    .card-yellow { border-left-color: #EAB308 !important; }
    .card-brown { border-left-color: #8D6E63 !important; }

    /* Force Light Mode cho Inputs */
    div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
        border: 1.5px solid #CBD5E1 !important;
        border-radius: 10px !important;
    }
    div[data-testid="stTextInput"] input, div[data-testid="stTextArea"] textarea {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border: 1.5px solid #CBD5E1 !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        padding: 10px 14px !important;
    }

    /* Tabs chính */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px !important;
        background-color: #F1F5F9 !important;
        padding: 8px !important;
        border-radius: 16px !important;
    }
    .stTabs [data-baseweb="tab"] {
        height: 45px !important;
        white-space: pre !important;
        background-color: #FFFFFF !important;
        border-radius: 12px !important;
        color: #475569 !important;
        font-weight: 700 !important;
        border: 1px solid #E2E8F0 !important;
        padding: 0px 16px !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        border-color: #1D4ED8 !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3) !important;
    }

    /* Nút nộp bài cam pastel nổi bật */
    div.stButton > button {
        background: linear-gradient(135deg, #F97316 0%, #EA580C 100%) !important;
        color: #FFFFFF !important;
        font-size: 17px !important;
        font-weight: 800 !important;
        padding: 12px 28px !important;
        border-radius: 14px !important;
        border: none !important;
        box-shadow: 0 4px 14px rgba(234, 88, 12, 0.3) !important;
        width: 100% !important;
    }
    div.stButton > button:hover {
        background: linear-gradient(135deg, #EA580C 0%, #C2410C 100%) !important;
        transform: translateY(-1px) !important;
    }

    /* FOOTER CHỈ ĐỂ 黄宝玉老师 THÔI */
    .footer {
        text-align: center;
        margin-top: 50px;
        padding: 20px;
        font-size: 18px;
        color: #475569;
        font-weight: 800;
        border-top: 1px solid #E2E8F0;
    }
</style>
""", unsafe_allow_html=True)

# --- WEBHOOK GỬI VỀ TAB HSK4 VÀO GOOGLE SHEETS CHUNG ---
GSHEET_WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbxfZ7f292zc7Rcq8OdalCQIKl9WDY1fAc21pBMAmXFKr1qnQ3F8FeH-vJqIebuWKQ1U8A/exec"

def send_score_to_gsheet(student_name, exam_code, section_name, score_raw, score_100):
    payload = {
        "student_name": student_name,
        "lesson": exam_code,
        "lesson_title": exam_code,
        "section": section_name,
        "score": f"{score_raw} ({score_100:.1f}/100 điểm)",
        "sheet_name": "HSK4",
        "tab_name": "HSK4",
        "sheet": "HSK4",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    try:
        res = requests.post(GSHEET_WEBHOOK_URL, json=payload, timeout=8)
        return True, "Đã gửi kết quả về Google Sheet (Tab HSK4) thành công!"
    except Exception as e:
        return False, f"Lỗi kết nối Webhook: {str(e)}"

# --- TRÌNH PHÁT BÀI NGHE THEO MÃ ĐỀ ---
def render_audio_player(exam_code):
    mp3_filename = f"{exam_code}.mp3"
    st.markdown(f"#### 🎧 **PHÁT ÂM THANH BÀI NGHE ({mp3_filename})**")
    if os.path.exists(mp3_filename):
        st.audio(mp3_filename, format="audio/mpeg")
    elif os.path.exists(os.path.join("audio", mp3_filename)):
        st.audio(os.path.join("audio", mp3_filename), format="audio/mpeg")
    else:
        st.info(f"💡 Tải file **{mp3_filename}** lên GitHub cùng dự án Streamlit để phát bài nghe nhé!")

# --- HÀM RENDER 5 TRANH CHO PHẦN VIẾT PHẦN 2 (_1, _2, _3, _4, _5) ---
def render_writing_image(exam_code, img_idx, word_hint):
    img_jpg = f"{exam_code}_{img_idx}.jpg"
    img_png = f"{exam_code}_{img_idx}.png"
    
    img_path = None
    if os.path.exists(img_jpg):
        img_path = img_jpg
    elif os.path.exists(img_png):
        img_path = img_png
    elif os.path.exists(os.path.join("images", img_jpg)):
        img_path = os.path.join("images", img_jpg)
    elif os.path.exists(os.path.join("images", img_png)):
        img_path = os.path.join("images", img_png)
        
    if img_path:
        st.image(img_path, width=280)
    else:
        st.markdown(f"📷 *[Hình ảnh {exam_code}_{img_idx}.jpg]*")
    st.markdown(f"Từ gợi ý: **{word_hint}**")


# ==============================================================================
# TIÊU ĐỀ BÀI LÀM
# ==============================================================================
st.markdown("<h1>ĐỀ LUYỆN HSK4</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Chúc các bạn ôn tập vui và hiệu quả</div>", unsafe_allow_html=True)

# Ô nhập tên học sinh
if "student_name" not in st.session_state:
    st.session_state.student_name = ""

student_name = st.text_input(
    "👤 Họ và tên học sinh:",
    value=st.session_state.student_name,
    placeholder="Ví dụ: Nguyễn Văn A",
    key="name_input_global"
)
st.session_state.student_name = student_name

st.markdown("<br>", unsafe_allow_html=True)

# DANH SÁCH MÃ ĐỀ
EXAM_CODES = ["H41110", "H41111", "H41218", "H41219", "H41220", "H41221", "H41327", "H41328", "H41329", "H41330", "H41331", "H41332", "H41333", "H41335"]

# TRỌN BỘ CÂU HỎI MÃ ĐỀ H41110 FULL 100 CÂU



# ==============================================================================
# QUY TRÌNH RENDER CHO MỖI TAB MÃ ĐỀ THI
# ==============================================================================
exam_tabs = st.tabs(EXAM_CODES)

for idx, exam_code in enumerate(EXAM_CODES):
    with exam_tabs[idx]:
        st.markdown(f"## 📋 ĐỀ THI MÃ: **{exam_code}**")
        
        # 3 Sub-tabs
        sub_t_listen, sub_tab_read, sub_tab_write = st.tabs(["🎧 听力 (Phần nghe)", "📖 阅读 (Phần đọc)", "✍️ 书写 (Phần viết)"])
        
        # ----------------------------------------------------------------------
        # 1. PHẦN NGHE (CÂU 1 - 45)
        # ----------------------------------------------------------------------
        with sub_t_listen:
            render_audio_player(exam_code)
            st.markdown("---")
            
            # Tải dữ liệu 100 câu cho H41110 hoặc các mã đề
            q_l_p1 = H41110_DATA["listen_p1"]
            q_l_p2 = H41110_DATA["listen_p2"]
            q_l_p3 = H41110_DATA["listen_p3"]

            u_l_ans = {}
            
            st.markdown("#### **第一部分 (Phần 1 - 判断对错: Câu 1-10)**")
            for q in q_l_p1:
                st.markdown(f"<div class='question-card card-pink'><strong>Câu {q['num']}:</strong><br>{q['text']}", unsafe_allow_html=True)
                ans = st.radio(f"l1_{exam_code}_{q['num']}", ["√", "×"], horizontal=True, key=f"w_l1_{exam_code}_{q['num']}", label_visibility="collapsed")
                u_l_ans[q['num']] = ans
                st.markdown("</div>", unsafe_allow_html=True)
                
            st.markdown("#### **第二部分 (Phần 2 - 单项选择: Câu 11-25)**")
            for q in q_l_p2:
                st.markdown(f"<div class='question-card card-purple'><strong>Câu {q['num']}:</strong>", unsafe_allow_html=True)
                ans = st.radio(f"l2_{exam_code}_{q['num']}", q['options'], key=f"w_l2_{exam_code}_{q['num']}", label_visibility="collapsed")
                u_l_ans[q['num']] = ans[0] if ans else ""
                st.markdown("</div>", unsafe_allow_html=True)
                
            st.markdown("#### **第三部分 (Phần 3 - 单项选择: Câu 26-45)**")
            for q in q_l_p3:
                st.markdown(f"<div class='question-card card-orange'><strong>Câu {q['num']}:</strong>", unsafe_allow_html=True)
                ans = st.radio(f"l3_{exam_code}_{q['num']}", q['options'], key=f"w_l3_{exam_code}_{q['num']}", label_visibility="collapsed")
                u_l_ans[q['num']] = ans[0] if ans else ""
                st.markdown("</div>", unsafe_allow_html=True)

            if st.button("🚀 NỘP BÀI PHẦN NGHE", key=f"btn_sub_l_{exam_code}"):
                if not student_name.strip():
                    st.warning("⚠️ Vui lòng nhập Họ và tên ở đầu trang trước khi nộp bài!")
                else:
                    tot = len(q_l_p1) + len(q_l_p2) + len(q_l_p3)
                    c_cnt = 0
                    for q in q_l_p1 + q_l_p2 + q_l_p3:
                        if u_l_ans.get(q['num']) == q['correct']:
                            c_cnt += 1
                    sc_100 = (c_cnt / tot) * 100
                    
                    st.success(f"🎉 Kết quả Phần Nghe Mã {exam_code}: Số câu đúng {c_cnt}/{tot} câu • Điểm số {sc_100:.1f} / 100 điểm")
                    send_score_to_gsheet(student_name, exam_code, "PHẦN NGHE", f"{c_cnt}/{tot}", sc_100)
                    
                    st.markdown("---")
                    st.markdown("### 🔍 CHI TIẾT CÂU SAI & SCRIPT NGHE:")
                    for q in q_l_p1 + q_l_p2 + q_l_p3:
                        if u_l_ans.get(q['num']) != q['correct']:
                            st.markdown(f"❌ **Câu {q['num']}**: Bạn chọn `{u_l_ans.get(q['num'])}` | Đáp án đúng: **{q['correct']}**")
                            with st.expander(f"📖 查看听力文本 (Xem Script Câu {q['num']})"):
                                st.write(q['script'])

        # ----------------------------------------------------------------------
        # 2. PHẦN ĐỌC (CÂU 46 - 85)
        # ----------------------------------------------------------------------
        with sub_tab_read:
            st.markdown("### 二、阅读 (Phần đọc - 40 câu)")
            
            q_r_p1 = H41110_DATA["read_p1"]
            q_r_p2 = H41110_DATA["read_p2"]
            q_r_p3 = H41110_DATA["read_p3"]

            u_r_ans = {}
            st.markdown("#### **第一部分 (Phần 1 - 选词填空: Câu 46-55)**")
            for q in q_r_p1:
                st.markdown(f"<div class='question-card card-yellow'><strong>Câu {q['num']}:</strong><br>{q['text']}", unsafe_allow_html=True)
                ans = st.radio(f"r1_{exam_code}_{q['num']}", q['options'], key=f"w_r1_{exam_code}_{q['num']}", label_visibility="collapsed")
                u_r_ans[q['num']] = ans[0] if ans else ""
                st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("#### **第二部分 (Phần 2 - 排列顺序: Câu 56-65)**")
            for q in q_r_p2:
                st.markdown(f"<div class='question-card card-brown'><strong>Câu {q['num']}:</strong><br>{q['text']}", unsafe_allow_html=True)
                ans = st.text_input(f"Nhập thứ tự (VD: BAC) cho câu {q['num']}:", key=f"w_r2_{exam_code}_{q['num']}").strip().upper()
                u_r_ans[q['num']] = ans
                st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("#### **第三部分 (Phần 3 - 阅读理解: Câu 66-85)**")
            for q in q_r_p3:
                st.markdown(f"<div class='question-card card-purple'><strong>Câu {q['num']}:</strong><br>{q['text']}", unsafe_allow_html=True)
                ans = st.radio(f"r3_{exam_code}_{q['num']}", q['options'], key=f"w_r3_{exam_code}_{q['num']}", label_visibility="collapsed")
                u_r_ans[q['num']] = ans[0] if ans else ""
                st.markdown("</div>", unsafe_allow_html=True)

            if st.button("🚀 NỘP BÀI PHẦN ĐỌC", key=f"btn_sub_r_{exam_code}"):
                if not student_name.strip():
                    st.warning("⚠️ Vui lòng nhập Họ và tên ở đầu trang trước khi nộp bài!")
                else:
                    tot = len(q_r_p1) + len(q_r_p2) + len(q_r_p3)
                    c_cnt = 0
                    for q in q_r_p1 + q_r_p2 + q_r_p3:
                        if u_r_ans.get(q['num']) == q['correct']:
                            c_cnt += 1
                    sc_100 = (c_cnt / tot) * 100
                    
                    st.success(f"🎉 Kết quả Phần Đọc Mã {exam_code}: Số câu đúng {c_cnt}/{tot} câu • Điểm số {sc_100:.1f} / 100 điểm")
                    send_score_to_gsheet(student_name, exam_code, "PHẦN ĐỌC", f"{c_cnt}/{tot}", sc_100)
                    
                    st.markdown("---")
                    st.markdown("### 🔍 CHI TIẾT CÂU SAI PHẦN ĐỌC:")
                    for q in q_r_p1 + q_r_p2 + q_r_p3:
                        if u_r_ans.get(q['num']) != q['correct']:
                            st.markdown(f"❌ **Câu {q['num']}**: Bạn chọn `{u_r_ans.get(q['num'])}` | Đáp án đúng: **{q['correct']}**")

        # ----------------------------------------------------------------------
        # 3. PHẦN VIẾT (CÂU 86 - 100)
        # ----------------------------------------------------------------------
        with sub_tab_write:
            st.markdown("### 三、书写 (Phần viết - 15 câu)")
            
            q_w_p1 = H41110_DATA["write_p1"]
            q_w_p2 = H41110_DATA["write_p2"]

            u_w_ans = {}
            st.markdown("#### **第一部分 (Phần 1 - Sắp xếp câu: Câu 86-95)**")
            for q in q_w_p1:
                st.markdown(f"<div class='question-card card-pink'><strong>Câu {q['num']}:</strong> {q['words']}", unsafe_allow_html=True)
                ans = st.text_input("Nhập câu hoàn chỉnh của bạn:", key=f"w_w1_{exam_code}_{q['num']}").strip()
                u_w_ans[q['num']] = ans
                st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("#### **第二部分 (Phần 2 - Nhìn tranh đặt câu: Câu 96-100)**")
            for idx_p2, q in enumerate(q_w_p2, start=96):
                st.markdown(f"<div class='question-card card-orange'><strong>Câu {idx_p2}:</strong>", unsafe_allow_html=True)
                render_writing_image(exam_code, idx_p2 - 95, q["hint"])
                ans = st.text_area(f"Nhập câu tự luận cho câu {idx_p2}:", key=f"w_w2_{exam_code}_{idx_p2}")
                u_w_ans[idx_p2] = ans
                st.markdown("</div>", unsafe_allow_html=True)

            st.info("📌 Note: Các câu từ 96-100 (đặt câu theo tranh) cô Ngọc sẽ chấm cụ thể sau.")

            if st.button("🚀 NỘP BÀI PHẦN VIẾT", key=f"btn_sub_w_{exam_code}"):
                if not student_name.strip():
                    st.warning("⚠️ Vui lòng nhập Họ và tên ở đầu trang trước khi nộp bài!")
                else:
                    c_cnt_p1 = sum(1 for q in q_w_p1 if u_w_ans.get(q['num']) in q['correct'])
                    c_cnt_total = c_cnt_p1 + len(q_w_p2) # Mặc định full điểm phần 2
                    tot = len(q_w_p1) + len(q_w_p2)
                    sc_100 = (c_cnt_total / tot) * 100
                    
                    st.success(f"🎉 Kết quả Phần Viết tương đối Mã {exam_code}: Số câu đúng {c_cnt_total}/{tot} câu • Điểm số {sc_100:.1f} / 100 điểm")
                    send_score_to_gsheet(student_name, exam_code, "PHẦN VIẾT", f"{c_cnt_total}/{tot}", sc_100)
                    
                    st.markdown("---")
                    st.markdown("### 🔍 CHI TIẾT PHẦN VIẾT (PHẦN 1):")
                    for q in q_w_p1:
                        if u_w_ans.get(q['num']) not in q['correct']:
                            st.markdown(f"❌ **Câu {q['num']}**: Bạn viết `{u_w_ans.get(q['num'])}` | Đáp án đúng: **{q['correct'][0]}**")


# CHỮ KÝ CHỈ ĐỂ 黄宝玉老师 THÔI
st.markdown("""
<div class="footer">
    黄宝玉老师
</div>
""", unsafe_allow_html=True)
