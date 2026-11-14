from agents.job_analysis_agent import job_analysis_agent
from agents.verification_agent import verification_agent


job_offer = """
Congratulations!

You have been selected for a Data Analyst Internship
at ABC Technologies.

Monthly salary: $1,500.

To secure your position, please pay $50
for registration and processing fees.

Contact: abctechcareers@gmail.com
"""


# Agent 1: Analyse the job offer
print("\n========== AGENT 1: JOB ANALYSIS ==========\n")

state = {
    "job_offer": job_offer
}

analysis_result = job_analysis_agent(state)

print(analysis_result["investigation"])


# Pass Agent 1 results to Agent 2
state.update(analysis_result)


# Agent 2: Verify the job offer
print("\n========== AGENT 2: VERIFICATION ==========\n")

verification_result = verification_agent(state)

print(verification_result["verification"])


print("\n========== INVESTIGATION COMPLETED ==========\n")
