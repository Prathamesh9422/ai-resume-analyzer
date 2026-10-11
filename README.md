# AI Resume Analyzer

A beginner-friendly Generative AI project that analyzes a resume against a Job Description and provides useful feedback to improve the resume.

This project uses Python, Streamlit, and the Gemini API. You can upload your resume as a PDF or Word document, paste a Job Description, and get an AI-generated analysis of your skills, strengths, missing skills, and areas for improvement.

---

## 1. What are we building?

We are building a simple web application that helps users understand how well their resume matches a particular job role.

You upload your resume, paste the Job Description, and click **Analyze Resume**.

The application analyzes the information and provides:

* Candidate skills and experience
* Skills required for the job
* Skills that match the Job Description
* Missing or weak skills
* Resume strengths and gaps
* Suggestions to improve the resume
* An overall summary of the match

You can also download the generated analysis report.

The main goal of this project is to learn how to use a Large Language Model (LLM) in a practical Python application.

---

## 2. What will I learn?

By building this project, I learned the basics of:

* **Python** — writing functions, handling files, and working with dictionaries.
* **Streamlit** — creating a simple web interface using Python.
* **File handling** — accepting PDF and DOCX files from users.
* **Text extraction** — extracting text from resumes using `pypdf` and `python-docx`.
* **Gemini API** — connecting a Python application to Google's Gemini models.
* **Environment variables** — keeping API credentials in a `.env` file instead of hardcoding them.
* **Prompt engineering** — writing instructions that guide the AI response.
* **JSON output** — asking the model to return structured information that Python can process.
* **Prompt chaining** — using the output of one AI call as input for another.
* **Error handling** — handling missing inputs, API errors, and unsupported files.
* **Report generation** — presenting the analysis in a readable format and allowing users to download it.

---

## 3. Project workflow

The application follows a two-step AI workflow.

```text
Resume + Job Description
          |
          v
    Text Extraction
          |
          v
      AI Call #1
          |
          v
   Structured Analysis
          |
          v
      AI Call #2
          |
          v
    Final AI Report
          |
          v
  Display Results in UI
          |
          v
    Download Report
```

### Step 1 — Upload and extract the resume

The user uploads a resume in PDF or DOCX format.

The application extracts the text using Python libraries:

* `pypdf` for PDF files
* `python-docx` for Word documents

The extracted text is then used for the AI analysis.

### Step 2 — Analyze the resume

The first AI call compares the resume with the Job Description and identifies information such as:

* Candidate skills
* Candidate experience
* Qualifications
* Required skills
* Preferred skills
* Matching skills
* Missing skills
* Gaps between the resume and job requirements

The response is requested in JSON format so the application can process the information.

### Step 3 — Generate the final report

The second AI call uses the structured analysis to generate a readable report.

The report includes:

* Strengths
* Gaps
* Missing or weak skills
* Improvement suggestions
* Overall summary

This two-step process is an example of **prompt chaining**. Instead of asking the AI to do everything in one request, the application separates the analysis and report-writing tasks.

### Step 4 — Display and download

Streamlit displays the final report in the browser.

The user can review the results and download the report for future reference.

---

## 4. Project structure

```text
AI-resume-Analyzer/
│
├── app.py
├── test_gemini.py
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
└── README.md
```

### What each file does

* **`app.py`** — contains the Streamlit interface, resume text extraction, AI analysis, and report generation.
* **`test_gemini.py`** — a small script used to test the Gemini API connection.
* **`requirements.txt`** — contains the Python packages required to run the project.
* **`.env`** — stores the API configuration used by the application. This file should never be uploaded to GitHub.
* **`.env.example`** — provides a template showing which environment variables are required, without containing a real API key.
* **`.gitignore`** — tells Git which files and folders should not be committed.
* **`README.md`** — explains the project, setup instructions, workflow, and usage.

---

## 5. Installation

### Step 1 — Clone the repository

After uploading the project to GitHub, open PowerShell and run:

```powershell
git clone YOUR_GITHUB_REPOSITORY_URL
```

Move into the project folder:

```powershell
cd AI-resume-Analyzer
```

Replace the placeholder repository URL with your actual GitHub repository URL.

If you already have the project on your computer, open PowerShell directly in the project folder instead.

### Step 2 — Create a virtual environment

A virtual environment keeps the project's Python packages separate from other Python projects.

```powershell
python -m venv .venv
```

### Step 3 — Activate the virtual environment

For Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

After activation, your terminal should show `(.venv)`.

### Step 4 — Install dependencies

```powershell
pip install -r requirements.txt
```

This installs the packages needed to run the application.

---

## 6. Environment setup

The Gemini API key is a secret, similar to a password. It should not be written directly in your Python code or published on GitHub.

### Step 1 — Get a Gemini API key

Create an API key through Google AI Studio:

https://aistudio.google.com/

Keep your key private.

### Step 2 — Create the `.env` file

In your project folder, create a file named `.env`.

