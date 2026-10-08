import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "bridgeway.db")


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # lets us use row["name"] instead of row[0]
    return conn


def create_tables():
    conn = get_connection()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        );

        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            topics TEXT,
            how_to_learn TEXT,
            resource_name TEXT,
            resource_url TEXT,
            hours INTEGER
        );

        CREATE TABLE IF NOT EXISTS role_skills (
            role_id INTEGER,
            skill_id INTEGER,
            position INTEGER
        );

        CREATE TABLE IF NOT EXISTS searches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT,
            skills_known TEXT,
            match_percent INTEGER,
            gaps TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    conn.close()


# ---------- Starting data ----------
yt = "https://www.youtube.com/results?search_query="

# name: (topics separated by |, how to learn, resource name, resource link, hours)
SKILLS = {
    "python": (
        "Variables and data types|Loops and conditions|Functions|Lists and dictionaries|File handling|Error handling",
        "Learn the basics, then solve one small problem every day. Build tiny programs like a calculator or a to-do list.",
        "Kaggle Learn: Python", "https://www.kaggle.com/learn/python", 30),
    "sql": (
        "SELECT and WHERE|JOINs|GROUP BY and aggregates|Subqueries|Creating tables",
        "Do interactive exercises first, then write your own queries on a sample database.",
        "SQLBolt", "https://sqlbolt.com", 15),
    "git": (
        "init, add, commit|Branches and merging|Push and pull|Pull requests",
        "Use Git on every project you build and store the code on GitHub.",
        "Pro Git book (free)", "https://git-scm.com/book/en/v2", 8),
    "django": (
        "Project and app structure|Models and migrations|Views and URLs|Templates|Admin panel|Forms",
        "Follow the official tutorial to build a polls app, then build your own small project.",
        "Django official tutorial", "https://docs.djangoproject.com/en/stable/intro/tutorial01/", 30),
    "rest api": (
        "HTTP methods (GET, POST, PUT, DELETE)|Status codes|JSON|Endpoints and routing|Authentication basics|Testing with Postman",
        "Learn the concepts, then build a small API and test every endpoint.",
        "RESTfulAPI.net", "https://restfulapi.net", 12),
    "communication": (
        "Active listening|Clear writing|Professional email etiquette|Speaking with confidence|Giving and receiving feedback",
        "Practise daily: write short summaries, explain ideas to friends, record yourself speaking.",
        "YouTube: communication skills", yt + "communication+skills+for+beginners", 10),
    "recruitment": (
        "Writing job descriptions|Sourcing candidates|Screening resumes|Using LinkedIn and job portals|Offer and onboarding process",
        "Understand the hiring cycle end to end, then practise screening sample resumes.",
        "YouTube: recruitment basics", yt + "recruitment+process+for+beginners", 15),
    "interviewing": (
        "Structured interview questions|Behavioural (STAR) method|Evaluating candidates fairly|Avoiding bias|Taking interview notes",
        "Watch real mock interviews, then practise conducting one with a friend.",
        "YouTube: interviewing skills", yt + "how+to+conduct+an+interview+hr", 10),
    "excel": (
        "Formulas (SUM, IF, VLOOKUP)|Sorting and filtering|Pivot tables|Charts|Data cleaning",
        "Follow the free lessons, then rebuild a small budget or attendance sheet yourself.",
        "Microsoft Excel training", "https://support.microsoft.com/en-us/excel", 15),
    "hr policies": (
        "Leave and attendance policy|Code of conduct|Labour law basics|Payroll basics|Grievance handling|Employee onboarding",
        "Read sample company policies and learn the basic labour laws that apply in your country.",
        "YouTube: HR policies", yt + "hr+policies+explained+for+beginners", 12),
    "statistics": (
        "Mean, median and mode|Probability|Distributions|Hypothesis testing|Correlation|Regression basics",
        "Learn the idea first, then apply it to a small real dataset.",
        "Khan Academy: Statistics", "https://www.khanacademy.org/math/statistics-probability", 30),
    "machine learning": (
        "Supervised vs unsupervised learning|Train/test split|Linear and logistic regression|Decision trees|Model evaluation|scikit-learn",
        "Learn the concepts, then train simple models on small datasets and compare results.",
        "Kaggle Learn: Intro to Machine Learning", "https://www.kaggle.com/learn/intro-to-machine-learning", 40),
    "pandas": (
        "DataFrames and Series|Reading CSV files|Filtering and selecting|Handling missing values|Grouping and merging",
        "Practise on real CSV files from Kaggle and clean them step by step.",
        "Kaggle Learn: Pandas", "https://www.kaggle.com/learn/pandas", 10),
        "html": (
        "Page structure and tags|Headings, links and images|Forms and tables|Semantic HTML|Accessibility basics",
        "Build a simple personal page first, then rebuild a page from a website you like.",
        "MDN Learn Web Development", "https://developer.mozilla.org/en-US/docs/Learn_web_development", 12),
    "css": (
        "Selectors and the box model|Colors and typography|Flexbox|Grid|Responsive design and media queries",
        "Style the page you built in HTML, then make it work on mobile screens.",
        "MDN Learn Web Development", "https://developer.mozilla.org/en-US/docs/Learn_web_development", 18),
    "javascript": (
        "Variables and functions|Arrays and objects|DOM manipulation|Events|Fetch API and promises|ES6 features",
        "Read a lesson, then immediately build a tiny feature such as a counter or a to-do list.",
        "javascript.info", "https://javascript.info", 35),
    "react": (
        "Components and JSX|Props and state|Hooks (useState, useEffect)|Lists and forms|Routing",
        "Follow the official tutorial, then rebuild one of your JavaScript mini projects in React.",
        "React official docs", "https://react.dev/learn", 30),
    "data visualization": (
        "Choosing the right chart|Bar, line and scatter plots|Dashboards|Storytelling with data|Matplotlib and Seaborn",
        "Take a small dataset and make 5 different charts, then explain what each one shows.",
        "Kaggle Learn: Data Visualization", "https://www.kaggle.com/learn/data-visualization", 12),
    "seo": (
        "Keyword research|On-page SEO|Technical SEO basics|Backlinks|Search intent",
        "Read the official guide, then optimize a sample blog post for one keyword.",
        "Google SEO Starter Guide", "https://developers.google.com/search/docs/fundamentals/seo-starter-guide", 12),
    "content writing": (
        "Writing headlines|Blog structure|Tone and audience|Editing and proofreading|Storytelling",
        "Write one short article a week and compare it with top-ranking articles.",
        "YouTube: content writing", yt + "content+writing+for+beginners", 12),
    "social media marketing": (
        "Platform basics|Content calendar|Post design and captions|Hashtags and reach|Engagement and community",
        "Run a practice page for a made-up brand and plan 2 weeks of posts.",
        "YouTube: social media marketing", yt + "social+media+marketing+for+beginners", 12),
    "google analytics": (
        "Setting up tracking|Traffic sources|Conversions and goals|Reports and dashboards|Audience analysis",
        "Take the free course, then explore the demo account to practise reading reports.",
        "Google Skillshop (free)", "https://skillshop.withgoogle.com", 10),    
}

