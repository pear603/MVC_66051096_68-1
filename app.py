from flask import Flask, render_template, redirect, url_for,request, session, flash,jsonify
from controller.controller import get_initial_data, project_detail_controller, list_projects_controller, login_controller, logout_controller, stats_controller
from model.model import User, Project, RewardTier, Pledge
import os
from model.utility import DATA_PATH, load_data
app = Flask(__name__)
app.secret_key = "secret"


users, projects, reward_tiers, pledges = get_initial_data()

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return login_controller(request.form)
    return login_controller({})  # empty dict for GET request

@app.route("/logout")
def logout():
    return logout_controller()

@app.route("/")
def list_projects():
    return list_projects_controller(request.args)

@app.route('/project/<project_id>', methods=["GET", "POST"])
def project_detail(project_id):
    return project_detail_controller(project_id)

@app.route('/project/<project_id>/pledges_api')
def pledges_api(project_id):
    project_pledges = [p for p in pledges if p.projectId == project_id]
    user_map = {u.userId: u.username for u in users}
    data = [
        {
            "user": user_map[p.userId],
            "amount": p.amount,
            "status": p.status,
            "time": p.time
        } for p in project_pledges
    ]
    return jsonify(data)


@app.route('/stats')
def stats():
    context = stats_controller()
    return render_template('stats.html', **context)


if __name__ == "__main__":
    app.run(debug=True)