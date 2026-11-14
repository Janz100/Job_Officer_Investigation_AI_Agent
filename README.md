# Job_Officer_Investigation_AI_Agent
An AI Agent 
# Job Offer Investigation and Verification Agent

An AI-powered multi-agent system designed to investigate, analyse, and verify job offers to help users identify potentially fraudulent recruitment activities and avoid job scams.

## 1. Project Overview

Online job opportunities have made it easier for people to find employment. However, fraudulent job offers and recruitment scams have also increased. Job seekers may encounter fake companies, misleading vacancies, suspicious email addresses, and requests for advance payments.

The **Job Offer Investigation and Verification Agent** aims to address this problem by examining job offers and gathering evidence to help users understand whether an opportunity appears legitimate, suspicious, or requires further verification.

The system uses multiple AI agents, verification tools, and memory mechanisms to conduct investigations and improve its responses through user feedback.

## 2. Project Objectives

- Analyse job offers and extract important information.
- Identify common warning signs associated with recruitment scams.
- Check company websites and email addresses using verification tools.
- Search for relevant information about companies and job opportunities.
- Generate investigation reports based on available evidence.
- Store previous investigation results and user feedback.
- Use reflection and memory to improve future investigations.

## 3. Key Features

### AI-Powered Job Analysis
Analyses submitted job offers and extracts relevant details such as company names, job positions, salaries, contact information, and payment requests.

### Multi-Agent Investigation
Uses specialised AI agents to perform different investigation tasks:

- **Job Analysis Agent:** Examines the job offer and identifies important information and possible warning signs.
- **Verification Agent:** Evaluates available evidence using verification tools and produces investigation findings.

### Verification Tools
The system includes tools for:

- Website checking
- Email address verification
- Web searching
- Information extraction
- Scam indicator detection

### Memory System
Uses SQLite-based memory to maintain investigation records, previous lessons, user feedback, and reflection information.

### Feedback and Reflection
Allows users to provide feedback on investigation results. The system stores feedback and uses previous lessons to support future investigations.

### Investigation Dashboard
A Streamlit-based interface provides access to:

- Home
- New Investigation
- Investigation History
- Feedback

## 4. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Ollama | Runs the local language model |
| Llama 3.2 | Language model used for AI analysis |
| LangChain | Connects language models and application components |
| LangGraph | Manages the multi-agent workflow |
| Streamlit | User interface and dashboard |
| SQLite | Stores investigation records and memory |
| DuckDuckGo Search | Retrieves relevant web information |

## 5. System Workflow

1. The user submits a job offer for investigation.
2. The Job Analysis Agent examines the offer and extracts relevant information.
3. The system identifies possible warning signs.
4. The Verification Agent uses available tools to examine websites, email addresses, and search results.
5. The agents use available memory and previous lessons during the investigation.
6. The system generates an investigation report based on the collected evidence.
7. The user can provide feedback on the result.
8. Feedback and investigation information are stored to support future investigations.

## 6. Project Structure

```text
Job_Offer_Investigation_Agent/
│
├── agents/
│   ├── __init__.py
│   ├── job_analysis_agent.py
│   └── verification_agent.py
│
├── memory/
│   ├── __init__.py
│   ├── database.py
│   ├── feedback_memory.py
│   ├── long_term_memory.py
│   ├── reflection_memory.py
│   └── short_term_memory.py
│
├── reflection/
│   └── reflection_agent.py
│
├── tools/
│   ├── __init__.py
│   ├── email_checker.py
│   ├── information_extractor.py
│   ├── scam_detector.py
│   ├── web_search.py
│   └── website_checker.py
│
├── app.py
├── agent.py
├── config.py
├── llm.py
├── requirements.txt
│
└── test_*.py
```

## 7. Installation and Setup

### Prerequisites

- Python 3.12 or a compatible Python version
- Git
- Ollama

### Step 1: Clone the Repository

```bash
git clone https://github.com/Janz100/Job_Officer_Investigation_AI_Agent.git
cd Job_Offer_Investigation_Agent
```

### Step 2: Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Ollama

Install Ollama and download the required model:

```bash
ollama pull llama3.2:3b
```

Make sure the Ollama service is running before starting the application.

### Step 5: Run the Application

```bash
streamlit run app.py
```

The application should open in your browser.

## 8. Testing

The project includes separate Python test files to test different components, including:

- Email verification
- Website checking
- Information extraction
- Scam detection
- Agent workflow
- Memory and feedback
- Reflection mechanisms
- Investigation report safeguards

Run an individual test using:

```bash
python test_full_investigation.py
```

## 9. Important Notes and Limitations

- The system provides investigation assistance, not a guarantee that a job offer is genuine or fraudulent.
- Search results do not automatically prove that a website belongs to a particular company.
- Company registration should not be considered verified unless an appropriate registration source has actually been checked.
- Email and website checks provide technical indicators, not proof of an employer's identity.
- Users should independently confirm important employment details before sharing personal information or making payments.
- Investigation accuracy depends on the availability and reliability of external information.

## 10. Future Improvements

- Improve company identity and registration verification.
- Expand the database of known fraudulent recruitment patterns.
- Improve the accuracy of AI-generated investigation reports.
- Add more verification sources.
- Improve the dashboard and user experience.
- Strengthen feedback-based learning and agent collaboration.

## 11. Project Purpose

This project demonstrates how AI agents, verification tools, multi-agent workflows, and memory mechanisms can be combined to address a real-world problem.

Its main purpose is to help job seekers make more informed decisions by providing evidence-based analysis of online job opportunities.

---

**Project:** Job Offer Investigation and Verification Agent  
**Repository:** [GitHub Repository](https://github.com/Janz100/Job_Officer_Investigation_AI_Agent)  
**Developed using:** Python, Ollama, LangChain, LangGraph, Streamlit, and SQLite
