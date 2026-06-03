import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

np.random.seed(42)
random.seed(42)

# ── Domain → Roles → Skills ──────────────────────────────────────────────────
domain_config = {
    "AI/ML": {
        "roles": ["ML Engineer", "AI Researcher", "NLP Engineer", "Computer Vision Engineer", "Deep Learning Engineer"],
        "skills_pool": ["Python", "TensorFlow", "PyTorch", "Scikit-learn", "NLP", "Computer Vision",
                        "Deep Learning", "Keras", "Hugging Face", "OpenCV", "MLflow", "BERT", "LLMs", "NumPy", "Pandas"],
        "count": 1200
    },
    "Data Analytics": {
        "roles": ["Data Analyst", "Business Analyst", "BI Developer", "Data Engineer", "Analytics Consultant"],
        "skills_pool": ["Python", "SQL", "Power BI", "Tableau", "Excel", "Pandas", "NumPy",
                        "Statistics", "R", "Google Analytics", "Looker", "Spark", "ETL", "Data Visualization"],
        "count": 1200
    },
    "Data Science": {
        "roles": ["Data Scientist", "Quantitative Analyst", "Research Scientist", "ML Analyst"],
        "skills_pool": ["Python", "R", "SQL", "Machine Learning", "Statistics", "Pandas", "Scikit-learn",
                        "Matplotlib", "Seaborn", "Jupyter", "A/B Testing", "Bayesian Analysis", "Feature Engineering"],
        "count": 800
    },
    "Web Development": {
        "roles": ["Frontend Developer", "Backend Developer", "Full Stack Developer", "React Developer", "Node.js Developer"],
        "skills_pool": ["HTML", "CSS", "JavaScript", "React", "Node.js", "Express", "MongoDB",
                        "TypeScript", "Vue.js", "Angular", "REST APIs", "GraphQL", "Next.js", "Django", "Flask"],
        "count": 1000
    },
    "Cybersecurity": {
        "roles": ["Security Analyst", "Penetration Tester", "SOC Analyst", "IAM Engineer", "Security Engineer"],
        "skills_pool": ["Network Security", "Ethical Hacking", "SIEM", "Firewalls", "Linux",
                        "Vulnerability Assessment", "Python", "OWASP", "ISO 27001", "Incident Response",
                        "Cloud Security", "Zero Trust", "CISSP", "CompTIA Security+"],
        "count": 900
    },
    "Cloud Engineering": {
        "roles": ["Cloud Architect", "AWS Engineer", "Azure Engineer", "GCP Engineer", "Cloud DevOps Engineer"],
        "skills_pool": ["AWS", "Azure", "GCP", "Terraform", "Kubernetes", "Docker",
                        "CI/CD", "Linux", "Networking", "IAM", "CloudFormation", "Ansible", "Jenkins"],
        "count": 800
    },
    "DevOps": {
        "roles": ["DevOps Engineer", "Site Reliability Engineer", "Platform Engineer", "Build Engineer"],
        "skills_pool": ["Docker", "Kubernetes", "Jenkins", "CI/CD", "Ansible", "Terraform",
                        "Linux", "Python", "Shell Scripting", "Git", "Prometheus", "Grafana", "AWS"],
        "count": 600
    },
    "Mobile Development": {
        "roles": ["Android Developer", "iOS Developer", "Flutter Developer", "React Native Developer"],
        "skills_pool": ["Flutter", "Dart", "React Native", "Swift", "Kotlin", "Java",
                        "Android SDK", "iOS SDK", "Firebase", "REST APIs", "UI/UX", "App Store"],
        "count": 500
    },
    "Business Consulting": {
        "roles": ["Business Consultant", "Strategy Analyst", "Management Consultant", "IT Consultant"],
        "skills_pool": ["Business Analysis", "Strategy", "PowerPoint", "Excel", "Project Management",
                        "Stakeholder Management", "Process Improvement", "Agile", "JIRA", "Communication"],
        "count": 900
    },
    "Finance": {
        "roles": ["Financial Analyst", "Investment Analyst", "Accountant", "Risk Analyst", "CFO Analyst"],
        "skills_pool": ["Excel", "Financial Modeling", "Accounting", "SAP", "SQL", "Power BI",
                        "Tally", "Taxation", "Audit", "Bloomberg", "Valuation", "CFA", "Python"],
        "count": 700
    },
    "HR": {
        "roles": ["HR Executive", "Talent Acquisition", "HR Business Partner", "Recruiter", "L&D Specialist"],
        "skills_pool": ["Recruitment", "Onboarding", "HRMS", "Communication", "LinkedIn Recruiter",
                        "Excel", "Employee Engagement", "Performance Management", "Labor Law", "ATS"],
        "count": 600
    },
    "Sales": {
        "roles": ["Sales Executive", "Account Manager", "Customer Success Manager", "Business Development"],
        "skills_pool": ["CRM", "Salesforce", "Communication", "Negotiation", "Excel",
                        "Lead Generation", "Cold Calling", "B2B Sales", "HubSpot", "Client Relations"],
        "count": 700
    },
    "Mechanical Engineering": {
        "roles": ["Mechanical Engineer", "Design Engineer", "Manufacturing Engineer", "Quality Engineer"],
        "skills_pool": ["AutoCAD", "SolidWorks", "CATIA", "ANSYS", "Thermodynamics",
                        "Manufacturing", "GD&T", "Six Sigma", "MATLAB", "Lean Manufacturing"],
        "count": 500
    },
    "Civil Engineering": {
        "roles": ["Civil Engineer", "Structural Engineer", "Site Engineer", "Project Manager"],
        "skills_pool": ["AutoCAD", "STAAD Pro", "Project Management", "Surveying",
                        "Structural Analysis", "Construction Management", "Revit", "MS Project"],
        "count": 500
    },
    "Electronics & Communication": {
        "roles": ["ECE Engineer", "Embedded Systems Engineer", "VLSI Engineer", "RF Engineer", "IoT Engineer"],
        "skills_pool": ["Embedded C", "Arduino", "Raspberry Pi", "MATLAB", "VHDL",
                        "PCB Design", "IoT", "Python", "Signal Processing", "Microcontrollers"],
        "count": 600
    },
    "Healthcare": {
        "roles": ["Nurse", "Pharmacist", "Healthcare Manager", "Clinical Data Analyst", "Medical Coder"],
        "skills_pool": ["Patient Care", "Medical Coding", "ICD-10", "EMR", "Clinical Research",
                        "Pharmacology", "Healthcare IT", "Excel", "HIPAA Compliance"],
        "count": 400
    },
    "Project Management": {
        "roles": ["Project Manager", "Scrum Master", "Agile Coach", "Program Manager"],
        "skills_pool": ["PMP", "Agile", "Scrum", "JIRA", "MS Project", "Risk Management",
                        "Stakeholder Management", "Budgeting", "Communication", "Confluence"],
        "count": 500
    },
}

