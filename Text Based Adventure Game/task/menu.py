from Player import Player
from Story import StoryHandling

class MainMenu:
    def __init__(self):
        self.show_title()
        self.exit_game = False

    def do_game_loop(self):
        while not self.exit_game:
            self.show_main_menu()
            self.exit_game = self.get_main_input()


    def show_main_menu(self):
        print("1. Start a new game (START)")
        print("2. Load your progress (LOAD)")
        print("3. Quit the game (QUIT)")

    def show_title(self):
        print("***Welcome to the Journey to Mount Qaf***")
        print()

    def get_main_input(self):
        while True:
            choice = input().lower()
            match choice:
                case "1" | "start":
                    print("Starting a new Game")
                    player = Player()
                    player.dummy()
#                    player.init_player()
                    story = StoryHandling(player)
                    story.start_story()


                    return False
                case "2" | "load":
                    print("Loading your progress")
                case "3" | "quit":
                    break
                case _:
                    print("Unknown input! Please enter a valid one.")
        return True
