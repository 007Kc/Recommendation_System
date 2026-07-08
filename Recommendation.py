# ─────────────────────────────────────────────
# Course Catalogue
# Each course maps to a list of relevant tags
# used for interest-based recommendations
# ─────────────────────────────────────────────
courses = {
# Introductory course covering core Python concepts
"Python Basics":
["python", "programming", "coding", "beginner", "automation"],
# Overview of artificial intelligence and ML concepta
"AI Fundamentals":
["ai", "machine learning", "python", "data", "automation"],
# Frontend web development using core web technologies
"Web Development":
["html", "css", "javascript", "web design", "frontend"],
# Design course focused on user interface and experience
"UI / UX Design":
["design", "figma", "ui", "ux", "creativity"],
# Data-focused course covering analysis and statistical methods
"Data Science":
["data", "python", "analytics", "statistics", "machine learning"]
}


# ─────────────────────────────────────────────
# User Class
# Stores user profile details and interests
# collected during onboarding
# ─────────────────────────────────────────────

class User:

    # Initializes a new user with their personal details and selected interests
    def __init__(self, name, user_name, age, interests):
        self.name = name              # User's full name
        self.user_name = user_name    # Chosen username/handle
        self.age = age                # User's age
        self.interests = interests    # List of topics the user is interested in

    # Prints a summary of the user's profile to the console
    def display_user_info(self):
        print(f"Name: {self.name}\n"
              f"Username: {self.user_name}\n"
              f"Age: {self.age}\n"
              f"Interests: {self.interests}")



# ─────────────────────────────────────────────
# Recommendation System Class
# Analyses user interests and matches them
# against available courses using a tag-based
# similarity algorithm
# ─────────────────────────────────────────────

class Recommendation_System:

    # Initializes the recommendation system with a User object
    def __init__(self, user):
        self.user = user

    # Compares course tags against the user's interests
    # and scores each course based on the number of matches
    def similarity_check(self):

        suggestions = []  # Stores (course_name, match_score)

        for course_name, course_tags in courses.items():
            match = 0  # Reset match counter for each course

            for tag in course_tags:
                # Capitalize tag to match the format of stored user interests
                if tag.capitalize() in self.user.interests:
                    match += 1  # Increment score for each matching tag

            # Only include courses with at least one matching tag
            if match > 0:
                suggestions.append((course_name, match))



        return suggestions  # Returns list of matched courses with their scores

        # Retrieves, sorts, and displays course recommendations
        # in descending order of relevance to the user's interests
    def display_recommendations(self):

        # Fetch matched courses with their similarity scores
        recommendations = self.similarity_check()

        # Sort courses by match score (highest relevance first)
        recommendations.sort(key=lambda x: x[1], reverse=True)
        if len(recommendations) == 0:
            print("No Recommended courses,\n An error occurred somewhere")
        else:
            print("Recommended Courses:\n")

            # Loop through sorted recommendations and display them numbered
            for index, (course_name, match) in enumerate(recommendations, start=1):
                print(f"Course {index}. {course_name}")




# ═════════════════════════════════════════════════════
# FILE SUMMARY — Recommendation.py
# ═════════════════════════════════════════════════════
# This module contains the core logic for Kc's Learning
# Platform recommendation system.
#
# Contents:
#   • courses         — Dictionary of available courses
#                       and their associated interest tags
#
#   • User            — Class representing a platform user,
#                       storing their name, username, age,
#                       and selected interests
#
#   • Recommendation_System — Class that compares user
#                       interests against course tags and
#                       returns ranked course suggestions
#
# Used by: main.py
# ═════════════════════════════════════════════════════







