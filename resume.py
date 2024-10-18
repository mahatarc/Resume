import streamlit as st 
class UserInfo:
    def __init__(self, name, address, phone_number, email,education,skills,projects):
        self.name = name
        self.address = address
        self.phone_number = phone_number
        self.email = email
        self.education= education
        self.skills= skills
        self.projects= projects
        
    def input_to_md(self):
        resume_md= f"""
# {self.name}

**Address**: {self.address}  
**Email**: {self.email}  
**Mobile Number**: {self.phone_number}\n
"""
        resume_md += f"## EDUCATION\n"
        for edu in self.education:
            resume_md += f"### {edu['level']}\n"
            resume_md += f"- {edu['institution']} / {edu['duration']}\n"
            resume_md += f" **Score**: {edu['score']}\n\n"
            
        resume_md += f"## SKILLS\n"
        for skill in self.skills:
            resume_md += f"- {skill}\n"
        resume_md += f"## PROJECTS\n"
        
        for project in self.projects:
            resume_md += f"**{project['project_name']}**\n\n"
            resume_md += f"{project['project_desc']}\n"
        return resume_md
# Initialize session state variables if not present
if 'education' not in st.session_state:
    st.session_state.education = []        
# function to take user input
def user_input():
    st.title('RESUME GENERATOR')
    name = st.text_input("Enter your name: ")
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
    skills=[]
    skill= st.text_input("Enter your skill: ")
    skills.append(skill)
    st.write("\nPROJECTS")
    projects=[]
    project_name= st.text_input("Enter your project name: ")
    project_desc= st.text_area("Enter your project description: ")
    if st.button("Add Project"):
        projects.append({"project_name": project_name, "project_desc": project_desc})
    return UserInfo(name, address, phone_number, email,st.session_state.education,skills,projects)

# Creating an instance of the UserInfo class
user = user_input()
resume_md= user.input_to_md()
st.markdown(resume_md)
# Save the Markdown content to a file
with open("resume.md", "w") as file:
    file.write(resume_md)