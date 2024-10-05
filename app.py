import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq
import random
import time
from datetime import datetime

# Load environment variables
load_dotenv()

# Set up API client
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_bio(job_hobby, vibe, length, hashtags, emojis):
    prompt = f"""Generate 3 unique Twitter bios for someone who is into {job_hobby} with a {vibe} vibe. 
    Each bio should be {length} and {"include hashtags" if hashtags else "not include hashtags"}.
    {"Include relevant emojis" if emojis else "Do not include emojis"}.
    Separate each bio with '|||'."""

    try:
        completion = groq_client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=200,
            top_p=1,
            stream=False,
            stop=None,
        )
        bios = completion.choices[0].message.content.strip().split('|||')
        return [bio.strip() for bio in bios]
    except Exception as e:
        st.error(f"Error with Groq API: {str(e)}")
        return []

def chat_with_groq(prompt):
    try:
        completion = groq_client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=150,
            top_p=1,
            stream=False,
            stop=None,
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Error with Groq AI Chat: {str(e)}")
        return None

# Set page config
st.set_page_config(page_title="TweetCraft AI", page_icon="🐦", layout="wide")

# Custom CSS for modern aesthetics with sky blue theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
    
    body {
        font-family: 'Roboto', sans-serif;
        background-color: #1a1a2e;
        color: #e0e0e0;
    }
    .stApp {
        background-color: #1a1a2e;
    }
    .stTextInput > div > div > input, .stSelectbox > div > div > select, .stTextArea > div > div > textarea {
        background-color: #16213e;
        color: #e0e0e0;
        border: 1px solid #0f3460;
    }
    .stButton > button {
        background-color: #87CEEB;
        color: #1a1a2e;
        font-weight: bold;
        border: none;
        border-radius: 20px;
        padding: 10px 20px;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #5F9EA0;
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(135, 206, 235, 0.2);
    }
    .sidebar .sidebar-content {
        background-color: #16213e;
    }
    .bio-card {
        background-color: #0f3460;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    .bio-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.2);
    }
    .bio-text {
        font-size: 18px;
        line-height: 1.5;
        margin-bottom: 15px;
    }
    .feature-box {
        background-color: #16213e;
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 30px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .chat-area {
        margin-top: 40px;
        padding-top: 20px;
        border-top: 1px solid #0f3460;
    }
    h1, h2, h3 {
        color: #87CEEB;
    }
    .stSlider > div > div > div > div {
        background-color: #87CEEB;
    }
    .stProgress > div > div > div > div {
        background-color: #87CEEB;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://placekitten.com/300/200", caption="TweetCraft AI")
    st.header("About")
    st.info("TweetCraft AI uses Groq AI to create unique and engaging Twitter bios tailored to your preferences.")

    st.header("Instructions")
    st.markdown("""
    1. Enter your job or favorite hobby.
    2. Select your preferred vibe and customize options.
    3. Click 'Generate Bios' to get your personalized Twitter bios.
    4. Rate and save your favorite bios.
    5. Use additional features like Bio Analyzer and Trend Insights.
    6. Chat with Groq AI for more personalized assistance.
    """)

    st.header("Features")
    st.markdown("""
    - Modern, responsive UI
    - Emoji integration
    - Bio history and favorites
    - Trend insights
    - Interactive bio builder
    - Social media preview
    """)

# Main content
st.title("🐦 TweetCraft AI")

# User Input Section
st.header("✏️ Customize Your Bio")
col1, col2, col3 = st.columns(3)

with col1:
    job_hobby = st.text_input("💼 Your job or favorite hobby", placeholder="e.g. Data Scientist")
    vibe = st.selectbox("✨ Select your vibe", ["Professional", "Creative", "Humorous", "Inspirational", "Technical"])

with col2:
    length = st.radio("📏 Bio length", ["Short (under 100 characters)", "Medium (100-140 characters)", "Long (140-160 characters)"])
    hashtags = st.checkbox("# Include hashtags")

with col3:
    emojis = st.checkbox("😊 Include emojis")
    st.write("")  # Spacer
    generate_button = st.button("🚀 Generate Bios")

# Bio Generation and Display
if generate_button:
    if job_hobby and vibe:
        with st.spinner('Crafting your perfect bios...'):
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress_bar.progress(i + 1)
            
            generated_bios = generate_bio(job_hobby, vibe, length, hashtags, emojis)
            if generated_bios:
                st.success("Bios generated successfully!")
                st.markdown("### 🎨 Your AI-generated Twitter bios:")
                for i, bio in enumerate(generated_bios[:3], 1):
                    with st.container():
                        st.markdown(f"<div class='bio-card'>", unsafe_allow_html=True)
                        st.markdown(f"<p class='bio-text'>{bio}</p>", unsafe_allow_html=True)
                        col1, col2, col3 = st.columns([2, 1, 1])
                        with col1:
                            st.button(f"📋 Copy Bio {i}", key=f"copy_{i}", help=f"Copy Bio {i} to clipboard")
                        with col2:
                            st.button(f"❤️ Save Bio {i}", key=f"save_{i}", help=f"Save Bio {i} to favorites")
                        with col3:
                            st.select_slider(f"Rate Bio {i}", options=["👎", "😐", "👍"], key=f"rate_{i}")
                        st.markdown("</div>", unsafe_allow_html=True)
                
                # Social Media Preview
                st.markdown("### 👁️ Social Media Preview")
                preview_col1, preview_col2 = st.columns([1, 2])
                with preview_col1:
                    st.image("https://placekitten.com/400/400", caption="Profile Picture")
                with preview_col2:
                    st.markdown(f"**Name:** {job_hobby.title()} Enthusiast")
                    st.markdown(f"**@handle:** @{job_hobby.lower().replace(' ', '')}_pro")
                    st.markdown(f"**Bio:** {random.choice(generated_bios)}")
                
                # Personalized bio tips
                st.markdown("### 💡 Personalized Bio Tips")
                tips_prompt = f"Give 3 quick tips for improving a Twitter bio for someone in {job_hobby} with a {vibe} vibe."
                tips = chat_with_groq(tips_prompt)
                if tips:
                    st.markdown(tips)
            else:
                st.error("Failed to generate bios. Please try again.")
    else:
        st.warning("Please fill in both job/hobby and vibe before generating bios.")

# Interactive Bio Builder
st.markdown("<div class='feature-box'>", unsafe_allow_html=True)
st.header("🛠️ Interactive Bio Builder")
st.write("Craft your bio step by step with AI assistance.")
builder_job = st.text_input("Your primary role or passion:")
builder_achievement = st.text_input("A key achievement or skill:")
builder_interest = st.text_input("An interesting hobby or side project:")

if st.button("Build My Bio"):
    if builder_job and builder_achievement and builder_interest:
        build_prompt = f"Create a concise Twitter bio incorporating these elements: Role: {builder_job}, Achievement: {builder_achievement}, Interest: {builder_interest}. Make it engaging and under 160 characters."
        built_bio = chat_with_groq(build_prompt)
        if built_bio:
            st.markdown(f"**Your Custom Bio:** {built_bio}")
            st.button("💾 Save to Favorites")
    else:
        st.warning("Please fill in all fields to build your bio.")
st.markdown("</div>", unsafe_allow_html=True)

# Bio Analyzer Feature
st.markdown("<div class='feature-box'>", unsafe_allow_html=True)
st.header("🔍 Bio Analyzer")
user_bio = st.text_area("Paste your current Twitter bio for analysis:", max_chars=160)
if st.button("Analyze Bio"):
    if user_bio:
        analysis_prompt = f"Analyze this Twitter bio and provide 3 specific suggestions for improvement:\n\n{user_bio}"
        analysis = chat_with_groq(analysis_prompt)
        if analysis:
            st.markdown(analysis)
    else:
        st.warning("Please enter a bio to analyze.")
st.markdown("</div>", unsafe_allow_html=True)

# Trend Insights
st.markdown("<div class='feature-box'>", unsafe_allow_html=True)
st.header("📈 Trend Insights")
st.write("Get insights on current Twitter bio trends.")
trend_category = st.selectbox("Select a category for trend insights:", ["Tech", "Creative", "Business", "Lifestyle"])
if st.button("Get Trend Insights"):
    trend_prompt = f"Provide 3 current trends for Twitter bios in the {trend_category} category."
    trends = chat_with_groq(trend_prompt)
    if trends:
        st.markdown(trends)
st.markdown("</div>", unsafe_allow_html=True)

# Bio History and Favorites
st.header("📚 Bio History and Favorites")
tab1, tab2 = st.tabs(["History", "Favorites"])
with tab1:
    st.write("Your recently generated bios will appear here.")
    # Placeholder for bio history
    st.text("1. Data Scientist | AI Enthusiast | Coffee Lover 🤖☕")
    st.text("2. Turning data into insights | Python & R | Marathon runner 🏃‍♂️")
with tab2:
    st.write("Your favorite bios will be saved here.")
    # Placeholder for favorites
    st.text("1. Code by day, DJ by night | Full-stack developer with a passion for music 🎧")

# Chat with Groq AI
st.markdown("<div class='chat-area'>", unsafe_allow_html=True)
st.header("💬 Chat with Groq AI")
user_input = st.text_input("Ask anything about Twitter bios, personal branding, or social media strategy:", key="groq_chat_input")

if st.button("Send", key="send_chat"):
    if user_input:
        with st.spinner('Groq AI is thinking...'):
            response = chat_with_groq(user_input)
            if response:
                st.markdown("<div class='output-area'>", unsafe_allow_html=True)
                st.markdown(f"**You:** {user_input}")
                st.markdown(f"**Groq AI:** {response}")
                st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("Please enter a message to chat with Groq AI.")

st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("Created with ❤️ by Shazy | Last updated: " + datetime.now().strftime("%B %d, %Y"))