job_role = input("Enter a job role: ").lower().strip()
skill_known = input("Enter the skills you know, separated by commas: ").lower()
skill_known = skill_known.split(",")
skill_known = [skill.strip() for skill in skill_known]
print ("you have entered the job role as:", job_role)
print ("you have entered the skill as:", skill_known)
job_requirements = {
    "backend developer": ["python", "sql", "git", "django", "rest api"],
    "hr": ["communication", "recruitment", "interviewing", "excel", "hr policies"],
    "data scientist": ["python", "sql", "statistics", "machine learning", "pandas"]
}
def find_skill_gaps(job_role, skill_known):
    required_skills = job_requirements.get(job_role)

    if required_skills is None:
        return None

    skill_gaps = []

    for skill in required_skills:
        if skill not in skill_known:
            skill_gaps.append(skill)

    return skill_gaps


skill_gaps = find_skill_gaps(job_role, skill_known)

if skill_gaps is None:
    print("Job role not found.")
else:
    print("The skill gaps are:", skill_gaps)