from tools.scam_detector import detect_scam_indicators

job_offer = """
Congratulations!

You have been selected for a Data Analyst Internship
at ABC Technologies.

Monthly salary: $1,500.

Pay $50 registration and processing fee
to secure your position.

Limited time offer. Pay immediately.
"""

result = detect_scam_indicators(job_offer)

print("\n===== SCAM INDICATOR RESULTS =====\n")

print("Total indicators:", result["total_indicators"])

for indicator in result["indicators"]:
    print("\nCategory:", indicator["category"])
    print("Matched phrases:", indicator["matched_phrases"])
