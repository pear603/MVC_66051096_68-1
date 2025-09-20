import os, json, random, uuid
from datetime import datetime, timedelta
from model.model import User, Project, RewardTier, Pledge

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, 'data.json')

os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)


# other generic utility functions can be added here

def save_data(users, projects, reward_tiers, pledges, file_path='model/data.json'):
    data = {
        "users": [u.to_dict() for u in users],
        "projects": [p.to_dict() for p in projects],
        "rewardTiers": [r.to_dict() for r in reward_tiers],
        "pledges": [p.to_dict() for p in pledges]
    }
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Data saved to {file_path}")


def load_data(filename="model/data.json"):
    import os, json
    if not os.path.exists(filename):
        print(f"⚠️ {filename} not found. Returning empty lists.")
        return [], [], [], []

    # Check if file is empty
    if os.path.getsize(filename) == 0:
        print(f"⚠️ {filename} is empty. Returning empty lists.")
        return [], [], [], []

    with open(filename, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"⚠️ JSON decode error: {e}. Returning empty lists.")
            return [], [], [], []

    users = [User(**u) for u in data.get("users", [])]
    projects = [Project(**p) for p in data.get("projects", [])]
    reward_tiers = [RewardTier(**r) for r in data.get("rewardTiers", [])]
    pledges = [Pledge(**p) for p in data.get("pledges", [])]

    print(f"📂 Data loaded from {filename}")
    return users, projects, reward_tiers, pledges



def generate_data(file_path=DATA_PATH):
    categories = ["Technology", "Art", "Environment"]
    usernames = ["alice", "bob", "charlie", "diana", "edward",
                 "fiona", "george", "hannah", "ian", "julia"]

    # --- Users with random passwords ---
    users = []
    for i, name in enumerate(usernames, start=1):
        # simple password: 6-8 random chars
        password = ''.join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=8))
        users.append(User(f"U{i:03d}", name, password))

    # --- Projects & Reward Tiers ---
    projects = []
    reward_tiers = []
    for pid in range(1, 9):
        project_id = f"{random.randint(1,9)}{random.randint(1000000,9999999)}"
        category = random.choice(categories)

        # Make the first project expired
        if pid == 1:
            deadline = (datetime.now() - timedelta(days=random.randint(1, 10))).strftime("%Y-%m-%d")
        else:
            deadline = (datetime.now() + timedelta(days=random.randint(10, 90))).strftime("%Y-%m-%d")

        project = Project(
            project_id,
            f"Project {pid} in {category}",
            category,
            random.randint(20000, 100000),
            deadline
        )
        projects.append(project)

        # 2–3 reward tiers
        for t in range(random.randint(2,3)):
            tier = RewardTier(
                f"R{uuid.uuid4().hex[:6].upper()}",
                project_id,
                f"Reward {t+1} for {project.name}",
                (t+1)*500,
                random.randint(5,20)
            )
            reward_tiers.append(tier)

    # --- Pledges ---
    pledges = []
    for _ in range(20):
        user = random.choice(users)
        project = random.choice(projects)
        tiers = [r for r in reward_tiers if r.projectId == project.projectId]
        chosen_tier = random.choice(tiers)
        success = random.choice([True, True, False])
        amount = chosen_tier.minAmount if success else chosen_tier.minAmount - 100

        pledge = Pledge(
            f"P{uuid.uuid4().hex[:6].upper()}",
            user.userId,
            project.projectId,
            amount,
            datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            chosen_tier.tierId,
            "SUCCESS" if success else "REJECTED"
        )
        pledges.append(pledge)
        if success:
            project.currentAmount += amount

    # Save all to JSON
    save_data(users, projects, reward_tiers, pledges, file_path)
    return users, projects, reward_tiers, pledges

def prepare_data():
    users, projects, reward_tiers, pledges = load_data()
    if not users and not projects and not reward_tiers and not pledges:
        return generate_data()
    return users, projects, reward_tiers, pledges

