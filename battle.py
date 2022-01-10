import os
import time

from utility import clear_screen


class Battle:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy

    def __str__(self) -> str:
        txt = ""
        return txt

    def run(self):
        cols, rows = os.get_terminal_size()

        enemy_first = False

        if self.player.spd < self.enemy.spd:
            enemy_first = True

        turn_summary = f"""[a] Attack Enemy
[b] Bag / Inventory"""
        break_flag = False
        while True:
            if enemy_first:
                # Enemy Turn
                turn_summary += "Enemy Attacked:"
                turn_stat, turn_result = self.player.take_dmg(self.enemy.atk)
                turn_summary += f"\n{turn_result}\n\n"

                # Check if they alive, can maybe use turn stat instead
                '''
                if not turn_stat:
                    if turn_status == 'dead':
                        print("Character Lost!)
                '''
            if not self.enemy.is_alive:
                # print("Hero won")
                # break
                turn_summary = "Hero Won"
                break_flag = True

            if not self.player.is_alive:
                # print("You have been DEFEATED.")
                # break
                turn_summary = "You have been DEFEATED."
                break_flag = True            

            # Display Current Status
            clear_screen()
            print(self.enemy)
            print(self.player)
            print(f"{'-'*cols}")
            # print(turn_summary)
            for line in turn_summary.split('\n'):
                # time.sleep(.25)
                print(line)
            print(f"{'-'*cols}")
            if break_flag:
                input("> ")
                break
            # Wait for user input
            user_input = input(f">>> ")
            
            # reset turn summary
            turn_summary = ""

            # Exit condition
            if user_input.lower() == 'q':
                break
            
            # player turn
            pturn_stat, pturn_result = self.player.battle_options(user_input, self.enemy)

            if pturn_stat:
                turn_summary += f"{pturn_result}\n"
            else:
                turn_summary += f"{pturn_result}"

            # # check if alive
            # if not self.enemy.is_alive:
            #     print("Hero won")
            #     break

            # if not self.player.is_alive:
            #     print("You have been DEFEATED.")
            #     break

            if not enemy_first:
                # Enemy Turn
                turn_summary += "Enemy Attacked!"
                pturn_stat, pturn_result = self.player.take_dmg(self.enemy.atk)

                turn_summary += f"\n{pturn_result}"
            
                # if not self.enemy.is_alive:
                #     print("Hero won")
                #     break

                # if not self.player.is_alive:
                #     print("You have been DEFEATED.")
                #     break

