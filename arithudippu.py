```python
import streamlit as st
import json
import time
from datetime import datetime

from google import genai
from google.genai import types


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="ReqPilot AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# SESSION STATE
# ============================================================

DEFAULT_STATE = {
    "logged_in": False,
    "username": "",
    "api_key": "",
    "messages": [],
    "analysis": None,
    "history": [],
    "project_name": "",
}

for key, value in DEFAULT_STATE.items():

    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# PREMIUM GLASS UI
# ============================================================

st.markdown(
    """
    <style>

    /* ======================================================
       GLOBAL
       ====================================================== */

    .stApp {

        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(108, 76, 255, 0.30),
                transparent 28%
            ),
            radial-gradient(
                circle at 90% 15%,
                rgba(0, 190, 255, 0.20),
                transparent 30%
            ),
            radial-gradient(
                circle at 50% 100%,
                rgba(255, 50, 190, 0.15),
                transparent 35%
            ),
            #050711;

        color: white;
    }


    .block-container {

        max-width: 1400px;

        padding-top: 2rem;
        padding-bottom: 4rem;
    }


    /* ======================================================
       GLASS CARDS
       ====================================================== */

    div[data-testid="stVerticalBlockBorderWrapper"] {

        background:
            linear-gradient(
                135deg,
                rgba(255,255,255,0.095),
                rgba(255,255,255,0.025)
            );

        border:
            1px solid rgba(255,255,255,0.13);

        border-radius: 25px;

        backdrop-filter:
            blur(25px);

        -webkit-backdrop-filter:
            blur(25px);

        box-shadow:
            0 20px 60px rgba(0,0,0,0.30),
            inset 0 1px 0 rgba(255,255,255,0.08);
    }


    /* ======================================================
       HEADINGS
       ====================================================== */

    h1 {

        font-size: 3.2rem !important;

        font-weight: 850 !important;

        letter-spacing: -2px;
    }


    h2 {

        font-weight: 800 !important;
    }


    h3 {

        font-weight: 700 !important;
    }


    /* ======================================================
       INPUTS
       ====================================================== */

    .stTextInput input,
    .stTextArea textarea {

        background:
            rgba(255,255,255,0.055) !important;

        color:
            white !important;

        border:
            1px solid rgba(255,255,255,0.13) !important;

        border-radius:
            16px !important;

        backdrop-filter:
            blur(15px);
    }


    .stTextInput input:focus,
    .stTextArea textarea:focus {

        border:
            1px solid rgba(100,160,255,0.65) !important;

        box-shadow:
            0 0 25px rgba(80,130,255,0.20);
    }


    /* ======================================================
       BUTTONS
       ====================================================== */

    .stButton > button {

        min-height:
            46px;

        border-radius:
            15px;

        background:
            rgba(255,255,255,0.065);

        color:
            white;

        border:
            1px solid rgba(255,255,255,0.14);

        font-weight:
            650;

        transition:
            0.2s ease;
    }


    .stButton > button:hover {

        background:
            rgba(255,255,255,0.13);

        transform:
            translateY(-2px);

        border-color:
            rgba(255,255,255,0.25);
    }


    .stButton > button[kind="primary"] {

        background:
            linear-gradient(
                135deg,
                rgba(118,74,255,0.92),
                rgba(0,184,255,0.82)
            );

        box-shadow:
            0 8px 30px rgba(70,100,255,0.25);
    }


    /* ======================================================
       METRICS
       ====================================================== */

    div[data-testid="stMetric"] {

        background:
            rgba(255,255,255,0.045);

        border:
            1px solid rgba(255,255,255,0.09);

        border-radius:
            18px;

        padding:
            14px;
    }


    /* ======================================================
       SIDEBAR
       ====================================================== */

    section[data-testid="stSidebar"] {

        background:
            rgba(4,6,15,0.90);

        border-right:
            1px solid rgba(255,255,255,0.08);

        backdrop-filter:
            blur(25px);
    }


    /* ======================================================
       CHAT
       ====================================================== */

    div[data-testid="stChatMessage"] {

        background:
            rgba(255,255,255,0.045);

        border:
            1px solid rgba(255,255,255,0.08);

        border-radius:
            18px;
    }


    /* ======================================================
       BADGE
       ====================================================== */

    .badge {

        display:
            inline-block;

        padding:
            7px 13px;

        border-radius:
            30px;

        background:
            rgba(255,255,255,0.065);

        border:
            1px solid rgba(255,255,255,0.12);

        font-size:
            13px;

        color:
            rgba(255,255,255,0.78);
    }


    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOGIN
# ============================================================

if not st.session_state.logged_in:

    st.markdown("<br><br><br>", unsafe_allow_html=True)

    left, center, right = st.columns(
        [1, 1.35, 1]
    )

    with center:

        with st.container(border=True):

            st.markdown(
                """
                <div style="text-align:center;">

                    <div style="
                        font-size:65px;
                        margin-bottom:5px;
                    ">
                        🚀
                    </div>

                    <h1>
                        ReqPilot
                    </h1>

                    <p>
                        AI Requirements Engineering Platform
                    </p>

                    <span class="badge">
                        🔐 Secure Workspace
                    </span>

                </div>
                """,
                unsafe_allow_html=True
            )

            st.divider()

            username = st.text_input(
                "👤 Username",
                placeholder="Enter username"
            )

            password = st.text_input(
                "🔐 Password",
                type="password",
                placeholder="Enter password"
            )

            st.write("")

            login = st.button(
                "🚀 Enter ReqPilot",
                type="primary",
                use_container_width=True
            )

            if login:

                if (
                    username == "reqpilot"
                    and password == "reqpilot123"
                ):

                    st.session_state.logged_in = True
                    st.session_state.username = username

                    st.rerun()

                else:

                    st.error(
                        "❌ Invalid username or password."
                    )

            st.write("")

            st.caption(
                "Demo account: reqpilot / reqpilot123"
            )

    st.stop()


# ============================================================
# API KEY
# ============================================================

def get_api_key():

    try:

        return st.secrets["GEMINI_API_KEY"]

    except Exception:

        return st.session_state.api_key


# ============================================================
# GEMINI CLIENT
# ============================================================

def get_client():

    key = get_api_key()

    if not key:
        return None

    return genai.Client(
        api_key=key
    )


# ============================================================
# GENERAL AI CHAT
# ============================================================

def ask_reqpilot(question):

    client = get_client()

    if client is None:

        return (
            "⚠️ Gemini API key is not configured.\n\n"
            "Add your Gemini API key in the sidebar."
        )

    prompt = f"""
You are ReqPilot, an advanced AI Requirements Engineering
and Software Engineering assistant.

Answer the user's question accurately.

You can help with:

- Software requirements
- Functional requirements
- Non-functional requirements
- SRS
- User stories
- Acceptance criteria
- Agile
- Scrum
- MoSCoW
- UML
- System architecture
- Database design
- API design
- Testing
- Cybersecurity
- Software engineering
- Programming
- Project ideas
- Technical explanations
- General questions

If the question is technical, give a practical answer.

User Question:

{question}
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:

        return f"❌ AI Error: {e}"


# ============================================================
# REQUIREMENT ANALYSIS
# ============================================================

def analyze_project(
    project_name,
    project_description
):

    client = get_client()

    if client is None:
        return None

    prompt = f"""
You are ReqPilot, an expert Requirements Engineering Agent.

Project Name:
{project_name}

Project Description:
{project_description}

Analyze the project deeply.

Return ONLY valid JSON.

Use EXACTLY this structure:

{{
    "project_summary": "",

    "functional_requirements": [
        {{
            "id": "FR-001",
            "requirement": "",
            "priority": "",
            "source": ""
        }}
    ],

    "non_functional_requirements": [
        {{
            "id": "NFR-001",
            "requirement": "",
            "category": "",
            "metric": ""
        }}
    ],

    "user_stories": [
        {{
            "id": "US-001",
            "story": "",
            "acceptance_criteria": []
        }}
    ],

    "priorities": [
        {{
            "requirement_id": "",
            "priority": "",
            "reason": ""
        }}
    ],

    "ambiguities": [
        {{
            "id": "AMB-001",
            "statement": "",
            "problem": "",
            "clarification": ""
        }}
    ],

    "duplicates": [
        {{
            "requirements": [],
            "reason": ""
        }}
    ],

    "contradictions": [
        {{
            "requirements": [],
            "problem": "",
            "resolution": ""
        }}
    ],

    "traceability": [
        {{
            "requirement_id": "",
            "user_story_id": "",
            "test_case_ids": []
        }}
    ],

    "test_cases": [
        {{
            "id": "TC-001",
            "requirement_id": "",
            "scenario": "",
            "steps": [],
            "expected_result": ""
        }}
    ],

    "architecture": {{
        "frontend": [],
        "backend": [],
        "database": [],
        "ai_services": [],
        "external_services": [],
        "deployment": []
    }},

    "api_specification": [
        {{
            "method": "",
            "endpoint": "",
            "purpose": "",
            "request": "",
            "response": ""
        }}
    ],

    "database_specification": [
        {{
            "table": "",
            "purpose": "",
            "columns": []
        }}
    ],

    "security_requirements": [],

    "scalability_requirements": [],

    "risks": [
        {{
            "risk": "",
            "impact": "",
            "mitigation": ""
        }}
    ],

    "srs": {{
        "introduction": "",
        "scope": "",
        "actors": [],
        "functional_overview": "",
        "non_functional_overview": "",
        "constraints": [],
        "assumptions": []
    }}
}}

Rules:

1. Do not invent unnecessary features.
2. Identify requirements from the supplied project.
3. Use measurable non-functional requirements when possible.
4. Detect vague statements.
5. Detect duplicate requirements.
6. Detect contradictions.
7. Maintain requirement traceability.
8. Generate realistic test cases.
9. Generate practical architecture.
10. Generate API suggestions only when relevant.
11. Generate database tables only when relevant.
12. Include security and scalability.
13. Use MoSCoW for priorities.
14. Keep IDs consistent.
15. Return valid JSON only.
"""

    try:

        response = client.models.generate_content(

            model="gemini-2.5-flash",

            contents=prompt,

            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )

        return json.loads(
            response.text
        )

    except Exception as e:

        st.error(
            f"❌ Analysis failed: {e}"
        )

        return None


# ============================================================
# MARKDOWN REPORT
# ============================================================

def create_markdown_report(data):

    srs = data.get(
        "srs",
        {}
    )

    text = "# ReqPilot Requirements Report\n\n"

    text += "## Project Summary\n\n"

    text += (
        data.get(
            "project_summary",
            ""
        )
        + "\n\n"
    )

    text += "## Functional Requirements\n\n"

    for item in data.get(
        "functional_requirements",
        []
    ):

        text += (
            f"- **{item.get('id')}** "
            f"{item.get('requirement')} "
            f"({item.get('priority')})\n"
        )

    text += "\n## Non-Functional Requirements\n\n"

    for item in data.get(
        "non_functional_requirements",
        []
    ):

        text += (
            f"- **{item.get('id')}** "
            f"{item.get('requirement')} "
            f"| Category: {item.get('category')} "
            f"| Metric: {item.get('metric')}\n"
        )

    text += "\n## User Stories\n\n"

    for story in data.get(
        "user_stories",
        []
    ):

        text += (
            f"### {story.get('id')}\n\n"
            f"{story.get('story')}\n\n"
        )

        text += "Acceptance Criteria:\n"

        for criteria in story.get(
            "acceptance_criteria",
            []
        ):

            text += f"- {criteria}\n"

        text += "\n"

    text += "## Ambiguities\n\n"

    for item in data.get(
        "ambiguities",
        []
    ):

        text += (
            f"- **{item.get('id')}** "
            f"{item.get('statement')}\n"
        )

        text += (
            f"  - Problem: {item.get('problem')}\n"
        )

        text += (
            f"  - Clarification: "
            f"{item.get('clarification')}\n"
        )

    text += "\n## Test Cases\n\n"

    for test in data.get(
        "test_cases",
        []
    ):

        text += (
            f"### {test.get('id')}\n\n"
            f"Requirement: "
            f"{test.get('requirement_id')}\n\n"
            f"Scenario: "
            f"{test.get('scenario')}\n\n"
            f"Expected Result: "
            f"{test.get('expected_result')}\n\n"
        )

    text += "## Security Requirements\n\n"

    for item in data.get(
        "security_requirements",
        []
    ):

        text += f"- {item}\n"

    text += "\n## Risks\n\n"

    for risk in data.get(
        "risks",
        []
    ):

        text += (
            f"- **{risk.get('risk')}**\n"
            f"  - Impact: {risk.get('impact')}\n"
            f"  - Mitigation: {risk.get('mitigation')}\n"
        )

    text += "\n## SRS\n\n"

    text += (
        "### Introduction\n"
        + srs.get("introduction", "")
        + "\n\n"
    )

    text += (
        "### Scope\n"
        + srs.get("scope", "")
        + "\n\n"
    )

    text += (
        "### Functional Overview\n"
        + srs.get("functional_overview", "")
        + "\n\n"
    )

    text += (
        "### Non-Functional Overview\n"
        + srs.get("non_functional_overview", "")
        + "\n\n"
    )

    return text


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        "## 🚀 ReqPilot"
    )

    st.caption(
        f"Logged in as **{st.session_state.username}**"
    )

    st.divider()

    st.markdown(
        "### 🧠 AI Modules"
    )

    modules = [
        "💬 AI Assistant",
        "📋 Requirement Extraction",
        "👤 User Stories",
        "⚡ MoSCoW",
        "🔎 Ambiguity Detection",
        "♻️ Duplicate Detection",
        "⚠️ Contradiction Detection",
        "🔗 Traceability",
        "🧪 Test Generation",
        "🏗️ Architecture",
        "🔌 API Specification",
        "🗄️ Database Specification",
        "🔐 Security",
        "📈 Scalability",
        "🚨 Risk Analysis",
        "📄 SRS Generator",
    ]

    for module in modules:
        st.write(module)

    st.divider()

    st.markdown(
        "### 🔑 Gemini"
    )

    try:

        st.secrets["GEMINI_API_KEY"]

        st.success(
            "API connected"
        )

    except Exception:

        key = st.text_input(
            "Gemini API Key",
            type="password"
        )

        if key:

            st.session_state.api_key = key

            st.success(
                "API key loaded"
            )

    st.divider()

    if st.button(
        "🗑️ Clear Everything",
        use_container_width=True
    ):

        st.session_state.messages = []
        st.session_state.analysis = None
        st.session_state.history = []

        st.rerun()

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False

        st.session_state.messages = []

        st.rerun()


# ============================================================
# MAIN HEADER
# ============================================================

with st.container(border=True):

    left, right = st.columns(
        [4, 1]
    )

    with left:

        st.markdown(
            "# 🚀 ReqPilot"
        )

        st.write(
            "AI Requirements Engineering Platform"
        )

        st.caption(
            "Transform raw ideas into traceable, "
            "testable and development-ready specifications."
        )

    with right:

        st.markdown(
            """
            <div style="
                text-align:right;
                padding-top:20px;
            ">
                <span class="badge">
                    🟢 SYSTEM ONLINE
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# DASHBOARD METRICS
# ============================================================

st.write("")

fr_count = 0
nfr_count = 0
story_count = 0
test_count = 0

if st.session_state.analysis:

    data = st.session_state.analysis

    fr_count = len(
        data.get(
            "functional_requirements",
            []
        )
    )

    nfr_count = len(
        data.get(
            "non_functional_requirements",
            []
        )
    )

    story_count = len(
        data.get(
            "user_stories",
            []
        )
    )

    test_count = len(
        data.get(
            "test_cases",
            []
        )
    )


m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric(
        "Functional",
        fr_count
    )

with m2:
    st.metric(
        "Non-Functional",
        nfr_count
    )

with m3:
    st.metric(
        "User Stories",
        story_count
    )

with m4:
    st.metric(
        "Test Cases",
        test_count
    )


# ============================================================
# MAIN NAVIGATION
# ============================================================

st.write("")

tabs = st.tabs(
    [
        "💬 AI Assistant",
        "🧠 Analyzer",
        "📊 Dashboard",
        "🏗️ Architecture",
        "🔗 Traceability",
        "📄 SRS",
        "📜 History"
    ]
)


# ============================================================
# AI ASSISTANT
# ============================================================

with tabs[0]:

    with st.container(border=True):

        st.markdown(
            "## 💬 ReqPilot AI Assistant"
        )

        st.caption(
            "Ask ReqPilot anything about your software project."
        )

        if not st.session_state.messages:

            st.info(
                "Try asking: "
                "\"Create requirements for an AI crop disease "
                "detection system\""
            )

        for message in st.session_state.messages:

            with st.chat_message(
                message["role"]
            ):

                st.markdown(
                    message["content"]
                )

        question = st.chat_input(
            "Ask ReqPilot anything..."
        )

        if question:

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": question
                }
            )

            with st.chat_message("user"):

                st.markdown(
                    question
                )

            with st.chat_message("assistant"):

                with st.spinner(
                    "ReqPilot is thinking..."
                ):

                    answer = ask_reqpilot(
                        question
                    )

                st.markdown(
                    answer
                )

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )


# ============================================================
# ANALYZER
# ============================================================

with tabs[1]:

    with st.container(border=True):

        st.markdown(
            "## 🧠 Requirements Intelligence Engine"
        )

        project_name = st.text_input(
            "Project Name",
            placeholder="Example: Smart Campus AI"
        )

        project_description = st.text_area(
            "Describe your project",
            height=220,
            placeholder=(
                "Explain your product idea, users, "
                "features and expected behavior..."
            )
        )

        analyze = st.button(
            "🚀 Analyze Project",
            type="primary",
            use_container_width=True
        )

        if analyze:

            if not project_description.strip():

                st.warning(
                    "Enter your project description."
                )

            elif not get_api_key():

                st.error(
                    "Gemini API key is required."
                )

            else:

                with st.spinner(
                    "🧠 ReqPilot is analyzing the project..."
                ):

                    result = analyze_project(
                        project_name,
                        project_description
                    )

                if result:

                    st.session_state.analysis = result

                    st.session_state.project_name = (
                        project_name
                    )

                    st.session_state.history.append(
                        {
                            "project": project_name,
                            "time": datetime.now().strftime(
                                "%Y-%m-%d %H:%M:%S"
                            ),
                            "requirements": len(
                                result.get(
                                    "functional_requirements",
                                    []
                                )
                            )
                        }
                    )

                    st.success(
                        "✅ Analysis completed."
                    )


# ============================================================
# DASHBOARD
# ============================================================

with tabs[2]:

    data = st.session_state.analysis

    if not data:

        st.info(
            "Run a project analysis first."
        )

    else:

        st.markdown(
            "## 📊 Requirement Dashboard"
        )

        c1, c2 = st.columns(2)

        with c1:

            st.markdown(
                "### 📋 Functional Requirements"
            )

            for item in data.get(
                "functional_requirements",
                []
            ):

                st.write(
                    f"**{item.get('id')}** — "
                    f"{item.get('requirement')}"
                )

        with c2:

            st.markdown(
                "### 📋 Non-Functional Requirements"
            )

            for item in data.get(
                "non_functional_requirements",
                []
            ):

                st.write(
                    f"**{item.get('id')}** — "
                    f"{item.get('requirement')}"
                )

        st.divider()

        st.markdown(
            "### 🔎 Requirement Quality"
        )

        q1, q2, q3 = st.columns(3)

        with q1:

            st.metric(
                "Ambiguities",
                len(
                    data.get(
                        "ambiguities",
                        []
                    )
                )
            )

        with q2:

            st.metric(
                "Duplicates",
                len(
                    data.get(
                        "duplicates",
                        []
                    )
                )
            )

        with q3:

            st.metric(
                "Contradictions",
                len(
                    data.get(
                        "contradictions",
                        []
                    )
                )
            )

        st.divider()

        st.markdown(
            "### 🚨 Risks"
        )

        for risk in data.get(
            "risks",
            []
        ):

            with st.container(
                border=True
            ):

                st.write(
                    f"**{risk.get('risk')}**"
                )

                st.write(
                    f"Impact: {risk.get('impact')}"
                )

                st.caption(
                    f"Mitigation: "
                    f"{risk.get('mitigation')}"
                )


# ============================================================
# ARCHITECTURE
# ============================================================

with tabs[3]:

    data = st.session_state.analysis

    if not data:

        st.info(
            "Analyze a project to generate architecture."
        )

    else:

        st.markdown(
            "## 🏗️ Suggested System Architecture"
        )

        architecture = data.get(
            "architecture",
            {}
        )

        categories = [
            ("🖥️ Frontend", "frontend"),
            ("⚙️ Backend", "backend"),
            ("🗄️ Database", "database"),
            ("🤖 AI Services", "ai_services"),
            ("🔌 External Services", "external_services"),
            ("☁️ Deployment", "deployment"),
        ]

        cols = st.columns(3)

        for index, (
            title,
            key
        ) in enumerate(categories):

            with cols[index % 3]:

                with st.container(
                    border=True
                ):

                    st.markdown(
                        f"### {title}"
                    )

                    for item in architecture.get(
                        key,
                        []
                    ):

                        st.write(
                            f"• {item}"
                        )

        st.divider()

        st.markdown(
            "## 🔌 API Specification"
        )

        for api in data.get(
            "api_specification",
            []
        ):

            with st.container(
                border=True
            ):

                st.write(
                    f"**{api.get('method')} "
                    f"{api.get('endpoint')}**"
                )

                st.write(
                    api.get(
                        "purpose",
                        ""
                    )
                )

                st.caption(
                    f"Request: "
                    f"{api.get('request', '')}"
                )

                st.caption(
                    f"Response: "
                    f"{api.get('response', '')}"
                )

        st.divider()

        st.markdown(
            "## 🗄️ Database Specification"
        )

        for table in data.get(
            "database_specification",
            []
        ):

            with st.container(
                border=True
            ):

                st.write(
                    f"### {table.get('table')}"
                )

                st.write(
                    table.get(
                        "purpose",
                        ""
                    )
                )

                for column in table.get(
                    "columns",
                    []
                ):

                    st.write(
                        f"• {column}"
                    )


# ============================================================
# TRACEABILITY
# ============================================================

with tabs[4]:

    data = st.session_state.analysis

    if not data:

        st.info(
            "Analyze a project to generate traceability."
        )

    else:

        st.markdown(
            "## 🔗 Requirements Traceability Matrix"
        )

        traceability = data.get(
            "traceability",
            []
        )

        for item in traceability:

            with st.container(
                border=True
            ):

                st.write(
                    f"### {item.get('requirement_id')}"
                )

                st.write(
                    f"👤 User Story: "
                    f"{item.get('user_story_id')}"
                )

                st.write(
                    "🧪 Tests: "
                    + ", ".join(
                        item.get(
                            "test_case_ids",
                            []
                        )
                    )
                )

        st.divider()

        st.markdown(
            "## 🔎 Ambiguities"
        )

        for item in data.get(
            "ambiguities",
            []
        ):

            with st.container(
                border=True
            ):

                st.write(
                    f"**{item.get('id')}**"
                )

                st.write(
                    f"Statement: "
                    f"{item.get('statement')}"
                )

                st.write(
                    f"Problem: "
                    f"{item.get('problem')}"
                )

                st.write(
                    f"Suggested clarification: "
                    f"{item.get('clarification')}"
                )

        st.markdown(
            "## ♻️ Duplicate Requirements"
        )

        for item in data.get(
            "duplicates",
            []
        ):

            st.write(
                f"Requirements: "
                f"{', '.join(item.get('requirements', []))}"
            )

            st.caption(
                item.get(
                    "reason",
                    ""
                )
            )

        st.markdown(
            "## ⚠️ Contradictions"
        )

        for item in data.get(
            "contradictions",
            []
        ):

            with st.container(
                border=True
            ):

                st.write(
                    ", ".join(
                        item.get(
                            "requirements",
                            []
                        )
                    )
                )

                st.write(
                    item.get(
                        "problem",
                        ""
                    )
                )

                st.caption(
                    f"Resolution: "
                    f"{item.get('resolution', '')}"
                )


# ============================================================
# SRS
# ============================================================

with tabs[5]:

    data = st.session_state.analysis

    if not data:

        st.info(
            "Analyze a project to generate SRS."
        )

    else:

        st.markdown(
            "## 📄 Software Requirements Specification"
        )

        srs = data.get(
            "srs",
            {}
        )

        st.markdown(
            "### 1. Introduction"
        )

        st.write(
            srs.get(
                "introduction",
                ""
            )
        )

        st.markdown(
            "### 2. Scope"
        )

        st.write(
            srs.get(
                "scope",
                ""
            )
        )

        st.markdown(
            "### 3. Actors"
        )

        for actor in srs.get(
            "actors",
            []
        ):

            st.write(
                f"• {actor}"
            )

        st.markdown(
            "### 4. Functional Overview"
        )

        st.write(
            srs.get(
                "functional_overview",
                ""
            )
        )

        st.markdown(
            "### 5. Non-Functional Overview"
        )

        st.write(
            srs.get(
                "non_functional_overview",
                ""
            )
        )

        st.markdown(
            "### 6. Constraints"
        )

        for item in srs.get(
            "constraints",
            []
        ):

            st.write(
                f"• {item}"
            )

        st.markdown(
            "### 7. Assumptions"
        )

        for item in srs.get(
            "assumptions",
            []
        ):

            st.write(
                f"• {item}"
            )

        st.divider()

        markdown_report = create_markdown_report(
            data
        )

        json_report = json.dumps(
            data,
            indent=2,
            ensure_ascii=False
        )

        c1, c2 = st.columns(2)

        with c1:

            st.download_button(
                "📥 Download SRS Markdown",
                data=markdown_report,
                file_name="reqpilot_srs.md",
                mime="text/markdown",
                use_container_width=True
            )

        with c2:

            st.download_button(
                "📥 Download Full JSON",
                data=json_report,
                file_name="reqpilot_full_report.json",
                mime="application/json",
                use_container_width=True
            )


# ============================================================
# HISTORY
# ============================================================

with tabs[6]:

    st.markdown(
        "## 📜 Analysis History"
    )

    if not st.session_state.history:

        st.info(
            "No analysis has been performed yet."
        )

    else:

        for item in reversed(
            st.session_state.history
        ):

            with st.container(
                border=True
            ):

                st.write(
                    f"### 🚀 {item['project']}"
                )

                st.caption(
                    item["time"]
                )

                st.write(
                    f"Functional requirements: "
                    f"{item['requirements']}"
                )


# ============================================================
# SECURITY + FOOTER
# ============================================================

st.write("")

with st.container(border=True):

    st.markdown(
        """
        <div style="text-align:center;">

        <h3>🚀 ReqPilot</h3>

        <p>
        AI Requirements Engineering Platform
        </p>

        <span class="badge">
            Requirements • Architecture • Testing • Traceability
        </span>

        </div>
        """,
        unsafe_allow_html=True
    )
```

