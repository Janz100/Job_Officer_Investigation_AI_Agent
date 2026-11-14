
import re
import html
import streamlit as st

from agent import (
    investigate_job_offer,
    get_previous_investigations,
    get_investigation_by_id
)

from memory.feedback_memory import FeedbackMemory
from memory.long_term_memory import LongTermMemory


# ==================================================
# 1. APPLICATION CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="JobVerify AI | Investigation Dashboard",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================================================
# 2. INITIALIZE MEMORY
# ==================================================

long_term_memory = LongTermMemory()
feedback_memory = FeedbackMemory()


# ==================================================
# 3. SESSION STATE
# ==================================================

if "latest_result" not in st.session_state:
    st.session_state.latest_result = None

if "selected_investigation_id" not in st.session_state:
    st.session_state.selected_investigation_id = None

if "navigation" not in st.session_state:
    st.session_state.navigation = "Home"


# ==================================================
# 4. CUSTOM DESIGN
# ==================================================

st.markdown("""
<style>
    .stApp {
        background-color: #f5f7fb;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1450px;
    }

    .main-title {
        color: #142d4e;
        font-size: 32px;
        font-weight: 750;
        margin-bottom: 5px;
    }

    .main-subtitle {
        color: #64748b;
        font-size: 15px;
        margin-bottom: 25px;
    }

    .feature-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 20px;
        min-height: 140px;
        margin-bottom: 12px;
    }

    .feature-title {
        color: #183b61;
        font-size: 17px;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .feature-description {
        color: #64748b;
        font-size: 14px;
        line-height: 1.6;
    }

    .result-panel {
        background: #ffffff;
        border: 1px solid #dce5ef;
        border-left: 5px solid #2563eb;
        border-radius: 10px;
        padding: 18px;
        margin-bottom: 15px;
    }

    .verification-panel {
        border-left-color: #0d9488;
    }

    .panel-title {
        color: #183b61;
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .panel-description {
        color: #64748b;
        font-size: 13px;
    }

    div[data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 17px;
    }

    div[data-testid="stMetricValue"] {
        color: #183b61;
        font-weight: 700;
    }

    div.stButton > button,
    div.stFormSubmitButton > button {
        border-radius: 8px;
        font-weight: 600;
        min-height: 42px;
    }

    section[data-testid="stSidebar"] {
        background-color: #edf2f8;
        border-right: 1px solid #dce5ef;
    }

    div[data-testid="stExpander"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 9px;
    }

    hr {
        border-color: #dce5ef;
    }
</style>
""", unsafe_allow_html=True)


# ==================================================
# 5. ASSESSMENT CLASSIFICATION AND COLOURS
# ==================================================

ASSESSMENT_STYLES = {
    "Suspicious": {
        "color": "#b91c1c",
        "background": "#fee2e2",
        "border": "#ef4444",
        "description": "Significant warning signs or suspicious evidence detected."
    },
    "Likely Legitimate": {
        "color": "#166534",
        "background": "#dcfce7",
        "border": "#22c55e",
        "description": "Positive supporting evidence was found. This is not a guarantee."
    },
    "Needs Further Verification": {
        "color": "#92400e",
        "background": "#fef3c7",
        "border": "#f59e0b",
        "description": "More information or independent checks are needed."
    },
    "Inconclusive": {
        "color": "#475569",
        "background": "#e2e8f0",
        "border": "#94a3b8",
        "description": "The available information does not support a clear assessment."
    }
}


