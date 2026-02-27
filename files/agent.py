"""
Hyper-Local Food Trend Agent — Streamlit Dashboard
Blue & Grey theme | Run: streamlit run app.py
"""

import json
import random
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from typing import Optional
import anthropic

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG & CUSTOM CSS
# ─────────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Food Trend Agent",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Sora:wght@400;600;700&display=swap');

/* ── Root palette ── */
:root {
  --blue-deep:   #0D1B2A;
  --blue-dark:   #1A2E44;
  --blue-mid:    #1E4D8C;
  --blue-bright: #2979FF;
  --blue-light:  #5B9BF8;
  --blue-pale:   #E8F1FF;
  --grey-dark:   #2D3748;
  --grey-mid:    #4A5568;
  --grey-light:  #A0AEC0;
  --grey-pale:   #EDF2F7;
  --white:       #F7FAFC;
  --accent:      #00B4D8;
}

/* ── Global ── */
html, body, [class*="css"] {
  font-family: 'Inter', sans-serif;
}

/* ── App background ── */
.stApp {
  background: linear-gradient(160deg, #0D1B2A 0%, #1A2E44 40%, #0D1B2A 100%);
  min-height: 100vh;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
  background: #0D1B2A !important;
  border-right: 1px solid rgba(41,121,255,0.15);
}
[data-testid="stSidebar"] * { color: #A0AEC0 !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: #E8F1FF !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stTextInput label { color: #A0AEC0 !important; font-size: 0.75rem !important; letter-spacing: 0.08em; text-transform: uppercase; }

/* ── Selectbox & Input in sidebar ── */
[data-testid="stSidebar"] [data-baseweb="select"] > div,
[data-testid="stSidebar"] [data-baseweb="input"] > div {
  background: rgba(255,255,255,0.05) !important;
  border: 1px solid rgba(41,121,255,0.3) !important;
  border-radius: 8px !important;
  color: #E8F1FF !important;
}

/* ── Main content area ── */
[data-testid="stMainBlockContainer"] {
  background: transparent;
  padding-top: 1.5rem;
}

/* ── Metric cards ── */
[data-testid="stMetric"] {
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(41,121,255,0.2);
  border-radius: 12px;
  padding: 1rem 1.25rem !important;
  backdrop-filter: blur(8px);
}
[data-testid="stMetric"] label {
  color: #A0AEC0 !important;
  font-size: 0.7rem !important;
  letter-spacing: 0.1em;
  text-transform: uppercase;
}
[data-testid="stMetricValue"] {
  color: #E8F1FF !important;
  font-family: 'Sora', sans-serif !important;
  font-size: 1.8rem !important;
}
[data-testid="stMetricDelta"] { color: #00B4D8 !important; }

/* ── Primary button ── */
.stButton > button[kind="primary"] {
  background: linear-gradient(135deg, #1E4D8C, #2979FF) !important;
  color: white !important;
  border: none !important;
  border-radius: 10px !important;
  padding: 0.6rem 2rem !important;
  font-family: 'Inter', sans-serif !important;
  font-weight: 600 !important;
  letter-spacing: 0.02em;
  transition: all 0.2s !important;
  box-shadow: 0 4px 16px rgba(41,121,255,0.3) !important;
}
.stButton > button[kind="primary"]:hover {
  transform: translateY(-1px);
  box-shadow: 0 8px 24px rgba(41,121,255,0.45) !important;
}

/* ── Secondary button ── */
.stButton > button[kind="secondary"] {
  background: rgba(255,255,255,0.06) !important;
  color: #A0AEC0 !important;
  border: 1px solid rgba(160,174,192,0.25) !important;
  border-radius: 10px !important;
}

/* ── Expander ── */
[data-testid="stExpander"] {
  background: rgba(255,255,255,0.03) !important;
  border: 1px solid rgba(41,121,255,0.15) !important;
  border-radius: 12px !important;
}
[data-testid="stExpander"] summary {
  color: #A0AEC0 !important;
  font-size: 0.875rem !important;
}

/* ── Divider ── */
hr { border-color: rgba(41,121,255,0.12) !important; }

/* ── Headings ── */
h1 { font-family: 'Sora', sans-serif !important; color: #E8F1FF !important; }
h2, h3 { font-family: 'Sora', sans-serif !important; color: #CBD5E0 !important; }
p, li { color: #A0AEC0 !important; }
strong { color: #E8F1FF !important; }

/* ── Info / success / warning boxes ── */
[data-testid="stInfo"] {
  background: rgba(0,180,216,0.1) !important;
  border-left: 3px solid #00B4D8 !important;
  border-radius: 0 8px 8px 0 !important;
  color: #A0AEC0 !important;
}
[data-testid="stSuccess"] {
  background: rgba(72,187,120,0.1) !important;
  border-left: 3px solid #48BB78 !important;
  border-radius: 0 8px 8px 0 !important;
}

/* ── Tab styling ── */
[data-baseweb="tab-list"] {
  background: rgba(255,255,255,0.03) !important;
  border-radius: 10px;
  padding: 4px;
  gap: 4px;
}
[data-baseweb="tab"] {
  border-radius: 8px !important;
  color: #A0AEC0 !important;
  font-size: 0.875rem !important;
}
[aria-selected="true"] {
  background: rgba(41,121,255,0.2) !important;
  color: #5B9BF8 !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(41,121,255,0.3); border-radius: 3px; }

/* ── Dish card ── */
.dish-card {
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(41,121,255,0.2);
  border-radius: 14px;
  padding: 1.25rem 1.4rem;
  margin-bottom: 0.75rem;
  border-left: 3px solid #2979FF;
  transition: all 0.2s;
}
.dish-card:hover { border-left-color: #00B4D8; background: rgba(255,255,255,0.06); }
.dish-name { font-family: 'Sora', sans-serif; font-size: 1.05rem; color: #E8F1FF; font-weight: 600; margin-bottom: 0.4rem; }
.dish-desc { font-size: 0.85rem; color: #A0AEC0; line-height: 1.55; margin-bottom: 0.6rem; }
.dish-meta { display: flex; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 0.5rem; }
.tag { display: inline-block; font-size: 0.7rem; padding: 0.2rem 0.65rem; border-radius: 100px; font-weight: 500; }
.tag-trend { background: rgba(41,121,255,0.2); color: #5B9BF8; }
.tag-price { background: rgba(0,180,216,0.15); color: #00B4D8; }
.dish-hook { font-size: 0.75rem; color: #4A5568; font-style: italic; }

/* ── Post feed item ── */
.post-item {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(41,121,255,0.1);
  border-radius: 10px;
  padding: 0.85rem 1rem;
  margin-bottom: 0.5rem;
  display: flex;
  gap: 0.75rem;
  align-items: flex-start;
}
.post-text { font-size: 0.82rem; color: #A0AEC0; line-height: 1.4; }
.post-sub { font-size: 0.7rem; color: #4A5568; margin-top: 0.25rem; }

/* ── Insight box ── */
.insight-box {
  background: linear-gradient(135deg, rgba(30,77,140,0.3), rgba(41,121,255,0.15));
  border: 1px solid rgba(41,121,255,0.3);
  border-radius: 14px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
}
.insight-label { font-size: 0.65rem; letter-spacing: 0.12em; text-transform: uppercase; color: #00B4D8; margin-bottom: 0.5rem; }
.insight-text { font-family: 'Sora', sans-serif; font-size: 1rem; color: #CBD5E0; line-height: 1.7; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# DATA LAYER
# ─────────────────────────────────────────────────────────────────────────────

MOCK_POSTS = [
    {"platform": "instagram", "text": "Obsessed with this truffle butter pasta at La Nonna! #food #truffle #pasta #foodie", "likes": 1240, "location": "Downtown"},
    {"platform": "instagram", "text": "Birria tacos are EVERYTHING right now 🔥 #birria #tacos #mexicanfood", "likes": 3400, "location": "Eastside"},
    {"platform": "instagram", "text": "Korean corn dogs > everything. Change my mind. #koreancorndog #streetfood", "likes": 2100, "location": "Koreatown"},
    {"platform": "instagram", "text": "Smash burgers with wagyu beef — this weekend's obsession #wagyu #smashburger", "likes": 1870, "location": "Westside"},
    {"platform": "instagram", "text": "Can't stop thinking about that miso caramel croissant #croissant #fusion #bakery", "likes": 4500, "location": "Northside"},
    {"platform": "twitter", "text": "birria tacos > all tacos. fight me", "likes": 890, "location": "City Center"},
    {"platform": "twitter", "text": "every restaurant needs a smash burger option. it's the law.", "likes": 560, "location": "Westside"},
    {"platform": "twitter", "text": "miso + caramel is the combo i didn't know i needed", "likes": 1200, "location": "Northside"},
    {"platform": "tiktok", "text": "Making viral Dubai chocolate at home #dubai #chocolate #viral #foodtok", "likes": 45000, "location": "Suburbs"},
    {"platform": "tiktok", "text": "Birria ramen fusion — the collab nobody asked for but everyone needed 🔥", "likes": 22000, "location": "Eastside"},
    {"platform": "tiktok", "text": "smash burger tutorial blew up 🍔 #smashburger #burger #foodtok", "likes": 31000, "location": "Westside"},
    {"platform": "tiktok", "text": "truffle everything is back. truffle fries, truffle pasta, truffle butter #truffle", "likes": 18000, "location": "Downtown"},
    {"platform": "yelp", "text": "The wagyu smash burger was incredible. Worth every penny.", "likes": 45, "location": "Westside"},
    {"platform": "yelp", "text": "Birria tacos — crispy, cheesy, and the consommé was perfect for dipping.", "likes": 67, "location": "Eastside"},
    {"platform": "yelp", "text": "Dubai chocolate dessert — unique and absolutely delicious.", "likes": 89, "location": "Suburbs"},
]

PLATFORM_EMOJI = {"instagram": "📸", "tiktok": "🎵", "twitter": "🐦", "yelp": "⭐"}

def scrape_local_trends(location: Optional[str] = None) -> list[dict]:
    posts = MOCK_POSTS.copy()
    if location and location != "All":
        posts = [p for p in posts if location.lower() in p["location"].lower()] or posts
    for post in posts:
        post["likes"] = post["likes"] + random.randint(-200, 600)
        post["scraped_at"] = datetime.now().isoformat()
    return posts

def analyze_trends(posts: list[dict]) -> dict:
    keywords = {}
    food_terms = [
        "birria", "truffle", "wagyu", "smash burger", "miso", "caramel",
        "croissant", "tacos", "ramen", "korean corn dog", "dubai chocolate",
        "pasta", "burger", "chocolate", "fusion"
    ]
    for post in posts:
        text = post["text"].lower()
        for term in food_terms:
            if term in text:
                keywords[term] = keywords.get(term, 0) + post["likes"]
    sorted_trends = sorted(keywords.items(), key=lambda x: x[1], reverse=True)
    saturday = datetime.now() + timedelta(days=(5 - datetime.now().weekday()) % 7 or 7)
    return {
        "top_ingredients": [k for k, _ in sorted_trends[:5]],
        "all_scores": dict(sorted_trends),
        "total_posts_analyzed": len(posts),
        "analysis_date": datetime.now().strftime("%Y-%m-%d"),
        "weekend": saturday.strftime("%B %d"),
    }

def suggest_dishes(trends: dict, restaurant_type: str, api_key: str) -> dict:
    client = anthropic.Anthropic(api_key=api_key)
    prompt = f"""You are a creative restaurant consultant designing weekend specials.

Local social media food trends:
- Top trending: {', '.join(trends['top_ingredients'])}
- Engagement scores: {json.dumps(trends['all_scores'], indent=2)}
- Weekend: {trends['weekend']}
- Restaurant type: {restaurant_type}

Generate 4 creative weekend special dishes. Return ONLY valid JSON:
{{
  "dishes": [
    {{
      "name": "Dish Name",
      "description": "Brief appetizing description (2 sentences)",
      "trending_element": "trend it capitalizes on",
      "price_range": "$XX-$XX",
      "social_hook": "Short Instagram caption"
    }}
  ],
  "marketing_headline": "Punchy weekend specials headline",
  "key_insight": "One sentence on why these trends matter right now"
}}"""
    msg = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    raw = msg.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())

def generate_report(trends: dict, suggestions: dict) -> str:
    lines = [
        f"# 🍽️ Weekly Food Trend Report — {trends['analysis_date']}",
        f"\n**Weekend Focus:** {trends['weekend']} · **Posts Analyzed:** {trends['total_posts_analyzed']}",
        "\n---\n",
        "## 📈 Top Trending Items\n",
    ]
    for item, score in list(trends["all_scores"].items())[:5]:
        lines.append(f"- **{item.title()}** — {score:,} engagement points")
    lines += [
        "\n---\n",
        "## 🍴 Weekend Specials\n",
        f"> {suggestions['marketing_headline']}\n",
    ]
    for i, d in enumerate(suggestions["dishes"], 1):
        lines += [
            f"### {i}. {d['name']} ({d['price_range']})",
            f"{d['description']}",
            f"- 🔥 Trend: *{d['trending_element']}*",
            f"- 📸 Hook: *\"{d['social_hook']}\"*\n",
        ]
    lines += ["---\n", f"## 💡 Key Insight\n\n{suggestions['key_insight']}",
              "\n\n*Generated by Hyper-Local Food Trend Agent · Powered by Claude*"]
    return "\n".join(lines)

# ─────────────────────────────────────────────────────────────────────────────
# PLOTLY CHART HELPERS (dark blue/grey theme)
# ─────────────────────────────────────────────────────────────────────────────

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#A0AEC0"),
    margin=dict(l=0, r=0, t=30, b=0),
    showlegend=False,
)

def make_bar_chart(all_scores: dict):
    items = list(all_scores.items())[:8]
    names = [k.title() for k, _ in items]
    values = [v for _, v in items]
    colors = [f"rgba(41,121,255,{0.9 - i*0.08})" for i in range(len(names))]
    fig = go.Figure(go.Bar(
        x=values, y=names, orientation="h",
        marker=dict(color=colors, line=dict(width=0)),
        hovertemplate="<b>%{y}</b><br>Score: %{x:,}<extra></extra>",
    ))
    fig.update_layout(
        **PLOTLY_LAYOUT,
        title=dict(text="Engagement Scores by Food Item", font=dict(color="#CBD5E0", size=13)),
        height=320,
        yaxis=dict(autorange="reversed", gridcolor="rgba(255,255,255,0.04)", tickfont=dict(size=11)),
        xaxis=dict(gridcolor="rgba(255,255,255,0.06)", tickfont=dict(size=10)),
    )
    return fig

def make_donut_chart(all_scores: dict):
    items = list(all_scores.items())[:5]
    labels = [k.title() for k, _ in items]
    values = [v for _, v in items]
    palette = ["#2979FF", "#00B4D8", "#5B9BF8", "#1E4D8C", "#4A5568"]
    fig = go.Figure(go.Pie(
        labels=labels, values=values,
        hole=0.55,
        marker=dict(colors=palette, line=dict(width=0)),
        hovertemplate="<b>%{label}</b><br>%{percent}<extra></extra>",
        textfont=dict(size=11, color="#E8F1FF"),
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color="#A0AEC0"),
        margin=dict(l=0, r=0, t=30, b=0),
        title=dict(text="Trend Share (Top 5)", font=dict(color="#CBD5E0", size=13)),
        height=280,
        showlegend=True,
        annotations=[dict(text="Trends", x=0.5, y=0.5, font_size=13, showarrow=False, font_color="#A0AEC0")],
        legend=dict(font=dict(color="#A0AEC0", size=11)),
    )
    return fig

def make_platform_chart(posts: list[dict]):
    platform_likes = {}
    for p in posts:
        platform_likes[p["platform"]] = platform_likes.get(p["platform"], 0) + p["likes"]
    platforms = list(platform_likes.keys())
    values = list(platform_likes.values())
    palette = ["#2979FF", "#00B4D8", "#5B9BF8", "#1A2E44"]
    fig = go.Figure(go.Bar(
        x=platforms, y=values,
        marker=dict(color=palette[:len(platforms)], line=dict(width=0)),
        hovertemplate="<b>%{x}</b><br>Total Likes: %{y:,}<extra></extra>",
    ))
    fig.update_layout(
        **PLOTLY_LAYOUT,
        title=dict(text="Engagement by Platform", font=dict(color="#CBD5E0", size=13)),
        height=260,
        xaxis=dict(gridcolor="rgba(0,0,0,0)", tickfont=dict(size=11, color="#A0AEC0")),
        yaxis=dict(gridcolor="rgba(255,255,255,0.06)", tickfont=dict(size=10)),
    )
    return fig

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("### 🍽️ Food Trend Agent")
    st.markdown('<p style="font-size:0.75rem;color:#4A5568;margin-top:-0.5rem;">Hyper-Local · #34 · Food Industry</p>', unsafe_allow_html=True)
    st.divider()

    if "api_key" not in st.session_state:
        st.session_state.api_key = ""
    api_key_input = st.text_input("🔑 Anthropic API Key", type="password", placeholder="sk-ant-...", value=st.session_state.api_key)
    if api_key_input:
        st.session_state.api_key = api_key_input
    api_key = st.session_state.api_key
    st.caption("Your key stays local and is never stored.")
    st.divider()

    location = st.selectbox("📍 Location", ["Downtown", "Eastside", "Westside", "Northside", "Koreatown", "Suburbs", "All"])
    restaurant_type = st.selectbox("🏪 Restaurant Type", ["Casual Dining", "Bistro", "Fine Dining", "Café", "Food Truck", "Bar & Grill"])

    run_btn = st.button("✦ Run Agent", type="primary", use_container_width=True)
    demo_btn = st.button("⚡ Quick Demo (no API key)", type="secondary", use_container_width=True)

    st.divider()
    st.markdown("""
    <div style='font-size:0.72rem;color:#2D3748;line-height:1.7'>
    <b style='color:#4A5568'>Tech Stack</b><br>
    Python · Anthropic SDK<br>
    Streamlit · Plotly<br>
    BeautifulSoup · Requests<br><br>
    <b style='color:#4A5568'>Pipeline</b><br>
    1. Scrape social posts<br>
    2. Analyze food trends<br>
    3. Claude generates dishes<br>
    4. Weekly report output
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# DEMO DATA
# ─────────────────────────────────────────────────────────────────────────────

DEMO_SUGGESTIONS = {
    "marketing_headline": "This Weekend: Trending Tastes, Locally Inspired",
    "key_insight": "Birria and smash burger culture are dominating local TikTok feeds, signaling demand for bold, shareable comfort food that photographs beautifully.",
    "dishes": [
        {"name": "Birria Wagyu Smash", "description": "Wagyu smash patty dipped in rich birria consommé, melted Oaxacan cheese, and crispy confit onions on a brioche bun. A crossover hit waiting to happen.", "trending_element": "birria + smash burger", "price_range": "$18–$22", "social_hook": "The smash burger got a birria glow-up 🌶️🔥"},
        {"name": "Truffle Miso Croissant Toast", "description": "Buttery croissant toasted flat, spread with white miso caramel butter and finished with shaved black truffle and sea salt. Brunch redefined.", "trending_element": "truffle + miso caramel", "price_range": "$14–$16", "social_hook": "Brunch just evolved. Trust us ✨"},
        {"name": "Dubai Chocolate Smash Tacos", "description": "Crispy smash-style street tacos filled with pistachio-studded Dubai chocolate ganache and pickled chilies. Sweet heat in every bite.", "trending_element": "dubai chocolate + tacos", "price_range": "$16–$20", "social_hook": "Dubai chocolate met birria tacos and we're never going back 🍫🌮"},
        {"name": "Truffle Corn Dog Bites", "description": "Mini Korean-style corn dogs with a mozzarella core, served with truffle aioli and spiced honey. Shareworthy by design.", "trending_element": "korean corn dog + truffle", "price_range": "$12–$15", "social_hook": "Korean corn dogs got a luxury upgrade 🌭✨"},
    ]
}

# ─────────────────────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("""
<h1 style='margin-bottom:0.1rem'>Hyper-Local Food Trend Agent</h1>
<p style='color:#4A5568;font-size:0.9rem;margin-bottom:1.5rem'>
  Scrapes local social media → identifies viral food trends → suggests weekend specials using Claude AI
</p>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# RUN LOGIC
# ─────────────────────────────────────────────────────────────────────────────

if "results" not in st.session_state:
    st.session_state.results = None

if run_btn:
    if not api_key:
        st.error("Please enter your Anthropic API key in the sidebar.")
    else:
        with st.spinner("🔍 Scraping social media posts…"):
            posts = scrape_local_trends(location)
        with st.spinner("📊 Analyzing food trends…"):
            trends = analyze_trends(posts)
        with st.spinner("🤖 Consulting Claude for dish suggestions…"):
            try:
                suggestions = suggest_dishes(trends, restaurant_type, api_key)
            except Exception as e:
                st.error(f"API error: {e}")
                st.stop()
        with st.spinner("📝 Generating report…"):
            report = generate_report(trends, suggestions)
        st.session_state.results = {"trends": trends, "suggestions": suggestions, "report": report, "posts": posts}
        st.success("✅ Agent run complete!")

if demo_btn:
    with st.spinner("⚡ Loading demo data…"):
        posts = scrape_local_trends(location)
        trends = analyze_trends(posts)
        report = generate_report(trends, DEMO_SUGGESTIONS)
        st.session_state.results = {"trends": trends, "suggestions": DEMO_SUGGESTIONS, "report": report, "posts": posts}
    st.success("Demo data loaded — run with a real API key to get live Claude suggestions!")

# ─────────────────────────────────────────────────────────────────────────────
# RESULTS
# ─────────────────────────────────────────────────────────────────────────────

if st.session_state.results:
    R = st.session_state.results
    trends = R["trends"]
    suggestions = R["suggestions"]
    posts = R["posts"]

    # ── Metrics ──
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Posts Analyzed", trends["total_posts_analyzed"], "Live scrape")
    col2.metric("Top Trend", trends["top_ingredients"][0].title())
    col3.metric("Dishes Suggested", len(suggestions["dishes"]), "Weekend specials")
    col4.metric("Weekend Target", trends["weekend"])

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Insight ──
    st.markdown(f"""
    <div class="insight-box">
      <div class="insight-label">💡 Claude's Key Insight</div>
      <div class="insight-text">{suggestions['key_insight']}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Tabs ──
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Trends", "🍴 Dish Suggestions", "📱 Social Feed", "📄 Weekly Report"])

    with tab1:
        c1, c2 = st.columns([3, 2])
        with c1:
            st.plotly_chart(make_bar_chart(trends["all_scores"]), use_container_width=True)
        with c2:
            st.plotly_chart(make_donut_chart(trends["all_scores"]), use_container_width=True)

        st.plotly_chart(make_platform_chart(posts), use_container_width=True)

        st.markdown("**Top 5 Trending Items**")
        for i, (item, score) in enumerate(list(trends["all_scores"].items())[:5], 1):
            pct = int(score / max(trends["all_scores"].values()) * 100)
            st.markdown(f"`#{i}` **{item.title()}** — {score:,} pts")
            st.progress(pct / 100)

    with tab2:
        st.markdown(f'<p style="color:#5B9BF8;font-style:italic;margin-bottom:1.25rem">"{suggestions["marketing_headline"]}"</p>', unsafe_allow_html=True)
        for i, dish in enumerate(suggestions["dishes"], 1):
            st.markdown(f"""
            <div class="dish-card">
              <div class="dish-name">#{i} {dish['name']}</div>
              <div class="dish-desc">{dish['description']}</div>
              <div class="dish-meta">
                <span class="tag tag-trend">🔥 {dish['trending_element']}</span>
                <span class="tag tag-price">{dish['price_range']}</span>
              </div>
              <div class="dish-hook">📸 "{dish['social_hook']}"</div>
            </div>
            """, unsafe_allow_html=True)

    with tab3:
        st.markdown(f"**{len(posts)} posts scraped** · Location: {location}")
        for post in posts:
            emoji = PLATFORM_EMOJI.get(post["platform"], "📱")
            st.markdown(f"""
            <div class="post-item">
              <div style="font-size:1.3rem;flex-shrink:0">{emoji}</div>
              <div>
                <div class="post-text">{post['text']}</div>
                <div class="post-sub">❤ {post['likes']:,} · {post.get('location','—')} · {post['platform'].title()}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    with tab4:
        st.download_button(
            label="⬇️ Download Report (.md)",
            data=R["report"],
            file_name=f"food_trend_report_{trends['analysis_date']}.md",
            mime="text/markdown",
        )
        st.markdown(R["report"])

else:
    # Welcome state
    st.markdown("""
    <div style='text-align:center;padding:4rem 2rem;'>
      <div style='font-size:3.5rem;margin-bottom:1rem'>🍽️</div>
      <h3 style='color:#CBD5E0;font-family:Sora,sans-serif'>Ready to analyze local food trends</h3>
      <p style='color:#4A5568;max-width:400px;margin:0 auto'>
        Configure your location and restaurant type in the sidebar,
        then click <strong style='color:#5B9BF8'>Run Agent</strong> or try the <strong style='color:#5B9BF8'>Quick Demo</strong>.
      </p>
    </div>
    """, unsafe_allow_html=True)
