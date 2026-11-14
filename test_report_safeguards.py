from agents.verification_agent import (
    get_report_section_validation_errors,
    correct_domain_match_claims,
    ensure_registry_limitation
)

# Test 1: All eight sections contain content
report = """
Assessment: Suspicious

Company Identity Verification:
- ABC Technologies is named in the offer.

Email and Domain Verification:
- hr@abctechnologies.com has a valid format.

Website Verification:
- No website was supplied.

Evidence Supporting Credibility:
- No independent credibility evidence was established.

Suspicious Findings:
- A $50 registration fee is requested.

Missing Information:
- Employer identity remains unverified.

Recommended Next Steps:
- Verify the employer independently.

Final Conclusion:
- The offer is suspicious, but fraud is not confirmed.
"""

errors = get_report_section_validation_errors(report)
print("TEST 1 - Section validation:")
print("PASS" if not errors else errors)

# Test 2: Matching domain must not be described as a mismatch
comparison = [
    {"matches_email_domain": True}
]

incorrect_text = (
    "The search results show that the company exists, "
    "but the website does not match the email domain."
)

corrected = correct_domain_match_claims(
    incorrect_text,
    comparison
)

print("\nTEST 2 - Domain wording:")
print(corrected)

# Test 3: Registry limitation must be stated
registry_text = """
Missing Information:
- Employer identity remains unverified.
"""

updated = ensure_registry_limitation(registry_text)

print("\nTEST 3 - Registry limitation:")
print(updated)

print("\nAll safeguard checks completed.")
