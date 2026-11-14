
import re

from llm import get_llm
from tools.information_extractor import extract_information


llm = get_llm()


# ==================================================
# 1. MONETARY AMOUNT EXTRACTION
# ==================================================

def extract_money_amounts(text: str) -> set:
    """
    Extract monetary amounts without assuming a currency
    that was not specified in the original offer.
    """

    if not isinstance(text, str):
        return set()

    pattern = (
        r"(?:[$€£]\s*|\b(?:USD|EUR|GBP|BTN|INR)\s*)"
        r"(\d[\d,]*(?:\.\d+)?)"
        r"|"
        r"\b(\d[\d,]*(?:\.\d+)?)\s*"
        r"(?:USD|EUR|GBP|BTN|INR)\b"
    )

    amounts = set()

    for match in re.finditer(pattern, text, re.IGNORECASE):
        amount = match.group(1) or match.group(2)

        if amount:
            amounts.add(amount.replace(",", ""))

    return amounts


def find_unsupported_amounts(
    generated_report: str,
    original_offer: str
) -> set:

    original_amounts = extract_money_amounts(original_offer)
    generated_amounts = extract_money_amounts(generated_report)

    return generated_amounts - original_amounts


def remove_unsupported_amount_lines(
    report: str,
    unsupported_amounts: set
) -> str:

    if not unsupported_amounts:
        return report

    cleaned_lines = []

    for line in report.splitlines():

        line_amounts = extract_money_amounts(line)

        if line_amounts.intersection(unsupported_amounts):
            continue

        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


# ==================================================
# 2. COMPANY REGISTRATION SAFEGUARDS
# ==================================================

def remove_unsupported_registry_claims(report: str) -> str:
    """
    Remove unsupported statements about company registration.

    This agent does not perform official registry checks.
    Applicant registration-fee information must be preserved.
    """

    if not isinstance(report, str):
        return report

    registry_patterns = [
        r"\babsence of (?:any )?(?:an? )?(?:official )?(?:company|business)?\s*registrations?\b",
        r"\black of (?:any )?(?:an? )?(?:official )?(?:company|business)?\s*registrations?\b",
        r"\bno (?:official )?(?:company|business)?\s*registration records?\b",
        r"\bno evidence (?:that|of) (?:the )?(?:company|business) is registered\b",
        r"\bno proof (?:that|of) (?:the )?(?:company|business) is registered\b",
        r"\bnot officially registered\b",
        r"\bunregistered company\b",
        r"\bcompany is unregistered\b",
        r"\bcompany has not been registered\b",
        r"\bcompany registration does not exist\b",
        r"\bcompany is not legally registered\b",
        r"\bregistration status (?:is|was) unknown\b",
        r"\bregistration status could not be (?:confirmed|verified|established)\b",
        r"\bcompany registration (?:was|has been) not verified\b",
        r"\bcompany registration (?:was|has been) not checked\b",
        r"\bcompany registration could not be verified\b",
        r"\bcompany registration information (?:is|was) unavailable\b",
        r"\bregistration evidence (?:is|was) (?:missing|unavailable|absent)\b",
        r"\bregistration records? (?:could not|couldn't) be found\b",
        r"\babsence of registration evidence\b",
        r"\black of registration evidence\b",
        r"\bno registration evidence\b",
        r"\bregistration information (?:is|was) missing\b",
        r"\bregistration details (?:are|were) unavailable\b",
        r"\bnot registered with (?:the )?(?:relevant )?authorit(?:y|ies)\b",
    ]

    combined_pattern = re.compile(
        "|".join(registry_patterns),
        re.IGNORECASE
    )

    cleaned_lines = []

    for line in report.splitlines():

        lower_line = line.lower()

        is_payment_line = re.search(
            r"\b(?:registration|application|processing|training|recruitment)"
            r"\s+(?:fee|charge|payment)\b",
            lower_line
        )

        if is_payment_line:
            cleaned_lines.append(line)
            continue

        if combined_pattern.search(line):
            continue

        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


# ==================================================
# 3. REPORT SECTION HELPERS
# ==================================================