def classify_assessment(result):
    """
    Read the assessment returned by the backend.

    First checks explicit assessment fields.
    Then checks for an explicit Assessment: line in the reports.
    Finally checks for known assessment phrases.

    Does not automatically treat missing information as legitimate.
    """

    if not isinstance(result, dict):
        return "Inconclusive"

    # Check explicit fields first
    direct_fields = [
        "assessment",
        "final_assessment",
        "risk_level",
        "risk_assessment",
        "overall_assessment"
    ]

    direct_value = None

    for field in direct_fields:
        value = result.get(field)

        if value:
            direct_value = str(value).strip()
            break

    # Read report text if there is no direct assessment field
    report_text = " ".join(
        str(result.get(field, ""))
        for field in ["verification", "investigation", "analysis"]
        if result.get(field) is not None
    )

    if direct_value:
        text = direct_value.lower()
    else:
        text = report_text.lower()

    # Look for an explicit assessment line
    explicit_match = re.search(
        r"(?:final\s+)?assessment\s*[:\-]\s*([^\n\r]+)",
        report_text,
        re.IGNORECASE
    )

    if explicit_match:
        explicit_text = explicit_match.group(1).strip().lower()
    else:
        explicit_text = ""

    text_to_check = explicit_text if explicit_text else text

    # Suspicious
    if any(term in text_to_check for term in [
        "suspicious",
        "potentially fraudulent",
        "likely scam",
        "high risk",
        "fraudulent"
    ]):
        if not any(phrase in text_to_check for phrase in [
            "not suspicious",
            "no suspicious",
            "not fraudulent",
            "not a scam"
        ]):
            return "Suspicious"

    # Likely legitimate
    if any(term in text_to_check for term in [
        "likely legitimate",
        "appears legitimate",
        "likely genuine",
        "appears genuine"
    ]):
        return "Likely Legitimate"

    # Further verification needed
    if any(term in text_to_check for term in [
        "needs further verification",
        "requires further verification",
        "further verification required",
        "insufficient evidence",
        "unable to verify",
        "not verified",
        "more information required",
        "cannot confirm"
    ]):
        return "Needs Further Verification"

    # Inconclusive
    if any(term in text_to_check for term in [
        "inconclusive",
        "uncertain",
        "undetermined",
        "unknown"
    ]):
        return "Inconclusive"

    return "Inconclusive"


