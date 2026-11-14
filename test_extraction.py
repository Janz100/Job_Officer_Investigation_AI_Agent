
import re

# Sample job analysis output
investigation = """
**1. Company name**
ABC Technologies

**2. Job or internship position**
Data Analyst Internship
"""

# Sample job offer
job_offer = """
ABC Technologies is hiring a Data Analyst Intern.
Contact: hr@abctechnologies.com
"""

# Extract company name
company_name = ""

lines = investigation.splitlines()

for i, line in enumerate(lines):

    cleaned_line = re.sub(r"\*", "", line).strip()

    match = re.match(
        r"^(?:\d+\.\s*)?Company\s+name\s*:?\s*(.*)$",
        cleaned_line,
        re.IGNORECASE
    )

    if match:

        company_name = match.group(1).strip()

        if not company_name:

            for next_line in lines[i + 1:]:

                candidate = next_line.strip().strip("*# ")

                if not candidate:
                    continue

                if re.match(
                    r"^(?:\d+\.\s*)?(Job or internship position|Salary and benefits|Contact information|Application requirements)",
                    candidate,
                    re.IGNORECASE
                ):
                    break

                company_name = candidate
                break

        break

# Extract email
email_match = re.search(
    r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
    job_offer
)

email_address = (
    email_match.group(0).lower()
    if email_match
    else ""
)

print("========== EXTRACTION TEST ==========")
print("Company name:", company_name)
print("Email address:", email_address)
print("=====================================")
