import os
from utility import buildHPBar, box, clear_screen
from items import Bag, Item, HealItem

class Player:
    def __init__(self, name, job="warrior", prebuilt_bag=None):
        # Check for pre built bag
        if prebuilt_bag is None:
            prebuilt_bag = {}

        # Create Bag
        self.bag = Bag(prebuilt_bag)
        self.processed_item_db = {
            'medicinal herb': HealItem(1, 'medicinal herb', False, 15),
            'small potion': HealItem(2, 'small potion', False, 10),
            "medium potion": HealItem(3, 'medium potion', False, 20),
            'large potion': HealItem(4, 'large potion', False, 30),
            'escape rope': Item(5, 'escape rope', 'utility', False)
        }
        self.raw_item_db = {
            'medicinal herb': {
                'id': 1,
                'name': 'medicinal herb',
                'type': 'heal',
                'amount': 15,
                'reuse': False
            },
            'small potion': {
                'id': 2,
                'name': 'small potion',
                'type': 'heal',
                'amount': 10,
                'reuse': False
            },
            "medium potion": {
                'id': 3,
                'name': 'medium potion',
                'type': 'heal',
                'amount': 20,
                'reuse': False
            },
            'large potion': {
                'id': 4,
                'name': 'large potion',
                'type': 'heal',
                'amount': 30,
                'reuse': False
            },
            'escape rope': {
                'id': 5,
                'name': 'escape rope',
                'type': 'utility',
                'reuse': False
            }
        }

        # player attributes
        self.name = name
        self.job = job

        self.is_alive = True

        # Stats
        self.hp = 40

        self.atk = 12
        self.res = 8
        self.spd = 11
        
        self.current_hp = 40

    def __str__(self):

        hp_length = 10
        healthbar = buildHPBar(self.current_hp, self.hp, hp_length)  # static length of 10
        total_length = hp_length + 5

        inner_txt = [
            f" {self.name.capitalize():{total_length-5}}    ",
            f" HP {healthbar} "
        ]

        txt = box(inner_txt, 'round', 'right')

        return txt

    def status_screen():
        ...

    def take_dmg(self, enemy_atk):
        total_dmg = enemy_atk - self.res

        self.current_hp -= total_dmg

        # check if current hp < 0
        if self.current_hp <= 0:
            self.is_alive = False
            return False, "You Died!"

        return True, f"Took {total_dmg} dmg!"

    def deal_dmg(self, enemy_res_amount):
        dmg_dealt = self.atk - enemy_res_amount
        return True, f"Dealt {dmg_dealt} dmg!"

    def heal(self, heal_amount):
        if self.current_hp == self.hp:
            return False, f"Healing Failed! Full HP\n"

        self.current_hp += heal_amount
        
        if self.current_hp > self.hp:
            result_txt = f"Healing Overload: {self.current_hp - self.hp} HP wasted...\n"
            self.current_hp = self.hp
            return False, result_txt
        return True, f"Healed {heal_amount}! Current Health -> {self.current_hp}"
    
    def battle_options(self, user_option, opponent):
        action_result = ""

        # Attack Option
        if user_option == 'a':
            action_result += "You Attack!"
            action_status, result = self.deal_dmg(opponent.res)
            action_result += f"\n{result}\n"

            opponent.take_dmg(self.atk)

            return action_status, action_result

        # Bag Option
        if user_option == 'b':
            # Display Bag
            clear_screen()
            print(self.bag)

            # Get input
            bag_input = input("\nChoose item: ")
            
            # Check input
            chosen_item = self.processed_item_db.get(bag_input, None)

            if chosen_item is None:
                return True, f"Invalid Item: {bag_input}\n"
            
            # Use Item if enough in inventory
            use_status, available_result = self.bag.use_item(bag_input)

            if use_status:
                action_result += f"{available_result}\n"
                # Actually use item/ perform action
                action_status, use_result = chosen_item.use(self)

                action_result += f"{use_result}\n"
            else:
                action_result += f"{available_result}\n"

            return action_status, action_result
        
        return False, ""


class Enemy:
    def __init__(self):
        self.name = "Enemy"
        self.is_alive = True

        # Stats
        self.hp = 30

        self.atk = 10
        self.res = 8
        self.spd = 10
        
        self.current_hp = 30


    def __str__(self):
        # len(healthbar) + 5
        # len(self.name) + 11

        hp_length = 10
        healthbar = buildHPBar(self.current_hp, self.hp, hp_length)  # static length of 10

        total_length = hp_length + 5

        inner_txt = [
            f" {self.name:{total_length-5}}    ",
            f" HP {healthbar} "
        ]

        txt = box(inner_txt, 'round')
        
        return txt
    
    def take_dmg(self, enemy_atk):
        total_dmg = enemy_atk - self.res

        self.current_hp -= total_dmg

        # check if current hp < 0
        if self.current_hp <= 0:
            self.is_alive = False
            return False, f"Enemy defeated!"
        return True, ""

    def heal(self, heal_amount):
        self.current_hp += heal_amount
        if self.current_hp > self.hp:
            self.current_hp = self.hp
            return False, f"Healing Failed! {self.current_hp - self.hp} HP wasted"
        result_txt = f"Healed {heal_amount}! Current Health -> {self.current_hp}"
        # return True, result_txt
        return True, result_txt