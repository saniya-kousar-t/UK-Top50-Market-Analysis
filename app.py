import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import networkx as nx
from collections import defaultdict
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="UK Top 50 Market Analysis", layout="wide", initial_sidebar_state="expanded")

@st.cache_data
def load_data():
    try:
        df = pd.read_csv('uk_top50_processed.csv')
        df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def parse_artists(artist_str):
    if pd.isna(artist_str):
        return []
    return [a.strip() for a in str(artist_str).split(',')]

def create_collaboration_network(df_filtered):
    collaborations = defaultdict(set)
    for idx, row in df_filtered[df_filtered['is_collaboration']].iterrows():
        artists = parse_artists(row['artist_list'])
        if len(artists) >= 2:
            for i in range(len(artists)):
                for j in range(i+1, len(artists)):
                    collaborations[artists[i]].add(artists[j])
                    collaborations[artists[j]].add(artists[i])
    return collaborations

def plot_collaboration_network(collaborations, top_n=15):
    if not collaborations:
        return None
    
    collab_counts = {artist: len(collabs) for artist, collabs in collaborations.items()}
    top_artists = sorted(collab_counts.items(), key=lambda x: x[1], reverse=True)[:top_n]
    top_artists_list = [artist for artist, _ in top_artists]
    
    G = nx.Graph()
    for artist in top_artists_list:
        G.add_node(artist)
        for collaborator in collaborations.get(artist, []):
            if collaborator in top_artists_list:
                G.add_edge(artist, collaborator)
    
    pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
    
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
    
    edge_trace = go.Scatter(x=edge_x, y=edge_y, mode='lines',
        line=dict(width=1, color='rgba(125,125,125,0.5)'),
        hoverinfo='none', showlegend=False)
    
    node_x = []
    node_y = []
    node_sizes = []
    node_colors = []
    node_text = []
    
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_sizes.append(collab_counts[node] * 20 + 20)
        node_colors.append(collab_counts[node])
        node_text.append(f"{node}<br>Collaborations: {collab_counts[node]}")
    
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=[node for node in G.nodes()],
        textposition="top center",
        hovertext=node_text,
        hoverinfo='text',
        marker=dict(
            size=node_sizes,
            color=node_colors,
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(thickness=15, title="Collaborations", xanchor="left"),
            line_width=2,
            line_color='white'
        ),
        showlegend=False
    )
    
    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(
        title="Artist Collaboration Network (Top 15 Most Connected)",
        showlegend=False,
        hovermode='closest',
        margin=dict(b=0, l=0, r=0, t=40),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        height=700,
        plot_bgcolor='rgba(240,240,240,0.9)'
    )
    return fig

df = load_data()
if df is None:
    st.stop()

