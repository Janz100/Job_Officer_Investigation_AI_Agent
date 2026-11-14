# Job Offer Investigation and Verification Agent

An AI-powered multi-agent system that investigates job offers, checks available evidence, and helps job seekers identify potential recruitment scams.

## 1. Project Overview

Online job platforms and digital recruitment have made it easier for people to find employment opportunities. However, fraudulent job advertisements, fake recruiters, misleading vacancies, suspicious email addresses, and requests for advance payments have also become common.

The **Job Offer Investigation and Verification Agent** is designed to help job seekers examine job offers before responding to them. Users can submit a job announcement or recruitment message, and the system analyses its contents, searches for relevant information, checks available websites and email addresses, and generates an investigation report.

The project uses a multi-agent architecture in which specialised agents perform different tasks. It also incorporates external verification tools, short-term and long-term memory, user feedback, and reflection mechanisms.

The system does not make decisions based only on the language model's opinion. It combines AI-generated analysis with information gathered through available tools to provide a more evidence-based assessment.

## 2. Project Objectives

The main objectives are to:

- Analyse job advertisements and extract important recruitment information.
- Identify possible warning signs associated with fraudulent job offers.
- Search for relevant information about employers and advertised vacancies.
- Examine website and email details using verification tools.
- Generate structured investigation reports based on available evidence.
- Maintain previous investigation records using a memory system.
- Collect user feedback about investigation results.
- Use reflection and previous lessons to inform future investigations.
- Provide an accessible dashboard for submitting and reviewing job investigations.

## 3. Key Features

### 3.1 AI-Powered Job Analysis

The Job Analysis Agent examines the submitted job offer and extracts relevant information, including:

- Company or organisation name
- Job title and position
- Salary and benefits, when provided
- Job location and duration
- Application deadline
- Contact information and email addresses
- Application or registration fees
- Other possible warning signs

The extracted information is passed to the verification stage for further investigation.

### 3.2 Multi-Agent Investigation

The system uses two specialised AI agents connected through a LangGraph workflow.

**Job Analysis Agent**

- Reads and analyses the submitted job announcement.
- Extracts important job and employer information.
- Identifies possible warning signs.
- Prepares structured information for the next agent.

**Verification Agent**

- Examines the information extracted by the first agent.
- Uses available verification tools to gather supporting evidence.
- Reviews search results, websites, email information, and scam indicators.
- Produces the final investigation findings.

The workflow follows a sequential process:

```text
              User Submits Job Offer
                       |
                       v
              Job Analysis Agent
                       |
                       v
             Information Extraction
                       |
                       v
              Verification Agent
                       |
          +------------+------------+
          |            |            |
          v            v            v
       Web Search   Website Check  Email Check
          |            |            |
          +------------+------------+
                       |
                       v
              Evidence Evaluation
                       |
                       v
              Investigation Report
                       |
                       v
                 User Feedback
                       |
                       v
             Memory and Reflection
```

LangGraph manages the movement of information between the agents through a shared investigation state.

### 3.3 Verification Tools

The system includes several tools that support the investigation process.

| Tool | Purpose |
|---|---|
| Web Search | Searches for relevant information about employers and job opportunities using DuckDuckGo Search. |
| Website Checker | Examines a supplied website and retrieves available technical and accessibility information. |
| Email Checker | Checks email format, domain information, free email providers, domain existence, and mail server records where available. |
| Information Extractor | Extracts relevant details such as salaries, contact information, and payment requests from job announcements. |
| Scam Detector | Identifies possible recruitment scam indicators, including suspicious payment requests and other warning signs. |

These tools provide information for the agents to evaluate. Their results are not treated as automatic proof that an employer or vacancy is genuine or fraudulent.

### 3.4 Investigation Assessment

The system generates an assessment based on the available investigation evidence.

The assessment categories include:

- **Likely Legitimate:** Available evidence supports the legitimacy of the offer.
- **Suspicious:** Evidence contains indicators that may suggest fraudulent recruitment activity.
- **Needs Further Verification:** Additional checks are needed before reaching a conclusion.
- **Inconclusive:** Available information is insufficient or conflicting.

The report also explains the evidence and verification gaps behind its findings. An assessment is intended to guide further checking, not replace independent verification by the job seeker.

### 3.5 Memory System

The project uses SQLite to store investigation information and support memory-related functions.

The memory system includes:

**Short-Term Memory**

Maintains information and context during an active investigation.

**Long-Term Memory**

Stores previous investigation records so that relevant information can be retrieved in later investigations.

**Feedback Memory**

Stores user feedback about investigation results, including feedback ratings and comments.

**Reflection Memory**

Stores lessons and reflection information generated from previous investigations.

The different memory components allow the system to retain useful investigation context rather than treating every investigation as completely unrelated.

### 3.6 Feedback and Reflection

Users can provide feedback on the investigation results.

The system stores this feedback and uses reflection mechanisms to identify lessons from previous investigations. Relevant previous lessons can be retrieved and supplied to the agents during subsequent investigations.

This creates a feedback-supported process in which previous investigation experiences can inform future analysis.

