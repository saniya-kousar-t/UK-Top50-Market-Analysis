# 🎵 UK Top 50 Music Market Analysis

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/saniya-kousar-t/UK-Top50-Market-Analysis?style=social)](https://github.com/saniya-kousar-t)

**Atlantic Recording Corporation** | Comprehensive Data Analysis & Interactive Dashboard

---

## 📊 Overview

Comprehensive analysis of the UK music market structure (May 2024 - November 2025) with **27,800+ playlist entries**. This project combines data science, market intelligence, and interactive visualization to provide actionable insights for music industry stakeholders.

**Key Finding:** UK market exhibits exceptional diversity (HHI = 114) with 364 unique artists competing fairly, contrary to superstar-dependent models.

---

## ✨ Features

### 📈 Core Modules
- ✅ **Artist Dominance Leaderboard** - Top performers with market share analysis
- ✅ **Collaboration Network Visualization** - Interactive network graph of artist partnerships
- ✅ **Explicit vs Clean Content Analysis** - Content type distribution & performance
- ✅ **Album Type Distribution** - Single vs Album strategy effectiveness
- ✅ **Track Duration Insights** - Listener preferences & consumption patterns

### 🎛️ Interactive Filters
- 📅 **Date Range Selector** - Custom time period analysis
- 🎤 **Artist Filter** - Multi-select specific artists
- 🤝 **Solo vs Collaboration Toggle** - Track type filtering
- 💿 **Album Type Filter** - Format-specific analysis

### 📊 Live Analytics Dashboard
- 6 interactive tabs with real-time updates
- Dynamic KPI metrics (artists, collaborations, explicit %, etc.)
- Network analysis with node sizing by collaboration count
- Position-stratified content analysis

---

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.9+
pip install streamlit plotly pandas networkx
```

### Installation
```bash
git clone https://github.com/saniya-kousar-t/UK-Top50-Market-Analysis.git
cd UK-Top50-Market-Analysis
pip install -r requirements.txt
```

### Run Dashboard
```bash
streamlit run app.py
```

Browser opens automatically at `http://localhost:8501`


---

## 🎯 Key Findings

| Metric | Value | Interpretation |
|--------|-------|-----------------|
| **HHI Index** | 114 | HIGHLY COMPETITIVE market (not concentrated) |
| **Unique Artists** | 364 | Exceptional diversity |
| **Collaboration Rate** | 18.4% | Peak at positions 11-25 (sustenance strategy) |
| **Explicit Content** | 32.1% | 40.4% in Top 10 (market accepts explicit) |
| **Singles Advantage** | +5.5 positions | Singles rank significantly higher |
| **International Artists** | 91.6% | Global market orientation |
| **Avg Duration** | 3.29 min | 60% long-form (balanced consumption) |

---

## 💡 Strategic Recommendations

1. **Build rosters with collaboration networks** - 18.4% is optimal collaboration rate
2. **Lead with SINGLES for chart penetration** - 5+ position ranking advantage
3. **Release BOTH explicit and clean versions** - Explicit for Top 10 impact, clean for longevity
4. **Fund collaboration ecosystem** - Peak effectiveness at mid-chart positions
5. **Maintain 3-3.5 min duration** - UK audience doesn't follow TikTok short-form trend
6. **Build global positioning** - 91.6% international competition demands international strategy

---

## 📊 Dashboard Tabs

### 🎤 Artists
Top N artists leaderboard with market concentration metrics (HHI, diversity score, top 5/10 share)

### 🤝 Network  
Interactive collaboration network showing which artists work together. Node size = collaboration count.

### 🔊 Explicit
Content type distribution and performance by chart position (Top 10 vs 11-25 vs 26-50)

### 💿 Format
Single vs Album analysis with average position and popularity metrics

### ⏱️ Duration
Track length distribution with short-form vs long-form breakdown

### 📊 Collaborations
Detailed collaboration metrics including position-based analysis and artist statistics

---

## 📈 Analysis Methodology

1. **Data Validation** - 27,800 entries, 0 missing values
2. **Artist Dominance** - Herfindahl-Hirschman Index (HHI) calculation
3. **Collaboration Network** - Graph-based analysis with NetworkX
4. **Content Analysis** - Chi-square tests, t-tests, effect size calculations
5. **Market Structure** - Concentration ratios, diversity indices
6. **Statistical Rigor** - α = 0.05, Cohen's d effect sizes
7. **Time Series** - 6-month trend analysis

---

## 🛠️ Technology Stack

- **Backend:** Python 3.9+, Pandas, NumPy
- **Visualization:** Plotly, NetworkX
- **Dashboard:** Streamlit
- **Analysis:** SciPy, Scikit-learn
- **Data:** CSV (27,800 rows × 14 columns)

---

## 📄 Additional Documents

### Research Paper
`UK_Music_Market_Research_Paper.txt` - 8,000+ word academic paper with:
- Abstract, methodology, results, discussion
- Statistical analysis and hypothesis testing
- Limitations and future research directions

### Executive Summary
`UK_Market_Executive_Summary.txt` - Strategic findings for business stakeholders

### Government Briefing  
`UK_Music_Market_Government_Briefing.txt` - Policy recommendations and cultural intelligence

---

## 👤 Author

**Saniya Kousar T*
🔗 **GitHub:** github.com/saniya-kousar-t  
💼 **LinkedIn:** www.linkedin.com/in/
saniya-kousar-t-1272b925b


---

## 📜 License

MIT License - Feel free to use and modify

---

## 🤝 Contributing

Found an insight? Have suggestions? Open an issue or submit a PR!

---

## 📞 Support

Questions about the analysis? 
- Check the Jupyter notebook for detailed methodology
- Read the research paper for academic background
- Review the government briefing for policy context

---

**Last Updated:** November 2025  
**Data Period:** May 18, 2024 - November 27, 2025  
**Dataset Size:** 27,800 entries | 364 unique artists | 14 columns