def split_report_sections(report: str) -> list:
    """
    Split the report into its eight numbered sections.
    """

    lines = report.splitlines()
    sections = []
    current_section = []

    heading_pattern = re.compile(
        r"^\s*\*{0,2}\s*\d+\s*[\.\)]\s+"
        r"(COMPANY INFORMATION|JOB INFORMATION|CONTACT INFORMATION|"
        r"APPLICATION REQUIREMENTS|PAYMENT REQUESTS|"
        r"POTENTIAL WARNING SIGNS|MISSING INFORMATION|"
        r"INITIAL OBSERVATIONS)\b",
        re.IGNORECASE
    )

    for line in lines:

        if heading_pattern.match(line):

            if current_section:
                sections.append(current_section)

            current_section = [line]

        elif current_section:
            current_section.append(line)

        else:
            if not sections:
                sections.append([line])

    if current_section:
        sections.append(current_section)

    return sections



def clean_unmentioned_payment_categories(
    section_lines: list,
    original_offer: str,
    section_name: str
) -> list:
    """Remove payment categories not supported by positive offer evidence."""

    positive_payment_text = " ".join(
        extract_payment_requests(original_offer)
    ).lower()

    cleaned_lines = []

    fee_categories = {
        "training fees": [
            "training fee",
            "training fees",
            "training charge",
            "training charges",
        ],
        "security deposits": [
            "security deposit",
            "security deposits",
        ],
        "processing fees": [
            "processing fee",
            "processing fees",
            "processing charge",
            "processing charges",
        ],
        "other upfront payment requests": [
            "other upfront payment",
            "other upfront payments",
        ],
    }

    for line in section_lines:

        lower_line = line.lower()
        matched_category = None

        for category, phrases in fee_categories.items():

            if any(phrase in lower_line for phrase in phrases):
                matched_category = category
                break

        if matched_category:

            category_phrases = fee_categories[matched_category]

            supported_by_offer = any(
                phrase in positive_payment_text
                for phrase in category_phrases
            )

            if not supported_by_offer:
                continue

        cleaned_lines.append(line)

    return cleaned_lines

def clean_educational_qualifications(
    section_lines: list,
    original_offer: str
) -> list:

    cleaned_lines = []

    offer_lower = original_offer.lower()

    qualification_terms = [
        "bachelor",
        "bachelors",
        "master",
        "masters",
        "degree",
        "diploma",
        "phd",
        "doctorate",
        "higher secondary",
        "high school qualification",
        "educational qualification",
        "minimum qualification",
    ]

    actual_qualification_mentioned = any(
        term in offer_lower
        for term in qualification_terms
    )

    for line in section_lines:

        lower_line = line.lower()

        is_qualification_line = (
            "educational qualifications:" in lower_line
            or "educational qualification:" in lower_line
        )

        if is_qualification_line and not actual_qualification_mentioned:

            prefix = line.split(":", 1)[0]

            cleaned_lines.append(
                f"{prefix}: Not provided"
            )

        else:
            cleaned_lines.append(line)

    return cleaned_lines


def clean_missing_information(
    section_lines: list,
    original_offer: str
) -> list:

    cleaned_lines = []

    excluded_terms = [
        "company registration status",
        "company registration information",
        "business registration status",
        "registration records",
        "official business registration",
        "training fees",
        "training fee",
        "security deposits",
        "security deposit",
        "processing fees",
        "processing fee",
        "other upfront payment requests",
    ]

    for line in section_lines:

        lower_line = line.lower()

        if any(term in lower_line for term in excluded_terms):
            continue

        cleaned_lines.append(line)

    return cleaned_lines


def clean_initial_observations(
    section_lines: list
) -> list:

    cleaned_lines = []

    excluded_phrases = [
        "company registration status",
        "company registration was not verified",
        "company registration was not checked",
        "company registration remains unverified",
        "business registration status",
        "official business registration",
    ]

    for line in section_lines:

        lower_line = line.lower()

        if any(phrase in lower_line for phrase in excluded_phrases):
            continue

        cleaned_lines.append(line)

    return cleaned_lines


def apply_report_cleanup(
    report: str,
    original_offer: str
) -> str:

    sections = split_report_sections(report)
    cleaned_sections = []

    for section_lines in sections:

        if not section_lines:
            continue

        heading = section_lines[0].lower()

        if "payment requests" in heading:

            section_lines = clean_unmentioned_payment_categories(
                section_lines,
                original_offer,
                "PAYMENT REQUESTS"
            )

        elif "missing information" in heading:

            section_lines = clean_missing_information(
                section_lines,
                original_offer
            )

        elif "application requirements" in heading:

            section_lines = clean_educational_qualifications(
                section_lines,
                original_offer
            )

        elif "initial observations" in heading:

            section_lines = clean_initial_observations(
                section_lines
            )

        cleaned_sections.append("\n".join(section_lines))

    return "\n".join(cleaned_sections)


