from agent import (
    investigate_job_offer,
    get_previous_investigations,
    get_investigation_by_id
)

# Test 1: Retrieve all previous investigations
print("\n========== PREVIOUS INVESTIGATIONS ==========")

investigations = get_previous_investigations()

for item in investigations:
    print("ID:", item["id"])
    print("Job Offer:", item["job_offer"])
    print("Verification:", item["verification"])
    print("-----------------------------------")


# Test 2: Retrieve a specific investigation
if investigations:

    investigation_id = investigations[0]["id"]

    print("\n========== SPECIFIC INVESTIGATION ==========")

    result = get_investigation_by_id(investigation_id)

    print(result)