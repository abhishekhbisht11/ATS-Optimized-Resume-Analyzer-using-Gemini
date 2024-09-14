import os
import streamlit as st

# Importing dotenv safely
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    st.error("The 'dotenv' package is missing. Please install it using 'pip install python-dotenv'.")

# Import other necessary modules
try:
    import google.generativeai as genai
    from streamlit_extras import add_vertical_space as avs
    import PyPDF2
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from PIL import Image
except ImportError as e:
    st.error(f"Module {str(e).split()[-1]} is missing. Please install it using the appropriate pip install command.")

# Ensure email credentials are loaded
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
    st.error("Email credentials are missing. Please ensure they are present in the .env file.")

# Configure Google Generative AI
try:
    genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error(f"Error with Google API configuration: {e}")

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
        text = ""
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
    career growth. Our innovative platform leverages advanced ATS technology to provide job seekers with valuable insights into their resume compatibility with job descriptions.</p>
    """, unsafe_allow_html=True)

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
