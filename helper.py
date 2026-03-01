from wordcloud import WordCloud
import matplotlib.pyplot as plt
import emoji

def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]
    words = []
    for message in df['message']:
        words.extend(message.split())

    return num_messages, len(words)


def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    text = " ".join(df['message'])
    wc = WordCloud(width=500, height=500).generate(text)

    return wc


def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    return emojis


import pandas as pd

# ===============================
# MONTHLY TIMELINE
# ===============================
def monthly_timeline(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.copy()
    timeline['month'] = timeline['date'].dt.month_name()
    timeline['year'] = timeline['date'].dt.year

    timeline_group = timeline.groupby(['year', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline_group.shape[0]):
        time.append(timeline_group['month'][i] + "-" + str(timeline_group['year'][i]))

    timeline_group['time'] = time

    return timeline_group


# ===============================
# MOST ACTIVE USER
# ===============================
def most_active_users(df):
    x = df['user'].value_counts().head()

    df_percent = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index()
    df_percent.columns = ['name', 'percent']

    return x, df_percent


# ===============================
# WEEKLY HEATMAP
# ===============================
def activity_heatmap(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    heatmap = df.copy()
    heatmap['day'] = heatmap['date'].dt.day_name()
    heatmap['period'] = heatmap['date'].dt.hour

    heatmap_data = heatmap.pivot_table(
        index='day',
        columns='period',
        values='message',
        aggfunc='count'
    ).fillna(0)

    return heatmap_data


# ===============================
# MESSAGE FREQUENCY (DAILY)
# ===============================
def daily_timeline(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily = df.copy()
    daily['only_date'] = daily['date'].dt.date

    daily_group = daily.groupby('only_date').count()['message'].reset_index()

    return daily_group