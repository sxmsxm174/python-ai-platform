import streamlit as st
import subprocess
import requests
import json
from database import StudyDatabase
from datetime import datetime

# 页面设置
st.set_page_config(
    page_title="AI Python学习平台", 
    page_icon="🎓", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- 自定义CSS美化 ----------
st.markdown("""
<style>
    /* 全局字体 */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* 主标题美化 */
    .main-title {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #ff6b6b 100%);
        padding: 30px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        animation: gradient 5s ease infinite;
        background-size: 200% 200%;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .main-title h1 {
        font-size: 3em;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-title p {
        font-size: 1.2em;
        opacity: 0.9;
    }
    
    /* 侧边栏美化 */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
        border-right: 1px solid #e0e0e0;
    }
    
    /* 按钮美化 */
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 16px;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* 运行按钮特殊颜色 */
    .stButton button:first-child {
        background: linear-gradient(135deg, #00b09b 0%, #96c93d 100%);
    }
    
    /* 代码编辑区 */
    .stTextArea textarea {
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        font-family: 'Consolas', 'Monaco', monospace;
        font-size: 14px;
        line-height: 1.5;
        padding: 15px;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.05);
        transition: border 0.3s;
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* 统计卡片 */
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        transition: transform 0.3s;
        border: 1px solid #f0f0f0;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.1);
    }
    
    .metric-card h3 {
        color: #667eea;
        font-size: 2em;
        margin: 10px 0;
    }
    
    .metric-card p {
        color: #666;
        font-size: 1em;
        margin: 0;
    }
    
    /* 分割线美化 */
    hr {
        background: linear-gradient(90deg, transparent, #667eea, #764ba2, #ff6b6b, transparent);
        height: 3px;
        border: none;
        margin: 30px 0;
        border-radius: 3px;
    }
    
    /* 提示框美化 */
    .stAlert {
        border-radius: 8px;
        border-left: 4px solid #667eea;
        background: #f8f9fa;
    }
    
    /* 题目选择框 */
    .stSelectbox label {
        font-weight: 600;
        color: #333;
    }
    
    /* 聊天消息美化 */
    .stChatMessage {
        background: #f8f9fa;
        border-radius: 15px;
        padding: 10px;
        margin: 5px 0;
        border: 1px solid #e0e0e0;
    }
    
    /* 用户登录卡片 */
    .login-card {
        background: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        margin: 20px 0;
        border: 1px solid #f0f0f0;
    }
</style>
""", unsafe_allow_html=True)

# ---------- 显示主标题 ----------
st.markdown("""
<div class="main-title">
    <h1>🤖 AI赋能Python自主学习平台</h1>
    <p>让AI成为你的专属Python导师 · 边学边练 · 智能答疑</p>
</div>
""", unsafe_allow_html=True)

# ---------- 初始化 ----------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "✨ 你好！我是你的AI助教，有什么Python问题都可以问我~"}
    ]

# ---------- 侧边栏 ----------
with st.sidebar:
    # 用户系统
    if "user_id" not in st.session_state:
        st.session_state.user_id = None
        st.session_state.username = None
        st.session_state.db = StudyDatabase()
    
    st.markdown("### 👤 用户中心")
    
    if st.session_state.user_id is None:
        with st.container():
            st.markdown('<div class="login-card">', unsafe_allow_html=True)
            username = st.text_input("✨ 输入昵称开始学习：", placeholder="例如：小明")
            if st.button("🎓 开始学习之旅", use_container_width=True):
                if username:
                    user_id = st.session_state.db.add_user(username)
                    st.session_state.user_id = user_id
                    st.session_state.username = username
                    st.success(f"欢迎 {username}！")
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.success(f"🌟 欢迎回来，**{st.session_state.username}**")
        if st.button("🔄 切换用户", use_container_width=True):
            st.session_state.user_id = None
            st.session_state.username = None
            st.rerun()
    
    st.divider()
    
    # AI助教
    st.markdown("### 💬 AI智能助教")
    
    # 显示对话历史
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    # 输入框
    user_question = st.chat_input("💭 输入你的Python问题...")
    
    if user_question:
        st.chat_message("user").markdown(user_question)
        st.session_state.messages.append({"role": "user", "content": user_question})
        
        with st.spinner("🤔 AI思考中..."):
            try:
                API_KEY = "6b5591a0d4e64ddebaca3553ae8c028e.qyKA0KPoRLwiz3NU"
                
                url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
                headers = {
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json"
                }
                
                messages = [
                    {"role": "system", "content": "你是Python导师，用简单易懂的语言解释问题，可以给代码例子。"}
                ]
                for msg in st.session_state.messages[-5:]:
                    messages.append(msg)
                
                data = {
                    "model": "glm-4-flash",
                    "messages": messages,
                    "temperature": 0.8
                }
                
                response = requests.post(url, headers=headers, json=data)
                result = response.json()
                
                if 'choices' in result:
                    ai_reply = result['choices'][0]['message']['content']
                else:
                    ai_reply = f"出错了：{result}"
                
                with st.chat_message("assistant"):
                    st.markdown(ai_reply)
                st.session_state.messages.append({"role": "assistant", "content": ai_reply})
                
            except Exception as e:
                st.error(f"调用AI出错：{e}")