def show_assessment(result):
    """Display a large, coloured assessment panel."""

    assessment = classify_assessment(result)
    style = ASSESSMENT_STYLES[assessment]

    st.markdown(
        f"""
        <div style="
            background-color: {style['background']};
            border-left: 7px solid {style['border']};
            border-radius: 12px;
            padding: 22px;
            margin-top: 12px;
            margin-bottom: 22px;
        ">
            <div style="
                color: {style['color']};
                font-size: 13px;
                font-weight: 700;
                letter-spacing: 1px;
                margin-bottom: 8px;
            ">
                OVERALL ASSESSMENT
            </div>

            <div style="
                color: {style['color']};
                font-size: 27px;
                font-weight: 800;
                margin-bottom: 7px;
            ">
                {html.escape(assessment)}
            </div>

            <div style="
                color: {style['color']};
                font-size: 14px;
            ">
                {html.escape(style['description'])}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def show_assessment_legend():
    """Show all assessment categories and their colours."""

    st.markdown("### Assessment Colour Guide")

    columns = st.columns(4)

    for column, (name, style) in zip(
        columns,
        ASSESSMENT_STYLES.items()
    ):
        with column:
            st.markdown(
                f"""
                <div style="
                    background-color: {style['background']};
                    border: 1px solid {style['border']};
                    border-radius: 9px;
                    padding: 12px;
                    min-height: 95px;
                ">
                    <div style="
                        color: {style['color']};
                        font-weight: 750;
                        font-size: 13px;
                        margin-bottom: 7px;
                    ">
                        {html.escape(name)}
                    </div>
                    <div style="
                        color: {style['color']};
                        font-size: 11px;
                    ">
                        {html.escape(style['description'])}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


# ==================================================
# 6. HELPER FUNCTIONS
# ==================================================

def get_investigations():
    return get_previous_investigations() or []


def display_report(report, empty_message="No report available."):

    if report is None or report == "":
        st.info(empty_message)

    elif isinstance(report, str):
        st.markdown(report)

    else:
        st.json(report)


def display_technical_details(result):

    technical_sections = [
        ("Extracted Information", "extracted_information"),
        ("Website Check", "website_check"),
        ("Email Check", "email_check"),
        ("Scam Indicators", "scam_indicators"),
        ("Web Search Results", "web_results")
    ]

    for title, key in technical_sections:

        with st.expander(title):

            value = result.get(key)

            if value:
                if isinstance(value, (dict, list)):
                    st.json(value)
                else:
                    st.write(value)
            else:
                st.caption("No information available.")


def show_investigation(record):

    if not record:
        st.warning("Investigation not found.")
        return

    investigation_id = record.get("id", "Unknown")

    st.markdown(
        f"### Investigation #{investigation_id}"
    )

    st.caption(
        f"Created: {record.get('created_at', 'Unknown date')}"
    )

    # Build a result dictionary from the saved record
    saved_result = {
        "assessment": record.get("assessment"),
        "investigation": (
            record.get("analysis")
            or record.get("investigation")
        ),
        "verification": record.get("verification")
    }

    show_assessment(saved_result)

    with st.expander("Original Job Offer"):
        st.write(
            record.get("job_offer") or "No job offer available."
        )

    col1, col2 = st.columns(2, gap="large")

    with col1:

        st.markdown(
            """
            <div class="result-panel">
                <div class="panel-title">Job Analysis Agent</div>
                <div class="panel-description">
                    Information extracted and analysed from the job offer.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        display_report(
            saved_result["investigation"],
            "No job analysis report available."
        )

    with col2:

        st.markdown(
            """
            <div class="result-panel verification-panel">
                <div class="panel-title">Verification Agent</div>
                <div class="panel-description">
                    Evidence and verification findings.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        display_report(
            saved_result["verification"],
            "No verification report available."
        )


def show_new_investigation_result(result):

    investigation_id = result.get("investigation_id", "Unknown")

    st.divider()

    st.markdown(
        '<div class="main-title">Investigation Results</div>',
        unsafe_allow_html=True
    )

    st.caption(f"Investigation ID: #{investigation_id}")

    # Coloured assessment
    show_assessment(result)

    with st.expander("View Submitted Job Offer"):
        st.write(result.get("job_offer", "Job offer not available."))

    col1, col2 = st.columns(2, gap="large")

    with col1:

        st.markdown(
            """
            <div class="result-panel">
                <div class="panel-title">01 | Job Analysis Agent</div>
                <div class="panel-description">
                    Analyses the job offer and extracts important information.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        display_report(
            result.get("investigation"),
            "The job analysis report is not available."
        )

    with col2:

        st.markdown(
            """
            <div class="result-panel verification-panel">
                <div class="panel-title">02 | Verification Agent</div>
                <div class="panel-description">
                    Examines available evidence and identifies findings.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        display_report(
            result.get("verification"),
            "The verification report is not available."
        )

    st.divider()

    st.markdown("### Supporting Evidence")

    display_technical_details(result)

    st.success(
        f"Investigation #{investigation_id} has been completed. "
        "The result is available in Investigation History."
    )


# ==================================================
# 7. SIDEBAR NAVIGATION
# ==================================================

with st.sidebar:

    st.markdown(
        """
        <div style="padding: 10px 0 18px 0;">
            <div style="
                font-size: 25px;
                font-weight: 800;
                color: #17365d;">
                JobVerify AI
            </div>
            <div style="
                color: #64748b;
                font-size: 12px;
                margin-top: 5px;">
                Job Offer Investigation System
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "Home",
            "New Investigation",
            "Investigation History",
            "Feedback"
        ],
        key="navigation"
    )

    st.divider()

    st.markdown("**SYSTEM INFORMATION**")
    st.caption("Architecture: Multi-agent")
    st.caption("Workflow: LangGraph")
    st.caption("Language model: Ollama")
    st.caption("Memory: SQLite")


# ==================================================
# 8. HOME PAGE
# ==================================================

if page == "Home":

    st.markdown(
        '<div class="main-title">'
        'Job Offer Investigation Dashboard'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="main-subtitle">'
        'Investigate job offers, examine evidence and review reports.'
        '</div>',
        unsafe_allow_html=True
    )

    investigations = get_investigations()
    all_feedback = feedback_memory.get_all_feedback() or []

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Investigations", len(investigations))

    with col2:
        st.metric("Feedback Records", len(all_feedback))

    with col3:
        st.metric("Investigation Agents", "2")

    st.divider()

    st.markdown("### Welcome")

    st.write(
        """
        JobVerify AI is a multi-agent system designed to help users
        investigate job advertisements and employment offers.

        It analyses submitted job information, gathers available
        verification evidence, checks potential warning signs and
        produces an investigation report.
        """
    )

    st.markdown("### System Features")

    col1, col2 = st.columns(2, gap="large")

    with col1:

        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-title">Job Offer Analysis</div>
                <div class="feature-description">
                    Extracts company name, position, salary,
                    contact details and payment requests.
                </div>
            </div>

            <div class="feature-card">
                <div class="feature-title">Investigation Memory</div>
                <div class="feature-description">
                    Stores previous investigations and feedback
                    to support reflection and future investigations.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-title">Evidence Verification</div>
                <div class="feature-description">
                    Uses web search, website checks, email checks
                    and other investigation tools.
                </div>
            </div>

            <div class="feature-card">
                <div class="feature-title">User Feedback</div>
                <div class="feature-description">
                    Allows users to rate results and provide
                    comments for system evaluation.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    show_assessment_legend()

    st.divider()

    st.markdown("### Recent Investigations")

    if investigations:

        for item in investigations[:5]:

            investigation_id = item.get("id")

            with st.container(border=True):

                col1, col2 = st.columns([4, 1])

                with col1:
                    st.markdown(
                        f"**Investigation #{investigation_id}**"
                    )
                    st.caption(
                        item.get("created_at", "Unknown date")
                    )

                with col2:

                    if st.button(
                        "View",
                        key=f"home_view_{investigation_id}",
                        use_container_width=True
                    ):
                        st.session_state.selected_investigation_id = (
                            investigation_id
                        )
                        st.session_state.navigation = (
                            "Investigation History"
                        )
                        st.rerun()

    else:
        st.info("No investigations have been completed yet.")

    if st.button(
        "Start a New Investigation",
        type="primary",
        use_container_width=True
    ):
        st.session_state.navigation = "New Investigation"
        st.rerun()


# ==================================================
# 9. NEW INVESTIGATION PAGE
# ==================================================

elif page == "New Investigation":

    st.markdown(
        '<div class="main-title">New Job Offer Investigation</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="main-subtitle">'
        'Submit a job advertisement, employment email or offer letter.'
        '</div>',
        unsafe_allow_html=True
    )

    with st.form("investigation_form"):

        job_offer = st.text_area(
            "Paste the complete job offer below",
            height=250,
            placeholder=(
                "Paste the job advertisement, email or offer letter here..."
            ),
            key="job_offer_input"
        )

        submitted = st.form_submit_button(
            "Start Investigation",
            type="primary",
            use_container_width=True
        )

    if submitted:

        if not job_offer.strip():

            st.warning("Please enter a job offer before starting.")

        else:

            try:

                with st.spinner(
                    "The investigation agents are analysing "
                    "and verifying the job offer. Please wait..."
                ):

                    result = investigate_job_offer(job_offer.strip())

                if not isinstance(result, dict):
                    raise ValueError(
                        "The investigation did not return a dictionary."
                    )

                if not result.get("investigation_id"):
                    raise ValueError(
                        "No investigation ID was returned."
                    )

                result["job_offer"] = job_offer.strip()

                st.session_state.latest_result = result

                st.session_state.selected_investigation_id = (
                    result["investigation_id"]
                )

                st.success(
                    f"Investigation completed! "
                    f"ID: #{result['investigation_id']}"
                )

            except Exception as error:

                st.error(
                    "The investigation could not be completed. "
                    "Please check the terminal for details."
                )

                with st.expander("Technical Error Details"):
                    st.exception(error)

    result = st.session_state.latest_result

    if result:
        show_new_investigation_result(result)

    else:
        st.info(
            "Your investigation results will appear here "
            "after you submit a job offer."
        )


# ==================================================
# 10. INVESTIGATION HISTORY PAGE
# ==================================================

elif page == "Investigation History":

    st.markdown(
        '<div class="main-title">Investigation History</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="main-subtitle">'
        'Review previous investigations saved in the database.'
        '</div>',
        unsafe_allow_html=True
    )

    investigations = get_investigations()

    if not investigations:

        st.info("No previous investigations found.")

    else:

        st.metric(
            "Total Saved Investigations",
            len(investigations)
        )

        options = {
            (
                f"Investigation #{item['id']} - "
                f"{item.get('created_at', 'Unknown date')}"
            ): item["id"]
            for item in investigations
        }

        labels = list(options.keys())

        selected_id = st.session_state.selected_investigation_id

        default_index = next(
            (
                index
                for index, label in enumerate(labels)
                if options[label] == selected_id
            ),
            0
        )

        selected_label = st.selectbox(
            "Select an investigation",
            labels,
            index=default_index
        )

        selected_id = options[selected_label]

        st.session_state.selected_investigation_id = selected_id

        selected_record = get_investigation_by_id(selected_id)

        st.divider()

        show_investigation(selected_record)


# ==================================================
# 11. FEEDBACK PAGE
# ==================================================

elif page == "Feedback":

    st.markdown(
        '<div class="main-title">User Feedback</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="main-subtitle">'
        'Evaluate investigation results and provide feedback.'
        '</div>',
        unsafe_allow_html=True
    )

    investigations = get_investigations()

    if not investigations:

        st.info(
            "Complete an investigation before submitting feedback."
        )

    else:

        options = {
            (
                f"Investigation #{item['id']} - "
                f"{item.get('created_at', 'Unknown date')}"
            ): item["id"]
            for item in investigations
        }

        selected_label = st.selectbox(
            "Choose an investigation",
            list(options.keys())
        )

        selected_id = options[selected_label]

        st.divider()

        st.markdown("### Submit Your Feedback")

        with st.form("feedback_form"):

            rating = st.selectbox(
                "How accurate was the investigation?",
                [
                    "correct",
                    "partially_correct",
                    "incorrect"
                ],
                format_func=lambda value: {
                    "correct": "Correct",
                    "partially_correct": "Partially Correct",
                    "incorrect": "Incorrect"
                }[value]
            )

            comment = st.text_area(
                "Comments or suggestions",
                height=120,
                placeholder="Explain your feedback here..."
            )

            submitted = st.form_submit_button(
                "Submit Feedback",
                type="primary",
                use_container_width=True
            )

            if submitted:

                try:

                    feedback_id = feedback_memory.save_feedback(
                        investigation_id=selected_id,
                        rating=rating,
                        comment=comment.strip()
                    )

                    st.success(
                        f"Feedback saved successfully! "
                        f"Feedback ID: {feedback_id}"
                    )

                except Exception as error:

                    st.error("Could not save feedback.")

                    with st.expander("Technical Error Details"):
                        st.exception(error)

        st.divider()

        st.markdown("### Previous Feedback")

        existing_feedback = (
            feedback_memory.get_feedback(selected_id) or []
        )

        if existing_feedback:

            for item in existing_feedback:

                with st.container(border=True):

                    st.markdown(
                        f"**Rating:** {item.get('rating', 'Unknown')}"
                    )

                    st.write(
                        item.get("comment") or "No comment provided."
                    )

                    st.caption(
                        item.get("created_at", "Unknown date")
                    )

        else:

            st.info(
                "No feedback has been submitted for this investigation."
            )
