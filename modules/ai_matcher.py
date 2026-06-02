# -*- coding: utf-8 -*-
"""
ai_matcher.py
TF-IDF + Cosine Similarity role recommender.
v5 fixes:
  - Splits on commas only (Power BI stays intact)
  - Missing skills from structured ROLE_SKILLS lists (no TF-IDF vocabulary noise)
  - Scores normalised + labelled Excellent / Good / Average
  - Career tip per role
  - PDF extraction via PyMuPDF -> pdfplumber fallback
"""
import re
import io
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ── Role profiles for TF-IDF vectorisation ───────────────────────────────────
ROLE_PROFILES = {
    "Data Analyst":      "python sql excel power bi tableau pandas numpy matplotlib seaborn statistics data visualization reporting dashboards",
    "BI Developer":      "power bi tableau qlik dax sql excel kpi dashboards reporting data modeling etl business intelligence",
    "Data Engineer":     "python sql spark hadoop etl pipeline airflow kafka aws gcp azure data lake warehouse postgresql pyspark",
    "ML Engineer":       "python scikit-learn tensorflow keras pytorch deep learning machine learning nlp computer vision feature engineering model deployment",
    "Data Scientist":    "python r statistics pandas numpy scikit-learn tensorflow hypothesis testing a/b testing machine learning data analysis",
    "AI Research Intern":"python pytorch tensorflow deep learning nlp transformer bert gpt research mathematics linear algebra probability statistics",
    "Frontend Developer":"html css javascript react vue angular typescript redux tailwind bootstrap responsive design ui ux figma",
    "Full Stack Developer":"html css javascript react node.js express mongodb postgresql python rest api graphql docker git",
    "Backend Developer": "python java node.js express flask django rest api postgresql mysql mongodb redis docker kubernetes microservices",
    "Cloud Engineer":    "aws azure gcp terraform ansible docker kubernetes linux bash iam vpc s3 ec2 lambda cloud networking security",
    "DevOps Engineer":   "docker kubernetes jenkins ci/cd gitlab github actions ansible terraform linux bash monitoring prometheus grafana aws",
    "Solutions Architect":"aws azure gcp cloud architecture microservices system design scalability security cost optimization networking enterprise",
    "Security Analyst":  "network security ethical hacking siem firewall linux python vulnerability assessment wireshark owasp cryptography incident response",
    "Penetration Tester":"ethical hacking kali linux metasploit nmap burp suite owasp web application network testing python scripting",
    "SOC Analyst":       "siem splunk incident response log analysis threat hunting firewall ids ips network monitoring security operations",
    "Business Analyst":  "excel powerpoint requirements gathering stakeholder management agile jira business analysis sql project management documentation",
    "IT Consultant":     "project management agile itil stakeholder management requirements business analysis technical writing presentations erp sap crm",
    "Project Manager":   "project management agile scrum kanban jira ms project risk management budgeting stakeholder communication planning",
}

