import re

def _split_payment_clauses(text: str) -> list:
    """Split the offer into small clauses for safer keyword detection."""

    clauses = []

    sentences = re.split(
        r"(?<=[.!?])\s+|\n+",
        text
    )

    for sentence in sentences:
        parts = re.split(
            r"\s*(?:,|;|\bbut\b|\bhowever\b|\bwhereas\b|\balthough\b)\s*",
            sentence,
            flags=re.IGNORECASE
        )

        clauses.extend(
            part.strip()
            for part in parts
            if part.strip()
        )

    return clauses


def _is_negative_payment_clause(clause: str) -> bool:
    """Recognize explicit payment denials and uncertain statements."""

    patterns = [
        r"\bno\b.{0,100}\b(?:fee|fees|charge|charges|payment|payments|deposit|deposits)\b",
        r"\b(?:fee|fees|charge|charges|payment|payments|deposit|deposits)\b.{0,45}\b(?:is|are|was|were)?\s*not\s+(?:required|needed|necessary|payable|requested)\b",
        r"\b(?:does|do|did)\s+not\s+(?:require|request|charge|ask for)\b",
        r"\b(?:not required|not needed|not necessary|not payable)\b",
        r"\b(?:free of charge|without (?:any )?(?:fee|charge)|no cost)\b",
        r"\bnot confirmed\b.{0,60}\b(?:fee|charge|payment)\b",
        r"\b(?:fee|charge|payment)\b.{0,60}\bnot confirmed\b",
        r"\b(?:fee|fees|payment|charge)\s*[:=-]\s*(?:none|no|n/?a|not applicable)\b",
    ]

    return any(
        re.search(pattern, clause, re.IGNORECASE)
        for pattern in patterns
    )


def detect_scam_indicators(job_offer: str) -> dict:
    """
    Detect potential job scam indicators using rule-based matching.

    Explicit fee denials are not treated as upfront payment requests.
    Detected indicators are warning signs, not proof of fraud.
    """

    text = job_offer.lower()
    clauses = _split_payment_clauses(text)

    rules = {
        "upfront_payment": {
            "severity": "high",
            "keywords": [
                "registration fee",
                "processing fee",
                "pay before joining",
                "payment to secure",
                "training fee",
                "application fee",
                "deposit required",
                "pay to apply",
                "pay before application",
                "fee before processing",
                "advance payment"
            ]
        },

        "personal_information": {
            "severity": "high",
            "keywords": [
                "send your bank details",
                "credit card details",
                "bank account password",
                "send your passport",
                "send your id",
                "share your banking password",
                "one-time password",
                "otp"
            ]
        },

        "unrealistic_promises": {
            "severity": "medium",
            "keywords": [
                "guaranteed income",
                "earn thousands daily",
                "get rich quickly",
                "instant employment",
                "guaranteed job",
                "earn money without working"
            ]
        },

        "urgency_pressure": {
            "severity": "medium",
            "keywords": [
                "limited time",
                "act immediately",
                "urgent payment",
                "offer expires today",
                "immediate payment",
                "apply immediately or lose",
                "pay now"
            ]
        }
    }

    indicators = []

    for category, rule in rules.items():

        matched = []

        for keyword in rule["keywords"]:

            keyword_found = any(
                keyword in clause
                and not (
                    category == "upfront_payment"
                    and _is_negative_payment_clause(clause)
                )
                for clause in clauses
            )

            if keyword_found:
                matched.append(keyword)

        if matched:
            indicators.append({
                "category": category,
                "severity": rule["severity"],
                "matched_phrases": matched
            })

    return {
        "total_indicators": len(indicators),
        "indicators": indicators,
        "warning": (
            "Detected phrases are potential warning signs. "
            "They do not independently establish fraud."
        )
    }


