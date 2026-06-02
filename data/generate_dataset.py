# -*- coding: utf-8 -*-
"""
Ancile Talent Intelligence - Dataset Generator
250 rows, Kaggle-style realistic Indian tech recruitment data
Columns match app.py exactly: Candidate_ID, Name, Domain, Role, Skills,
Experience_Years, Location, Status, Client_Company, Match_Score, Joined_Month
"""
import pandas as pd
import random

random.seed(42)

FIRST_NAMES = [
    "Aarav","Priya","Rohan","Ananya","Kiran","Sneha","Vikram","Pooja","Arjun","Meera",
    "Rahul","Deepika","Sanjay","Kavya","Amit","Shreya","Nikhil","Tanvi","Raj","Divya",
    "Aditya","Nisha","Siddharth","Riya","Kartik","Dev","Swathi","Varun","Lakshmi","Harish",
    "Anjali","Suresh","Bhavna","Mohan","Geeta","Sunil","Lavanya","Mahesh","Padma","Ganesh",
    "Venkat","Usha","Prasad","Suma","Naveen","Hema","Rajesh","Shobha","Vijay","Sudha",
    "Krishna","Manoj","Sunitha","Ravi","Vani","Satish","Latha","Dinesh","Revathi","Ashok",
    "Chitra","Balaji","Saranya","Vinod","Malathi","Prakash","Geetha","Ramesh","Yamini","Srinivas",
]

LAST_NAMES = [
    "Kumar","Sharma","Reddy","Patel","Singh","Nair","Rao","Iyer","Gupta","Joshi",
    "Verma","Mehta","Shah","Menon","Pillai","Bhat","Agarwal","Sinha","Pandey","Tiwari",
    "Chauhan","Malhotra","Kapoor","Saxena","Dubey","Mishra","Shukla","Trivedi","Dasgupta","Bose",
    "Naidu","Shetty","Chatterjee","Murthy","Krishnan","Venkatesh","Subramanian","Rajan","Hegde","Kulkarni",
]

DOMAINS = {
    "Data Analytics": {
        "roles": ["Data Analyst", "BI Developer", "Data Engineer"],
        "skills": ["Python","SQL","Power BI","Excel","Tableau","Pandas","NumPy","R","Matplotlib","Seaborn","Statistics","Data Visualization"],
    },
    "Web Development": {
        "roles": ["Frontend Developer", "Full Stack Developer", "Backend Developer"],
        "skills": ["HTML","CSS","JavaScript","React","Node.js","MongoDB","Express","TypeScript","Vue.js","REST API","Git","Bootstrap","Redux"],
    },
    "Cloud & DevOps": {
        "roles": ["Cloud Engineer", "DevOps Engineer", "Solutions Architect"],
        "skills": ["AWS","Azure","GCP","Docker","Kubernetes","Terraform","Linux","CI/CD","Jenkins","Ansible","Git","Prometheus","Grafana"],
    },
    "AI/ML": {
        "roles": ["ML Engineer", "Data Scientist", "AI Research Intern"],
        "skills": ["Python","TensorFlow","Scikit-learn","Keras","NLP","PyTorch","OpenCV","Pandas","Statistics","Deep Learning","Hugging Face","LLMs"],
    },
    "Cybersecurity": {
        "roles": ["Security Analyst", "Penetration Tester", "SOC Analyst"],
        "skills": ["Network Security","Ethical Hacking","SIEM","Firewall","Linux","Python","Vulnerability Assessment","Wireshark","OWASP","Cryptography","Splunk","Metasploit"],
    },
    "Business Consulting": {
        "roles": ["Business Analyst", "IT Consultant", "Project Manager"],
        "skills": ["Excel","PowerPoint","Project Management","Agile","JIRA","Business Analysis","SQL","Stakeholder Management","SAP","CRM","ITIL","Scrum"],
    },
}

LOCATIONS = ["Hyderabad","Bangalore","Chennai","Mumbai","Delhi","Pune","Ahmedabad","Kolkata","Noida","Gurgaon","Coimbatore","Kochi","Jaipur","Chandigarh"]

CLIENTS = ["Volvo","TCS","Infosys","Wipro","Accenture","Capgemini","IBM","Deloitte","HCL","Tech Mahindra","Cognizant","Amazon","Microsoft","Google India","Zoho","Freshworks","Swiggy","Bosch","SAP Labs","Oracle"]

MONTHS = ["January","February","March","April","May","June","July","August","September","October","November","December"]

STATUS_MAP = {
    "Placed":   (0.50, 1.00),   # 50% of rows
    "Pending":  (0.20, 0.49),
    "Rejected": (0.07, 0.19),
}

def random_name(used):
    for _ in range(200):
        n = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        if n not in used:
            used.add(n)
            return n
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"

def match_score_for_status(status, exp):
    if status == "Placed":
        base = random.randint(62, 98)
        return round(min(base + exp * 0.8, 99), 1)
    if status == "Pending":
        return round(random.uniform(38, 73), 1)
    return round(random.uniform(20, 55), 1)

rows = []
used_names = set()
# Distribution: 125 Placed, 85 Pending, 40 Rejected
status_pool = (["Placed"] * 125) + (["Pending"] * 85) + (["Rejected"] * 40)
random.shuffle(status_pool)

for i, status in enumerate(status_pool):
    idx = i + 1
    domain = random.choice(list(DOMAINS.keys()))
    info   = DOMAINS[domain]
    role   = random.choice(info["roles"])
    exp    = round(random.uniform(0.5, 8.5), 1)

    n_skills = random.randint(3, 8)
    skills   = ", ".join(random.sample(info["skills"], min(n_skills, len(info["skills"]))))

    client = random.choice(CLIENTS) if status == "Placed" else "N/A"
    score  = match_score_for_status(status, exp)
    name   = random_name(used_names)
    loc    = random.choice(LOCATIONS)
    month  = random.choice(MONTHS)
    year   = random.choice([2024, 2025, 2026])

    rows.append({
        "Candidate_ID":    f"ANC{1000 + idx:04d}",
        "Name":            name,
        "Domain":          domain,
        "Role":            role,
        "Skills":          skills,
        "Experience_Years": exp,
        "Location":        loc,
        "Status":          status,
        "Client_Company":  client,
        "Match_Score":     score,
        "Joined_Month":    f"{month} {year}",
    })

df = pd.DataFrame(rows)
df.to_csv("candidates.csv", index=False)
print(f"Generated {len(df)} rows x {len(df.columns)} columns")
print(df["Status"].value_counts())
print(df["Domain"].value_counts())
