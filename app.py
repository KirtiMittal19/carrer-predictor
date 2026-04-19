import streamlit as st
from model import CAT_MAP, CONF_MAP, predict_btech, predict_bcom
from roadmaps import ROADMAPS

st.set_page_config(page_title="Career Predictor", page_icon="🎯", layout="centered")

field = st.session_state.get("field", "home")

# ── Theme ─────────────────────────────────────────────────────────
if field == "BTech":
    A1, A2    = "#6366F1", "#06B6D4"
    PILL_BG   = "#EEF2FF"
    PILL_CLR  = "#4338CA"
    CARD_TOP  = "linear-gradient(135deg, #6366F1 0%, #06B6D4 100%)"
    GLOW      = "rgba(99,102,241,0.15)"
    RADIO_CLR = "#6366F1"
    T = [("#EEF2FF","#4338CA","#C7D2FE"),
         ("#ECFEFF","#0E7490","#A5F3FC"),
         ("#EEF2FF","#4338CA","#C7D2FE")]
elif field == "BCom":
    A1, A2    = "#F59E0B", "#EF4444"
    PILL_BG   = "#FFFBEB"
    PILL_CLR  = "#92400E"
    CARD_TOP  = "linear-gradient(135deg, #F59E0B 0%, #EF4444 100%)"
    GLOW      = "rgba(245,158,11,0.15)"
    RADIO_CLR = "#F59E0B"
    T = [("#FFFBEB","#92400E","#FCD34D"),
         ("#FFF1F2","#9F1239","#FECDD3"),
         ("#FFFBEB","#92400E","#FCD34D")]
else:
    A1, A2    = "#8B5CF6", "#EC4899"
    PILL_BG   = "#F5F3FF"
    PILL_CLR  = "#5B21B6"
    CARD_TOP  = "linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%)"
    GLOW      = "rgba(139,92,246,0.15)"
    RADIO_CLR = "#8B5CF6"
    T = [("#F5F3FF","#5B21B6","#DDD6FE"),
         ("#FDF2F8","#831843","#FBCFE8"),
         ("#F5F3FF","#5B21B6","#DDD6FE")]

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=Inter:wght@400;500;600;700&display=swap');

