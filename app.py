import json
import os

import streamlit as st
from docx import Document
from dotenv import load_dotenv
from openai import OpenAI, APIError, APITimeoutError
from pypdf import PdfReader


# Load API settings from the .env file
load_dotenv(override=True)

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv(
    "BASE_URL",
    "https://generativelanguage.googleapis.com/v1beta/openai/"
)
MODEL = os.getenv("OLLAMA_MODEL", "gemini-3.5-flash")


# Sections to display in the final report
REPORT_SECTIONS = [
    ("strengths", "Strengths"),
    ("gaps", "Gaps"),
    ("missing_or_weak_skills", "Missing or Weak Skills"),
    ("improvement_suggestions", "Improvement Suggestions"),
    ("overall_summary", "Overall Summary"),
]


# Create the Gemini client
@st.cache_resource
def get_client():
    return OpenAI(
        api_key=API_KEY,
        base_url=BASE_URL,
        timeout=300,
        max_retries=1
    )


# Extract text from the uploaded resume
def extract_resume_text(uploaded_file):
    file_name = uploaded_file.name.lower()

    if file_name.endswith(".pdf"):
        reader = PdfReader(uploaded_file)
        resume_text = []

        for page in reader.pages:
            resume_text.append(page.extract_text() or "")

        return "\n".join(resume_text).strip()

    elif file_name.endswith(".docx"):
        document = Document(uploaded_file)
        resume_text = []

        for paragraph in document.paragraphs:
            if paragraph.text.strip():
                resume_text.append(paragraph.text)

        # Read text from tables in the Word document
        for table in document.tables:
            for row in table.rows:
                row_text = " | ".join(
                    cell.text.strip() for cell in row.cells
                )
                if row_text.strip():
                    resume_text.append(row_text)

        return "\n".join(resume_text).strip()

    return ""


# Send a request to Gemini and receive JSON
def get_ai_response(instructions, user_message, max_tokens=2500):
    client = get_client()

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": instructions},
            {"role": "user", "content": user_message}
        ],
        response_format={"type": "json_object"},
        temperature=0.2,
        max_tokens=max_tokens
    )

    result = response.choices[0].message.content

    if not result or not result.strip():
        raise ValueError(
            "Gemini returned an empty response. Please try again "
            "with a shorter resume or job description."
        )

    return json.loads(result)


# Compare the resume with the job description
def analyze_resume(resume_text, job_description):
    instructions = """
    You are an AI resume analyzer.

    Compare the resume with the job description and return JSON
    using exactly these keys. Every value must be a list of strings.

    {
        "candidate_skills": [],
        "candidate_experience": [],
        "candidate_qualifications": [],
        "required_skills": [],
        "preferred_skills": [],
        "matching_skills": [],
        "missing_skills": [],
        "gaps": []
    }

    Rules:
    - Use only information from the provided documents.
    - Do not invent skills, qualifications or experience.
    - Identify skills that match the job requirements.
    - List required skills not mentioned in the resume.
    - Do not assume an unmentioned skill is something the
      candidate cannot perform.
    - Keep the response clear and concise.
    - Return valid JSON only.
    """

    user_message = f"""
    Compare the following resume with the job description.

    RESUME:
    {resume_text}

    JOB DESCRIPTION:
    {job_description}

    Return the comparison in JSON format.
    """

    return get_ai_response(
        instructions,
        user_message,
        max_tokens=2500
    )


# Generate the final resume feedback report
def generate_final_report(analysis):
    instructions = """
    You are a resume reviewer who provides useful and honest feedback.

    Return JSON using exactly these keys.
    Every value must be a string.

    {
        "strengths": "",
        "gaps": "",
        "missing_or_weak_skills": "",
        "improvement_suggestions": "",
        "overall_summary": ""
    }

    Rules:
    - Write the first four sections as Markdown bullet lists.
    - Write the overall summary as a short paragraph.
    - Keep the feedback specific and constructive.
    - Put technical skills and tools in missing_or_weak_skills.
    - Put experience, qualifications and responsibilities in gaps.
    - Avoid repeating the same point.
    - Never invent information.
    - Describe skills not mentioned as "not identified in the resume".
    - Do not provide a numerical score or percentage.
    - Return valid JSON only.
    """

    user_message = f"""
    Generate a resume feedback report using this analysis:

    {json.dumps(analysis, indent=2)}

    Return the report in JSON format.
    """

    report = get_ai_response(
        instructions,
        user_message,
        max_tokens=1800
    )

    # Make sure all report sections contain readable text
    for key, heading in REPORT_SECTIONS:
        value = report.get(key, "")

        if isinstance(value, list):
            value = "\n".join(
                "- " + str(item) for item in value
            )

        if not isinstance(value, str) or not value.strip():
            value = "- No further information was identified."

        report[key] = value

    return report


# Create a Markdown file for downloading
def create_report(final_report):
    report_text = ["# AI Resume Analysis"]

    for key, heading in REPORT_SECTIONS:
        report_text.append("")
        report_text.append(f"## {heading}")
        report_text.append("")
        report_text.append(final_report.get(key, ""))

    return "\n".join(report_text)


# Main Streamlit application
def main():
    st.set_page_config(
        page_title="AI Resume Analyzer",
        page_icon="📄",
        layout="wide"
    )

    st.title("AI Resume Analyzer")

    st.write(
        "Upload your resume and paste a job description to analyze "
        "your skills, identify gaps and get improvement suggestions."
    )

    uploaded_file = st.file_uploader(
        "Upload your Resume",
        type=["pdf", "docx"]
    )

    job_description = st.text_area(
        "Paste the Job Description",
        height=250
    )

    if st.button("Analyze Resume", type="primary"):

        if uploaded_file is None:
            st.warning("Please upload your resume.")
            st.stop()

        if not job_description.strip():
            st.warning("Please paste the job description.")
            st.stop()

        if not API_KEY:
            st.error(
                "API key not found. Please check your .env file."
            )
            st.stop()

        try:
            with st.spinner("Reading your resume..."):
                resume_text = extract_resume_text(uploaded_file)

            if not resume_text:
                st.error(
                    "Could not extract text from the resume. "
                    "Scanned PDFs may require OCR."
                )
                st.stop()

            # Limit very long inputs
            resume_text = resume_text[:25000]
            job_description = job_description.strip()[:15000]

            # Remove any previous result before a new analysis
            st.session_state.pop("final_report", None)

            with st.spinner("Analyzing resume and job requirements..."):
                analysis = analyze_resume(
                    resume_text,
                    job_description
                )

            with st.spinner("Generating your feedback report..."):
                final_report = generate_final_report(analysis)

            st.session_state["final_report"] = final_report

            st.success("Resume analysis completed!")

        except APITimeoutError:
            st.error(
                "The request timed out. Check your internet connection "
                "or try a shorter resume and job description."
            )

        except APIError as error:
            st.error(
                "There was a problem connecting to the Gemini API."
            )

            with st.expander("Error details"):
                st.code(str(error))

        except Exception as error:
            st.error("Could not complete the resume analysis.")

            with st.expander("Error details"):
                st.code(f"{type(error).__name__}: {error}")

    # Display the report
    if "final_report" in st.session_state:
        final_report = st.session_state["final_report"]

        st.divider()
        st.header("Analysis Results")

        for key, heading in REPORT_SECTIONS:
            st.subheader(heading)
            st.markdown(final_report[key])

        st.download_button(
            label="Download Report",
            data=create_report(final_report),
            file_name="resume_analysis.md",
            mime="text/markdown"
        )


if __name__ == "__main__":
    main()