Add the following configuration:

```env
BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
API_KEY=your_gemini_api_key_here
OLLAMA_MODEL=gemini-3.5-flash
```

Replace `your_gemini_api_key_here` with your own API key.

Keep the variable names exactly as expected by your `app.py`.

**Note:** Despite the name `OLLAMA_MODEL`, this project uses the configured Gemini model through Google's OpenAI-compatible API endpoint. The name is simply an environment variable used by the current application code.

### Step 3 — Protect your API key

Make sure `.env` is included in `.gitignore`.

Example:

```gitignore
.env
.venv/
__pycache__/
*.pyc
```

You can safely upload `.env.example` if it contains only placeholder values and no real secrets.

Never commit your real API key to GitHub.

---

## 7. Running the application

Make sure your virtual environment is activated and your `.env` file is configured.

Run the following command:

```powershell
streamlit run app.py
```

Streamlit will start the application and show a local URL, usually:

http://localhost:8501

Open that URL in your browser if it does not open automatically.

To stop the application, press `Ctrl + C` in the terminal.

---

## 8. How to use the application

1. **Upload your resume:** Select a PDF or DOCX file from your computer.
2. **Paste the Job Description:** Copy the description of the job you want to apply for into the provided text area.
3. **Click Analyze Resume:** The application extracts the resume text and sends the information through the AI analysis workflow.
4. **Review the analysis:** Read the matching skills, missing skills, gaps, strengths, and improvement suggestions.
5. **Download the report:** Save the generated report if you want to review it later.

For better results, provide a complete Job Description and a resume containing selectable text rather than scanned images.

---

## 9. Example workflow

Imagine that a candidate's resume mentions:

* Python
* SQL
* Pandas
* Two years of data analysis experience

The Job Description requires:

* Python
* SQL
* AWS
* Apache Airflow

The AI might identify the following:

**Matching skills**

* Python
* SQL

**Missing skills**

* AWS
* Apache Airflow

**Strengths**

* The resume includes Python and SQL, which are relevant to the role.
* The candidate has experience in data analysis.

**Improvement suggestions**

* If the candidate has worked with cloud platforms or data pipelines, they should describe that experience clearly in the resume.
* The candidate could consider learning AWS or Apache Airflow if these skills are important for their target roles.

This is only an illustrative example. Actual results depend on the uploaded resume, the Job Description, and the AI model's response.

One important point: if a skill is missing from the resume, it does not necessarily mean the candidate lacks that skill. It may simply mean the resume does not mention it.

---

## 10. Common errors

### API key or authentication error

Check that:

* Your `.env` file is in the same folder as `app.py`.
* The `API_KEY` variable contains a valid Gemini API key.
* You have not accidentally added quotation marks or extra spaces.
* The key has not been revoked.

Never share your API key when asking for help.

### Model or API error

Check the `BASE_URL` and `OLLAMA_MODEL` values in your `.env` file.

The current project uses the Gemini OpenAI-compatible endpoint:

```text
https://generativelanguage.googleapis.com/v1beta/openai/
```

Also confirm that the configured model is available to your API setup.

### Missing resume or Job Description

Make sure you have uploaded a resume and entered a Job Description before clicking **Analyze Resume**.

### PDF text extraction problem

Some PDFs contain scanned images instead of selectable text. The current text-extraction approach may not be able to read those files.

Try using a text-based PDF or a DOCX file. Scanned documents may require OCR, which is not currently included.

### Streamlit command not found

Activate the virtual environment and install the dependencies:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Then run:

```powershell
streamlit run app.py
```

### Slow response or timeout

AI responses may take longer depending on the document size, internet connection, API availability, and model response time.

Try a shorter resume or Job Description if the problem continues.

---

## 11. What this project does NOT cover

This project is designed as a beginner-friendly introduction to GenAI application development.

It does not currently include:

* Resume OCR for scanned documents
* A database for saving previous analyses
* User accounts or authentication
* Retrieval-Augmented Generation (RAG)
* Embeddings or vector databases
* Fine-tuning a language model
* An autonomous AI agent
* Automated job searching or applications
* A guarantee that a resume will pass an Applicant Tracking System (ATS)

The application provides AI-generated feedback based on the supplied resume and Job Description. It should be used as a decision-support tool, not as a guarantee of hiring success.

---

## 12. Future improvements

Possible improvements for future versions include:

* Adding OCR support for scanned resumes
* Improving the user interface
* Adding resume improvement and rewriting features
* Supporting additional file formats
* Saving previous reports
* Adding more detailed skill-match scoring
* Deploying the application online
* Adding sample resumes for testing

---

## 13. Security and privacy

* Keep your Gemini API key private.
* Do not upload `.env` to GitHub.
* Use `.env.example` to document the required configuration.
* Avoid uploading resumes containing sensitive personal information unless you understand how the information will be processed.
* Review the API provider's current privacy and data-handling policies before using real resumes.

---

