"""
AI Journalist Agent — Powered by Google Gemini 1.5 Flash
A three-agent pipeline: Searcher → Writer → Editor
Run with: streamlit run ai_journalist.py
"""

import streamlit as st
from google import genai
from datetime import datetime

# Page config & custom CSS
# ──────────────────────────────────────────
st.set_page_config(
    page_title="AI Journalist",
    page_icon="🗞️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Source+Serif+4:opsz,wght@8..60,300;8..60,400;8..60,600&display=swap');

/* ── global reset ── */
html, body, [class*="css"] {
    font-family: 'Source Serif 4', Georgia, serif;
    background-color: #FAF7F2;
    color: #1A1612;
}

/* ── masthead ── */
.masthead {
    text-align: center;
    border-top: 4px solid #1A1612;
    border-bottom: 1px solid #1A1612;
    padding: 18px 0 12px;
    margin-bottom: 6px;
}
.masthead-date {
    font-size: 0.72rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #6B6156;
    margin-bottom: 6px;
}
.masthead-title {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 3.4rem;
    font-weight: 700;
    letter-spacing: -0.5px;
    line-height: 1;
    margin: 0;
}
.masthead-sub {
    font-size: 0.78rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #6B6156;
    margin-top: 6px;
}

/* ── section rule ── */
.rule {
    border: none;
    border-top: 1px solid #C8BFB5;
    margin: 18px 0;
}

/* ── input card ── */
.input-card {
    background: #FFFFFF;
    border: 1px solid #DDD6CE;
    border-radius: 2px;
    padding: 28px 32px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    margin-bottom: 28px;
}
.input-card label {
    font-size: 0.72rem !important;
    letter-spacing: 0.16em !important;
    text-transform: uppercase !important;
    color: #6B6156 !important;
    font-family: 'Source Serif 4', serif !important;
}

/* ── pipeline steps ── */
.pipeline-step {
    display: flex;
    align-items: flex-start;
    gap: 14px;
    padding: 14px 18px;
    background: #FFFFFF;
    border-left: 3px solid #C8BFB5;
    margin-bottom: 10px;
    border-radius: 0 2px 2px 0;
    font-size: 0.88rem;
}
.pipeline-step.active   { border-left-color: #B5451B; }
.pipeline-step.complete { border-left-color: #2E6B3E; }
.step-icon { font-size: 1.3rem; line-height: 1; }
.step-label { font-weight: 600; font-size: 0.78rem; letter-spacing: 0.1em; text-transform: uppercase; }
.step-desc  { color: #6B6156; font-size: 0.83rem; margin-top: 2px; }

/* ── article output ── */
.article-container {
    background: #FFFFFF;
    border: 1px solid #DDD6CE;
    border-radius: 2px;
    padding: 48px 56px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.06);
    max-width: 820px;
    margin: 0 auto;
    line-height: 1.8;
}
.article-container h1 {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 2.2rem;
    line-height: 1.25;
    font-weight: 700;
    border-bottom: 1px solid #E8E0D8;
    padding-bottom: 18px;
    margin-bottom: 22px;
}
.article-container h2 {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 1.45rem;
    font-weight: 700;
    margin-top: 36px;
}
.article-container p {
    font-size: 1.05rem;
    text-align: justify;
    hyphens: auto;
    margin-bottom: 18px;
}
.article-container blockquote {
    border-left: 3px solid #B5451B;
    padding-left: 18px;
    color: #4A3F35;
    font-style: italic;
    margin: 24px 0;
}

/* ── byline ── */
.byline {
    font-size: 0.78rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #6B6156;
    margin-bottom: 28px;
    padding-bottom: 14px;
    border-bottom: 1px solid #E8E0D8;
}

/* ── status badge ── */
.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 2px;
    font-size: 0.72rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    font-weight: 600;
}
.badge-success { background: #E8F4EC; color: #2E6B3E; }
.badge-error   { background: #FDECE8; color: #B5451B; }

/* ── button ── */
div.stButton > button {
    background: #1A1612 !important;
    color: #FAF7F2 !important;
    font-family: 'Source Serif 4', serif !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 2px !important;
    padding: 12px 32px !important;
    transition: opacity 0.2s !important;
}
div.stButton > button:hover { opacity: 0.8 !important; }

/* ── expander ── */
.streamlit-expanderHeader {
    font-size: 0.78rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: #6B6156 !important;
}
</style>
""", unsafe_allow_html=True)



# Masthead
# ──────────────────────────────────────────
today = datetime.now().strftime("%A, %B %d, %Y")
st.markdown(f"""
<div class="masthead">
    <div class="masthead-date">{today}</div>
    <div class="masthead-title">The AI Journalist</div>
    <div class="masthead-sub">Powered by Google Gemini &nbsp;·&nbsp; Three-Agent Newsroom</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="rule">', unsafe_allow_html=True)



# Sidebar — API key + settings
# ──────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    gemini_api_key = st.text_input("Gemini API Key", type="password",
                                    help="Get yours at https://aistudio.google.com")
    st.markdown("---")
    st.markdown("**Model:** `gemini-1.5-flash`")
    st.markdown("**Pipeline**")
    st.markdown("1. 🔍 Searcher Agent")
    st.markdown("2. ✍️ Writer Agent")
    st.markdown("3. 📝 Editor Agent")
    st.markdown("---")
    st.caption("Paste your Gemini API key and enter a topic above to generate a full-length article.")


# Helper: call Gemini
# ──────────────────────────────────────────
def call_gemini(api_key: str, system_prompt: str, user_prompt: str, temperature: float = 0.7) -> str:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        system_instruction=system_prompt,
        generation_config=genai.types.GenerationConfig(
            temperature=temperature,
            max_output_tokens=8192,
        ),
    )
    response = model.generate_content(user_prompt)
    return response.text.strip()



# Agent 1 — Searcher
# ──────────────────────────────────────────
def run_searcher(api_key: str, topic: str) -> str:
    system = """You are an elite research journalist at The New York Times with 20 years of experience.
Your specialty is identifying the most credible, relevant, and timely sources for any given story."""

    user = f"""Research task: '{topic}'

Generate a comprehensive research briefing that includes:

1. **Search Strategy** — List 5 precise search queries a journalist would use to research this topic thoroughly.

2. **Key Source Categories** — Identify the types of authoritative sources that would be most valuable:
   - Academic / scientific institutions
   - Government agencies or official bodies
   - Leading journalists or experts in the field
   - Reputable news organizations
   - Industry reports or databases

3. **Simulated Source Discovery** — Based on your knowledge, describe 8–10 specific, credible sources (publications, organizations, reports, studies, or notable experts) that would likely contain high-quality information on this topic. For each source, note:
   - The source name / type
   - Why it is authoritative for this topic
   - What angle or data it likely covers

4. **Key Angles & Story Threads** — Identify 4–5 distinct editorial angles a NYT journalist might pursue.

5. **Critical Questions** — List 6 hard-hitting questions the article must answer for the reader.

Be specific, thorough, and journalistically rigorous. Today's date: {datetime.now().strftime('%B %d, %Y')}."""

    return call_gemini(api_key, system, user, temperature=0.5)



# Agent 2 — Writer
# ──────────────────────────────────────────
def run_writer(api_key: str, topic: str, research_briefing: str) -> str:
    system = """You are a Pulitzer Prize-winning senior writer at The New York Times.
You write with authority, nuance, and narrative craft. Your prose is elegant yet accessible.
You never fabricate quotes or facts — you synthesize information responsibly and attribute claims clearly.
You write in markdown format."""

    user = f"""Write a full-length, publication-ready New York Times feature article on the following topic.

**Topic:** {topic}

**Research Briefing from our team:**
{research_briefing}

**Article Requirements:**
- Minimum 1,500 words (aim for 2,000+)
- Minimum 15 well-developed paragraphs
- Start with a powerful, scene-setting lede that pulls the reader in immediately
- Use the "inverted pyramid" structure but with narrative depth
- Include a nut graf (paragraph 3–4) that clearly states why this matters now
- Weave in relevant data, statistics, and expert perspectives drawn from the research briefing
- Provide balanced, nuanced analysis — acknowledge complexity and counterarguments
- Use subheadings (##) to organize major sections
- End with a forward-looking conclusion that resonates
- Maintain an authoritative but engaging tone throughout
- Use blockquotes (>) for any notable statements or key findings
- Do NOT fabricate specific quotes from named individuals; frame insights as analysis or reported findings

**Format:**
# [Compelling Headline]

*[One-sentence deck/subheadline]*

---

[Full article body in markdown]

---
*Reported by The AI Journalist | {datetime.now().strftime('%B %d, %Y')}*"""

    return call_gemini(api_key, system, user, temperature=0.75)



# Agent 3 — Editor
# ──────────────────────────────────────────
def run_editor(api_key: str, topic: str, draft_article: str) -> str:
    system = """You are the Executive Editor of The New York Times with three decades of editorial experience.
You have an unfailing eye for clarity, accuracy, narrative flow, and journalistic standards.
You elevate good writing to great writing. You preserve the author's voice while sharpening every sentence.
You return the final, polished article in markdown format — no editorial commentary, just the finished piece."""

    user = f"""You are editing this draft article for immediate publication in The New York Times.

**Topic:** {topic}

**Draft Article:**
{draft_article}

**Your Editorial Pass — address all of the following:**

1. **Headline & Deck** — Is the headline irresistible and accurate? Sharpen if needed.
2. **Lede** — Does the opening grab attention within the first two sentences? Rewrite if necessary.
3. **Clarity** — Eliminate jargon, ambiguity, and passive voice. Make every sentence sing.
4. **Structure** — Ensure logical flow between paragraphs. Add or rewrite transitions where needed.
5. **Depth & Nuance** — Strengthen analysis. Add missing context. Ensure balanced perspectives.
6. **Factual Framing** — Flag any overly speculative claims and reframe them responsibly.
7. **Engagement** — Inject narrative energy. Cut any dead weight or redundant passages.
8. **Length** — The final piece must be substantive (1,500+ words). Expand thin sections if needed.
9. **Closing** — The final paragraph must leave a lasting impression. Rewrite if it doesn't.
10. **Polish** — Correct grammar, punctuation, and style to strict NYT standards.

Return ONLY the final, fully edited article in clean markdown. No meta-commentary."""

    return call_gemini(api_key, system, user, temperature=0.6)


# Main UI
# ──────────────────────────────────────────
st.markdown('<div class="input-card">', unsafe_allow_html=True)
col1, col2 = st.columns([4, 1])
with col1:
    topic = st.text_input(
        "Article Topic",
        placeholder="e.g., The global race to develop humanoid robots",
        label_visibility="visible",
    )
with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    generate_btn = st.button("Generate Article →", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Pipeline execution
# ──────────────────────────────────────────
if generate_btn:
    if not gemini_api_key:
        st.error("⚠️  Please enter your Gemini API key in the sidebar.")
        st.stop()
    if not topic.strip():
        st.error("⚠️  Please enter a topic for the article.")
        st.stop()

    # Pipeline progress display
    st.markdown("### Newsroom Pipeline")
    step1 = st.empty()
    step2 = st.empty()
    step3 = st.empty()

    def render_step(container, icon, label, desc, state="pending"):
        cls = {"pending": "", "active": "active", "complete": "complete"}.get(state, "")
        container.markdown(f"""
        <div class="pipeline-step {cls}">
            <div class="step-icon">{icon}</div>
            <div>
                <div class="step-label">{label}</div>
                <div class="step-desc">{desc}</div>
            </div>
        </div>""", unsafe_allow_html=True)

    render_step(step1, "🔍", "Searcher Agent", "Identifying sources and research angles…", "active")
    render_step(step2, "✍️", "Writer Agent", "Waiting…")
    render_step(step3, "📝", "Editor Agent", "Waiting…")

    try:
        # ── Step 1: Searcher 
        research = run_searcher(gemini_api_key, topic)
        render_step(step1, "✅", "Searcher Agent", "Research briefing complete.", "complete")

        # ── Step 2: Writer 
        render_step(step2, "✍️", "Writer Agent", "Drafting full-length article…", "active")
        draft = run_writer(gemini_api_key, topic, research)
        render_step(step2, "✅", "Writer Agent", "Draft article complete.", "complete")

        # ── Step 3: Editor 
        render_step(step3, "📝", "Editor Agent", "Editing and refining for publication…", "active")
        final_article = run_editor(gemini_api_key, topic, draft)
        render_step(step3, "✅", "Editor Agent", "Article polished and ready.", "complete")

        # Show article
        st.markdown("---")
        st.markdown('<div class="article-container">', unsafe_allow_html=True)
        st.markdown(f'<div class="byline">By The AI Journalist &nbsp;·&nbsp; {datetime.now().strftime("%B %d, %Y")}</div>', unsafe_allow_html=True)
        st.markdown(final_article)
        st.markdown('</div>', unsafe_allow_html=True)

        # Research briefing (collapsed)
        with st.expander("📋 View Research Briefing (Searcher Agent Output)"):
            st.markdown(research)

        # Download 
        st.download_button(
            label="⬇ Download Article (.md)",
            data=final_article,
            file_name=f"{topic[:50].replace(' ','_').lower()}_article.md",
            mime="text/markdown",
        )

    except Exception as e:
        st.markdown(f'<span class="badge badge-error">Pipeline Error</span>', unsafe_allow_html=True)
        st.error(f"An error occurred: {e}")
        st.info("Ensure your Gemini API key is valid and has sufficient quota.")




