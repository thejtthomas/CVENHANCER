import openai
import os
import streamlit as st
from dotenv import load_dotenv
import pandas as pd
import pdfkit

wkhtmltopdf_path = 'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'
load_dotenv()

# Set up OpenAI API key
client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


# Chat-based language model system messages
system_messages = f"""Enhance a CV for a specific job application. Provide details about your skills, experience, and the job you are applying for. 
Specify the job title, key responsibilities, and any specific requirements mentioned in the job description.
Ensure to include the following elements in the enhanced CV:
1. Personal Information
2. Professional Summary
3. Skills
4. Work Experience
5. Education
6. Certifications
7. Projects (if applicable)
8. Contact Information

Provide response in the following format:
Enhanced CV:
<Enhanced CV Content>
"""

def get_enhanced_cv(prompt):
    # Call OpenAI API for CV enhancement
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_messages},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content

# Main part of the Streamlit app
def cv_enhancer():
    st.header("CV Enhancer")
    st.subheader("Enhance Your CV for a Specific Job")

    # User input for CV enhancement
    job_title = st.text_input("Enter the Job Title:")
    responsibilities = st.text_area("Key Responsibilities in the Job Description:")
    requirements = st.text_area("Specific Requirements in the Job Description:")
    user_skills = st.text_area("Enter Your Skills (comma-separated):")
    experience = st.text_area("Work Experience:")
    education = st.text_area("Education:")
    certifications = st.text_area("Certifications:")
    projects = st.text_area("Projects (if applicable):")
    contact_info = st.text_area("Contact Information:")

    user_prompt = f"Enhance my CV for the position of {job_title}. Skills: {user_skills}. Experience: {experience}. Education: {education}. Certifications: {certifications}. Projects: {projects}. Contact Information: {contact_info}. Job Description: {responsibilities}. Requirements: {requirements}"

    if st.button("Generate Enhanced CV"):
        if job_title and user_skills and experience and education and contact_info:
            # Get enhanced CV from OpenAI
            enhanced_cv = get_enhanced_cv(user_prompt)
            st.success("Enhanced CV:")
            st.write(enhanced_cv)

            # Convert to HTML
            html_content = f"""
            <html>
            <head>
                <style>
                    /* Add your custom CSS styling for a classy CV here */
                    /* Example: */
                    body {{
                        font-family: 'Arial', sans-serif;
                        margin: 20px;
                    }}
                    h1, h2, h3, p {{
                        margin-bottom: 10px;
                    }}
                    /* Add more styles as needed */
                </style>
            </head>
            <body>
                {enhanced_cv.replace('\n','<br>')}
            </body>
            </html>
            """
            pdfkit_config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
            pdf = pdfkit.from_string(enhanced_cv, False, configuration=pdfkit_config)
            st.success("🎉 Your CV was generated!")
            st.download_button(
                            "⬇️ Download PDF",
                            data=pdf,
                            file_name="cv.pdf",
                            mime="application/octet-stream",
            )

           
        

           

            # Provide download link for the PDF
            st.markdown(f"[Download PDF]({pdf_file_path})")

        else:
            st.warning("Please fill in the required details.")

# Run the Streamlit app
if __name__ == "__main__":
    cv_enhancer()
