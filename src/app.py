"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Competitive basketball team with games and tournaments",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["james@mergington.edu"]
    },
    "Soccer Club": {
        "description": "Soccer training and friendly matches",
        "schedule": "Mondays and Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["alex@mergington.edu", "maya@mergington.edu"]
    },
    "Tennis Team": {
        "description": "Tennis training, practice matches, and tournaments",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["lucas@mergington.edu"]
    },
    "Volleyball Club": {
        "description": "Volleyball skills development and competitive play",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 16,
        "participants": ["sarah@mergington.edu", "tyler@mergington.edu"]
    },
    "Drama Club": {
        "description": "Theater productions and acting workshops",
        "schedule": "Fridays, 4:00 PM - 6:00 PM",
        "max_participants": 20,
        "participants": ["aria@mergington.edu"]
    },
    "Art Studio": {
        "description": "Painting, drawing, and visual arts",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["isabella@mergington.edu", "lucas@mergington.edu"]
    },
    "Music Band": {
        "description": "Instrument practice, ensemble performance, and concerts",
        "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 25,
        "participants": ["emily@mergington.edu", "jacob@mergington.edu"]
    },
    "Photography Club": {
        "description": "Photography techniques, editing, and portfolio building",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 14,
        "participants": ["grace@mergington.edu"]
    },
    "Math Club": {
        "description": "Advanced mathematics, problem-solving, and competitions",
        "schedule": "Wednesdays, 3:30 PM - 4:30 PM",
        "max_participants": 15,
        "participants": ["ryan@mergington.edu"]
    },
    "Science Club": {
        "description": "Hands-on experiments and STEM exploration",
        "schedule": "Mondays and Fridays, 3:30 PM - 4:45 PM",
        "max_participants": 18,
        "participants": ["zoe@mergington.edu", "noah@mergington.edu"]
    },
    "Debate Team": {
        "description": "Public speaking, argumentation, and debate competitions",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 10,
        "participants": ["andrew@mergington.edu", "jessica@mergington.edu"]
    },
    "Robotics Club": {
        "description": "Build and program robots for competitions and challenges",
        "schedule": "Mondays and Wednesdays, 3:30 PM - 5:30 PM",
        "max_participants": 12,
        "participants": ["kevin@mergington.edu", "sophia@mergington.edu"]
    }
}

@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student is already signed up for this activity")
        # Check if activity is at max capacity
        if len(activity["participants"]) >= activity["max_participants"]:
            raise HTTPException(status_code=400, detail="Activity is at max capacity")
    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}
