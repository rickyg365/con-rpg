import os
import sys

import time

from battle import Battle
from utility import clear_screen


class Scene:
    def __init__(self, scene_id, scene_data, scene_type="scene", delay=None):
        self.id = scene_id
        self.data = scene_data
        self.type = scene_type
        self.delay = delay

    def __str__(self):
        txt = f"[{self.id}]"
        return txt

    def show(self, debug=False):
        # Build Display
        txt = f"{self.data['data']}"
        if debug:
            txt = f"""Displaying Scene...

[{self.data['name']}]
{self.data['data']}"""
        
        # Clear Console and Display on Console
        clear_screen()
        print(txt)

        # haha can be an int or none idk if this is a good practice
        if self.delay is None:
            input("> ")
        else:
            time.sleep(self.delay)


class BattleScene(Scene):
    def __init__(self, scene_id, player, enemy):
        super().__init__(scene_id, scene_data={}, scene_type='battle')
        self.player = player
        self.enemy = enemy

    def __str__(self):
        return super().__str__()
    
    def show(self):
        new_battle = Battle(self.player, self.enemy)

        try:
            new_battle.run()
        except KeyboardInterrupt:
            print("\n[Quit Program]\n")


class SceneManager:
    def __init__(self):
        self.length = 0
        self.scenes = {}

    def __str__(self):
        txt = f"Length: {self.length}"
        return txt
        
    def scene_check(self, scene_id):
        if scene_id in self.scenes.keys():
            return True
        return False

    def validate_length(self):
        self.length = len(self.scenes.keys())

    def add(self, new_scene):
        # Check if already exists
        already_exists = self.scene_check(new_scene.id)

        if already_exists:
            return False

        self.scenes[new_scene.id] = new_scene
        self.length += 1
        return True

    def remove(self, scene_id):
        valid_scene = self.scene_check(scene_id)
        
        if not valid_scene:
            return False
        
        del self.scenes[scene_id]
        self.length -= 1
        return True

    
    def get(self, scene_id):
        # valid_scene = self.scene_check(scene_id)

        # if not valid_scene:
        #     return None
        chosen_scene = self.scenes.get(scene_id, None)
        return chosen_scene

    def run(self, single_loop=False, pause_time=.1):
        # assuming we are using a sorted dict
        # or we can add a sort function and make a lit in id order 

        # infinite loop
        list_of_scenes = list(self.scenes.values())
        list_length = len(list_of_scenes)

        max_loops = 0
        current_index = 0

        while True:
            # Break Condition
            if max_loops == 100:
                break

            # Select Current Scene
            current_scene = list_of_scenes[current_index]

            '''
            display scene 
            -> 

                current_scene.run()
            
            '''

            # Display Scene
            current_scene.show()
            # print(current_scene)
            
            time.sleep(pause_time)

            # End Conditions
            current_index += 1

            if current_index == list_length:
                if single_loop:
                    break
                current_index = 0

        return


def main():
    my_scene = SceneManager()

    for i in range(5):
        new_id = i+1

        sample_scene_data = {
            'name': "test scene",
            'data': f"""Scene {new_id} Running...""",
        }

        new_scene = Scene(new_id, sample_scene_data)

        my_scene.add(new_scene)

    print(my_scene)

    # print(my_scene.get(4))

    my_scene.run(True, 2)
    
    return 1


if __name__ == "__main__":
    main()