indian_cities = [
    "Bangalore", "Hyderabad", "Chennai", "Pune", "Mumbai",
    "Delhi", "Noida", "Gurgaon", "Kochi", "Ahmedabad",
    "Vijayawada", "Visakhapatnam", "Kolkata", "Jaipur", "Chandigarh"
]

client_companies = [
    "Microsoft", "Google", "Amazon", "Infosys", "TCS",
    "Accenture", "Capgemini", "Deloitte", "Wipro", "Cognizant",
    "HCL", "IBM", "Oracle", "SAP", "Salesforce",
    "Tech Mahindra", "Hexaware", "Mphasis", "LTIMindtree", "Persistent"
]

first_names = [
    "Rahul", "Priya", "Arjun", "Sneha", "Kiran", "Divya", "Amit", "Pooja",
    "Vijay", "Ananya", "Ravi", "Meera", "Suresh", "Lakshmi", "Naveen",
    "Kavitha", "Sanjay", "Deepa", "Rajesh", "Nithya", "Arun", "Sowmya",
    "Harish", "Bhavana", "Ganesh", "Swathi", "Venkat", "Padma", "Krishna",
    "Sindhu", "Mohan", "Rekha", "Prasad", "Uma", "Srikanth", "Anjali",
    "Manoj", "Lavanya", "Ashok", "Revathi", "Vishal", "Keerthi", "Sunil",
    "Nandini", "Prakash", "Sirisha", "Ramesh", "Spandana", "Dinesh", "Asha"
]

last_names = [
    "Sharma", "Reddy", "Kumar", "Patel", "Singh", "Rao", "Nair", "Iyer",
    "Gupta", "Verma", "Joshi", "Mehta", "Pillai", "Menon", "Chaudhary",
    "Naidu", "Shetty", "Bhat", "Mishra", "Tiwari", "Agarwal", "Saxena",
    "Kulkarni", "Desai", "Shah", "Kapoor", "Malhotra", "Khanna", "Chopra"
]

months = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]

statuses = ["Placed", "In Process", "Not Placed", "On Bench", "Offer Accepted", "Offer Declined"]
status_weights = [0.40, 0.25, 0.15, 0.10, 0.07, 0.03]

education_levels = ["B.Tech", "B.E.", "B.Sc", "M.Tech", "MBA", "MCA", "BCA", "M.Sc", "B.Com", "M.Com"]

records = []
candidate_id = 10001

for domain, config in domain_config.items():
    for _ in range(config["count"]):
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        role = random.choice(config["roles"])
        num_skills = random.randint(3, 7)
        skills = ", ".join(random.sample(config["skills_pool"], min(num_skills, len(config["skills_pool"]))))
        experience = round(random.uniform(0.5, 12.0), 1)
        location = random.choice(indian_cities)
        status = random.choices(statuses, weights=status_weights)[0]
        client = random.choice(client_companies) if status in ["Placed", "Offer Accepted"] else "N/A"
        match_score = random.randint(55, 98) if status == "Placed" else random.randint(30, 75)
        joined_month = random.choice(months) + " " + random.choice(["2024", "2025", "2026"])
        education = random.choice(education_levels)
        salary_lpa = round(random.uniform(3.0, 35.0), 1) if status == "Placed" else 0.0

        records.append({
            "Candidate_ID": f"ANC{candidate_id}",
            "Name": name,
            "Education": education,
            "Domain": domain,
            "Role": role,
            "Skills": skills,
            "Experience_Years": experience,
            "Location": location,
            "Status": status,
            "Client_Company": client,
            "Match_Score": match_score,
            "Salary_LPA": salary_lpa,
            "Joined_Month": joined_month,
        })
        candidate_id += 1

df = pd.DataFrame(records)
df.to_csv("/home/claude/ancile_talent_dataset.csv", index=False)

print(f"✅ Dataset generated: {len(df)} records")
print(f"\n📊 Domain Distribution:")
print(df["Domain"].value_counts().to_string())
print(f"\n📈 Status Distribution:")
print(df["Status"].value_counts().to_string())
print(f"\n🏙️ Top Locations:")
print(df["Location"].value_counts().head(5).to_string())
print(f"\n💼 Sample Records:")
print(df.head(3).to_string())
