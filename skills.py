def extract_skills_from_text(text, skill_bank):
    text = text.lower()
    return [skill for skill in skill_bank if skill.lower() in text]

def compare_skills(jd_skills, resume_skills):
    matching = list(set(jd_skills) & set(resume_skills))
    missing = list(set(jd_skills) - set(resume_skills))
    return matching, missing

def calculate_score(jd_skills, matching):
    if not jd_skills:
        return 0
    return int((len(matching) / len(jd_skills)) * 100)