st.markdown("""
<div style='text-align: center; margin-bottom: 30px;'>
    <h1 style='color: #667eea; font-size: 36px;'>🎵 UK Top 50 Market Analysis</h1>
    <h3 style='color: #666;'>Interactive Dashboard with Filters</h3>
    <p style='color: #999;'>Atlantic Recording Corporation | May 2024 - November 2025</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("## 🔧 FILTERS")
st.sidebar.markdown("---")

st.sidebar.markdown("### 📅 Date Range")
min_date = df['date'].min().date()
max_date = df['date'].max().date()

col1, col2 = st.sidebar.columns(2)
with col1:
    start_date = st.date_input("Start Date", value=min_date, min_value=min_date, max_value=max_date)
with col2:
    end_date = st.date_input("End Date", value=max_date, min_value=min_date, max_value=max_date)

st.sidebar.markdown("### 🎤 Artist Filter")
artist_filter = st.sidebar.multiselect("Select Artists (leave empty for all)", options=sorted(df['artist'].unique()), default=[])

st.sidebar.markdown("### 🤝 Track Type")
collaboration_filter = st.sidebar.multiselect("Select Track Type", options=["Solo", "Collaboration"], default=["Solo", "Collaboration"])

st.sidebar.markdown("### 💿 Album Type")
album_filter = st.sidebar.multiselect("Select Album Type", options=sorted(df['album_type'].unique()), default=sorted(df['album_type'].unique()))

collab_map = {"Solo": False, "Collaboration": True}
selected_collab = [collab_map[x] for x in collaboration_filter]

df_filtered = df[
    (df['date'].dt.date >= start_date) &
    (df['date'].dt.date <= end_date) &
    (df['is_collaboration'].isin(selected_collab)) &
    (df['album_type'].isin(album_filter))
].copy()

if artist_filter:
    df_filtered = df_filtered[df_filtered['artist'].isin(artist_filter)]

st.markdown("### 📊 KEY METRICS (Filtered Data)")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("🎤 Artists", df_filtered['artist'].nunique())
with col2:
    collab_pct = df_filtered['is_collaboration'].mean() * 100 if len(df_filtered) > 0 else 0
    st.metric("🤝 Collab %", f"{collab_pct:.1f}%")
with col3:
    explicit_pct = df_filtered['is_explicit'].mean() * 100 if len(df_filtered) > 0 else 0
    st.metric("🔊 Explicit %", f"{explicit_pct:.1f}%")
with col4:
    single_pct = (df_filtered['album_type'] == 'single').mean() * 100 if len(df_filtered) > 0 else 0
    st.metric("💿 Single %", f"{single_pct:.1f}%")
with col5:
    avg_pop = df_filtered['popularity'].mean() if len(df_filtered) > 0 else 0
    st.metric("⭐ Popularity", f"{avg_pop:.1f}")

st.markdown("---")
st.info(f"📊 Showing {len(df_filtered)} entries out of {len(df)} total")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["🎤 Artists", "🤝 Network", "🔊 Explicit", "💿 Format", "⏱️ Duration", "📊 Collabs"])

with tab1:
    st.markdown("### Artist Dominance & Market Concentration")
    if len(df_filtered) > 0:
        top_n = st.slider("Show Top N Artists", 5, 30, 15)
        top_artists = df_filtered['artist'].value_counts().head(top_n)
        col1, col2 = st.columns(2)
        with col1:
            fig1 = px.bar(x=top_artists.values, y=top_artists.index, orientation='h',
                         title=f"Top {top_n} Artists", color=top_artists.values,
                         color_continuous_scale='Viridis')
            fig1.update_layout(height=500, showlegend=False)
            st.plotly_chart(fig1, use_container_width=True)
        with col2:
            fig2 = px.pie(values=top_artists.head(8).values, names=top_artists.head(8).index,
                         title="Top 8 Market Share")
            st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("No data matching filters")

with tab2:
    st.markdown("### Artist Collaboration Network")
    st.markdown("*Interactive network showing which artists collaborate together*")
    if len(df_filtered) > 0:
        collaborations = create_collaboration_network(df_filtered)
        if collaborations:
            fig_network = plot_collaboration_network(collaborations, top_n=15)
            st.plotly_chart(fig_network, use_container_width=True)
            st.markdown("#### Network Statistics")
            collab_counts = {artist: len(collabs) for artist, collabs in collaborations.items()}
            top_collab = sorted(collab_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Artists", len(collaborations))
            with col2:
                st.metric("Total Collaborations", sum(len(c) for c in collaborations.values()) // 2)
            with col3:
                st.metric("Avg Collaborators", f"{sum(len(c) for c in collaborations.values()) / len(collaborations) / 2:.1f}")
            st.markdown("#### Top 10 Most Connected")
            for i, (artist, count) in enumerate(top_collab, 1):
                st.write(f"{i}. **{artist}** - {count} collaborators")
        else:
            st.info("No collaborations found")
    else:
        st.warning("No data matching filters")

with tab3:
    st.markdown("### Explicit Content Analysis")
    if len(df_filtered) > 0:
        col1, col2 = st.columns(2)
        with col1:
            explicit_dist = df_filtered['is_explicit'].value_counts()
            fig = px.pie(values=[explicit_dist.get(False, 0), explicit_dist.get(True, 0)],
                        names=['Clean', 'Explicit'],
                        color_discrete_map={'Clean': '#4CAF50', 'Explicit': '#FF5252'})
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            if len(df_filtered) > 0:
                try:
                    explicit_by_pos = df_filtered.groupby(pd.cut(df_filtered['position'], bins=[0, 10, 25, 50]))['is_explicit'].mean() * 100
                    if len(explicit_by_pos) > 0:
                        fig = px.bar(x=['Top 10', 'Positions 11-25', 'Positions 26-50'][:len(explicit_by_pos)],
                                    y=explicit_by_pos.values, color=explicit_by_pos.values,
                                    color_continuous_scale='Reds')
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("No data for position ranges")
                except:
                    st.warning("Unable to display position analysis")
    else:
        st.warning("No data matching filters")

with tab4:
    st.markdown("### Release Format Analysis")
    if len(df_filtered) > 0:
        col1, col2 = st.columns(2)
        with col1:
            format_dist = df_filtered['album_type'].value_counts()
            fig = px.pie(values=format_dist.values, names=format_dist.index, title="Format Distribution")
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            pos_by_format = df_filtered.groupby('album_type')['position'].mean()
            fig = px.bar(x=pos_by_format.index, y=pos_by_format.values, title="Avg Position by Format",
                        color=pos_by_format.values, color_continuous_scale='Turbo')
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No data matching filters")

with tab5:
    st.markdown("### Duration Analysis")
    if len(df_filtered) > 0:
        col1, col2 = st.columns(2)
        with col1:
            fig = px.histogram(df_filtered, x='duration_minutes', nbins=30, title="Duration Distribution",
                              labels={'duration_minutes': 'Duration (minutes)'})
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            short = (df_filtered['duration_minutes'] < 3).sum()
            long = len(df_filtered) - short
            fig = px.pie(values=[short, long], names=['<3 min', '≥3 min'],
                        color_discrete_map={'<3 min': '#FF6B6B', '≥3 min': '#4ECDC4'})
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No data matching filters")

with tab6:
    st.markdown("### Collaboration Detailed Analysis")
    if len(df_filtered) > 0:
        collaborations = create_collaboration_network(df_filtered)
        col1, col2 = st.columns(2)
        with col1:
            if len(df_filtered) > 0:
                try:
                    collab_by_pos = df_filtered.groupby('position')['is_collaboration'].mean() * 100
                    if len(collab_by_pos) > 0:
                        fig = go.Figure()
                        fig.add_trace(go.Scatter(x=collab_by_pos.index, y=collab_by_pos.values,
                                                fill='tozeroy', mode='lines+markers', name='Collab %',
                                                line=dict(color='steelblue')))
                        fig.update_layout(title="Collaboration Rate by Position", xaxis_title="Position",
                                         yaxis_title="%", height=400)
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("No collaboration data")
                except:
                    st.warning("Unable to display collaboration chart")
        with col2:
            collab_dist = df_filtered['is_collaboration'].value_counts()
            fig = px.pie(values=[collab_dist.get(False, 0), collab_dist.get(True, 0)],
                        names=['Solo', 'Collaboration'],
                        color_discrete_map={'Solo': '#4CAF50', 'Collaboration': '#FF5252'})
            st.plotly_chart(fig, use_container_width=True)
        st.markdown("#### Collaboration Statistics")
        stat_col1, stat_col2, stat_col3 = st.columns(3)
        with stat_col1:
            st.metric("Solo Tracks", (~df_filtered['is_collaboration']).sum())
        with stat_col2:
            st.metric("Collaborative Tracks", df_filtered['is_collaboration'].sum())
        with stat_col3:
            st.metric("Avg Artists/Track", f"{df_filtered['num_artists'].mean():.2f}")
    else:
        st.warning("No data matching filters")

st.markdown("---")
st.markdown("<div style='text-align: center; color: #999;'><p>UK Top 50 Market Analysis | Atlantic Recording Corporation</p></div>", unsafe_allow_html=True)