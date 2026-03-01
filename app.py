import streamlit as st
import preprocess
import helper
import matplotlib.pyplot as plt
import seaborn as sns 
from sample_data import sample_chat

st.title("📊 WhatsApp Chat Analyzer")

st.sidebar.title("Options")

uploaded_file = st.file_uploader("Upload WhatsApp Chat")

# 🔥 NEW: choose data source
data_source = st.sidebar.radio(
    "Select Data Source",
    ("Use Sample Data", "Upload Your Chat")
)

# -----------------------------
# CASE 1: SAMPLE DATA
# -----------------------------
if data_source == "Use Sample Data":
    df = preprocess.preprocess(sample_chat)

# -----------------------------
# CASE 2: UPLOADED FILE
# -----------------------------
elif uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocess.preprocess(data)
else:
    st.stop()

# -----------------------------
# USER SELECTION
# -----------------------------
user_list = df['user'].unique().tolist()
user_list.sort()
user_list.insert(0, "Overall")

selected_user = st.sidebar.selectbox(
    "Show analysis for",
    user_list
)



if st.sidebar.button("Show Analysis"):

    # stats
    num_messages, words = helper.fetch_stats(selected_user, df)
    st.header("📌 Top Statistics")
    st.write("Total Messages:", num_messages)
    st.write("Total Words:", words)

 
    # wordcloud
    st.header("☁️ WordCloud")
    wc = helper.create_wordcloud(selected_user, df)
    fig, ax = plt.subplots()
    ax.imshow(wc)
    ax.axis("off")
    st.pyplot(fig)

    # emoji analysis
    st.header("😂 Emoji Analysis")
    emojis = helper.emoji_helper(selected_user, df)
    st.write("Total Emojis:", len(emojis))

# ===============================
# MONTHLY TIMELINE
# ===============================
st.header("📆 Monthly Timeline")

timeline = helper.monthly_timeline(selected_user, df)

fig, ax = plt.subplots()
ax.plot(timeline['time'], timeline['message'])
plt.xticks(rotation='vertical')
st.pyplot(fig)

# ===============================
# MOST ACTIVE USERS
# ===============================
if selected_user == 'Overall':
    st.header("🔥 Most Active Users")

    x, new_df = helper.most_active_users(df)

    fig, ax = plt.subplots()
    ax.bar(x.index, x.values)
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

    st.dataframe(new_df)

    # ===============================
# DAILY TIMELINE
# ===============================
st.header("📅 Daily Message Frequency")

daily_timeline = helper.daily_timeline(selected_user, df)

fig, ax = plt.subplots()
ax.plot(daily_timeline['only_date'], daily_timeline['message'])
plt.xticks(rotation='vertical')
st.pyplot(fig)

# ===============================
# ACTIVITY HEATMAP
# ===============================
st.header("🗺️ Weekly Activity Heatmap")

heatmap_data = helper.activity_heatmap(selected_user, df)

fig, ax = plt.subplots()
sns.heatmap(heatmap_data)
st.pyplot(fig)


