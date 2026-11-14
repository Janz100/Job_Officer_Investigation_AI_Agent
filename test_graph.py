from agent import investigate_job_offer

job_offer = """
You have been selected for a Data Analyst Internship
at ABC Technologies.

Monthly salary: $1,500.

To secure your position, please pay $50
for registration and processing fees.

Contact: abctechcareers@gmail.com
"""

result = investigate_job_offer(job_offer)

print("\n========== JOB ANALYSIS ==========\n")
print(result["investigation"])

print("\n========== VERIFICATION ==========\n")
print(result["verification"])

print("\n========== WORKFLOW COMPLETED ==========\n")
print("Saved Investigation ID:", result["investigation_id"])