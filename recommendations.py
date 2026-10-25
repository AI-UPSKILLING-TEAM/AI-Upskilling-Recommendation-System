"""Transparent content-based learning recommendations for the student prototype.

TF-IDF cosine matching is computed from a small, curated text catalog. This
is a content-based ranking algorithm, not a trained neural network or an LLM.
"""
from collections import Counter
import math
import re

CATALOG = {
    "Python": ("Python official tutorial", "https://docs.python.org/3/tutorial/", "course", "python coding data analysis scripting backend"),
    "SQL": ("Microsoft Learn: Introduction to Transact-SQL", "https://learn.microsoft.com/en-us/training/modules/introduction-to-transact-sql/", "course", "sql relational databases querying data analytics"),
    "Excel": ("Microsoft Excel training", "https://support.microsoft.com/en-us/excel", "resource", "excel spreadsheets tabular data visualization"),
    "Statistics": ("Khan Academy: Statistics and probability", "https://www.khanacademy.org/math/statistics-probability", "course", "statistics probability data analysis data science"),
    "Data Visualization": ("Matplotlib tutorials", "https://matplotlib.org/stable/tutorials/index.html", "course", "data visualization plots charts python analytics"),
    "Machine Learning": ("Google Machine Learning Crash Course", "https://developers.google.com/machine-learning/crash-course", "course", "machine learning artificial intelligence data science"),
    "HTML": ("MDN: Learn web development", "https://developer.mozilla.org/en-US/docs/Learn_web_development", "course", "html markup websites frontend web development"),
    "CSS": ("MDN: CSS styling basics", "https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics", "course", "css styling web frontend development"),
    "JavaScript": ("MDN: JavaScript", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide", "course", "javascript interactive web frontend programming"),
    "Git": ("Pro Git book", "https://git-scm.com/book/en/v2", "course", "git version control collaboration software development"),
    "APIs": ("MDN: Web APIs", "https://developer.mozilla.org/en-US/docs/Web/API", "resource", "apis web application backend frontend integration"),
    "Testing": ("Python unittest documentation", "https://docs.python.org/3/library/unittest.html", "resource", "testing unit automated software quality"),
    "Linux": ("Ubuntu command-line introduction", "https://ubuntu.com/tutorials/command-line-for-beginners", "course", "linux shell commands cloud security operations"),
    "Networking": ("Cloudflare: Learning center", "https://www.cloudflare.com/learning/", "resource", "networking protocols internet security infrastructure"),
    "Cloud Fundamentals": ("Microsoft Learn: Azure fundamentals", "https://learn.microsoft.com/en-us/training/paths/microsoft-azure-fundamentals-describe-cloud-concepts/", "course", "cloud fundamentals computing architecture"),
    "Security Fundamentals": ("OWASP Top 10", "https://owasp.org/www-project-top-ten/", "resource", "cybersecurity security risk vulnerability web protection"),
}


PROJECT_IDEAS = {
    "Python": "Create a CSV data cleaning and summary command-line tool.",
    "SQL": "Design a student-course database and write analytical JOIN queries.",
    "Excel": "Build a budget workbook with charts and validated formulas.",
    "Statistics": "Analyze survey data and explain sample variability.",
    "Data Visualization": "Create a dashboard of trends from a public dataset.",
    "Machine Learning": "Train and evaluate a small supervised classification baseline.",
    "HTML": "Build an accessible portfolio page with semantic HTML.",
    "CSS": "Implement a responsive landing page with mobile layouts.",
    "JavaScript": "Build an interactive study task tracker in the browser.",
    "Git": "Contribute changes through branches, reviews and pull requests.",
    "APIs": "Build a small HTTP API and client to manage tasks.",
    "Testing": "Add automated unit and integration tests to an API.",
    "Linux": "Write a Bash script that automates file backups.",
    "Networking": "Document a small LAN topology and test DNS/HTTP.",
    "Cloud Fundamentals": "Create an architecture diagram for a cloud-hosted app.",
    "Security Fundamentals": "Threat-model a sample web app and document mitigations.",
}

# Provider pages verified 25 October 2026. Eligibility, prices and versions can change.
CERTIFICATION_OPTIONS = {
    "Data Analyst": {"title": "Microsoft Certified: Power BI Data Analyst Associate",
                     "url": "https://learn.microsoft.com/en-us/credentials/certifications/data-analyst-associate/",
                     "note": "Intermediate; check eligibility and exam requirements."},
    "Cloud Engineer": {"title": "AWS Certified Cloud Practitioner",
                       "url": "https://aws.amazon.com/certification/certified-cloud-practitioner/",
                       "note": "Foundational; check current exam details."},
    "Cybersecurity Analyst": {"title": "ISC2 Certified in Cybersecurity (CC)",
                              "url": "https://www.isc2.org/Certifications",
                              "note": "Entry-level; check current exam and registration details."},
}


def certificates_for(goal):
    option = CERTIFICATION_OPTIONS.get(goal)
    return [dict(option)] if option else []


def words(value):
    return re.findall(r"[a-z0-9]+", value.lower())


def rank_learning(missing, goal, interests=""):
    """Rank missing skills against the student's stated interests and goal."""
    items = [(skill, CATALOG[skill]) for skill in missing if skill in CATALOG]
    if not items:
        return []
    documents = [words(skill + " " + data[3]) for skill, data in items]
    n = len(documents)
    df = Counter(word for document in documents for word in set(document))
    def vector(tokens):
        term_freq = Counter(tokens)
        return {word: (1 + math.log(count)) * (1 + math.log((1+n)/(1+df.get(word,0))))
                for word, count in term_freq.items()}
    query = vector(words(goal + " " + interests))
    norm_q = math.sqrt(sum(v*v for v in query.values())) or 1
    result = []
    for i, (skill, (title, url, kind, description)) in enumerate(items):
        doc = vector(documents[i])
        norm_d = math.sqrt(sum(v*v for v in doc.values())) or 1
        similarity = sum(value * doc.get(word, 0) for word, value in query.items()) / (norm_q * norm_d)
        result.append({
            "skill": skill, "resource": title, "url": url, "type": kind,
            "activity": PROJECT_IDEAS.get(skill, "Design a practical project using " + skill),
            "project": PROJECT_IDEAS.get(skill, "Design a practical project using " + skill),
            "relevance_score": round(similarity, 4),
            "_order": i,
        })
    result.sort(key=lambda row: (-row["relevance_score"], row["_order"]))
    for row in result:
        del row["_order"]
    return result


def resource_catalog():
    return [{"skill": skill, "title": data[0], "url": data[1], "type": data[2]}
            for skill, data in sorted(CATALOG.items())]
