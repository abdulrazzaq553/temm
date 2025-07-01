import streamlit as st
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd
import emoji
import seaborn as sns
import link
import link2nd
import zipfile
import os
from textblob import TextBlob
from transformers import pipeline
from googletrans import Translator
import re
import time
from streamlit_extras.colored_header import colored_header
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.dataframe_explorer import dataframe_explorer

# Set page config with better theme
st.set_page_config(
    page_title="WhatsAp Chat Analyzer Pro",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
    <style>
        .main {
            background-color: #f8f9fa;
        }
        .sidebar .sidebar-content {
            background-color: #ffffff;
        }
        .stButton>button {
            background-color: #4A90E2;
            color: white;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            border: none;
        }
        .stButton>button:hover {
            background-color: #3a7bc8;
        }
        .stSelectbox>div>div>select {
            border-radius: 8px;
        }
        .stSlider>div>div>div>div {
            background-color: #4A90E2;
        }
        .stDataFrame {
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .css-1aumxhk {
            background-color: #ffffff;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .stProgress>div>div>div>div {
            background-color: #4A90E2;
        }
        .css-1v3fvcr {
            padding: 1rem;
        }
        .metric-card {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 15px;
        }
        .metric-title {
            font-size: 14px;
            color: #6c757d;
            margin-bottom: 5px;
        }
        .metric-value {
            font-size: 24px;
            font-weight: bold;
            color: #343a40;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar with improved design
with st.sidebar:
    colored_header(
        label="📊 WhatsApp Chat Analyzer Pro",
        description="",
        color_name="blue-70"
    )
    
    st.markdown("""
        <div style='text-align: center; margin-bottom: 20px;'>
            <p style='color: #6c757d;'>Upload your WhatsApp chat export to analyze conversation patterns, emotions, and more.</p>
        </div>
    """, unsafe_allow_html=True)
    
    file = st.file_uploader('📁 Choose a File', type=['txt', 'zip'], help="Upload your WhatsApp chat export (TXT or ZIP)")
    
    if file is None:
        st.info(
            """
            **How to export your WhatsApp chat:**
            1. Open the chat you want to analyze
            2. Tap ⋮ (Android) or ⓘ (iPhone)
            3. Select "More" → "Export chat"
            4. Choose "Without media" (for TXT) or "With media" (for ZIP)
            5. Send it to yourself or save to device
            6. Upload the file here
            """
        )
    
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center;'>
            <h4 style='color: #4A90E2; margin-bottom: 5px;'>💻 Developed By</h4>
            <h3 style='color: #4A90E2; margin-top: 0;'>Abdul Razzaq</h3>
            <p style='color: #6c757d;'>
                <a href='mailto:arazzaq7789@gmail.com' style='color: #4A90E2; text-decoration: none;'>
                    📧 arazzaq7789@gmail.com
                </a>
            </p>
        </div>
    """, unsafe_allow_html=True)

# Main content
if file is not None:
    # Progress bar for file processing
    with st.spinner('Processing your chat file...'):
        progress_bar = st.progress(0)
        for percent_complete in range(100):
            time.sleep(0.01)
            progress_bar.progress(percent_complete + 1)
        
        response = link2nd.razzaq(file)

        if file.type == "application/zip":
            with zipfile.ZipFile(file, 'r') as zip_ref:
                zip_ref.extractall("./extracted_files")
                extracted_files = os.listdir("./extracted_files")
                for extracted_file in extracted_files:
                    if extracted_file.endswith('.txt'):
                        with open(f"./extracted_files/{extracted_file}", 'r', encoding='utf-8') as f:
                            chat = f.read()
                        R1 = link.start(chat)
        elif file.type == "text/plain":
            chat = file.getvalue().decode('utf-8')
            R1 = link.start(chat)
        
        progress_bar.empty()

    # Title with animation
    st.markdown("""
        <h1 style='text-align: center; color: #4A90E2; margin-bottom: 30px;'>
            <span style='display: inline-block; animation: fadeIn 2s;'>WhatsApp Chat Analysis</span>
        </h1>
    """, unsafe_allow_html=True)
    
    # User selection
    user_list = R1['User'].unique().tolist()
    user_list.insert(0, 'Overall')
    
    col1, col2 = st.columns([1, 3])
    with col1:
        select_user = st.selectbox('👤 Choose User', user_list, help="Select a user to analyze or 'Overall' for group analysis")
    
    total_messages = len(R1)
    
    with col2:
        msg_count = st.slider(
            "🔢 Select number of recent messages to analyze (Emotion/Sentiment)",
            min_value=5,
            max_value=total_messages,
            value=min(100, total_messages),
            step=5,
            help="Analyzing fewer messages will be faster for sentiment/emotion analysis"
        )
    
    if st.button('🚀 Show Analysis', use_container_width=True):
        # Performance optimization - cache heavy computations
        @st.cache_data(show_spinner=False)
        def compute_metrics(user, data):
            return (
                link2nd.select(user, data),
                link2nd.media_shared(user, data),
                link2nd.url(user, data),
                link2nd.busy_user(user, data),
                link2nd.days(user, data),
                link2nd.wordscount(user, data),
                link2nd.common_words(user, data),
                link2nd.emojis(user, data),
                link2nd.Month(user, data),
                link2nd.year(user, data),
                link2nd.daily(user, data),
                link2nd.search(user, data)
            )
        
        with st.spinner('Crunching the numbers... This may take a moment for large chats'):
            start_time = time.time()
            
            # Compute all metrics in one cached function
            (total_mesage, total_words), media_shared, links, (x1, x2, x3), days2, wordcloud_img, common, emoji_df, month, year, daily, search = compute_metrics(select_user, R1)
            
            # Metrics cards with better styling
            st.subheader('📊 Chat Overview')
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-title">Total Messages</div>
                        <div class="metric-value">{total_mesage}</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-title">Total Words</div>
                        <div class="metric-value">{total_words}</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-title">Media Shared</div>
                        <div class="metric-value">{media_shared}</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-title">Links Shared</div>
                        <div class="metric-value">{links}</div>
                    </div>
                """, unsafe_allow_html=True)
            
            style_metric_cards()
            
            # Most Active Users section
            st.subheader('🏆 Most Active Users')
            tab1, tab2, tab3 = st.tabs(["📊 Chart", "📋 Top Users", "📋 Least Active"])
            
            with tab1:
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.bar(x1.index, x1.values, color='#4A90E2')
                plt.xticks(rotation=45, ha='right')
                plt.title('Message Count by User', pad=20)
                plt.grid(axis='y', linestyle='--', alpha=0.7)
                st.pyplot(fig)
            
            with tab2:
                st.dataframe(x2.style.background_gradient(cmap='Blues'), use_container_width=True)
            
            with tab3:
                st.dataframe(x3.style.background_gradient(cmap='Reds'), use_container_width=True)
            
            # Emotion and Sentiment Analysis with progress bars
            st.subheader('😃 Emotion & Sentiment Analysis')
            
            neutral_keywords = [
                # English neutral/common phrases
                "neutral", "ok", "okay", "fine", "normal", "alright", "nothing much",
                "i'm fine", "i am fine", "i'm okay", "i am okay", "all good", "going good", "not bad",
                # Roman Urdu (chat-friendly neutral mood)
                "acha hn","acha","acha hoon", "theek hn", 'nhi','sahi','hn',"theek hoon", "sahi hn", "sahi hoon",
                "mast chal raha", "bht kuch nahi", "kuch khas nahi", "bas theek", "thik hn", "thik hoon",
                "me theek hoon", "main theek hoon", "sab theek", "normal chal raha", "bas chal raha",
                # Salam / Religious expressions
                "salam", "asalamualaikum", "assalamualaikum", "asalamo alaikum", "as-salamu alaykum",
                "walaikum salam", "walaikum assalam", "wa alaikumussalam", "wa alaikum salam",
                "alhamdulillah", "alhamdulilah", "shukar", "shukar allah ka", "thanks to allah",
                "by the grace of allah", "allah ka shukar", "allah ka karam",
                # Good night / Chat closing phrases
                "good night", "good nyt", "gn", "shabba khair", "shab bakhair", "sweet dreams",
                "take rest", "have a good sleep", "kal milty", "bye", "ok bye", "allah hafiz", "allah hafz",
                # Short replies and lingo
                "oky", "okk", "k", '<Media omitted>',"kk", "hmm", "haan theek", "thk hn", "thk hoon", "bas", "acha","come","bavy","sai"
            ]
            
            emojis = {'joy': '😄', 'sadness': '😢', 'anger': '😠', 'fear': '😨', 'surprise': '😲', 'love': '❤️'}
            
            @st.cache_resource(show_spinner=False)
            def load_emotion_model():
                return pipeline("text-classification", model="nateraw/bert-base-uncased-emotion", return_all_scores=True, framework="pt")
            
            @st.cache_data(show_spinner=False)
            def detect_emotion(msg):
                try:
                    # FIRST: Check original message for neutral keywords
                    if any(word.lower() in msg.lower() for word in neutral_keywords):
                        return "neutral 😐"
                    
                    # THEN: Translate and classify
                    translator = Translator()
                    text = translator.translate(msg).text.lower()
                    classifier = load_emotion_model()
                    result = classifier(text)
                    top = max(result[0], key=lambda x: x['score'])
                    
                    if top['score'] < 0.4:
                        return "neutral 😐"
                    return f"{top['label']} {emojis.get(top['label'], '')}"
                except Exception:
                    return "neutral 😐"
            
            @st.cache_data(show_spinner=False)
            def analyze_sentiment(msg):
                if not msg.strip() or re.match(r'https?://', msg.strip()):
                    return 'Neutral'
                try:
                    translator = Translator()
                    text = translator.translate(msg, dest='en').text
                    polarity = TextBlob(text).sentiment.polarity
                    if polarity > 0:
                        return 'Positive'
                    elif polarity < 0:
                        return 'Negative'
                    return 'Neutral'
                except Exception:
                    return 'Neutral'
            
            # Emotion Analysis with progress
            with st.expander("🎭 Emotion Analysis (Click to expand)", expanded=True):
                with st.spinner(f"Analyzing emotions for {msg_count} messages..."):
                    emotion_progress = st.progress(0)
                    sample = R1.tail(msg_count).copy()
                    
                    # Process in chunks for better progress updates
                    chunk_size = max(1, msg_count // 10)
                    for i in range(0, msg_count, chunk_size):
                        chunk = sample.iloc[i:i+chunk_size]
                        sample.loc[chunk.index, 'emotion'] = chunk['Message'].apply(detect_emotion)
                        emotion_progress.progress(min((i + chunk_size) / msg_count, 1.0))
                    
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.dataframe(sample[['User', 'Message', 'emotion']].style.applymap(
                            lambda x: 'background-color: #e6f3ff' if x == 'neutral 😐' else '', 
                            subset=['emotion']
                        ), use_container_width=True, height=300)
                    
                    with col2:
                        fig, ax = plt.subplots(figsize=(5, 4))
                        emotion_counts = sample['emotion'].value_counts()
                        colors = ['#4A90E2', '#50C878', '#FF6B6B', '#FFD166', '#845EC2', '#FF9671']
                        emotion_counts.plot(kind='bar', ax=ax, color=colors[:len(emotion_counts)])
                        plt.title('Emotion Distribution', pad=10)
                        plt.xticks(rotation=45, ha='right')
                        plt.tight_layout()
                        st.pyplot(fig)
                    
                    emotion_progress.empty()
            
            # Sentiment Analysis with progress
            with st.expander("😊 Sentiment Analysis (Click to expand)", expanded=True):
                with st.spinner(f"Analyzing sentiment for {msg_count} messages..."):
                    sentiment_progress = st.progress(0)
                    sample2 = R1.tail(msg_count).copy()
                    
                    # Process in chunks for better progress updates
                    for i in range(0, msg_count, chunk_size):
                        chunk = sample2.iloc[i:i+chunk_size]
                        sample2.loc[chunk.index, 'Sentiment'] = chunk['Message'].apply(analyze_sentiment)
                        sentiment_progress.progress(min((i + chunk_size) / msg_count, 1.0))
                    
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.dataframe(sample2[['User', 'Message', 'Sentiment']].style.applymap(
                            lambda x: 'background-color: #e6ffe6' if x == 'Positive' else 
                                    'background-color: #ffe6e6' if x == 'Negative' else '',
                            subset=['Sentiment']
                        ), use_container_width=True, height=300)
                    
                    with col2:
                        fig, ax = plt.subplots(figsize=(5, 4))
                        sentiment_counts = sample2['Sentiment'].value_counts()
                        colors = ['#50C878', '#FF6B6B', '#4A90E2']  # Green, Red, Blue
                        sentiment_counts.plot(kind='bar', ax=ax, color=colors[:len(sentiment_counts)])
                        plt.title('Sentiment Distribution', pad=10)
                        plt.xticks(rotation=45, ha='right')
                        plt.tight_layout()
                        st.pyplot(fig)
                    
                    sentiment_progress.empty()
            
            # Word Cloud section
            st.subheader('🔠 Word Cloud')
            col1, col2 = st.columns([2, 1])
            with col1:
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.imshow(wordcloud_img)
                ax.axis("off")
                ax.set_title('Most Frequent Words', pad=20)
                st.pyplot(fig)
            
            with col2:
                st.subheader('📊 Common Words')
                fig, ax = plt.subplots(figsize=(6, 4))
                ax.barh(common[0][:10][::-1], common[1][:10][::-1], color='#4A90E2')
                plt.title('Top 10 Words', pad=10)
                plt.tight_layout()
                st.pyplot(fig)
            
            # Emoji analysis
            st.subheader('😃 Emoji Analysis')
            if not emoji_df.empty:
                col1, col2 = st.columns(2)
                with col1:
                    st.dataframe(emoji_df.style.background_gradient(cmap='Purples'), use_container_width=True)
                
                with col2:
                    fig, ax = plt.subplots(figsize=(8, 4))
                    emoji_df.head(10).plot(kind='bar', x='Emoji', y='Count', ax=ax, color='#845EC2')
                    plt.title('Top 10 Emojis', pad=10)
                    plt.xticks(rotation=45, ha='right')
                    plt.tight_layout()
                    st.pyplot(fig)
            else:
                st.info("No emojis found in this chat selection")
            
            # Temporal analysis sections
            st.subheader('⏳ Temporal Analysis')
            
            tab1, tab2, tab3 = st.tabs(["📅 Daily Activity", "📆 Monthly Activity", "📈 Yearly Trends"])
            
            with tab1:
                st.write("### Busy Days of Week")
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.bar(days2['dayss'], days2['Message'], color='#4A90E2')
                plt.title('Messages by Day of Week', pad=15)
                plt.grid(axis='y', linestyle='--', alpha=0.7)
                st.pyplot(fig)
                
                st.write("### Daily Timeline")
                st.dataframe(daily.style.background_gradient(cmap='Blues'), use_container_width=True)
            
            with tab2:
                st.write("### Monthly Distribution")
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.dataframe(month.style.background_gradient(cmap='Greens'), use_container_width=True)
                
                with col2:
                    fig, ax = plt.subplots(figsize=(8, 6))
                    month.set_index('NEW_Month')['count'].plot(
                        kind='pie', ax=ax, autopct='%.1f%%', 
                        colors=sns.color_palette('pastel'), 
                        textprops={'fontsize': 10}
                    )
                    plt.title('Messages by Month', pad=20)
                    plt.ylabel('')
                    st.pyplot(fig)
            
            with tab3:
                st.write("### Yearly Trends")
                fig, ax = plt.subplots(figsize=(12, 6))
                ax.plot(year['new'], year['Message'], marker='o', color='#4A90E2', linewidth=2)
                plt.xticks(rotation=45, ha='right')
                plt.title('Message Trends Over Time', pad=15)
                plt.grid(True, linestyle='--', alpha=0.7)
                st.pyplot(fig)
            
            # Full data explorer
            st.subheader('🔍 Full Chat Data Explorer')
            filtered_df = dataframe_explorer(R1, case=False)
            st.dataframe(filtered_df, use_container_width=True)
            
            # Performance metrics
            end_time = time.time()
            st.success(f"Analysis completed in {end_time - start_time:.2f} seconds!")
            
            # Add a nice completion message
            st.balloons()
            st.markdown("""
                <div style='text-align: center; padding: 20px; background-color: #e6f7ff; border-radius: 10px; margin-top: 20px;'>
                    <h3 style='color: #4A90E2;'>Analysis Complete! 🎉</h3>
                    <p style='color: #6c757d;'>Explore the tabs above to discover insights from your WhatsApp chat.</p>
                </div>
            """, unsafe_allow_html=True)

# Empty state design
else:
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown("""
            <div style='text-align: center; margin-top: 100px;'>
                <h2 style='color: #4A90E2;'>Welcome to WhatsApp Chat Analyzer Pro</h2>
                <p style='color: #6c757d; font-size: 16px;'>
                    Upload your WhatsApp chat export in the sidebar to begin analysis.<br>
                    Discover conversation patterns, emotions, and insights from your chats.
                </p>
                <img src='https://cdn-icons-png.flaticon.com/512/220/220236.png' width='150' style='margin: 30px 0; opacity: 0.8;'>
                <div style='background-color: #e6f7ff; padding: 20px; border-radius: 10px;'>
                    <h4 style='color: #4A90E2;'>What you'll discover:</h4>
                    <ul style='text-align: left; color: #6c757d;'>
                        <li>Most active users and times</li>
                        <li>Emotion and sentiment trends</li>
                        <li>Common words and emojis</li>
                        <li>Temporal patterns in your chats</li>
                    </ul>
                </div>
            </div>
        """, unsafe_allow_html=True)