from flask import Flask, jsonify, render_template, request

import Recommendation as rec


app = Flask(__name__)


def get_available_interests():
    """Build a sorted list of unique interests from the existing course data."""
    interests = set()

    for course_tags in rec.courses.values():
        for tag in course_tags:
            interests.add(tag.capitalize())

    return sorted(interests)


def remove_duplicate_interests(interests):
    """Keep the user's selections unique while preserving their order."""
    unique_interests = []

    for interest in interests:
        clean_interest = str(interest).strip().capitalize()
        if clean_interest and clean_interest not in unique_interests:
            unique_interests.append(clean_interest)

    return unique_interests


@app.route("/")
def home():
    return render_template("index.html", interests=get_available_interests())


@app.route("/recommend", methods=["POST"])
def recommend_courses():
    data = request.get_json() or {}

    name = str(data.get("name", "")).strip()
    username = str(data.get("username", "")).strip()
    selected_interests = remove_duplicate_interests(data.get("interests", []))

    try:
        age = int(data.get("age", ""))
    except (TypeError, ValueError):
        age = 0

    errors = []
    if not name:
        errors.append("Please enter your name.")
    if not username:
        errors.append("Please enter your username.")
    if age <= 0:
        errors.append("Please enter a valid age.")
    if not selected_interests:
        errors.append("Please choose at least one interest.")

    if errors:
        return jsonify({"errors": errors}), 400

    user = rec.User(name, username, age, selected_interests)
    recommendation_system = rec.Recommendation_System(user)

    # Use the existing OOP recommendation logic, then format it for the web page.
    recommendations = recommendation_system.similarity_check()
    recommendations.sort(key=lambda course: course[1], reverse=True)

    formatted_recommendations = []
    for index, (course_name, match_score) in enumerate(recommendations):
        course_tags = rec.courses[course_name]
        matching_interests = [
            tag.capitalize()
            for tag in course_tags
            if tag.capitalize() in selected_interests
        ]
        score_percent = round((match_score / len(course_tags)) * 100)

        formatted_recommendations.append(
            {
                "course_name": course_name,
                "match_score": match_score,
                "score_percent": score_percent,
                "matching_interests": matching_interests,
                "is_top_pick": index == 0,
                "reason": (
                    f"Recommended because it matches {match_score} "
                    f"of your selected interests."
                ),
            }
        )

    return jsonify(
        {
            "user": {"name": user.name, "username": user.user_name, "age": user.age},
            "recommendations": formatted_recommendations,
        }
    )


if __name__ == "__main__":
    app.run()
