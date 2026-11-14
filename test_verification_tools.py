
from tools.web_search import search_web
from tools.website_checker import check_website
from tools.email_checker import check_email
from tools.scam_detector import detect_scam_indicators


job_offer = """
ABC Technologies is hiring a Data Analyst Intern.
Contact: hr@abctechnologies.com.
Applicants must pay a $50 registration fee.
"""


print("\n========== TESTING VERIFICATION TOOLS ==========")

# 1. Web search
print("\n1. WEB SEARCH")
search_results = search_web(
    "ABC Technologies official company website",
    max_results=2
)
print("Results:", search_results)

# 2. Website checker
print("\n2. WEBSITE CHECKER")
website_result = check_website("https://www.google.com")
print("Result:", website_result)

# 3. Email checker
print("\n3. EMAIL CHECKER")
email_result = check_email("hr@abctechnologies.com")
print("Result:", email_result)

# 4. Scam detector
print("\n4. SCAM DETECTOR")
scam_result = detect_scam_indicators(job_offer)
print("Result:", scam_result)

print("\n========== TOOL TEST COMPLETED ==========")
