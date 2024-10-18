import streamlit as st 
import pdfkit
from pdfkit import configuration
import markdown
# CSS for styling the resume
css = """
    <style>
        html {
    font-size: 17px; /* Sets the root font size */
    }
        body {
            font-family:Verdana, Geneva, Tahoma, sans-serif;
            font-size: 17px;
            line-height: 1.6;
            margin: 20px;
        }
        h1 {
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 5px;
        }
        h2 {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 5px;
            margin-top: 20px;
        }
        h3 {
            font-size: 16px;
            font-weight: bold;
            margin-bottom: 5px;
            margin-top: 20px;
        }
        p, li {
            font-size: 17px;
            margin-bottom: 5px;
        }
        .section {
            margin-bottom: 15px;
        }
        hr {
            margin-top: 30px;
            margin-bottom: 25px;
        }
    </style>
"""
class UserInfo:
    def __init__(self, name,summary, address, phone_number, email,education,skills,projects,certifications):
        self.name = name
        self.summary=summary
        self.address = address
        self.phone_number = phone_number
        self.email = email
        self.education= education
        self.skills= skills
        self.projects= projects
        self.certifications= certifications
        
    def input_to_md(self):
        resume_md= f"""
# {self.name}
---
Address:{self.address}\n
Email:{self.email}\n  
Mobile Number:{self.phone_number}\n\n
---
## SUMMARY\n\n{self.summary}\n
---
"""
        resume_md += f"## EDUCATION\n"
        for edu in self.education:
            resume_md += f"**{edu['level']}**\n"
            resume_md += f"- {edu['institution']} | {edu['duration']}\n"
            resume_md += f" Score: {edu['score']}\n\n"
        resume_md += "---\n"    
        resume_md += f"## SKILLS\n"
        for skill in self.skills:
            resume_md += f"- {skill}\n"
        resume_md += "---\n"    
        resume_md += f"## PROJECTS\n"
        for project in self.projects:
            resume_md += f"**{project['project_name']}**\n\n"
            resume_md += f"{project['project_desc']}\n\n"
        resume_md += "---\n"    
        resume_md += f"## CERTIFICATIONS\n"
        for certificate in self.certifications:
            resume_md += f"**{certificate['certification_title']}**\n\n"
            resume_md += f"{certificate['certification_inst']}\n"
            resume_md += f"{certificate['completion_date']}\n\n"
             
        return resume_md
# Initialize session state variables if not present
if 'education' not in st.session_state:
    st.session_state.education = []     
if 'skills' not in st.session_state:
    st.session_state.skills = [] 
if 'projects' not in st.session_state:
    st.session_state.projects = []   
if 'certifications' not in st.session_state:
    st.session_state.certifications = []  
# function to take user input
def user_input():
    st.title('RESUME GENERATOR')
    name = st.text_input("Enter your name: ")
    summary=st.text_area("About Yourself")
    address = st.text_input("Enter your address: ")
    phone_number = st.text_input("Enter your phone number: ")
    email = st.text_input("Enter your email address: ")
    
    st.write("\nEducation")
    if st.checkbox("Add education details"):
        # Create input fields for education details
        level = st.text_input("Education Level:", key="level")
        institution = st.text_input("Institution Name:", key="institution")
        duration = st.text_input("Duration:", key="duration")
        score = st.text_input("Score:", key="score")

        # Button to save education details
        if st.button("Save Education"):
            st.session_state.education.append({
                "level": level,
                "institution": institution,
                "duration": duration,
                "score": score
            })
        # Display the list of saved education details
    if st.session_state.education:
        for idx, edu in enumerate(st.session_state.education):
            st.write(f"{idx+1}. {edu['level']} at {edu['institution']} ({edu['duration']}) - Score: {edu['score']}")
            
    st.write("\nSKILLS")  
    skill= st.text_input("Enter your skill: ")
    # Button to add each skill to the list
    if st.button("Add Skill"):
        st.session_state.skills.append(skill)
    if st.session_state.skills:
        for idx, sk in enumerate(st.session_state.skills):
            st.write(f"{idx+1}. {sk}")
    
    st.write("\nPROJECTS")
    if st.checkbox("Add Project"):
        project_name= st.text_input("Project Name:",key="project_name")
        project_desc= st.text_area("Project Description: ",key="project_desc")
        if st.button("Save",key="save_button_project"):
            st.session_state.projects.append({
                "project_name": project_name, 
                "project_desc": project_desc
                })
    if st.session_state.projects:
        for idx, project in enumerate(st.session_state.projects):
            st.write(f"{idx+1}. **{project['project_name']}** \n {project['project_desc']}")
            
    st.write("\nCertifications")
    if st.checkbox("Add Certificate"):
        certification_title= st.text_input("Certification Title:",key="certification_title")
        certification_inst= st.text_input("Institution/Organization: ",key="certification_inst")
        completion_date=st.text_input("Completion Date: ",key="completion_date")
        if st.button("Save",key="save_button_certificate"):
            st.session_state.certifications.append({
                "certification_title": certification_title, 
                "certification_inst": certification_inst,
                "completion_date": completion_date
                })
    if st.session_state.certifications:
        for idx, cert in enumerate(st.session_state.certifications):
            st.write(f"{idx+1}. **{cert['certification_title']}** :{cert['certification_inst']}-{cert['completion_date']}")
            
    return UserInfo(name,summary, address, phone_number, email,st.session_state.education,st.session_state.skills,st.session_state.projects,st.session_state.certifications)

# Creating an instance of the UserInfo class
user = user_input()
resume_md= user.input_to_md()
st.markdown(resume_md)

# Save the Markdown content to a file
with open("resume.md", "w") as file:
    file.write(resume_md)
 
# Specify the path to wkhtmltopdf.exe
config = configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')    

if st.button("Confirm Download"):
    # Convert Markdown to HTML
    resume_html = markdown.markdown(resume_md)
    resume_html = css + resume_html
    # Generate PDF from HTML
    options = {
    'page-size': 'A4',         # Set page size to A4
    'margin-top': '15mm',      # Set top margin
    'margin-right': '15mm',    # Set right margin
    'margin-bottom': '15mm',   # Set bottom margin
    'margin-left': '15mm',     # Set left margin
    'orientation': 'Portrait', # Portrait orientation
}

    pdf = pdfkit.from_string(resume_html, False, options=options, configuration=config)
    
    # Provide the download button for the generated PDF
    st.download_button(label="Download PDF", data=pdf, file_name="resume.pdf", mime='application/pdf')