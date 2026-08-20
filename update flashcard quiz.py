import json
import random
import os
from datetime import datetime

DATA_FILE = "flashcards.json"


# -----------------------------
# DATA MANAGEMENT
# -----------------------------

def load_cards():
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_cards(cards):
    with open(DATA_FILE, "w") as file:
        json.dump(cards, file, indent=4)


# -----------------------------
# HELPER FUNCTIONS
# -----------------------------

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    input("\nPress Enter to continue...")


def get_card_by_id(cards, card_id):
    for card in cards:
        if card["id"] == card_id:
            return card
    return None


def generate_id(cards):
    if not cards:
        return 1
    return max(card["id"] for card in cards) + 1


# -----------------------------
# ADD FLASHCARD
# -----------------------------

def add_flashcard(cards):
    clear_screen()
    print("========== ADD FLASHCARD ==========\n")

    question = input("Question: ").strip()
    answer = input("Answer: ").strip()
    category = input("Category: ").strip()

    print("\nDifficulty:")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")

    choice = input("Choose difficulty: ")

    difficulty = {
        "1": "Easy",
        "2": "Medium",
        "3": "Hard"
    }.get(choice, "Medium")

    card = {
        "id": generate_id(cards),
        "question": question,
        "answer": answer,
        "category": category,
        "difficulty": difficulty,
        "times_seen": 0,
        "times_correct": 0,
        "times_wrong": 0,
        "last_reviewed": None
    }

    cards.append(card)
    save_cards(cards)

    print("\nFlashcard added successfully!")
    pause()


# -----------------------------
# VIEW FLASHCARDS
# -----------------------------

def view_cards(cards):
    clear_screen()
    print("========== ALL FLASHCARDS ==========\n")

    if not cards:
        print("No flashcards available.")
        pause()
        return

    for card in cards:
        print(f"ID: {card['id']}")
        print(f"Question: {card['question']}")
        print(f"Answer: {card['answer']}")
        print(f"Category: {card['category']}")
        print(f"Difficulty: {card['difficulty']}")
        print(
            f"Stats: {card['times_correct']} correct / "
            f"{card['times_wrong']} wrong"
        )
        print("-" * 45)

    pause()


# -----------------------------
# EDIT FLASHCARD
# -----------------------------

def edit_flashcard(cards):
    clear_screen()
    print("========== EDIT FLASHCARD ==========\n")

    if not cards:
        print("No flashcards available.")
        pause()
        return

    try:
        card_id = int(input("Enter card ID: "))
    except ValueError:
        print("Invalid ID.")
        pause()
        return

    card = get_card_by_id(cards, card_id)

    if not card:
        print("Flashcard not found.")
        pause()
        return

    print("\nLeave blank to keep the existing value.")

    question = input(f"Question [{card['question']}]: ").strip()
    answer = input(f"Answer [{card['answer']}]: ").strip()
    category = input(f"Category [{card['category']}]: ").strip()

    if question:
        card["question"] = question

    if answer:
        card["answer"] = answer

    if category:
        card["category"] = category

    print("\nDifficulty:")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")

    difficulty = input("New difficulty [Enter to keep]: ")

    if difficulty in ["1", "2", "3"]:
        card["difficulty"] = {
            "1": "Easy",
            "2": "Medium",
            "3": "Hard"
        }[difficulty]

    save_cards(cards)

    print("\nFlashcard updated!")
    pause()


# -----------------------------
# DELETE FLASHCARD
# -----------------------------

def delete_flashcard(cards):
    clear_screen()
    print("========== DELETE FLASHCARD ==========\n")

    try:
        card_id = int(input("Enter card ID: "))
    except ValueError:
        print("Invalid ID.")
        pause()
        return

    card = get_card_by_id(cards, card_id)

    if not card:
        print("Flashcard not found.")
        pause()
        return

    print(f"\nQuestion: {card['question']}")

    confirm = input("Delete this card? (y/n): ").lower()

    if confirm == "y":
        cards.remove(card)
        save_cards(cards)
        print("Flashcard deleted.")
    else:
        print("Deletion cancelled.")

    pause()


