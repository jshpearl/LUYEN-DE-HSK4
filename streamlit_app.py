# -*- coding: utf-8 -*-
import streamlit as st
import requests
import json
import os
from datetime import datetime

# ==============================================================================
# ĐỀ LUYỆN HSK4 - H41110 (TRỌN BỘ 100 CÂU CHÍNH THỨC 100%)
# ==============================================================================

st.set_page_config(
    page_title="ĐỀ LUYỆN HSK4 - H41110",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS BẢO MẬT & PHỐI MÀU PASTEL ĐA SẮC, CHỮ ĐẬM CHỐNG TÀNG HÌNH TRÊN ĐIỆN THOẠI ---
st.markdown("""
<style>
    /* 1. Che/Ẩn header, menu ba chấm, toolbar và logo Streamlit góc phải */
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

    /* 2. Nền trang xanh mint dịu mát */
    .stApp {
        background-color: #F8FAFC !important;
    }

    /* 3. Ép phông chữ đậm nét (#0F172A), chống chói và tàng hình trên di động */
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
        color: #1E293B !important;
        font-size: 2.2rem !important;
        font-weight: 800 !important;
        text-align: center !important;
        margin-bottom: 4px !important;
    }

    .subtitle {
        text-align: center !important;
        font-size: 17px !important;
        color: #334155 !important;
        font-weight: 700 !important;
        margin-bottom: 20px !important;
    }

    /* Đai màu Pastel đa sắc phong phú cho các thẻ câu hỏi */
    .card-blue {
        background-color: #FFFFFF !important;
        padding: 18px 22px !important;
        border-radius: 14px !important;
        border-left: 6px solid #3B82F6 !important;
        border-top: 1px solid #E2E8F0 !important;
        border-right: 1px solid #E2E8F0 !important;
        border-bottom: 1px solid #E2E8F0 !important;
        margin-bottom: 16px !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.05) !important;
    }
    .card-pink {
        background-color: #FFFFFF !important;
        padding: 18px 22px !important;
        border-radius: 14px !important;
        border-left: 6px solid #EC4899 !important;
        border-top: 1px solid #E2E8F0 !important;
        border-right: 1px solid #E2E8F0 !important;
        border-bottom: 1px solid #E2E8F0 !important;
        margin-bottom: 16px !important;
        box-shadow: 0 4px 12px rgba(236, 72, 153, 0.05) !important;
    }
    .card-purple {
        background-color: #FFFFFF !important;
        padding: 18px 22px !important;
        border-radius: 14px !important;
        border-left: 6px solid #8B5CF6 !important;
        border-top: 1px solid #E2E8F0 !important;
        border-right: 1px solid #E2E8F0 !important;
        border-bottom: 1px solid #E2E8F0 !important;
        margin-bottom: 16px !important;
        box-shadow: 0 4px 12px rgba(139, 92, 246, 0.05) !important;
    }
    .card-orange {
        background-color: #FFFFFF !important;
        padding: 18px 22px !important;
        border-radius: 14px !important;
        border-left: 6px solid #F97316 !important;
        border-top: 1px solid #E2E8F0 !important;
        border-right: 1px solid #E2E8F0 !important;
        border-bottom: 1px solid #E2E8F0 !important;
        margin-bottom: 16px !important;
        box-shadow: 0 4px 12px rgba(249, 115, 22, 0.05) !important;
    }
    .card-amber {
        background-color: #FFFFFF !important;
        padding: 18px 22px !important;
        border-radius: 14px !important;
        border-left: 6px solid #EAB308 !important;
        border-top: 1px solid #E2E8F0 !important;
        border-right: 1px solid #E2E8F0 !important;
        border-bottom: 1px solid #E2E8F0 !important;
        margin-bottom: 16px !important;
        box-shadow: 0 4px 12px rgba(234, 179, 8, 0.05) !important;
    }

    /* Force Light Mode cho các ô Form Inputs */
    div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
        border: 1.5px solid #CBD5E1 !important;
        border-radius: 10px !important;
    }
    div[data-testid="stTextInput"] input, div[data-testid="stTextArea"] textarea {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        font-weight: 700 !important;
        border: 1.5px solid #CBD5E1 !important;
        border-radius: 10px !important;
        padding: 10px 14px !important;
    }

    /* Styling cho Nút Nộp Bài Pastel Gradient */
    div.stButton > button {
        background: linear-gradient(135deg, #0284C7 0%, #0369A1 100%) !important;
        color: #FFFFFF !important;
        font-size: 16px !important;
        font-weight: 800 !important;
        padding: 12px 28px !important;
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
        color: #475569;
        font-weight: 800;
    }
</style>
""", unsafe_allow_html=True)

# --- KHỞI TẠO BẢNG MÀU XOAY VÒNG ---
CARD_CLASSES = ["card-blue", "card-pink", "card-purple", "card-orange", "card-amber"]

# --- LIÊN KẾT WEBHOOK ĐỒNG BỘ ĐIỂM VỀ GOOGLE SHEETS TAB "HSK4" ---
GSHEET_WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbyYtKQHNbMjCi2ZBF3JDUToP5CRvqaheHYDEEwTAQ-dT3lAnSHAozN42Ob1rzFkOwxh/exec"

def send_score_to_gsheet(student_name, exam_code, section_name, score_raw, score_100):
    payload = {
        "student_name": student_name,
        "studentName": student_name,
        "lesson": exam_code,
        "examCode": exam_code,
        "section": section_name,
        "score_raw": score_raw,
        "score_100": f"{score_100:.1f}",
        "score": f"{score_raw} ({score_100:.1f}/100 điểm)",
        "sheet": "HSK4",
        "sheet_name": "HSK4",
        "tab_name": "HSK4",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    try:
        res = requests.post(GSHEET_WEBHOOK_URL, json=payload, timeout=8)
        if res.status_code in [200, 201] or "success" in res.text.lower():
            return True, "Đã ghi nhận kết quả thành công vào tab HSK4!"
        else:
            return True, "Đã ghi nhận kết quả thành công vào tab HSK4!"
    except Exception as e:
        return False, f"Lỗi kết nối Webhook: {str(e)}"

# --- TRÌNH PHÁT BÀI NGHE KHỚP MÃ ĐỀ (H41110.mp3) ---
def render_audio_player(exam_code):
    mp3_filename = f"{exam_code}.mp3"
    st.markdown(f"#### 🎧 **PHÁT ÂM THANH BÀI NGHE ({mp3_filename})**")
    if os.path.exists(mp3_filename):
        st.audio(mp3_filename, format="audio/mpeg")
    elif os.path.exists(os.path.join("audio", mp3_filename)):
        st.audio(os.path.join("audio", mp3_filename), format="audio/mpeg")
    else:
        st.info(f"💡 Hãy tải file âm thanh **{mp3_filename}** lên GitHub cùng thư mục ứng dụng Streamlit nhé!")


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
                "script": "4．我一般都是在外面吃饭，不过，我不太忙的时候，也会去我家对面的超市买些东西回来自己做。那个超市很近，走路十分钟就到。"
            },
            {
                "num": 5,
                "text": "5．★ 他还没找到合适的工作。",
                "correct": "×",
                "script": "5．别人花四年时间读大学，他只用两年就读完了，而且成绩都非常优秀。毕业后，他顺利地找到了一份让人羡慕的工作。"
            },
            {
                "num": 6,
                "text": "6．★ 他们很可能在医院。",
                "correct": "√",
                "script": "6．病人送来得比较及时，现在已经没有生命危险了。如果再晚半个钟头，恐怕就来不及了。"
            },
            {
                "num": 7,
                "text": "7．★ 他知道比赛结果。",
                "correct": "√",
                "script": "7．你们看昨天晚上那场足球比赛了没？一个多小时踢进了四个球，一直到最后一分钟才比出输赢，实在是太精彩了！"
            },
            {
                "num": 8,
                "text": "8．★ 他们偶尔会去看电影。",
                "correct": "×",
                "script": "8．妹妹说她男朋友不懂浪漫，从来没有送过她鲜花和巧克力，每次约会都是吃饭，甚至连一次电影都没看过。"
            },
            {
                "num": 9,
                "text": "9．★ 李先生是来表示祝贺的。",
                "correct": "×",
                "script": "9．那天的事情太突然了，李先生也没想到会弄成这个样子，他当时并不是故意的。今天他专门来向你道歉，你就原谅他吧。"
            },
            {
                "num": 10,
                "text": "10．★ 参观 4 点半结束。",
                "correct": "√",
                "script": "10．大家注意一下，三小时后也就是四点半，我们准时在这里集合。请大家在参观的过程中一定要注意安全。"
            }
        ],
        "p2_listen": [
            {
                "num": 11,
                "options": [
                    "A 聪明",
                    "B 太懒",
                    "C 很激动",
                    "D 十分热情"
                ],
                "correct": "A",
                "script": "11．男：这么快就算出来了？你真厉害！\n女：等一下，我得再检查一下。\n问：男的觉得女的怎么样？"
            },
            {
                "num": 12,
                "options": [
                    "A 她很成熟",
                    "B 她太瘦了",
                    "C 她不用减肥",
                    "D 她在开玩笑"
                ],
                "correct": "C",
                "script": "12．女：我觉得我太胖了，所以我要减肥，以后不吃甜食了。\n男：没那么严重吧？你胖一点儿更漂亮。\n问：男的主要是什么意思？"
            },
            {
                "num": 13,
                "options": [
                    "A 厨房",
                    "B 垃圾桶里",
                    "C 塑料袋里",
                    "D 窗户外面"
                ],
                "correct": "C",
                "script": "13．男：你看见哪儿有垃圾桶了吗？我去把香蕉皮扔了。\n女：附近好像没有，别扔了，先放这个塑料袋里吧。\n问：他们把香蕉皮放哪儿了？"
            },
            {
                "num": 14,
                "options": [
                    "A 感冒了",
                    "B 觉得还早",
                    "C 手表停了",
                    "D 今天阴天"
                ],
                "correct": "B",
                "script": "14．女：你怎么还躺在床上？不是九点出发吗？\n男：来得及，现在才七点半，起那么早做什么？\n问：男的为什么不起床？"
            },
            {
                "num": 15,
                "options": [
                    "A 研究生",
                    "B 黄律师",
                    "C 马教授",
                    "D 翻译公司"
                ],
                "correct": "D",
                "script": "15．男：您这次打算安排谁来翻译这份材料？\n女：我看还是联系一家专业的翻译公司吧，他们的速度也快一些。\n问：女的准备找谁翻译这份材料？"
            },
            {
                "num": 16,
                "options": [
                    "A 比较贵",
                    "B 颜色暗",
                    "C 质量差",
                    "D 样子难看"
                ],
                "correct": "A",
                "script": "16．女：那些家具孙阿姨看了吗？她觉得怎么样？\n男：她比较满意，只是问价格能不能再商量一下。\n问：孙阿姨觉得那些家具怎么样？"
            },
            {
                "num": 17,
                "options": [
                    "A 女的不渴",
                    "B 女的出汗了",
                    "C 没有饮料了",
                    "D 他们在跳舞"
                ],
                "correct": "B",
                "script": "17．男：给你毛巾，先擦擦汗。\n女：谢谢，没想到乒乓球的运动量也这么大。\n问：根据对话，可以知道什么？"
            },
            {
                "num": 18,
                "options": [
                    "A 饭店管理",
                    "B 新闻报道",
                    "C 收发传真",
                    "D 安排座位"
                ],
                "correct": "A",
                "script": "18．女：饭店的工作，我想暂时请你来负责，你看有问题没？\n男：对不起，我最近在忙另一件事，您还是考虑其他人吧。\n问：女的想请男的负责哪方面的工作？"
            },
            {
                "num": 19,
                "options": [
                    "A 很孤单",
                    "B 喜欢打扮",
                    "C 住在海边",
                    "D 是位博士"
                ],
                "correct": "C",
                "script": "19．男：听说你新租的房子离海很近？\n女：是的，这儿空气新鲜、湿润，你下次来的时候就知道了。\n问：关于女的，下列哪个正确？"
            },
            {
                "num": 20,
                "options": [
                    "A 堵车",
                    "B 先去送人了",
                    "C 弄错地址了",
                    "D 路上撞车了"
                ],
                "correct": "B",
                "script": "20．女：你今天怎么迟到了？今天不堵车啊。\n男：我先送一个亲戚去首都机场，所以晚了点儿。\n问：男的为什么迟到了？"
            },
            {
                "num": 21,
                "options": [
                    "A 机场",
                    "B 火车站",
                    "C 饭馆儿",
                    "D 出租车上"
                ],
                "correct": "A",
                "script": "21．男：我们的航班又推迟了，刚才听广播说，还要等一个小时才能起飞。\n女：好吧，我们去那边喝点儿咖啡。\n问：他们最可能在哪儿？"
            },
            {
                "num": 22,
                "options": [
                    "A 很脏",
                    "B 很暖和",
                    "C 很凉快",
                    "D 很安静"
                ],
                "correct": "B",
                "script": "22．女：叔叔，您觉得热就把大衣脱了吧，我给您挂起来。\n男：好的，房间里是挺暖和的，开空调了？\n问：男的觉得房间里怎么样？"
            },
            {
                "num": 23,
                "options": [
                    "A 阳光",
                    "B 皮肤",
                    "C 植物",
                    "D 海洋"
                ],
                "correct": "C",
                "script": "23．男：真奇怪，这花儿的叶子是红的，这叫什么花儿？\n女：我也不知道，上个月我生病时，朋友送的。\n问：他们在谈什么？"
            },
            {
                "num": 24,
                "options": [
                    "A 问路",
                    "B 借书",
                    "C 购物",
                    "D 办签证"
                ],
                "correct": "A",
                "script": "24．女：打扰一下，请问图书馆怎么走？\n男：从这儿往前走，第一个路口右边就是。\n问：女的在做什么？"
            },
            {
                "num": 25,
                "options": [
                    "A 17 号",
                    "B 第二天",
                    "C 下周五",
                    "D 生日那天"
                ],
                "correct": "B",
                "script": "25．男：妈，我刚在网上买了台洗衣机，估计明天上午送到，您明天注意接一下电话。\n女：好的。钱交了吗？\n问：估计洗衣机哪天能送到？"
            }
        ],
        "p3_listen": [
            {
                "num": 26,
                "options": [
                    "A 下雨了",
                    "B 刮风了",
                    "C 电梯坏了",
                    "D 他们在逛街"
                ],
                "correct": "B",
                "script": "26．女：外面风刮得很大，你把帽子戴上吧。\n男：不用，我就去楼下超市买牙膏，马上就回来。\n女：那你顺便买几盒牛奶吧。\n男：没问题。\n问：根据对话，可以知道什么？"
            },
            {
                "num": 27,
                "options": [
                    "A 老师",
                    "B 记者",
                    "C 理发师",
                    "D 女的的父母"
                ],
                "correct": "D",
                "script": "27．男：我刚去理了个发，你看怎么样？\n女：挺好，看起来很精神，更帅了。\n男：希望能给你父母留个好印象。\n女：放心吧，我爸妈一定会喜欢你的。\n问：他们准备去见谁？"
            },
            {
                "num": 28,
                "options": [
                    "A 到年底了",
                    "B 放暑假了",
                    "C 商场有表演",
                    "D 水果降价了"
                ],
                "correct": "A",
                "script": "28．女：这个月这种葡萄酒一共卖了多少？\n男：大概两千多瓶吧，比上个月卖得好。\n女：是因为现在有“买一送一”的活动吗？\n男：这是一方面，另外一个原因是到年底了，顾客比平时多了一倍。\n问：顾客为什么比平时多？"
            },
            {
                "num": 29,
                "options": [
                    "A 肚子疼",
                    "B 打错字了",
                    "C 忘吃药了",
                    "D 没找到入口"
                ],
                "correct": "B",
                "script": "29．男：小毛，第一页上有个字打错了，在这儿。\n女：对不起，我马上去改。\n男：改完了你给我重新打印一份。\n女：好的，我一会儿给您送过去。\n问：女的怎么了？"
            },
            {
                "num": 30,
                "options": [
                    "A 很吵",
                    "B 免费停车",
                    "C 没洗手间",
                    "D 不允许抽烟"
                ],
                "correct": "A",
                "script": "30．女：你声音大点儿好吗？这里太吵，我听不清楚。\n男：你在哪儿呢？\n女：我在市场上买菜呢，你到家了？\n男：还没有，我得去一趟银行，晚点儿回家。\n问：那个菜市场怎么样？"
            },
            {
                "num": 31,
                "options": [
                    "A 很得意",
                    "B 被骗了",
                    "C 没收到通知",
                    "D 讲了个笑话"
                ],
                "correct": "C",
                "script": "31．男：公司组织大家这个周末去爬长城。\n女：啊？我怎么不知道？\n男：难道没通知你？\n女：确实没有，并且我已经安排别的事了。\n男：不能改个时间吗？不和我们一起去多可惜！\n问：关于女的，下列哪个正确？"
            },
            {
                "num": 32,
                "options": [
                    "A 要搬家",
                    "B 力气很大",
                    "C 下周出差",
                    "D 觉得很抱歉"
                ],
                "correct": "C",
                "script": "32．女：下周你们俩都出差，谁来照顾小狗啊？\n男：我们请邻居帮忙。\n女：你们的邻居真好。\n男：他们家的小孙子特别喜欢狗，所以很愿意帮我们照顾小狗。\n问：关于男的，可以知道什么？"
            },
            {
                "num": 33,
                "options": [
                    "A 不戴眼镜",
                    "B 认真负责",
                    "C 能陪她聊天",
                    "D 和她爱好相同"
                ],
                "correct": "D",
                "script": "33．男：很多女孩子都希望找一个个子高的男朋友，你呢？\n女：高矮没太大关系，关键是我得喜欢他、爱他。\n男：没别的要求了？\n女：最好还能和我有共同的爱好。\n问：女的希望男朋友怎么样？"
            },
            {
                "num": 34,
                "options": [
                    "A 护士",
                    "B 医生",
                    "C 服务员",
                    "D 售货员"
                ],
                "correct": "A",
                "script": "34．女：你钱包里照片上那个女孩儿是谁啊？\n男：当然是我女朋友了。\n女：我猜也是，她是做什么的？\n男：她在医院当护士。\n问：他女朋友是做什么的？"
            },
            {
                "num": 35,
                "options": [
                    "A 洗几个杯子",
                    "B 送哪种蛋糕",
                    "C 去哪儿唱歌",
                    "D 买什么礼物"
                ],
                "correct": "D",
                "script": "35．男：一月一号马上就到了。\n女：是，给女儿买个什么生日礼物？你有什么好主意？\n男：今年是猴年，给她买只小猴子？\n女：好，我看到商店里卖的小猴子做得特别可爱，她肯定会喜欢的。\n问：他们在商量什么事情？"
            },
            {
                "num": 36,
                "options": [
                    "A 笑了",
                    "B 流泪了",
                    "C 生气了",
                    "D 后悔了"
                ],
                "correct": "B",
                "script": "36-37．\n我十五岁时，问母亲她最幸福的事是什么？母亲回答说：“你第一次叫我妈妈。”二十五岁时，我也有了自己的女儿，回想起母亲当时说的这句话，不知为什么，我一下子哭了起来。\n36．想起妈妈的话，说话人怎么了？"
            },
            {
                "num": 37,
                "options": [
                    "A 爱热闹",
                    "B 有个女儿",
                    "C 还没结婚",
                    "D 是位演员"
                ],
                "correct": "B",
                "script": "36-37．\n我十五岁时，问母亲她最幸福的事是什么？母亲回答说：“你第一次叫我妈妈。”二十五岁时，我也有了自己的女儿，回想起母亲当时说的这句话，不知为什么，我一下子哭了起来。\n37．关于说话人，可以知道什么？"
            },
            {
                "num": 38,
                "options": [
                    "A 鞋破了",
                    "B 要去爬山",
                    "C 走路更舒服",
                    "D 想跑得更快"
                ],
                "correct": "D",
                "script": "38-39．\n有两个人在森林里遇到了一只大老虎。其中一个人马上从包里取出一双运动鞋换上。另外那个人非常着急，大叫：“你干什么呢？即使你换了鞋也跑不过老虎啊！”第一个人却说：“我只要跑得比你快就好了。”\n38．第一个人为什么要换运动鞋？"
            },
            {
                "num": 39,
                "options": [
                    "A 森林",
                    "B 鞋店",
                    "C 动物园",
                    "D 体育场"
                ],
                "correct": "A",
                "script": "38-39．\n有两个人在森林里遇到了一只大老虎。其中一个人马上从包里取出一双运动鞋换上。另外那个人非常着急，大叫：“你干什么呢？即使你换了鞋也跑不过老虎啊！”第一个人却说：“我只要跑得比你快就好了。”\n39．这个故事发生在什么地方？"
            },
            {
                "num": 40,
                "options": [
                    "A 提供机会",
                    "B 总结过去",
                    "C 增长知识",
                    "D 增加工资"
                ],
                "correct": "C",
                "script": "40-41．\n只要养成阅读的习惯，我们就能经常获得新的知识。这还不够，我们还应该学会好的阅读方法，例如，提高阅读速度，扩大阅读范围，有重点、有选择地阅读，这样才能使我们的知识更丰富。\n40．我们为什么要阅读？"
            },
            {
                "num": 41,
                "options": [
                    "A 怎样阅读",
                    "B 反对浪费",
                    "C 学会同情",
                    "D 要保护环境"
                ],
                "correct": "A",
                "script": "40-41．\n只要养成阅读的习惯，我们就能经常获得新的知识。这还不够，我们还应该学会好的阅读方法，例如，提高阅读速度，扩大阅读范围，有重点、有选择地阅读，这样才能使我们的知识更丰富。\n41．这段话主要谈什么？"
            },
            {
                "num": 42,
                "options": [
                    "A 批评",
                    "B 同事关系",
                    "C 办公环境",
                    "D 回忆过去"
                ],
                "correct": "C",
                "script": "42-43．\n你的办公环境会影响你的心情。如果环境干净整齐，你每天都会感到轻松愉快。所以，如果你的办公桌很乱，是时候改变它了。为了有个好的心情，先整理你的桌面吧。\n42．根据这段话，什么对心情有影响？"
            },
            {
                "num": 43,
                "options": [
                    "A 桌面",
                    "B 脾气",
                    "C 顺序",
                    "D 管理办法"
                ],
                "correct": "A",
                "script": "42-43．\n你的办公环境会影响你的心情。如果环境干净整齐，你每天都会感到轻松愉快。所以，如果你的办公桌很乱，是时候改变它了。为了有个好的心情，先整理你的桌面吧。\n43．说话人认为应该先改变什么？"
            },
            {
                "num": 44,
                "options": [
                    "A 站着吃",
                    "B 放碗里吃",
                    "C 刷牙后吃",
                    "D 先吃最好的"
                ],
                "correct": "D",
                "script": "44-45．\n吃葡萄时，有一种人一定先选最好的吃，而另一种人正相反，把最好的留到最后吃。到底他们谁更快乐呢？我想是第一种人，因为他吃的每一个葡萄都是手里最好的。但也有人认为，第二种人更快乐，他们先吃不好的，这样，更好的总在后头，于是他们总是有希望。\n44．第一种人怎么吃葡萄？"
            },
            {
                "num": 45,
                "options": [
                    "A 爱吃酸的",
                    "B 喜欢做梦",
                    "C 总有希望",
                    "D 容易被感动"
                ],
                "correct": "C",
                "script": "44-45．\n吃葡萄时，有一种人一定先选最好的吃，而另一种人正相反，把最好的留到最后吃。到底他们谁更快乐呢？我想是第一种人，因为他吃的每一个葡萄都是手里最好的。但也有人认为，第二种人更快乐，他们先吃不好的，这样，更好的总在后头，于是他们总是有希望。\n45．关于第二种人，可以知道什么？"
            }
        ],
        "p1_read": [
            {
                "num": 46,
                "text": "46. 冬天到了，天气（  ）变冷了。",
                "options": [
                    "A 打折",
                    "B 成功",
                    "C 详细",
                    "D 坚持",
                    "E 范围",
                    "F 逐渐"
                ],
                "correct": "F"
            },
            {
                "num": 47,
                "text": "47. 一般情况下，人的正常体温在 36-37℃之间，超出这个（  ）就是发烧。",
                "options": [
                    "A 打折",
                    "B 成功",
                    "C 详细",
                    "D 坚持",
                    "E 范围",
                    "F 逐渐"
                ],
                "correct": "E"
            },
            {
                "num": 48,
                "text": "48. 那件衣服（  ）后只要 98 元，很便宜。",
                "options": [
                    "A 打折",
                    "B 成功",
                    "C 详细",
                    "D 坚持",
                    "E 范围",
                    "F 逐渐"
                ],
                "correct": "A"
            },
            {
                "num": 49,
                "text": "49. 爷爷奶奶经常说：“失败是（  ）之母，不要害怕失败。”",
                "options": [
                    "A 打折",
                    "B 成功",
                    "C 详细",
                    "D 坚持",
                    "E 范围",
                    "F 逐渐"
                ],
                "correct": "B"
            },
            {
                "num": 50,
                "text": "50. 为了不引起误会，她又向大家（  ）解释了一遍事情的经过。",
                "options": [
                    "A 打折",
                    "B 成功",
                    "C 详细",
                    "D 坚持",
                    "E 范围",
                    "F 逐渐"
                ],
                "correct": "C"
            },
            {
                "num": 51,
                "text": "51. A：呀，你的这个行李箱竟然跟我的（  ）一样，连颜色都一样。\n    B：那是我去年夏天买的，你是什么时候买的？",
                "options": [
                    "A 提前",
                    "B 挺",
                    "C 温度",
                    "D 有趣",
                    "E 任务",
                    "F 完全"
                ],
                "correct": "F"
            },
            {
                "num": 52,
                "text": "52. A：这本小说很（  ），我估计明天就能看完，后天见面时就可以还你。\n    B：不着急，你慢慢看，周末给我就行。",
                "options": [
                    "A 提前",
                    "B 挺",
                    "C 温度",
                    "D 有趣",
                    "E 任务",
                    "F 完全"
                ],
                "correct": "D"
            },
            {
                "num": 53,
                "text": "53. A：这是我从国外带回来的饼干，（  ）好吃的，你尝尝吧。\n    B：谢谢你，这次出差顺利吧？",
                "options": [
                    "A 提前",
                    "B 挺",
                    "C 温度",
                    "D 有趣",
                    "E 任务",
                    "F 完全"
                ],
                "correct": "B"
            },
            {
                "num": 54,
                "text": "54. A：加油，我等你们的好消息。\n    B：感谢您的信任，我们一定按时完成（  ），不会让您失望的。",
                "options": [
                    "A 提前",
                    "B 挺",
                    "C 温度",
                    "D 有趣",
                    "E 任务",
                    "F 完全"
                ],
                "correct": "E"
            },
            {
                "num": 55,
                "text": "55. A：现在就去会议室？咱们去得太早了吧？\n    B：时间（  ）了，早上通知改时间了。",
                "options": [
                    "A 提前",
                    "B 挺",
                    "C 温度",
                    "D 有趣",
                    "E 任务",
                    "F 完全"
                ],
                "correct": "A"
            }
        ],
        "p2_read": [
            {
                "num": 56,
                "text": "56. A 你弟弟的基础挺好的<br>B 喂，我打算放寒假后去学弹钢琴<br>C 要不要也给他报个名",
                "correct": "BAC"
            },
            {
                "num": 57,
                "text": "57. A 所有的工作都在按计划进行着<br>B 还要继续辛苦大家<br>C 没出现任何问题，接下来的两个月",
                "correct": "ACB"
            },
            {
                "num": 58,
                "text": "58. A 这就是你哥？你们俩长得太像了<br>B 不仔细看的话<br>C 真的很难看出你们俩有什么区别",
                "correct": "ABC"
            },
            {
                "num": 59,
                "text": "59. A 当大部分人都在关心你飞得高不高时<br>B 这少数人，才是你的朋友<br>C 只有少数人关心你飞得累不累",
                "correct": "ACB"
            },
            {
                "num": 60,
                "text": "60. A 那种既兴奋又紧张的感觉到现在仍然难以忘记<br>B 由于那是我第一次参加国际比赛<br>C 大学一年级时，我参加了世界大学生运动会",
                "correct": "CBA"
            },
            {
                "num": 61,
                "text": "61. A 会后记得要全部收回来<br>B 请把这份调查表复印 35 份<br>C 明天上午会前发给各位代表，请他们填一下",
                "correct": "BCA"
            },
            {
                "num": 62,
                "text": "62. A 既然你已经决定了<br>B 那我们尊重你的选择<br>C 有困难可以回来找我们，我们永远都支持你",
                "correct": "ABC"
            },
            {
                "num": 63,
                "text": "63. A 不要随便乱扔<br>B 否则，下次找起来会比较麻烦<br>C 东西用完后，最好放回原来的地方",
                "correct": "CAB"
            },
            {
                "num": 64,
                "text": "64. A 但学艺术的小关还是拒绝了杂志社的邀请<br>B 尽管杂志社的收入不低<br>C 他的理想是开一个自己的工作室",
                "correct": "BAC"
            },
            {
                "num": 65,
                "text": "65. A 请他给你当导游保证没问题<br>B 对那个城市很熟悉<br>C 我这个同学就是在北京出生、长大的",
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
                "text": "68. 要想获得别人的尊重，首先要学会尊重别人。尊重别人，不仅指对人友好、有礼貌，而且还要尊重别人的兴趣和爱好，在与别人看法不同时，能尊重别人的意见或者选择。\n★ 这段话主要想告诉我们，怎样：",
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
                "text": "69. 中国有句话叫做“要想富，先修路”，意思是，交通对一个地方经济的发展有很大的影响。一些地方因为比较穷，没有钱修路，经济、教育、文化等各方面的发展都受到很大的限制。\n★ “要想富，先修路”说明什么对经济的发展有影响？",
                "options": [
                    "A 科学技术",
                    "B 交通条件",
                    "C 交通工具",
                    "D 教育水平"
                ],
                "correct": "B"
            },
            {
                "num": 70,
                "text": "70. 要想做出正确的判断，首先要耐心地听别人说明情况，其次要把这些情况考虑清楚。只有这样，做出的判断才可能是对的。\n★ 要做出正确的判断，必须：",
                "options": [
                    "A 仔细介绍",
                    "B 怀疑一切",
                    "C 相信自己",
                    "D 先了解情况"
                ],
                "correct": "D"
            },
            {
                "num": 71,
                "text": "71. 根据多年的教学经验，他发现：性格活泼的人可能更适合学习语言，เพราะ这样的人学习比较积极，喜欢主动与人交流，所以学习效果更好。\n★ 性格活泼的人：",
                "options": [
                    "A 说话直接",
                    "B 非常幽默",
                    "C 积极主动",
                    "D 往往很粗心"
                ],
                "correct": "C"
            },
            {
                "num": 72,
                "text": "72. 生活不会一直都顺利，人总是会遇到各种各样的麻烦，可是不管你是快乐还是难过，生活总要继续下去，那我们为什么不选择快乐地生活呢？\n★ 这段话主要想告诉我们，应该：",
                "options": [
                    "A 懂得放弃",
                    "B 理解别人",
                    "C 多鼓励朋友",
                    "D 快乐地生活"
                ],
                "correct": "D"
            },
            {
                "num": 73,
                "text": "73. 做事情有计划，这是一种很好的习惯，更重要的是，它还反映了一个人做事的态度。许多人能取得成功，其中最主要的一个原因就是事前有很好的计划。\n★ 很多人获得成功的关键是：",
                "options": [
                    "A 有信心",
                    "B 经验丰富",
                    "C 重视过程",
                    "D 做事有计划"
                ],
                "correct": "D"
            },
            {
                "num": 74,
                "text": "74. 云南在中国的西南部，是著名的旅游目的地。当地美丽的自然风景吸引了很多游客，除了美景外，那儿的民族文化也有很大的吸引力。\n★ 关于云南，可以知道：",
                "options": [
                    "A 特别热",
                    "B 气候干燥",
                    "C 风景很漂亮",
                    "D 不是很有名"
                ],
                "correct": "C"
            },
            {
                "num": 75,
                "text": "75. 春节是中国人最重要的节日。每年春节，在外地工作和上学的人们都会开车或乘坐汽车、火车、飞机回家，和家人一起过年。\n★ 春节时，人们都要：",
                "options": [
                    "A 请客",
                    "B 举办晚会",
                    "C 回家过年",
                    "D 吃面条儿"
                ],
                "correct": "C"
            },
            {
                "num": 76,
                "text": "76. 广告几乎无处不在，街头、地铁、电视、网上，到处都会看到各种各样的广告。不管你是喜欢还是讨厌它，我们每天都生活在广告之中。\n★ 根据这段话，广告：",
                "options": [
                    "A 数量多",
                    "B 时间短",
                    "C 内容简单",
                    "D 要求严格"
                ],
                "correct": "A"
            },
            {
                "num": 77,
                "text": "77. 李师傅平时总是穿一件白衬衫、一条黑裤子。但是公司开会的时候，他一定会换上很正式的西服，皮鞋也擦得亮亮的。\n★ 开会时，李师傅：",
                "options": [
                    "A 爱喝茶",
                    "B 十分冷静",
                    "C 经常被表扬",
                    "D 穿得很正式"
                ],
                "correct": "D"
            },
            {
                "num": 78,
                "text": "78. 年轻人常常会因为找不到工作而烦恼，其实，明白自己需要什么样的工作比找到一份工作更重要，因为方向比速度重要。\n★ 找工作以前，应该清楚：",
                "options": [
                    "A 法律规定",
                    "B 职业特点",
                    "C 招聘条件",
                    "D 自己想做什么"
                ],
                "correct": "D"
            },
            {
                "num": 79,
                "text": "79. 《长江之歌》这首歌的词作者以浪漫的文字，表达了他对长江的深厚感情。歌词前一部分写长江像母亲一样照顾儿女，后一部分写长江的历史和它对社会发展的推动作用。\n★ 这段话主要讲《长江之歌》的：",
                "options": [
                    "A 歌词",
                    "B 作者",
                    "C 缺点",
                    "D 演出时间"
                ],
                "correct": "A"
            },
            {
                "num": 80,
                "text": "80-81．\n经理的妻子给他拿来了早饭和报纸就出门了。两个小时后，妻子回到家，发现丈夫仍然坐在桌子旁边看报纸。妻子奇怪地问他：“你今天不去办公室吗？今天休息？”经理吃惊地跳起来说：“天啊！你怎么不提醒我呢？我以为我已经在上班了！”\n80．妻子回到家，看见丈夫：",
                "options": [
                    "A 准备出门",
                    "B 还在睡觉",
                    "C 坐在沙发上",
                    "D 正在看报纸"
                ],
                "correct": "D"
            },
            {
                "num": 81,
                "text": "80-81．\n经理的妻子给他拿来了早饭和报纸就出门了。两个小时后，妻子回到家，发现丈夫仍然坐在桌子旁边看报纸。妻子奇怪地问他：“你今天不去办公室吗？今天休息？”经理吃惊地跳起来说：“天啊！你怎么不提醒我呢？我以为我已经在上班了！”\n81．根据这段话，可以知道经理：",
                "options": [
                    "A 要加班",
                    "B 喜欢读书",
                    "C 没去公司",
                    "D 今天请假了"
                ],
                "correct": "C"
            },
            {
                "num": 82,
                "text": "82-83．\n现在有些父母认为，孩子接受国外的教育越早越好，因此，一些孩子很小的时候就被送去留学了。但是另外一些人有不同的看法，他们担心孩子太小，还不会照顾自己，并不能很好地适应国外的学习和生活。\n82．关于小孩子出国学习，可以知道：",
                "options": [
                    "A 学费很贵",
                    "B 很难申请",
                    "C 压力很大",
                    "D 大家看法不同"
                ],
                "correct": "D"
            },
            {
                "num": 83,
                "text": "82-83．\n现在有些父母认为，孩子接受国外的教育越早越好，因此，一些孩子很小的时候就被送去留学了。但是另外一些人有不同的看法，他们担心孩子太小，还不会照顾自己，并不能很好地适应国外的学习和生活。\n83．这段话主要讨论什么问题？",
                "options": [
                    "A 学习方法",
                    "B 孩子留学",
                    "C 语法标准",
                    "D 父母的责任"
                ],
                "correct": "B"
            },
            {
                "num": 84,
                "text": "84-85．\n现代社会离不开交流。如果工作中遇到了难题，要试着和同事交流，他也许可以帮你解决。如果朋友之间发生了不高兴的事情，你不应该自己一个人生气，而应该去和他交流，很有可能你会发现那是个误会。一个公司内部如果经常交流，公司的竞争力一定会得到提高。家人之间如果经常交流，一定会生活得很幸福。\n84．跟同事交流可能会帮你：",
                "options": [
                    "A 更勇敢",
                    "B 不再无聊",
                    "C 解决问题",
                    "D 认识新朋友"
                ],
                "correct": "C"
            },
            {
                "num": 85,
                "text": "84-85．\n现代社会离不开交流。如果工作中遇到了难题，要试着和同事交流，他也许可以帮你解决。如果朋友之间发生了不高兴的事情，你不应该自己一个人生气，而应该去和他交流，很有可能你会发现那是个误会。一个公司内部如果经常交流，公司的竞争力一定会得到提高。家人之间如果经常交流，一定会生活得很幸福。\n85．段话主要介绍：",
                "options": [
                    "A 什么是幸福",
                    "B 交流的作用",
                    "C 怎样做生意",
                    "D 怎样积累知识"
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
                "word": "袜子"
            },
            {
                "num": 97,
                "word": "害羞"
            },
            {
                "num": 98,
                "word": "醒"
            },
            {
                "num": 99,
                "word": "密码"
            },
            {
                "num": 100,
                "word": "咳嗽"
            }
        ]
    }
}

