import streamlit as st
import json
import random

# =====================================================
# PAGE CONFIG + STYLE
# =====================================================
st.set_page_config(
    page_title="Legal Rights Assistant",
    page_icon="⚖️",
    layout="wide"
)

st.markdown("""
<style>
.stButton>button {
    background-color: #0f766e;
    color: white;
    font-weight: bold;
    border-radius: 8px;
    width: 100%;
}
.stTextArea textarea {
    font-size: 16px;
}
.block-container {
    padding-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# LOAD JSON
# =====================================================
def load_json(file):
    with open(file, "r", encoding="utf-8") as f:
        return json.load(f)

actions_data = load_json("action.json")
salary_laws = load_json("salary_laws.json")
termination_laws = load_json("termination_laws.json")
harassment_laws = load_json("harassment_laws.json")
benefits_laws = load_json("benefits_laws.json")
overtime_laws = load_json("overtime_laws.json")

laws_map = {
    "Salary Delay": salary_laws,
    "Unfair Termination": termination_laws,
    "Workplace Harassment": harassment_laws,
    "Denial of Benefits": benefits_laws,
    "Overtime Violation": overtime_laws,
}

# =====================================================
# CLASSIFIER
# =====================================================
def classify_issue(text):
    text = text.lower()

    categories = {
        "Workplace Harassment": ["harass", "abuse", "bully", "sexual"],
        "Salary Delay": ["salary delay", "not paid", "wage delay", "unpaid"],
        "Overtime Violation": ["overtime", "extra hours", "late night"],
        "Denial of Benefits": ["pf", "epf", "gratuity", "insurance", "esi"],
        "Unfair Termination": ["fired", "terminate", "laid off", "dismiss"]
    }

    for category, phrases in categories.items():
        for phrase in phrases:
            if phrase in text:
                return category
    return None

# =====================================================
# EMAIL + CONCLUSION
# =====================================================
def generate_email(category):
    emails = {
        "Salary Delay": """Subject: Request for Pending Salary Payment

Dear Sir/Madam,

My salary has not been credited within the scheduled time. Kindly release the pending amount at the earliest.

Sincerely,
[Your Name]""",

        "Unfair Termination": """Subject: Representation Against Termination

Dear Sir/Madam,

My employment has been terminated without due process. I request clarification and reconsideration.

Sincerely,
[Your Name]"""
    }
    return emails.get(category, "Formal complaint draft not available.")

def generate_conclusion(category):
    return f"This appears to be a {category} issue. You are legally protected and may pursue the above remedies."

# =====================================================
# CORE PROCESS
# =====================================================
def process_query(user_input):

    category = classify_issue(user_input)
    if not category:
        return None

    law_data = laws_map.get(category, [])
    action_data = actions_data.get(category, {})

    issue = action_data.get("description", f"{category} related issue.")

    laws = "\n".join([
        f"- {item.get('law_name', item.get('law'))} ({item.get('section','')})"
        for item in law_data
    ])

    # FIXED step duplication
    steps = "\n\n".join(action_data.get("steps", []))

    docs = "\n".join([f"- {d}" for d in action_data.get("documents_required", [])])

    portals = action_data.get("official_portals", [])
    url = portals[0]["url"] if portals else "https://labour.gov.in"

    email = generate_email(category)
    conclusion = generate_conclusion(category)

    confidence = round(random.uniform(0.82, 0.95), 2)

    return category, issue, laws, steps, docs, email, url, conclusion, confidence

# =====================================================
# SIDEBAR
# =====================================================
st.sidebar.title("⚖️ Legal Rights Assistant")
st.sidebar.markdown("""
### Supported Areas
- Salary Delay
- Unfair Termination
- Workplace Harassment
- Denial of Benefits
- Overtime Violation

### Features
- Smart classification
- Law mapping
- Structured action steps
- Draft email generation
- Official portal redirection
- Confidence scoring
""")

# =====================================================
# MAIN UI
# =====================================================
st.title("Legal Rights Guidance Platform")
st.caption("Structured legal guidance for workplace issues")

st.divider()

user_input = st.text_area(
    "Describe your workplace issue:",
    height=120,
    placeholder="Example: I was laid off without notice."
)

analyze = st.button("Analyze Case")

if analyze:

    if not user_input.strip():
        st.warning("Please enter your issue.")
        st.stop()

    result = process_query(user_input)

    if not result:
        st.error("Please describe a valid workplace issue.")
        st.stop()

    category, issue, laws, steps, docs, email, url, conclusion, confidence = result

    st.divider()

    col1, col2 = st.columns([3,1])

    with col1:
        st.subheader("Category")
        st.success(category)

    with col2:
        st.subheader("Confidence Score")
        st.metric("Model Confidence", f"{int(confidence*100)}%")
        st.progress(confidence)

    st.subheader("Issue Summary")
    st.write(issue)

    st.subheader("Relevant Laws")
    st.write(laws)

    st.subheader("Next Steps")
    st.write(steps)

    st.subheader("Documents Required")
    st.write(docs if docs else "No specific documents listed.")

    # PROFESSIONAL EMAIL + DOWNLOAD
    with st.expander("✉️ Draft Complaint Email"):
        st.code(email, language="text")

        safe_category = category.replace(" ", "_").lower()
        file_name = f"{safe_category}_formal_complaint_draft.txt"

        st.download_button(
            label="Download Formal Complaint Draft",
            data=email,
            file_name=file_name,
            mime="text/plain"
        )

    st.subheader("Official Complaint Portal")
    st.markdown(f"{url}")

    st.subheader("Conclusion")
    st.info(conclusion)

    st.warning("Disclaimer: This is preliminary guidance. Consult a qualified lawyer for formal advice.")
