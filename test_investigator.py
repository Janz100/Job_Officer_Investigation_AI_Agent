from agents.job_analysis_agent import job_analysis_agent

test_state = {
    "job_offer": """
    Congratulations!

    You have been selected for a Data Analyst Internship
    at ABC Technologies.

    Monthly salary: $1,500

    To secure your position, please pay $50
    for registration and processing fees.

    Contact: abctechcareers@gmail.com
    """
}

result = job_analysis_agent(test_state)

print("\n===== JOB ANALYSIS RESULTS =====\n")
print(result["investigation"])
