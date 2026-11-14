
from memory.long_term_memory import LongTermMemory

memory = LongTermMemory()

# Sample investigation
job_offer = "Data Analyst Internship at ABC Technologies. Pay $50 registration fee."

analysis = "Company: ABC Technologies. Position: Data Analyst Internship."

verification = "Assessment: Suspicious due to upfront payment request."

# Save investigation
investigation_id = memory.save_investigation(
    job_offer,
    analysis,
    verification
)

print("Investigation saved successfully!")
print("Investigation ID:", investigation_id)

# Retrieve saved investigation
result = memory.get_investigation(investigation_id)

print("\n========== RETRIEVED MEMORY ==========")

print("Job Offer:", result["job_offer"])
print("Analysis:", result["analysis"])
print("Verification:", result["verification"])

# Display all saved investigations
print("\n========== INVESTIGATION HISTORY ==========")

for item in memory.get_all_investigations():
    print(item["id"], item["verification"])

