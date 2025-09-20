
from datetime import datetime, timedelta



class User:
    def __init__(self, userId, username, password=None):
        self.userId = userId
        self.username = username
        self.password = password

    def to_dict(self):
        return {
            "userId": self.userId,
            "username": self.username,
            "password": self.password
        }


class Project:
    def __init__(self, projectId, name, category, targetAmount, deadline, currentAmount=0):
        self.projectId = projectId
        self.name = name
        self.category = category
        self.targetAmount = targetAmount
        self.deadline = deadline
        self.currentAmount = currentAmount

    def to_dict(self):
        return {
            "projectId": self.projectId,
            "name": self.name,
            "category": self.category,
            "targetAmount": self.targetAmount,
            "deadline": self.deadline,
            "currentAmount": self.currentAmount
        }
    
    def progress(self):
        return min(self.currentAmount / self.targetAmount * 100, 100)

    def is_deadline_passed(self):
        return datetime.now() > datetime.strptime(self.deadline, "%Y-%m-%d")



class RewardTier:
    def __init__(self, tierId, projectId, name, minAmount, quota):
        self.tierId = tierId
        self.projectId = projectId
        self.name = name
        self.minAmount = minAmount
        self.quota = quota

    def to_dict(self):
        return {
            "tierId": self.tierId,
            "projectId": self.projectId,
            "name": self.name,
            "minAmount": self.minAmount,
            "quota": self.quota
        }
    
    def is_available(self):
        return self.quota > 0


class Pledge:
    def __init__(self, pledgeId, userId, projectId, amount, time, tierId, status):
        self.pledgeId = pledgeId
        self.userId = userId
        self.projectId = projectId
        self.amount = amount
        self.time = time
        self.tierId = tierId
        self.status = status

    def to_dict(self):
        return {
            "pledgeId": self.pledgeId,
            "userId": self.userId,
            "projectId": self.projectId,
            "amount": self.amount,
            "time": self.time,
            "tierId": self.tierId,
            "status": self.status
        }
    
def can_pledge(project: Project, tier: RewardTier, amount: float) -> (bool, str):
    if project.is_deadline_passed():
        return False, "Project deadline passed"
    if tier and amount < tier.minAmount:
        return False, "Amount below tier minimum"
    if tier and not tier.is_available():
        return False, "Tier quota exhausted"
    if amount <= 0:
        return False, "Amount must be positive"
    return True, "Valid pledge"

def apply_pledge(project: Project, tier: RewardTier, pledge: Pledge):
    project.currentAmount += pledge.amount
    if tier:
        tier.quota -= 1
