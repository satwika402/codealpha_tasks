import random
from colorama import Fore, Style, init

init(autoreset=True)

# Exactly 5 categories, each with exactly 5 predefined words.
WORDS = {
    "Movies": ["inception", "avatar", "titanic", "matrix", "joker"],
    "Countries": ["canada", "india", "brazil", "france", "japan"],
    "Tech": ["python", "network", "binary", "server", "kernel"],
    "Fruits": ["apple", "mango", "grape", "orange", "kiwi"],
    "Space": ["galaxy", "orbit", "comet", "planet", "rocket"]
}

MAX_ATTEMPTS = 6
DIFFICULTY_HINTS = {
    "easy": 2,
    "medium": 1,
    "hard": 0,
}

HANGMAN_STAGES = [
    """
    +---+
    |   |
        |
        |
        |
        |
    =========
    """,
    """
    +---+
    |   |
    O   |
        |
        |
        |
    =========
    """,
    """
    +---+
    |   |
    O   |
    |   |
        |
        |
    =========
    """,
    """
    +---+
    |   |
    O   |
   /|   |
        |
        |
    =========
    """,
    """
    +---+
    |   |
    O   |
   /|\\  |
        |
        |
    =========
    """,
    """
    +---+
    |   |
    O   |
   /|\\  |
   /    |
        |
    =========
    """,
    """
    +---+
    |   |
    O   |
   /|\\  |
   / \\ |
        |
    =========
    """
]


def choose_category():
    """Let the user choose a category before each round."""
    print(Fore.CYAN + "\n=== CATEGORY MENU ===" + Style.RESET_ALL)
    print(Fore.GREEN + "[1] Movies" + Style.RESET_ALL)
    print(Fore.GREEN + "[2] Countries" + Style.RESET_ALL)
    print(Fore.GREEN + "[3] Tech" + Style.RESET_ALL)
    print(Fore.GREEN + "[4] Fruits" + Style.RESET_ALL)
    print(Fore.GREEN + "[5] Space" + Style.RESET_ALL)
    print(Fore.RED + "[6] Quit" + Style.RESET_ALL)

    while True:
        category_choice = input(Fore.BLUE + "Select option: " + Style.RESET_ALL).strip().lower()
        if category_choice in ["6", "q", "quit"]:
            print(Fore.RED + "You quit the game." + Style.RESET_ALL)
            raise SystemExit
        for idx, category in enumerate(WORDS.keys(), start=1):
            if str(idx) == category_choice:
                return category
            if category.lower() == category_choice:
                return category
        print(Fore.RED + "Invalid category. Choose a number or category name from the list." + Style.RESET_ALL)


def choose_difficulty():
    """Let the user choose a difficulty and return hint count for that round."""
    print(Fore.CYAN + "\n=== DIFFICULTY MENU ===" + Style.RESET_ALL)
    print(Fore.YELLOW + "[1] Easy   -> 2 hints" + Style.RESET_ALL)
    print(Fore.YELLOW + "[2] Medium -> 1 hint" + Style.RESET_ALL)
    print(Fore.YELLOW + "[3] Hard   -> 0 hints" + Style.RESET_ALL)
    print(Fore.RED + "[4] Quit" + Style.RESET_ALL)

    while True:
        difficulty_choice = input(Fore.BLUE + "Select option: " + Style.RESET_ALL).strip().lower()
        if difficulty_choice in ["4", "q", "quit"]:
            print(Fore.RED + "You quit the game." + Style.RESET_ALL)
            raise SystemExit
        if difficulty_choice == "1":
            return "easy"
        if difficulty_choice == "2":
            return "medium"
        if difficulty_choice == "3":
            return "hard"
        if difficulty_choice in DIFFICULTY_HINTS:
            return difficulty_choice
        print(Fore.RED + "Invalid difficulty. Choose 1, 2, 3, Easy, Medium, or Hard, or Quit." + Style.RESET_ALL)


def display_word(word, guessed_letters):
    """Show the hidden word using underscores and reveal correct guessed letters in green."""
    displayed = []
    for letter in word:
        if letter in guessed_letters:
            displayed.append(Fore.GREEN + letter + Style.RESET_ALL)
        else:
            displayed.append("_")
    return " ".join(displayed)


