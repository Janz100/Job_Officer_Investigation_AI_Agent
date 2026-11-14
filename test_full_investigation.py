
from agent import investigate_job_offer

print("\n========== TESTING FULL INVESTIGATION SYSTEM ==========\n")

job_offer = """
ABC Technologies is offering a Data Analyst Internship.

Monthly salary: $800.

Applicants must submit their CV and academic certificates.

Contact: hr@abctechnologies.com

The company requests a $50 registration fee before
the internship application can be processed.
"""

print("NEW JOB OFFER:")
print(job_offer)

print("\n========== STARTING INVESTIGATION ==========\n")

result = investigate_job_offer(job_offer)

print("\n========== INVESTIGATION RESULTS ==========\n")

print("\n--- JOB ANALYSIS ---")
print(result["investigation"])

print("\n--- VERIFICATION ---")
print(result["verification"])

print("\n--- PREVIOUS LESSONS ---")
print(result.get("previous_lessons", "Not returned in result"))

print("\n--- INVESTIGATION ID ---")
print(result["investigation_id"])

print("\n========== TEST COMPLETED ==========")