# ==================================================
# 4. REPORT COMPLETENESS CHECK
# ==================================================

def report_has_all_sections(report: str) -> bool:
    """
    Check whether the LLM has actually generated all eight sections.
    """

    required_headings = [
        "COMPANY INFORMATION",
        "JOB INFORMATION",
        "CONTACT INFORMATION",
        "APPLICATION REQUIREMENTS",
        "PAYMENT REQUESTS",
        "POTENTIAL WARNING SIGNS",
        "MISSING INFORMATION",
        "INITIAL OBSERVATIONS",
    ]

    for heading in required_headings:

        pattern = (
            r"^\s*\*{0,2}\s*\d+\s*[\.\)]\s*"
            + re.escape(heading)
            + r"\b"
        )

        if not re.search(
            pattern,
            report,
            re.IGNORECASE | re.MULTILINE
        ):
            return False

    return True


def report_contains_original_facts(
    report: str,
    original_offer: str
) -> bool:
    """
    Check whether important identifiable facts from the offer
    appear in the generated report.

    This prevents a report with eight empty headings from
    being accepted as complete.
    """

    original_lower = original_offer.lower()
    report_lower = report.lower()

    # Check email addresses.
    original_emails = re.findall(
        r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",
        original_offer,
        re.IGNORECASE
    )

    for email in original_emails:

        if email.lower() not in report_lower:
            return False

    # Check monetary amounts.
    original_amounts = extract_money_amounts(original_offer)
    report_amounts = extract_money_amounts(report)

    if not original_amounts.issubset(report_amounts):
        return False

    # Check important document references.
    document_terms = [
        "cv",
        "resume",
        "academic certificate",
        "academic certificates",
        "transcript",
        "portfolio",
    ]

    for term in document_terms:

        if term in original_lower and term not in report_lower:
            return False

    return True


def is_report_complete(
    report: str,
    original_offer: str
) -> bool:
    """
    Validate the report before passing it to Verification Agent.
    """

    if not isinstance(report, str) or len(report.strip()) < 100:
        return False

    if not report_has_all_sections(report):
        return False

    if not report_contains_original_facts(
        report,
        original_offer
    ):
        return False

    return True


# ==================================================
# 5. DETERMINISTIC EXTRACTION HELPERS
# ==================================================

def normalize_offer_text(text: str) -> str:
    """
    Normalize whitespace while preserving the original wording.
    """

    return re.sub(r"\s+", " ", text).strip()


def extract_sentences(text: str) -> list:
    """
    Split an offer into readable sentences.
    """

    normalized = normalize_offer_text(text)

    if not normalized:
        return []

    return re.split(r"(?<=[.!?])\s+", normalized)


def extract_company_name(original_offer: str) -> str:
    """
    Extract a company name from common offer wording.

    Example:
    ABC Technologies is offering a Data Analyst Internship.
    """

    patterns = [
        r"^\s*(.{2,100}?)\s+is offering\b",
        r"\bposition\s+(?:at|with)\s+(.{2,100}?)(?:[.,;\n]|$)",
        r"\bcompany\s*:\s*(.{2,100}?)(?:[.,;\n]|$)",
        r"\bemployer\s*:\s*(.{2,100}?)(?:[.,;\n]|$)",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            original_offer,
            re.IGNORECASE | re.MULTILINE
        )

        if match:

            value = match.group(1).strip(" \t.,;:")

            if value:
                return value

    return "Not provided"


def extract_job_title(original_offer: str) -> str:
    """
    Extract the role from common job-offer wording.
    """

    patterns = [
        r"\bis offering\s+(?:an?|the)\s+(.+?)(?:[.!?;\n]|$)",
        r"\bposition\s*:\s*(.+?)(?:[.!?;\n]|$)",
        r"\bjob title\s*:\s*(.+?)(?:[.!?;\n]|$)",
        r"\brole\s*:\s*(.+?)(?:[.!?;\n]|$)",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            original_offer,
            re.IGNORECASE
        )

        if match:
            return match.group(1).strip(" \t.,;:")

    return "Not provided"


