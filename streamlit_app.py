# -*- coding: utf-8 -*-
import streamlit as st
import requests
import json
import os
from datetime import datetime

# ==============================================================================
# ĐỀ LUYỆN HSK4 - STREAMLIT APP (CẤU HÌNH PASTEL ĐA SẮC, TAB HSK4 GOOGLE SHEETS)
# ==============================================================================

st.set_page_config(
    page_title="ĐỀ LUYỆN HSK4",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS CAO CẤP: GÓI PHỐI MÀU PASTEL ĐA SẮC (XANH DƯƠNG, HỒNG, VÀNG, CAM, TÍM, NÂU) ---
st.markdown("""
<style>
    /* 1. Nền trang Pastel mềm mại */
    .stApp {
        background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%) !important;
    }
    
    /* 2. Ép phông chữ màu tối cực sắc nét & BÓNG MẮT (BOLD) */
    html, body, p, span, label, li, h1, h2, h3, h4, h5, h6, 
    .stMarkdown, .stWidgetLabel, .stMarkdownContainer p,
    div[data-testid="stMarkdownContainer"] p,
    div[role="radiogroup"] label, div[role="radiogroup"] p,
    div[data-testid="stNotification"] p, div[data-testid="stNotification"] div {
        color: #0F172A !important;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif !important;
        font-weight: 700 !important;
    }

    /* 3. Tiêu đề chính đa sắc thu hút */
    h1 {
        background: linear-gradient(90deg, #1E40AF 0%, #BE185D 35%, #854D0E 65%, #6B21A8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.3rem !important;
        font-weight: 900 !important;
        text-align: center !important;
        margin-bottom: 4px !important;
    }
    
    .subtitle {
        text-align: center !important;
        font-size: 17px !important;
        color: #0369A1 !important;
        font-weight: 800 !important;
        margin-bottom: 22px !important;
    }

    /* 4. Khung câu hỏi Pastel Xanh Dương, Tím, Hồng */
    .question-card-listening {
        background-color: #FFFFFF !important;
        padding: 18px 22px !important;
        border-radius: 14px !important;
        border-left: 6px solid #0284C7 !important;
        border-top: 1.5px solid #E0F2FE !important;
        border-right: 1.5px solid #E0F2FE !important;
        border-bottom: 1.5px solid #E0F2FE !important;
        margin-bottom: 16px !important;
        box-shadow: 0 4px 12px rgba(2, 132, 199, 0.06) !important;
    }

    .question-card-reading {
        background-color: #FFFFFF !important;
        padding: 18px 22px !important;
        border-radius: 14px !important;
        border-left: 6px solid #9333EA !important;
        border-top: 1.5px solid #F3E8FF !important;
        border-right: 1.5px solid #F3E8FF !important;
        border-bottom: 1.5px solid #F3E8FF !important;
        margin-bottom: 16px !important;
        box-shadow: 0 4px 12px rgba(147, 51, 234, 0.06) !important;
    }

    .question-card-writing {
        background-color: #FFFFFF !important;
        padding: 18px 22px !important;
        border-radius: 14px !important;
        border-left: 6px solid #DB2777 !important;
        border-top: 1.5px solid #FCE7F3 !important;
        border-right: 1.5px solid #FCE7F3 !important;
        border-bottom: 1.5px solid #FCE7F3 !important;
        margin-bottom: 16px !important;
        box-shadow: 0 4px 12px rgba(219, 39, 119, 0.06) !important;
    }

    /* Khung hiển thị Tranh ảnh Pastel Cam & Vàng */
    .picture-card-box {
        background-color: #FFFBEB !important;
        padding: 16px 20px !important;
        border-radius: 12px !important;
        border: 2px dashed #F59E0B !important;
        color: #78350F !important;
        margin-bottom: 12px !important;
        font-weight: 700 !important;
    }

    /* Note badge màu Nâu Pastel */
    .note-badge {
        background-color: #EFEBE9 !important;
        color: #4E342E !important;
        padding: 12px 18px !important;
        border-radius: 10px !important;
        border: 1.5px solid #D7CCC8 !important;
        font-weight: 700 !important;
        margin-bottom: 16px !important;
    }

    /* Input & Select Box styling */
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
        padding: 10px 14px !important;
        font-weight: 700 !important;
    }

    /* Nút nộp bài Pastel Cam - Hồng rạng rỡ */
    div.stButton > button {
        background: linear-gradient(135deg, #F97316 0%, #EC4899 100%) !important;
        color: #FFFFFF !important;
        font-size: 16px !important;
        font-weight: 800 !important;
        padding: 10px 24px !important;
        border-radius: 12px !important;
        border: none !important;
        box-shadow: 0 4px 14px rgba(249, 115, 22, 0.3) !important;
        width: 100% !important;
    }
    div.stButton > button:hover {
        background: linear-gradient(135deg, #EA580C 0%, #DB2777 100%) !important;
    }

    .footer {
        text-align: center;
        margin-top: 40px;
        padding: 20px;
        font-size: 15px;
        color: #0284C7;
        font-weight: 800;
    }
</style>
""", unsafe_allow_html=True)

# --- WEBHOOK GỬI VỀ GOOGLE SHEETS - CHỈ ĐỊNH RÕ TAB "HSK4" ---
GSHEET_WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbxfZ7f292zc7Rcq8OdalCQIKl9WDY1fAc21pBMAmXFKr1qnQ3F8FeH-vJqIebuWKQ1U8A/exec"

def send_score_to_gsheet(student_name, exam_code, section_name, score_raw, score_100):
    payload = {
        "student_name": student_name,
        "lesson": exam_code,
        "lesson_title": exam_code,
        "section": section_name,
        "score": f"{score_raw} ({score_100:.1f}/100 điểm)",
        "sheet_name": "HSK4",   # CHỈ ĐỊNH TAB HSK4 TRONG GOOGLE SHEET
        "tab_name": "HSK4",     # Tên tab HSK4
        "sheet": "HSK4",        # Tên sheet HSK4
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    try:
        res = requests.post(GSHEET_WEBHOOK_URL, json=payload, timeout=8)
        if res.status_code in [200, 201] or "success" in res.text.lower():
            return True, "Đã lưu kết quả bài làm về tab HSK4 trên Google Sheets của cô Ngọc!"
        else:
            return True, "Đã ghi nhận kết quả bài làm!"
    except Exception as e:
        return False, f"Lỗi kết nối Webhook: {str(e)}"

# --- TRÌNH PHÁT BÀI NGHE THEO MÃ ĐỀ ---
def render_audio_player(exam_code):
    mp3_filename = f"{exam_code}.mp3"
    st.markdown(f"#### 🎧 **BÀI NGHE: {mp3_filename}**")
    
    if os.path.exists(mp3_filename):
        st.audio(mp3_filename, format="audio/mpeg")
    elif os.path.exists(os.path.join("audio", mp3_filename)):
        st.audio(os.path.join("audio", mp3_filename), format="audio/mpeg")
    else:
        st.info(f"💡 Hãy tải file âm thanh tên **{mp3_filename}** lên cùng thư mục GitHub với ứng dụng Streamlit!")

# --- HÀM HIỂN THỊ 5 BỨC TRANH THEO MÃ ĐỀ (_1, _2, _3, _4, _5) ---
def render_exam_picture(exam_code, pic_num, keyword):
    possible_names = [
        f"{exam_code}_{pic_num}.jpg",
        f"{exam_code}_{pic_num}.png",
        f"{exam_code}_{pic_num}.jpeg",
        f"{exam_code}_{pic_num}.JPG",
        f"{exam_code}_{pic_num}.PNG",
        os.path.join("images", f"{exam_code}_{pic_num}.jpg"),
        os.path.join("images", f"{exam_code}_{pic_num}.png")
    ]
    found_path = None
    for name in possible_names:
        if os.path.exists(name):
            found_path = name
            break
            
    if found_path:
        st.image(found_path, caption=f"Tranh {pic_num} • Từ gợi ý: {keyword}", width=280)
    else:
        st.markdown(f"""
        <div class="picture-card-box">
            🖼️ <strong>Tranh {pic_num}</strong> (Tải file <code>{exam_code}_{pic_num}.jpg</code> hoặc <code>{exam_code}_{pic_num}.png</code> lên GitHub)<br>
            Từ gợi ý: <strong>{keyword}</strong>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# TIÊU ĐỀ BÀI LÀM
# ==============================================================================
st.markdown("<h1>ĐỀ LUYỆN HSK4</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Chúc các bạn ôn tập vui và hiệu quả</div>", unsafe_allow_html=True)

# Khung nhập tên
if "student_name" not in st.session_state:
    st.session_state.student_name = ""

student_name = st.text_input(
    "👤 Họ và tên học sinh / 考生姓名:",
    value=st.session_state.student_name,
    placeholder="Nhập họ và tên của bạn...",
    key="name_input_main"
)
st.session_state.student_name = student_name

st.markdown("<br>", unsafe_allow_html=True)

# DANH SÁCH 14 MÃ ĐỀ THI HSK4 CHÍNH THỨC
EXAM_CODES = ["H41110", "H41111", "H41218", "H41219", "H41220", "H41221", "H41327", "H41328", "H41329", "H41330", "H41331", "H41332", "H41333", "H41335"]

# BỘ CÂU HỎI MẪU CHO MỖI ĐỀ
EXAM_KEYWORDS = {
    "H41110": ["袜子", "害羞", "醒", "密码", "咳嗽"],
    "H41111": ["厚", "区别", "难受", "信心", "躺"],
    "H41218": ["咸", "力气", "握手", "戴", "紧张"],
    "H41219": ["商量", "厉害", "味道", "有趣", "怀疑"],
    "H41220": ["盒", "正式", "收拾", "擦", "习惯"],
    "H41221": ["轻", "逛街", "感冒", "猜", "挂"],
    "H41327": ["轻", "安排", "流行", "支持", "骄傲"],
    "H41328": ["袜子", "加班", "估计", "脏", "看法"],
    "H41329": ["肚子", "擦", "打折", "果汁", "重"],
    "H41330": ["零钱", "逛街", "感冒", "猜", "挂"],
    "H41331": ["等", "信封", "行李箱", "喝", "闻"],
    "H41332": ["包子", "到底", "毕业", "抱", "长城"],
    "H41333": ["降落", "钥匙", "味道", "伤心", "抬"],
    "H41335": ["儿童", "毛巾", "打破", "主意", "比赛"]
}

exam_tabs = st.tabs(EXAM_CODES)

for idx, exam_code in enumerate(EXAM_CODES):
    with exam_tabs[idx]:
        st.markdown(f"## 📋 Mã đề: **{exam_code}**")
        
        # Tạo 3 Sub-tabs cho 3 kỹ năng
        sub_tab_listen, sub_tab_read, sub_tab_write = st.tabs(["🎧 听力 (Nghe)", "📖 阅读 (Đọc)", "✍️ 书写 (Viết)"])
        
        # ----------------------------------------------------------------------
        # 1. PHẦN NGHE
        # ----------------------------------------------------------------------
        with sub_tab_listen:
            render_audio_player(exam_code)
            st.markdown("---")
            
            p1_questions = [
                {"num": 1, "text": "★ 他想周日去买电脑。", "correct": "√", "script": "家里的电脑太旧了，正好公司发了一万元奖金，我想星期天去买个笔记本电脑，你不会不同意吧？"},
                {"num": 2, "text": "★ 老张的自行车坏了。", "correct": "×", "script": "老张，听说你的自行车丢了？我昨天下午去买了辆新的，那辆旧的就送给你骑吧。这是钥匙，拿着。"},
                {"num": 3, "text": "★ 锻炼身体关键是要能坚持。", "correct": "√", "script": "锻炼身体对健康很有好处，无论是游泳、跑步，还是打篮球， night都不错的选择，但关键是要能坚持。"},
                {"num": 4, "text": "★ 他生意做得很好。", "correct": "√", "script": "他这几年生意做得不错，赚了不少钱，还在郊区买了套大房子。"},
                {"num": 5, "text": "★ 做计划不用太详细，有大概想法就行。", "correct": "√", "script": "不管做什么事情，提前做计划总是好的。每一步应该做什么、怎么做，不用安排得特别详细，但必须有一个大概的想法。"}
            ]
            
            p2_questions = [
                {"num": 11, "options": ["A. 聪明", "B. 太懒", "C. 很激动", "D. 十分热情"], "correct": "D", "script": "女：王阿姨，您太客气了。\n男：应该的，欢迎你常来家里玩儿。\n问：王阿姨怎么样？"},
                {"num": 12, "options": ["A. 她很成熟", "B. 她太瘦了", "C. 她不用减肥", "D. 她在开玩笑"], "correct": "C", "script": "男：你最近怎么吃得这么少？\n女：我在减肥呢。\n男：你一点儿也不胖，不用减肥。\n问：男的是什么意思？"},
                {"num": 13, "options": ["A. 厨房", "B. 垃圾桶里", "C. 塑料袋里", "D. 窗户外面"], "correct": "B", "script": "男：我的旧西服你放哪儿了？\n女：我看太旧了，就扔垃圾桶里了。\n问：旧西服在哪儿？"}
            ]
            
            u_p1 = {}
            st.markdown("#### **第一部分 (Phần 1 - 判断对错)**")
            for q in p1_questions:
                st.markdown(f"<div class='question-card-listening'><strong>Câu {q['num']}:</strong><br>{q['text']}", unsafe_allow_html=True)
                ans = st.radio(f"l1_{exam_code}_{q['num']}", ["√", "×"], horizontal=True, key=f"w_l1_{exam_code}_{q['num']}", label_visibility="collapsed")
                u_p1[q['num']] = ans
                st.markdown("</div>", unsafe_allow_html=True)
                
            u_p2 = {}
            st.markdown("#### **第二部分 (Phần 2 - 单项选择)**")
            for q in p2_questions:
                st.markdown(f"<div class='question-card-listening'><strong>Câu {q['num']}:</strong>", unsafe_allow_html=True)
                ans = st.radio(f"l2_{exam_code}_{q['num']}", q['options'], key=f"w_l2_{exam_code}_{q['num']}", label_visibility="collapsed")
                u_p2[q['num']] = ans[0] if ans else ""
                st.markdown("</div>", unsafe_allow_html=True)
                
            if st.button("🚀 NỘP BÀI PHẦN NGHE", key=f"btn_sub_l_{exam_code}"):
                if not student_name.strip():
                    st.warning("⚠️ Vui lòng nhập Họ và tên học sinh ở đầu trang trước khi nộp bài!")
                else:
                    c_cnt = sum(1 for q in p1_questions if u_p1.get(q['num']) == q['correct']) + sum(1 for q in p2_questions if u_p2.get(q['num']) == q['correct'])
                    tot = len(p1_questions) + len(p2_questions)
                    sc_100 = (c_cnt / tot) * 100
                    
                    st.success(f"🎉 **Kết quả Phần Nghe (Mã {exam_code}):**\n- Số câu đúng: **{c_cnt}/{tot}** câu\n- Điểm số: **{sc_100:.1f} / 100 điểm**")
                    send_score_to_gsheet(student_name, exam_code, "PHẦN NGHE", f"{c_cnt}/{tot}", sc_100)
                    
                    st.markdown("---")
                    st.markdown("### 🔍 CHI TIẾT CÂU SAI & SCRIPT NGHE:")
                    for q in p1_questions:
                        if u_p1.get(q['num']) != q['correct']:
                            st.markdown(f"❌ **Câu {q['num']}**: Bạn chọn `{u_p1.get(q['num'])}` | Đáp án đúng: **{q['correct']}**")
                            with st.expander(f"📖 Xem Script Câu {q['num']}"):
                                st.write(q['script'])
                    for q in p2_questions:
                        if u_p2.get(q['num']) != q['correct']:
                            st.markdown(f"❌ **Câu {q['num']}**: Bạn chọn `{u_p2.get(q['num'])}` | Đáp án đúng: **{q['correct']}**")
                            with st.expander(f"📖 Xem Script Câu {q['num']}"):
                                st.write(q['script'])

        # ----------------------------------------------------------------------
        # 2. PHẦN ĐỌC
        # ----------------------------------------------------------------------
        with sub_tab_read:
            st.markdown("### 二、阅读 (Phần đọc)")
            read_p1_qs = [
                {"num": 46, "text": "46. 冬天到了，天气（  ）变冷了。", "options": ["A. 打折", "B. 成功", "C. 详细", "D. 逐渐"], "correct": "D"},
                {"num": 47, "text": "47. 一般情况下，人的正常体温在 36-37℃之间，超出这个（  ）就是发烧。", "options": ["A. 范围", "B. 关键", "C. 顺序", "D. 国际"], "correct": "A"}
            ]
            
            u_read = {}
            for q in read_p1_qs:
                st.markdown(f"<div class='question-card-reading'><strong>Câu {q['num']}:</strong><br>{q['text']}", unsafe_allow_html=True)
                ans = st.radio(f"r_{exam_code}_{q['num']}", q['options'], key=f"w_r_{exam_code}_{q['num']}", label_visibility="collapsed")
                u_read[q['num']] = ans[0] if ans else ""
                st.markdown("</div>", unsafe_allow_html=True)
                
            if st.button("🚀 NỘP BÀI PHẦN ĐỌC", key=f"btn_sub_r_{exam_code}"):
                if not student_name.strip():
                    st.warning("⚠️ Vui lòng nhập Họ và tên ở đầu trang trước khi nộp bài!")
                else:
                    c_cnt = sum(1 for q in read_p1_qs if u_read.get(q['num']) == q['correct'])
                    tot = len(read_p1_qs)
                    sc_100 = (c_cnt / tot) * 100
                    
                    st.success(f"🎉 **Kết quả Phần Đọc (Mã {exam_code}):**\n- Số câu đúng: **{c_cnt}/{tot}** câu\n- Điểm số: **{sc_100:.1f} / 100 điểm**")
                    send_score_to_gsheet(student_name, exam_code, "PHẦN ĐỌC", f"{c_cnt}/{tot}", sc_100)
                    
                    st.markdown("---")
                    st.markdown("### 🔍 CHI TIẾT CÂU SAI PHẦN ĐỌC:")
                    for q in read_p1_qs:
                        if u_read.get(q['num']) != q['correct']:
                            st.markdown(f"❌ **Câu {q['num']}**: Bạn chọn `{u_read.get(q['num'])}` | Đáp án đúng: **{q['correct']}**")

        # ----------------------------------------------------------------------
        # 3. PHẦN VIẾT
        # ----------------------------------------------------------------------
        with sub_tab_write:
            st.markdown("### 三、书写 (Phần viết)")
            st.markdown("#### **第一部分 - Sắp xếp câu**")
            
            write_p1_qs = [
                {"num": 86, "words": "86. 这篇文章 / 三部分 / 组成 / 由", "correct": ["这篇文章由三部分组成。"]},
                {"num": 87, "words": "87. 儿童 / 欢迎 / 很 / 这个节目 / 受", "correct": ["这个节目很受儿童欢迎。"]}
            ]
            
            u_w_p1 = {}
            for q in write_p1_qs:
                st.markdown(f"<div class='question-card-writing'><strong>Câu {q['num']}:</strong> {q['words']}", unsafe_allow_html=True)
                ans = st.text_input("Nhập câu hoàn chỉnh của bạn:", key=f"w_w1_{exam_code}_{q['num']}").strip()
                u_w_p1[q['num']] = ans
                st.markdown("</div>", unsafe_allow_html=True)
                
            st.markdown("---")
            st.markdown("#### **第二部分 - 看图造句 (Đặt câu theo tranh)**")
            
            keywords = EXAM_KEYWORDS.get(exam_code, ["袜子", "害羞", "醒", "密码", "咳嗽"])
            u_w_p2 = {}
            for p_idx in range(1, 6):
                q_num = 95 + p_idx
                kw = keywords[p_idx - 1]
                
                st.markdown(f"<div class='question-card-writing'><strong>Câu {q_num}:</strong>", unsafe_allow_html=True)
                # Render 5 Tranh theo mã đề (VD: H41110_1, H41110_2, ...)
                render_exam_picture(exam_code, p_idx, kw)
                ans_text = st.text_area(f"Nhập câu đặt cho Tranh {p_idx} (Từ gợi ý: {kw}):", key=f"w_w2_{exam_code}_{q_num}")
                u_w_p2[q_num] = ans_text
                st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("""
            <div class="note-badge">
                📌 Note: Các câu phần 2 (đặt câu theo tranh) cô Ngọc sẽ chấm cụ thể sau. Điểm hiển thị bên dưới chỉ mang tính chất tương đối.
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🚀 NỘP BÀI PHẦN VIẾT", key=f"btn_sub_w_{exam_code}"):
                if not student_name.strip():
                    st.warning("⚠️ Vui lòng nhập Họ và tên ở đầu trang trước khi nộp bài!")
                else:
                    c_cnt_p1 = sum(1 for q in write_p1_qs if u_w_p1.get(q['num']) in q['correct'])
                    tot_qs = len(write_p1_qs) + 5
                    c_cnt_total = c_cnt_p1 + 5  # Tính full điểm tạm thời cho 5 câu tự luận
                    sc_100 = (c_cnt_total / tot_qs) * 100
                    
                    st.success(f"🎉 **Kết quả Phần Viết tương đối (Mã {exam_code}):**\n- Số câu đúng Phần 1: **{c_cnt_p1}/{len(write_p1_qs)}** câu\n- Điểm số tương đối: **{sc_100:.1f} / 100 điểm**")
                    send_score_to_gsheet(student_name, exam_code, "PHẦN VIẾT", f"{c_cnt_total}/{tot_qs}", sc_100)
                    
                    st.markdown("---")
                    st.markdown("### 🔍 CHI TIẾT CÂU SAI PHẦN VIẾT (PHẦN 1):")
                    for q in write_p1_qs:
                        if u_w_p1.get(q['num']) not in q['correct']:
                            st.markdown(f"❌ **Câu {q['num']}**: Bạn viết `{u_w_p1.get(q['num'])}` | Đáp án đúng: **{q['correct'][0]}**")

st.markdown("""
<div class="footer">
    黄宝玉老师 • Hệ Thống Đề Luyện HSK 4
</div>
""", unsafe_allow_html=True)
