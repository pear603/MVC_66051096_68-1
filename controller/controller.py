from model.utility import load_data

def generateData():
    DB = load_data
    if not DB:
        import random

        allData =[]