def extract_salary_detail(original_offer: str) -> str:
    """
    Extract the complete salary-related statement.

    The original wording is preserved to avoid changing
    the currency or payment frequency.
    """

    for sentence in extract_sentences(original_offer):

        if re.search(
            r"\b(salary|stipend|compensation|remuneration|pay)\b",
            sentence,
            re.IGNORECASE
        ):
            return sentence.strip()

    return "Not provided"


def extract_contact_details(original_offer: str) -> tuple:
    """
    Extract email addresses and phone numbers.
    """

    emails = re.findall(
        r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",
        original_offer,
        re.IGNORECASE
    )

    phone_numbers = re.findall(
        r"(?<!\w)(?:\+?\d[\d\s().-]{6,}\d)(?!\w)",
        original_offer
    )

    email_text = (
        ", ".join(dict.fromkeys(emails))
        if emails
        else "Not provided"
    )

    phone_text = (
        ", ".join(dict.fromkeys(
            number.strip() for number in phone_numbers
        ))
        if phone_numbers
        else "Not provided"
    )

    return email_text, phone_text


def extract_document_requirements(original_offer: str) -> str:
    """
    Extract sentences that explicitly mention application documents.
    """

    document_terms = [
        "cv",
        "resume",
        "academic certificate",
        "academic certificates",
        "transcript",
        "portfolio",
        "cover letter",
        "recommendation letter",
    ]

    matching_sentences = []

    for sentence in extract_sentences(original_offer):

        lower_sentence = sentence.lower()

        if any(term in lower_sentence for term in document_terms):
            matching_sentences.append(sentence)

    if matching_sentences:
        return " ".join(dict.fromkeys(matching_sentences))

    return "Not provided"


def extract_application_procedure(original_offer: str) -> str:
    """
    Extract an explicitly stated application procedure.
    """

    matching_sentences = []

    procedure_terms = [
        "apply",
        "application",
        "submit",
        "send your",
        "send the",
        "email your",
        "email the",
    ]

    for sentence in extract_sentences(original_offer):

        lower_sentence = sentence.lower()

        if any(term in lower_sentence for term in procedure_terms):
            matching_sentences.append(sentence)

    if matching_sentences:
        return " ".join(dict.fromkeys(matching_sentences))

    return "Not provided"



def _split_payment_clauses(text: str) -> list:
    """Split text into small clauses for payment detection."""

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
    """Identify statements denying or not confirming a payment."""

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


def _has_positive_payment_signal(clause: str) -> bool:
    """Check for an actual amount or payment requirement."""

    has_amount = re.search(
        r"(?:[$£€]\s*\d|\b\d+(?:[.,]\d{1,2})?\s*(?:USD|EUR|GBP|BTN|Nu\.?)\b)",
        clause,
        re.IGNORECASE
    )

    has_payment_action = re.search(
        r"\b(?:must|have to|need to|required to|pay|paid|payable|charged|charge|deposit|transfer|send|remit|submit|applies|due)\b",
        clause,
        re.IGNORECASE
    )

    return bool(has_amount or has_payment_action)


def extract_payment_requests(original_offer: str) -> list:
    """
    Extract sentences containing actual payment requests.

    Explicit fee denials and uncertain statements are not
    treated as payment requests.
    """

    payment_terms = re.compile(
        r"\b(?:fee|fees|payment|payments|pay|deposit|deposits|charge|charges)\b",
        re.IGNORECASE
    )

    matching_sentences = []

    sentences = re.split(
        r"(?<=[.!?])\s+|\n+",
        original_offer
    )

    for sentence in sentences:

        if not payment_terms.search(sentence):
            continue

        clauses = _split_payment_clauses(sentence)

        has_positive_request = any(
            not _is_negative_payment_clause(clause)
            and payment_terms.search(clause)
            and _has_positive_payment_signal(clause)
            for clause in clauses
        )

        if has_positive_request:
            matching_sentences.append(sentence.strip())

    return list(dict.fromkeys(matching_sentences))

