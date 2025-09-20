from flask import render_template, request, redirect, url_for, session, flash
from model.utility import save_data, DATA_PATH, load_data, generate_data, prepare_data
from model.model import Project, RewardTier, Pledge, can_pledge, apply_pledge
import uuid
from datetime import datetime

def get_initial_data():
    return prepare_data()

def project_detail_controller(project_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    project = next((p for p in projects if p.projectId == project_id), None)
    if not project:
        return "Project not found", 404

    project_tiers = [r for r in reward_tiers if r.projectId == project_id]
    project_pledges = [p for p in pledges if p.projectId == project_id]
    user_map = {u.userId: u.username for u in users}

    if request.method == "POST":
        amount = float(request.form["amount"])
        tier_id = request.form.get("tier_id")
        selected_tier = next((t for t in reward_tiers if t.tierId == tier_id), None) if tier_id else None

        # --- Business rule check via model ---
        valid, message = can_pledge(project, selected_tier, amount)
        status = "SUCCESS" if valid else "REJECTED"
        flash(message if not valid else "Pledge successful!", "success" if valid else "danger")

        new_pledge = Pledge(
            f"P{uuid.uuid4().hex[:6].upper()}",
            session["user_id"],
            project_id,
            amount,
            datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            tier_id,
            status
        )

        if valid:
            apply_pledge(project, selected_tier, new_pledge)

        pledges.append(new_pledge)
        save_data(users, projects, reward_tiers, pledges, DATA_PATH)

        return redirect(url_for("project_detail", project_id=project_id))

    return render_template(
        'project_detail.html',
        project=project,
        progress=project.progress(),
        reward_tiers=project_tiers,
        project_pledges=project_pledges,
        user_map=user_map
    )

DATA_PATH = "model/data.json"

# Load data globally or you can reload inside each function
users, projects, reward_tiers, pledges = load_data(DATA_PATH)

# --- Login logic ---
def login_controller(form):
    username = form.get("username")
    password = form.get("password")

    user = next((u for u in users if u.username == username), None)
    if user:
        if user.password == password:
            session["user_id"] = user.userId
            flash("Logged in successfully!", "success")
            return redirect(url_for("list_projects"))
        else:
            flash("Incorrect password.", "danger")
    else:
        flash("User not found.", "danger")
    return render_template("login.html")


# --- Logout logic ---
def logout_controller():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


# --- Project listing logic ---
def list_projects_controller(args):
    category = args.get('category')
    sort_by = args.get('sort', 'newest')

    filtered = projects
    if category:
        filtered = [p for p in projects if p.category == category]

    if sort_by == 'newest':
        filtered.sort(key=lambda x: x.deadline, reverse=True)
    elif sort_by == 'ending':
        filtered.sort(key=lambda x: x.deadline)
    elif sort_by == 'most_funded':
        filtered.sort(key=lambda x: x.currentAmount, reverse=True)

    categories = list(set(p.category for p in projects))
    return render_template('projects.html', projects=filtered, categories=categories)

def stats_controller():
    users, projects, reward_tiers, pledges = load_data(DATA_PATH)

    success_count = len([p for p in pledges if p.status == "SUCCESS"])
    rejected_count = len([p for p in pledges if p.status == "REJECTED"])

    user_map = {u.userId: u.username for u in users}
    project_map = {p.projectId: p.name for p in projects}

    return {
        "pledges": pledges,
        "user_map": user_map,
        "project_map": project_map,
        "success_count": success_count,
        "rejected_count": rejected_count
    }