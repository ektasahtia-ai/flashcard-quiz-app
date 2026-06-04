import random

flashcards = {
    "What is the capital of India?": "Delhi",
    "Who developed Python?": "Guido van Rossum",
    "What is 5 + 7?": "12",
    "Which planet is known as the Red Planet?": "Mars",
    "What does CPU stand for?": "Central Processing Unit"
}

score = 0

questions = list(flashcards.keys())
random.shuffle(questions)

print("=== Flashcard Quiz App ===\n")

for question in questions:
    answer = input(question + "\nYour Answer: ")

    if answer.lower() == flashcards[question].lower():
        print("✅ Correct!\n")
        score += 1
    else:
        print(f"❌ Wrong! Correct answer: {flashcards[question]}\n")

print("=== Quiz Finished ===")
print(f"Your Score: {score}/{len(flashcards)}")

percentage = (score / len(flashcards)) * 100
print(f"Percentage: {percentage:.2f}%")