def build_deterministic_report(
    original_offer: str,
    extracted_info: dict
) -> str:
    """
    Create all eight report sections directly from the original offer.

    This fallback is used only when the LLM response is incomplete
    or fails the report completeness checks.

    It does not make a final scam decision.
    """

    company = extract_company_name(original_offer)
    position = extract_job_title(original_offer)
    salary = extract_salary_detail(original_offer)

    email, phone = extract_contact_details(original_offer)

    documents = extract_document_requirements(original_offer)
    application_procedure = extract_application_procedure(original_offer)

    payments = extract_payment_requests(original_offer)

    # --------------------------------------------------
    # Company information
    # --------------------------------------------------

    company_section = [
        "1. COMPANY INFORMATION",
        f"- Company name: {company}",
        "- Company location: Not provided",
        "- Company website: Not provided",
        "- Other company details: Not provided",
    ]

    # --------------------------------------------------
    # Job information
    # --------------------------------------------------

    job_section = [
        "",
        "2. JOB INFORMATION",
        f"- Job or internship position: {position}",
        f"- Salary: {salary}",
        "- Currency: Not separately specified unless stated in the salary description",
        "- Payment frequency: Not provided unless stated in the salary description",
        "- Job responsibilities: Not provided",
        "- Employment type: Not provided separately",
        "- Benefits: Not provided",
        "- Skills or other requirements: Not provided",
    ]

    # --------------------------------------------------
    # Contact information
    # --------------------------------------------------

    contact_section = [
        "",
        "3. CONTACT INFORMATION",
        f"- Email address: {email}",
        f"- Phone number: {phone}",
        "- Contact person's name: Not provided",
        "- Other communication channels: Not provided",
    ]

    # --------------------------------------------------
    # Application requirements
    # --------------------------------------------------

    application_section = [
        "",
        "4. APPLICATION REQUIREMENTS",
        "- Educational qualifications: Not provided",
        f"- Required documents: {documents}",
        "- Experience requirements: Not provided",
        f"- Application procedure: {application_procedure}",
        "- Application deadline: Not provided",
    ]

    # --------------------------------------------------
    # Payment requests
    # --------------------------------------------------

    payment_section = [
        "",
        "5. PAYMENT REQUESTS",
    ]

    if payments:

        for payment in payments:
            payment_section.append(f"- {payment}")

    else:

        payment_section.append(
            "- No payment request identified in the provided offer."
        )

    # --------------------------------------------------
    # Potential warning signs
    # --------------------------------------------------

    warning_section = [
        "",
        "6. POTENTIAL WARNING SIGNS",
    ]

    if payments:

        for payment in payments:

            warning_section.append(
                f"- Evidence: {payment}"
            )

            warning_section.append(
                "- Why it may be concerning: Requests for upfront "
                "payments during recruitment require careful checking."
            )

            warning_section.append(
                "- Potential risk: The applicant may lose money "
                "if the request is not legitimate."
            )

    else:

        warning_section.append(
            "- No payment-related warning sign was identified "
            "from the extracted offer text."
        )

    # --------------------------------------------------
    # Missing information
    # --------------------------------------------------

    missing_section = [
        "",
        "7. MISSING INFORMATION",
    ]

    missing_fields = [
        ("Company location", "location"),
        ("Company website", "website"),
        ("Contact phone number", "phone"),
        ("Application deadline", "deadline"),
        ("Job responsibilities", "responsibilities"),
        ("Experience requirements", "experience"),
        ("Interview procedure", "interview"),
    ]

    offer_lower = original_offer.lower()

    for label, keyword in missing_fields:

        if keyword not in offer_lower:
            missing_section.append(f"- {label}: Not provided")

    if len(missing_section) == 2:
        missing_section.append(
            "- No additional missing information identified by this fallback."
        )

    # --------------------------------------------------
    # Initial observations
    # --------------------------------------------------

    observations = [
        "",
        "8. INITIAL OBSERVATIONS",
        f"- Company stated in the offer: {company}",
        f"- Position stated in the offer: {position}",
        f"- Salary information: {salary}",
        f"- Contact email: {email}",
        f"- Required documents: {documents}",
    ]

    if payments:

        observations.append(
            "- The offer includes a payment request that requires "
            "further verification."
        )

    else:

        observations.append(
            "- No payment request was identified in the offer."
        )

    observations.append(
        "- External verification is required before relying "
        "on the employer's claims."
    )

    report_sections = (
        company_section
        + job_section
        + contact_section
        + application_section
        + payment_section
        + warning_section
        + missing_section
        + observations
    )

    return "\n".join(report_sections)