# ── Structured skill lists per role (for clean gap detection) ─────────────────
ROLE_SKILLS = {
    "Data Analyst":      ["Python","SQL","Excel","Power BI","Tableau","Pandas","NumPy","Statistics","Data Visualization","Seaborn"],
    "BI Developer":      ["Power BI","Tableau","DAX","SQL","Excel","ETL","Data Modeling","KPI Dashboards","QlikView"],
    "Data Engineer":     ["Python","SQL","Spark","Hadoop","Airflow","Kafka","AWS","ETL","PostgreSQL","PySpark","dbt"],
    "ML Engineer":       ["Python","Scikit-learn","TensorFlow","Keras","PyTorch","NLP","Deep Learning","Feature Engineering","Docker"],
    "Data Scientist":    ["Python","R","Statistics","Pandas","NumPy","Scikit-learn","TensorFlow","A/B Testing","Hypothesis Testing","SQL"],
    "AI Research Intern":["Python","PyTorch","TensorFlow","NLP","Transformers","BERT","Mathematics","Statistics","Deep Learning"],
    "Frontend Developer":["HTML","CSS","JavaScript","React","TypeScript","Tailwind","Bootstrap","Figma","Redux","Vue.js"],
    "Full Stack Developer":["React","Node.js","MongoDB","PostgreSQL","REST API","Docker","JavaScript","TypeScript","Git","GraphQL"],
    "Backend Developer": ["Python","Node.js","Django","Flask","REST API","PostgreSQL","MongoDB","Docker","Kubernetes","Redis"],
    "Cloud Engineer":    ["AWS","Azure","GCP","Terraform","Docker","Kubernetes","Linux","Ansible","IAM","Networking"],
    "DevOps Engineer":   ["Docker","Kubernetes","Jenkins","CI/CD","Ansible","Terraform","Prometheus","Grafana","Linux","GitHub Actions"],
    "Solutions Architect":["AWS","Azure","Cloud Architecture","Microservices","System Design","Scalability","Security","Networking"],
    "Security Analyst":  ["Network Security","SIEM","Ethical Hacking","Firewall","Python","Linux","OWASP","Wireshark","Vulnerability Assessment"],
    "Penetration Tester":["Kali Linux","Metasploit","Burp Suite","Nmap","OWASP","Ethical Hacking","Python","Network Security"],
    "SOC Analyst":       ["SIEM","Splunk","Incident Response","Log Analysis","Threat Hunting","Firewall","IDS/IPS","Network Monitoring"],
    "Business Analyst":  ["Excel","SQL","Agile","JIRA","Requirements Gathering","Stakeholder Management","PowerPoint","Business Analysis"],
    "IT Consultant":     ["Project Management","Agile","ITIL","SAP","CRM","Stakeholder Management","Business Analysis","ERP"],
    "Project Manager":   ["Agile","Scrum","JIRA","Risk Management","Budgeting","MS Project","Stakeholder Communication","Kanban"],
}

CAREER_TIPS = {
    "Data Analyst":      "Strong fit for analytics roles. A Power BI or Tableau certification will significantly boost your profile.",
    "BI Developer":      "Great BI foundation. Mastering DAX and Power BI Premium features will open senior BI roles.",
    "Data Engineer":     "Solid DE profile. AWS Data Engineer or dbt certifications are high-value additions in 2026.",
    "ML Engineer":       "Strong AI/ML stack. Focus on model deployment (MLflow, FastAPI) to stand out from research-only profiles.",
    "Data Scientist":    "Good DS alignment. Publishing a Kaggle notebook or a research project on GitHub builds strong credibility.",
    "AI Research Intern":"NLP and LLM skills are extremely in demand. Hands-on Hugging Face projects will attract top recruiters.",
    "Frontend Developer":"React remains dominant. TypeScript and accessibility skills are increasingly required for senior roles.",
    "Full Stack Developer":"Full-stack is highly versatile. Deploying a live project (Vercel, Railway) impresses interviewers significantly.",
    "Backend Developer": "Solid backend profile. API security and microservices patterns are the most valued next skills.",
    "Cloud Engineer":    "Cloud demand is surging. AWS Solutions Architect Associate is the most impactful certification to pursue.",
    "DevOps Engineer":   "Strong DevOps base. GitOps practices and observability (Prometheus + Grafana) are the top growth areas.",
    "Solutions Architect":"Excellent architecture profile. Practicing system design interviews (with diagrams) will differentiate you.",
    "Security Analyst":  "Cybersecurity demand is very high. CEH or CompTIA Security+ certification adds immediate credibility.",
    "Penetration Tester":"OSCP certification is the gold standard for pentesters and will dramatically increase your earning potential.",
    "SOC Analyst":       "SOC is a strong entry point into cybersecurity. Splunk certification and threat-hunting skills are valued.",
    "Business Analyst":  "Good BA foundation. CBAP certification and SQL + Power BI skills bridge the business-to-data gap well.",
    "IT Consultant":     "Good consulting profile. PMP or PRINCE2 + domain expertise will command premium consulting rates.",
    "Project Manager":   "Solid PM foundation. PMP certification and hands-on Agile delivery experience are key differentiators.",
}

ALL_ROLES = list(ROLE_PROFILES.keys())


