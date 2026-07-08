# ─────────────────────────────────────────────
# Imports
# ─────────────────────────────────────────────
import Recommendation as rec   # Core recommendation and user logic
from time import sleep          # Used for timed delays and animations


# ─────────────────────────────────────────────
# Collects the user's personal details
# Validates age input to ensure it's a number
# Returns name, username and age as a tuple
# ─────────────────────────────────────────────
def collect_user_details():
    name = input("Enter your fullname: ")
    username = input("Enter your username: ")

    # Keep prompting until a valid integer age is entered
    while True:
        try:
            age = int(input("Enter your age: "))
            break
        except ValueError:
            print("Invalid age ")

    # Animated loading sequence after details are collected
    processes = ["Processing...      ", "Almost done...     ", "Complete! ✅        "]
    for process in processes:
        print(process, end="\r", flush=True)
        sleep(3)
    print()

    return name, username, age


# ─────────────────────────────────────────────
# Builds a unique list of all available
# interest tags pulled from the course catalogue
# ─────────────────────────────────────────────
def available_interest():
    available_interests = []

    for course_name, course_tags in rec.courses.items():
        for tags in course_tags:
            # Only add tag if it hasn't been added already (avoids duplicates)
            if tags.capitalize() not in available_interests:
                available_interests.append(tags.capitalize())

    return available_interests


# ─────────────────────────────────────────────
# Displays available interests to the user
# and collects their selections by index
# Returns a list of the user's chosen interests
# ─────────────────────────────────────────────
def collect_user_interests():
    list_of_interests = available_interest()

    # Display all available interests with their index numbers
    print("\nSelect your interests: ")
    for index, interest in enumerate(list_of_interests, start=1):
        print(f" {index}. {interest}")

    # Keep prompting until valid index input is received
    while True:
        index_list = []
        user_interests_index = input("\nEnter the index number of your interests. Ensure to separate it with a comma: ")


        try:
            for index in user_interests_index.split(","):
                index_list.append(int(index.strip()))

        except ValueError:
            print("Please enter valid numbers separated by commas!")
            continue  # Re-prompt if a non-integer value is entered

        break
    try:
        # Map selected indexes back to their corresponding interest names
        user_interest = []
        for interest_index in index_list:
            user_interest.append(list_of_interests[(interest_index - 1)])
    except IndexError:
        pass

    return user_interest


# ─────────────────────────────────────────────
# Main Function
# Entry point of the program
# the full user onboarding and recommendation
# ─────────────────────────────────────────────
def main():
    # Welcome message
    print("Welcome to Kc's learning platform🥳\nWhere learning becomes fun😁")
    sleep(2)

    # Collect user profile details
    print("\nFill in your credentials below: ")
    user_details = collect_user_details()

    # Collect user interests
    user_interests = collect_user_interests()

    # Create a User object with the collected details
    user = rec.User(user_details[0], user_details[1], user_details[2], user_interests)

    # Animated loading sequence while recommendations are being generated
    print("\nWait while we recommend courses for you based on your interests....")
    steps = ["Fetching data...   ", "Processing...      ", "Almost done...     ", "Complete! ✅  "]
    for step in steps:
        print(step, end="\r", flush=True)
        sleep(2)

    # Generate and display recommendations
    rec_sys = rec.Recommendation_System(user)
    rec_sys.display_recommendations()

    # Closing message
    print("\nThanks for choosing Kc's learning platform")
    sleep(1)
    print("We shall be adding courses soon🤧")

if __name__ == "__main__":
    main()


# ─────────────────────────────────────────────
# Run the program
# ─────────────────────────────────────────────
main()


# ═════════════════════════════════════════════════════
# FILE SUMMARY — main.py
# ═════════════════════════════════════════════════════
# This is the entry point for Kc's Learning Platform.
#
# Contents:
#   • collect_user_details()    — Gathers name, username
#                                 and age from the user
#
#   • available_interest()      — Extracts a unique list
#                                 of interests from the
#                                 course catalogue
#
#   • collect_user_interests()  — Displays interests and
#                                 captures user selections
#
#   • main()                    — Orchestrates the full
#                                 onboarding and course
#                                 recommendation flow
#
# Depends on: Recommendation.py
# ═════════════════════════════════════════════════════