# ==================================================
# 7. MAIN JOB ANALYSIS AGENT
# ==================================================

def job_analysis_agent(state: dict) -> dict:
    """
    Analyze the original job offer.

    Responsibilities:
    - Extract factual information.
    - Identify actual payment requests.
    - Identify potential warning signs.
    - Identify genuinely missing information.

    This agent does not make the final scam decision.
    """

    job_offer = state.get("job_offer", "")

    if not isinstance(job_offer, str):
        job_offer = str(job_offer)

    previous_lessons = state.get("previous_lessons", "")

    # --------------------------------------------------
    # Extract information using Python
    # --------------------------------------------------

    extracted_info = extract_information(job_offer)

    # --------------------------------------------------
    # LLM analysis prompt
    # --------------------------------------------------

    prompt = f"""
/no_think

You are a Job Offer Analysis Agent.

Analyze the original job offer and produce a factual report
for a separate Verification Agent.

IMPORTANT REPORT TITLE RULE:
- The first line MUST be: JOB ANALYSIS REPORT
- Never use "Verification Report" as the title.
- This agent produces the initial job analysis only.
- A separate Verification Agent produces the verification report.

Do not make a final scam or legitimacy decision.

IMPORTANT RULES:

1. The original offer is the source of truth.
2. Only report facts explicitly stated in the original offer.
3. If information is absent, write "Not provided".
4. Never invent company details, responsibilities or requirements.
5. Do not assume a company website from an email domain.
6. Do not assume a contact person's identity from an email.
7. Do not copy facts from previous investigations.
8. Do not make unsupported company-registration claims.
9. Do not assume that a dollar symbol means USD.
10. Keep salary and payment requests separate.
11. Every monetary amount must appear in the original offer.
12. Do not create payment categories that are not mentioned.
13. CVs and academic certificates are application documents,
    not educational qualifications.
14. An actual request for an upfront registration or application fee is a potential warning sign, but it does not prove fraud.
15. Explicit denial statements such as 'no application fee is required', 'no registration fee', 'free to apply', or 'the company does not require payment' are NOT payment requests or warning signs.
16. Never describe an explicit statement that no fee is required as suspicious. Do not reverse the meaning of a negative statement.
17. If the offer says that a fee is not confirmed or does not specify whether a fee applies, classify it as unknown, not as an actual payment request.
18. If no actual payment request is stated, report that no payment-related warning sign was identified.
15. Missing information is not automatically evidence of fraud.

PYTHON-EXTRACTED INFORMATION:

{extracted_info}

Use this as supporting information. The original offer
always takes priority.

PREVIOUS INVESTIGATION LESSONS:

{previous_lessons}

Previous lessons are guidance only. Never copy their company
names, email addresses, amounts or payment requests.

ORIGINAL JOB OFFER:

{job_offer}

PRODUCE ALL EIGHT SECTIONS:

1. COMPANY INFORMATION
Include company name, location, website and other stated details.

2. JOB INFORMATION
Include position, responsibilities, employment type, salary,
currency, payment frequency, benefits and stated requirements.

3. CONTACT INFORMATION
Include email, phone number, contact person's name
and other communication channels.

4. APPLICATION REQUIREMENTS
Include educational qualifications, experience requirements,
required documents, application procedure and deadline.
Keep documents separate from educational qualifications.

5. PAYMENT REQUESTS
Include only actual payment requests stated in the offer.
Preserve exact amounts and their stated purposes.
Do not list unmentioned fee categories.

6. POTENTIAL WARNING SIGNS
Describe actual evidence, why it may be concerning,
and the potential risk. Do not make a final fraud decision.

7. MISSING INFORMATION
List only important information genuinely absent from the offer.
Do not list information that is already provided.

8. INITIAL OBSERVATIONS
Summarize the actual facts, potential warning signs,
missing information and details requiring verification.

FINAL RULES:

- Use simple, clear English.
- Preserve exact company names, job titles, email addresses,
  documents and monetary amounts.
- Do not assume a currency.
- Do not invent facts.
- Do not make company-registration claims.
- Do not make the final scam decision.

Return the complete report with:
1. The title "JOB ANALYSIS REPORT" as the first line.
2. All eight numbered sections.
3. No verification-report title.
"""

    # --------------------------------------------------
    # First LLM attempt
    # --------------------------------------------------

    try:

        response = llm.invoke(prompt)

        report = (
            response.content
            if hasattr(response, "content")
            else str(response)
        )

        if not isinstance(report, str):
            report = str(report)

    except Exception as e:

        print("\nJob Analysis LLM failed:", str(e))

        report = ""

    # --------------------------------------------------
    # Monetary consistency check
    # --------------------------------------------------

    unsupported_amounts = find_unsupported_amounts(
        report,
        job_offer
    )

    if unsupported_amounts:

        print(
            "\nWarning: Unsupported monetary amounts detected."
        )

        print(
            "Unsupported amounts:",
            ", ".join(sorted(unsupported_amounts))
        )

        print(
            "Retrying the Job Analysis Agent..."
        )

        correction_prompt = f"""
/no_think

Your previous report introduced monetary amounts
not supported by the original job offer.

ORIGINAL JOB OFFER:
{job_offer}

PREVIOUS REPORT:
{report}

UNSUPPORTED AMOUNTS:
{sorted(unsupported_amounts)}

Correct the complete report.

Rules:

1. The original offer is the only source of facts.
2. Remove unsupported amounts.
3. Preserve genuine salary and payment amounts.
4. Do not invent fees.
5. Do not assume that "$" means USD.
6. Preserve all required documents explicitly stated.
7. Keep CVs and certificates under Required documents.
8. Do not list unmentioned fee categories as missing.
9. Do not make company-registration claims.
10. Preserve all eight report sections.
11. Do not make the final scam decision.

Return the complete corrected report.
"""

        try:

            corrected_response = llm.invoke(correction_prompt)

            corrected_report = (
                corrected_response.content
                if hasattr(corrected_response, "content")
                else str(corrected_response)
            )

            remaining_unsupported = find_unsupported_amounts(
                corrected_report,
                job_offer
            )

            if remaining_unsupported:

                print(
                    "Correction still contains unsupported amounts."
                )

                report = remove_unsupported_amount_lines(
                    corrected_report,
                    remaining_unsupported
                )

            else:

                report = corrected_report

                print(
                    "Monetary consistency check passed after correction."
                )

        except Exception as e:

            print(
                "Correction attempt failed:",
                str(e)
            )

            report = remove_unsupported_amount_lines(
                report,
                unsupported_amounts
            )

    else:

        print(
            "\nMonetary consistency check passed. "
            "No unsupported amounts detected."
        )

    # --------------------------------------------------
    # Deterministic report cleanup
    # --------------------------------------------------

    report = remove_unsupported_registry_claims(report)

    report = apply_report_cleanup(
        report,
        job_offer
    )

    # --------------------------------------------------
    # Ensure exactly one correct Job Analysis title.
    report_lines = report.strip().splitlines()

    title_pattern = r"\s*\*{0,2}\s*(?:VERIFICATION REPORT|JOB ANALYSIS REPORT)\s*\*{0,2}\s*"

    if report_lines and __import__("re").fullmatch(
        title_pattern, report_lines[0], __import__("re").IGNORECASE
    ):
        report_lines[0] = "JOB ANALYSIS REPORT"

        while len(report_lines) > 1 and __import__("re").fullmatch(
            title_pattern, report_lines[1], __import__("re").IGNORECASE
        ):
            report_lines.pop(1)

        report = "\n".join(report_lines)
    else:
        report = "JOB ANALYSIS REPORT\n\n" + report.strip()

    # Report completeness validation
    # --------------------------------------------------

    if not is_report_complete(report, job_offer):

        print(
            "\nWarning: Job Analysis Agent returned an incomplete "
            "or insufficient report."
        )

        print(
            "Using deterministic Python report fallback."
        )

        report = build_deterministic_report(
            job_offer,
            extracted_info
        )

        # Apply the existing safeguards to the fallback too.
        report = remove_unsupported_registry_claims(report)

        report = apply_report_cleanup(
            report,
            job_offer
        )

        print(
            "Deterministic report generated with all eight sections."
        )

    else:

        print(
            "\nJob Analysis report passed completeness validation."
        )

    # --------------------------------------------------
    # Return investigation results
    # --------------------------------------------------

    return {
        "investigation": report,
        "extracted_information": extracted_info
    }
