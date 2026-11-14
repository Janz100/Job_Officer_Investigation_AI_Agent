from agent import investigate_job_offer

job_offer = """
Company: Global Tech Solutions
Position: Remote Data Analyst Intern
Salary: $800 per month
Requirements: Basic Python and SQL skills
Contact: recruitment.globaltech@gmail.com
Application fee: $30
"""

print("\n========== NEW JOB INVESTIGATION ==========")

result = investigate_job_offer(job_offer)

print("\n========== JOB ANALYSIS ==========")
print(result["investigation"])

print("\n========== VERIFICATION RESULT ==========")
print(result["verification"])

print("\nInvestigation ID:", result["investigation_id"])