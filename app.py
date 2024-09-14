from dotenv import load_dotenv
import streamlit as st
from streamlit_extras import add_vertical_space as avs
import google.generativeai as genai
import os
import PyPDF2
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from PIL import Image

# Load environment variables
load_dotenv()

EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')  # Your email address
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')  # Your email password

# Check if the environment variables are correctly loaded
if EMAIL_ADDRESS is None or EMAIL_PASSWORD is None:
    st.error("Error: Email credentials not found. Check your .env file.")

# Configure Generative AI
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-pro')

# Function to generate response from Gemini model
def get_gemini_response(input):
    try:
        response = model.generate_content(input)
        return response.text
    except Exception as e:
        st.error(f"Error generating response from Gemini API: {e}")
        return ""

# Function to extract text from PDF
def input_pdf_text(uploaded_file):
    try:
        reader = PyPDF2.PdfReader(uploaded_file)
        text = ''
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += str(page.extract_text())
        return text
    except Exception as e:
        st.error(f"Error reading PDF file: {e}")
        return ""

# Streamlit UI Introduction
st.set_page_config(page_title="Resume ATS Tracker", layout="wide")

avs.add_vertical_space(4)

# CareerCraft Introduction
col1, col2 = st.columns([3, 2])
with col1:
    st.title("CareerCraft")
    st.header("Navigate the Job Market with Confidence!")
    st.markdown("""
    <p style='text-align: justify;'>Introducing CareerCraft, an ATS-Optimized Resume Analyzer - your ultimate solution for optimizing job applications and accelerating
    career growth. Our innovative platform leverages advanced ATS technology to provide job seekers with valuable insights into their resume compatibility with job descriptions.
    From resume optimization and skill enhancement to career progression guidance, CareerCraft empowers users to stand out in today's competitive job market.</p>""", unsafe_allow_html=True)

with col2:
    st.image('https://cdn.dribbble.com/userupload/12500996/file/original-b458fe398a6d7f4e9999ce66ec856ff9.gif', use_column_width=True)

avs.add_vertical_space(10)

# Resume ATS Tracking Application
col1, col2 = st.columns([3, 2])
with col1:
    st.markdown("<h1 style='text-align: center;'>Embark on Your Career Adventure</h1>", unsafe_allow_html=True)
    jd = st.text_area("Paste the Job Description")
    uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the PDF")

    submit = st.button("Submit")

    if submit:
        if uploaded_file is not None:
            text = input_pdf_text(uploaded_file)
            input_prompt = f"""
            As an experienced ATS, proficient in Software Engineering, Data Science, etc., assess the resume against the job description.
            Resume: {text}
            Description: {jd}

            Structure:
            1. Percentage match
            2. Missing keywords
            3. Profile summary
            """
            response = get_gemini_response(input_prompt)
            st.subheader(response)
        else:
            st.warning("Please upload a resume.")

with col2:
    img2 = Image.open("images/icon2.jpg")
    st.image(img2, use_column_width=True)

avs.add_vertical_space(10)

# FAQ Section
col1, col2 = st.columns([2, 3])
with col2:
    st.markdown("<h1 style='text-align: center;'>FAQ</h1>", unsafe_allow_html=True)
    st.write("**Question**: How does CareerCraft analyze resumes and job descriptions?")
    st.write("**Answer**: CareerCraft uses advanced algorithms to analyze resumes and job descriptions, identifying key keywords and assessing compatibility.")
    avs.add_vertical_space(3)

    st.write("**Question**: Can CareerCraft suggest improvements for my resume?")
    st.write("**Answer**: Yes, CareerCraft provides personalized recommendations to optimize your resume for specific job openings.")

    avs.add_vertical_space(3)

    st.write("**Question**: Is CareerCraft suitable for both entry-level and experienced professionals?")
    st.write("**Answer**: Absolutely! CareerCraft caters to job seekers at all career stages, offering tailored insights and guidance.")

with col1:
    img3 = Image.open("images/icon3.jpg")
    st.image(img3, use_column_width=True)

avs.add_vertical_space(3)

# Contact Us Section
col1, col2 = st.columns([2, 3])
with col1:
    st.subheader("Contact Us")
    st.write("Have any questions or feedback? Feel free to reach out!")

    contact_email = st.text_input("Your Email", key="contact_email")
    message = st.text_area("Your Message", key="contact_message")

    if st.button("Send", key="contact_submit"):
        if contact_email and message:
            try:
                msg = MIMEMultipart()
                msg['From'] = EMAIL_ADDRESS
                msg['To'] = "abhishekhbisht11@gmail.com"  # Replace with your support email
                msg['Subject'] = "New Contact Us Message"

                body = f"From: {contact_email}\n\nMessage:\n{message}"
                msg.attach(MIMEText(body, 'plain'))

                with smtplib.SMTP('smtp.gmail.com', 587) as server:
                    server.starttls()
                    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                    server.send_message(msg)

                st.success("Thank you for contacting us! We'll get back to you soon.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please fill in both your email and message.")

# Footer
st.markdown("""---""", unsafe_allow_html=True)
footer_text = st.markdown("""<p style='text-align: center;'>Developed by Abhishekh Bisht! &copy; 2024</p>""", unsafe_allow_html=True)