def match_skills(user_skills_text: str, top_n: int = 3) -> dict | None:
    """
    Match skills against role profiles using TF-IDF + Cosine Similarity.

    Fixes applied:
    1. Splits on commas only -> 'Power BI' stays as one unit
    2. Missing skills from structured ROLE_SKILLS lists (no vocabulary noise)
    3. Scores normalised + labelled Excellent / Good / Average

    Returns dict with: top_role, top_score, match_level, alternatives,
                       missing_skills, matched_skills, career_tip
    """
    if not user_skills_text or not user_skills_text.strip():
        return None

    # FIX 1: comma-only split to preserve multi-word skills
    user_skill_set = {s.strip().lower() for s in user_skills_text.split(",") if s.strip()}
    user_text = " ".join(user_skill_set)

    corpus = [user_text] + list(ROLE_PROFILES.values())
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True)
    tfidf_matrix = vectorizer.fit_transform(corpus)

    similarities = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1:]).flatten()
    scored = sorted(zip(ALL_ROLES, similarities), key=lambda x: x[1], reverse=True)

    top_role, top_raw = scored[0]

    # FIX 2: normalise score
    score = round(float(top_raw) * 100)
    if score < 50:
        score = min(score + 18, 62)
    score = min(score, 99)

    # FIX 3: match level label
    match_level = "Excellent" if score >= 72 else "Good" if score >= 52 else "Average"

    # Alternatives
    alternatives = []
    for role, raw in scored[1:top_n + 1]:
        s = round(float(raw) * 100)
        if s < 50:
            s = min(s + 18, 62)
        s = min(s, 99)
        if s > 0:
            alternatives.append({"role": role, "score": s})

    # FIX 4: missing skills from structured list (no random vocabulary words)
    top_role_skills_lower = [sk.lower() for sk in ROLE_SKILLS.get(top_role, [])]
    missing_skills = [
        sk for sk in ROLE_SKILLS.get(top_role, [])
        if sk.lower() not in user_skill_set
    ][:6]

    # Matched skills: user skills that appear in top role skill list
    matched_skills = [
        sk.title() for sk in user_skill_set
        if sk in top_role_skills_lower
    ][:8]

    return {
        "top_role":      top_role,
        "top_score":     score,
        "match_level":   match_level,
        "alternatives":  alternatives,
        "missing_skills": missing_skills,
        "matched_skills": matched_skills,
        "career_tip":    CAREER_TIPS.get(top_role, "Keep building your skills and stay consistent."),
    }


def extract_text_from_pdf(uploaded_file) -> str:
    """Extract text from an uploaded PDF — PyMuPDF first, pdfplumber fallback."""
    try:
        import fitz
        pdf_bytes = uploaded_file.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        text = "".join(page.get_text() for page in doc)
        doc.close()
        return text.strip()
    except ImportError:
        pass
    except Exception:
        pass

    try:
        import pdfplumber
        uploaded_file.seek(0)
        with pdfplumber.open(io.BytesIO(uploaded_file.read())) as pdf:
            return "\n".join(p.extract_text() or "" for p in pdf.pages).strip()
    except Exception:
        return ""


def extract_skills_from_resume(text: str) -> str:
    """Extract known skills from resume text via keyword matching."""
    if not text:
        return ""

    KNOWN_SKILLS = [
        "python","java","javascript","typescript","sql","r","c++","c#","go",
        "react","vue","angular","node.js","express","django","flask","fastapi",
        "html","css","bootstrap","tailwind","redux",
        "aws","azure","gcp","docker","kubernetes","terraform","ansible",
        "linux","bash","git","jenkins","ci/cd","github actions",
        "pandas","numpy","scikit-learn","tensorflow","keras","pytorch",
        "matplotlib","seaborn","plotly","power bi","tableau","excel","dax",
        "mongodb","postgresql","mysql","redis","elasticsearch","spark","hadoop",
        "nlp","deep learning","machine learning","data science","statistics","a/b testing",
        "agile","scrum","jira","project management","business analysis","stakeholder management",
        "network security","ethical hacking","wireshark","owasp","siem","splunk",
        "kali linux","metasploit","burp suite","vulnerability assessment",
        "itil","sap","crm","erp","powerpoint",
    ]

    text_lower = text.lower()
    found = [s for s in KNOWN_SKILLS if s in text_lower]
    return ", ".join(found) if found else text[:2000]
