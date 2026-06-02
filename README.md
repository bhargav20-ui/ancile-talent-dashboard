# 🚀 Ancile Talent Intelligence Dashboard

An AI-powered Recruitment Analytics and Talent Intelligence Platform developed using Python, Streamlit, Pandas, Plotly, and Machine Learning techniques.

The project helps recruiters and talent acquisition teams analyze candidate data, monitor hiring trends, identify in-demand skills, track placement outcomes, and recommend suitable job roles through an AI-based skill matching engine.

---

# 📌 Project Overview

Modern recruitment processes generate large volumes of candidate data across multiple domains. Analyzing candidate skills, experience levels, placement outcomes, and role suitability manually is time-consuming and inefficient.

The **Ancile Talent Intelligence Dashboard** provides a centralized platform for:

* Recruitment Analytics
* Candidate Intelligence
* Skill Demand Analysis
* Placement Tracking
* Talent Insights
* AI-Based Role Recommendations

---

# ✨ Key Features

## 📊 Executive Dashboard

Provides high-level recruitment insights through:

* Total Candidate Count
* Placement Rate
* Average Match Score
* Average Experience
* Salary Insights
* Domain Distribution

---

## 📈 Recruitment Analytics

Interactive analytics and visualizations including:

* Hiring Trends Analysis
* Placement Funnel
* Skill Demand Analysis
* Domain-wise Candidate Distribution
* Client-wise Recruitment Insights
* Experience Distribution
* Monthly Recruitment Trends

---

## 🤖 AI Skill Matcher

An intelligent recommendation engine built using:

* TF-IDF Vectorization
* Cosine Similarity
* Skill Gap Analysis

### Input

```text
Python, SQL, Excel, Power BI
```

### Output

```text
Recommended Role: Data Analyst
Match Score: 92%
Missing Skills: Tableau, Statistics
```

Features:

* Role Recommendations
* Match Score Calculation
* Missing Skill Detection
* Career Suggestions

---

## 🔍 Candidate Explorer

Advanced candidate search and filtering:

* Search by Candidate Name
* Filter by Domain
* Filter by Status
* Filter by Experience
* View Detailed Candidate Profiles

---

## 📁 Dataset Explorer

Interactive dataset management:

* Explore Candidate Records
* Search and Filter Data
* Download Dataset
* Real-Time Data Inspection

---

# 🏗️ System Architecture

```text
Candidate Dataset (CSV)
           │
           ▼
Data Processing (Pandas)
           │
           ▼
Analytics Engine (Plotly)
           │
           ▼
Streamlit Dashboard
           │
           ▼
AI Skill Matching Engine
(TF-IDF + Cosine Similarity)
           │
           ▼
Role Recommendations
```

---

# 🛠️ Technology Stack

| Category                 | Technology                 |
| ------------------------ | -------------------------- |
| Programming Language     | Python                     |
| Dashboard Framework      | Streamlit                  |
| Data Processing          | Pandas                     |
| Data Visualization       | Plotly                     |
| Machine Learning         | Scikit-learn               |
| AI Recommendation Engine | TF-IDF + Cosine Similarity |
| Dataset Storage          | CSV                        |
| Version Control          | Git & GitHub               |

---

# 📂 Project Structure

```text
ancile-talent-dashboard/
│
├── app.py
├── requirements.txt
├── README.md
│
├── assets/
│   └── ancile_logo.png
│
├── data/
│   ├── candidates.csv
│   └── generate_dataset.py
│
├── modules/
│   ├── __init__.py
│   ├── ai_matcher.py
│   ├── analytics.py
│   └── data_loader.py
│
├── notebooks/
│   └── data_cleaning.py
│
└── .streamlit/
    └── config.toml
```

---

# 🤖 AI Skill Matching Workflow

### Step 1

Candidate enters skills

```text
Python, SQL, Power BI
```

### Step 2

Skills are converted into TF-IDF vectors.

### Step 3

Job role profiles are vectorized.

### Step 4

Cosine Similarity calculates the similarity between candidate skills and role requirements.

### Step 5

Top matching roles are identified.

### Step 6

Missing skills are highlighted.

### Step 7

Career recommendations are generated.

---

# 📊 Sample Roles Supported

* Data Analyst
* Business Analyst
* Data Engineer
* Data Scientist
* Machine Learning Engineer
* Frontend Developer
* Backend Developer
* Full Stack Developer
* Cloud Engineer
* DevOps Engineer
* Security Analyst
* SOC Analyst
* IT Consultant
* Project Manager

---

# 📈 Dataset Information

The project utilizes a recruitment dataset containing:

* Candidate Information
* Skills
* Experience
* Domain
* Applied Role
* Client Company
* Placement Status
* Match Score
* Salary Information

### Domains Covered

* Data Analytics
* Artificial Intelligence & Machine Learning
* Cybersecurity
* Cloud & DevOps
* Software Development
* IT Consulting

---

# 🚀 Installation & Setup

## Clone Repository

```bash
git clone https://github.com/bhargav20-ui/ancile-talent-dashboard.git
cd ancile-talent-dashboard
```

## Create Virtual Environment

```bash
python -m venv venv
```

## Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run Application

```bash
streamlit run app.py
```

---

# 🎯 Learning Outcomes

This project strengthened practical skills in:

* Python Programming
* Data Analytics
* Data Visualization
* Machine Learning Fundamentals
* Dashboard Development
* Business Intelligence
* Git & GitHub
* Software Project Development
* Technical Documentation

---

# 💡 Future Enhancements

Planned improvements:

* Resume PDF Upload
* Automatic Skill Extraction
* Live Database Integration
* Real-Time Recruitment Analytics
* User Authentication
* Dashboard Export to PDF
* Cloud Deployment
* Advanced AI Recommendations

---

# 👨‍💻 Developer

### N. Vinay Venkata Bhargav

Designed and developed the Ancile Talent Intelligence Dashboard as an AI-powered recruitment analytics platform.

### Key Contributions

* Developed the complete Streamlit dashboard
* Built recruitment analytics visualizations using Plotly
* Implemented AI Skill Matching using TF-IDF and Cosine Similarity
* Processed and analyzed candidate datasets using Pandas
* Designed responsive UI components
* Integrated filtering and candidate exploration modules
* Managed source code using Git and GitHub

---

# 📚 Academic & Internship Context

This project was developed as part of a software engineering internship and serves as a practical implementation of:

* Data Analytics
* Business Intelligence
* Machine Learning Fundamentals
* Recruitment Technology
* Dashboard Development

---

# 📄 License

This project is intended for educational, internship, and portfolio purposes.