### 3.7 Streamlit Dashboard

The application provides a web-based dashboard developed using Streamlit.

The dashboard includes:

- **Home:** Provides an overview of the application.
- **New Investigation:** Allows users to submit a job offer for investigation.
- **Investigation History:** Displays previously recorded investigations.
- **Feedback:** Allows users to provide feedback on investigation results.

The interface presents investigation information and assessment results in a structured format.

## 4. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Ollama | Runs the local language model |
| Llama 3.2 / configured local model | Supports local AI analysis |
| Groq API | Provides cloud-based language model access |
| GPT-OSS-20B through Groq | Cloud model configuration |
| LangChain | Connects language models with application components |
| LangGraph | Manages the multi-agent workflow |
| Streamlit | Builds the web dashboard |
| SQLite | Stores investigation records and memory |
| DuckDuckGo Search (DDGS) | Retrieves relevant web information |
| Requests and BeautifulSoup | Support website information retrieval |
| Pydantic | Supports structured data handling and validation |

The application supports local and cloud-based model configurations. The selected model depends on the available configuration and API credentials.

## 5. System Workflow

The complete investigation process follows these steps:

1. **Job Offer Submission:** The user enters a job announcement into the dashboard.
2. **Job Analysis:** The Job Analysis Agent examines the announcement and extracts relevant details.
3. **Information Extraction:** Important information, including employer details, contact information, salary, and payment requests, is identified.
4. **Verification:** The Verification Agent examines the extracted information and determines which checks are relevant.
5. **Tool Execution:** The system uses available tools to search for information and check supplied websites and email addresses.
6. **Evidence Evaluation:** The agent evaluates the collected information and identifies confirmed findings, possible warning signs, and information that could not be verified.
7. **Report Generation:** The system produces an investigation report with an assessment and supporting explanations.
8. **Memory Storage:** Investigation information is stored in the SQLite database.
9. **User Feedback:** The user can submit feedback about the result.
10. **Reflection:** Feedback and previous lessons are used to inform future investigations.

## 6. Project Structure

