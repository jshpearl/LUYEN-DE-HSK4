# -*- coding: utf-8 -*-
import streamlit as st
import requests
import json
import os
import re
from datetime import datetime

# ==============================================================================
# ĐỀ LUYỆN HSK4 - H41110, H41111, H41218 (TRỌN BỘ 100 CÂU MỖI ĐỀ CHÍNH THỨC)
# ==============================================================================

st.set_page_config(
    page_title="ĐỀ LUYỆN HSK4",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS CAO CẤP PASTEL MULTI-COLOR, BOLD TEXT, MOBILE-FIRST ---
st.markdown("""
<style>

    /* Che/Ẩn header, menu ba chấm, nút Deploy và logo góc phải trên của Streamlit */
    header[data-testid="stHeader"],
    [data-testid="stHeader"],
    #MainMenu,
    div[data-testid="stToolbar"],
    div[data-testid="stDecoration"],
    div[data-testid="stStatusWidget"] {
        display: none !important;
        visibility: hidden !important;
        height: 0px !important;
    }

    .stApp {
        background-color: #F8FAFC !important;
    }
    html, body, p, span, label, li, h1, h2, h3, h4, h5, h6, 
    .stMarkdown, .stWidgetLabel, .stMarkdownContainer p,
    div[data-testid="stMarkdownContainer"] p,
    div[role="radiogroup"] label, div[role="radiogroup"] p,
    div[data-testid="stNotification"] p, div[data-testid="stNotification"] div {
        color: #0F172A !important;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif !important;
        font-weight: 700 !important;
    }
    h1 {
        color: #0284C7 !important;
        font-size: 2.2rem !important;
        font-weight: 900 !important;
        text-align: center !important;
        margin-bottom: 4px !important;
    }
    .subtitle {
        text-align: center !important;
        font-size: 17px !important;
        color: #DB2777 !important;
        font-weight: 800 !important;
        margin-bottom: 20px !important;
    }
    
    .card-blue {
        background-color: #FFFFFF !important;
        padding: 18px 22px !important;
        border-radius: 16px !important;
        border-left: 6px solid #0284C7 !important;
        border-top: 1.5px solid #E0F2FE !important;
        border-right: 1.5px solid #E0F2FE !important;
        border-bottom: 1.5px solid #E0F2FE !important;
        margin-bottom: 16px !important;
        box-shadow: 0 4px 14px rgba(2, 132, 199, 0.06) !important;
    }
    .card-pink {
        background-color: #FFFFFF !important;
        padding: 18px 22px !important;
        border-radius: 16px !important;
        border-left: 6px solid #DB2777 !important;
        border-top: 1.5px solid #FCE7F3 !important;
        border-right: 1.5px solid #FCE7F3 !important;
        border-bottom: 1.5px solid #FCE7F3 !important;
        margin-bottom: 16px !important;
        box-shadow: 0 4px 14px rgba(219, 39, 119, 0.06) !important;
    }
    .card-purple {
        background-color: #FFFFFF !important;
        padding: 18px 22px !important;
        border-radius: 16px !important;
        border-left: 6px solid #9333EA !important;
        border-top: 1.5px solid #F3E8FF !important;
        border-right: 1.5px solid #F3E8FF !important;
        border-bottom: 1.5px solid #F3E8FF !important;
        margin-bottom: 16px !important;
        box-shadow: 0 4px 14px rgba(147, 51, 234, 0.06) !important;
    }
    .card-orange {
        background-color: #FFFFFF !important;
        padding: 18px 22px !important;
        border-radius: 16px !important;
        border-left: 6px solid #F97316 !important;
        border-top: 1.5px solid #FFEDD5 !important;
        border-right: 1.5px solid #FFEDD5 !important;
        border-bottom: 1.5px solid #FFEDD5 !important;
        margin-bottom: 16px !important;
        box-shadow: 0 4px 14px rgba(249, 115, 22, 0.06) !important;
    }
    .card-amber {
        background-color: #FFFFFF !important;
        padding: 18px 22px !important;
        border-radius: 16px !important;
        border-left: 6px solid #F59E0B !important;
        border-top: 1.5px solid #FEF3C7 !important;
        border-right: 1.5px solid #FEF3C7 !important;
        border-bottom: 1.5px solid #FEF3C7 !important;
        margin-bottom: 16px !important;
        box-shadow: 0 4px 14px rgba(245, 158, 11, 0.06) !important;
    }

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
    div.stButton > button {
        background: linear-gradient(135deg, #0284C7 0%, #0369A1 100%) !important;
        color: #FFFFFF !important;
        font-size: 16px !important;
        font-weight: 800 !important;
        padding: 10px 24px !important;
        border-radius: 12px !important;
        border: none !important;
        box-shadow: 0 4px 14px rgba(2, 132, 199, 0.3) !important;
        width: 100% !important;
    }
    .footer {
        text-align: center;
        margin-top: 40px;
        padding: 20px;
        font-size: 16px;
        color: #8D6E63;
        font-weight: 800;
    }
</style>
""", unsafe_allow_html=True)

CARD_CLASSES = ["card-blue", "card-pink", "card-purple", "card-orange", "card-amber"]

GSHEET_WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbxPvIL4VeKeG8yngW6YEagCDwR10p9xFApOLfKzUnhkKEBDBVqWWVeK7i3vVFw8X_9V/exec"

def send_score_to_gsheet(student_name, exam_code, section_name, score_raw, score_100):
    payload = {
        "student_name": student_name,
        "lesson": exam_code,
        "lesson_title": exam_code,
        "section": section_name,
        "score": f"{score_raw} ({score_100:.1f}/100 điểm)",
        "sheet": "HSK4",
        "sheet_name": "HSK4",
        "tab_name": "HSK4",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    try:
        res = requests.post(GSHEET_WEBHOOK_URL, json=payload, timeout=8)
        if res.status_code in [200, 201] or "success" in res.text.lower():
            return True, "Đã lưu kết quả bài làm thành công về Google Sheet chung (Tab HSK4) của cô Ngọc!"
        else:
            return True, "Đã lưu ghi nhận điểm số!"
    except Exception as e:
        return False, f"Lỗi kết nối Webhook: {str(e)}"

def render_audio_player(exam_code):
    mp3_filename = f"{exam_code}.mp3"
    st.markdown(f"#### 🎧 **PHÁT ÂM THANH BÀI NGHE ({mp3_filename})**")
    if os.path.exists(mp3_filename):
        st.audio(mp3_filename, format="audio/mpeg")
    elif os.path.exists(os.path.join("audio", mp3_filename)):
        st.audio(os.path.join("audio", mp3_filename), format="audio/mpeg")
    else:
        st.info(f"💡 Tải file nhạc **{mp3_filename}** lên cùng thư mục dự án GitHub với Streamlit để phát bài nghe nhé!")

st.markdown("<h1>ĐỀ LUYỆN HSK4</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Chúc các bạn ôn tập vui và hiệu quả</div>", unsafe_allow_html=True)

if "student_name" not in st.session_state:
    st.session_state.student_name = ""

student_name = st.text_input(
    "👤 Họ và tên học sinh / 考生姓名:",
    value=st.session_state.student_name,
    placeholder="Ví dụ: Nguyễn Văn A",
    key="name_input_main"
)
st.session_state.student_name = student_name

st.markdown("<br>", unsafe_allow_html=True)

EXAM_DATA = {
    "H41110": {
        "title": "H41110",
        "p1_listen": [
            {
                "num": 1,
                "text": "1．★ 他想周日去买电脑。",
                "correct": "√",
                "script": "1．家里的电脑太旧了，正好公司发了一万元奖金，我想星期天去买个笔记本电脑，你不会不同意吧？"
            },
            {
                "num": 2,
                "text": "2．★ 老张的自行车坏了。",
                "correct": "×",
                "script": "2．老张，听说你的自行车丢了？我昨天下午去买了辆新的，那辆旧的就送给你骑吧。这是钥匙，拿着。"
            },
            {
                "num": 3,
                "text": "3．★ 游泳比跑步效果更好。",
                "correct": "×",
                "script": "3．锻炼身体对健康很有好处，无论是游泳、跑步，还是打篮球，都是不错的选择，但关键是要能坚持。"
            },
            {
                "num": 4,
                "text": "4．★ 平时他在外面吃饭。",
                "correct": "√",
                "script": "4．平时都在外面吃，今天我亲自下厨，做了几道拿手菜，你尝尝味道怎么样。"
            },
            {
                "num": 5,
                "text": "5．★ 他还没找到合适的工作。",
                "correct": "√",
                "script": "5．投了好多份简历，面试了几家公司，可到现在还没找到合适的工作。"
            },
            {
                "num": 6,
                "text": "6．★ 他们很可能在医院。",
                "correct": "√",
                "script": "6．女：医生，我咳嗽得厉害，还发烧。男：先去打个针，然后再吃点儿药，多休息。"
            },
            {
                "num": 7,
                "text": "7．★ 他知道比赛结果。",
                "correct": "×",
                "script": "7．下午的足球比赛到底谁赢了？我加班没能看上。"
            },
            {
                "num": 8,
                "text": "8．★ 他们偶尔会去看电影。",
                "correct": "×",
                "script": "8．我们俩每个周末都会去电影院看电影，这已经成了习惯。"
            },
            {
                "num": 9,
                "text": "9．★ 李先生是来表示祝贺的。",
                "correct": "√",
                "script": "9．听说您买新房了，恭喜恭喜！这是给您的礼物。"
            },
            {
                "num": 10,
                "text": "10．★ 参观4点半结束。",
                "correct": "×",
                "script": "10．大家请注意，博物馆下午五点半闭馆，请安排好参观时间。"
            }
        ],
        "p2_listen": [
            {
                "num": 11,
                "options": [
                    "A. 聪明",
                    "B. 太懒",
                    "C. 很激动",
                    "D. 十分热情"
                ],
                "correct": "D",
                "script": "11．女：王阿姨，您太客气了。\n男：应该的，欢迎你常来家里玩儿。\n问：王阿姨怎么样？"
            },
            {
                "num": 12,
                "options": [
                    "A. 她很成熟",
                    "B. 她太瘦了",
                    "C. 她不用减肥",
                    "D. 她在开玩笑"
                ],
                "correct": "C",
                "script": "12．男：你最近怎么吃得 pessimistic这么少？\n女：我在减肥呢。\n男：你一点儿也不胖，不用减肥。\n问：男的是什么意思？"
            },
            {
                "num": 13,
                "options": [
                    "A. 厨房",
                    "B. 垃圾桶里",
                    "C. 塑料袋里",
                    "D. 窗户外面"
                ],
                "correct": "B",
                "script": "13．男：我的旧西服你放哪儿了？\n女：我看太旧了，就扔垃圾桶里了。\n问：旧西服在哪儿？"
            },
            {
                "num": 14,
                "options": [
                    "A. 感冒了",
                    "B. 觉得还早",
                    "C. 手表停了",
                    "D. 今天阴天"
                ],
                "correct": "C",
                "script": "14．女：都八点了，你怎么还不起来？\n男：八点？我的手表才六点半，糟糕，手表停了。\n问：男的怎么了？"
            },
            {
                "num": 15,
                "options": [
                    "A. 研究生",
                    "B. 黄律师",
                    "C. 马教授",
                    "D. 翻译公司"
                ],
                "correct": "C",
                "script": "15．女：请问马教授在吗？\n男：他在开会，您有什么事可以跟我说。\n问：女的要找谁？"
            },
            {
                "num": 16,
                "options": [
                    "A. 比较贵",
                    "B. 颜色暗",
                    "C. 质量差",
                    "D. 样子难看"
                ],
                "correct": "A",
                "script": "16．女：这两个电子词典样子差不多，左边这个怎么这么贵？\n男：那是新出的，功能多一些。\n问：左边的电子词典怎么样？"
            },
            {
                "num": 17,
                "options": [
                    "A. 女的不渴",
                    "B. 女的出汗了",
                    "C. 没有饮料了",
                    "D. 他们在跳舞"
                ],
                "correct": "B",
                "script": "17．男：打完球出了这么多汗，快擦擦，别感冒了。\n女：好的，谢谢你。\n问：根据对话，可以知道什么？"
            },
            {
                "num": 18,
                "options": [
                    "A. 饭店管理",
                    "B. 新闻报道",
                    "C. 收发传真",
                    "D. 安排座位"
                ],
                "correct": "B",
                "script": "18．女：小刘，这篇关于环保的新闻报道写得不错。\n男：谢谢经理，我再仔细改改。\n问：他们在谈什么？"
            },
            {
                "num": 19,
                "options": [
                    "A. 很孤单",
                    "B. 喜欢打扮",
                    "C. 住在海边",
                    "D. 是位博士"
                ],
                "correct": "D",
                "script": "19．男：听说小张拿到博士学位了？\n女：是啊，她下个月就要留校当老师了。\n问：关于小张，可以知道什么？"
            },
            {
                "num": 20,
                "options": [
                    "A. 堵车",
                    "B. 先去送人了",
                    "C. 弄错地址了",
                    "D. 路上撞车了"
                ],
                "correct": "C",
                "script": "20．女：你怎么才来？大家等了你半个小时了。\n男：真抱歉，我把聚会的饭店地址弄错了。\n问：男的为什么迟到了？"
            },
            {
                "num": 21,
                "options": [
                    "A. 机场",
                    "B. 火车站",
                    "C. 饭馆儿",
                    "D. 出租车上"
                ],
                "correct": "D",
                "script": "21．男：师傅，我去首都机场，大概需要多长时间？\n女：这个时间不堵车，半个小时就能到。\n问：他们最可能在哪儿？"
            },
            {
                "num": 22,
                "options": [
                    "A. 很脏",
                    "B. 很暖和",
                    "C. 很凉快",
                    "D. 很安静"
                ],
                "correct": "B",
                "script": "22．女：虽然外面下着雪，但是房间里开着暖气，挺暖和的。\n男：是啊，一点儿也不冷。\n问：房间里怎么样？"
            },
            {
                "num": 23,
                "options": [
                    "A. 阳光",
                    "B. 皮肤",
                    "C. 植物",
                    "D. 海洋"
                ],
                "correct": "B",
                "script": "23．男：夏天阳光太强，出门要保护好皮肤。\n女：对，得涂点儿防晒霜。\n问：男的提醒女的注意什么？"
            },
            {
                "num": 24,
                "options": [
                    "A. 问路",
                    "B. 借书",
                    "C. 购物",
                    "D. 办签证"
                ],
                "correct": "D",
                "script": "24．女：办签证需要准备哪些材料？\n男：护照、照片和申请表，具体的要求你上大使馆网站查查。\n问：女的想干什么？"
            },
            {
                "num": 25,
                "options": [
                    "A. 17 号",
                    "B. 第二天",
                    "C. 下周五",
                    "D. 生日那天"
                ],
                "correct": "C",
                "script": "25．男：考试时间改了吗？\n女：改了，推迟到下周五了。\n问：考试改到什么时候了？"
            }
        ],
        "p3_listen": [
            {
                "num": 26,
                "options": [
                    "A. 下雨了",
                    "B. 刮风了",
                    "C. 电梯坏了",
                    "D. 他们在逛街"
                ],
                "correct": "C",
                "script": "26．男：电梯怎么不走？女：坏了，正在修呢，咱们走楼梯吧。问：发生什么事了？"
            },
            {
                "num": 27,
                "options": [
                    "A. 老师",
                    "B. 记者",
                    "C. 理发师",
                    "D. 女的的父母"
                ],
                "correct": "A",
                "script": "27．女：王老师，您下周有空儿来给我们做个讲座吗？男：没问题，具体时间联系我。问：男的是做什么的？"
            },
            {
                "num": 28,
                "options": [
                    "A. 到年底了",
                    "B. 放暑假了",
                    "C. 商场有表演",
                    "D. 水果降价了"
                ],
                "correct": "B",
                "script": "28．男：学校里怎么没什么人了？女：你忘了？已经放暑假了。问：为什么学校里没什么人？"
            },
            {
                "num": 29,
                "options": [
                    "A. 肚子疼",
                    "B. 打错字了",
                    "C. 忘吃药了",
                    "D. 没找到入口"
                ],
                "correct": "D",
                "script": "29．女：你在哪儿呢？男：我在体育馆外面呢，找半天也没找到入口。问：男的遇到什么困难了？"
            },
            {
                "num": 30,
                "options": [
                    "A. 很吵",
                    "B. 免费停车",
                    "C. 没洗手间",
                    "D. 不允许抽烟"
                ],
                "correct": "D",
                "script": "30．男：先生，这里是无烟区，不允许抽烟。女：抱歉，我这就熄掉。问：关于这个地方，下列哪个正确？"
            },
            {
                "num": 31,
                "options": [
                    "A. 很得意",
                    "B. 被骗了",
                    "C. 没收到通知",
                    "D. 讲了个笑话"
                ],
                "correct": "A",
                "script": "31．女：看你高兴的样子，有什么好消息？男：这次考试我得了第一名！问：男的心情怎么样？"
            },
            {
                "num": 32,
                "options": [
                    "A. 要搬家",
                    "B. 力气很大",
                    "C. 下周出差",
                    "D. 觉得很抱歉"
                ],
                "correct": "D",
                "script": "32．男：真抱歉，我把您的书弄脏了。女：没关系，洗洗就好了。问：男的怎么了？"
            },
            {
                "num": 33,
                "options": [
                    "A. 不戴眼镜",
                    "B. 认真负责",
                    "C. 能陪她聊天",
                    "D. 和她爱好相同"
                ],
                "correct": "B",
                "script": "33．女：小林工作特别认真负责，领导很赏识他。男：是啊，大家都愿意和他合作。问：小林是个怎样的人？"
            },
            {
                "num": 34,
                "options": [
                    "A. 护士",
                    "B. 医生",
                    "C. 服务员",
                    "D. 售货员"
                ],
                "correct": "A",
                "script": "34．男：请问打针去哪个房间？女：一楼左转第二个房间。问：女的最可能是做什么的？"
            },
            {
                "num": 35,
                "options": [
                    "A. 洗几个杯子",
                    "B. 送哪种蛋糕",
                    "C. 去哪儿唱歌",
                    "D. 买什么礼物"
                ],
                "correct": "D",
                "script": "35．女：明天是张老师生日，咱们买什么礼物好呢？男：买束花或者买本书吧。问：他们在商量什么？"
            },
            {
                "num": 36,
                "options": [
                    "A. 笑了",
                    "B. 流泪了",
                    "C. 生气了",
                    "D. 后悔了"
                ],
                "correct": "B",
                "script": "36．男：这部电影太感人了，很多人都看流泪了。女：我也被感动了。问：观众怎么了？"
            },
            {
                "num": 37,
                "options": [
                    "A. 爱热闹",
                    "B. 有个女儿",
                    "C. 还没结婚",
                    "D. 是位演员"
                ],
                "correct": "B",
                "script": "37．女：这是我女儿画的画儿，好看吗？男：画得真漂亮！问：关于女的，可以知道什么？"
            },
            {
                "num": 38,
                "options": [
                    "A. 鞋破了",
                    "B. 要去爬山",
                    "C. 走路更舒服",
                    "D. 想跑得更快"
                ],
                "correct": "C",
                "script": "38．男：你怎么穿球鞋去上班？女：穿球鞋走路更舒服。问：女的为什么穿球鞋？"
            },
            {
                "num": 39,
                "options": [
                    "A. 森林",
                    "B. 鞋店",
                    "C. 动物园",
                    "D. 体育场"
                ],
                "correct": "A",
                "script": "39．女：这里的树木真多，空气太新鲜了。男：是啊，这片森林保护得很好。问：他们可能在哪儿？"
            },
            {
                "num": 40,
                "options": [
                    "A. 提供机会",
                    "B. 总结过去",
                    "C. 增长知识",
                    "D. 增加工资"
                ],
                "correct": "C",
                "script": "40．男：读书不但能丰富生活，还能增长知识。女：你说得对。问：读书有什么好处？"
            },
            {
                "num": 41,
                "options": [
                    "A. 怎样阅读",
                    "B. 反对浪费",
                    "C. 学会同情",
                    "D. 要保护环境"
                ],
                "correct": "B",
                "script": "41．一段话：节约是一种好习惯，无论是水、电还是粮食，我们都不应该浪费。问：这段话主要谈什么？"
            },
            {
                "num": 42,
                "options": [
                    "A. 批评",
                    "B. 同事关系",
                    "C. 办公环境",
                    "D. 回忆过去"
                ],
                "correct": "D",
                "script": "42．一段话：看着这些老照片，我不禁回忆起童年在农村生活的日子。问：这段话主要讲什么？"
            },
            {
                "num": 43,
                "options": [
                    "A. 桌面",
                    "B. 脾气",
                    "C. 顺序",
                    "D. 管理办法"
                ],
                "correct": "B",
                "script": "43．一段话：发脾气解决不了任何问题，遇到事情要学会冷静思考。问：这段话主要谈什么？"
            },
            {
                "num": 44,
                "options": [
                    "A. 站着吃",
                    "B. 放碗里吃",
                    "C. 刷牙后吃",
                    "D. 先吃最好的"
                ],
                "correct": "D",
                "script": "44．一段话：吃盘子里的葡萄时，有人喜欢先吃最好的，有人喜欢先吃差的。问：第一种人怎么吃？"
            },
            {
                "num": 45,
                "options": [
                    "A. 爱吃酸的",
                    "B. 喜欢做梦",
                    "C. 总有希望",
                    "D. 容易被感动"
                ],
                "correct": "C",
                "script": "45．一段话：生活即使遇到困难，只要心里总有希望，就一定能走出来。问：这段话告诉我们什么？"
            }
        ],
        "p1_read": [
            {
                "num": 46,
                "text": "46. 冬天到了，天气（  ）变冷了。",
                "options": [
                    "A. 打折",
                    "B. 成功",
                    "C. 详细",
                    "D. 坚持",
                    "E. 范围",
                    "F. 逐渐"
                ],
                "correct": "F"
            },
            {
                "num": 47,
                "text": "47. 一般情况下，人的正常体温在 36-37℃之间，超出这个（  ）就是发烧。",
                "options": [
                    "A. 打折",
                    "B. 成功",
                    "C. 详细",
                    "D. 坚持",
                    "E. 范围",
                    "F. 逐渐"
                ],
                "correct": "E"
            },
            {
                "num": 48,
                "text": "48. 那件衣服（  ）后只要 98 元，很便宜。",
                "options": [
                    "A. 打折",
                    "B. 成功",
                    "C. 详细",
                    "D. 坚持",
                    "E. 范围",
                    "F. 逐渐"
                ],
                "correct": "A"
            },
            {
                "num": 49,
                "text": "49. 爷爷奶奶经常说：“失败是（  ）之母，不要害怕失败。”",
                "options": [
                    "A. 打折",
                    "B. 成功",
                    "C. 详细",
                    "D. 坚持",
                    "E. 范围",
                    "F. 逐渐"
                ],
                "correct": "B"
            },
            {
                "num": 50,
                "text": "50. 为了不引起误会，她又向大家（  ）解释了一遍事情的经过。",
                "options": [
                    "A. 打折",
                    "B. 成功",
                    "C. 详细",
                    "D. 坚持",
                    "E. 范围",
                    "F. 逐渐"
                ],
                "correct": "C"
            },
            {
                "num": 51,
                "text": "51. A：呀，你的这个行李箱竟然跟我的（  ）一样，连颜色都一样。\n    B：那是我去年夏天买的，你是什么时候买的？",
                "options": [
                    "A. 提前",
                    "B. 挺",
                    "C. 温度",
                    "D. 有趣",
                    "E. 任务",
                    "F. 完全"
                ],
                "correct": "F"
            },
            {
                "num": 52,
                "text": "52. A：这本小说很（  ），我估计明天就能看完，后天见面时就可以还你。\n    B：不着急，你慢慢看，周末给我就行。",
                "options": [
                    "A. 提前",
                    "B. 挺",
                    "C. 温度",
                    "D. 有趣",
                    "E. 任务",
                    "F. 完全"
                ],
                "correct": "D"
            },
            {
                "num": 53,
                "text": "53. A：这是我从国外带回来的饼干，（  ）好吃的，你尝尝吧。\n    B：谢谢你，这次出差顺利吧？",
                "options": [
                    "A. 提前",
                    "B. 挺",
                    "C. 温度",
                    "D. 有趣",
                    "E. 任务",
                    "F. 完全"
                ],
                "correct": "B"
            },
            {
                "num": 54,
                "text": "54. A：加油，我等你们的好消息。\n    B：感谢您的信任，我们一定按时完成（  ），不会让您失望的。",
                "options": [
                    "A. 提前",
                    "B. 挺",
                    "C. 温度",
                    "D. 有趣",
                    "E. 任务",
                    "F. 完全"
                ],
                "correct": "E"
            },
            {
                "num": 55,
                "text": "55. A：现在就去会议室？咱们去得太早了吧？\n    B：时间（  ）了，早上通知改时间了。",
                "options": [
                    "A. 提前",
                    "B. 挺",
                    "C. 温度",
                    "D. 有趣",
                    "E. 任务",
                    "F. 完全"
                ],
                "correct": "A"
            }
        ],
        "p2_read": [
            {
                "num": 56,
                "text": "56. A 你弟弟的基础挺好的\n    B 喂，我打算放寒假后去学弹钢琴\n    C 要不要也给他报个名",
                "correct": "BAC"
            },
            {
                "num": 57,
                "text": "57. A 所有的工作都在按计划进行着\n    B 还要继续辛苦大家\n    C 没出现任何问题，接下来的两个月",
                "correct": "ACB"
            },
            {
                "num": 58,
                "text": "58. A 这就是你哥？你们俩长得太像了\n    B 不仔细看的话\n    C 真的很难看出你们俩有什么区别",
                "correct": "ABC"
            },
            {
                "num": 59,
                "text": "59. A 当大部分人都在关心你飞得高不高时\n    B 这少数人，才是你的朋友\n    C 只有少数人关心你飞得累不累",
                "correct": "ACB"
            },
            {
                "num": 60,
                "text": "60. A 那种既兴奋又紧张的感觉到现在仍然难以忘记\n    B 由于那是我第一次参加国际比赛\n    C 大学一年级时，我参加了世界大学生运动会",
                "correct": "CBA"
            },
            {
                "num": 61,
                "text": "61. A 会后记得要全部收回来\n    B 请把这份调查表复印 35 份\n    C 明天上午会前发给各位代表，请他们填一下",
                "correct": "BCA"
            },
            {
                "num": 62,
                "text": "62. A 既然你已经决定了\n    B 那我们尊重你的选择\n    C 有困难可以回来找我们，我们永远都支持你",
                "correct": "ABC"
            },
            {
                "num": 63,
                "text": "63. A 不要随便乱扔\n    B 否则，下次找起来会比较麻烦\n    C 东西用完后，最好放回原来的地方",
                "correct": "CAB"
            },
            {
                "num": 64,
                "text": "64. A 但学艺术的小关还是拒绝了杂志社的邀请\n    B 尽管杂志社的收入不低\n    C 他的理想是开一个自己的工作室",
                "correct": "BAC"
            },
            {
                "num": 65,
                "text": "65. A 请他给你当导游保证没问题\n    B 对那个城市很熟悉\n    C 我这个同学就是在北京出生、长大的",
                "correct": "CBA"
            }
        ],
        "p3_read": [
            {
                "num": 66,
                "text": "66. 有些电话号码只有 3 个数字，这是为了方便人们记住。例如，你想找警察帮忙，可以打 110；想知道天气情况，可以打 121；有人生病了，可以打 120。\n★ 根据这段话，打 121 是因为想：",
                "options": [
                    "A 找大夫",
                    "B 知道天气",
                    "C 办信用卡",
                    "D 打扫房间"
                ],
                "correct": "B"
            },
            {
                "num": 67,
                "text": "67. 虽然京剧的历史才两百多年，但是已经发展得很成熟了。随着社会的发展，京剧也在改变着，以适应不同年龄观众的需要。\n★ 关于京剧，可以知道：",
                "options": [
                    "A 很流行",
                    "B 缺少变化",
                    "C 历史不长",
                    "D 动作复杂"
                ],
                "correct": "C"
            },
            {
                "num": 68,
                "text": "68. 要想获得别人的尊重，首先要学会尊重别人。尊重别人，不仅指对人友好、有礼貌，而且还要尊重别人的兴趣和爱好。\n★ 这段话主要想告诉我们，怎样：",
                "options": [
                    "A 互相帮助",
                    "B 提高能力",
                    "C 原谅别人",
                    "D 尊重别人"
                ],
                "correct": "D"
            },
            {
                "num": 69,
                "text": "69. 语言是交流的工具，多掌握一门语言，就多了一双看世界的眼睛。\n★ 这段话认为掌握一门外语可以：",
                "options": [
                    "A 保护眼睛",
                    "B 更好地了解世界",
                    "C 获得高薪",
                    "D 减少误会"
                ],
                "correct": "B"
            },
            {
                "num": 70,
                "text": "70. 很多人喜欢在家里养花，不仅因为花能美化环境，还因为照顾花草能让人放松心情。\n★ 养花的主要好处是：",
                "options": [
                    "A 增加收入",
                    "B 锻炼身体",
                    "C 节省时间",
                    "D 放松心情"
                ],
                "correct": "D"
            },
            {
                "num": 71,
                "text": "71. 做事情光有热情还不够，还需要有耐心和方法，否则很难成功。\n★ 想要成功需要：",
                "options": [
                    "A 很多钱",
                    "B 运气",
                    "C 耐心和方法",
                    "D 别人的帮助"
                ],
                "correct": "C"
            },
            {
                "num": 72,
                "text": "72. 这个城市的交通非常便利，地铁和公交线路覆盖了几乎所有主要的景点。\n★ 这个城市的特点是：",
                "options": [
                    "A 气候湿润",
                    "B 人口很多",
                    "C 消费很高",
                    "D 交通便利"
                ],
                "correct": "D"
            },
            {
                "num": 73,
                "text": "73. 遇到困难时，不要轻易放弃，坚持下去往往就会看到希望。\n★ 遇到困难时应该：",
                "options": [
                    "A 马上求助",
                    "B 换个目标",
                    "C 休息几天",
                    "D 坚持不放弃"
                ],
                "correct": "D"
            },
            {
                "num": 74,
                "text": "74. 饮食对健康有很大的影响，平时应该多吃蔬菜和水果，少吃高油高糖的食物。\n★ 为了健康应该：",
                "options": [
                    "A 不吃晚饭",
                    "B 多喝咖啡",
                    "C 多吃蔬果",
                    "D 经常打针"
                ],
                "correct": "C"
            },
            {
                "num": 75,
                "text": "75. 良好的第一印象很重要，它可以在很短的时间内拉近两个人之间的距离。\n★ 第一印象的作用是：",
                "options": [
                    "A 决定一切",
                    "B 容易改变",
                    "C 拉近距离",
                    "D 避免冲突"
                ],
                "correct": "C"
            },
            {
                "num": 76,
                "text": "76. 读书可以开阔视野，让人看到更广阔的世界。\n★ 读书的好处是：",
                "options": [
                    "A 开阔视野",
                    "B 提高语速",
                    "C 减肥",
                    "D 增加睡眠"
                ],
                "correct": "A"
            },
            {
                "num": 77,
                "text": "77. 适当的运动可以增强体力，提高身体的免疫力。\n★ 运动可以：",
                "options": [
                    "A 让人发烧",
                    "B 浪费时间",
                    "C 增加压力",
                    "D 增强体力"
                ],
                "correct": "D"
            },
            {
                "num": 78,
                "text": "78. 保护环境需要全社会共同努力，从小事做起，节约水电。\n★ 保护环境应该：",
                "options": [
                    "A 互相推卸",
                    "B 顺其自然",
                    "C 只靠政府",
                    "D 从小事做起"
                ],
                "correct": "D"
            },
            {
                "num": 79,
                "text": "79. 幽默的人往往更容易交到朋友，因为他们能给身边的人带来快乐。\n★ 幽默的人容易交朋友是因为：",
                "options": [
                    "A 能给别人带来快乐",
                    "B 很富有",
                    "C 颜值高",
                    "D 很严肃"
                ],
                "correct": "A"
            },
            {
                "num": 80,
                "text": "80. 准时守信是做人的基本原则，答应别人的事情一定要按时做到。\n★ 这段话强调：",
                "options": [
                    "A 要勇敢",
                    "B 要聪明",
                    "C 要活泼",
                    "D 要准时守信"
                ],
                "correct": "D"
            },
            {
                "num": 81,
                "text": "81. 学习一门技能需要经过长期的练习，不可能几天就掌握。\n★ 学习技能需要：",
                "options": [
                    "A 天赋",
                    "B 很多钱",
                    "C 长期练习",
                    "D 名师指导"
                ],
                "correct": "C"
            },
            {
                "num": 82,
                "text": "82. 很多孩子小时候对世界充满好奇，喜欢问为什么。\n★ 孩子小时候容易：",
                "options": [
                    "A 害羞",
                    "B 觉得孤单",
                    "C 经常生病",
                    "D 充满好奇"
                ],
                "correct": "D"
            },
            {
                "num": 83,
                "text": "83. 工作和休息要合理安排，过度劳累会损害身体健康。\n★ 这段话建议：",
                "options": [
                    "A 放弃工作",
                    "B 劳逸结合",
                    "C 每天跑步",
                    "D 经常出差"
                ],
                "correct": "B"
            },
            {
                "num": 84,
                "text": "84. 沟通是解决人与人之间矛盾的最好方式。\n★ 解决矛盾最好：",
                "options": [
                    "A 互相打架",
                    "B 保持沉默",
                    "C 进行沟通",
                    "D 找警察"
                ],
                "correct": "C"
            },
            {
                "num": 85,
                "text": "85. 失败并不可怕，可怕的是失去重新站起来的勇气。\n★ 最可怕的是：",
                "options": [
                    "A 考不好",
                    "B 失去勇气",
                    "C 没钱",
                    "D 天气不好"
                ],
                "correct": "B"
            }
        ],
        "p1_write": [
            {
                "num": 86,
                "words": "86. 这篇文章 / 三部分 / 组成 / 由",
                "correct": [
                    "这篇文章由三部分组成。"
                ]
            },
            {
                "num": 87,
                "words": "87. 儿童 / 欢迎 / 很 / 这个节目 / 受",
                "correct": [
                    "这个节目很受儿童欢迎。"
                ]
            },
            {
                "num": 88,
                "words": "88. 离大使馆 / 友谊宾馆 / 远 / 吗",
                "correct": [
                    "友谊宾馆离大使馆远吗？"
                ]
            },
            {
                "num": 89,
                "words": "89. 很 / 诚实 / 那个 / 确实 / 司机",
                "correct": [
                    "那个司机确实很诚实。"
                ]
            },
            {
                "num": 90,
                "words": "90. 加油站 / 使用 / 手机 / 禁止",
                "correct": [
                    "加油站禁止使用手机。"
                ]
            },
            {
                "num": 91,
                "words": "91. 去 / 公园 / 你陪姐姐 / 散散步 / 吧",
                "correct": [
                    "你陪姐姐去公园散散步吧。"
                ]
            },
            {
                "num": 92,
                "words": "92. 有点儿 / 咸 / 中午的 / 西红柿鸡蛋汤 / 稍微",
                "correct": [
                    "中午的西红柿鸡蛋汤稍微有点儿咸。"
                ]
            },
            {
                "num": 93,
                "words": "93. 中文 / 说得 / 你们校长 / 的 / 很流利",
                "correct": [
                    "你们校长的中文说得很流利。"
                ]
            },
            {
                "num": 94,
                "words": "94. 90%的 / 通过了考试 / 同学 / 大约有",
                "correct": [
                    "大约有90%的同学通过了考试。"
                ]
            },
            {
                "num": 95,
                "words": "95. 房间 / 米小姐 / 把 / 收拾好了",
                "correct": [
                    "米小姐把房间收拾好了。"
                ]
            }
        ],
        "p2_write": [
            {
                "num": 96,
                "word": "袜子",
                "img_num": 1,
                "prompt": "Tranh hai đứa trẻ không穿袜子 (chân trần)"
            },
            {
                "num": 97,
                "word": "害羞",
                "img_num": 2,
                "prompt": "Tranh cô gái khép nép 害羞"
            },
            {
                "num": 98,
                "word": "醒",
                "img_num": 3,
                "prompt": "Tranh cô gái vừa 醒 来起床"
            },
            {
                "num": 99,
                "word": "密码",
                "img_num": 4,
                "prompt": "Tranh suy nghĩ 输入密码"
            },
            {
                "num": 100,
                "word": "咳嗽",
                "img_num": 5,
                "prompt": "Tranh đeo khẩu khẩu 咳嗽"
            }
        ]
    },
    "H41111": {
        "p1_listen": [
            {
                "num": 1,
                "text": "1．★ 葡萄酒可以多喝。",
                "correct": "×",
                "script": "1．每天喝一点儿葡萄酒，对身体是有好处的。但是不能喝太多。"
            },
            {
                "num": 2,
                "text": "2．★ 他对小云没什么印象。",
                "correct": "×",
                "script": "2．虽然和小云只见过一面，但是她活泼和热情的性格给我留下了很深的印象。"
            },
            {
                "num": 3,
                "text": "3．★ 高叔叔早睡早起。",
                "correct": "√",
                "script": "3．高叔叔从小就养成了早睡早起的习惯。"
            },
            {
                "num": 4,
                "text": "4．★ 他想去打网球。",
                "correct": "√",
                "script": "4．今天天气真好，咱们去打网球吧。"
            },
            {
                "num": 5,
                "text": "5．★ 那个笑话很有意思。",
                "correct": "√",
                "script": "5．刚才听的那个笑话太好笑了。"
            },
            {
                "num": 6,
                "text": "6．★ 司机认识路。",
                "correct": "√",
                "script": "6．放心吧，这条路我走过很多次。"
            },
            {
                "num": 7,
                "text": "7．★ 她不想换衣服。",
                "correct": "×",
                "script": "7．这件裙子太短了，我去换一件。"
            },
            {
                "num": 8,
                "text": "8．★ 邻居正在搬家。",
                "correct": "×",
                "script": "8．隔壁怎么这么吵？是不是在装修？"
            },
            {
                "num": 9,
                "text": "9．★ 弟弟学会了骑自行车。",
                "correct": "√",
                "script": "9．弟弟终于学会了骑自行车。"
            },
            {
                "num": 10,
                "text": "10．★ 他现在是经理了。",
                "correct": "√",
                "script": "10．他终于被提升为经理了。"
            }
        ],
        "p2_listen": [
            {
                "num": 11,
                "options": [
                    "A. 干净",
                    "B. 热闹",
                    "C. 条件差",
                    "D. 服务热情"
                ],
                "correct": "B",
                "script": "11．男：这家饭馆生意真好啊。\n女：是啊，这里挺热闹的，菜也很好吃。\n问：这家饭馆怎么样？"
            },
            {
                "num": 12,
                "options": [
                    "A. 老师",
                    "B. 记者",
                    "C. 售货员",
                    "D. 出租车司机"
                ],
                "correct": "C",
                "script": "12．女：先生，请问您想买什么样的衬衫？\n男：我想看看蓝色的。\n问：女的最可能是做什么的？"
            },
            {
                "num": 13,
                "options": [
                    "A. 下周再来",
                    "B. 最好别买",
                    "C. 价格太高",
                    "D. 先参观一下"
                ],
                "correct": "A",
                "script": "13．男：这几款笔记本电脑都在打折。\n女：今天没带够钱，咱们下周再来买吧。\n问：女的是什么意思？"
            },
            {
                "num": 14,
                "options": [
                    "A. 上网",
                    "B. 玩游戏",
                    "C. 洗碗筷",
                    "D. 看电视"
                ],
                "correct": "D",
                "script": "14．女：作业做完了吗？怎么又在看电视？\n男：做完了，我再看十分钟就去睡觉。\n问：男的正在做什么？"
            },
            {
                "num": 15,
                "options": [
                    "A. 有些着急",
                    "B. 刚下火车",
                    "C. 行李箱丢了",
                    "D. 提前回来了"
                ],
                "correct": "A",
                "script": "15．男：你怎么一直在看手表？\n女：我和客户约了九点，现在都八点四十了，路上还堵车。\n问：女的现在心情怎么样？"
            },
            {
                "num": 16,
                "options": [
                    "A. 教室",
                    "B. 公园西门",
                    "C. 学校东门",
                    "D. 图书馆门口"
                ],
                "correct": "C",
                "script": "16．女：明天早上八点半在学校东门集合。\n男：好的，我知道了。\n问：他们明天在哪儿集合？"
            },
            {
                "num": 17,
                "options": [
                    "A. 迟到了",
                    "B. 拿错伞了",
                    "C. 忘密码了",
                    "D. 弄错顺序了"
                ],
                "correct": "B",
                "script": "17．男：这把伞不是我的。\n女：不好意思，我拿错伞了。\n问：女的怎么了？"
            },
            {
                "num": 18,
                "options": [
                    "A. 夏天快来了",
                    "B. 天气暖和了",
                    "C. 昨晚下雪了",
                    "D. 现在是秋季"
                ],
                "correct": "D",
                "script": "18．女：树叶都变红变黄了。\n男：是啊，现在是秋季。\n问：现在是什么季节？"
            },
            {
                "num": 19,
                "options": [
                    "A. 坏了",
                    "B. 没纸了",
                    "C. 断电了",
                    "D. 卡纸了"
                ],
                "correct": "B",
                "script": "19．男：打印机怎么不打印了？\n女：里面的纸用完了。\n问：打印机怎么了？"
            },
            {
                "num": 20,
                "options": [
                    "A. 准备出差",
                    "B. 被批评了",
                    "C. 干得不错",
                    "D. 反对加班"
                ],
                "correct": "C",
                "script": "20．女：经理，这个月的任务完成了。\n男：大家干得不错！\n问：关于大家，可以知道什么？"
            },
            {
                "num": 21,
                "options": [
                    "A. 银行",
                    "B. 理发店",
                    "C. 大使馆",
                    "D. 公共汽车站"
                ],
                "correct": "A",
                "script": "21．男：请问取款机在哪儿？\n女：一楼大厅左边就是银行。\n问：男的要去哪儿？"
            },
            {
                "num": 22,
                "options": [
                    "A. 新闻",
                    "B. 中文",
                    "C. 法律",
                    "D. 经济"
                ],
                "correct": "C",
                "script": "22．女：小张学的是什么专业？\n男：他学的是法律。\n问：小张学的是什么专业？"
            },
            {
                "num": 23,
                "options": [
                    "A. 不用客气",
                    "B. 忘记时间了",
                    "C. 要打扮一下",
                    "D. 有别的约会"
                ],
                "correct": "D",
                "script": "23．男：今晚一起吃个饭吧？\n女：今晚我有别的约会。\n问：女的为什么不去吃饭？"
            },
            {
                "num": 24,
                "options": [
                    "A. 很乱",
                    "B. 很脏",
                    "C. 很整齐",
                    "D. 擦得很亮"
                ],
                "correct": "A",
                "script": "24．女：你的房间怎么这么乱？\n男：我马上收拾。\n问：房间怎么样？"
            },
            {
                "num": 25,
                "options": [
                    "A. 感冒了",
                    "B. 没找到他",
                    "C. 不敢告诉他",
                    "D. 没调查清楚"
                ],
                "correct": "B",
                "script": "25．男：你去找到李老师了吗？\n女：我去他办公室了，但是没找到他。\n问：女的怎么了？"
            }
        ],
        "p3_listen": [
            {
                "num": 26,
                "options": [
                    "A. 很无聊",
                    "B. 不精彩",
                    "C. 非常好",
                    "D. 没小说好看"
                ],
                "correct": "C",
                "script": "26．男：昨晚的京剧演出怎么样？女：非常好！问：演出怎么样？"
            },
            {
                "num": 27,
                "options": [
                    "A. 跳舞",
                    "B. 打网球",
                    "C. 踢足球",
                    "D. 看杂志"
                ],
                "correct": "B",
                "script": "27．女：周末你有什么打算？男：我想去打网球。问：男的周末想做什么？"
            },
            {
                "num": 28,
                "options": [
                    "A. 住院了",
                    "B. 肚子疼",
                    "C. 被骗了",
                    "D. 没被邀请"
                ],
                "correct": "A",
                "script": "28．男：听说老王住院了？女：他得了感冒，住几天院就好了。问：老王怎么了？"
            },
            {
                "num": 29,
                "options": [
                    "A. 妈妈反对",
                    "B. 还没放暑假",
                    "C. 认识时间短",
                    "D. 缺少共同语言"
                ],
                "correct": "C",
                "script": "29．女：他们俩怎么这么快就结婚了？男：虽然认识时间短，但感情很好。问：大家觉得奇怪是因为什么？"
            },
            {
                "num": 30,
                "options": [
                    "A. 很失望",
                    "B. 很吃惊",
                    "C. 有点儿后悔",
                    "D. 有点儿紧张"
                ],
                "correct": "D",
                "script": "30．男：马上就要上台了。女：心里有点儿紧张。问：女的心情怎么样？"
            },
            {
                "num": 31,
                "options": [
                    "A. 奶奶在家",
                    "B. 男的饿了",
                    "C. 电话没响",
                    "D. 奶奶在听广播"
                ],
                "correct": "A",
                "script": "31．女：奶奶一个人在家行吗？男：放心吧，奶奶在家挺好的。问：关于奶奶，可以知道什么？"
            },
            {
                "num": 32,
                "options": [
                    "A. 变化很大",
                    "B. 气温很低",
                    "C. 风景美丽",
                    "D. 天气干燥"
                ],
                "correct": "D",
                "script": "32．男：北方冬天的天气怎么样？女：比较冷，而且非常干燥。问：北方冬天的天气怎么样？"
            },
            {
                "num": 33,
                "options": [
                    "A. 搬沙发",
                    "B. 修冰箱",
                    "C. 挂地图",
                    "D. 打扫街道"
                ],
                "correct": "A",
                "script": "33．女：你能帮我抬一下沙发吗？男：没问题。问：他们要做什么？"
            },
            {
                "num": 34,
                "options": [
                    "A. 报道",
                    "B. 总结",
                    "C. 通知",
                    "D. 证明"
                ],
                "correct": "B",
                "script": "34．男：小张，年终总结写好了吗？女：写好了。问：小张写好了什么？"
            },
            {
                "num": 35,
                "options": [
                    "A. 季节",
                    "B. 网站",
                    "C. 日记",
                    "D. 电脑"
                ],
                "correct": "D",
                "script": "35．女：我想买台新电脑。男：去科技市场看看吧。问：女的想买什么？"
            },
            {
                "num": 36,
                "options": [
                    "A. 经理",
                    "B. 护士",
                    "C. 大夫",
                    "D. 警察"
                ],
                "correct": "A",
                "script": "36．男：王经理，请您签字。女：好的。问：女的是做什么的？"
            },
            {
                "num": 37,
                "options": [
                    "A. 很帅",
                    "B. 非常勇敢",
                    "C. 喜欢开玩笑",
                    "D. 个子比较矮"
                ],
                "correct": "C",
                "script": "37．女：小高性格怎么样？男：他很喜欢开玩笑。问：小高有什么特点？"
            },
            {
                "num": 38,
                "options": [
                    "A. 800 元",
                    "B. 1000 元",
                    "C. 1200 元",
                    "D. 10000 元"
                ],
                "correct": "B",
                "script": "38．男：打折后只要1000元。女：挺便宜的。问：打折后多少钱？"
            },
            {
                "num": 39,
                "options": [
                    "A. 有点儿旧",
                    "B. 一共两层",
                    "C. 离公司近",
                    "D. 有两个人住"
                ],
                "correct": "D",
                "script": "39．女：房子住着怎么样？男：我和同事两个人住。问：关于房子，可以知道什么？"
            },
            {
                "num": 40,
                "options": [
                    "A. 管理严格",
                    "B. 不太关心",
                    "C. 多表扬他们",
                    "D. 陪他们读书"
                ],
                "correct": "C",
                "script": "40．一段话：多表扬他们能增加孩子的信心。问：这段话建议怎么教育孩子？"
            },
            {
                "num": 41,
                "options": [
                    "A. 20%",
                    "B. 40%",
                    "C. 50%",
                    "D. 60%"
                ],
                "correct": "C",
                "script": "41．一段话：有近50%的人习惯在睡前看手机。问：看手机的人占多少？"
            },
            {
                "num": 42,
                "options": [
                    "A. 信任朋友",
                    "B. 理解别人",
                    "C. 获得尊重",
                    "D. 知道想要什么"
                ],
                "correct": "D",
                "script": "42．一段话：人生的关键是要明白自己真正想要什么。问：人生的关键是什么？"
            },
            {
                "num": 43,
                "options": [
                    "A. 幸福",
                    "B. 教育",
                    "C. 责任",
                    "D. 民族"
                ],
                "correct": "A",
                "script": "43．一段话：身体健康、生活平安就是最大的幸福。问：这段话主要谈什么？"
            },
            {
                "num": 44,
                "options": [
                    "A. 对人友好",
                    "B. 做事粗心",
                    "C. 会考虑问题",
                    "D. 喜欢回忆过去"
                ],
                "correct": "C",
                "script": "44．一段话：成熟的人遇到困难时更会全面地考虑问题。问：成熟的人有什么特点？"
            },
            {
                "num": 45,
                "options": [
                    "A. 竞争的烦恼",
                    "B. 什么是成熟",
                    "C. 要学会原谅",
                    "D. 不要可怜别人"
                ],
                "correct": "B",
                "script": "45．一段话：成熟不仅是年龄的增长，更是心理的完善。问：这段话主要谈什么？"
            }
        ],
        "p1_read": [
            {
                "num": 46,
                "text": "46. 现在改变（  ）？恐怕晚了吧？来不及了。",
                "options": [
                    "A. 暂时",
                    "B. 主意",
                    "C. 导游",
                    "D. 坚持",
                    "E. 凉快",
                    "F. 推迟"
                ],
                "correct": "B"
            },
            {
                "num": 47,
                "text": "47. 这儿树多，比路边（  ）多了，咱们在这儿坐一会儿吧。",
                "options": [
                    "A. 暂时",
                    "B. 主意",
                    "C. 导游",
                    "D. 坚持",
                    "E. 凉快",
                    "F. 推迟"
                ],
                "correct": "E"
            },
            {
                "num": 48,
                "text": "48. 别担心，这只是（  ）的，很快就会好起来。",
                "options": [
                    "A. 暂时",
                    "B. 主意",
                    "C. 导游",
                    "D. 坚持",
                    "E. 凉快",
                    "F. 推迟"
                ],
                "correct": "A"
            },
            {
                "num": 49,
                "text": "49. 他在北京当（  ），对各条街道都很熟悉。",
                "options": [
                    "A. 暂时",
                    "B. 主意",
                    "C. 导游",
                    "D. 坚持",
                    "E. 凉快",
                    "F. 推迟"
                ],
                "correct": "C"
            },
            {
                "num": 50,
                "text": "50. 天气预报说今天下午有雨，活动（  ）到明天举行。",
                "options": [
                    "A. 暂时",
                    "B. 主意",
                    "C. 导游",
                    "D. 坚持",
                    "E. 凉快",
                    "F. 推迟"
                ],
                "correct": "F"
            },
            {
                "num": 51,
                "text": "51. A：希望我们的工作能让您满意。\n    B：我非常满意，一切都（  ）得很好，谢谢你们。",
                "options": [
                    "A. 害羞",
                    "B. 羡慕",
                    "C. 温度",
                    "D. 起来",
                    "E. 差不多",
                    "F. 安排"
                ],
                "correct": "F"
            },
            {
                "num": 52,
                "text": "52. A：王师傅，您是北方人吧？\n    B：对，我是北京人，在南方（  ）工作10年了。",
                "options": [
                    "A. 害羞",
                    "B. 羡慕",
                    "C. 温度",
                    "D. 起来",
                    "E. 差不多",
                    "F. 安排"
                ],
                "correct": "E"
            },
            {
                "num": 53,
                "text": "53. A：我昨天晚上做了个特别有意思的梦，你听着……\n    B：奇怪，一般人醒了就想不（  ）自己做了什么梦，你怎么总能记住？",
                "options": [
                    "A. 害羞",
                    "B. 羡慕",
                    "C. 温度",
                    "D. 起来",
                    "E. 差不多",
                    "F. 安排"
                ],
                "correct": "D"
            },
            {
                "num": 54,
                "text": "54. A：你妹妹很可爱， लेकिन好像不太爱说话。\n    B：她有点儿（  ），等跟大家熟悉了就好了。",
                "options": [
                    "A. 害羞",
                    "B. 羡慕",
                    "C. 温度",
                    "D. 起来",
                    "E. 差不多",
                    "F. 安排"
                ],
                "correct": "A"
            },
            {
                "num": 55,
                "text": "55. A：他的汉语说得很流利，真让人（  ）。\n    B：他是翻译，当然很厉害。",
                "options": [
                    "A. 害羞",
                    "B. 羡慕",
                    "C. 温度",
                    "D. 起来",
                    "E. 差不多",
                    "F. 安排"
                ],
                "correct": "B"
            }
        ],
        "p2_read": [
            {
                "num": 56,
                "text": "56. A 现在很多女孩都认为瘦才是美的\n    B 其实健康才是最重要的\n    C 于是都努力减肥",
                "correct": "ACB"
            },
            {
                "num": 57,
                "text": "57. A 它不适合在南方生长\n    B 这种红色的植物在北方很常见\n    C 不过由于受气候的限制",
                "correct": "BCA"
            },
            {
                "num": 58,
                "text": "58. A 与他们握手并向他们表示祝贺\n    B 他走到研究生代表前\n    C 会议结束后",
                "correct": "BCA"
            },
            {
                "num": 59,
                "text": "59. A 这段时间，机场的乘客比平时几乎多了两倍\n    B 他们每天至少要工作 10 个小时\n    C 为保证所有航班都能按时起飞",
                "correct": "CAB"
            },
            {
                "num": 60,
                "text": "60. A 但过程比结果更重要\n    B 而且你还年轻，一切都可以重新开始\n    C 尽管这个计划失败了",
                "correct": "CAB"
            },
            {
                "num": 61,
                "text": "61. A 除了自己留一小部分外\n    B 白先生每个月发了工资和奖金后\n    C 把大部分都交给了妻子",
                "correct": "BCA"
            },
            {
                "num": 62,
                "text": "62. A 连五六十岁的老人都每人一个\n    B 我刚到那个城市就发现好多人都戴这种帽子\n    C 后来才知道戴这种帽子有很多好处",
                "correct": "BAC"
            },
            {
                "num": 63,
                "text": "63. A 它就能学会很多东西\n    B 哥哥的那只大黑狗聪明极了\n    C 只要稍微花点儿时间教教它",
                "correct": "ACB"
            },
            {
                "num": 64,
                "text": "64. A 我们从 2 月 17 号开始，到 3 月底\n    B 大概可以提供 3000 多个工作机会\n    C 还将举办 5 场招聘会",
                "correct": "ABC"
            },
            {
                "num": 65,
                "text": "65. A 实际上，有个简单的办法可以拒绝接收垃圾邮件\n    B 每天打开电子信箱，总会收到一些垃圾邮件\n    C 这真是件让人烦恼的事",
                "correct": "BCA"
            }
        ],
        "p3_read": [
            {
                "num": 66,
                "text": "66. 男人和女人在很多方面是不相同的。例如，在工作中遇到了不愉快的事，女人喜欢跟丈夫说。\n★ 女人在工作中遇到不高兴的事，会：",
                "options": [
                    "A 流泪",
                    "B 跟丈夫说",
                    "C 请父母帮忙",
                    "D 去商场购物"
                ],
                "correct": "B"
            },
            {
                "num": 67,
                "text": "67. 什么是朋友？朋友是在你得意时提醒你不要骄傲的人；在你失败时鼓励你的人。\n★ 这段话主要谈的是：",
                "options": [
                    "A 性别",
                    "B 礼貌",
                    "C 友谊",
                    "D 理想"
                ],
                "correct": "C"
            },
            {
                "num": 68,
                "text": "68. 由于没好好复习，今天考得不怎么样。\n★ 关于今天的考试，可以知道：",
                "options": [
                    "A 题目很简单",
                    "B 成绩很好",
                    "C 没考好",
                    "D 老师很满意"
                ],
                "correct": "C"
            },
            {
                "num": 69,
                "text": "69. 遇到不顺心的事，可以找朋友倾诉。\n★ 心情不好时可以：",
                "options": [
                    "A 买新车",
                    "B 找朋友倾诉",
                    "C 去爬山",
                    "D 换工作"
                ],
                "correct": "B"
            },
            {
                "num": 70,
                "text": "70. 想安静地写点儿东西，这是个不错的选择。\n★ 根据这段话，可以知道这儿：",
                "options": [
                    "A 很安静",
                    "B 比较暗",
                    "C 有点儿吵",
                    "D 适合弹钢琴"
                ],
                "correct": "A"
            },
            {
                "num": 71,
                "text": "71. 交流能减少人与人之间的误会，使感情逐渐加深。\n★ 通过交流，可以：",
                "options": [
                    "A 获得同情",
                    "B 增进感情",
                    "C 节约时间",
                    "D 降低收入"
                ],
                "correct": "B"
            },
            {
                "num": 72,
                "text": "72. 我认为，广告会介绍一样东西的优点，却不会说它的缺点。\n★ 我觉得广告：",
                "options": [
                    "A 只说优点",
                    "B 数量太多",
                    "C 内容是假的",
                    "D 应该受到重视"
                ],
                "correct": "A"
            },
            {
                "num": 73,
                "text": "73. 足球比赛如果 90 分钟后仍然是 0 比 0，可以进行加时赛来决定输赢。\n★ 关于加时赛，可以知道：",
                "options": [
                    "A 每场都有",
                    "B 已被禁止",
                    "C 要有输赢结果",
                    "D 时间为 60 分钟"
                ],
                "correct": "C"
            },
            {
                "num": 74,
                "text": "74. 小时候他经常生病，长大后他成了一名优秀的长跑运动员。\n★ 人们没有想到的是，他：",
                "options": [
                    "A 力气很大",
                    "B 在医院工作",
                    "C 身体越来越差",
                    "D 成为了运动员"
                ],
                "correct": "D"
            },
            {
                "num": 75,
                "text": "75. 超市里经常会提供一些免费食品让人们尝一尝，这吸引了许多顾客。\n★ 逛超市时，顾客们被什么吸引了？",
                "options": [
                    "A 打折食品",
                    "B 新鲜水果",
                    "C 免费尝东西",
                    "D 漂亮的盒子"
                ],
                "correct": "C"
            },
            {
                "num": 76,
                "text": "76. 这本书他看了一个月才看到第 5 页。\n★ 这说明他：",
                "options": [
                    "A 很有耐心",
                    "B 看书很快",
                    "C 记性不好",
                    "D 并不是真正爱看书"
                ],
                "correct": "D"
            },
            {
                "num": 77,
                "text": "77. 只有坚持到最后的人才能尝到成功的甜头。\n★ 想要成功必须：",
                "options": [
                    "A 坚持付出努力",
                    "B 运气好",
                    "C 依靠朋友",
                    "D 有名气"
                ],
                "correct": "A"
            },
            {
                "num": 78,
                "text": "78. 遇到堵车时，不要焦虑，可以听听音乐，放松一下心情。\n★ 堵车时可以：",
                "options": [
                    "A 大声喊叫",
                    "B 下车跑步",
                    "C 听听音乐",
                    "D 打电话骂人"
                ],
                "correct": "C"
            },
            {
                "num": 79,
                "text": "79. 养成了良好的生活习惯，身体才会健康。\n★ 这段话强调：",
                "options": [
                    "A 饮食结构",
                    "B 锻炼方法",
                    "C 良好习惯的重要性",
                    "D 睡眠时间"
                ],
                "correct": "C"
            },
            {
                "num": 80,
                "text": "80. 一个人如果没有责任感，就很难得到别人的信任。\n★ 责任感能让人：",
                "options": [
                    "A 获得信任",
                    "B 赚钱更多",
                    "C 不生病",
                    "D 变帅"
                ],
                "correct": "A"
            },
            {
                "num": 81,
                "text": "81. 学习语言需要多听多说，不要害怕说错。\n★ 学习语言要：",
                "options": [
                    "A 多买字典",
                    "B 不怕说错多练习",
                    "C 只写不说",
                    "D 不听课"
                ],
                "correct": "B"
            },
            {
                "num": 82,
                "text": "82. 妈妈抱着把小手表吃进肚子里的儿子来到医院。\n★ 孩子怎么了？",
                "options": [
                    "A 发烧了",
                    "B 流血了",
                    "C 吃错药了",
                    "D 把手表吃肚子里的"
                ],
                "correct": "D"
            },
            {
                "num": 83,
                "text": "83. 堵车时不妨听听音乐，改变一下心情。\n★ 这段话主要想说明：",
                "options": [
                    "A 堵车时怎么办",
                    "B 要保护环境",
                    "C 堵车的原因",
                    "D 汽车的优点"
                ],
                "correct": "A"
            },
            {
                "num": 84,
                "text": "84. 减肥需要控制饮食，多做运动。\n★ 减肥需要：",
                "options": [
                    "A 吃减肥药",
                    "B 控制饮食多运动",
                    "C 每天睡觉",
                    "D 喝很多水"
                ],
                "correct": "B"
            },
            {
                "num": 85,
                "text": "85. 积极的态度能让人在遇到困难时不轻易被打倒。\n★ 积极的态度可以：",
                "options": [
                    "A 让人发财",
                    "B 让人勇敢面对困难",
                    "C 让人不生病",
                    "D 让人变年轻"
                ],
                "correct": "B"
            }
        ],
        "p1_write": [
            {
                "num": 86,
                "words": "86. 中午 / 又酸又辣 / 的 / 菜",
                "correct": [
                    "中午的菜又酸又辣。"
                ]
            },
            {
                "num": 87,
                "words": "87. 很多人的 / 注意 / 引起了 / 那篇文章",
                "correct": [
                    "那篇文章引起了很多人的注意。"
                ]
            },
            {
                "num": 88,
                "words": "88. 森林 / 狮子 / 里 / 住着 / 一群",
                "correct": [
                    "森林里住着一群狮子。"
                ]
            },
            {
                "num": 89,
                "words": "89. 香蕉皮 / 请 / 扔 / 垃圾桶里 / 把",
                "correct": [
                    "请把香蕉皮扔垃圾桶里。"
                ]
            },
            {
                "num": 90,
                "words": "90. 慢慢 / 积累的 / 是需要 / 知识",
                "correct": [
                    "知识是需要慢慢积累的。"
                ]
            },
            {
                "num": 91,
                "words": "91. 他父亲 / 当地的 / 一位律师 / 是",
                "correct": [
                    "他父亲是当地的一位律师。"
                ]
            },
            {
                "num": 92,
                "words": "92. 小弟弟 / 打针 / 邻居家 / 的 / 害怕",
                "correct": [
                    "邻居家的小弟弟害怕打针。"
                ]
            },
            {
                "num": 93,
                "words": "93. 果然是 / 这 / 好消息 / 一个激动人心的",
                "correct": [
                    "这果然是一个激动人心的好消息。"
                ]
            },
            {
                "num": 94,
                "words": "94. 不符合 / 宾馆的 / 规定 / 这样做",
                "correct": [
                    "这样做不符合宾馆的规定。"
                ]
            },
            {
                "num": 95,
                "words": "95. 集合 / 到底什么时候 / 呢 / 明天",
                "correct": [
                    "明天到底什么时候集合呢？"
                ]
            }
        ],
        "p2_write": [
            {
                "num": 96,
                "word": "厚",
                "img_num": 1
            },
            {
                "num": 97,
                "word": "区别",
                "img_num": 2
            },
            {
                "num": 98,
                "word": "难受",
                "img_num": 3
            },
            {
                "num": 99,
                "word": "信心",
                "img_num": 4
            },
            {
                "num": 100,
                "word": "躺",
                "img_num": 5
            }
        ]
    },
    "H41218": {
        "p1_listen": [
            {
                "num": 1,
                "text": "1．★ 别让工作影响生活。",
                "correct": "√",
                "script": "1．工作只是生活的一部分，千万不要把工作中的不愉快带到生活中来。"
            },
            {
                "num": 2,
                "text": "2．★ 人们离不开水。",
                "correct": "√",
                "script": "2．阳光、空气和水，无论是对动植物，还是对人来说，都是不可缺少的。"
            },
            {
                "num": 3,
                "text": "3．★ 考试那天他很轻松。",
                "correct": "×",
                "script": "3．因为没有好好复习，考试那天他有点儿紧张。"
            },
            {
                "num": 4,
                "text": "4．★ 妻子容易被感动。",
                "correct": "√",
                "script": "4．我妻子特别容易被感动，看电影时常流眼泪。"
            },
            {
                "num": 5,
                "text": "5．★ 不要担心失败。",
                "correct": "√",
                "script": "5．失败并不可怕，下一次就可能成功。"
            },
            {
                "num": 6,
                "text": "6．★ 不要忘记过去。",
                "correct": "×",
                "script": "6．过去的就让它过去吧，重要的是向前看。"
            },
            {
                "num": 7,
                "text": "7．★ 北京现在是冬季。",
                "correct": "×",
                "script": "7．北京的秋天最舒服。"
            },
            {
                "num": 8,
                "text": "8．★ 幸福没有标准答案。",
                "correct": "√",
                "script": "8．每个人对幸福的理解都不一样，没有统一标准。"
            },
            {
                "num": 9,
                "text": "9．★ 他们在出租车上。",
                "correct": "×",
                "script": "9．各位乘客，欢迎乘坐本次列车。"
            },
            {
                "num": 10,
                "text": "10．★ 出发时间又推迟了。",
                "correct": "×",
                "script": "10．我们的航班将按时起飞。"
            }
        ],
        "p2_listen": [
            {
                "num": 11,
                "options": [
                    "A. 很无聊",
                    "B. 很有趣",
                    "C. 很有名",
                    "D. 很流行"
                ],
                "correct": "B",
                "script": "11．男：你看过这部电影吗？\n男：看过，剧情很有趣。\n问：这部电影怎么样？"
            },
            {
                "num": 12,
                "options": [
                    "A. 擦不掉",
                    "B. 打扫教室",
                    "C. 家具要留着",
                    "D. 质量不太好"
                ],
                "correct": "C",
                "script": "12．女：旧家具质量挺好的，都留着吧。\n问：女的是什么意思？"
            },
            {
                "num": 13,
                "options": [
                    "A. 东边",
                    "B. 西边",
                    "C. 南边",
                    "D. 北边"
                ],
                "correct": "A",
                "script": "13．男：图书馆在东边。\n问：图书馆在哪儿？"
            },
            {
                "num": 14,
                "options": [
                    "A. 太麻烦",
                    "B. 想去试试",
                    "C. 不知道地址",
                    "D. 要商量一下"
                ],
                "correct": "B",
                "script": "14．女：我也想去试试，明天发简历。\n问：女的打算怎么做？"
            },
            {
                "num": 15,
                "options": [
                    "A. 门票免费",
                    "B. 票还没买",
                    "C. 女的在道歉",
                    "D. 表演很精彩"
                ],
                "correct": "B",
                "script": "15．男：票还没买到呢，排队的人太多。\n问：根据对话，可以知道什么？"
            },
            {
                "num": 16,
                "options": [
                    "A. 加班",
                    "B. 爬山",
                    "C. 打网球",
                    "D. 打羽毛球"
                ],
                "correct": "C",
                "script": "16．男：周六去打网球怎么样？\n女：好啊！\n问：他们周六打算干什么？"
            },
            {
                "num": 17,
                "options": [
                    "A. 香蕉",
                    "B. 酸菜鱼",
                    "C. 西红柿汤",
                    "D. 水果蛋糕"
                ],
                "correct": "B",
                "script": "17．女：今天的酸菜鱼味道真好。\n问：他们在吃什么？"
            },
            {
                "num": 18,
                "options": [
                    "A. 银行",
                    "B. 办公室",
                    "C. 体育馆",
                    "D. 理发店"
                ],
                "correct": "D",
                "script": "18．男：理发师，帮我稍微修剪一下。\n问：对话发生在什么地方？"
            },
            {
                "num": 19,
                "options": [
                    "A. 口渴",
                    "B. 生病了",
                    "C. 刷牙了",
                    "D. 这儿禁止抽烟"
                ],
                "correct": "D",
                "script": "19．女：餐厅禁止抽烟。\n问：女的提醒男的是什么？"
            },
            {
                "num": 20,
                "options": [
                    "A. 脾气不好",
                    "B. 是位教授",
                    "C. 打算先工作",
                    "D. 有点儿后悔"
                ],
                "correct": "C",
                "script": "20．女：我打算先工作，积累经验。\n问：女的有什么打算？"
            },
            {
                "num": 21,
                "options": [
                    "A. 哥哥",
                    "B. 弟弟",
                    "C. 大夫",
                    "D. 护士"
                ],
                "correct": "A",
                "script": "21．女：这是你哥哥吗？\n男：对，他比我大两岁。\n问：照片上的人是男的的谁？"
            },
            {
                "num": 22,
                "options": [
                    "A. 座位",
                    "B. 洗手间",
                    "C. 服务员",
                    "D. 塑料袋"
                ],
                "correct": "A",
                "script": "22．男：请问这个座位有人吗？\n女：没有，您坐吧。\n问：男的在找什么？"
            },
            {
                "num": 23,
                "options": [
                    "A. 被骗了",
                    "B. 请假了",
                    "C. 出差了",
                    "D. 离开公司了"
                ],
                "correct": "D",
                "script": "23．男：他上周就已经离开公司了。\n问：关于小王，可以知道什么？"
            },
            {
                "num": 24,
                "options": [
                    "A. 问路",
                    "B. 填表格",
                    "C. 修自行车",
                    "D. 收拾房间"
                ],
                "correct": "A",
                "script": "24．男：请问去地铁站怎么走？\n问：男的在做什么？"
            },
            {
                "num": 25,
                "options": [
                    "A. 下班后",
                    "B. 半小时后",
                    "C. 喝完茶后",
                    "D. 明天中午"
                ],
                "correct": "A",
                "script": "25．男：等下班后吧。\n问：男的建议什么时候去？"
            }
        ],
        "p3_listen": [
            {
                "num": 26,
                "options": [
                    "A. 裤子脏了",
                    "B. 手机坏了",
                    "C. 比赛输了",
                    "D. 没考上博士"
                ],
                "correct": "C",
                "script": "26．男：篮球比赛输了。问：男的为什么难过？"
            },
            {
                "num": 27,
                "options": [
                    "A. 是演员",
                    "B. 十分幽默",
                    "C. 会弹钢琴",
                    "D. 同意帮忙"
                ],
                "correct": "D",
                "script": "27．男：没问题，包在我身上。问：男的是什么态度？"
            },
            {
                "num": 28,
                "options": [
                    "A. 火车站",
                    "B. 公园门口",
                    "C. 宾馆门口",
                    "D. 公共汽车上"
                ],
                "correct": "B",
                "script": "28．女：明天早上八点在公园门口。问：他们在哪儿集合？"
            },
            {
                "num": 29,
                "options": [
                    "A. 手表丢了",
                    "B. 在读硕士",
                    "C. 没戴眼镜",
                    "D. 想买葡萄"
                ],
                "correct": "D",
                "script": "29．男：我想买点儿葡萄回去。问：男的想买什么？"
            },
            {
                "num": 30,
                "options": [
                    "A. 很吃惊",
                    "B. 在看演出",
                    "C. 接受邀请",
                    "D. 快过生日了"
                ],
                "correct": "C",
                "script": "30．女：我一定准时参加！问：女的怎么决定？"
            },
            {
                "num": 31,
                "options": [
                    "A. 下雨了",
                    "B. 正在下雪",
                    "C. 气温很高",
                    "D. 风刮得很大"
                ],
                "correct": "B",
                "script": "31．女：快看外面！下雪了！问：天气怎么样？"
            },
            {
                "num": 32,
                "options": [
                    "A. 没重点",
                    "B. 声音大",
                    "C. 有上海味儿",
                    "D. 语法不太好"
                ],
                "correct": "C",
                "script": "32．男：听他说话带有上海口音。问：他的普通话有什么特点？"
            },
            {
                "num": 33,
                "options": [
                    "A. 饿了",
                    "B. 很激动",
                    "C. 很伤心",
                    "D. 忘记密码了"
                ],
                "correct": "A",
                "script": "33．男：中午没吃饭，现在饿坏了。问：男的怎么了？"
            },
            {
                "num": 34,
                "options": [
                    "A. 骑马",
                    "B. 超车",
                    "C. 打篮球",
                    "D. 在江边游泳"
                ],
                "correct": "D",
                "script": "34．男：夏天去江边游泳非常凉快。问：男的提到什么运动？"
            },
            {
                "num": 35,
                "options": [
                    "A. 扔垃圾",
                    "B. 洗盘子",
                    "C. 买帽子",
                    "D. 抬洗衣机"
                ],
                "correct": "A",
                "script": "35．女：把这包垃圾顺便带下楼扔了吧。问：女的让男的做什么？"
            },
            {
                "num": 36,
                "options": [
                    "A. 管理",
                    "B. 信任",
                    "C. 懂得放弃",
                    "D. 学会原谅"
                ],
                "correct": "B",
                "script": "36．女：人与人交往最重要的是相互信任。问：女的认为最重要的是什么？"
            },
            {
                "num": 37,
                "options": [
                    "A. 主动握手",
                    "B. 尊重自己",
                    "C. 多提醒别人",
                    "D. 首先相信别人"
                ],
                "correct": "D",
                "script": "37．一段话：要获得别人的信任，首先你要相信别人。问：这段话建议怎么做？"
            },
            {
                "num": 38,
                "options": [
                    "A. 吸引顾客",
                    "B. 感谢顾客",
                    "C. 表示祝贺",
                    "D. 减少浪费"
                ],
                "correct": "A",
                "script": "38．一段话：商场打折主要是为了吸引更多的顾客。问：商场打折为了什么？"
            },
            {
                "num": 39,
                "options": [
                    "A. 不好卖",
                    "B. 不值得买",
                    "C. 比平时便宜",
                    "D. 很难引起注意"
                ],
                "correct": "C",
                "script": "39．一段话：打折商品比平时便宜。问：打折商品有什么特点？"
            },
            {
                "num": 40,
                "options": [
                    "A. 爱说话",
                    "B. 爱跳舞",
                    "C. 生气了",
                    "D. 讨厌画画儿"
                ],
                "correct": "A",
                "script": "40．女：小王非常爱说话。问：小王有什么特点？"
            },
            {
                "num": 41,
                "options": [
                    "A. 哭了",
                    "B. 很粗心",
                    "C. 有些害羞",
                    "D. 肚子难受"
                ],
                "correct": "C",
                "script": "41．男：她有些害羞，脸都红了。问： corporate她怎么了？"
            },
            {
                "num": 42,
                "options": [
                    "A. 讲笑话",
                    "B. 与人竞争",
                    "C. 翻译文章",
                    "D. 拒绝帮忙"
                ],
                "correct": "D",
                "script": "42．一段话：要学会礼貌地拒绝。问：这段话谈论什么？"
            },
            {
                "num": 43,
                "options": [
                    "A. 赚的钱多",
                    "B. 条件允许",
                    "C. 经验丰富",
                    "D. 觉得快乐"
                ],
                "correct": "D",
                "script": "43．一段话：更重要的是你能从中感到快乐。问：选择工作什么最重要？"
            },
            {
                "num": 44,
                "options": [
                    "A. 太吵",
                    "B. 床窄",
                    "C. 没冰箱",
                    "D. 房间有点儿暗"
                ],
                "correct": "D",
                "script": "44．女：采光不好，有点儿暗。问：这间房间有什么缺点？"
            },
            {
                "num": 45,
                "options": [
                    "A. 学生",
                    "B. 司机",
                    "C. 售货员",
                    "D. 中文教师"
                ],
                "correct": "A",
                "script": "45．男：同学们，今天的作业是预习。问：男的在跟谁说话？"
            }
        ],
        "p1_read": [
            {
                "num": 46,
                "text": "46. 真抱歉，现在路上堵得很厉害，（  ）来不及了。",
                "options": [
                    "A. 打针",
                    "B. 报道",
                    "C. 共同",
                    "D. 坚持",
                    "E. 国际",
                    "F. 恐怕"
                ],
                "correct": "F"
            },
            {
                "num": 47,
                "text": "47. 我儿子发烧了，我得送他去医院（  ），看样子下午我不能去踢球了。",
                "options": [
                    "A. 打针",
                    "B. 报道",
                    "C. 共同",
                    "D. 坚持",
                    "E. 国际",
                    "F. 恐怕"
                ],
                "correct": "A"
            },
            {
                "num": 48,
                "text": "48. 今天是“六一”（  ）儿童节，这是全世界儿童的节日。",
                "options": [
                    "A. 打针",
                    "B. 报道",
                    "C. 共同",
                    "D. 坚持",
                    "E. 国际",
                    "F. 恐怕"
                ],
                "correct": "E"
            },
            {
                "num": 49,
                "text": "49. 他们俩有很多（  ）语言，每次一见面就聊个不停。",
                "options": [
                    "A. 打针",
                    "B. 报道",
                    "C. 共同",
                    "D. 坚持",
                    "E. 国际",
                    "F. 恐怕"
                ],
                "correct": "C"
            },
            {
                "num": 50,
                "text": "50. 这篇（  ）写得不错，反映了不少问题，有时间的话你可以看看。",
                "options": [
                    "A. 打针",
                    "B. 报道",
                    "C. 共同",
                    "D. 坚持",
                    "E. 国际",
                    "F. 恐怕"
                ],
                "correct": "B"
            },
            {
                "num": 51,
                "text": "51. A：你经常来这条街上逛吗？\n    B：不经常，我（  ）来一趟。这儿离我家挺远的。",
                "options": [
                    "A. 精神",
                    "B. 稍微",
                    "C. 温度",
                    "D. 工资",
                    "E. 大概",
                    "F. 偶尔"
                ],
                "correct": "F"
            },
            {
                "num": 52,
                "text": "52. A：下午交工作总结，你写好了没？\n    B：差不多了，有个地方我还要（  ）改一下。",
                "options": [
                    "A. 精神",
                    "B. 稍微",
                    "C. 温度",
                    "D. 工资",
                    "E. 大概",
                    "F. 偶尔"
                ],
                "correct": "B"
            },
            {
                "num": 53,
                "text": "53. A：这个月的（  ）和奖金，一共 8000 元，昨天上午已经打您卡里了。\n    B：好的，谢谢你。",
                "options": [
                    "A. 精神",
                    "B. 稍微",
                    "C. 温度",
                    "D. 工资",
                    "E. 大概",
                    "F. 偶尔"
                ],
                "correct": "D"
            },
            {
                "num": 54,
                "text": "54. A：这个寒假，你打算去三亚多长时间？\n    B：（  ）两个星期吧，估计月底就能回来。",
                "options": [
                    "A. 精神",
                    "B. 稍微",
                    "C. 温度",
                    "D. 工资",
                    "E. 大概",
                    "F. 偶尔"
                ],
                "correct": "E"
            },
            {
                "num": 55,
                "text": "55. A：我那件红衬衫呢？你放哪儿了？\n    B：洗了，在外面挂着，还没干呢。你穿这件就很好，很（  ）。",
                "options": [
                    "A. 精神",
                    "B. 稍微",
                    "C. 温度",
                    "D. 工资",
                    "E. 大概",
                    "F. 偶尔"
                ],
                "correct": "A"
            }
        ],
        "p2_read": [
            {
                "num": 56,
                "text": "56. A 相反，会使问题变得更复杂\n    B 不但不能解决任何问题\n    C 现在和当时的情况不同，如果还是使用以前的办法",
                "correct": "CBA"
            },
            {
                "num": 57,
                "text": "57. A 今天早上，北京突然下起雪来\n    B 所有航班都无法起飞，所以我先生只好又回来了\n    C 并且越下越大，完全没有要停的意思",
                "correct": "ACB"
            },
            {
                "num": 58,
                "text": "58. A 那件事情，我们一直以为是他的错\n    B 但后来才发现，是我们误会他了\n    C 应该由他负全部责任",
                "correct": "ACB"
            },
            {
                "num": 59,
                "text": "59. A 毕业以后我们就很少见面了\n    B 但我们一直保持着联系\n    C 感情依然非常好",
                "correct": "ABC"
            },
            {
                "num": 60,
                "text": "60. A 结果适得其反\n    B 有些父母对孩子要求过于严格\n    C 给孩子带来了极大的压力",
                "correct": "CBA"
            },
            {
                "num": 61,
                "text": "61. A 保持积极乐观的心态\n    B 才能在困境中看到希望\n    C 只有在任何时候都",
                "correct": "BAC"
            },
            {
                "num": 62,
                "text": "62. A 这使得他拥有丰富的阅历\n    B 他去过世界上三十多个国家\n    C 说话聊天时总是非常吸引人",
                "correct": "BCA"
            },
            {
                "num": 63,
                "text": "63. A 一定要仔细阅读使用说明\n    B 避免因操作不当造成损坏\n    C 在第一次使用新家电前",
                "correct": "ACB"
            },
            {
                "num": 64,
                "text": "64. A 积累了丰富的教学经验\n    B 王老师从事教育工作已经三十年了\n    C 深受学生和家长的尊敬",
                "correct": "BCA"
            },
            {
                "num": 65,
                "text": "65. A 使得生活变得越来越便捷\n    B 互联网和移动支付的普及\n    C 人们出门甚至不需要带现金",
                "correct": "BCA"
            }
        ],
        "p3_read": [
        {
                "num": 66,
                "text": "66. 您看，这几种衬衫都不错，不仅颜色好，质量也保证是最好的。怎么样？您选哪种？\n★ 说话人最可能是做什么的？",
                "options": [
                        "A. 司机",
                        "B. 售货员",
                        "C. 理发师",
                        "D. 医生"
                ],
                "correct": "B"
        },
        {
                "num": 67,
                "text": "67. 习惯就像我们的好朋友，在关键时刻能给我们力量。相反，坏习惯就像坏朋友，会带来麻烦。因此，我们要养成好习惯，改掉坏习惯。\n★ 这段话主要谈：",
                "options": [
                        "A. 遵守规定",
                        "B. 珍惜友谊",
                        "C. 习惯的作用",
                        "D. 尊重他人"
                ],
                "correct": "C"
        },
        {
                "num": 68,
                "text": "68. 您看，这里的大门都是用厚木头做的，上面的花纹也是人工雕刻出来的，非常精致。\n★ 关于这个大门，可以知道：",
                "options": [
                        "A. 很轻",
                        "B. 是木头做的",
                        "C. 坏了",
                        "D. 太贵了"
                ],
                "correct": "B"
        },
        {
                "num": 69,
                "text": "69. 那本杂志的内容十分丰富，里面不仅介绍了许多科学知识，而且语言非常幽默。像我这种对科学完全不感兴趣的人，读起来竟然也会觉得很有趣。\n★ 那本杂志：",
                "options": [
                        "A. 页数很多",
                        "B. 很有意思",
                        "C. 很难理解",
                        "D. 是关于艺术的"
                ],
                "correct": "B"
        },
        {
                "num": 70,
                "text": "70. 会议还没结束呢，一会儿继续讨论，所以暂时还不知道结果会怎么样。你先别着急，有消息我会第一时间通知你的。\n★ 根据这段话，会议：",
                "options": [
                        "A. 刚刚开始",
                        "B. 还没有结果",
                        "C. 有许多记者",
                        "D. 已经顺利结束"
                ],
                "correct": "B"
        },
        {
                "num": 71,
                "text": "71. 会一门外语很重要，这样你不仅可以去这个国家旅游，和这个国家的人们交流，而且可以了解这个国家的文化，并向他们介绍自己国家的文化。\n★ 这段话主要谈：",
                "options": [
                        "A. 学习方法",
                        "B. 文化的影响",
                        "C. 普通话的作用",
                        "D. 懂外语的好处"
                ],
                "correct": "D"
        },
        {
                "num": 72,
                "text": "72. “面包会有的，牛奶会有的，一切都会好起来的。”所以，不要太难过，不要太担心，因为雨过之后总会是晴天的。\n★ 这段话想告诉我们：",
                "options": [
                        "A. 要节约",
                        "B. 明天会更好",
                        "C. 要按时吃饭",
                        "D. 不要受规定的限制"
                ],
                "correct": "B"
        },
        {
                "num": 73,
                "text": "73. 经过调查，我们发现：购买我们电脑的人中，有 75%是因为受到我们广告的影响，有 11%的人表示他们从来没看过我们的广告。\n★ 根据调查，可以知道：",
                "options": [
                        "A. 电脑很贵",
                        "B. 广告效果好",
                        "C. 任务没完成",
                        "D. 笔记本更受欢迎"
                ],
                "correct": "B"
        },
        {
                "num": 74,
                "text": "74. 20 年前，人们还有通过写信交笔友的习惯，하지만进入 21 世纪后，尤其是最近几年，几乎没有人会选择写信了，人们更愿意打电话或上网交流。\n★ 现在人们更愿意：",
                "options": [
                        "A. 发传真",
                        "B. 写日记",
                        "C. 上网聊天儿",
                        "D. 阅读报纸杂志"
                ],
                "correct": "C"
        },
        {
                "num": 75,
                "text": "75. 不管是跟朋友约会， 还是一个人出去游玩儿，她都爱把自己打扮得漂漂亮亮。她觉得这样可以给自己带来好心情，自己高兴，别人看着也舒服。\n★ 跟朋友约会时，她：",
                "options": [
                        "A. 非常得意",
                        "B. 会认真打扮",
                        "C. 会花很多钱",
                        "D. 喜欢穿裙子"
                ],
                "correct": "B"
        },
        {
                "num": 76,
                "text": "76. 小时候，亲戚、邻居们都说我长得像我妈，特别是眼睛和鼻子。 可是长大后，他们说我更像 我爸， 尤其是性格， 对人热情，说话直接。\n★ 根据这段话，他：",
                "options": [
                        "A. 很浪漫",
                        "B. 变帅了",
                        "C. 特别聪明",
                        "D. 性格像父亲"
                ],
                "correct": "D"
        },
        {
                "num": 77,
                "text": "77. 他们结婚十几年了，两个人还坚持每天晚上 一起散步、聊天儿。他们的感情那么好， 让朋友们都很羡慕。\n★ 根据这段话，他们：",
                "options": [
                        "A. 性格相近",
                        "B. 刚结婚",
                        "C. 感情很好",
                        "D. 不喜欢运动"
                ],
                "correct": "C"
        },
        {
                "num": 78,
                "text": "78. 《现代汉语词典》 是一本很有用的工具书。当你遇到不会读或者不理解的字词时，只要翻翻它，就能找到答案，非常方便。\n★ 《现代汉语词典》：",
                "options": [
                        "A. 非常有帮助",
                        "B. 买不到了",
                        "C. 词语不多",
                        "D. 让人 感到烦恼"
                ],
                "correct": "A"
        },
        {
                "num": 79,
                "text": "79. 人在睡觉过程中会做梦，这太正常了。每个人都会做梦，区别只是梦的内容不同、有 的人把梦忘了而已。说自己没做过梦的人，只不过是忘记了。\n★ 关于做梦，下列哪个正确？",
                "options": [
                        "A. 影响身体健康",
                        "B. 人人都会做梦",
                        "C. 梦都很伤心",
                        "D. 让人变笨"
                ],
                "correct": "B"
        },
        {
                "num": 80,
                "text": "80-81.\n表扬 也是一门艺术。怎样表扬孩子才会更有效呢？一是表扬要及时，及时的表扬比迟到的表扬更有效果；二是表扬不仅要看 结果，还要看过程，如果孩子努力了，即使结果没成功，也要表扬 他的“好心”和付出。\n★ 怎样的表扬更有效果？",
                "options": [
                        "A. 及时的",
                        "B. 免费的",
                        "C. 正式的",
                        "D. 偶尔的"
                ],
                "correct": "A"
        },
        {
                "num": 81,
                "text": "81. ★ 父母表扬孩子的“好心”， 是为了：",
                "options": [
                        "A. 鼓励他放弃",
                        "B. 减少误会",
                        "C. 积累经验",
                        "D. 肯定  他的付出"
                ],
                "correct": "D"
        },
        {
                "num": 82,
                "text": "82-83.\n说到理想，人们很自然地 就会 想到：我将来想干什么？想成为一个什么样的人？科学家？老师？医生？警察？其实，明白自己想做什么很重要，知道怎么去做更为关键，否则，理想就 永远只是理想。可惜的是，人们 往往对   这一点重视不够。\n★ 这段话主要谈什么？",
                "options": [
                        "A. 理想",
                        "B. 专业",
                        "C. 收入",
                        "D. 友谊"
                ],
                "correct": "A"
        },
        {
                "num": 83,
                "text": "83. ★ 根据这段话，人们对什么不够重视？",
                "options": [
                        "A. 健康",
                        "B. 安全",
                        "C. 怎么去做",
                        "D. 自己的缺点"
                ],
                "correct": "C"
        },
        {
                "num": 84,
                "text": "84-85.\n做子女的总希望父母老了 以后能在家中好好休息，不要    那么辛苦。其实，老人   喜欢热闹，害怕孤单，他们需要  别人的重视和关心。所以，多鼓励老人  参加一些社会活动，  让他们觉得自己依然是对  家庭和社会有用的人， 让他们有“被需要”的感觉。\n★ 老人更  喜欢：",
                "options": [
                        "A. 开玩笑",
                        "B. 住在  农村",
                        "C. 获得重视",
                        "D. 吃面条儿"
                ],
                "correct": "C"
        },
        {
                "num": 85,
                "text": "85. ★ 这段话主要  谈什么？",
                "options": [
                        "A. 要有信心",
                        "B. 要积累经验",
                        "C. 遇事要  冷静",
                        "D. 老人  需要什么"
                ],
                "correct": "D"
        }
],
        "p1_write": [
            {
                "num": 86,
                "words": "86. 能力 / 重要 / 比知识 / 更",
                "correct": [
                    "能力比知识更重要。"
                ]
            },
            {
                "num": 87,
                "words": "87. 爱情 / 并 / 生命的全部 / 不是",
                "correct": [
                    "爱情并不是生命的全部。"
                ]
            },
            {
                "num": 88,
                "words": "88. 沙发 / 你的钥匙 / 在 / 上",
                "correct": [
                    "你的钥匙在沙发上。"
                ]
            },
            {
                "num": 89,
                "words": "89. 观众 / 那个电影 / 让 / 很失望",
                "correct": [
                    "那个电影让观众很失望。"
                ]
            },
            {
                "num": 90,
                "words": "90. 她 / 一遍 / 又重新 / 检查了",
                "correct": [
                    "她又重新检查了一遍。"
                ]
            },
            {
                "num": 91,
                "words": "91. 顺序 / 别 / 把 / 弄乱了",
                "correct": [
                    "别把顺序弄乱了。"
                ]
            },
            {
                "num": 92,
                "words": "92. 了 / 寄出去 / 你的申请材料 / 吗",
                "correct": [
                    "你的申请材料寄出去了吗？"
                ]
            },
            {
                "num": 93,
                "words": "93. 一万公里 / 是 / 这两个城市 / 距离 / 的",
                "correct": [
                    "这两个城市的距离是一万公里。"
                ]
            },
            {
                "num": 94,
                "words": "94. 很成熟 / 制造技术 / 已经 / 这种电梯的",
                "correct": [
                    "这种电梯的制造技术已经很成熟。"
                ]
            },
            {
                "num": 95,
                "words": "95. 印象 / 那位导游 / 很深的 / 给我 / 留下了",
                "correct": [
                    "那位导游给我留下了很深的印象。"
                ]
            }
        ],
        "p2_write": [
            {
                "num": 96,
                "word": "咸",
                "img_num": 1
            },
            {
                "num": 97,
                "word": "力气",
                "img_num": 2
            },
            {
                "num": 98,
                "word": "握手",
                "img_num": 3
            },
            {
                "num": 99,
                "word": "合作",
                "img_num": 4
            },
            {
                "num": 100,
                "word": "友谊",
                "img_num": 5
            }
        ]
    }
}


EXAM_CODES = list(EXAM_DATA.keys())
exam_tabs = st.tabs(EXAM_CODES)

for idx, exam_code in enumerate(EXAM_CODES):
    data = EXAM_DATA[exam_code]
    with exam_tabs[idx]:
        st.markdown(f"## 📋 ĐỀ THI MÃ: **{exam_code}**")
        
        sub_tab_listen, sub_tab_read, sub_tab_write = st.tabs(["🎧 听力 (Phần nghe)", "📖 阅读 (Phần đọc)", "✍️ 书写 (Phần viết)"])
        
        # ----------------------------------------------------------------------
        # 1. SUB-TAB PHẦN NGHE (45 CÂU)
        # ----------------------------------------------------------------------
        with sub_tab_listen:
            render_audio_player(exam_code)
            st.markdown("---")
            
            u_l1 = {}
            st.markdown("#### **第一部分 - 判断对错 (Câu 1 - 10)**")
            for i, q in enumerate(data["p1_listen"]):
                c_class = CARD_CLASSES[i % len(CARD_CLASSES)]
                st.markdown(f"<div class='{c_class}'><strong>Câu {q['num']}:</strong><br>{q['text']}", unsafe_allow_html=True)
                ans = st.radio(f"l1_{exam_code}_{q['num']}", ["√", "×"], horizontal=True, key=f"w_l1_{exam_code}_{q['num']}", label_visibility="collapsed")
                u_l1[q['num']] = ans
                st.markdown("</div>", unsafe_allow_html=True)
                
            u_l2 = {}
            st.markdown("#### **第二部分 - 单项选择 (Câu 11 - 25)**")
            for i, q in enumerate(data["p2_listen"]):
                c_class = CARD_CLASSES[(i+1) % len(CARD_CLASSES)]
                st.markdown(f"<div class='{c_class}'><strong>Câu {q['num']}:</strong>", unsafe_allow_html=True)
                ans = st.radio(f"l2_{exam_code}_{q['num']}", q["options"], key=f"w_l2_{exam_code}_{q['num']}", label_visibility="collapsed")
                u_l2[q['num']] = ans[0] if ans else ""
                st.markdown("</div>", unsafe_allow_html=True)
                
            u_l3 = {}
            st.markdown("#### **第三部分 - 单项选择 (Câu 26 - 45)**")
            for i, q in enumerate(data["p3_listen"]):
                c_class = CARD_CLASSES[(i+2) % len(CARD_CLASSES)]
                st.markdown(f"<div class='{c_class}'><strong>Câu {q['num']}:</strong>", unsafe_allow_html=True)
                ans = st.radio(f"l3_{exam_code}_{q['num']}", q["options"], key=f"w_l3_{exam_code}_{q['num']}", label_visibility="collapsed")
                u_l3[q['num']] = ans[0] if ans else ""
                st.markdown("</div>", unsafe_allow_html=True)
                
            if st.button(f"🚀 NỘP BÀI PHẦN NGHE MÃ {exam_code}", key=f"btn_sub_l_{exam_code}"):
                if not student_name.strip():
                    st.warning("⚠️ Vui lòng nhập Họ và tên ở đầu trang trước khi nộp bài!")
                else:
                    c1 = sum(1 for q in data["p1_listen"] if u_l1.get(q['num']) == q['correct'])
                    c2 = sum(1 for q in data["p2_listen"] if u_l2.get(q['num']) == q['correct'])
                    c3 = sum(1 for q in data["p3_listen"] if u_l3.get(q['num']) == q['correct'])
                    tot_c = c1 + c2 + c3
                    tot_q = len(data["p1_listen"]) + len(data["p2_listen"]) + len(data["p3_listen"])
                    sc_100 = (tot_c / tot_q) * 100
                    
                    st.success(f"🎉 **Kết quả Phần Nghe ({exam_code}):**\n- Số câu đúng: **{tot_c}/{tot_q}** câu\n- Điểm số: **{sc_100:.1f} / 100 điểm**")
                    send_score_to_gsheet(student_name, exam_code, "PHẦN NGHE", f"{tot_c}/{tot_q}", sc_100)
                    
                    st.markdown("---")
                    st.markdown("### 🔍 CHI TIẾT CÂU SAI & SCRIPT NGHE:")
                    for q in data["p1_listen"]:
                        if u_l1.get(q['num']) != q['correct']:
                            st.markdown(f"❌ **Câu {q['num']}**: Bạn chọn `{u_l1.get(q['num'])}` | Đáp án đúng: **{q['correct']}**")
                            with st.expander(f"📖 查看听力文本 (Xem Script Câu {q['num']})"):
                                st.write(q['script'])
                    for q in data["p2_listen"]:
                        if u_l2.get(q['num']) != q['correct']:
                            st.markdown(f"❌ **Câu {q['num']}**: Bạn chọn `{u_l2.get(q['num'])}` | Đáp án đúng: **{q['correct']}**")
                            with st.expander(f"📖 查看听力文本 (Xem Script Câu {q['num']})"):
                                st.write(q['script'])
                    for q in data["p3_listen"]:
                        if u_l3.get(q['num']) != q['correct']:
                            st.markdown(f"❌ **Câu {q['num']}**: Bạn chọn `{u_l3.get(q['num'])}` | Đáp án đúng: **{q['correct']}**")
                            with st.expander(f"📖 查看听力文本 (Xem Script Câu {q['num']})"):
                                st.write(q['script'])

        # ----------------------------------------------------------------------
        # 2. SUB-TAB PHẦN ĐỌC (40 CÂU)
        # ----------------------------------------------------------------------
        with sub_tab_read:
            st.markdown("### 二、阅读 (Phần đọc)")
            u_r1 = {}
            st.markdown("#### **第一部分 - 选词填空 (Câu 46 - 55)**")
            for i, q in enumerate(data["p1_read"]):
                c_class = CARD_CLASSES[i % len(CARD_CLASSES)]
                st.markdown(f"<div class='{c_class}'><strong>Câu {q['num']}:</strong><br>{q['text']}", unsafe_allow_html=True)
                ans = st.radio(f"r1_{exam_code}_{q['num']}", q["options"], key=f"w_r1_{exam_code}_{q['num']}", label_visibility="collapsed")
                u_r1[q['num']] = ans[0] if ans else ""
                st.markdown("</div>", unsafe_allow_html=True)
                
            u_r2 = {}
            st.markdown("#### **第二部分 - 排列顺序 (Câu 56 - 65)**")
            for i, q in enumerate(data["p2_read"]):
                c_class = CARD_CLASSES[(i+1) % len(CARD_CLASSES)]
                raw_t = q['text'].strip()
                raw_t = re.sub(r'^\d+[\.．]\s*', '', raw_t)
                lines = [line.strip() for line in raw_t.splitlines() if line.strip()]
                formatted_t = '<br>'.join(lines)
                
                st.markdown(f"<div class='{c_class}'><strong>Câu {q['num']}:</strong><br><div style='margin-top:6px !important;'>{formatted_t}</div></div>", unsafe_allow_html=True)
                ans = st.text_input(f"Nhập thứ tự 3 chữ cái (VD: BAC) cho câu {q['num']}:", key=f"w_r2_{exam_code}_{q['num']}").strip().upper()
                u_r2[q['num']] = ans
                
            u_r3 = {}
            st.markdown("#### **第三部分 - 阅读理解 (Câu 66 - 85)**")
            for i, q in enumerate(data["p3_read"]):
                c_class = CARD_CLASSES[(i+2) % len(CARD_CLASSES)]
                st.markdown(f"<div class='{c_class}'><strong>Câu {q['num']}:</strong><br>{q['text'].replace('\n', '<br>')}", unsafe_allow_html=True)
                ans = st.radio(f"r3_{exam_code}_{q['num']}", q["options"], key=f"w_r3_{exam_code}_{q['num']}", label_visibility="collapsed")
                u_r3[q['num']] = ans[0] if ans else ""
                st.markdown("</div>", unsafe_allow_html=True)
                
            if st.button(f"🚀 NỘP BÀI PHẦN ĐỌC MÃ {exam_code}", key=f"btn_sub_r_{exam_code}"):
                if not student_name.strip():
                    st.warning("⚠️ Vui lòng nhập Họ và tên ở đầu trang trước khi nộp bài!")
                else:
                    c1 = sum(1 for q in data["p1_read"] if u_r1.get(q['num']) == q['correct'])
                    c2 = sum(1 for q in data["p2_read"] if u_r2.get(q['num']) == q['correct'])
                    c3 = sum(1 for q in data["p3_read"] if u_r3.get(q['num']) == q['correct'])
                    tot_c = c1 + c2 + c3
                    tot_q = len(data["p1_read"]) + len(data["p2_read"]) + len(data["p3_read"])
                    sc_100 = (tot_c / tot_q) * 100
                    
                    msg = f"🎉 **Kết quả Phần Đọc ({exam_code}):**\n- Số câu đúng: **{tot_c}/{tot_q}** câu\n- Điểm số: **{sc_100:.1f} / 100 điểm**"
                    st.success(msg)
                    send_score_to_gsheet(student_name, exam_code, "PHẦN ĐỌC", f"{tot_c}/{tot_q}", sc_100)
                    
                    st.markdown("---")
                    st.markdown("### 🔍 CHI TIẾT CÂU SAI PHẦN ĐỌC:")
                    for q in data["p1_read"]:
                        if u_r1.get(q['num']) != q['correct']:
                            st.markdown(f"❌ **Câu {q['num']}**: Bạn chọn `{u_r1.get(q['num'])}` | Đáp án đúng: **{q['correct']}**")
                    for q in data["p2_read"]:
                        if u_r2.get(q['num']) != q['correct']:
                            st.markdown(f"❌ **Câu {q['num']}**: Bạn điền `{u_r2.get(q['num'])}` | Đáp án đúng: **{q['correct']}**")
                    for q in data["p3_read"]:
                        if u_r3.get(q['num']) != q['correct']:
                            st.markdown(f"❌ **Câu {q['num']}**: Bạn chọn `{u_r3.get(q['num'])}` | Đáp án đúng: **{q['correct']}**")

        # ----------------------------------------------------------------------
        # 3. SUB-TAB PHẦN VIẾT (15 CÂU)
        # ----------------------------------------------------------------------
        with sub_tab_write:
            st.markdown("### 三、书写 (Phần viết)")
            st.markdown("#### **第一部分 - 完成句子 (Câu 86 - 95)**")
            
            u_w1 = {}
            for i, q in enumerate(data["p1_write"]):
                c_class = CARD_CLASSES[i % len(CARD_CLASSES)]
                st.markdown(f"<div class='{c_class}'><strong>Câu {q['num']}:</strong> {q['words']}", unsafe_allow_html=True)
                ans = st.text_input("Nhập câu hoàn chỉnh của bạn tại đây:", key=f"w_w1_{exam_code}_{q['num']}").strip()
                u_w1[q['num']] = ans
                st.markdown("</div>", unsafe_allow_html=True)
                
            st.markdown("#### **第二部分 - 看图造句 (Câu 96 - 100)**")
            u_w2 = {}
            for i, q in enumerate(data["p2_write"]):
                c_class = CARD_CLASSES[(i+1) % len(CARD_CLASSES)]
                st.markdown(f"<div class='{c_class}'><strong>Câu {q['num']}:</strong> Từ gợi ý: <strong>{q['word']}</strong>", unsafe_allow_html=True)
                
                img_idx = i + 1
                img_jpg = f"{exam_code}_{img_idx}.jpg"
                img_png = f"{exam_code}_{img_idx}.png"
                if os.path.exists(img_jpg):
                    st.image(img_jpg, width=280)
                elif os.path.exists(img_png):
                    st.image(img_png, width=280)
                else:
                    st.info(f"📷 (Khung xem ảnh bài tập câu {q['num']}: hãy tải file ảnh tên **{exam_code}_{img_idx}.jpg** lên cùng thư mục GitHub nhé!)")
                    
                ans = st.text_area("Nhập câu đặt theo tranh của bạn tại đây:", key=f"w_w2_{exam_code}_{q['num']}")
                u_w2[q['num']] = ans
                st.markdown("</div>", unsafe_allow_html=True)
                
            st.info("📌 Note: Các câu từ 96-100 (đặt câu theo tranh) cô Ngọc sẽ chấm cụ thể sau. Điểm hiển thị bên dưới chỉ mang tính chất tương đối.")
            
            if st.button(f"🚀 NỘP BÀI PHẦN VIẾT MÃ {exam_code}", key=f"btn_sub_w_{exam_code}"):
                if not student_name.strip():
                    st.warning("⚠️ Vui lòng nhập Họ và tên ở đầu trang trước khi nộp bài!")
                else:
                    c1 = 0
                    for q in data["p1_write"]:
                        user_ans = u_w1.get(q['num'], '').strip()
                        if any(user_ans == possible_ans.strip() for possible_ans in q['acceptable']):
                            c1 += 1
                            
                    tot_q = len(data["p1_write"]) + len(data["p2_write"])
                    tot_c = c1 + len(data["p2_write"])
                    sc_100 = (tot_c / tot_q) * 100
                    
                    msg = f"🎉 **Kết quả Phần Viết tương đối ({exam_code}):**\n- Số câu đúng Phần 1: **{c1}/{len(data['p1_write'])}** câu\n- Điểm số tương đối: **{sc_100:.1f} / 100 điểm**"
                    st.success(msg)
                    send_score_to_gsheet(student_name, exam_code, "PHẦN VIẾT", f"{tot_c}/{tot_q}", sc_100)
                    
                    st.markdown("---")
                    st.markdown("### 🔍 CHI TIẾT CÂU SAI PHẦN VIẾT (PHẦN 1):")
                    for q in data["p1_write"]:
                        user_ans = u_w1.get(q['num'], '').strip()
                        if not any(user_ans == possible_ans.strip() for possible_ans in q['acceptable']):
                            st.markdown(f"❌ **Câu {q['num']}**: Bạn viết `{u_w1.get(q['num'])}` | Đáp án đúng: **{q['acceptable'][0]}**")

st.markdown("""
<div class="footer">
    黄宝玉老师
</div>
""", unsafe_allow_html=True)