# role: skills in the order they should be learned
ROLES = {
    "backend developer": ["python", "sql", "git", "rest api", "django"],
    "hr": ["communication", "hr policies", "recruitment", "interviewing", "excel"],
    "data scientist": ["python", "statistics", "sql", "pandas", "machine learning"],
    "frontend developer": ["html", "css", "javascript", "git", "react"],
    "data analyst": ["excel", "sql", "statistics", "python", "data visualization"],
    "digital marketer": ["content writing", "seo", "social media marketing", "google analytics"],
}


def seed_data():
    conn = get_connection()

    for name, (topics, how, res_name, res_url, hours) in SKILLS.items():
        conn.execute(
            "INSERT OR IGNORE INTO skills (name, topics, how_to_learn, resource_name, resource_url, hours) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (name, topics, how, res_name, res_url, hours),
        )

    for role_name, skill_list in ROLES.items():
        conn.execute("INSERT OR IGNORE INTO roles (name) VALUES (?)", (role_name,))
        role_id = conn.execute("SELECT id FROM roles WHERE name = ?", (role_name,)).fetchone()["id"]

        # skip if this role already has its skills linked
        if conn.execute("SELECT COUNT(*) FROM role_skills WHERE role_id = ?", (role_id,)).fetchone()[0] > 0:
            continue

        for position, skill_name in enumerate(skill_list, start=1):
            skill_id = conn.execute("SELECT id FROM skills WHERE name = ?", (skill_name,)).fetchone()["id"]
            conn.execute(
                "INSERT INTO role_skills (role_id, skill_id, position) VALUES (?, ?, ?)",
                (role_id, skill_id, position),
            )

    conn.commit()
    conn.close()