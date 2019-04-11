from django.shortcuts import render, HttpResponse, redirect
import random
from time import strftime

# Create your views here.

####################
# RENDER INDEX PAGE
####################
def index(request):
    if 'wincondition' in request.session:
        pass
    else:
        request.session["wincondition"] = {
            "turns": 10,
            "gold": 100
        }
    request.session["placeDict"] = {
        "farm": [10, 20],
        "cave": [5, 10],
        "house": [2, 5],
        "casino": [-50, 50]
    }
    if "counter" in request.session and request.session["counter"] < request. session["wincondition"]["turns"]:
        request.session["counter"] += 1
    elif "counter" in request.session and request.session["counter"] >= request.session["wincondition"]["turns"]:
        if request.session["gold"] >= int(request.session["wincondition"]["gold"]):
            request.session["win"] = True
        else:
            request.session["win"] = False
    else:
        request.session["counter"] = 1
        request.session["gold"] = 0
        request.session["ledger"] = ""
        request.session["gain"] = ""
    return render(request, "game/index.html")

####################
# PROCESS CHANGE IN FUNDS
####################
def process(request):
    now = strftime("%Y/%m/%d %H:%m %p")
    change = random.randint(request.session["placeDict"][request.POST["place"]][0], request.session["placeDict"][request.POST["place"]][1])
    
    activity_str = "Entered the " + request.POST["place"] + " and "
    
    request.session["gold"] += change
    if change >= 0:
        gain_str = "gain"
        activity_str += "got"
    else:
        gain_str = "loss"
        activity_str += "lost"
    
    activity_str += " " + str(abs(change)) + " gold!"
    activity_str += " " + now + "."
    ledgerDict = {
            "activity": activity_str,
            "gain": gain_str
        }
    if not "activity_log" in request.session:
        request.session["activity_log"] = []
    request.session["activity_log"].append(ledgerDict)
    
    return redirect("/")

####################
# RESET GAME
####################
def reset(request):
    request.session.clear()
    turnsblank = False
    goldblank = False

    if len(request.POST["turnsGoal"]) < 1 or int(request.POST["turnsGoal"]) <= 0:
        turnsblank = True
    if len(request.POST["goldGoal"]) < 1 or int(request.POST["goldGoal"]) <= 0:
        goldblank = True
    
    if turnsblank and goldblank:
        request.session["wincondition"] = {
            "turns": 10,
            "gold": 100
        }
    elif turnsblank and not goldblank:
        request.session["wincondition"] = {
            "turns": 10,
            "gold": int(request.POST["goldGoal"])
        }
    elif not turnsblank and goldblank:
        request.session["wincondition"] = {
            "turns": int(request.POST["turnsGoal"]),
            "gold": 100
        }
    else:
        request.session["wincondition"] = {
            "turns": int(request.POST["turnsGoal"]),
            "gold": int(request.POST["goldGoal"])
        }
    
    return redirect("/")