*, *::before, *::after {{ box-sizing: border-box; }}

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif !important;
    background-color: #F1F5F9 !important;
    color: #0F172A !important;
    -webkit-text-fill-color: #0F172A !important;
}}
.block-container {{
    max-width: 640px !important;
    padding-top: 2.5rem !important;
    padding-bottom: 3rem !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
    margin: 0 auto !important;
}}
#MainMenu, footer, header {{ visibility: hidden; }}
.stApp {{ background-color: #F1F5F9 !important; }}

/* ── Animations ── */
@keyframes fadeUp {{
    from {{ opacity:0; transform:translateY(14px); }}
    to   {{ opacity:1; transform:translateY(0); }}
}}
@keyframes shimmer {{
    0%   {{ background-position:-200% center; }}
    100% {{ background-position: 200% center; }}
}}
section.main > div {{ animation: fadeUp 0.4s ease both; }}

/* ── Typography ── */
h1 {{
    font-family: 'Syne', sans-serif !important;
    font-weight: 800 !important;
    font-size: 2.2rem !important;
    color: #0F172A !important;
    -webkit-text-fill-color: #0F172A !important;
    line-height: 1.2 !important;
    letter-spacing: -0.5px !important;
}}
h2, h3 {{
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    color: #0F172A !important;
    -webkit-text-fill-color: #0F172A !important;
}}

/* ── Accent span ── */
.accent {{
    background: {CARD_TOP};
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-family: 'Syne', sans-serif;
    font-weight: 800;
}}

/* ── Top strip card ── */
.top-card {{
    background: #fff;
    border-radius: 20px;
    border: 1px solid #E2E8F0;
    box-shadow: 0 2px 16px rgba(0,0,0,0.06);
    padding: 1.8rem 2rem;
    margin-bottom: 1.2rem;
    position: relative;
    overflow: hidden;
}}
.top-card::before {{
    content: '';
    position: absolute; top:0; left:0; right:0; height:4px;
    background: {CARD_TOP};
}}
.top-card-label {{
    font-size: 0.7rem; font-weight: 700;
    letter-spacing: 1.2px; text-transform: uppercase;
    color: #64748B; -webkit-text-fill-color: #64748B;
    margin-bottom: 0.3rem;
}}
.top-card-title {{
    font-family: 'Syne', sans-serif;
    font-size: 1.6rem; font-weight: 700;
    line-height: 1.3;
}}
.top-card-sub {{
    font-size: 0.88rem; color: #64748B;
    -webkit-text-fill-color: #64748B; margin-top: 0.3rem;
}}

/* ── Stat pill (like GATE score boxes) ── */
.stat-row {{ display:grid; grid-template-columns: repeat(5, 1fr); gap:0.6rem; margin:1rem 0; }}

@media (max-width: 600px) {{
    .stat-row { grid-template-columns: repeat(2, 1fr); }
    .stat-pill-label { font-size: 0.65rem; white-space: nowrap; }
    .stat-pill-val { font-size: 1.1rem; white-space: nowrap; }
    .top-card-title { font-size: 1.3rem; }
}}
.stat-pill {{
    background: #fff;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 0.6rem 1rem;
    flex: 1; min-width: 80px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}}
.stat-pill-label {{
    font-size: 0.75rem; font-weight: 600;
    letter-spacing: 0.8px; text-transform: uppercase;
    color: #94A3B8; -webkit-text-fill-color: #94A3B8;
    margin-bottom: 2px;
}}
.stat-pill-val {{
    font-family: 'Inter', sans-serif;
    font-size: 1.3rem; font-weight: 700;
}}

/* ── Buttons ── */
.stButton > button {{
    background: {CARD_TOP} !important;
    color: #fff !important;
    -webkit-text-fill-color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 1.4rem !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    transition: all 0.18s ease !important;
    box-shadow: 0 3px 12px {GLOW} !important;
    width: 100% !important;
}}
.stButton > button:hover {{
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 22px {GLOW} !important;
    filter: brightness(1.06) !important;
}}
.stButton > button:active {{ transform: translateY(0) !important; }}

/* ── Radio (question cards) ── */
div[data-testid="stRadio"] {{
    background: #fff !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 14px !important;
    padding: 1.2rem 1.4rem !important;
    margin-bottom: 0.75rem !important;
    box-shadow: 0 1px 6px rgba(0,0,0,0.05) !important;
    transition: border-color 0.2s, box-shadow 0.2s, transform 0.2s !important;
    width: 100% !important;
}}
div[data-testid="stRadio"]:hover {{
    border-color: {A1} !important;
    box-shadow: 0 4px 18px {GLOW} !important;
    transform: translateY(-1px) !important;
}}
div[data-testid="stRadio"] > label {{
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    color: #0F172A !important;
    -webkit-text-fill-color: #0F172A !important;
    display: block !important;
    margin-bottom: 0.5rem !important;
    line-height: 1.4 !important;
}}
div[data-testid="stRadio"] label {{
    font-size: 0.86rem !important;
    color: #475569 !important;
    -webkit-text-fill-color: #475569 !important;
    padding: 2px 0 !important;
}}
div[data-testid="stRadio"] label:hover {{
    color: {A1} !important;
    -webkit-text-fill-color: {A1} !important;
}}

/* Remove selected option highlight background completely */
div[data-testid="stRadio"] label[data-selected="true"],
div[data-testid="stRadio"] label[aria-checked="true"],
[data-baseweb="radio"] label {{
    background: transparent !important;
    background-color: transparent !important;
}}
/* Override Streamlit radio accent color */
.st-bx {{ border-color: {A1} !important; }}
.st-by {{ border-color: {A1} !important; }}
[data-baseweb="radio"] [role="radio"][aria-checked="true"] div {{
    background-color: {A1} !important;
    border-color: {A1} !important;
}}
/* Kill the orange/yellow highlight on selected option */
[data-baseweb="radio"] label > div:first-child {{
    background: transparent !important;
}}
div[data-testid="stRadio"] > div > label {{
    background: transparent !important;
    padding: 2px 4px !important;
    border-radius: 4px !important;
}}

/* ── Section tag ── */
.stag {{
    display: inline-flex; align-items: center; gap: 5px;
    font-size: 0.68rem; font-weight: 700;
    letter-spacing: 0.8px; text-transform: uppercase;
    padding: 4px 12px; border-radius: 6px;
    margin-bottom: 0.9rem; border: 1px solid;
    font-family: 'Inter', sans-serif;
}}
.stag-a {{ background:{T[0][0]}; color:{T[0][1]}; -webkit-text-fill-color:{T[0][1]}; border-color:{T[0][2]}; }}
.stag-b {{ background:{T[1][0]}; color:{T[1][1]}; -webkit-text-fill-color:{T[1][1]}; border-color:{T[1][2]}; }}
.stag-c {{ background:{T[2][0]}; color:{T[2][1]}; -webkit-text-fill-color:{T[2][1]}; border-color:{T[2][2]}; }}

/* ── Result card ── */
.result-card {{
    background: #fff;
    border: 1px solid #E2E8F0;
    border-radius: 20px;
    padding: 2.2rem 2rem;
    text-align: center;
    box-shadow: 0 4px 24px rgba(0,0,0,0.07);
    position: relative; overflow: hidden;
    margin-bottom: 1.2rem;
}}
.result-card::before {{
    content: '';
    position: absolute; top:0; left:0; right:0; height:5px;
    background: {CARD_TOP};
    background-size: 200% auto;
    animation: shimmer 3s linear infinite;
}}
.result-emoji {{ font-size: 3rem; margin-bottom: 0.5rem; }}
.result-name {{
    font-family: 'Syne', sans-serif;
    font-size: 1.9rem; font-weight: 800;
    background: {CARD_TOP};
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.25rem;
}}
.result-sub {{
    font-size: 0.85rem; color: #64748B;
    -webkit-text-fill-color: #64748B;
}}
.conf-pill {{
    display: inline-block; margin-top: 0.9rem;
    background: {T[0][0]}; color: {T[0][1]};
    -webkit-text-fill-color: {T[0][1]};
    font-weight: 700; font-size: 0.82rem;
    padding: 5px 16px; border-radius: 6px;
    border: 1px solid {T[0][2]};
    font-family: 'Inter', sans-serif;
}}

/* ── Roadmap steps ── */
.rm-wrap {{ display:flex; flex-direction:column; gap:0.6rem; }}
.rm-step {{
    background: #fff;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 0.9rem 1.1rem;
    display: flex; gap: 0.75rem; align-items: flex-start;
    box-shadow: 0 1px 5px rgba(0,0,0,0.04);
    transition: border-color 0.18s, box-shadow 0.18s, transform 0.18s;
}}
.rm-step:hover {{
    border-color: {A1};
    box-shadow: 0 4px 16px {GLOW};
    transform: translateX(3px);
}}
.rm-num {{
    min-width: 24px; height: 24px;
    background: {CARD_TOP};
    color: #fff; -webkit-text-fill-color: #fff;
    border-radius: 6px;
    font-size: 0.7rem; font-weight: 800;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0; margin-top: 1px;
    font-family: 'Inter', sans-serif;
}}
.rm-year {{
    font-weight: 700; font-size: 0.82rem;
    color: {A1}; -webkit-text-fill-color: {A1};
}}
.rm-desc {{
    font-size: 0.85rem; color: #475569;
    -webkit-text-fill-color: #475569; line-height: 1.5;
    margin-top: 1px;
}}

/* ── Chips ── */
.chips {{ display:flex; flex-wrap:wrap; gap:0.4rem; margin-top:0.5rem; }}
.chip {{
    background: #fff; border: 1px solid #E2E8F0;
    border-radius: 8px; padding: 5px 12px;
    font-size: 0.8rem; font-weight: 500;
    color: #334155; -webkit-text-fill-color: #334155;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    transition: border-color 0.15s, color 0.15s;
}}
.chip:hover {{
    border-color: {A1}; color: {A1};
    -webkit-text-fill-color: {A1};
}}
.chip-hi {{
    background: {T[0][0]}; border: 1px solid {T[0][2]};
    border-radius: 8px; padding: 5px 12px;
    font-size: 0.8rem; font-weight: 600;
    color: {T[0][1]}; -webkit-text-fill-color: {T[0][1]};
}}

/* ── Scope box ── */
.scope-box {{
    background: #fff; border: 1px solid #E2E8F0;
    border-left: 4px solid {A2};
    border-radius: 12px; padding: 1.1rem 1.3rem;
    font-size: 0.88rem; color: #334155;
    -webkit-text-fill-color: #334155; line-height: 1.7;
    box-shadow: 0 1px 5px rgba(0,0,0,0.04);
}}

/* ── Divider ── */
hr {{ border-color: #E2E8F0 !important; margin: 1.4rem 0 !important; }}

/* ── Progress bar ── */
.progress-wrap {{
    background: #E2E8F0;
    border-radius: 99px;
    height: 6px;
    margin-bottom: 1.5rem;
    overflow: hidden;
}}
.progress-fill {{
    height: 100%;
    border-radius: 99px;
    background: {CARD_TOP};
    transition: width 0.4s ease;
}}
.progress-label {{
    font-size: 0.72rem; font-weight: 600;
    color: #94A3B8; -webkit-text-fill-color: #94A3B8;
    text-align: right; margin-bottom: 4px;
}}

/* ── Question number badge ── */
.q-num {{
    display: inline-block;
    background: {T[0][0]};
    color: {T[0][1]}; -webkit-text-fill-color: {T[0][1]};
    border: 1px solid {T[0][2]};
    font-size: 0.65rem; font-weight: 700;
    padding: 2px 8px; border-radius: 5px;
    margin-bottom: 4px; letter-spacing: 0.5px;
    font-family: 'Inter', sans-serif;
}}

/* ── Alert ── */
.stAlert {{ border-radius: 10px !important; }}
</style>
""", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "home"

# ══════════════════════════════════════════════════════════════════
# HOME
# ══════════════════════════════════════════════════════════════════
if st.session_state.page == "home":
    # Hero card
    st.markdown(f"""
    <div class="top-card">
        <div class="top-card-title">Find Your Perfect<br><span class="accent">Specialization</span></div>
        <div class="top-card-sub">Not sure which path to choose? Answer a few honest questions — our trained model figures it out.</div>
    </div>
    """, unsafe_allow_html=True)

    # Stat pills
    st.markdown("""
    <div class="stat-row">
        <div class="stat-pill"><div class="stat-pill-label">Accuracy</div><div class="stat-pill-val">93%</div></div>
        <div class="stat-pill"><div class="stat-pill-label">Questions</div><div class="stat-pill-val">16</div></div>
        <div class="stat-pill"><div class="stat-pill-label">Streams</div><div class="stat-pill-val">2</div></div>
        <div class="stat-pill"><div class="stat-pill-label">Careers</div><div class="stat-pill-val">10</div></div>
        <div class="stat-pill"><div class="stat-pill-label">Time</div><div class="stat-pill-val" style="white-space:nowrap">~3 min</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown('<p style="font-size:0.75rem;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:#94A3B8;margin-bottom:0.8rem">Select your field</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🖥️  BTech Student", use_container_width=True):
            st.session_state.field = "BTech"
            st.session_state.page = "quiz"
            st.rerun()
        st.markdown('<p style="text-align:center;font-size:0.73rem;color:#94A3B8;margin-top:5px">CS · IT · Engineering</p>', unsafe_allow_html=True)
    with col2:
        if st.button("📊  BCom / BBA Student", use_container_width=True):
            st.session_state.field = "BCom"
            st.session_state.page = "quiz"
            st.rerun()
        st.markdown('<p style="text-align:center;font-size:0.73rem;color:#94A3B8;margin-top:5px">Commerce · Business · Management</p>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# QUIZ
# ══════════════════════════════════════════════════════════════════
elif st.session_state.page == "quiz":
    field    = st.session_state.field
    is_btech = field == "BTech"

    st.markdown(f"""
    <div class="top-card">
        <div class="top-card-label">{"🖥️ BTech Track" if is_btech else "📊 BCom / BBA Track"}</div>
        <div class="top-card-title">{"Discover Your <span class='accent'>Tech Path</span>" if is_btech else "Discover Your <span class='accent'>Business Path</span>"}</div>
        <div class="top-card-sub">Answer honestly — no right or wrong answers here.</div>
    </div>
    """, unsafe_allow_html=True)

    # Progress bar
    answered = sum([1 for q in [st.session_state.get(f"q{i}") for i in range(2,18)] if q is not None])
    pct = int((answered / 16) * 100)
    st.markdown(f"""
    <div class="progress-label">{answered} / 16 answered</div>
    <div class="progress-wrap"><div class="progress-fill" style="width:{pct}%"></div></div>
    """, unsafe_allow_html=True)

    # Common
    st.markdown('<span class="stag stag-a">● &nbsp;Section 1 — About You</span>', unsafe_allow_html=True)
    st.markdown('<div class="q-num">Q 1</div>', unsafe_allow_html=True)
    q2 = st.radio("How confident are you about your future career path?",
        ["Not confident at all","Somewhat confident","Very confident"], index=None, key="q2")
    st.markdown('<div class="q-num">Q 2</div>', unsafe_allow_html=True)
    q3 = st.radio("You just joined a new college club. You naturally gravitate towards —",
        ["A. The technical side — building, fixing, setting things up",
         "B. The creative side — designing, content, visuals",
         "C. The management side — organizing people and events",
         "D. The research side — planning, strategizing, deep diving into topics"],
        index=None, key="q3")
    st.markdown('<div class="q-num">Q 3</div>', unsafe_allow_html=True)
    q4 = st.radio("When you have a big decision to make, you —",
        ["A. Think it through logically step by step",
         "B. Go with what feels right instinctively",
         "C. Ask everyone around you for opinions",
         "D. Research every option thoroughly before deciding"],
        index=None, key="q4")
    st.divider()

    if is_btech:
        st.markdown('<span class="stag stag-b">● &nbsp;Section 2 — Your Reactions</span>', unsafe_allow_html=True)
        st.markdown('<div class="q-num">Q 4</div>', unsafe_allow_html=True)
        q5 = st.radio("You sit down and try coding for the very first time. After 30 minutes you feel —",
            ["A. This is actually interesting, I want to keep going",
             "B. It's okay but nothing is exciting me yet",
             "C. I'd rather be doing something else honestly"], index=None, key="q5")
        st.markdown('<div class="q-num">Q 5</div>', unsafe_allow_html=True)
        q6 = st.radio("Someone shows you a really clean and beautiful app design. You —",
            ["A. Appreciate it but wonder how it was technically built",
             "B. Instantly start noticing every design detail and feel inspired",
             "C. Think it looks nice but design stuff doesn't really pull me in"], index=None, key="q6")
        st.markdown('<div class="q-num">Q 6</div>', unsafe_allow_html=True)
        q7 = st.radio("Your friend explains how a hacker broke into a big company's system. You —",
            ["A. Find this genuinely fascinating and want to know more",
             "B. Think it's interesting but not something I'd want to pursue",
             "C. Feel a bit uncomfortable and uninterested honestly"], index=None, key="q7")
        st.markdown('<div class="q-num">Q 7</div>', unsafe_allow_html=True)
        q8 = st.radio("You watch a video about how Spotify knows your mood from your listening data. You —",
            ["A. Find data and pattern stuff like this genuinely exciting",
             "B. Think it's cool but wouldn't want to work on something like this",
             "C. Feel a bit bored watching this kind of content"], index=None, key="q8")
        st.markdown('<div class="q-num">Q 8</div>', unsafe_allow_html=True)
        q9 = st.radio("You find out every app you use runs on massive servers managed by engineers. You —",
            ["A. Find this genuinely fascinating — I'd love to work on something like that",
             "B. Interesting fact but doesn't excite me career wise",
             "C. Never really thought about it and don't find it that interesting"], index=None, key="q9")
        st.divider()
        st.markdown('<span class="stag stag-c">● &nbsp;Section 3 — Forced Choices</span>', unsafe_allow_html=True)
        st.markdown('<div class="q-num">Q 9</div>', unsafe_allow_html=True)
        q10 = st.radio("Full day — coding a working app OR designing a beautiful interface —",
            ["A. Coding the working app","B. Designing the beautiful interface"], index=None, key="q10")
        st.markdown('<div class="q-num">Q 10</div>', unsafe_allow_html=True)
        q11 = st.radio("Choose — how to hack ethically OR how to build a website —",
            ["A. How to hack ethically","B. How to build a website"], index=None, key="q11")
        st.markdown('<div class="q-num">Q 11</div>', unsafe_allow_html=True)
        q12 = st.radio("Pick — building something millions use OR securing systems —",
            ["A. Building something people use","B. Securing systems from attacks"], index=None, key="q12")
        st.markdown('<div class="q-num">Q 12</div>', unsafe_allow_html=True)
        q13 = st.radio("Choose — understand data and find patterns OR design anything beautifully —",
            ["A. Understand data and find patterns","B. Design anything beautifully"], index=None, key="q13")
        st.markdown('<div class="q-num">Q 13</div>', unsafe_allow_html=True)
        q14 = st.radio("Full day — building a new app feature OR making sure it never crashes —",
            ["A. Building the new feature","B. Making sure it never crashes for everyone"], index=None, key="q14")
        st.divider()
        st.markdown('<span class="stag stag-a">● &nbsp;Section 4 — Self Assessment</span>', unsafe_allow_html=True)
        st.markdown('<div class="q-num">Q 14</div>', unsafe_allow_html=True)
        q15 = st.radio("Maths and logical thinking — be honest —",
            ["1 — I avoid it as much as possible",
             "2 — I can manage it when needed",
             "3 — I genuinely enjoy it"], index=None, key="q15")
        st.markdown('<div class="q-num">Q 15</div>', unsafe_allow_html=True)
        q16 = st.radio("Creative and visual stuff — design, colors, how things look and feel —",
            ["1 — Doesn't interest me much",
             "2 — I appreciate it but it's not my thing",
             "3 — This is genuinely my thing"], index=None, key="q16")
    else:
        st.markdown('<span class="stag stag-b">● &nbsp;Section 2 — Your Interests</span>', unsafe_allow_html=True)
        st.markdown('<div class="q-num">Q 4</div>', unsafe_allow_html=True)
        q5  = st.radio("I enjoy keeping track of money, budgets, or expenses in daily life —",
            ["1 — Not really","2 — Somewhat","3 — Yes definitely"], index=None, key="q5")
        st.markdown('<div class="q-num">Q 5</div>', unsafe_allow_html=True)
        q6  = st.radio("I enjoy convincing people, selling ideas, or promoting things —",
            ["1 — Not really","2 — Somewhat","3 — Yes definitely"], index=None, key="q6")
        st.markdown('<div class="q-num">Q 6</div>', unsafe_allow_html=True)
        q7  = st.radio("I often think about starting my own business or venture someday —",
            ["1 — Not really","2 — Somewhat","3 — Yes definitely"], index=None, key="q7")
        st.markdown('<div class="q-num">Q 7</div>', unsafe_allow_html=True)
        q8  = st.radio("I enjoy organizing teams, managing people, making sure everyone works well —",
            ["1 — Not really","2 — Somewhat","3 — Yes definitely"], index=None, key="q8")
        st.markdown('<div class="q-num">Q 8</div>', unsafe_allow_html=True)
        q9  = st.radio("I enjoy analyzing data or reports to understand what is working and what is not —",
            ["1 — Not really","2 — Somewhat","3 — Yes definitely"], index=None, key="q9")
        st.markdown('<div class="q-num">Q 9</div>', unsafe_allow_html=True)
        q10 = st.radio("I am interested in how stock markets, investments, or banking systems work —",
            ["1 — Not really","2 — Somewhat","3 — Yes definitely"], index=None, key="q10")
        st.markdown('<div class="q-num">Q 10</div>', unsafe_allow_html=True)
        q11 = st.radio("I enjoy creative work like making campaigns, content, or building a brand image —",
            ["1 — Not really","2 — Somewhat","3 — Yes definitely"], index=None, key="q11")
        st.markdown('<div class="q-num">Q 11</div>', unsafe_allow_html=True)
        q12 = st.radio("I prefer taking decisions based on data and facts rather than gut feeling —",
            ["1 — Not really","2 — Somewhat","3 — Yes definitely"], index=None, key="q12")
        st.divider()
        st.markdown('<span class="stag stag-c">● &nbsp;Section 3 — Forced Choices</span>', unsafe_allow_html=True)
        st.markdown('<div class="q-num">Q 12</div>', unsafe_allow_html=True)
        q13 = st.radio("Your friend shows you their profit and loss sheet from their online business. You —",
            ["A. Find this exciting — numbers and business performance interest me",
             "B. Immediately think about how they could market it better",
             "C. Start thinking about how you'd run the whole operation differently",
             "D. Feel a bit lost — this kind of stuff doesn't excite me much"],
            index=None, key="q13")
        st.markdown('<div class="q-num">Q 13</div>', unsafe_allow_html=True)
        q14 = st.radio("Full day — managing a team OR analyzing business data —",
            ["A. Managing the team","B. Analyzing the data"], index=None, key="q14")
        st.markdown('<div class="q-num">Q 14</div>', unsafe_allow_html=True)
        q15 = st.radio("Choose — build your own startup OR work up to CFO —",
            ["A. Build my own startup","B. Work up to CFO"], index=None, key="q15")
        st.markdown('<div class="q-num">Q 15</div>', unsafe_allow_html=True)
        q16 = st.radio("Weekend — viral marketing campaign OR financial statements —",
            ["A. Viral marketing campaign","B. Financial statements"], index=None, key="q16")

    st.divider()
    if st.button("🎯  Predict My Specialization", use_container_width=True):
        all_answered = all([q2,q3,q4,q5,q6,q7,q8,q9,q10,q11,q12,q13,q14,q15,q16])
        if not all_answered:
            st.warning("⚠️ Please answer all questions before predicting!")
        else:
            if field == "BTech":
                st.session_state.answers = {
                    "Q2_Confidence":      CONF_MAP[q2],
                    "Q3_ClubChoice":      CAT_MAP[q3[0]],
                    "Q4_DecisionStyle":   CAT_MAP[q4[0]],
                    "Q5_CodingReaction":  CAT_MAP[q5[0]],
                    "Q6_DesignReaction":  CAT_MAP[q6[0]],
                    "Q7_HackingReaction": CAT_MAP[q7[0]],
                    "Q8_DataReaction":    CAT_MAP[q8[0]],
                    "Q9_CloudReaction":   CAT_MAP[q9[0]],
                    "Q10_CodeVsDesign":   CAT_MAP[q10[0]],
                    "Q11_HackVsBuild":    CAT_MAP[q11[0]],
                    "Q12_BuildVsSecure":  CAT_MAP[q12[0]],
                    "Q13_DataVsDesign":   CAT_MAP[q13[0]],
                    "Q14_FeatureVsScale": CAT_MAP[q14[0]],
                    "Q15_MathsRating":    int(q15[0]),
                    "Q16_CreativeRating": int(q16[0]),
                }
            else:
                st.session_state.answers = {
                    "Q2_Confidence":         CONF_MAP[q2],
                    "Q3_ClubChoice":         CAT_MAP[q3[0]],
                    "Q4_DecisionStyle":      CAT_MAP[q4[0]],
                    "Q5_MoneyBudgets":       int(q5[0]),
                    "Q6_ConvincingSelling":  int(q6[0]),
                    "Q7_OwnBusiness":        int(q7[0]),
                    "Q8_ManagingTeams":      int(q8[0]),
                    "Q9_AnalyzingData":      int(q9[0]),
                    "Q10_StockMarkets":      int(q10[0]),
                    "Q11_CampaignsBranding": int(q11[0]),
                    "Q12_DataOverGut":       int(q12[0]),
                    "Q13_BusinessReaction":  CAT_MAP[q13[0]],
                    "Q14_ManageVsAnalyze":   CAT_MAP[q14[0]],
                    "Q15_StartupVsCFO":      CAT_MAP[q15[0]],
                    "Q16_MarketingVsFinance":CAT_MAP[q16[0]],
                }
            st.session_state.page = "result"
            st.rerun()

# ══════════════════════════════════════════════════════════════════
# RESULT
# ══════════════════════════════════════════════════════════════════
elif st.session_state.page == "result":
    answers = st.session_state.answers
    field   = st.session_state.field
    if field == "BTech":
        specialization, confidence = predict_btech(answers)
    else:
        specialization, confidence = predict_bcom(answers)
    st.session_state.specialization = specialization
    data = ROADMAPS[specialization]

    st.markdown(f"""
    <div class="result-card">
        <div class="result-emoji">{data['emoji']}</div>
        <div class="result-name">{specialization}</div>
        <div class="result-sub">Best matched specialization based on your answers</div>
        <div class="conf-pill">✓ &nbsp;{confidence:.1f}% Confidence</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📍  View My Roadmap", use_container_width=True):
            st.session_state.page = "roadmap"
            st.rerun()
    with col2:
        if st.button("🔄  Retake Quiz", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()

# ══════════════════════════════════════════════════════════════════
# ROADMAP
# ══════════════════════════════════════════════════════════════════
elif st.session_state.page == "roadmap":
    spec  = st.session_state.specialization
    data  = ROADMAPS[spec]

    st.markdown(f"""
    <div class="top-card">
        <div class="top-card-label">Your Personalised Roadmap</div>
        <div class="top-card-title">{data['emoji']} <span class="accent">{spec}</span></div>
        <div class="top-card-sub">{data['about']}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🗺️ Year-by-Year Roadmap")
    st.markdown('<div class="rm-wrap">', unsafe_allow_html=True)
    for i, step in enumerate(data["roadmap"], 1):
        year, desc = step.split(" — ", 1)
        st.markdown(f"""
        <div class="rm-step">
            <div class="rm-num">{i}</div>
            <div>
                <div class="rm-year">{year}</div>
                <div class="rm-desc">{desc}</div>
            </div>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()
    st.markdown("### 💼 Career Options")
    careers_html = "".join([f'<span class="chip-hi">{c}</span>' for c in data["careers"]])
    st.markdown(f'<div class="chips">{careers_html}</div>', unsafe_allow_html=True)

    st.divider()
    st.markdown("### 🏢 Top Companies Hiring")
    companies_html = "".join([f'<span class="chip">{c}</span>' for c in data["companies"]])
    st.markdown(f'<div class="chips">{companies_html}</div>', unsafe_allow_html=True)

    st.divider()
    st.markdown("### 🔭 Future Scope")
    st.markdown(f'<div class="scope-box">{data["scope"]}</div>', unsafe_allow_html=True)

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄  Retake Quiz", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()
    with col2:
        if st.button("⬅️  Back to Result", use_container_width=True):
            st.session_state.page = "result"
            st.rerun()
