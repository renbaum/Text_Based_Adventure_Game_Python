import json
from copy import deepcopy


class Player:
    def __init__(self):
        self.user = ""
        self.name = ""
        self.species = ""
        self.gender = ""
        self.lives = 0
        self.difficulty = ""
        self.inventory = {}
        self.progress = {}
        self.stored_player = None

    def __str__(self):
        return f"""Good luck on your journey, {self.user}!
Your character: {self.name}, {self.species}, {self.gender}
Your inventory: {self.inventory["snack"]}, {self.inventory["weapon"]}, {self.inventory["tool"]}
Difficulty: {self.difficulty}
Number of lives: {self.lives}"""

    def dummy(self):
        self.user = "Hyperskill"
        self.name = "John"
        self.species = "Human"
        self.gender = "male"
        self.difficulty = "hard"
        self.lives = 1
        self.add_item("apple", "snack")
        self.add_item("sword", "weapon")
        self.add_item("pickaxe", "tool")
        self.stored_player = None
        self.store_credentials()

    def init_player(self):
        if not self.create_user(): return False
        self.create_character()
        self.create_inventory()
        self.choose_dificulty()
        self.store_credentials()
        print(self)
        return True

    def set_progress(self, level, scene):
        self.progress["scene"] = scene
        self.progress["level"] = level

    def store_credentials(self):
        self.stored_player = Player()
        self.stored_player.lives = 1
        self.stored_player.inventory = deepcopy(self.inventory)

    def restore_credentials(self):
        self.lives = self.stored_player.lives
        self.inventory = deepcopy(self.stored_player.inventory)

    def add_item(self, item, type):
        self.inventory[type] = item

    def remove_item(self, type):
        del self.inventory[type]

    def create_user(self):
        self.user = input("Enter a username ('/b' to go back): ")
        if self.user == "/b":
            return False
        return True

    def create_character(self):
        print("Create your character:")
        self.name = input("   Name: ")
        self.species = input("   Species: ")
        self.gender = input("   Gender: ")

    def create_inventory(self):
        print("Pack your bag for the journey:")
        self.add_item(input("   Snack: "), "snack")
        self.add_item(input("   Weapon: "), "weapon")
        self.add_item(input("   Tool: "), "tool")

    def choose_dificulty(self):
        print("Choose your difficulty:")
        print("   1. Easy")
        print("   2. Medium")
        print("   3. Hard")
        while True:
            self.difficulty = input()
            match self.difficulty.lower():
                case "1" | "easy":
                    self.lives = 5
                    self.difficulty = "easy"
                    break
                case "2" | "medium":
                    self.lives = 3
                    self.difficulty = "medium"
                    break
                case "3" | "hard":
                    self.lives = 1
                    self.difficulty = "hard"
                    break
                case _:
                    print("Unknown input! Please enter a valid one.")

    def play_remove(self, item):
        value = self.inventory[item]
        self.remove_item(item)
        print(f"------ Item removed: {value} ------")

    def play_add(self, item):
        self.add_item(item, item)
        print(f"------ Item added: {item} ------")

    def doAction(self, actions):
        for action in actions:
            if action == "": continue
            if action.startswith("-{") and action.endswith("}"):
                self.play_remove(action[2:-1])
            elif action.startswith("+") and not action.endswith("}"):
                self.add_item(action[1:], action[1:])
            elif action.startswith("-") and not action.endswith("}"):
                self.play_remove(action[1:])
            elif action == "heal":
                self.change_health(1)
            elif action == "hit":
                self.change_health(-1)

    def change_health(self, amount):
        self.lives += amount
        print(f"Lives remaining: {self.lives}")

    def print_traits(self):
        print(f"Your character: {self.name}, {self.species}, {self.gender}.")
        print(f"Lives remaining: {self.lives}")

    def print_inventory(self):
        str_inv = ""
        for key, value in self.inventory.items():
            if str_inv == "":
                str_inv += f"{value}"
            else:
                str_inv += f", {value}\n"
        print(f"Inventory: {str_inv}")
        
    def adjust_text(self, text):
        for key, value in self.inventory.items():
            placeholder =  "{" + key + "}"
            text = text.replace(placeholder, value)
        return text

    def save_game(self, directory):
        filename = f"{directory}\\{self.user}.json"
        # Gather the data in the required JSON structure
        data = {"character": {
                    "name": self.name,
                    "species": self.species,
                    "gender": self.gender
                },
                "inventory": {
                    "snack_name": self.inventory.get("snack", ""),
                    "weapon_name": self.inventory.get("weapon", ""),
                    "tool_name": self.inventory.get("tool", ""),
                    "content": list(self.inventory.values())
                },
                "progress": {
                    "level": self.progress["level"],
                    "scene": self.progress["scene"]
                },
                "lives": self.lives,
                "difficulty": self.difficulty
            }

        # Write data to a JSON file
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)
        print("Game saved!")