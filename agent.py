
from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from agents.job_analysis_agent import job_analysis_agent
from agents.verification_agent import verification_agent

from memory.long_term_memory import LongTermMemory
from memory.reflection_memory import ReflectionMemory


# Initialize memory systems
long_term_memory = LongTermMemory()
reflection_memory = ReflectionMemory()


# 1. Define the shared state
class InvestigationState(TypedDict, total=False):

    job_offer: str
    previous_lessons: str

    investigation: str
    verification: str

    # Information extracted using Python
    extracted_information: dict

    # Verification results
    web_results: list
    website_check: dict
    email_check: dict
    scam_indicators: dict


# 2. Retrieve previous lessons from reflection memory
def retrieve_previous_lessons():

    reflections = reflection_memory.get_all_reflections()

    if not reflections:
        return "No previous investigation lessons available."

    lessons = []
    seen_investigations = set()

    for reflection in reflections:

        investigation_id = reflection["investigation_id"]

        # Skip investigations already processed
        if investigation_id in seen_investigations:
            continue

        seen_investigations.add(investigation_id)

        lesson = reflection["reflection"].strip()

        # Limit each reflection to 3000 characters
        lesson = lesson[:3000]

        lessons.append(
            f"Investigation {investigation_id}:\n{lesson}"
        )

        # Maximum of three unique investigations
        if len(lessons) >= 3:
            break

    return "\n\n".join(lessons)


# 3. Create the LangGraph workflow
def create_investigation_graph():

    workflow = StateGraph(InvestigationState)

    # Register agents as workflow nodes
    workflow.add_node("job_analysis", job_analysis_agent)
    workflow.add_node("verification", verification_agent)

    # Define execution order
    workflow.add_edge(START, "job_analysis")
    workflow.add_edge("job_analysis", "verification")
    workflow.add_edge("verification", END)

    return workflow.compile()


# 4. Create the application
investigation_app = create_investigation_graph()


# 5. Run a new investigation
def investigate_job_offer(job_offer: str):

    # Retrieve previous lessons before investigation
    previous_lessons = retrieve_previous_lessons()

    initial_state = {
        "job_offer": job_offer,
        "previous_lessons": previous_lessons
    }

    # Execute both agents through LangGraph
    result = investigation_app.invoke(initial_state)

    # Save investigation into long-term memory
    investigation_id = long_term_memory.save_investigation(
        job_offer=job_offer,
        analysis=result["investigation"],
        verification=result["verification"]
    )

    result["investigation_id"] = investigation_id

    return result


# 6. Retrieve all previous investigations
def get_previous_investigations():

    return long_term_memory.get_all_investigations()


# 7. Retrieve a specific investigation
def get_investigation_by_id(investigation_id):

    return long_term_memory.get_investigation(investigation_id)
