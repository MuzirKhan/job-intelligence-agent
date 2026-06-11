import streamlit as st
import json
import os
import time
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Job Intelligence Agent",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
* { font-family: 'Inter', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem; max-width: 1100px; }
.stApp { background: #0A0A0F; }

.hero-badge {
    display: inline-block;
    background: linear-gradient(135deg, rgba(139,92,246,0.15), rgba(59,130,246,0.15));
    border: 1px solid rgba(139,92,246,0.3);
    color: #A78BFA; padding: 6px 16px; border-radius: 100px;
    font-size: 12px; font-weight: 500; letter-spacing: 0.08em;
    text-transform: uppercase; margin-bottom: 1rem;
}
.hero-title {
    font-size: 3rem; font-weight: 700;
    background: linear-gradient(135deg, #FFFFFF 0%, #A78BFA 50%, #60A5FA 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    line-height: 1.15; margin: 0.5rem 0;
}
.hero-sub { font-size: 1rem; color: #6B7280; line-height: 1.7; max-width: 580px; margin-bottom: 1.5rem; }

.step-card {
    background: linear-gradient(135deg, rgba(139,92,246,0.06), rgba(59,130,246,0.06));
    border: 1px solid rgba(139,92,246,0.2); border-radius: 16px; padding: 2rem; margin-bottom: 1.5rem;
}
.step-num {
    width: 28px; height: 28px; border-radius: 50%;
    background: linear-gradient(135deg, #7C3AED, #3B82F6);
    color: white; font-size: 13px; font-weight: 700;
    display: inline-flex; align-items: center; justify-content: center; margin-bottom: 12px;
}
.step-heading { font-size: 1.1rem; font-weight: 600; color: #F9FAFB; margin-bottom: 4px; }
.step-sub { font-size: 0.82rem; color: #6B7280; margin-bottom: 1.2rem; }

.profile-preview {
    background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px; padding: 1.25rem 1.5rem; margin-top: 1rem;
}
.profile-name { font-size: 1.1rem; font-weight: 600; color: #F9FAFB; margin-bottom: 2px; }
.profile-meta { font-size: 0.82rem; color: #8B5CF6; margin-bottom: 12px; }

.chip-green { display:inline-block; background:rgba(16,185,129,0.1); color:#10B981; border:1px solid rgba(16,185,129,0.25); padding:3px 10px; border-radius:100px; font-size:11px; margin:2px; }
.chip-red   { display:inline-block; background:rgba(239,68,68,0.1);  color:#F87171; border:1px solid rgba(239,68,68,0.25);  padding:3px 10px; border-radius:100px; font-size:11px; margin:2px; }
.chip-amber { display:inline-block; background:rgba(245,158,11,0.1); color:#FCD34D; border:1px solid rgba(245,158,11,0.25); padding:3px 10px; border-radius:100px; font-size:11px; margin:2px; }
.chip-blue  { display:inline-block; background:rgba(59,130,246,0.1); color:#93C5FD; border:1px solid rgba(59,130,246,0.25); padding:3px 10px; border-radius:100px; font-size:11px; margin:2px; }
.chip-purple{ display:inline-block; background:rgba(139,92,246,0.1); color:#C4B5FD; border:1px solid rgba(139,92,246,0.25); padding:3px 10px; border-radius:100px; font-size:11px; margin:2px; }

.section-header { display:flex; align-items:center; gap:10px; margin:2rem 0 1rem; }
.section-dot { width:8px; height:8px; border-radius:50%; background:linear-gradient(135deg,#8B5CF6,#3B82F6); flex-shrink:0; }
.section-title { font-size:0.7rem; font-weight:600; color:#6B7280; text-transform:uppercase; letter-spacing:0.1em; }

.job-header {
    background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px; padding: 1.25rem 1.5rem; margin-bottom: 1.25rem;
    display: flex; justify-content: space-between; align-items: flex-start;
}
.job-title { font-size: 1rem; font-weight: 600; color: #F9FAFB; margin-bottom: 3px; }
.job-company { font-size: 0.85rem; color: #8B5CF6; font-weight: 500; }
.job-location { font-size: 0.78rem; color: #6B7280; margin-top: 3px; }
.score-high { background:rgba(16,185,129,0.15); color:#10B981; border:1px solid rgba(16,185,129,0.3); padding:4px 14px; border-radius:100px; font-size:13px; font-weight:700; }
.score-mid  { background:rgba(245,158,11,0.15); color:#F59E0B; border:1px solid rgba(245,158,11,0.3); padding:4px 14px; border-radius:100px; font-size:13px; font-weight:700; }
.score-low  { background:rgba(239,68,68,0.15);  color:#EF4444; border:1px solid rgba(239,68,68,0.3);  padding:4px 14px; border-radius:100px; font-size:13px; font-weight:700; }

.gap-section { background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.05); border-radius:12px; padding:1.25rem; margin-bottom:1rem; }
.gap-label { font-size:0.72rem; color:#6B7280; text-transform:uppercase; letter-spacing:0.07em; margin-bottom:8px; font-weight:500; }

.q-card {
    background: rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.06);
    border-left: 3px solid #8B5CF6; border-radius: 0 10px 10px 0;
    padding: 1rem 1.25rem; margin-bottom: 0.75rem;
}
.q-text { font-size:0.88rem; color:#E5E7EB; font-weight:500; margin-bottom:6px; }
.q-hint { font-size:0.78rem; color:#6B7280; line-height:1.6; }

.tmay-card {
    background: linear-gradient(135deg, rgba(139,92,246,0.08), rgba(59,130,246,0.06));
    border: 1px solid rgba(139,92,246,0.2); border-radius: 16px;
    padding: 1.75rem; margin-bottom: 1.25rem;
}
.tmay-tag { font-size:0.72rem; color:#8B5CF6; font-weight:600; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:10px; }
.tmay-quote { font-size:2.5rem; color:rgba(139,92,246,0.25); line-height:1; margin-bottom:6px; }
.tmay-text { font-size:0.88rem; color:#D1D5DB; line-height:1.9; white-space:pre-wrap; }

.pipeline-step { display:flex; align-items:center; gap:12px; padding:9px 0; }
.ps-icon { width:34px; height:34px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:15px; flex-shrink:0; }
.ps-done   { background:rgba(16,185,129,0.15); color:#10B981; }
.ps-active { background:rgba(139,92,246,0.2); color:#A78BFA; }
.ps-wait   { background:rgba(255,255,255,0.04); color:#374151; }
.ps-label  { font-size:0.85rem; color:#9CA3AF; }
.ps-label-active { color:#E5E7EB; font-weight:500; }

.metric-box { background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.07); border-radius:12px; padding:1.1rem 1.25rem; text-align:center; }
.metric-val { font-size:1.9rem; font-weight:700; color:#F9FAFB; }
.metric-label { font-size:0.72rem; color:#6B7280; text-transform:uppercase; letter-spacing:0.06em; margin-top:4px; }

.divider { height:1px; background:rgba(255,255,255,0.06); margin:2rem 0; }

.stButton > button {
    background: linear-gradient(135deg, #7C3AED, #3B82F6) !important;
    color: white !important; border: none !important; border-radius: 10px !important;
    padding: 0.65rem 2rem !important; font-weight: 600 !important;
    font-size: 0.9rem !important; letter-spacing: 0.02em !important;
    transition: opacity 0.2s !important; cursor: pointer !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

.stTextInput > div > div > input, .stTextArea > div > div > textarea {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 8px !important; color: #F9FAFB !important; padding: 0.6rem 1rem !important;
}
.stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
    border-color: rgba(139,92,246,0.5) !important;
    box-shadow: 0 0 0 2px rgba(139,92,246,0.1) !important;
}
.stTextInput label, .stTextArea label, .stSelectbox label { color: #9CA3AF !important; font-size: 0.8rem !important; font-weight: 500 !important; }
.stSelectbox > div > div { background: rgba(255,255,255,0.05) !important; border: 1px solid rgba(255,255,255,0.1) !important; border-radius: 8px !important; color: #F9FAFB !important; }

.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.03) !important; border-radius: 10px !important;
    padding: 4px !important; gap: 4px !important; border: 1px solid rgba(255,255,255,0.06) !important;
}
.stTabs [data-baseweb="tab"] { color: #6B7280 !important; border-radius: 8px !important; padding: 8px 16px !important; font-size: 0.85rem !important; }
.stTabs [aria-selected="true"] { background: rgba(139,92,246,0.2) !important; color: #A78BFA !important; }

.stNumberInput > div > div > input {
    background: rgba(255,255,255,0.05) !important; border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 8px !important; color: #F9FAFB !important;
}

@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.4} }
.ps-active { animation: pulse 1.5s infinite; }
</style>
""", unsafe_allow_html=True)


# ─── helpers ───
def chips(items, cls):
    if not items: return '<span style="color:#374151;font-size:11px">None listed</span>'
    return " ".join([f'<span class="{cls}">{i}</span>' for i in items])

def section(icon, label):
    st.markdown(f'<div class="section-header"><div class="section-dot"></div><span class="section-title">{icon}&nbsp;&nbsp;{label}</span></div>', unsafe_allow_html=True)

def score_cls(s):
    return "score-high" if s >= 65 else ("score-mid" if s >= 40 else "score-low")


# ─── session state init ───
for key in ["profile", "step", "results"]:
    if key not in st.session_state:
        st.session_state[key] = None
if "step" not in st.session_state or st.session_state.step is None:
    st.session_state.step = "profile"


# ─── HERO ───
st.markdown('<div class="hero-badge">✦ Multi-Agent AI · Powered by Mistral</div>', unsafe_allow_html=True)
st.markdown('<h1 class="hero-title">Job Intelligence Agent</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-sub">Get personalized job gap analysis, interview questions, and a tailored "Tell Me About Yourself" — for any role, any location.</p>', unsafe_allow_html=True)
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# STEP 1 — PROFILE BUILDER
# ══════════════════════════════════════════════
if st.session_state.step == "profile":

    st.markdown('<div class="step-card">', unsafe_allow_html=True)
    st.markdown('<div class="step-num">1</div>', unsafe_allow_html=True)
    st.markdown('<div class="step-heading">Tell us about yourself</div>', unsafe_allow_html=True)
    st.markdown('<div class="step-sub">Fill in your details below — our AI will structure your profile automatically.</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        name = st.text_input("Full Name *", placeholder="e.g. Alex Johnson")
        education = st.text_input("Education *", placeholder="e.g. B.Tech Computer Science, MCA")
        current_role = st.text_input("Current / Target Role *", placeholder="e.g. Data Engineer, Software Developer")
    with c2:
        experience = st.number_input("Years of Experience *", min_value=0, max_value=30, value=1, step=1)
        certifications = st.text_input("Certifications (optional)", placeholder="e.g. AWS Solutions Architect, AZ-900")
        location_home = st.text_input("Your Location (optional)", placeholder="e.g. Bangalore, India")

    strong_skills = st.text_input(
        "Strong Skills * (comma separated)",
        placeholder="e.g. Python, SQL, PySpark, Azure Data Factory, Databricks"
    )
    moderate_skills = st.text_input(
        "Moderate Skills (comma separated)",
        placeholder="e.g. dbt, Airflow, Power BI"
    )
    learning_skills = st.text_input(
        "Currently Learning (comma separated)",
        placeholder="e.g. LangChain, GenAI, Kafka, Terraform"
    )

    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Build My Profile →"):
        if not name.strip() or not strong_skills.strip() or not education.strip() or not current_role.strip():
            st.warning("Please fill in Name, Education, Current Role, and Strong Skills at minimum.")
        else:
            with st.spinner("Structuring your profile with AI..."):
                from langchain_mistralai import ChatMistralAI
                from langchain_core.output_parsers import JsonOutputParser
                from langchain_core.prompts import ChatPromptTemplate

                raw_input = f"""
Name: {name}
Education: {education}
Current/Target Role: {current_role}
Years of Experience: {experience}
Strong Skills: {strong_skills}
Moderate Skills: {moderate_skills}
Currently Learning: {learning_skills}
Certifications: {certifications}
Location: {location_home}
"""
                llm = ChatMistralAI(model="mistral-small-2506",
                    api_key=st.secrets.get("MISTRAL_API_KEY"))
                prompt = ChatPromptTemplate.from_messages([
                    ("system", """You are a professional profile extractor.
Extract the information and return ONLY a valid JSON object with these exact keys:
name, education, current_role, experience_years, location,
strong_skills, moderate_skills, learning_skills, certifications.
strong_skills, moderate_skills, learning_skills, certifications must be arrays.
No markdown, no extra text, just the JSON."""),
                    ("human", "{query}")
                ])
                chain = prompt | llm | JsonOutputParser()
                profile = chain.invoke({"query": raw_input})
                st.session_state.profile = profile
                st.session_state.step = "profile_confirm"
                st.rerun()


# ══════════════════════════════════════════════
# STEP 1b — PROFILE CONFIRM
# ══════════════════════════════════════════════
elif st.session_state.step == "profile_confirm":
    p = st.session_state.profile

    st.markdown('<div class="step-card">', unsafe_allow_html=True)
    st.markdown('<div class="step-num">1</div>', unsafe_allow_html=True)
    st.markdown('<div class="step-heading">Your Profile</div>', unsafe_allow_html=True)
    st.markdown('<div class="step-sub">Confirm your details look right before we start the analysis.</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="profile-preview">
        <div class="profile-name">{p.get('name','—')}</div>
        <div class="profile-meta">{p.get('current_role','—')} · {p.get('experience_years','?')} yrs · {p.get('education','—')}</div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<p style="color:#9CA3AF;font-size:0.72rem;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:6px">Strong Skills</p>', unsafe_allow_html=True)
        st.markdown(chips(p.get("strong_skills", []), "chip-green"), unsafe_allow_html=True)
    with col2:
        st.markdown('<p style="color:#9CA3AF;font-size:0.72rem;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:6px">Moderate Skills</p>', unsafe_allow_html=True)
        st.markdown(chips(p.get("moderate_skills", []), "chip-amber"), unsafe_allow_html=True)
    with col3:
        st.markdown('<p style="color:#9CA3AF;font-size:0.72rem;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:6px">Currently Learning</p>', unsafe_allow_html=True)
        st.markdown(chips(p.get("learning_skills", []), "chip-blue"), unsafe_allow_html=True)

    if p.get("certifications"):
        st.markdown('<p style="color:#9CA3AF;font-size:0.72rem;text-transform:uppercase;letter-spacing:0.06em;margin:12px 0 6px">Certifications</p>', unsafe_allow_html=True)
        st.markdown(chips(p.get("certifications", []), "chip-purple"), unsafe_allow_html=True)

    st.markdown('</div></div>', unsafe_allow_html=True)

    bc1, bc2 = st.columns([1, 4])
    with bc1:
        if st.button("← Edit Profile"):
            st.session_state.step = "profile"
            st.rerun()
    with bc2:
        if st.button("Looks Good — Find Jobs →"):
            st.session_state.step = "search"
            st.rerun()


# ══════════════════════════════════════════════
# STEP 2 — JOB SEARCH
# ══════════════════════════════════════════════
elif st.session_state.step == "search":
    p = st.session_state.profile

    # mini profile bar
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:12px;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);border-radius:10px;padding:10px 16px;margin-bottom:1.5rem">
        <span style="font-size:1.2rem">👤</span>
        <div>
            <span style="color:#F9FAFB;font-size:0.9rem;font-weight:600">{p.get('name','—')}</span>
            <span style="color:#6B7280;font-size:0.8rem;margin-left:8px">{p.get('current_role','—')} · {p.get('experience_years','?')} yrs</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="step-card">', unsafe_allow_html=True)
    st.markdown('<div class="step-num">2</div>', unsafe_allow_html=True)
    st.markdown('<div class="step-heading">Search Jobs</div>', unsafe_allow_html=True)
    st.markdown('<div class="step-sub">Enter the role and location you want to analyze. We will scrape 2 live jobs from LinkedIn.</div>', unsafe_allow_html=True)

    s1, s2 = st.columns(2)
    with s1:
        role = st.text_input("Job Role *", placeholder="e.g. Data Engineer, ML Engineer, Backend Developer")
    with s2:
        location = st.text_input("Location *", placeholder="e.g. India, USA, Germany")

    st.markdown('</div>', unsafe_allow_html=True)

    bc1, bc2 = st.columns([1, 4])
    with bc1:
        if st.button("← Edit Profile"):
            st.session_state.step = "profile_confirm"
            st.rerun()
    with bc2:
        if st.button("Run Full Analysis →"):
            if not role.strip() or not location.strip():
                st.warning("Please enter both a job role and location.")
            else:
                st.session_state.search_role = role
                st.session_state.search_location = location
                st.session_state.step = "running"
                st.rerun()


# ══════════════════════════════════════════════
# STEP 3 — PIPELINE RUNNING
# ══════════════════════════════════════════════
elif st.session_state.step == "running":
    p = st.session_state.profile
    role = st.session_state.search_role
    location = st.session_state.search_location

    section("⚡", "Running Multi-Agent Pipeline")
    steps_meta = [
        ("🔎", "Scraping LinkedIn for live jobs"),
        ("🧠", "Extracting required skills from JDs"),
        ("📊", "Analyzing your skill gaps"),
        ("💬", "Generating interview questions"),
        ("🎤", "Crafting your Tell Me About Yourself"),
    ]

    progress_ph = st.empty()

    def render_steps(current):
        html = ""
        for i, (icon, label) in enumerate(steps_meta):
            if i < current:
                ic, lc = "ps-icon ps-done", "ps-label"
                ic_val = "✓"
            elif i == current:
                ic, lc = "ps-icon ps-active", "ps-label ps-label-active"
                ic_val = icon
            else:
                ic, lc = "ps-icon ps-wait", "ps-label"
                ic_val = icon
            html += f'<div class="pipeline-step"><div class="{ic}">{ic_val}</div><span class="{lc}">{label}</span></div>'
        progress_ph.markdown(html, unsafe_allow_html=True)

    try:
        from tools import scrape_jobs, extract_skills, analyze_gap, prep_questions, generate_tmay
        
        os.makedirs("data", exist_ok=True)
        with open("data/profile.json", "w") as f:
            json.dump(p, f, indent=4)

        render_steps(0)
        raw_json = scrape_jobs.invoke({"role": role, "location": location})
        raw_jobs = json.loads(raw_json)[:2]
        raw_json = json.dumps(raw_jobs)

        render_steps(1)
        extracted_json = extract_skills.invoke({"jobs_json": raw_json})

        render_steps(2)
        # Pass user's session profile, not file
        profile_json = json.dumps(p)
        gap_json = analyze_gap.invoke({
        "extracted_jobs_json": extracted_json,
        "profile_json": json.dumps(p)
        })
        gap_data = json.loads(gap_json)

        render_steps(3)
        prep_json = prep_questions.invoke({"gap_json": gap_json})
        prep_data = json.loads(prep_json)

        render_steps(4)
        tmay_json = generate_tmay.invoke({"gap_json": gap_json})
        tmay_data = json.loads(tmay_json)

        render_steps(5)
        time.sleep(0.4)
        progress_ph.empty()

        st.session_state.results = {
            "raw_jobs": raw_jobs,
            "gap_data": gap_data,
            "prep_data": prep_data,
            "tmay_data": tmay_data,
        }
        st.session_state.step = "results"
        st.rerun()

    except Exception as e:
        progress_ph.empty()
        st.error(f"Pipeline error: {str(e)}")
        st.exception(e)
        if st.button("← Try Again"):
            st.session_state.step = "search"
            st.rerun()


# ══════════════════════════════════════════════
# STEP 4 — RESULTS
# ══════════════════════════════════════════════
elif st.session_state.step == "results":
    p = st.session_state.profile
    r = st.session_state.results
    gap_data  = r["gap_data"]
    prep_data = r["prep_data"]
    tmay_data = r["tmay_data"]
    raw_jobs  = r["raw_jobs"]

    # top bar
    st.markdown(f"""
    <div style="display:flex;align-items:center;justify-content:space-between;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);border-radius:10px;padding:10px 16px;margin-bottom:1.5rem">
        <div>
            <span style="color:#F9FAFB;font-size:0.9rem;font-weight:600">{p.get('name','—')}</span>
            <span style="color:#6B7280;font-size:0.8rem;margin-left:8px">{p.get('current_role','—')} · {p.get('experience_years','?')} yrs</span>
        </div>
        <span style="color:#8B5CF6;font-size:0.8rem">🔍 {st.session_state.search_role} · {st.session_state.search_location}</span>
    </div>
    """, unsafe_allow_html=True)

    # summary metrics
    section("📈", "Analysis Summary")
    total = len(gap_data)
    avg_score = int(sum(j.get("match_score", 0) for j in gap_data) / total) if total else 0
    best = max(gap_data, key=lambda x: x.get("match_score", 0)) if gap_data else {}

    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f'<div class="metric-box"><div class="metric-val">{total}</div><div class="metric-label">Jobs Analyzed</div></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="metric-box"><div class="metric-val">{avg_score}%</div><div class="metric-label">Avg Match Score</div></div>', unsafe_allow_html=True)
    with m3:
        best_name = best.get("company", "—")
        st.markdown(f'<div class="metric-box"><div class="metric-val" style="font-size:1rem;padding:8px 0">{best_name}</div><div class="metric-label">Best Match</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # per-job tabs
    tab_labels = [f"{j.get('company','Job')}  ·  {j.get('match_score',0)}%" for j in gap_data]
    tabs = st.tabs(tab_labels) if tab_labels else []

    for idx, tab in enumerate(tabs):
        with tab:
            gap  = gap_data[idx]  if idx < len(gap_data)  else {}
            prep = prep_data[idx] if idx < len(prep_data) else {}
            tmay = tmay_data[idx] if idx < len(tmay_data) else {}
            raw  = raw_jobs[idx]  if idx < len(raw_jobs)  else {}

            score = gap.get("match_score", 0)
            st.markdown(f"""
            <div class="job-header">
                <div>
                    <div class="job-title">{gap.get('title', raw.get('title','—'))}</div>
                    <div class="job-company">{gap.get('company', raw.get('company','—'))}</div>
                    <div class="job-location">📍 {raw.get('location','—')}</div>
                </div>
                <span class="{score_cls(score)}">{score}% Match</span>
            </div>
            """, unsafe_allow_html=True)

            # gap analysis
            section("🔬", "Skill Gap Analysis")
            g1, g2 = st.columns(2)
            with g1:
                st.markdown('<div class="gap-section"><div class="gap-label">✅ You Already Have</div>', unsafe_allow_html=True)
                st.markdown(chips(gap.get("matching_skills", []), "chip-green"), unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

                st.markdown('<div class="gap-section"><div class="gap-label">⚡ Quick to Learn (1–2 weeks)</div>', unsafe_allow_html=True)
                st.markdown(chips(gap.get("quick_learnable", []), "chip-amber"), unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            with g2:
                st.markdown('<div class="gap-section"><div class="gap-label">❌ Missing Skills</div>', unsafe_allow_html=True)
                st.markdown(chips(gap.get("gaps", []), "chip-red"), unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

                st.markdown('<div class="gap-section"><div class="gap-label">📅 Long Term Investment</div>', unsafe_allow_html=True)
                st.markdown(chips(gap.get("long_term", []), "chip-blue"), unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

            # interview prep
            section("💬", "Interview Prep Questions")
            questions = prep.get("questions", [])
            for i, q in enumerate(questions):
                st.markdown(f"""
                <div class="q-card">
                    <div class="q-text">Q{i+1}. {q.get('question','')}</div>
                    <div class="q-hint">💡 {q.get('hint','')}</div>
                </div>""", unsafe_allow_html=True)

            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

            # TMAY
            section("🎤", "Your 90-Second Pitch")
            tmay_text = tmay.get("tmay", "")
            company = gap.get("company", "this role")
            if tmay_text:
                st.markdown(f"""
                <div class="tmay-card">
                    <div class="tmay-tag">Tailored for {company}</div>
                    <div class="tmay-quote">"</div>
                    <div class="tmay-text">{tmay_text}</div>
                </div>""", unsafe_allow_html=True)
                st.download_button(
                    label="⬇  Download TMAY as .txt",
                    data=tmay_text,
                    file_name=f"tmay_{company.replace(' ','_')}.txt",
                    mime="text/plain",
                    key=f"dl_{idx}"
                )

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # restart
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🔍 Search Another Role"):
            st.session_state.step = "search"
            st.rerun()
    with col2:
        if st.button("👤 Start Fresh (New Profile)"):
            st.session_state.profile = None
            st.session_state.step = "profile"
            st.session_state.results = None
            st.rerun()

# footer
st.markdown('<p style="text-align:center;color:#1F2937;font-size:0.72rem;margin-top:2rem">Job Intelligence Agent · Multi-Agent Pipeline · LangChain + Mistral AI</p>', unsafe_allow_html=True)
