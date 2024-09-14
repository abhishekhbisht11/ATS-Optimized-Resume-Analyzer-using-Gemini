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

load_dotenv()
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')  # Your email address
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')  # Your email password

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-pro')

def  get_gemini_response(input):
    response=model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader=PyPDF2.PdfReader(uploaded_file)
    text=''
    for page_num in range(len(reader.pages)):
        page=reader.pages[page_num]
        text+= str(page.extract_text()) 
    return text  
  
input_prompt="""
 As a expierienced ATS (Applicant Tracking System), proficient in the technical domain encompassing Software Engineering, Data Science,
 Data Analysis, Big Data Engineering, Web Developer, Mobile App Developer, Dev Ops Engineer, Machine Learning Engineer, Cybersecurity 
 Analyst, Cloud Solutions Architect, Database Administrator, Network Engineer, AI Engineer, Systems Analyst, Full Stack Developer, UI/UX 
 Designer, IT Project Manager, and additional specialized areas, your objective is to meticulously assess  resumes against provided job 
 description. In a fiercely competitive job market, your expertise is crucial in  offering not notch guidance for resume enhancement.  
 Assign precise matching percentages based on the JD(Job Description) and meticulously identify any missing keywords with utmost accuracy.
 resume:{text}
 description:{jd} 

 I want the response in the following structure:
 the first line indicates the percentage match with the job description(JD).
 The second line presents a list of missing keywords.
 The third section provides a profile summary.

 Mention the title for all the three sections.
 While generating the response put some space to seprate all the three section.
 """

## streamlit UI  INTRODUCTION
st.set_page_config(page_title="Resume ATS Tracker",layout="wide") 

avs.add_vertical_space(4) 

col1, col2 = st.columns([3,2]) 
with col1: 
         st.title("CareerCraft") 
         st.header("Navigate the Job Market with Confidence!") 
         st.markdown("""<p style='text-align: justify;'> Introducing CareerCraft, an ATS-Optimized Resume Analyzer - your ultimate solution for optimizing job applications and accelerating
                      career growth. Our innovative platform leverages advanced ATS technology to provide job 
                     seekers with valuable insights into their resume com patibility with job descriptions. 
                     From resume optimization and skill enhancement to career progression guidance, CareerCraft 
                      empowers users to stand out in today's competitive job market. Streamline your job application
                      process, enhance your skills, and navigate your career path with confidence. Join CareerCraft 
                     today and unlock new opportunities for professional success! 
</p>""", unsafe_allow_html=True)

with col2: 
         st.image('https://cdn.dribbble.com/userupload/12500996/file/original-b458fe398a6d7f4e9999ce66ec856ff9.gif', use_column_width=True) 

avs.add_vertical_space(10)

## streamlit UI  WIDE RANGE OF OFFERING
col1, col2 = st.columns([3,2]) 
with col2: 
      st.header("Wide Range of Offerings") 
      st.write('ATS Optimized Resume Analysis') 
      st.write('Resume Optimization') 
      st.write('Skill Enhancement') 
      st.write('Career Progression Guidance') 
      st.write('Tailored Profile Summaries') 
      st.write('Streamlined Application Process') 
      st.write('Personalized Recommendations') 
      st.write('Efficient Career Navigation') 

with col1: 
    img1 = Image.open("images/icon1.jpg")
    st.image(img1, use_column_width=True)


avs.add_vertical_space(10)

## Resume ATS Tracking Application:
col1, col2 =st.columns([3,2]) 
with col1: 
    st.markdown("<h1 style='text-align: center;'>Embark on \
        Your Career Adventure</h1>", unsafe_allow_html=True)
    jd=st.text_area("Paste the Job Description") 
    uploaded_file=st.file_uploader("Upload Your Resume", type="pdf", 
                                   help="Please uplaod the pdf") 
    submit = st.button("Submit") 

if submit: 
     if uploaded_file is not None: 
        text=input_pdf_text(uploaded_file) 
        response=get_gemini_response(input_prompt)
        st.subheader(response) 

with col2: 
    img2 = Image.open("images/icon2.jpg")
    st.image(img2, use_column_width=True) 
avs.add_vertical_space(10)

## FAQ
col1, col2 =st.columns([2, 3]) 
with col2: 
    st.markdown("<h1 style='text-align: center;'>FAQ</h1>", unsafe_allow_html=True)
    st.write("Question: How does CareerCraft analyze resumes and job descriptions?") 
    st.write("""Answer: CareerCraft uses advanced algorithms to analyze resumes and job descriptions,
             
              identifying key keywords and assessing compatibility between the two.""") 
    avs.add_vertical_space(3) 
    st.write("Question: Can CareerCraft suggest improvements for my resume?") 
    st.write("""Answer: Yes, CareerCraft provides personalized recommendations to optimize your resume
              for specific job openings, including suggestions for missing keywords and alignment with desired job roles.""")

    avs.add_vertical_space(3) 
    st. write("Question: Is CareerCraft suitable for both entry-level and experienced professionals?") 
    st.write("""Answer: Absolutely! CareerCraft caters to job seekers at all career stages, offering 
             tailored insights and guidance to enhance their resumes and advance their careers.""")

with col1: 
     img3 = Image.open("images/icon3.jpg") 
     st.image(img3, use_column_width=True) 
avs.add_vertical_space(3) 



# contact us column build by me personally uses smtp to send email 
col1, col2 = st.columns([2, 3])  # Adjust column widths as needed

with col1:
    st.subheader("Contact Us")
    st.write("Have any questions or feedback? Feel free to reach out!")

    # Input fields for user
    contact_email = st.text_input("Your Email", key="contact_email")
    message = st.text_area("Your Message", key="contact_message")

    # Send button logic
    if st.button("Send", key="contact_submit"):
        if contact_email and message:
            try:
                # Create the email
                msg = MIMEMultipart()
                msg['From'] = EMAIL_ADDRESS
                msg['To'] = "abhishekhbisht11@gmail.com"  # Replace with your support email
                msg['Subject'] = "New Contact Us Message"

                # Email body
                body = f"From: {contact_email}\n\nMessage:\n{message}"
                msg.attach(MIMEText(body, 'plain'))

                # Connect to SMTP server and send email  using gmail
                with smtplib.SMTP('smtp.gmail.com', 587) as server:  # Use your SMTP server details
                    server.starttls()  # Secure the connection
                    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                    server.send_message(msg)

                st.success("Thank you for contacting us! We'll get back to you soon.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please fill in both your email and message.")
# Add this after all other UI element
st.markdown("""---""", unsafe_allow_html=True)  # Add a separator

# Center align text using CSS
footer_text = st.markdown("""<p style='text-align: center;'>Developed by Abhishekh Bisht! &copy; 2024</p>""", unsafe_allow_html=True)   