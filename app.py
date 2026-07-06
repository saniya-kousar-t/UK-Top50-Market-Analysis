import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="UK Top 50 Analysis", layout="wide")

st.markdown("""
<h1 style='text-align: center; color: #667eea;'>🎵 UK Top 50 Market Analysis</h1>
<p style='text-align: center;'>Interactive Dashboard</p>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    try:
        df = pd.read_csv('uk_top50_processed.csv')
        df['date'] = pd.to_datetime(df['date'])
        return df
    except:
        st.error("❌ File 'uk_top50_processed.csv' not found in Downloads folder")
        return None

df = load_data()
if df is None:
    st.stop()

st.markdown("### 📊 KEY METRICS")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("🎤 Artists", df['artist'].nunique())
with col2:
    st.metric("🤝 Collab %", f"{df['is_collaboration'].mean()*100:.1f}%")
with col3:
    st.metric("🔊 Explicit %", f"{df['is_explicit'].mean()*100:.1f}%")
with col4:
    st.metric("💿 Single %", f"{(df['album_type']=='single').mean()*100:.1f}%")
with col5:
    st.metric("⭐ Popularity", f"{df['popularity'].mean():.1f}")

st.markdown("---")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["🎤 Artists", "🤝 Collaborations", "🔊 Explicit", "💿 Format", "⏱️ Duration"])

with tab1:
    st.markdown("### Top 15 Artists")
    top_artists = df['artist'].value_counts().head(15)
    col1, col2 = st.columns(2)
    with col1:
        fig1 = px.bar(x=top_artists.values, y=top_artists.index, orientation='h',
                     title="Artist Appearances", color=top_artists.values,
                     color_continuous_scale='Viridis')
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        fig2 = px.pie(values=top_artists.values, names=top_artists.index,
                     title="Top 15 Market Share")
        st.plotly_chart(fig2, use_container_width=True)

with tab2:
    st.markdown("### Collaboration Analysis")
    col1, col2 = st.columns(2)
    with col1:
        collab_by_pos = df.groupby('position')['is_collaboration'].mean() * 100
        fig = go.Figure(data=[go.Scatter(x=collab_by_pos.index, y=collab_by_pos.values,
                            fill='tozeroy', mode='lines+markers', name='Collab %')])
        fig.update_layout(title="Collaboration by Position", xaxis_title="Position",
                         yaxis_title="%", height=400)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        collab_dist = df['is_collaboration'].value_counts()
        fig = px.pie(values=[collab_dist[False], collab_dist[True]],
                    names=['Solo', 'Collaboration'],
                    color_discrete_map={'Solo': '#4CAF50', 'Collaboration': '#FF5252'})
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.markdown("### Explicit Content Analysis")
    col1, col2 = st.columns(2)
    with col1:
        explicit_dist = df['is_explicit'].value_counts()
        fig = px.pie(values=explicit_dist.values, names=['Clean', 'Explicit'],
                    color_discrete_map={'Clean': '#4CAF50', 'Explicit': '#FF5252'})
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        explicit_by_pos = df.groupby(pd.cut(df['position'], bins=[0, 10, 25, 50]))['is_explicit'].mean() * 100
        fig = px.bar(x=['Top 10', '11-25', '26-50'], y=explicit_by_pos.values,
                    title="Explicit % by Position", color=explicit_by_pos.values,
                    color_continuous_scale='Reds')
        st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.markdown("### Release Format Analysis")
    col1, col2 = st.columns(2)
    with col1:
        format_dist = df['album_type'].value_counts()
        fig = px.pie(values=format_dist.values, names=format_dist.index,
                    title="Format Distribution")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        pos_by_format = df.groupby('album_type')['position'].mean()
        fig = px.bar(x=pos_by_format.index, y=pos_by_format.values,
                    title="Avg Position by Format", color=pos_by_format.values,
                    color_continuous_scale='Turbo')
        st.plotly_chart(fig, use_container_width=True)

with tab5:
    st.markdown("### Duration Analysis")
    df['duration_minutes'] = df['duration_ms'] / 60000
    col1, col2 = st.columns(2)
    with col1:
        fig = px.histogram(df, x='duration_minutes', nbins=30,
                          title="Duration Distribution",
                          labels={'duration_minutes': 'Minutes'})
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        short = (df['duration_minutes'] < 3).sum()
        long = len(df) - short
        fig = px.pie(values=[short, long], names=['<3 min', '≥3 min'],
                    color_discrete_map={'<3 min': '#FF6B6B', '≥3 min': '#4ECDC4'})
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("*Data: May 2024 - Nov 2025 | 27,800+ entries*")