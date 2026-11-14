
from llm import get_llm
from memory.long_term_memory import LongTermMemory
from memory.feedback_memory import FeedbackMemory
from memory.reflection_memory import ReflectionMemory


class ReflectionAgent:

    def __init__(self):
        self.llm = get_llm()
        self.long_term_memory = LongTermMemory()
        self.feedback_memory = FeedbackMemory()
        self.reflection_memory = ReflectionMemory()

    def reflect_on_investigation(self, investigation_id):

        # 1. Retrieve previous investigation
        investigation = self.long_term_memory.get_investigation(
            investigation_id
        )

        if investigation is None:
            return "Investigation not found."

        # 2. Retrieve user feedback
        feedback_list = self.feedback_memory.get_feedback(
            investigation_id
        )

        if not feedback_list:
            return "No feedback available for reflection."

        feedback_text = ""

        for feedback in feedback_list:
            feedback_text += f"""
Rating: {feedback.get('rating', 'Not provided')}
Comment: {feedback.get('comment', 'No comment')}
"""

        # 3. Generate reflection using Qwen3
        prompt = f"""
You are a careful Reflection Agent in a Job Offer Investigation System.

Your responsibility is to learn from previous investigations
and user feedback to improve future investigations.

PREVIOUS JOB OFFER:
{investigation['job_offer']}

PREVIOUS ANALYSIS:
{investigation['analysis']}

PREVIOUS VERIFICATION:
{investigation['verification']}

USER FEEDBACK:
{feedback_text}

TASKS:

1. Identify what the investigation did correctly.
2. Identify weaknesses and missing verification steps.
3. Evaluate the user's feedback.
4. Identify mistakes or unsupported conclusions.
5. Suggest improvements for future investigations.
6. Generate clear and reusable lessons for future investigations.

IMPORTANT RULES:

- Never invent statistics, percentages, evidence or facts.
- Never claim an opportunity is definitely fraudulent without
  sufficient supporting evidence.
- An upfront payment request is a serious warning sign,
  but does not independently prove fraud.
- A generic company name does not prove that a company is fake.
- User feedback is an opinion, not automatically verified evidence.
- Separate confirmed facts, warning signs and unknown information.
- Recommend checking official company websites, business
  registrations, contact details and trusted job platforms.
- Do not repeat the same lesson unnecessarily.
- Focus on practical improvements that future agents can apply.
- Keep the reflection concise and useful.
- Limit the reflection to approximately 2500 characters.

OUTPUT FORMAT:

1. What Was Done Correctly:
2. Weaknesses Identified:
3. Feedback Evaluation:
4. Lessons for Future Investigations:
5. Recommended Improvements:

Write in simple, clear English.
"""

        response = self.llm.invoke(prompt)
        reflection = response.content.strip()

        # 4. Save reflection into existing reflection memory
        reflection_id = self.reflection_memory.save_reflection(
            investigation_id=investigation_id,
            reflection=reflection
        )

        print("Reflection saved successfully!")
        print("Investigation ID:", investigation_id)
        print("Reflection ID:", reflection_id)

        return reflection