# -----------------------------
# STUDY MODE
# -----------------------------

def study_mode(cards):
    clear_screen()
    print("========== STUDY MODE ==========\n")

    if not cards:
        print("No flashcards available.")
        pause()
        return

    selected_cards = cards.copy()
    random.shuffle(selected_cards)

    for card in selected_cards:

        clear_screen()

        print(f"Category: {card['category']}")
        print(f"Difficulty: {card['difficulty']}")
        print("\nQUESTION:")
        print(card["question"])

        input("\nPress Enter to reveal answer...")

        print("\nANSWER:")
        print(card["answer"])

        card["times_seen"] += 1
        card["last_reviewed"] = datetime.now().strftime(
            "%Y-%m-%d %H:%M"
        )

        save_cards(cards)

        choice = input(
            "\nDid you know this? (y = correct / n = wrong / q = quit): "
        ).lower()

        if choice == "y":
            card["times_correct"] += 1
        elif choice == "n":
            card["times_wrong"] += 1
        elif choice == "q":
            break

        save_cards(cards)


# -----------------------------
# MULTIPLE CHOICE QUIZ
# -----------------------------

def create_options(card, cards):
    wrong_cards = [
        c for c in cards
        if c["id"] != card["id"]
    ]

    random.shuffle(wrong_cards)

    wrong_answers = [
        c["answer"]
        for c in wrong_cards[:3]
    ]

    options = wrong_answers + [card["answer"]]

    # If there aren't enough cards, add fallback options
    while len(options) < 4:
        options.append("None of the above")

    random.shuffle(options)

    return options[:4]


def quiz_mode(cards):
    clear_screen()
    print("========== QUIZ MODE ==========\n")

    if len(cards) < 2:
        print("Add at least 2 flashcards to start the quiz.")
        pause()
        return

    print("Choose category:")
    print("1. All")
    print("2. Select category")

    choice = input("\nChoice: ")

    if choice == "2":
        categories = sorted(
            set(card["category"] for card in cards)
        )

        print("\nCategories:")
        for i, category in enumerate(categories, 1):
            print(f"{i}. {category}")

        try:
            category_number = int(input("Select category: "))
            selected_category = categories[category_number - 1]

            quiz_cards = [
                card for card in cards
                if card["category"] == selected_category
            ]

        except (ValueError, IndexError):
            print("Invalid category.")
            pause()
            return

    else:
        quiz_cards = cards.copy()

    if len(quiz_cards) < 2:
        print("Not enough cards in this category.")
        pause()
        return

    random.shuffle(quiz_cards)

    try:
        number = int(
            input(
                f"\nHow many questions? (1-{len(quiz_cards)}): "
            )
        )
    except ValueError:
        print("Invalid number.")
        pause()
        return

    number = max(1, min(number, len(quiz_cards)))

    quiz_cards = quiz_cards[:number]

    score = 0
    wrong_answers = []

    for index, card in enumerate(quiz_cards, 1):

        clear_screen()

        print(
            f"Question {index}/{number}"
        )

        print(
            f"Category: {card['category']} | "
            f"Difficulty: {card['difficulty']}"
        )

        print("\n" + card["question"])

        options = create_options(card, cards)

        for i, option in enumerate(options, 1):
            print(f"\n{i}. {option}")

        while True:
            try:
                answer = int(input("\nYour answer: "))

                if 1 <= answer <= 4:
                    break

                print("Choose between 1 and 4.")

            except ValueError:
                print("Enter a number.")

        selected_answer = options[answer - 1]

        card["times_seen"] += 1
        card["last_reviewed"] = datetime.now().strftime(
            "%Y-%m-%d %H:%M"
        )

        if selected_answer == card["answer"]:
            print("\nCorrect!")
            score += 1
            card["times_correct"] += 1

        else:
            print("\nWrong!")
            print(f"Correct answer: {card['answer']}")

            card["times_wrong"] += 1

            wrong_answers.append({
                "question": card["question"],
                "your_answer": selected_answer,
                "correct_answer": card["answer"]
            })

        save_cards(cards)

        input("\nPress Enter for next question...")

    clear_screen()

    percentage = (score / number) * 100

    print("========== QUIZ RESULT ==========\n")

    print(f"Score: {score}/{number}")
    print(f"Percentage: {percentage:.2f}%")

    if percentage >= 90:
        print("Excellent!")
    elif percentage >= 75:
        print("Great job!")
    elif percentage >= 50:
        print("Good effort. Keep practicing!")
    else:
        print("Keep practicing — you'll improve!")

    if wrong_answers:

        print("\n========== REVIEW WRONG ANSWERS ==========\n")

        for item in wrong_answers:
            print(f"Q: {item['question']}")
            print(f"Your answer: {item['your_answer']}")
            print(f"Correct answer: {item['correct_answer']}")
            print("-" * 40)

    pause()


