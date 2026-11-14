
from agents.verification_agent import (
    has_explicit_fee_request,
    extract_fee_categories,
    extract_fee_details,
)
from agents.job_analysis_agent import extract_payment_requests
from tools.scam_detector import detect_scam_indicators


def run_test(name, offer, expected_fee, expected_categories):
    detected = has_explicit_fee_request(offer)
    categories = extract_fee_categories(offer)
    amounts = extract_fee_details(offer)
    payments = extract_payment_requests(offer)
    scam = detect_scam_indicators(offer)

    upfront_detected = any(
        item.get("category") == "upfront_payment"
        for item in scam.get("indicators", [])
    )

    passed = (
        detected == expected_fee
        and categories == expected_categories
        and upfront_detected == expected_fee
        and bool(payments) == expected_fee
    )

    print(f"\n{name}: {'PASS' if passed else 'FAIL'}")
    print("Fee detected:", detected)
    print("Categories:", categories)
    print("Amounts:", amounts)
    print("Payment requests:", payments)
    print("Upfront payment indicator:", upfront_detected)

    if not passed:
        raise AssertionError(f"{name} failed")


run_test(
    "TEST 1 - Explicit fee denial",
    "No application or registration fee is required.",
    False,
    []
)

run_test(
    "TEST 2 - Positive registration fee",
    "Applicants must pay a $50 registration fee before processing.",
    True,
    ["registration"]
)

run_test(
    "TEST 3 - Positive training fee",
    "A $100 training fee is required before joining.",
    True,
    ["training"]
)

run_test(
    "TEST 4 - Employer does not require application fee",
    "The employer does not require an application fee.",
    False,
    []
)

run_test(
    "TEST 5 - Free application",
    "There is no fee to apply.",
    False,
    []
)

run_test(
    "TEST 6 - Unconfirmed training fee",
    "The employer has not confirmed whether a training fee applies.",
    False,
    []
)

run_test(
    "TEST 7 - Mixed negative and positive fees",
    "No application fee is required, but applicants must pay a $50 registration fee.",
    True,
    ["registration"]
)

print("\nAll fee detection tests passed.")
