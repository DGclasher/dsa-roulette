import random
from bs4 import BeautifulSoup


def parse_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    title = soup.title.string.strip() if soup.title else 'No title found'
    problems = []

    for row in soup.select("table tbody tr"):
        cells = row.find_all("td")
        if len(cells) < 2:
            continue
        link = cells[0].find("a")
        if not link:
            continue
        problem_title = link.get_text(strip=True)
        url = link.get("href")
        difficulty = cells[1].get_text(strip=True)
        problems.append({
            "title": problem_title,
            "url": url,
            "difficulty": difficulty
        })
    problems = clean_problems(problems)
    return title, problems


def clean_problems(problems):
    l = len(problems)
    l -= 1
    while l >= 0:
        if problems[l]['difficulty'] in ['Easy', 'Medium', 'Hard']:
            break
        l -= 1
    return problems[:l+1]


def get_random_problem(problems):
    return random.choice(problems) if problems else None


def get_problems_by_difficulty(problems, difficulty):
    p = [problem for problem in problems if problem['difficulty'].lower()
         == difficulty.lower()]
    return random.choice(p) if p else None
