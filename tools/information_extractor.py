import re


def extract_information(job_offer: str) -> dict:
    """
    Extract factual information from a job offer using Python.
    This function does not make scam or legitimacy decisions.
    """

    result = {
        "salary": [],
        "payment_requests": [],
        "emails": [],
        "phone_numbers": [],
        "dates": []
    }

    if not job_offer:
        return result

    money_pattern = re.compile(
        r'(?<!\w)(?:US\$|USD|Nu\.?|BTN|INR|Rs\.?|[$€£₹])\s*'
        r'\d[\d,]*(?:\.\d{1,2})?'
        r'|\b\d[\d,]*(?:\.\d{1,2})?\s*'
        r'(?:USD|BTN|INR|dollars?|euros?|pounds?)\b',
        re.IGNORECASE
    )

    salary_keywords = [
        "salary", "wage", "stipend",
        "remuneration", "monthly pay",
        "annual pay", "hourly pay"
    ]

    payment_keywords = [
        "registration fee", "training fee",
        "processing fee", "security deposit",
        "application fee", "recruitment fee",
        "upfront fee", "deposit", "fee",
        "payment", "charge"
    ]

    # Split the offer into individual sentences.
    sentences = re.split(r'(?<=[.!?;])\s+', job_offer)

    # Extract and classify monetary amounts.
    for sentence in sentences:

        sentence_lower = sentence.lower()

        salary_positions = [
            sentence_lower.find(keyword)
            for keyword in salary_keywords
            if sentence_lower.find(keyword) != -1
        ]

        payment_positions = [
            sentence_lower.find(keyword)
            for keyword in payment_keywords
            if sentence_lower.find(keyword) != -1
        ]

        for match in money_pattern.finditer(sentence):

            amount = match.group().strip()
            amount_position = match.start()

            salary_distance = min(
                (abs(amount_position - pos) for pos in salary_positions),
                default=float("inf")
            )

            payment_distance = min(
                (abs(amount_position - pos) for pos in payment_positions),
                default=float("inf")
            )

            if salary_distance < payment_distance:
                result["salary"].append(amount)

            elif payment_distance < float("inf"):
                result["payment_requests"].append(amount)

    # Extract email addresses.
    result["emails"] = list(dict.fromkeys(
        re.findall(
            r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',
            job_offer
        )
    ))

    # Extract phone numbers.
    phone_pattern = re.compile(
        r'(?<!\w)\+?\d[\d\s().-]{6,}\d(?!\w)'
    )

    result["phone_numbers"] = list(dict.fromkeys(
        match.group().strip()
        for match in phone_pattern.finditer(job_offer)
    ))

    # Extract dates.
    date_pattern = re.compile(
        r'\b(?:'
        r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}'
        r'|\d{4}-\d{2}-\d{2}'
        r'|\d{1,2}\s+'
        r'(?:January|February|March|April|May|June|July|'
        r'August|September|October|November|December)'
        r'\s+\d{4}'
        r')\b',
        re.IGNORECASE
    )

    result["dates"] = list(dict.fromkeys(
        date_pattern.findall(job_offer)
    ))

    return result