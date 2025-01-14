import json
from os import getcwd
import os

from unittest import case

from Player import Player

class Story:
    def __init__(self, levels):
        self.levels = levels
        self.actLevel = self.levels[0]

    def doOption(self, player, command):
        l, change = self.actLevel.doOption(player, command)
        self.setActLevel(l, change)

    def setActLevel(self, l, change):
        l = ''.join(filter(str.isdigit, l))
        self.actLevel = self.levels[int(l)-1]
        if change:
            self.actLevel.print_title()


class Level:
    def __init__(self, level_name, scenes, next_level):
        self.level_name = level_name
        self.scenes = scenes
        self.next_level = next_level
        self.actScene = self.scenes["scene1"]

    def print_story(self, player):
        self.actScene.print_story(player)

    def doOption(self, player, command):
        sceneKey = self.actScene.doOption(player, command)
        if sceneKey == None:
            return self.next_level, True
        else:
            self.actScene = self.scenes[sceneKey]
            return self.level_name, False

    def print_title(self):
        print(f"------ {self.level_name} ------")
        print()

class Scene:
    def __init__(self, scene_id, text, options):
        self.scene_id = scene_id
        self.text = text
        self.options = options

    def print_story(self, player):
        print(player.adjust_text(self.text))
        for i in range(1, len(self.options) + 1):
            print(f"{i}. {player.adjust_text(self.options[i-1].text)}")

    def doOption(self, player, command):
        index = int(command)-1
        return self.options[index].doOption(player)


class Option:
    def __init__(self, option_text, result_text, actions, next_scene):
        self.text = option_text
        self.result = result_text
        self.actions = actions
        self.next_scene = next_scene

    def doOption(self, player):
        print(player.adjust_text(self.result))
        player.doAction(self.actions)
        print()
        if self.next_scene == "end":
            return None
        else:
            return self.next_scene

class StoryHandling:
    def __init__(self, player):
        directory = getcwd()
        self.story = self.load_story(directory + "\data\story2.json")
        self.player = player

    def load_story(self, json_file_path):
        """Load a Story object from a JSON file."""
        # Step 1: Load JSON data from the file
        with open(json_file_path, "r") as file:
            data = json.load(file)

        # Step 2: Parse levels
        levels = [self.load_level(level_name, level_data) for level_name, level_data in data.items()]

        # Step 3: Return a Story object
        return Story(levels=levels)

    def load_level(self, level_name, level_data):
        """Load a Level object from JSON data."""
        scenes = {scene_id: self.load_scene(scene_id, scene_data) for scene_id, scene_data in level_data["scenes"].items()}
        return Level(
            level_name=level_name,
            scenes=scenes,
            next_level=level_data.get("next")  # Use .get() in case "next" is not present
        )

    def load_scene(self, scene_id, scene_data):
        """Load a Scene object from JSON data."""
        options = [self.load_option(option) for option in scene_data["options"]]
        return Scene(
            scene_id=scene_id,
            text=scene_data["text"],
            options=options
        )

    def load_option(self, option_data):
        """Load an Option object from JSON data."""
        return Option(
            option_text=option_data["option_text"],
            result_text=option_data["result_text"],
            actions=option_data["actions"],
            next_scene=option_data["next"]
        )

    def reset(self):
        self.player.restore_credentials()
        directory = getcwd()
        self.story = self.load_story(directory + "\data\story2.json")

    def save_game(self):
        directory = getcwd() + "\data\saves"
        # Ensure the directory exists
        if not os.path.exists(directory):
            os.makedirs(directory)
        self.player.save_game(directory)


    def set_progress(self):
        level = self.story.actLevel.level_name
        scene = self.story.actLevel.actScene.scene_id
        self.player.set_progress(level, scene)

    def start_story(self):
        while True:
            self.set_progress()
            if self.player.lives == 0:
                print("------ You died ------")
                self.reset()
            self.story.actLevel.print_story(self.player)
            command = input()
            match(command):
                case "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9":
                    self.story.doOption(self.player, command)
                    #print(self.story.actLevel)
                case "/h":
                    print('''Type the number of the option you want to choose.
Commands you can use:
/i => Shows inventory.
/q => Exits the game.
/c => Shows the character traits.
/s => Save the game
/h => Shows help.''')
                case "/c":
                    self.player.print_traits()
                case "/i":
                    self.player.print_inventory()
                case "/q":
                    print("Thanks for playing!")
                    exit()
                case "/s":
                    self.save_game()
                case _:
                    print("Wrong command!")