The main project files and folders are organised as follows:

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
├── test_email_checker.py
├── test_extraction.py
├── test_fee_detection.py
├── test_feedback.py
├── test_full_investigation.py
├── test_graph.py
├── test_integrated_memory.py
├── test_investigator.py
├── test_learning.py
├── test_legitimate_offer.py
├── test_llm.py
├── test_long_term_memory.py
├── test_memory.py
├── test_memory_learning.py
├── test_memory_retrieval.py
├── test_reflection.py
├── test_reflection_agent.py
├── test_report_safeguards.py
├── test_scam_detector.py
├── test_verification_agent.py
├── test_verification_tools.py
├── test_web_search.py
└── test_website_checker.py
```

## 7. Installation and Setup

### Prerequisites

The following software and services are required for local execution:

- Python 3.12 or a compatible Python version
- Git
- Ollama
- An internet connection for web search and external verification
- A Groq API key if using the cloud-based model configuration

### Step 1: Clone the Repository

```bash
git clone https://github.com/Janz100/Job_Officer_Investigation_AI_Agent.git
cd Job_Officer_Investigation_AI_Agent
```

### Step 2: Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment in Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Configure the Language Model

For local execution, install Ollama and download the model configured in `config.py`.

For example, if the configured model is Llama 3.2:

```bash
ollama pull llama3.2:3b
```

Make sure the Ollama service is running before starting the application.

For cloud execution, configure the `GROQ_API_KEY` environment variable or add the key to the application's Streamlit secrets.

**Important:** Never upload API keys or other private credentials to GitHub. Keep them in environment variables or the platform's secrets manager.

### Step 5: Run the Application

```bash
streamlit run app.py
```

The application will open in a browser, where users can submit job offers and access the dashboard.

## 8. Web Deployment

The project has also been deployed using **Streamlit Community Cloud**.

The deployed application provides browser-based access to the investigation dashboard without requiring users to install the project locally.

The deployment uses the GitHub repository as its source and Streamlit secrets for protected configuration such as the Groq API key.

Deployment overview:

1. The project source code is maintained in GitHub.
2. The GitHub repository is connected to Streamlit Community Cloud.
3. The main application file is configured as `app.py`.
4. Required dependencies are installed from `requirements.txt`.
5. API credentials are configured through Streamlit secrets.
6. The application is made accessible through its deployed web address.

The deployed application has been opened and tested successfully.

## 9. Testing and Evaluation

### 9.1 Component Testing

The project contains separate test files for checking different parts of the system.

The testing areas include:

- Email address verification
- Website checking
- Information extraction
- Scam indicator detection
- Job analysis and verification agents
- LangGraph workflow execution
- Investigation memory
- Feedback storage
- Reflection mechanisms
- Report safeguards
- Language model connection

Individual test files can be executed using commands such as:

```bash
python test_email_checker.py
python test_extraction.py
python test_fee_detection.py
python test_full_investigation.py
python test_verification_agent.py
python test_report_safeguards.py
```

These tests examine individual components and selected integrated workflows.

### 9.2 Job Announcement Investigation

The system was also tested using real-world-style job announcements, including opportunities associated with UNICEF Bhutan and the Ministry of Agriculture and Livestock.

The selected investigation reports included:

- Child Protection Programme Intern
- Child-Sensitive Climate and Finance Strategy Consultant
- Farm Labourer / Attendant
- Security Guard

The reports demonstrated how the system analyses different job announcements, searches for supporting information, checks available details, and produces investigation assessments.

### 9.3 Evaluation Scope and Limitation

The evaluation discussed in this project is based on **selected investigation reports rather than every job announcement or every investigation conducted by the system**.

For example, the selected reports from Investigation IDs 4–10 included seven investigation runs. However, these represented only four unique job announcements because three of the runs were repeated investigations of announcements already examined.

Among these selected runs:

- Three received a Suspicious assessment.
- Four received an Insufficient Evidence assessment.

These results describe only the selected reports reviewed. They must not be interpreted as the overall accuracy, success rate, or performance score of the complete system.

The evaluation was not an exhaustive benchmark covering all possible job categories, employers, recruitment platforms, or types of recruitment fraud. Furthermore, the selected announcements did not all have independently established ground-truth labels. Therefore, formal measures such as overall accuracy, precision, recall, and F1-score cannot be reliably claimed from this selected review alone.

The evaluation provides examples of the system's investigation behaviour and demonstrates how it handles available evidence and missing information. It does not establish that every generated assessment is correct.

## 10. Safety, Ethics, and Limitations

The system is designed as an investigation-support tool. It is not intended to replace official recruitment authorities, legal advice, or independent verification by job seekers.

The following limitations should be considered:

### 10.1 Dependence on Available Information

The accuracy of an investigation depends on the information supplied by the user and the information available through external sources. Incomplete job announcements may result in insufficient evidence for a reliable conclusion.

### 10.2 External Search Limitations

Web search results may be incomplete, outdated, or unrelated to the specific employer or vacancy. Finding a similar company name or website does not automatically establish that it belongs to the organisation mentioned in the job offer.

### 10.3 Website and Email Verification Limitations

Website and email checks provide technical information, such as domain existence, email format, and mail server records. These checks cannot independently prove that a recruiter is authorised or that a particular job vacancy is genuine.

### 10.4 Employer and Vacancy Verification

Confirming that an organisation exists does not automatically confirm that a specific job announcement was published by that organisation. Similarly, company registration should not be considered verified unless an appropriate official registration source has actually been checked.

### 10.5 Assessment Limitations

AI-generated assessments may be affected by incomplete information, search limitations, model responses, or incorrect interpretation of evidence. Missing information alone does not necessarily prove that a job offer is fraudulent.

Users should treat the generated report as guidance and independently confirm important employment details through official employer websites, recruitment portals, or verified contact channels.

### 10.6 Evaluation Limitations

The project evaluation was conducted using selected investigation reports. Not all announcements and investigation runs were examined in detail. Some selected reports were repeated runs of the same job announcement, and the review did not establish ground-truth labels for every case.

Consequently, the selected evaluation cannot be used as a complete measurement of the system's overall accuracy or general performance.

### 10.7 External Service and Deployment Limitations

The system depends on external services for web search and, when cloud execution is selected, language model access. Network problems, API limits, service availability, or changes to external services may affect investigation results.

The deployed application also depends on the hosting platform's resource and storage behaviour. Local SQLite data may not be permanently retained if the hosting platform does not provide persistent storage.

### 10.8 Privacy and Responsible Use

Users should avoid submitting unnecessary sensitive personal information. The system should not be treated as an authority for making employment, financial, or legal decisions. Users remain responsible for independently verifying offers before sharing personal documents, paying money, or accepting employment.

## 11. Project Significance

The Job Offer Investigation and Verification Agent demonstrates how multiple AI agents, external tools, memory, feedback, and reflection can be combined to address a practical problem.

Instead of relying only on a language model to judge a job advertisement, the system follows a structured investigation process. It extracts information, gathers available evidence, performs verification checks, and presents findings in an organised report.

The project also demonstrates important concepts in intelligent agent development, including multi-agent coordination, tool use, workflow management, memory, feedback-based learning, reflection, and human-centred decision support.

## 12. Conclusion

The Job Offer Investigation and Verification Agent was developed to support job seekers in examining online employment opportunities and recognising possible recruitment scams.

Through its multi-agent architecture, verification tools, memory mechanisms, feedback system, and Streamlit dashboard, the project brings together several important concepts of intelligent and generative agents in one practical application.

Although the system has limitations in external information availability, verification certainty, and evaluation coverage, it demonstrates how an AI agent can perform a structured investigation rather than simply generate a response from a user's input.

The final system provides an accessible way to examine job offers and understand the evidence available before taking further action.

---

**Project:** Job Offer Investigation and Verification Agent  
**Repository:** https://github.com/Janz100/Job_Officer_Investigation_AI_Agent  
**Interface:** Streamlit  
**Main Language:** Python  
**Core Frameworks:** LangChain and LangGraph  
**Memory Storage:** SQLite  
**Model Support:** Ollama and Groq  