def display_status_panel(category, wrong_guesses, hints_left, guessed_letters, wrong_letters, word):
    """Show a more presentable status panel with the category separated and the wrong-letters list visible."""
    attempts_left = MAX_ATTEMPTS - wrong_guesses
    wrong_list = ", ".join(wrong_letters) if wrong_letters else "None"
    correct_word = display_word(word, guessed_letters)

    # Category block above the panel
    print(Fore.CYAN + "\n" + "=" * 60 + Style.RESET_ALL)
    print(Fore.MAGENTA + "CATEGORY: " + category + Style.RESET_ALL)
    print(Fore.CYAN + "=" * 60 + Style.RESET_ALL)

    # Main boxed panel
    print(Fore.CYAN + "╔" + "═" * 60 + "╗" + Style.RESET_ALL)
    print(Fore.CYAN + "║" + Style.RESET_ALL + Fore.RED + " Wrong Guesses  " + Style.RESET_ALL +
          Fore.WHITE + f"{wrong_guesses}/{MAX_ATTEMPTS}".rjust(26) + Style.RESET_ALL + Fore.CYAN + "║" + Style.RESET_ALL)
    print(Fore.CYAN + "║" + Style.RESET_ALL + Fore.YELLOW + " Attempts Left  " + Style.RESET_ALL +
          Fore.WHITE + str(attempts_left).rjust(26) + Style.RESET_ALL + Fore.CYAN + "║" + Style.RESET_ALL)
    print(Fore.CYAN + "║" + Style.RESET_ALL + Fore.RED + " Wrong Letters  " + Style.RESET_ALL +
          Fore.WHITE + wrong_list[:44].rjust(26) + Style.RESET_ALL + Fore.CYAN + "║" + Style.RESET_ALL)
    print(Fore.CYAN + "║" + Style.RESET_ALL + Fore.MAGENTA + " Hints Left     " + Style.RESET_ALL +
          Fore.WHITE + str(hints_left).rjust(26) + Style.RESET_ALL + Fore.CYAN + "║" + Style.RESET_ALL)
    print(Fore.CYAN + "║" + Style.RESET_ALL + Fore.GREEN + " Word           " + Style.RESET_ALL +
          Fore.WHITE + correct_word.rjust(26) + Style.RESET_ALL + Fore.CYAN + "║" + Style.RESET_ALL)
    print(Fore.CYAN + "╚" + "═" * 60 + "╝" + Style.RESET_ALL)


def display_hangman_stage(wrong_guesses):
    """Show the ASCII hangman stage for 0 through 6 wrong guesses."""
    print(HANGMAN_STAGES[wrong_guesses])


def get_valid_guess(guessed_letters, hints_left):
    """Read input, handling hint command, repeated guesses, invalid input, and quit gracefully."""
    while True:
        guess = input(Fore.BLUE + "Enter a letter, type HINT, or type QUIT: " + Style.RESET_ALL).strip().lower()

        if guess in ["q", "quit"]:
            print(Fore.RED + "You quit the game." + Style.RESET_ALL)
            raise SystemExit

        # HINT command reveals one random unguessed letter.
        if guess == "hint":
            if hints_left <= 0:
                print("No hints left for this round.")
                continue
            return "HINT"

        # Only allow a single alphabetic character.
        if not guess.isalpha() or len(guess) != 1:
            print("Invalid input! Please enter one letter only, or type HINT/QUIT.")
            continue

        # Prevent repeated guesses.
        if guess in guessed_letters:
            print("You already guessed that letter. Try a different one.")
            continue

        return guess


def use_hint(word, guessed_letters, hints_left):
    """Reveal one random unguessed letter from the word and consume one hint credit."""
    if hints_left <= 0:
        print("No hints left for this round.")
        return guessed_letters, hints_left, False

    unguessed_letters = sorted(set(word) - set(guessed_letters))
    if not unguessed_letters:
        print("No unguessed letters remain.")
        return guessed_letters, hints_left, False

    chosen_letter = random.choice(unguessed_letters)
    guessed_letters.append(chosen_letter)
    hints_left -= 1
    print(f"Hint used: the word contains the letter '{chosen_letter}'.")
    return guessed_letters, hints_left, True


