import requests
from flask import Flask, render_template, request

from helper import get_problems_by_difficulty, get_random_problem, parse_html

app = Flask(__name__)

SDE_SHEET_URL = "https://www.geeksforgeeks.org/dsa/sde-sheet-a-complete-guide-for-sde-preparation/"
DIFFICULTIES = ("Easy", "Medium", "Hard")


def load_problems():
    response = requests.get(SDE_SHEET_URL, timeout=15)
    response.raise_for_status()
    return parse_html(response.text)[1]


@app.route("/", methods=["GET", "POST"])
def index():
    choice = request.form.get("choice", "")
    difficulty = request.form.get("difficulty", "")
    problem = None
    message = None

    try:
        problems = load_problems()
        if request.method == "POST":
            if choice == "random":
                problem = get_random_problem(problems)
            elif choice == "difficulty" and difficulty in DIFFICULTIES:
                problem = get_problems_by_difficulty(problems, difficulty)
            elif choice == "difficulty":
                message = "Please select a valid difficulty."
            else:
                message = "Please choose how to find a problem."

            if problem is None and message is None:
                message = "No problem was found for that selection."
    except requests.RequestException:
        message = "The problem sheet could not be loaded. Please try again later."

    return render_template(
        "index.html",
        choice=choice,
        difficulty=difficulty,
        difficulties=DIFFICULTIES,
        message=message,
        problem=problem,
    )


if __name__ == "__main__":
    app.run(debug=True)
