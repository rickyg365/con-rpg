import os

from player import Player, Enemy
from utility import clear_screen
from items import Item, HealItem
from scenes import SceneManager, Scene, BattleScene

from battle import Battle
'''


'''
cols, rows = os.get_terminal_size()

def main():
    sample_bag = {
        'medicinal herb': 2,
        'small potion': 3,
        'medium potion': 1,
        'large potion': 1,
        'escape rope': 1,
    }
    new_player = Player("Hero", prebuilt_bag=sample_bag)
    # new_enemy = Enemy()

    main_game = SceneManager()

    # sample_scene_data = {
    #     'name': "test scene",
    #     'data': f"""Scene {new_id} Running...""",
    # }

    main_game.add(Scene(1, {
        'name': "intro scene",
        'data': f"""\n\n\n\n\n\n{'Welcome!':^{cols}}\n\n\n\n\n\n""",
    }, delay=3))
    main_game.add(BattleScene(2, new_player, Enemy()))

    main_game.add(Scene(3, {
        "name": "Outro Scene",
        "data": f"""\n\n\n\n\n\n{'Game Over!':^{cols}}\n\n\n\n\n\n"""
    }, delay=3))

    main_game.run(True)
    

if __name__ == "__main__":
    main()
