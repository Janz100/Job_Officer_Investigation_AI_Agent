import streamlit as st

from agent import (
    investigate_job_offer,
    get_previous_investigations,
    get_investigation_by_id
)

from memory.feedback_memory import FeedbackMemory
from memory.long_term_memory import LongTermMemory


# --------------------------------------------------
# 1. APPLICATION CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Job Offer Investigation Agent",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# 2. INITIALIZE MEMORY
# --------------------------------------------------

long_term_memory = LongTermMemory()
feedback_memory = FeedbackMemory()


# --------------------------------------------------
# 3. SESSION STATE
# --------------------------------------------------

if "latest_result" not in st.session_state:
    st.session_state.latest_result = None

if "selected_investigation_id" not in st.session_state:
    st.session_state.selected_investigation_id = None


# --------------------------------------------------
# 4. CUSTOM DESIGN
# --------------------------------------------------

st.markdown("""
<style>
    .main {
        background-color: #f7f9fc;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .main-heading {
        font-size: 30px;
        font-weight: 700;
        color: #17365d;
    }

    .sub-heading {
        font-size: 15px;
        color: #64748b;
    }

    div[data-testid="stMetric"] {
        background-color: white;
        border: 1px solid #e2e8f0;
        padding: 18px;
        border-radius: 10px;
    }

    div.stButton > button {
        border-radius: 8px;
        font-weight: 600;
    }

    section[data-testid="stSidebar"] {
        background-color: #eef3f9;
    }
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# 5. SIDEBAR NAVIGATION
# --------------------------------------------------

with st.sidebar:
    st.title("🔎 JobVerify AI")

    st.caption("Job Offer Investigation and Verification Agent")

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

    st.caption("Multi-agent AI investigation system")
    st.caption("Powered by LangGraph and Ollama")


# --------------------------------------------------
# 6. HELPER FUNCTION
# --------------------------------------------------

def show_investigation(record):
    """Display a saved investigation."""

    if not record:
        st.warning("Investigation not found.")
        return

    st.subheader(f"Investigation #{record['id']}")

    st.caption(f"Created: {record.get('created_at', 'Unknown')}")

    with st.expander("Original Job Offer"):
        st.text(record.get("job_offer") or "No job offer available.")

    st.markdown("### Job Analysis")

    st.text_area(
        "Analysis report",
        value=record.get("analysis") or "No analysis available.",
        height=350,
        disabled=True,
        key=f"analysis_{record['id']}"
    )

    st.markdown("### Verification Report")

    st.text_area(
        "Verification report",
        value=record.get("verification") or "No verification available.",
        height=450,
        disabled=True,
        key=f"verification_{record['id']}"
    )


# --------------------------------------------------
# 7. HOME PAGE
# --------------------------------------------------

if page == "Home":

    st.markdown(
        '<div class="main-heading">Job Offer Investigation Dashboard</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sub-heading">'
        'Investigate job offers, examine evidence and review verification reports.'
        '</div>',
        unsafe_allow_html=True
    )

    st.write("")

    investigations = get_previous_investigations()
    all_feedback = feedback_memory.get_all_feedback()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Investigations",
            len(investigations)
        )

    with col2:
        st.metric(
            "Feedback Records",
            len(all_feedback)
        )

    with col3:
        st.metric(
            "Investigation Agents",
            "2"
        )

    st.divider()

    st.subheader("Welcome")

    st.write(
        """
        This system helps users investigate suspicious job offers
        through a multi-agent AI workflow.

        The system analyses job information, checks available evidence,
        identifies potential warning signs and generates a verification report.
        """
    )

    st.markdown("### Main Features")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🔍 Job Offer Analysis")
        st.write(
            "Extracts important information such as company name, "
            "job position, salary and contact details."
        )

        st.markdown("#### 🌐 Verification")
        st.write(
            "Uses available web, website and email checks "
            "to gather supporting evidence."
        )

    with col2:
        st.markdown("#### 🧠 Memory")
        st.write(
            "Stores previous investigations and reflection lessons "
            "for future investigations."
        )

        st.markdown("#### 📝 User Feedback")
        st.write(
            "Allows users to rate investigation results "
            "and provide comments."
        )

    st.divider()

    if investigations:
        st.subheader("Recent Investigations")

        for item in investigations[:5]:
            with st.container(border=True):
                st.write(f"**Investigation #{item['id']}**")
                st.caption(item.get("created_at", "Unknown date"))

                if st.button(
                    "View Investigation",
                    key=f"home_view_{item['id']}"
                ):
                    st.session_state.selected_investigation_id = item["id"]
                    st.session_state.navigation = "Investigation History"
                    st.rerun()

    else:
        st.info("No investigations have been saved yet.")


# --------------------------------------------------
# 8. NEW INVESTIGATION PAGE
# --------------------------------------------------

elif page == "New Investigation":

    st.title("🔍 New Job Offer Investigation")

    st.write(
        "Paste the complete job offer below. "
        "The AI agents will analyse and verify the available information."
    )

    job_offer = st.text_area(
        "Job Offer Details",
        height=250,
        placeholder=(
            "Paste the job advertisement, email or offer letter here..."
        ),
        key="job_offer_input"
    )

    if st.button(
        "Start Investigation",
        type="primary",
        use_container_width=True
    ):

        if not job_offer.strip():
            st.warning("Please enter a job offer before starting.")

        else:
            try:
                with st.spinner(
                    "The AI agents are investigating the job offer. "
                    "This may take some time..."
                ):

                    result = investigate_job_offer(job_offer.strip())

                st.session_state.latest_result = result
                st.session_state.selected_investigation_id = (
                    result["investigation_id"]
                )

                st.success(
                    f"Investigation completed! "
                    f"ID: {result['investigation_id']}"
                )

            except Exception as error:
                st.error(
                    "The investigation could not be completed. "
                    "Please check the terminal for details."
                )
                st.exception(error)

    # Display results from the completed investigation
    result = st.session_state.latest_result

    if result:

        st.divider()

        st.subheader(
            f"Investigation Results - #{result['investigation_id']}"
        )

        tab1, tab2, tab3 = st.tabs(
            [
                "Job Analysis",
                "Verification",
                "Technical Details"
            ]
        )

        with tab1:
            st.text_area(
                "Job Analysis Report",
                value=result.get("investigation", "No analysis available."),
                height=450,
                disabled=True,
                key=f"new_analysis_{result['investigation_id']}"
            )

        with tab2:
            st.text_area(
                "Verification Report",
                value=result.get("verification", "No verification available."),
                height=500,
                disabled=True,
                key=f"new_verification_{result['investigation_id']}"
            )

        with tab3:
            st.write("**Investigation ID:**", result["investigation_id"])

            st.write("**Website Check:**")
            st.json(result.get("website_check", {}))

            st.write("**Email Check:**")
            st.json(result.get("email_check", {}))

            st.write("**Scam Indicators:**")
            st.json(result.get("scam_indicators", {}))

            st.write("**Web Search Results:**")
            st.json(result.get("web_results", []))

            st.write("**Extracted Information:**")
            st.json(result.get("extracted_information", {}))

        st.info(
            "This investigation has been saved automatically "
            "in the existing SQLite database."
        )


# --------------------------------------------------
# 9. INVESTIGATION HISTORY PAGE
# --------------------------------------------------

elif page == "Investigation History":

    st.title("📚 Investigation History")

    investigations = get_previous_investigations()

    if not investigations:
        st.info("No previous investigations found.")

    else:
        st.write(
            f"Total saved investigations: {len(investigations)}"
        )

        investigation_options = {
            f"Investigation #{item['id']} - {item.get('created_at', '')}":
            item["id"]
            for item in investigations
        }

        labels = list(investigation_options.keys())

        selected_label = st.selectbox(
            "Select an investigation",
            labels,
            index=next(
                (
                    i for i, label in enumerate(labels)
                    if investigation_options[label]
                    == st.session_state.selected_investigation_id
                ),
                0
            )
        )

        selected_id = investigation_options[selected_label]

        st.session_state.selected_investigation_id = selected_id

        selected_record = get_investigation_by_id(selected_id)

        st.divider()

        show_investigation(selected_record)


# --------------------------------------------------
# 10. FEEDBACK PAGE
# --------------------------------------------------

elif page == "Feedback":

    st.title("📝 User Feedback")

    st.write(
        "Your feedback helps evaluate the quality of investigation results."
    )

    investigations = get_previous_investigations()

    if not investigations:
        st.info("Complete an investigation before submitting feedback.")

    else:

        options = {
            f"Investigation #{item['id']} - {item.get('created_at', '')}":
            item["id"]
            for item in investigations
        }

        selected_label = st.selectbox(
            "Choose an investigation",
            list(options.keys())
        )

        selected_id = options[selected_label]

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
                placeholder="Explain your feedback here..."
            )

            submitted = st.form_submit_button(
                "Submit Feedback",
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
                    st.exception(error)

        st.divider()

        st.subheader("Previous Feedback")

        existing_feedback = feedback_memory.get_feedback(selected_id)

        if existing_feedback:

            for item in existing_feedback:
                with st.container(border=True):
                    st.write(f"**Rating:** {item['rating']}")
                    st.write(
                        item.get("comment") or "No comment provided."
                    )
                    st.caption(item.get("created_at", ""))

        else:
            st.info("No feedback has been submitted for this investigation.")
