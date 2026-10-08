import math
from flask import Flask, render_template, request
from database import get_connection, create_tables, seed_data

app = Flask(__name__)

create_tables()
seed_data()


def get_all_roles():
    conn = get_connection()
    rows = conn.execute("SELECT name FROM roles ORDER BY name").fetchall()
    conn.close()
    return [r["name"] for r in rows]


def find_skill_gaps(job_role, skill_known):
    conn = get_connection()
    role = conn.execute("SELECT id FROM roles WHERE name = ?", (job_role,)).fetchone()

    if role is None:
        conn.close()
        return None, None, None

    required = conn.execute("""
        SELECT skills.* FROM skills
        JOIN role_skills ON skills.id = role_skills.skill_id
        WHERE role_skills.role_id = ?
        ORDER BY role_skills.position
    """, (role["id"],)).fetchall()
    conn.close()

    have = [s for s in required if s["name"] in skill_known]
    gaps = [s for s in required if s["name"] not in skill_known]
    return required, have, gaps


def save_search(job_role, skill_known, match_percent, gaps):
    conn = get_connection()
    conn.execute(
        "INSERT INTO searches (role, skills_known, match_percent, gaps) VALUES (?, ?, ?, ?)",
        (job_role, ", ".join(skill_known), match_percent, ", ".join(g["name"] for g in gaps)),
    )
    conn.commit()
    conn.close()

def build_roadmap(gaps, hours_per_week):
    steps = []
    total_hours = 0

    for number, skill in enumerate(gaps, start=1):
        start_week = math.floor(total_hours / hours_per_week) + 1
        total_hours += skill["hours"]
        end_week = math.ceil(total_hours / hours_per_week)

        steps.append({
            "number": number,
            "name": skill["name"],
            "hours": skill["hours"],
            "start_week": start_week,
            "end_week": end_week,
        })

    total_weeks = math.ceil(total_hours / hours_per_week) if total_hours else 0
    return steps, total_hours, total_weeks

@app.route("/")
def home():
    return render_template("index.html", roles=get_all_roles())


@app.route("/result", methods=["POST"])
def result():
    job_role = request.form["job_role"].lower().strip()
    raw_skills = request.form["skills"].lower()
    skill_known = [s.strip() for s in raw_skills.split(",") if s.strip()]
    try:
        hours_per_week = int(request.form.get("hours_per_week", 10))
    except ValueError:
        hours_per_week = 10
    hours_per_week = max(1, hours_per_week)

    required, have, gaps = find_skill_gaps(job_role, skill_known)

    if required is None:
        return render_template("index.html", roles=get_all_roles(),
                               error="Job role not found.")

    match_percent = round(len(have) / len(required) * 100)
    save_search(job_role, skill_known, match_percent, gaps)

    roadmap, total_hours, total_weeks = build_roadmap(gaps, hours_per_week)

    return render_template("result.html", job_role=job_role, have=have, gaps=gaps,
                           match_percent=match_percent, roadmap=roadmap,
                           total_hours=total_hours, total_weeks=total_weeks,
                           hours_per_week=hours_per_week)
    
@app.errorhandler(404)
@app.errorhandler(405)
def client_error(e):
    return render_template("error.html", code=e.code,
                           message="We couldn't find that page."), e.code


@app.errorhandler(500)
def server_error(e):
    return render_template("error.html", code=500,
                           message="Something went wrong on our side."), 500

if __name__ == "__main__":
    app.run(debug=True)