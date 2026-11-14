
from agent import investigate_job_offer

job_offer = """
ABC Digital Solutions is offering a Junior Data Analyst position.

The position is based in Singapore.

Monthly salary: SGD 3,500.

Applicants must submit their CV and academic certificates.

Applications should be submitted through the company's
official recruitment website.

Contact: careers@abcdigital.example

No application or registration fee is required.

The company will conduct an interview before selecting
the successful candidate.
"""

print("\n========== TESTING LEGITIMATE JOB OFFER ==========\n")

result = investigate_job_offer(job_offer)

print("\n--- JOB ANALYSIS ---")
print(result["investigation"])

print("\n--- VERIFICATION ---")
print(result["verification"])

print("\n--- INVESTIGATION ID ---")
print(result["investigation_id"])

print("\n========== TEST COMPLETED ==========")