# ---------- 主界面 ----------
# 创建两列布局
left_col, right_col = st.columns([2, 1])

with left_col:
    st.markdown("### 📝 Python代码练习")
    
    # 题目选择
    question = st.selectbox(
        "📌 选择练习题：",
        ["打印1到10", "计算1到100的和", "打印偶数", "自定义题目"],
        help="选择一道题目开始练习"
    )
    
    if question == "打印1到10":
        default_code = "for i in range(1, 11):\n    print(i)"
        description = "🎯 使用for循环打印数字1到10，每个数字一行。"
    elif question == "计算1到100的和":
        default_code = "total = 0\nfor i in range(1, 101):\n    total += i\nprint(total)"
        description = "🎯 计算1+2+3+...+100的结果并打印。"
    elif question == "打印偶数":
        default_code = "for i in range(1, 21):\n    if i % 2 == 0:\n        print(i)"
        description = "🎯 打印1到20之间的所有偶数。"
    else:
        default_code = "# 在这里写你的代码\nprint('Hello World')"
        description = "🎯 自由练习，想写什么写什么。"
    
    st.info(description)
    
    # 代码编辑区
    code = st.text_area(
        "📝 代码编辑区：", 
        value=default_code, 
        height=250,
        help="在这里编写Python代码"
    )
    
    # 按钮组
    col1, col2, col3 = st.columns(3)
    with col1:
        run_clicked = st.button("🚀 运行代码", use_container_width=True)
    with col2:
        analyze_clicked = st.button("🔍 AI分析代码", use_container_width=True)
    with col3:
        clear_clicked = st.button("🗑️ 清空输出", use_container_width=True)
    
    # 运行代码
    if run_clicked:
        st.code(code, language="python", line_numbers=True)
        with st.spinner("⏳ 正在运行..."):
            try:
                with open("temp.py", "w", encoding="utf-8") as f:
                    f.write(code)
                result = subprocess.run(
                    ["python", "temp.py"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                output = result.stdout + result.stderr
                
                if output:
                    st.markdown("**📤 运行结果：**")
                    st.code(output, language="text")
                else:
                    st.success("✅ 运行成功，无输出")
                
                # 记录学习记录
                if st.session_state.user_id:
                    st.session_state.db.add_record(
                        st.session_state.user_id,
                        question,
                        code,
                        output[:100] if output else "运行成功"
                    )
                    
            except Exception as e:
                st.error(f"❌ 运行出错：{e}")
    
    # 清空输出
    if clear_clicked:
        st.info("输出已清空")

with right_col:
    # AI分析结果显示区
    if analyze_clicked:
        with st.spinner("🤖 AI正在分析代码..."):
            try:
                API_KEY = "6b5591a0d4e64ddebaca3553ae8c028e.qyKA0KPoRLwiz3NU"
                
                url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
                headers = {
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json"
                }
                
                prompt = f"请分析下面这段Python代码，给出改进建议：\n```python\n{code}\n```"
                
                data = {
                    "model": "glm-4-flash",
                    "messages": [
                        {"role": "system", "content": "你是Python导师，分析代码并给出改进建议。"},
                        {"role": "user", "content": prompt}
                    ]
                }
                
                response = requests.post(url, json=data, headers=headers)
                result = response.json()
                
                if 'choices' in result:
                    ai_reply = result['choices'][0]['message']['content']
                    st.markdown("### 🔍 AI分析结果")
                    st.info(ai_reply)
                    
                    # 加到对话历史
                    st.session_state.messages.append({"role": "user", "content": "帮我分析代码"})
                    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
                else:
                    st.error(f"AI返回错误：{result}")
                    
            except Exception as e:
                st.error(f"调用AI出错：{e}")
    
    # 学习统计
    if st.session_state.user_id:
        st.divider()
        st.markdown("### 📊 学习统计")
        
        stats = st.session_state.db.get_user_stats(st.session_state.user_id)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <p>总练习</p>
                <h3>{stats['total']}</h3>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <p>题目类型</p>
                <h3>{len(stats['by_type'])}</h3>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            if stats['total'] > 0:
                most_common = max(stats['by_type'], key=stats['by_type'].get)
                st.markdown(f"""
                <div class="metric-card">
                    <p>最常练习</p>
                    <h3 style="font-size: 1.2em;">{most_common[:6]}</h3>
                </div>
                """, unsafe_allow_html=True)