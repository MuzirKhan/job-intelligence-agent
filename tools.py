from langchain.tools import tool
from linkedin_jobs_scraper import LinkedinScraper
from linkedin_jobs_scraper.events import Events, EventData
from linkedin_jobs_scraper.query import Query, QueryOptions
from langchain_mistralai import ChatMistralAI
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import json
import os

# ─────────────────────────────────────────────
# TOOL 1 — Scrape Jobs
# ─────────────────────────────────────────────
@tool
def scrape_jobs(role: str, location: str) -> str:
    """Scrapes LinkedIn for job listings based on role and location.
    Returns job listings as a JSON string."""

    jobs = []

    def on_data(data: EventData):
        jobs.append({
            "title": data.title,
            "company": data.company,
            "location": data.location,
            "description": data.description
        })

    scraper = LinkedinScraper()
    scraper.on(Events.DATA, on_data)
    scraper.on(Events.ERROR, lambda e: print(f"Scraper error: {e}"))

    scraper.run([Query(
        query=role,
        options=QueryOptions(locations=[location], limit=2)
    )])

    os.makedirs("data", exist_ok=True)
    with open("data/jobs_raw.json", "w") as f:
        json.dump(jobs, f, indent=4)

    return json.dumps(jobs)


# ─────────────────────────────────────────────
# TOOL 2 — Extract Skills from JDs
# ─────────────────────────────────────────────
@tool
def extract_skills(jobs_json: str) -> str:
    """Extracts required skills, domain, and experience from job descriptions.
    Takes a JSON string of jobs, returns extracted skills as JSON string."""

    llm = ChatMistralAI(model="mistral-small-2506",
            api_key=st.secrets.get("MISTRAL_API_KEY"))
    parser = JsonOutputParser()
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a professional skills extractor from job descriptions.
        Extract skills and return ONLY a valid JSON with these exact keys:
        required_skills, nice_to_have_skills, experience_years, domain, soft_skills.
        No markdown, no extra text, just JSON."""),
        ("human", "{query}")
    ])
    chain = prompt | llm | parser

    jobs = json.loads(jobs_json)
    extracted = []
    for job in jobs:
        result = chain.invoke({"query": job})
        result["title"] = job.get("title", "")
        result["company"] = job.get("company", "")
        extracted.append(result)

    with open("data/jobs_extracted.json", "w") as f:
        json.dump(extracted, f, indent=4)

    return json.dumps(extracted)


# ─────────────────────────────────────────────
# TOOL 3 — Gap Analyzer
# ─────────────────────────────────────────────
@tool
def analyze_gap(extracted_jobs_json: str, profile_json: str = "") -> str:
    """Analyzes skill gaps between extracted job requirements and user profile.
    Returns match score, matching skills, gaps, quick learnable and long term gaps."""

    # Use passed profile, fall back to file
    if profile_json:
        profile = json.loads(profile_json)
    else:
        with open("data/profile.json", "r") as f:
            profile = json.load(f)

    llm = ChatMistralAI(model="mistral-small-2506",    
        api_key=st.secrets.get("MISTRAL_API_KEY"))
    parser = JsonOutputParser()
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a professional gap analyzer for data engineers.
        Compare the job requirements against the candidate profile.
        match_score should be a number between 0 and 100.
        gaps, quick_learnable, long_term must always be flat lists of strings, never nested objects.
        Return ONLY a valid JSON with these exact keys:
        match_score, matching_skills, gaps, quick_learnable, long_term.
        No markdown, no extra text, just JSON."""),
        ("human", "Job Skills: {job_skills}\n\nMy Profile: {profile}")
    ])
    chain = prompt | llm | parser

    jobs = json.loads(extracted_jobs_json)
    gap_results = []
    for job in jobs:
        result = chain.invoke({"job_skills": job, "profile": profile})
        result["title"] = job.get("title", "")
        result["company"] = job.get("company", "")
        gap_results.append(result)

    with open("data/jobs_gap.json", "w") as f:
        json.dump(gap_results, f, indent=4)

    return json.dumps(gap_results)


# ─────────────────────────────────────────────
# TOOL 4 — Interview Prep Questions
# ─────────────────────────────────────────────
@tool
def prep_questions(gap_json: str) -> str:
    """Generates 5 tailored interview questions with hints based on job gaps and user profile.
    Returns questions as JSON string."""

    with open("data/profile.json", "r") as f:
        profile = json.load(f)

    llm = ChatMistralAI(model="mistral-large-latest",
    api_key=st.secrets.get("MISTRAL_API_KEY")
)
    parser = JsonOutputParser()
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a professional interview preparation coach for data engineers.
        Based on the user profile and job gaps, generate exactly 5 interview questions with hints.
        Return ONLY a valid JSON with this exact structure:
        {{ "questions": [ {{ "question": "...", "hint": "..." }} ] }}
        No markdown, no extra text, just JSON."""),
        ("human", "Here is the users profile: {profile} and gaps: {gaps}")
    ])
    chain = prompt | llm | parser

    gaps = json.loads(gap_json)
    prep_results = []
    for gap in gaps:
        result = chain.invoke({"profile": profile, "gaps": gap})
        result["title"] = gap.get("title", "")
        result["company"] = gap.get("company", "")
        prep_results.append(result)

    with open("data/jobs_prep.json", "w") as f:
        json.dump(prep_results, f, indent=4)

    return json.dumps(prep_results)


# ─────────────────────────────────────────────
# TOOL 5 — TMAY Generator
# ─────────────────────────────────────────────
@tool
def generate_tmay(gap_json: str) -> str:
    """Generates a tailored 90-second Tell Me About Yourself for each job.
    Returns TMAY responses as JSON string."""

    with open("data/profile.json", "r") as f:
        profile = json.load(f)

    llm = ChatMistralAI(model="mistral-large-latest",
    api_key=st.secrets.get("MISTRAL_API_KEY"))
    parser = StrOutputParser()
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a professional interview coach.
        Generate a confident, natural 90-second Tell Me About Yourself
        tailored to the specific job. Use simple language, highlight
        matching skills, address gaps gracefully, and end with enthusiasm."""),
        ("human", "Here is the users profile: {profile} and job gap analysis: {gaps}")
    ])
    chain = prompt | llm | parser

    gaps = json.loads(gap_json)
    tmay_results = []
    for gap in gaps:
        result = chain.invoke({"profile": profile, "gaps": gap})
        tmay_results.append({  
            "title": gap.get("title", ""),
            "company": gap.get("company", ""),
            "tmay": result
        })

    with open("data/tmay.json", "w") as f:
        json.dump(tmay_results, f, indent=4)

    return json.dumps(tmay_results)
