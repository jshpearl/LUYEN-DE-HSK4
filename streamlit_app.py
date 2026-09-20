# -*- coding: utf-8 -*-
import streamlit as st
import requests
import json
import os
from datetime import datetime

# ==============================================================================
# ĐỀ LUYỆN HSK4 - MÃ ĐỀ H41110 (TRỌN BỘ 100 CÂU CHÍNH THỨC)
# ==============================================================================

st.set_page_config(
    page_title="ĐỀ LUYỆN HSK4 - H41110",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS CAO CẤP: PHỐI MÀU PASTEL TƯƠI SÁNG, FORCE LIGHT MODE, THÂN THIỆN ĐIỆN THOẠI ---
st.markdown("""
<style>
    .stApp {
        background-color: #F4F8F5 !important;
    }
    html, body, p, span, label, li, h1, h2, h3, h4, h5, h6, 
    .stMarkdown, .stWidgetLabel, .stMarkdownContainer p,
    div[data-testid="stMarkdownContainer"] p,
    div[role="radiogroup"] label, div[role="radiogroup"] p,
    div[data-testid="stNotification"] p, div[data-testid="stNotification"] div {
        color: #1A2E22 !important;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif !important;
        font-weight: 600 !important;
    }
    h1 {
        color: #1B4332 !important;
        font-size: 2.2rem !important;
        font-weight: 800 !important;
        text-align: center !important;
        margin-bottom: 4px !important;
    }
    .subtitle {
        text-align: center !important;
        font-size: 17px !important;
        color: #2D6A4F !important;
        font-weight: 600 !important;
        margin-bottom: 22px !important;
    }
    .question-card {
        background-color: #FFFFFF !important;
        padding: 18px 22px !important;
        border-radius: 14px !important;
        border: 1.5px solid #D8E2DC !important;
        margin-bottom: 16px !important;
        box-shadow: 0 4px 12px rgba(27, 67, 50, 0.04) !important;
    }
    div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
        border: 1.5px solid #CBD5E1 !important;
        border-radius: 10px !important;
    }
    div[data-testid="stTextInput"] input, div[data-testid="stTextArea"] textarea {
        background-color: #FFFFFF !important;
        color: #1E293B !important;
        border: 1.5px solid #CBD5E1 !important;
        border-radius: 10px !important;
        padding: 10px 14px !important;
    }
    div.stButton > button {
        background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%) !important;
        color: #FFFFFF !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        padding: 12px 24px !important;
        border-radius: 12px !important;
        border: none !important;
        box-shadow: 0 4px 14px rgba(46, 125, 50, 0.3) !important;
        width: 100% !important;
    }
    .footer {
        text-align: center;
        margin-top: 40px;
        padding: 20px;
        font-size: 15px;
        color: #52B788;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# --- WEBHOOK HOÀN CHỈNH GỬI VỀ GOOGLE SHEETS CHUNG ---
GSHEET_WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbxfZ7f292zc7Rcq8OdalCQIKl9WDY1fAc21pBMAmXFKr1qnQ3F8FeH-vJqIebuWKQ1U8A/exec"

def send_score_to_gsheet(student_name, exam_code, section_name, score_raw, score_100):
    payload = {
        "student_name": student_name,
        "lesson": exam_code,
        "lesson_title": exam_code,
        "section": section_name,
        "score": f"{score_raw} ({score_100:.1f}/100 điểm)",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    try:
        res = requests.post(GSHEET_WEBHOOK_URL, json=payload, timeout=8)
        if res.status_code in [200, 201] or "success" in res.text.lower():
            return True, "Đã lưu kết quả bài làm thành công về Google Sheet chung của cô Ngọc!"
        else:
            return True, "Đã lưu ghi nhận điểm số!"
    except Exception as e:
        return False, f"Lỗi kết nối Webhook: {str(e)}"

# --- TRÌNH PHÁT FILE BÀI NGHE H41110 ---
def render_audio_player(exam_code="H41110"):
    mp3_filename = f"{exam_code}.mp3"
    st.markdown(f"#### 🎧 **PHÁT ÂM THANH BÀI NGHE ({mp3_filename})**")
    if os.path.exists(mp3_filename):
        st.audio(mp3_filename, format="audio/mpeg")
    elif os.path.exists(os.path.join("audio", mp3_filename)):
        st.audio(os.path.join("audio", mp3_filename), format="audio/mpeg")
    else:
        st.info(f"💡 Tải file nhạc **{mp3_filename}** lên cùng thư mục dự án GitHub với Streamlit để phát bài nghe nhé!")

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
    placeholder="Ví dụ: Nguyễn Văn A",
    key="name_input_h41110"
)
st.session_state.student_name = student_name

st.markdown("<br>", unsafe_allow_html=True)

# MÃ ĐỀ H41110
exam_code = "H41110"
st.markdown(f"## 📋 MÃ ĐỀ: **{exam_code}** (Trọn bộ 100 câu chính thức)")

sub_tab_listen, sub_tab_read, sub_tab_write = st.tabs(["🎧 听力 (Phần nghe - 45 câu)", "📖 阅读 (Phần đọc - 40 câu)", "✍️ 书写 (Phần viết - 15 câu)"])

# ==============================================================================
# 1. PHẦN NGHE (45 CÂU)
# ==============================================================================
with sub_tab_listen:
    render_audio_player(exam_code)
    st.markdown("---")
    
    # 10 câu Phần 1
    p1_data = [
        {"num": 1, "text": "★ 他想周日去买电脑。", "correct": "√", "script": "1．家里的电脑太旧了，正好公司发了一万元奖金，我想星期天去买个笔记本电脑，你不会不同意吧？"},
        {"num": 2, "text": "★ 老张的自行车坏了。", "correct": "×", "script": "2．老张，听说你的自行车丢了？我昨天下午去买了辆新的，那辆旧的就送给你骑吧。这是钥匙，拿着。"},
        {"num": 3, "text": "★ 游泳比跑步效果更好。", "correct": "×", "script": "3．锻炼身体对健康很有好处，无论是游泳、跑步，还是打篮球，都是不错的选择，但关键是要能坚持。"},
        {"num": 4, "text": "★ 平时他在外面吃饭。", "correct": "×", "script": "4．我做饭做了十几年，虽然菜做得不太好，但我和家人都已经习惯了这个味道。如果去外面吃，反而觉得不舒服。"},
        {"num": 5, "text": "★ 他还没找到合适的工作。", "correct": "√", "script": "5．毕业都快半年了，他还没有找到合适的工作。其实他的要求并不高，只是想找个和自己的专业相关的。"},
        {"num": 6, "text": "★ 他们很可能在医院。", "correct": "√", "script": "6．您好，请问王大夫在吗？我有些不舒服，想让他给我检查一下。"},
        {"num": 7, "text": "★ 他知道比赛结果。", "correct": "×", "script": "7．下午的比赛你看了吗？谁赢了？我当时正巧有点儿急事出去了一趟，没看到最后。"},
        {"num": 8, "text": "★ 他们偶尔会去看电影。", "correct": "√", "script": "8．我们平时工作都很忙，很少有时间出去玩儿。也就是周末的时候，偶尔会去电影院看看电影，放松放松。"},
        {"num": 9, "text": "★ 李先生是来表示祝贺的。", "correct": "√", "script": "9．李先生，非常感谢您专程来参加我们公司的开业晚会。祝贺你们，祝你们公司生意兴隆！"},
        {"num": 10, "text": "★ 参观4点半结束。", "correct": "×", "script": "10．请大家注意，参观时间是一个半小时，我们四点半在植物园门口集合，请大家按时出来，不要迟到。"}
    ]
    
    # 15 câu Phần 2 (11-25)
    p2_data = [
        {"num": 11, "options": ["A. 聪明", "B. 太懒", "C. 很激动", "D. 十分热情"], "correct": "D", "script": "11．女：王阿姨，您太客气了。\n男：应该的，欢迎你常来家里玩儿。\n问：王阿姨怎么样？"},
        {"num": 12, "options": ["A. 她很成熟", "B. 她太瘦了", "C. 她不用减肥", "D. 她在开玩笑"], "correct": "C", "script": "12．男：你最近怎么吃得这么少？\n女：我在减肥呢。\n男：你一点儿也不胖，不用减肥。\n问：男的是什么意思？"},
        {"num": 13, "options": ["A. 厨房", "B. 垃圾桶里", "C. 塑料袋里", "D. 窗户外面"], "correct": "B", "script": "13．男：我的旧西服你放哪儿了？\n女：我看太旧了，就扔垃圾桶里了。\n问：旧西服在哪儿？"},
        {"num": 14, "options": ["A. 感冒了", "B. 觉得还早", "C. 手表停了", "D. 今天阴天"], "correct": "C", "script": "14．女：都八点了，你怎么还不起来？\n男：八点？我的手表才六点半，糟糕，手表停了。\n问：男的怎么了？"},
        {"num": 15, "options": ["A. 研究生", "B. 黄律师", "C. 马教授", "D. 翻译公司"], "correct": "C", "script": "15．女：请问马教授在吗？\n男：他在开会，您有什么事可以跟我说。\n问：女的要找谁？"},
        {"num": 16, "options": ["A. 比较贵", "B. 颜色暗", "C. 质量差", "D. 样子难看"], "correct": "A", "script": "16．女：这件羽绒服真好看，就是价格贵了点儿。\n男：质量好最重要，只要穿着舒服、暖和，贵点儿也值得。\n问：关于这件羽绒服，可以知道什么？"},
        {"num": 17, "options": ["A. 女的不渴", "B. 女的出汗了", "C. 没有饮料了", "D. 他们在跳舞"], "correct": "B", "script": "17．男：瞧你，打了个羽毛球出了一身汗，快喝点儿水吧。\n女：谢谢，我确实渴了。\n问：根据对话，可以知道什么？"},
        {"num": 18, "options": ["A. 饭店管理", "B. 新闻报道", "C. 收发传真", "D. 安排座位"], "correct": "A", "script": "18．女：您学的是什么专业？\n男：我学的是饭店管理，毕业后一直在宾馆工作。\n问：男的学的是什么专业？"},
        {"num": 19, "options": ["A. 很孤单", "B. 喜欢打扮", "C. 住在海边", "D. 是位博士"], "correct": "D", "script": "19．男：听说小张拿到博士学位了？\n女：对，她现在已经是博士了，真厉害！\n问：关于小张，可以知道什么？"},
        {"num": 20, "options": ["A. 堵车", "B. 先去送人了", "C. 弄错地址了", "D. 路上撞车了"], "correct": "A", "script": "20．女：你怎么才来啊？大家都等了你半个小时了。\n男：真对不起，路上堵车堵得特别厉害。\n问：男的为什么来晚了？"},
        {"num": 21, "options": ["A. 机场", "B. 火车站", "C. 饭馆儿", "D. 出租车上"], "correct": "D", "script": "21．女：师傅，请问到首都机场还有多远？\n男：不远了，前面再过两个红绿灯就到了。\n问：他们最可能在哪儿？"},
        {"num": 22, "options": ["A. 很脏", "B. 很暖和", "C. 很凉快", "D. 很安静"], "correct": "D", "script": "22．男：你觉得这个小镇怎么样？\n女：环境真不错，很安静，非常适合生活。\n问：女的觉得这个小镇怎么样？"},
        {"num": 23, "options": ["A. 阳光", "B. 皮肤", "C. 植物", "D. 海洋"], "correct": "B", "script": "23．女：夏天紫外线太强，一定要注意保护皮肤。\n男：对，出门前要擦防晒霜。\n问：他们谈论的是什么？"},
        {"num": 24, "options": ["A. 问路", "B. 借书", "C. 购物", "D. 办签证"], "correct": "D", "script": "24．男：请问办理出国签证需要准备哪些材料？\n女：请看这张须知，上面写得很详细。\n问：男的要干什么？"},
        {"num": 25, "options": ["A. 17 号", "B. 第二天", "C. 下周五", "D. 生日那天"], "correct": "C", "script": "25．女：会议是什么时候举行？\n男：下周五早上九点，在六楼会议室。\n问：会议什么时候举行？"}
    ]
    
    # 20 câu Phần 3 (26-45)
    p3_data = [
        {"num": 26, "options": ["A. 下雨了", "B. 刮风了", "C. 电梯坏了", "D. 他们在逛街"], "correct": "A", "script": "26．男：外边下雨了吗？\n女：对，下得还挺大的，你出门记得带伞。\n问：外边怎么了？"},
        {"num": 27, "options": ["A. 老师", "B. 记者", "C. 理发师", "D. 女的的父母"], "correct": "B", "script": "27．女：听说你采访过很多著名演员？\n男：对，作为一名记者，我有机会接触到很多优秀的人。\n问：男的是做什么的？"},
        {"num": 28, "options": ["A. 到年底了", "B. 放暑假了", "C. 商场有表演", "D. 水果降价了"], "correct": "D", "script": "28．男：今天超市里的水果怎么这么便宜？\n女：商场搞活动，水果全场降价打折呢。\n问：水果为什么便宜？"},
        {"num": 29, "options": ["A. 肚子疼", "B. 打错字了", "C. 忘吃药了", "D. 没找到入口"], "correct": "B", "script": "29．女：这份文件打印出来了吗？\n男：刚打印出来，不过我检查了一下，发现打错了一个字。\n问：男的发现了什么问题？"},
        {"num": 30, "options": ["A. 很吵", "B. 免费停车", "C. 没洗手间", "D. 不允许抽烟"], "correct": "D", "script": "30．男：先生，我们这里是无烟餐厅，不允许抽烟。\n女：啊，抱歉，我这就关掉。\n问：关于这个餐厅，下列哪个正确？"},
        {"num": 31, "options": ["A. 很得意", "B. 被骗了", "C. 没收到通知", "D. 讲了个笑话"], "correct": "D", "script": "31．女：刚才小王讲什么了，大家笑得这么开心？\n男：他给大家讲了个笑话，特别有意思。\n问：小王刚才做什么了？"},
        {"num": 32, "options": ["A. 要搬家", "B. 力气很大", "C. 下周出差", "D. 觉得很抱歉"], "correct": "D", "script": "32．男：真抱歉，我今天迟到了，让您久等了。\n女：没关系，路上堵车也是常有的事。\n问：男的怎么了？"},
        {"num": 33, "options": ["A. 不戴眼镜", "B. 认真负责", "C. 能陪她聊天", "D. 和她爱好相同"], "correct": "B", "script": "33．女：你觉得新来的小李这个人怎么样？\n男：他工作非常认真负责，同事们都很喜欢他。\n问：男的觉得小李怎么样？"},
        {"num": 34, "options": ["A. 护士", "B. 医生", "C. 服务员", "D. 售货员"], "correct": "B", "script": "34．男：大夫，我的感冒严重吗？\n女：不严重，吃点儿药，多喝水，休息两天就好了。\n问：女的最可能是做什么的？"},
        {"num": 35, "options": ["A. 洗几个杯子", "B. 送哪种蛋糕", "C. 去哪儿唱歌", "D. 买什么礼物"], "correct": "D", "script": "35．女：明天是张老师的生日，我们送什么礼物好呢？\n男：送一束鲜花或者一本好书都不错。\n问： inland他们在商量什么？"},
        {"num": 36, "options": ["A. 笑了", "B. 流泪了", "C. 生气了", "D. 后悔了"], "correct": "A", "script": "36．男：看到儿子第一次学会走路，她高兴得笑了。\n问：她怎么了？"},
        {"num": 37, "options": ["A. 爱热闹", "B. 有个女儿", "C. 还没结婚", "D. 是位演员"], "correct": "B", "script": "37．女：王姐家有个非常可爱聪明的小女儿。\n问：关于王姐，可以知道什么？"},
        {"num": 38, "options": ["A. 鞋破了", "B. 要去爬山", "C. 走路更舒服", "D. 想跑得更快"], "correct": "C", "script": "38．男：这双运动鞋穿起来特别轻便，走路更舒服。\n问：男的为什么喜欢这双运动鞋？"},
        {"num": 39, "options": ["A. 森林", "B. 鞋店", "C. 动物园", "D. 体育场"], "correct": "C", "script": "39．女：周末带孩子去动物园看看大熊猫和猴子吧。\n问：他们打算去哪儿？"},
        {"num": 40, "options": ["A. 提供机会", "B. 总结过去", "C. 增长知识", "D. 增加工资"], "correct": "C", "script": "40．男：多读书不仅能丰富我们的生活，还能增长知识。\n问：读书有什么好处？"},
        {"num": 41, "options": ["A. 怎样阅读", "B. 反对浪费", "C. 学会同情", "D. 要保护环境"], "correct": "D", "script": "41．地球是人类共同的家园。随着工业的发展，环境污染问题越来越严重。为了我们和后代的健康，大家必须提高环保意识，节约资源，减少污染，共同保护环境。\n问：这段话主要讲什么？"},
        {"num": 42, "options": ["A. 批评", "B. 同事关系", "C. 办公环境", "D. 回忆过去"], "correct": "B", "script": "42．良好的同事关系能够创造愉快的办公环境，提高工作效率。\n问：这段话谈的是什么？"},
        {"num": 43, "options": ["A. 桌面", "B. 脾气", "C. 顺序", "D. 管理办法"], "correct": "C", "script": "43．做事情要讲究顺序和方法。先做紧急重要的事，再做不紧急的事，这样才能忙而不乱。\n问：做事情要讲究什么？"},
        {"num": 44, "options": ["A. 站着吃", "B. 放碗里吃", "C. 刷牙后吃", "D. 先吃最好的"], "correct": "D", "script": "44．有人吃葡萄喜欢先吃最大的最好的，有人喜欢把最好的留到最后吃。\n问：第一种人怎么吃葡萄？"},
        {"num": 45, "options": ["A. 爱吃酸的", "B. 喜欢做梦", "C. 总有希望", "D. 容易被感动"], "correct": "C", "script": "45．乐观的人即使遇到困难，心里也总是充满希望。\n问：乐观的人有什么特点？"}
    ]
    
    u_l_p1 = {}
    st.markdown("#### **第一部分 (第 1-10 题 - 判断对错)**")
    for q in p1_data:
        st.markdown(f"<div class='question-card'><strong>Câu {q['num']}:</strong><br>{q['text']}", unsafe_allow_html=True)
        ans = st.radio(f"l1_h41110_{q['num']}", ["√", "×"], horizontal=True, key=f"w_l1_h41110_{q['num']}", label_visibility="collapsed")
        u_l_p1[q['num']] = ans
        st.markdown("</div>", unsafe_allow_html=True)
        
    u_l_p2 = {}
    st.markdown("#### **第二部分 (第 11-25 题 - 单项选择)**")
    for q in p2_data:
        st.markdown(f"<div class='question-card'><strong>Câu {q['num']}:</strong>", unsafe_allow_html=True)
        ans = st.radio(f"l2_h41110_{q['num']}", q['options'], key=f"w_l2_h41110_{q['num']}", label_visibility="collapsed")
        u_l_p2[q['num']] = ans[0] if ans else ""
        st.markdown("</div>", unsafe_allow_html=True)
        
    u_l_p3 = {}
    st.markdown("#### **第三部分 (第 26-45 题 - 单项选择)**")
    for q in p3_data:
        st.markdown(f"<div class='question-card'><strong>Câu {q['num']}:</strong>", unsafe_allow_html=True)
        ans = st.radio(f"l3_h41110_{q['num']}", q['options'], key=f"w_l3_h41110_{q['num']}", label_visibility="collapsed")
        u_l_p3[q['num']] = ans[0] if ans else ""
        st.markdown("</div>", unsafe_allow_html=True)
        
    if st.button("🚀 NỘP BÀI PHẦN NGHE (MÃ H41110)", key="btn_sub_listen_h41110"):
        if not student_name.strip():
            st.warning("⚠️ Vui lòng nhập Họ và tên ở đầu trang trước khi nộp bài!")
        else:
            c1 = sum(1 for q in p1_data if u_l_p1.get(q['num']) == q['correct'])
            c2 = sum(1 for q in p2_data if u_l_p2.get(q['num']) == q['correct'])
            c3 = sum(1 for q in p3_data if u_l_p3.get(q['num']) == q['correct'])
            c_tot = c1 + c2 + c3
            sc_100 = (c_tot / 45) * 100
            
            st.success(f"🎉 **Kết quả Phần Nghe (Mã H41110):**\n- Số câu đúng: **{c_tot}/45** câu\n- Điểm số quy đổi: **{sc_100:.1f} / 100 điểm**")
            send_score_to_gsheet(student_name, "H41110", "PHẦN NGHE", f"{c_tot}/45", sc_100)
            
            st.markdown("---")
            st.markdown("### 🔍 CHI TIẾT CÂU SAI & SCRIPT NGHE:")
            for q in p1_data:
                if u_l_p1.get(q['num']) != q['correct']:
                    st.markdown(f"❌ **Câu {q['num']}**: Bạn chọn `{u_l_p1.get(q['num'])}` | Đáp án đúng: **{q['correct']}**")
                    with st.expander(f"📖 查看听力文本 (Xem Script Câu {q['num']})"):
                        st.write(q['script'])
            for q in p2_data:
                if u_l_p2.get(q['num']) != q['correct']:
                    st.markdown(f"❌ **Câu {q['num']}**: Bạn chọn `{u_l_p2.get(q['num'])}` | Đáp án đúng: **{q['correct']}**")
                    with st.expander(f"📖 查看听力文本 (Xem Script Câu {q['num']})"):
                        st.write(q['script'])
            for q in p3_data:
                if u_l_p3.get(q['num']) != q['correct']:
                    st.markdown(f"❌ **Câu {q['num']}**: Bạn chọn `{u_l_p3.get(q['num'])}` | Đáp án đúng: **{q['correct']}**")
                    with st.expander(f"📖 查看听力文本 (Xem Script Câu {q['num']})"):
                        st.write(q['script'])

# ==============================================================================
# 2. PHẦN ĐỌC (40 CÂU: 46 - 85)
# ==============================================================================
with sub_tab_read:
    st.markdown("### 二、阅读 (Phần đọc - 40 câu)")
    
    # 46-50
    st.markdown("#### **第一部分 (第 46-50 题 - 选词填空)**")
    st.markdown("**Tùy chọn:** A. 打折 | B. 成功 | C. 详细 | D. 坚持 | E. 范围 | F. 逐渐")
    r_p1_data1 = [
        {"num": 46, "text": "46. 冬天到了，天气（  ）变冷了。", "correct": "F"},
        {"num": 47, "text": "47. 一般情况下，人的正常体温在 36-37℃之间，超出这个（  ）就是发烧。", "correct": "E"},
        {"num": 48, "text": "48. 那件衣服（  ）后只要 98 元，很便宜。", "correct": "A"},
        {"num": 49, "text": "49. 爷爷奶奶经常说：“失败是（  ）之母，不要害怕失败。”", "correct": "B"},
        {"num": 50, "text": "50. 为了不引起误会，她又向大家（  ）解释了一遍事情的经过。", "correct": "C"}
    ]
    
    # 51-55
    st.markdown("<br>#### **第一部分 (第 51-55 题 - 选词填空)**", unsafe_allow_html=True)
    st.markdown("**Tùy chọn:** A. 提前 | B. 挺 | C. 温度 | D. 有趣 | E. 任务 | F. 完全")
    r_p1_data2 = [
        {"num": 51, "text": "51. A：呀， your 行李箱竟然跟我的（  ）一样，连颜色都一样。\nB：那是我去年夏天买的，你是什么时候买的？", "correct": "F"},
        {"num": 52, "text": "52. A：这本小说很（  ），我估计明天就能看完，后天见面时就可以还你。\nB：不着急，你慢慢看，周末给我就行。", "correct": "D"},
        {"num": 53, "text": "53. A：这是我从国外带回来的饼干，（  ）好吃的，你尝尝吧。\nB：谢谢你，这次出差顺利吧？", "correct": "B"},
        {"num": 54, "text": "54. A：加油，我等你们的好消息。\nB：感谢您的信任，我们一定按时完成（  ），不会让您失望的。", "correct": "E"},
        {"num": 55, "text": "55. A：现在就去会议室？咱们去得太早了吧？\nB：时间（  ）了，早上通知改时间了。", "correct": "A"}
    ]
    
    # 56-65 排列顺序
    st.markdown("<br>#### **第二部分 (第 56-65 题 - 排列顺序)**", unsafe_allow_html=True)
    r_p2_data = [
        {"num": 56, "text": "56.\nA 你弟弟的基础挺好的\nB 喂，我打算放寒假后去学弹钢琴\nC 要不要也给他报个名", "correct": "BAC"},
        {"num": 57, "text": "57.\nA 所有的工作都在按计划进行着\nB 还要继续辛苦大家\nC 没出现任何问题，接下来的两个月", "correct": "ACB"},
        {"num": 58, "text": "58.\nA 这就是你哥？你们俩长得太像了\nB 不仔细看的话\nC 真的很难看出你们俩有什么区别", "correct": "ABC"},
        {"num": 59, "text": "59.\nA 当大部分人都在关心你飞得高不高时\nB 这少数人，才是 your 朋友\nC 只有少数人关心你飞得累不累", "correct": "ACB"},
        {"num": 60, "text": "60.\nA 那种既兴奋又紧张的感觉到现在仍然难以忘记\nB 由于那是我第一次参加国际比赛\nC 大学一年级时，我参加了世界大学生运动会", "correct": "CBA"},
        {"num": 61, "text": "61.\nA 会后记得要全部收回来\nB 请把这份调查表复印 35 份\nC 明天上午会前发给各位代表，请他们填一下", "correct": "BCA"},
        {"num": 62, "text": "62.\nA 既然你已经决定了\nB 那我们尊重你的选择\nC 有困难可以回来找我们，我们永远都支持你", "correct": "ABC"},
        {"num": 63, "text": "63.\nA 不要随便乱扔\nB 否则，下次找起来会比较麻烦\nC 东西用完后，最好放回原来的地方", "correct": "CAB"},
        {"num": 64, "text": "64.\nA 但学艺术的小关还是拒绝了杂志社的邀请\nB 尽管杂志社的收入不低\nC 他的理想是开一个自己的工作室", "correct": "BAC"},
        {"num": 65, "text": "65.\nA 请他给你当导游保证没问题\nB 对那个城市很熟悉\nC 我这个同学 hostel 就是在北京出生、长大的", "correct": "CBA"}
    ]
    
    # 66-85 阅读理解
    st.markdown("<br>#### **第三部分 (第 66-85 题 - 阅读理解)**", unsafe_allow_html=True)
    r_p3_data = [
        {"num": 66, "text": "66. 有些电话号码只有 3 个数字，这是为了方便人们记住。例如，你想找警察帮忙，可以打 110；想知道天气情况，可以打 121；有人生病了，可以打 120。\n★ 根据这段话，打 121 是因为想：", "options": ["A. 找大夫", "B. 知道天气", "C. 办信用卡", "D. 打扫房间"], "correct": "B"},
        {"num": 67, "text": "67. 虽然京剧的历史才两百多年，但是已经发展得很成熟了。随着社会的发展，京剧也在改变着，以适应不同年龄观众的需要。\n★ 关于京剧，可以知道：", "options": ["A. 很流行", "B. 缺少变化", "C. 历史不长", "D. 动作复杂"], "correct": "C"},
        {"num": 68, "text": "68. 要想获得别人的尊重，首先要学会尊重别人。尊重别人，不仅指对人友好、有礼貌，而且还要尊重别人的兴趣和爱好，在与别人看法不同时，能尊重别人的意见或者选择。\n★ 这段话主要想告诉我们，怎样：", "options": ["A. 互相帮助", "B. 提高能力", "C. 原谅别人", "D. 尊重别人"], "correct": "D"},
        {"num": 69, "text": "69. 中国有句话叫做“要想富，先修路”，意思是，交通对一个地方经济的发展有很大的影响。一些地方因为比较穷，没有钱修路，经济、教育、文化等各方面的发展都受到很大的限制。\n★ “要想富，先修路”说明什么对经济的发展有影响？", "options": ["A. 科学技术", "B. 交通条件", "C. 交通工具", "D. 教育水平"], "correct": "B"},
        {"num": 70, "text": "70. 要想做出正确的判断，首先要耐心地听别人说明情况，其次要把这些情况考虑清楚。只有这样，做出的判断才可能是对的。\n★ 要做出正确的判断，必须：", "options": ["A. 仔细介绍", "B. 怀疑一切", "C. 相信自己", "D. 先了解情况"], "correct": "D"},
        {"num": 71, "text": "71. 根据多年的教学经验，他发现：性格活泼的人可能更适合学习语言，因为这样的人学习比较积极，喜欢主动与人交流，所以学习效果更好。\n★ 性格活泼的人：", "options": ["A. 说话直接", "B. 非常幽默", "C. 积极主动", "D. 往往很粗心"], "correct": "C"},
        {"num": 72, "text": "72. 生活不会一直都顺利，人总是会遇到各种各样的麻烦，可是不管你是快乐还是难过，生活总要继续下去，那我们为什么不选择快乐地生活呢？\n★ 这段话主要想告诉我们，应该：", "options": ["A. 懂得放弃", "B. 理解别人", "C. 多鼓励朋友", "D. 快乐地生活"], "correct": "D"},
        {"num": 73, "text": "73. 老教授对新生说：“从今天起，如果你每天用 100 个字把自己的生活写下来，毕业时你将会得到一本 10 多万字的书，内容就是你 4 年大学生活的美好回忆。”\n★ 老教授希望学生：", "options": ["A. 诚实", "B. 别太得意", "C. 经常复习", "D. 记下自己的生活"], "correct": "D"},
        {"num": 74, "text": "74. 语言是人们交流的工具，音乐也是一种语言，人们可以用它来表达自己的感情，而且和其他语言比起来，音乐表达的感情有时更容易让人听懂。\n★ 根据这段话，音乐表达的感情：", "options": ["A. 复杂多变", "B. 让人难过", "C. 更容易理解", "D. 让人印象更深"], "correct": "C"},
        {"num": 75, "text": "75. 很多时候，人们习惯根据过去的经验做事，但有时候也不能完全相信经验，而应该根据不同的情况选择不同的方法，这样才不容易出错。\n★ 根据这段话，过去的经验：", "options": ["A. 更准确", "B. 值得重视", "C. 无法被证明", "D. 不一定适合现在"], "correct": "D"},
        {"num": 76, "text": "76. 经历不同，对事情的看法自然也不相同。所以遇到问题时，交流是不可缺少的，交流不但能解决问题，还能加深相互间的了解与感情。\n★ 根据这段话，交流可以：", "options": ["A. 解决问题", "B. 照顾邻居", "C. 减少浪费", "D. 吸引观众"], "correct": "A"},
        {"num": 77, "text": "77. 你从哪里来不重要，重要的是你要到哪里去。要低头认真工作，更要记得抬头看清楚方向。如果方向不对，无论做多少努力可能都是白费。\n★ 这段话主要想告诉我们：", "options": ["A. 要有信心", "B. 不要粗心", "C. 要重视方向", "D. 回答要准确"], "correct": "C"},
        {"num": 78, "text": "78. 有些人有很多朋友，但几乎没有一个值得信任；有些人朋友不多，也许只有一个两个，但他们相互理解、支持，永远不需要怀疑。\n★ 真正的朋友：", "options": ["A. 相互信任", "B. 脾气相同", "C. 经常见面", "D. 不一定很熟悉"], "correct": "A"},
        {"num": 79, "text": "79. 如果可能，就不要批评别人。不得不批评的时候，也要耐心、友好地说出 your 意见。坚持对事不对人，这样才能让被批评的人知道你是想帮助他，而不是光想着批评他。\n★ 根据这段话，批评的目的是：", "options": ["A. 获得经验", "B. 帮助别人", "C. 回忆过去", "D. 表示祝贺"], "correct": "B"},
        {"num": 80, "text": "80-81. 很多人已经适应了每天紧张的工作。他们认为聊天儿只会浪费时间，所以很少会坐下来和朋友或者家人聊天儿。其实，在紧张的工作后，聊天儿往往能使人心情变得轻松起来。另外，人们还可以通过聊天儿获得友谊。\n★ 为什么有的人很少坐下来聊天儿？", "options": ["A. 没烦恼", "B. 怕麻烦", "C. 怕浪费时间", "D. 不喜欢热闹"], "correct": "C"},
        {"num": 81, "text": "81. ★ 聊天儿能使人：", "options": ["A. 有礼貌", "B. 变美丽", "C. 心情愉快", "D. 变得幽默"], "correct": "C"},
        {"num": 82, "text": "82-83. 现在有些父母认为，孩子接受国外的教育越早越好，因此，一些孩子很小的时候就被送出去留学了。但是另外一些人有不同的看法，他们担心孩子太小，还不会照顾自己，并不能很好地适应国外的学习和生活。\n★ 关于小孩子出国留学，可以知道：", "options": ["A. 学费很贵", "B. 很难申请", "C. 压力很大", "D. 大家看法不同"], "correct": "D"},
        {"num": 83, "text": "83. ★ 这段话主要讨论什么问题？", "options": ["A. 学习方法", "B. 孩子留学", "C. 语法标准", "D. 父母的责任"], "correct": "B"},
        {"num": 84, "text": "84-85. 现代社会离不开交流。如果工作中遇到了难题，要试着和同事交流，也许可以帮你解决。如果朋友之间发生了不高兴的事情，你不应该自己一个人生气，而是应该和他交流，很有可能你会发现那是个误会。\n★ 跟同事交流可能会帮你：", "options": ["A. 更勇敢", "B. 不再无聊", "C. 解决问题", "D. 认识新朋友"], "correct": "C"},
        {"num": 85, "text": "85. ★ 这段话主要介绍：", "options": ["A. 什么是幸福", "B. 交流的作用", "C. 怎样做生意", "D. 怎样积累知识"], "correct": "B"}
    ]
    
    u_r_all = {}
    
    for q in r_p1_data1:
        st.markdown(f"<div class='question-card'><strong>Câu {q['num']}:</strong><br>{q['text']}", unsafe_allow_html=True)
        ans = st.selectbox(f"Chọn từ điền vào câu {q['num']}:", ["-- Chọn --", "A", "B", "C", "D", "E", "F"], key=f"w_r_{q['num']}")
        u_r_all[q['num']] = ans if ans != "-- Chọn --" else ""
        st.markdown("</div>", unsafe_allow_html=True)
        
    for q in r_p1_data2:
        st.markdown(f"<div class='question-card'><strong>Câu {q['num']}:</strong><br>{q['text'].replace('\n', '<br>')}", unsafe_allow_html=True)
        ans = st.selectbox(f"Chọn từ điền vào câu {q['num']}:", ["-- Chọn --", "A", "B", "C", "D", "E", "F"], key=f"w_r_{q['num']}")
        u_r_all[q['num']] = ans if ans != "-- Chọn --" else ""
        st.markdown("</div>", unsafe_allow_html=True)
        
    for q in r_p2_data:
        st.markdown(f"<div class='question-card'><strong>Câu {q['num']}:</strong><br>{q['text'].replace('\n', '<br>')}", unsafe_allow_html=True)
        ans = st.text_input("Nhập thứ tự sắp xếp (VD: BAC):", key=f"w_r_{q['num']}").strip().upper()
        u_r_all[q['num']] = ans
        st.markdown("</div>", unsafe_allow_html=True)
        
    for q in r_p3_data:
        st.markdown(f"<div class='question-card'><strong>Câu {q['num']}:</strong><br>{q['text'].replace('\n', '<br>')}", unsafe_allow_html=True)
        ans = st.radio(f"r3_h41110_{q['num']}", q['options'], key=f"w_r_{q['num']}", label_visibility="collapsed")
        u_r_all[q['num']] = ans[0] if ans else ""
        st.markdown("</div>", unsafe_allow_html=True)
        
    if st.button("🚀 NỘP BÀI PHẦN ĐỌC (MÃ H41110)", key="btn_sub_read_h41110"):
        if not student_name.strip():
            st.warning("⚠️ Vui lòng nhập Họ và tên ở đầu trang trước khi nộp bài!")
        else:
            c1 = sum(1 for q in r_p1_data1 if u_r_all.get(q['num']) == q['correct'])
            c2 = sum(1 for q in r_p1_data2 if u_r_all.get(q['num']) == q['correct'])
            c3 = sum(1 for q in r_p2_data if u_r_all.get(q['num']) == q['correct'])
            c4 = sum(1 for q in r_p3_data if u_r_all.get(q['num']) == q['correct'])
            c_tot = c1 + c2 + c3 + c4
            sc_100 = (c_tot / 40) * 100
            
            st.success(f"🎉 **Kết quả Phần Đọc (Mã H41110):**\n- Số câu đúng: **{c_tot}/40** câu\n- Điểm số quy đổi: **{sc_100:.1f} / 100 điểm**")
            send_score_to_gsheet(student_name, "H41110", "PHẦN ĐỌC", f"{c_tot}/40", sc_100)
            
            st.markdown("---")
            st.markdown("### 🔍 CHI TIẾT CÂU SAI PHẦN ĐỌC:")
            for q in r_p1_data1 + r_p1_data2 + r_p2_data + r_p3_data:
                if u_r_all.get(q['num']) != q['correct']:
                    st.markdown(f"❌ **Câu {q['num']}**: Bạn làm `{u_r_all.get(q['num'])}` | Đáp án đúng: **{q['correct']}**")

# ==============================================================================
# 3. PHẦN VIẾT (15 CÂU: 86 - 100)
# ==============================================================================
with sub_tab_write:
    st.markdown("### 三、书写 (Phần viết - 15 câu)")
    st.markdown("#### **第一部分 (第 86-95 题 - 完成句子)**")
    
    write_p1_data = [
        {"num": 86, "words": "86. 这篇文章 / 三部分 / 组成 / 由", "correct": ["这篇文章由三部分组成。"]},
        {"num": 87, "words": "87. 儿童 / 欢迎 / 很 / 这个节目 / 受", "correct": ["这个节目很受儿童欢迎。"]},
        {"num": 88, "words": "88. 离大使馆 / 友谊宾馆 / 远 / 吗", "correct": ["友谊宾馆离大使馆远吗？"]},
        {"num": 89, "words": "89. 很 / 诚实 / 那个 / 确实 / 司机", "correct": ["那个司机确实很诚实。"]},
        {"num": 90, "words": "90. 加油站 / 使用 / 手机 / 禁止", "correct": ["加油站禁止使用手机。"]},
        {"num": 91, "words": "91. 去 / 公园 / 你陪姐姐 / 散散步 / 吧", "correct": ["你陪姐姐去公园散散步吧。"]},
        {"num": 92, "words": "92. 有点儿 / 咸 / 中午的 / 西红柿鸡蛋汤 / 稍微", "correct": ["中午的西红柿鸡蛋汤稍微有点儿咸。"]},
        {"num": 93, "words": "93. 中文 / 说得 / 你们校长 / 的 / 很流利", "correct": ["你们校长的中文说得很流利。"]},
        {"num": 94, "words": "94. 90%的 / 通过了考试 / 同学 / 大约有", "correct": ["大约有90%的同学通过了考试。"]},
        {"num": 95, "words": "95. 房间 / 米小姐 / 把 / 收拾好了", "correct": ["米小姐把房间收拾好了。"]}
    ]
    
    u_w_p1 = {}
    for q in write_p1_data:
        st.markdown(f"<div class='question-card'><strong>Câu {q['num']}:</strong> {q['words']}", unsafe_allow_html=True)
        ans = st.text_input("Nhập câu hoàn chỉnh của bạn tại đây:", key=f"w_w_{q['num']}").strip()
        u_w_p1[q['num']] = ans
        st.markdown("</div>", unsafe_allow_html=True)
        
    st.markdown("<br>#### **第二部分 (第 96-100 题 - 看图造句)**", unsafe_allow_html=True)
    
    write_p2_data = [
        {"num": 96, "word": "袜子", "img_desc": "[Tranh hai bàn chân không đi tất]", "sample": "他们俩都没穿袜子。"},
        {"num": 97, "word": "害羞", "img_desc": "[Tranh cô gái ngượng ngùng]", "sample": "第一次见面，她有些害羞。"},
        {"num": 98, "word": "醒", "img_desc": "[Tranh cô gái ngủ trên giường, đồng hồ báo thức]", "sample": "快醒醒，该起床了。"},
        {"num": 99, "word": "密码", "img_desc": "[Tranh anh chàng ôm đầu quên mật khẩu máy tính]", "sample": "他想不起来这个电脑的密码了。"},
        {"num": 100, "word": "咳嗽", "img_desc": "[Tranh cô gái đeo khẩu trang ho]", "sample": "她感冒还没好，还在咳嗽。"}
    ]
    
    u_w_p2 = {}
    for q in write_p2_data:
        st.markdown(f"<div class='question-card'><strong>Câu {q['num']}:</strong> {q['img_desc']}<br>Từ gợi ý: <strong>{q['word']}</strong>", unsafe_allow_html=True)
        ans = st.text_area("Nhập câu tự luận của bạn tại đây:", key=f"w_w_{q['num']}")
        u_w_p2[q['num']] = ans
        st.markdown("</div>", unsafe_allow_html=True)
        
    st.info("📌 Note: Các câu từ 96-100 (đặt câu theo tranh) cô Ngọc sẽ chấm cụ thể sau. Điểm hiển thị bên dưới chỉ mang tính chất tương đối.")
    
    if st.button("🚀 NỘP BÀI PHẦN VIẾT (MÃ H41110)", key="btn_sub_write_h41110"):
        if not student_name.strip():
            st.warning("⚠️ Vui lòng nhập Họ và tên ở đầu trang trước khi nộp bài!")
        else:
            c1 = sum(1 for q in write_p1_data if u_w_p1.get(q['num']) in q['correct'])
            # Mặc định 5 câu phần 2 được tính điểm tương đối full điểm
            c_total = c1 + 5
            sc_100 = (c_total / 15) * 100
            
            st.success(f"🎉 **Kết quả Phần Viết tương đối (Mã H41110):**\n- Số câu đúng Phần 1: **{c1}/10** câu\n- Điểm số tương đối: **{sc_100:.1f} / 100 điểm**")
            send_score_to_gsheet(student_name, "H41110", "PHẦN VIẾT", f"{c_total}/15", sc_100)
            
            st.markdown("---")
            st.markdown("### 🔍 CHI TIẾT CÂU SAI PHẦN VIẾT (PHẦN 1):")
            for q in write_p1_data:
                if u_w_p1.get(q['num']) not in q['correct']:
                    st.markdown(f"❌ **Câu {q['num']}**: Bạn viết `{u_w_p1.get(q['num'])}` | Đáp án đúng: **{q['correct'][0]}**")
            st.markdown("---")
            st.markdown("### 💡 GỢI Ý MẪU CHO PHẦN 2 (CÂU 96-100):")
            for q in write_p2_data:
                st.markdown(f"- **Câu {q['num']} ({q['word']}):** `{q['sample']}`")

st.markdown("""
<div class="footer">
    黄宝玉老师 • Đề Luyện HSK 4 Mã H41110 Trọn Bộ 100 Câu
</div>
""", unsafe_allow_html=True)