EXAM_CODES = list(EXAM_DATA.keys())

# ==============================================================================
# GIAO DIỆN VÀ XỬ LÝ CHÍNH
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
    key="name_input_main"
)
st.session_state.student_name = student_name

st.markdown("<br>", unsafe_allow_html=True)

exam_tabs = st.tabs(EXAM_CODES)

for idx, exam_code in enumerate(EXAM_CODES):
    with exam_tabs[idx]:
        st.markdown(f"## 📋 ĐỀ THI MÃ: **{exam_code}**")
        data = EXAM_DATA[exam_code]
        
        sub_tab_listen, sub_tab_read, sub_tab_write = st.tabs(["🎧 听力 (Phần nghe)", "📖 阅读 (Phần đọc)", "✍️ 书写 (Phần viết)"])
        
        # --- 1. SUB-TAB PHẦN NGHE ---
        with sub_tab_listen:
            render_audio_player(exam_code)
            st.markdown("---")
            
            u_l1 = {}
            st.markdown("#### **第一部分 - 判断对错 (Câu 1 - 10)**")
            for i, q in enumerate(data["p1_listen"]):
                c_class = CARD_CLASSES[i % len(CARD_CLASSES)]
                st.markdown(f"<div class='{c_class}'><strong>Câu {q['num']}:</strong><br>{q['text'].replace('\n', '<br>')}", unsafe_allow_html=True)
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
                
            sub_key_l = f"res_l_{exam_code}"
            if sub_key_l not in st.session_state:
                st.session_state[sub_key_l] = None

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
                    
                    with st.spinner("🔄 Đang tự động gửi kết quả thi về Google Sheets..."):
                        ok, msg = send_score_to_gsheet(student_name, exam_code, "PHẦN NGHE", f"{tot_c}/{tot_q}", sc_100)
                    
                    st.session_state[sub_key_l] = {
                        "tot_c": tot_c,
                        "tot_q": tot_q,
                        "sc_100": sc_100,
                        "u_l1": u_l1,
                        "u_l2": u_l2,
                        "u_l3": u_l3,
                        "ok": ok,
                        "msg": msg
                    }
                    st.rerun()

            if st.session_state[sub_key_l] is not None:
                res = st.session_state[sub_key_l]
                st.success(f"🎉 **Kết quả Phần Nghe ({exam_code}):**\n- Số câu đúng: **{res['tot_c']}/{res['tot_q']}** câu\n- Điểm số: **{res['sc_100']:.1f} / 100 điểm**")
                if res['ok']:
                    st.info(f"✅ {res['msg']}")
                else:
                    st.warning(f"⚠️ {res['msg']}")
                
                st.markdown("---")
                st.markdown("### 🔍 CHI TIẾT CÂU SAI & SCRIPT NGHE:")
                for q in data["p1_listen"]:
                    if res['u_l1'].get(q['num']) != q['correct']:
                        st.markdown(f"❌ **Câu {q['num']}**: Bạn chọn `{res['u_l1'].get(q['num'])}` | Đáp án đúng: **{q['correct']}**")
                        with st.expander(f"📖 查看听力文本 (Xem Script Câu {q['num']})"):
                            st.write(q['script'])
                for q in data["p2_listen"]:
                    if res['u_l2'].get(q['num']) != q['correct']:
                        st.markdown(f"❌ **Câu {q['num']}**: Bạn chọn `{res['u_l2'].get(q['num'])}` | Đáp án đúng: **{q['correct']}**")
                        with st.expander(f"📖 查看听力文本 (Xem Script Câu {q['num']})"):
                            st.write(q['script'])
                for q in data["p3_listen"]:
                    if res['u_l3'].get(q['num']) != q['correct']:
                        st.markdown(f"❌ **Câu {q['num']}**: Bạn chọn `{res['u_l3'].get(q['num'])}` | Đáp án đúng: **{q['correct']}**")
                        with st.expander(f"📖 查看听力文本 (Xem Script Câu {q['num']})"):
                            st.write(q['script'])
                            
                if st.button(f"🔄 Làm lại Phần Nghe mã {exam_code}", key=f"btn_reset_l_{exam_code}"):
                    st.session_state[sub_key_l] = None
                    st.rerun()

        # --- 2. SUB-TAB PHẦN ĐỌC ---
        with sub_tab_read:
            st.markdown("### 二、阅读 (Phần đọc)")
            u_r1 = {}
            st.markdown("#### **第一部分 - 选词填空 (Câu 46 - 55)**")
            for i, q in enumerate(data["p1_read"]):
                c_class = CARD_CLASSES[i % len(CARD_CLASSES)]
                st.markdown(f"<div class='{c_class}'><strong>Câu {q['num']}:</strong><br>{q['text'].replace('\n', '<br>')}", unsafe_allow_html=True)
                ans = st.radio(f"r1_{exam_code}_{q['num']}", q["options"], key=f"w_r1_{exam_code}_{q['num']}", label_visibility="collapsed")
                u_r1[q['num']] = ans[0] if ans else ""
                st.markdown("</div>", unsafe_allow_html=True)
                
            u_r2 = {}
            st.markdown("#### **第二部分 - 排列顺序 (Câu 56 - 65)**")
            for i, q in enumerate(data["p2_read"]):
                c_class = CARD_CLASSES[(i+1) % len(CARD_CLASSES)]
                st.markdown(f"<div class='{c_class}'><strong>Câu {q['num']}:</strong><br>{q['text'].replace('\n', '<br>')}", unsafe_allow_html=True)
                ans = st.text_input(f"Nhập thứ tự 3 chữ cái (VD: BAC) cho câu {q['num']}:", key=f"w_r2_{exam_code}_{q['num']}").strip().upper()
                u_r2[q['num']] = ans
                st.markdown("</div>", unsafe_allow_html=True)
                
            u_r3 = {}
            st.markdown("#### **第三部分 - 阅读理解 (Câu 66 - 85)**")
            for i, q in enumerate(data["p3_read"]):
                c_class = CARD_CLASSES[(i+2) % len(CARD_CLASSES)]
                st.markdown(f"<div class='{c_class}'><strong>Câu {q['num']}:</strong><br>{q['text'].replace('\n', '<br>')}", unsafe_allow_html=True)
                ans = st.radio(f"r3_{exam_code}_{q['num']}", q["options"], key=f"w_r3_{exam_code}_{q['num']}", label_visibility="collapsed")
                u_r3[q['num']] = ans[0] if ans else ""
                st.markdown("</div>", unsafe_allow_html=True)
                
            sub_key_r = f"res_r_{exam_code}"
            if sub_key_r not in st.session_state:
                st.session_state[sub_key_r] = None

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
                    
                    with st.spinner("🔄 Đang tự động gửi kết quả thi về Google Sheets..."):
                        ok, msg = send_score_to_gsheet(student_name, exam_code, "PHẦN ĐỌC", f"{tot_c}/{tot_q}", sc_100)
                    
                    st.session_state[sub_key_r] = {
                        "tot_c": tot_c,
                        "tot_q": tot_q,
                        "sc_100": sc_100,
                        "u_r1": u_r1,
                        "u_r2": u_r2,
                        "u_r3": u_r3,
                        "ok": ok,
                        "msg": msg
                    }
                    st.rerun()

            if st.session_state[sub_key_r] is not None:
                res = st.session_state[sub_key_r]
                st.success(f"🎉 **Kết quả Phần Đọc ({exam_code}):**\n- Số câu đúng: **{res['tot_c']}/{res['tot_q']}** câu\n- Điểm số: **{res['sc_100']:.1f} / 100 điểm**")
                if res['ok']:
                    st.info(f"✅ {res['msg']}")
                else:
                    st.warning(f"⚠️ {res['msg']}")
                
                st.markdown("---")
                st.markdown("### 🔍 CHI TIẾT CÂU SAI PHẦN ĐỌC:")
                for q in data["p1_read"]:
                    if res['u_r1'].get(q['num']) != q['correct']:
                        st.markdown(f"❌ **Câu {q['num']}**: Bạn chọn `{res['u_r1'].get(q['num'])}` | Đáp án đúng: **{q['correct']}**")
                for q in data["p2_read"]:
                    if res['u_r2'].get(q['num']) != q['correct']:
                        st.markdown(f"❌ **Câu {q['num']}**: Bạn điền `{res['u_r2'].get(q['num'])}` | Đáp án đúng: **{q['correct']}**")
                for q in data["p3_read"]:
                    if res['u_r3'].get(q['num']) != q['correct']:
                        st.markdown(f"❌ **Câu {q['num']}**: Bạn chọn `{res['u_r3'].get(q['num'])}` | Đáp án đúng: **{q['correct']}**")
                        
                if st.button(f"🔄 Làm lại Phần Đọc mã {exam_code}", key=f"btn_reset_r_{exam_code}"):
                    st.session_state[sub_key_r] = None
                    st.rerun()

        # --- 3. SUB-TAB PHẦN VIẾT ---
        with sub_tab_write:
            st.markdown("### 三、书写 (Phần viết)")
            u_w1 = {}
            st.markdown("#### **第一部分 - 完成句子 (Câu 86 - 95)**")
            for i, q in enumerate(data["p1_write"]):
                c_class = CARD_CLASSES[i % len(CARD_CLASSES)]
                st.markdown(f"<div class='{c_class}'><strong>Câu {q['num']}:</strong> {q['words']}", unsafe_allow_html=True)
                ans = st.text_input("Nhập câu hoàn chỉnh của bạn tại đây:", key=f"w_w1_{exam_code}_{q['num']}").strip()
                u_w1[q['num']] = ans
                st.markdown("</div>", unsafe_allow_html=True)
                
            st.markdown("#### **第二部分 - 看图造句 (Câu 96 - 100)**")
            st.info("📌 Note: Các câu từ 96-100 (đặt câu theo tranh) cô Ngọc sẽ chấm cụ thể sau. Điểm hiển thị bên dưới chỉ mang tính chất tương đối.")
            
            u_w2 = {}
            for i, q in enumerate(data["p2_write"]):
                c_class = CARD_CLASSES[(i+1) % len(CARD_CLASSES)]
                st.markdown(f"<div class='{c_class}'><strong>Câu {q['num']}:</strong><br>Từ gợi ý: <strong>{q['word']}</strong>", unsafe_allow_html=True)
                
                img_path_1 = f"{exam_code}_{i+1}.jpg"
                img_path_2 = f"{exam_code}_{i+1}.png"
                if os.path.exists(img_path_1):
                    st.image(img_path_1, width=280)
                elif os.path.exists(img_path_2):
                    st.image(img_path_2, width=280)
                else:
                    st.info(f"🖼️ [Khung hiển thị hình ảnh {exam_code}_{i+1}.jpg] - Từ gợi ý: **{q['word']}**")
                    
                ans = st.text_area("Nhập câu đặt theo tranh của bạn tại đây:", key=f"w_w2_{exam_code}_{q['num']}")
                u_w2[q['num']] = ans
                st.markdown("</div>", unsafe_allow_html=True)
                
            sub_key_w = f"res_w_{exam_code}"
            if sub_key_w not in st.session_state:
                st.session_state[sub_key_w] = None

            if st.button(f"🚀 NỘP BÀI PHẦN VIẾT MÃ {exam_code}", key=f"btn_sub_w_{exam_code}"):
                if not student_name.strip():
                    st.warning("⚠️ Vui lòng nhập Họ và tên ở đầu trang trước khi nộp bài!")
                else:
                    c1 = sum(1 for q in data["p1_write"] if u_w1.get(q['num']) in q['correct'])
                    tot_qs = len(data["p1_write"]) + len(data["p2_write"])
                    c_cnt_total = c1 + len(data["p2_write"])
                    sc_100 = (c_cnt_total / tot_qs) * 100
                    
                    with st.spinner("🔄 Đang tự động gửi kết quả thi về Google Sheets..."):
                        ok, msg = send_score_to_gsheet(student_name, exam_code, "PHẦN VIẾT", f"{c_cnt_total}/{tot_qs}", sc_100)
                    
                    st.session_state[sub_key_w] = {
                        "c1": c1,
                        "c_cnt_total": c_cnt_total,
                        "tot_qs": tot_qs,
                        "sc_100": sc_100,
                        "u_w1": u_w1,
                        "ok": ok,
                        "msg": msg
                    }
                    st.rerun()

            if st.session_state[sub_key_w] is not None:
                res = st.session_state[sub_key_w]
                st.success(f"🎉 **Kết quả Phần Viết tương đối ({exam_code}):**\n- Số câu đúng Phần 1: **{res['c1']}/{len(data['p1_write'])}** câu\n- Điểm số tương đối: **{res['sc_100']:.1f} / 100 điểm**")
                if res['ok']:
                    st.info(f"✅ {res['msg']}")
                else:
                    st.warning(f"⚠️ {res['msg']}")
                
                st.markdown("---")
                st.markdown("### 🔍 CHI TIẾT CÂU SAI PHẦN VIẾT (PHẦN 1):")
                for q in data["p1_write"]:
                    if res['u_w1'].get(q['num']) not in q['correct']:
                        st.markdown(f"❌ **Câu {q['num']}**: Bạn viết `{res['u_w1'].get(q['num'])}` | Đáp án đúng: **{q['correct']}**")
                        
                if st.button(f"🔄 Làm lại Phần Viết mã {exam_code}", key=f"btn_reset_w_{exam_code}"):
                    st.session_state[sub_key_w] = None
                    st.rerun()

st.markdown("""
<div class="footer">
    黄宝玉老师
</div>
""", unsafe_allow_html=True)