def play_round(wins, losses, current_streak, best_streak):
    """Play one complete Hangman round and update session scores and streaks."""
    try:
        category = choose_category()
        difficulty = choose_difficulty()
    except SystemExit:
        print(Fore.CYAN + "\nFinal Summary" + Style.RESET_ALL)
        print(f"Wins: {wins}")
        print(f"Losses: {losses}")
        print(f"Best Streak: {best_streak}")
        print(Fore.MAGENTA + "\nCodeAlpha Internship – Task 1: Hangman Game" + Style.RESET_ALL)
        raise

    hints_left = DIFFICULTY_HINTS[difficulty]

    # Choose a word from the selected category.
    word = random.choice(WORDS[category])
    guessed_letters = []
    wrong_letters = []
    wrong_guesses = 0
    game_won = False

    print(f"\nCategory: {category}")
    print(f"Difficulty: {difficulty.title()}")
    print("The word is ready. Start guessing!\n")

    # Play until correct word is guessed or a player reaches 6 wrong guesses.
    while wrong_guesses < MAX_ATTEMPTS:
        display_hangman_stage(wrong_guesses)
        display_status_panel(category, wrong_guesses, hints_left, guessed_letters, wrong_letters, word)

        try:
            guess = get_valid_guess(guessed_letters, hints_left)
        except SystemExit:
            print(Fore.CYAN + "\nFinal Summary" + Style.RESET_ALL)
            print(f"Wins: {wins}")
            print(f"Losses: {losses}")
            print(f"Best Streak: {best_streak}")
            print(Fore.MAGENTA + "\nCodeAlpha Internship – Task 1: Hangman Game" + Style.RESET_ALL)
            raise

        # If the player types HINT, reveal one random letter and do not count as a wrong guess.
        if guess == "HINT":
            guessed_letters, hints_left, used_hint = use_hint(word, guessed_letters, hints_left)
            if used_hint:
                print(Fore.MAGENTA + f"Hints Left: {hints_left}" + Style.RESET_ALL)
                print("Word:", display_word(word, guessed_letters))
                continue

            # If input was HINT and no hint is available, ask again.
            continue

        # If a single-letter guess is entered, add it to guessed letters.
        guessed_letters.append(guess)

        if guess in word:
            print("Correct guess!")
        else:
            wrong_guesses += 1
            wrong_letters.append(guess)
            print("Wrong guess!")

        attempts_left = MAX_ATTEMPTS - wrong_guesses
        print(Fore.YELLOW + f"Attempts Left: {attempts_left}" + Style.RESET_ALL)
        print("Word:", display_word(word, guessed_letters))

        # Win condition.
        if all(letter in guessed_letters for letter in word):
            game_won = True
            wins += 1
            current_streak += 1
            if current_streak > best_streak:
                best_streak = current_streak
            print(Fore.GREEN + "\nWIN" + Style.RESET_ALL)
            print(f"You guessed the word: {word}")
            print(Fore.GREEN + "You WON" + Style.RESET_ALL)
            print(f"Current Streak: {current_streak}")
            print(f"Best Streak: {best_streak}")
            break

    # Loss condition after wrong_guesses reaches maximum.
    if not game_won:
        losses += 1
        current_streak = 0
        print(Fore.RED + "\nGAME OVER" + Style.RESET_ALL)
        print(f"The word was: {word}")
        print(Fore.RED + "You LOST" + Style.RESET_ALL)
        print(f"Current Streak: {current_streak}")
        print(f"Best Streak: {best_streak}")

    # Return updated tracking numbers for the end of session.
    return wins, losses, current_streak, best_streak


def show_final_summary(wins, losses, best_streak):
    """Display the final summary and the mandatory CodeAlpha message."""
    print(Fore.CYAN + "\nFinal Summary" + Style.RESET_ALL)
    print(f"Wins: {wins}")
    print(f"Losses: {losses}")
    print(f"Best Streak: {best_streak}")
    print(Fore.MAGENTA + "\nCodeAlpha Internship – Task 1: Hangman Game" + Style.RESET_ALL)


def main():
    """Main loop for the game. Keeps score, streak, and play-again behavior."""
    wins = 0
    losses = 0
    current_streak = 0
    best_streak = 0

    while True:
        try:
            wins, losses, current_streak, best_streak = play_round(wins, losses, current_streak, best_streak)
        except SystemExit:
            show_final_summary(wins, losses, best_streak)
            return

        while True:
            print(Fore.CYAN + "\n=== PLAY AGAIN MENU ===" + Style.RESET_ALL)
            print(Fore.GREEN + "[1] Yes" + Style.RESET_ALL)
            print(Fore.RED + "[2] No" + Style.RESET_ALL)
            print(Fore.RED + "[3] Quit" + Style.RESET_ALL)
            again = input(Fore.BLUE + "Select option: " + Style.RESET_ALL).strip().lower()
            if again in ["1", "yes", "y"]:
                break
            elif again in ["2", "no", "n"]:
                show_final_summary(wins, losses, best_streak)
                return
            elif again in ["3", "q", "quit"]:
                show_final_summary(wins, losses, best_streak)
                return
            else:
                print(Fore.RED + "Invalid input! Choose 1 for Yes, 2 for No, or 3 to Quit." + Style.RESET_ALL)


if __name__ == "__main__":
    main()