# -----------------------------
# SEARCH
# -----------------------------

def search_cards(cards):
    clear_screen()
    print("========== SEARCH ==========\n")

    keyword = input("Search: ").lower().strip()

    results = []

    for card in cards:

        text = (
            card["question"] + " " +
            card["answer"] + " " +
            card["category"]
        ).lower()

        if keyword in text:
            results.append(card)

    print(f"\nFound {len(results)} card(s).\n")

    for card in results:
        print(f"ID: {card['id']}")
        print(f"Q: {card['question']}")
        print(f"A: {card['answer']}")
        print(f"Category: {card['category']}")
        print("-" * 40)

    pause()


# -----------------------------
# STATISTICS
# -----------------------------

def statistics(cards):
    clear_screen()
    print("========== STATISTICS ==========\n")

    if not cards:
        print("No flashcards available.")
        pause()
        return

    total_seen = sum(
        card["times_seen"] for card in cards
    )

    total_correct = sum(
        card["times_correct"] for card in cards
    )

    total_wrong = sum(
        card["times_wrong"] for card in cards
    )

    print(f"Total flashcards: {len(cards)}")
    print(f"Times studied: {total_seen}")
    print(f"Correct answers: {total_correct}")
    print(f"Wrong answers: {total_wrong}")

    if total_seen:
        accuracy = (
            total_correct / total_seen
        ) * 100

        print(f"Overall accuracy: {accuracy:.2f}%")

    print("\n========== BY CATEGORY ==========\n")

    categories = sorted(
        set(card["category"] for card in cards)
    )

    for category in categories:

        category_cards = [
            card for card in cards
            if card["category"] == category
        ]

        seen = sum(
            c["times_seen"]
            for c in category_cards
        )

        correct = sum(
            c["times_correct"]
            for c in category_cards
        )

        accuracy = (
            correct / seen * 100
            if seen else 0
        )

        print(
            f"{category}: "
            f"{len(category_cards)} cards | "
            f"{accuracy:.1f}% accuracy"
        )

    pause()


# -----------------------------
# MAIN MENU
# -----------------------------

def main():

    cards = load_cards()

    while True:

        clear_screen()

        print("=" * 50)
        print("          FLASHCARD QUIZ APP")
        print("=" * 50)

        print("\n1. Add Flashcard")
        print("2. View Flashcards")
        print("3. Edit Flashcard")
        print("4. Delete Flashcard")
        print("5. Study Mode")
        print("6. Start Quiz")
        print("7. Search Flashcards")
        print("8. Statistics")
        print("9. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            add_flashcard(cards)

        elif choice == "2":
            view_cards(cards)

        elif choice == "3":
            edit_flashcard(cards)

        elif choice == "4":
            delete_flashcard(cards)

        elif choice == "5":
            study_mode(cards)

        elif choice == "6":
            quiz_mode(cards)

        elif choice == "7":
            search_cards(cards)

        elif choice == "8":
            statistics(cards)

        elif choice == "9":
            print("\nThanks for using Flashcard Quiz App!")
            break

        else:
            print("\nInvalid choice.")
            pause()


if __name__ == "__main__":
    main()