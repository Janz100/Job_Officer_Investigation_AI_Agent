
from memory.feedback_memory import FeedbackMemory

# Initialize feedback memory
feedback_memory = FeedbackMemory()

# Test saving feedback
feedback_id = feedback_memory.save_feedback(
    investigation_id=1,
    rating="correct",
    comment="The agent correctly identified the upfront payment warning."
)

print("Feedback saved successfully!")
print("Feedback ID:", feedback_id)


# Test retrieving feedback
print("\n========== RETRIEVED FEEDBACK ==========")

feedback = feedback_memory.get_feedback(1)

for item in feedback:
    print("Feedback ID:", item["id"])
    print("Investigation ID:", item["investigation_id"])
    print("Rating:", item["rating"])
    print("Comment:", item["comment"])
    print("Date:", item["created_at"])
    print("-----------------------------------")
