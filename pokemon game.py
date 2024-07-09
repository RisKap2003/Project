import random
import time

type_effectiveness = {
    "Normal": {"Rock": 0.5, "Ghost": 0, "Steel": 0.5},
    "Fire": {"Fire": 0.5, "Water": 0.5, "Grass": 2, "Ice": 2, "Bug": 2, "Rock": 0.5, "Dragon": 0.5, "Steel": 2},
    "Water": {"Fire": 2, "Water": 0.5, "Grass": 0.5, "Ground": 2, "Rock": 2, "Dragon": 0.5},
    "Electric": {"Water": 2, "Electric": 0.5, "Grass": 0.5, "Ground": 0, "Flying": 2, "Dragon": 0.5},
    "Grass": {"Fire": 0.5, "Water": 2, "Grass": 0.5, "Poison": 0.5, "Ground": 2, "Flying": 0.5, "Bug": 0.5, "Rock": 2, "Dragon": 0.5, "Steel": 0.5},
    "Ice": {"Fire": 0.5, "Water": 0.5, "Grass": 2, "Ice": 0.5, "Ground": 2, "Flying": 2, "Dragon": 2, "Steel": 0.5},
    "Fighting": {"Normal": 2, "Ice": 2, "Poison": 0.5, "Flying": 0.5, "Psychic": 0.5, "Bug": 0.5, "Rock": 2, "Ghost": 0, "Dark": 2, "Steel": 2, "Fairy": 0.5},
    "Poison": {"Grass": 2, "Poison": 0.5, "Ground": 0.5, "Rock": 0.5, "Ghost": 0.5, "Steel": 0, "Fairy": 2},
    "Ground": {"Fire": 2, "Electric": 2, "Grass": 0.5, "Poison": 2, "Flying": 0, "Bug": 0.5, "Rock": 2, "Steel": 2},
    "Flying": {"Electric": 0.5, "Grass": 2, "Fighting": 2, "Bug": 2, "Rock": 0.5, "Steel": 0.5},
    "Psychic": {"Fighting": 2, "Poison": 2, "Psychic": 0.5, "Dark": 0, "Steel": 0.5},
    "Bug": {"Fire": 0.5, "Grass": 2, "Fighting": 0.5, "Poison": 0.5, "Flying": 0.5, "Psychic": 2, "Ghost": 0.5, "Dark": 2, "Steel": 0.5, "Fairy": 0.5},
    "Rock": {"Fire": 2, "Ice": 2, "Fighting": 0.5, "Ground": 0.5, "Flying": 2, "Bug": 2, "Steel": 0.5},
    "Ghost": {"Normal": 0, "Psychic": 2, "Ghost": 2, "Dark": 0.5},
    "Dragon": {"Dragon": 2, "Steel": 0.5, "Fairy": 0},
    "Dark": {"Fighting": 0.5, "Psychic": 2, "Ghost": 2, "Dark": 0.5, "Fairy": 0.5},
    "Steel": {"Fire": 0.5, "Water": 0.5, "Electric": 0.5, "Ice": 2, "Rock": 2, "Steel": 0.5, "Fairy": 2},
    "Fairy": {"Fire": 0.5, "Fighting": 2, "Poison": 0.5, "Dragon": 2, "Dark": 2, "Steel": 0.5}
}

class Pokemon:
    def __init__(self, name, ptype, health, attack, defence, special_attack, special_defence, speed, level, experience, moves, is_wild=True):
        self.name = name
        self.ptype = ptype
        self.max_health = health
        self.health = health
        self.attack = attack
        self.defence = defence
        self.special_attack = special_attack
        self.special_defence = special_defence
        self.speed = speed
        self.level = level
        self.experience = experience
        self.moves = moves
        self.move_cooldowns = {move.name: 0 for move in moves}
        self.defense_cooldown = 0
        self.is_wild = is_wild

    def attack_opponent(self, opponent, move):
        if move in self.moves and self.move_cooldowns[move.name] == 0:
            damage = self.calculate_damage(opponent, move)
            opponent.take_damage(damage)
            self.move_cooldowns[move.name] = move.cooldown
            print(f"{self.name} used {move.name} on {opponent.name}! It dealt {damage:.1f} damage.")
        else:
            print(f"{move.name} is still recharging.")
            return False
        return True

    def calculate_damage(self, opponent, move):
        type_multiplier = type_effectiveness.get(move.mtype, {}).get(opponent.ptype, 1)
        if move.category == 'physical':
            base_damage = ((2 * self.level / 5 + 2) * move.power * self.attack / opponent.defence / 50 + 2)
        elif move.category == 'special':
            base_damage = ((2 * self.level / 5 + 2) * move.power * self.special_attack / opponent.special_defence / 50 + 2)
        return base_damage * type_multiplier * random.uniform(0.85, 1.0)

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.faint()
        else:
            print(f"{self.name} now has {self.health:.1f} HP remaining.")

    def faint(self):
        print(f"{self.name} has fainted!")

    def gain_experience(self, exp):
        self.experience += exp
        print(f"{self.name} gained {exp} experience points!")
        if self.experience >= self.level * 10:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.max_health += 10
        self.health = self.max_health
        self.attack += 2
        self.defence += 2
        self.special_attack += 2
        self.special_defence += 2
        self.speed += 1
        print(f"{self.name} leveled up to level {self.level}!")

    def learn_move(self, move):
        if len(self.moves) < 4:
            self.moves.append(move)
            self.move_cooldowns[move.name] = 0
            print(f"{self.name} learned {move.name}!")
        else:
            print(f"{self.name} already knows 4 moves. Forget a move to learn {move.name}.")

    def recharge_moves(self):
        for move in self.moves:
            if self.move_cooldowns[move.name] > 0:
                self.move_cooldowns[move.name] -= 1
        if self.defense_cooldown > 0:
            self.defense_cooldown -= 1

    def get_stat(self, stat):
        return getattr(self, stat, None)

    def display_stats(self):
        strengths = [t for t, effect in type_effectiveness.get(self.ptype, {}).items() if effect > 1]
        weaknesses = [t for t, effect in type_effectiveness.get(self.ptype, {}).items() if effect < 1 and effect > 0]
        strengths_str = ', '.join(strengths) if strengths else "None"
        weaknesses_str = ', '.join(weaknesses) if weaknesses else "None"
        return f"- Type: {self.ptype}\n- Strengths: {strengths_str}\n- Weaknesses: {weaknesses_str}\n"


class Move:
    def __init__(self, name, mtype, power, accuracy, category, cooldown, effect=None):
        self.name = name
        self.mtype = mtype
        self.power = power
        self.accuracy = accuracy
        self.category = category
        self.cooldown = cooldown
        self.effect = effect

    def apply_effect(self, target):
        if self.effect:
            self.effect(target)
            print(f"{self.name} applied its effect on {target.name}.")

class Trainer:
    def __init__(self, name, team, inventory):
        self.name = name
        self.team = team
        self.inventory = inventory

    def catch_pokemon(self, wild_pokemon):
        pokeball = next((item for item in self.inventory if item.itype == 'pokeball'), None)
        if pokeball:
            success = pokeball.use(wild_pokemon)
            if success:
                self.team.append(wild_pokemon)
                print(f"{self.name} caught {wild_pokemon.name}!")
            else:
                print(f"{wild_pokemon.name} escaped!")
        else:
            print("No Pokeballs left!")

    def use_item(self, item, target):
        if item in self.inventory:
            item.use(target)
            self.inventory.remove(item)
            print(f"{self.name} used {item.name} on {target.name}.")

    def battle(self, opponent):
        print(f"{self.name} is battling {opponent.name}!")
        player_active_pokemon = self.choose_pokemon()
        opponent_active_pokemon = opponent.team[0]
        while any(p.health > 0 for p in self.team) and any(p.health > 0 for p in opponent.team):
            print(f"\n{self.name}'s {player_active_pokemon.name}: {player_active_pokemon.health:.1f} HP")
            print(f"{opponent.name}'s {opponent_active_pokemon.name}: {opponent_active_pokemon.health:.1f} HP")

            player_action = self.get_valid_input("Choose action: [1] Attack [2] Switch [3] Use Item [4] Defend [5] Surrender: ", ["1", "2", "3", "4", "5"])
            if player_action == "1":
                while True:
                    move = self.choose_move(player_active_pokemon)
                    if player_active_pokemon.attack_opponent(opponent_active_pokemon, move):
                        break
                    print("Move is recharging. Choose another move.")
                time.sleep(3)
                if opponent_active_pokemon.health <= 0:
                    print(f"{opponent_active_pokemon.name} fainted!")
                    if all(p.health <= 0 for p in opponent.team):
                        print(f"{self.name} won the battle!")
                        return
                    opponent_active_pokemon = next(p for p in opponent.team if p.health > 0)
            elif player_action == "2":
                player_active_pokemon = self.choose_pokemon()
            elif player_action == "3":
                item = self.choose_item()
                self.use_item(item, player_active_pokemon)
                time.sleep(3)
            elif player_action == "4":
                if player_active_pokemon.defense_cooldown == 0:
                    player_active_pokemon.defence += 20
                    player_active_pokemon.defense_cooldown = 2
                    print(f"{player_active_pokemon.name} is defending! Defense increased by 20.")
                else:
                    print(f"{player_active_pokemon.name} is still recovering from the last defense.")
                time.sleep(3)
            elif player_action == "5":
                print(f"{self.name} surrendered!")
                return

            if opponent_active_pokemon.health > 0:
                opponent_move = random.choice(opponent_active_pokemon.moves)
                opponent_active_pokemon.attack_opponent(player_active_pokemon, opponent_move)
                time.sleep(3)
                if player_active_pokemon.health <= 0:
                    print(f"{player_active_pokemon.name} fainted!")
                    if all(p.health <= 0 for p in self.team):
                        print(f"{opponent.name} won the battle!")
                        return
                    player_active_pokemon = self.choose_pokemon()

            player_active_pokemon.recharge_moves()
            opponent_active_pokemon.recharge_moves()

    def choose_pokemon(self):
        while True:
            print("Choose your Pokémon:")
            for i, pokemon in enumerate(self.team):
                print(f"{i + 1}. {pokemon.name} (HP: {pokemon.health:.1f})")
            choice = input("Enter the number of the Pokémon: ")
            if choice.isdigit() and 1 <= int(choice) <= len(self.team):
                return self.team[int(choice) - 1]
            print("Invalid choice. Please enter a valid number.")

    def choose_move(self, pokemon):
        while True:
            print(f"Choose a move for {pokemon.name}:")
            for i, move in enumerate(pokemon.moves):
                print(f"{i + 1}. {move.name} (Type: {move.mtype}, Power: {move.power}, Accuracy: {move.accuracy}, Cooldown: {pokemon.move_cooldowns[move.name]})")
            choice = input("Enter the number of the move: ")
            if choice.isdigit() and 1 <= int(choice) <= len(pokemon.moves):
                return pokemon.moves[int(choice) - 1]
            print("Invalid choice. Please enter a valid number.")

    def choose_item(self):
        while True:
            print("Choose an item:")
            for i, item in enumerate(self.inventory):
                print(f"{i + 1}. {item.name}")
            choice = input("Enter the number of the item: ")
            if choice.isdigit() and 1 <= int(choice) <= len(self.inventory):
                return self.inventory[int(choice) - 1]
            print("Invalid choice. Please enter a valid number.")

    def get_valid_input(self, prompt, valid_options):
        while True:
            choice = input(prompt)
            if choice in valid_options:
                return choice
            print("Invalid choice. Please enter a valid option.")

class Item:
    def __init__(self, name, itype, effect):
        self.name = name
        self.itype = itype
        self.effect = effect

    def use(self, target):
        self.effect(target)
        print(f"{self.name} applied its effect on {target.name}.")

# Example usage with user input:
def main():
    tackle = Move(name="Tackle", mtype="Normal", power=40, accuracy=100, category="physical", cooldown=1)
    ember = Move(name="Ember", mtype="Fire", power=40, accuracy=100, category="special", cooldown=1)
    vine_whip = Move(name="Vine Whip", mtype="Grass", power=45, accuracy=100, category="physical", cooldown=1)
    water_gun = Move(name="Water Gun", mtype="Water", power=40, accuracy=100, category="special", cooldown=1)
    thunder_shock = Move(name="Thunder Shock", mtype="Electric", power=40, accuracy=100, category="special", cooldown=1)
    gust = Move(name="Gust", mtype="Flying", power=40, accuracy=100, category="special", cooldown=1)
    rock_throw = Move(name="Rock Throw", mtype="Rock", power=50, accuracy=90, category="physical", cooldown=2)
    psychic = Move(name="Psychic", mtype="Psychic", power=90, accuracy=100, category="special", cooldown=3)
    bite = Move(name="Bite", mtype="Dark", power=60, accuracy=100, category="physical", cooldown=2)
    flamethrower = Move(name="Flamethrower", mtype="Fire", power=90, accuracy=100, category="special", cooldown=3)
    hydro_pump = Move(name="Hydro Pump", mtype="Water", power=110, accuracy=80, category="special", cooldown=3)
    solar_beam = Move(name="Solar Beam", mtype="Grass", power=120, accuracy=100, category="special", cooldown=4)
    thunderbolt = Move(name="Thunderbolt", mtype="Electric", power=90, accuracy=100, category="special", cooldown=3)
    air_slash = Move(name="Air Slash", mtype="Flying", power=75, accuracy=95, category="special", cooldown=2)

    bulbasaur = Pokemon(name="Bulbasaur", ptype="Grass", health=100, attack=49, defence=49, special_attack=65, special_defence=65, speed=45, level=5, experience=0, moves=[tackle, vine_whip, solar_beam])
    charmander = Pokemon(name="Charmander", ptype="Fire", health=100, attack=52, defence=43, special_attack=60, special_defence=50, speed=65, level=5, experience=0, moves=[tackle, ember, flamethrower])
    squirtle = Pokemon(name="Squirtle", ptype="Water", health=100, attack=48, defence=65, special_attack=50, special_defence=64, speed=43, level=5, experience=0, moves=[tackle, water_gun, hydro_pump])
    pikachu = Pokemon(name="Pikachu", ptype="Electric", health=100, attack=55, defence=40, special_attack=50, special_defence=50, speed=90, level=5, experience=0, moves=[tackle, thunder_shock, thunderbolt])
    pidgey = Pokemon(name="Pidgey", ptype="Flying", health=100, attack=45, defence=40, special_attack=35, special_defence=35, speed=56, level=5, experience=0, moves=[tackle, gust, air_slash])
    geodude = Pokemon(name="Geodude", ptype="Rock", health=100, attack=80, defence=100, special_attack=30, special_defence=30, speed=20, level=5, experience=0, moves=[tackle, rock_throw])
    onix = Pokemon(name="Onix", ptype="Rock", health=100, attack=45, defence=160, special_attack=30, special_defence=45, speed=70, level=5, experience=0, moves=[tackle, rock_throw])
    psyduck = Pokemon(name="Psyduck", ptype="Water", health=100, attack=52, defence=48, special_attack=65, special_defence=50, speed=55, level=5, experience=0, moves=[tackle, water_gun, hydro_pump])
    growlithe = Pokemon(name="Growlithe", ptype="Fire", health=100, attack=70, defence=45, special_attack=70, special_defence=50, speed=60, level=5, experience=0, moves=[tackle, ember, flamethrower, bite])
    abra = Pokemon(name="Abra", ptype="Psychic", health=100, attack=20, defence=15, special_attack=105, special_defence=55, speed=90, level=5, experience=0, moves=[tackle, psychic])

    pokeball = Item(name="Pokeball", itype="pokeball", effect=lambda target: random.random() < 0.5)
    potion = Item(name="Potion", itype="potion", effect=lambda target: setattr(target, 'health', min(target.max_health, target.health + 20)))
    super_potion = Item(name="Super Potion", itype="potion", effect=lambda target: setattr(target, 'health', min(target.max_health, target.health + 50)))

    trainers = {
        "Ash": Trainer(name="Ash", team=[bulbasaur, pikachu], inventory=[pokeball, potion, super_potion]),
        "Misty": Trainer(name="Misty", team=[squirtle, psyduck], inventory=[potion, super_potion]),
        "Brock": Trainer(name="Brock", team=[geodude, onix], inventory=[potion, super_potion]),
        "Gary": Trainer(name="Gary", team=[charmander, pidgey], inventory=[potion, super_potion]),
        "Jessie": Trainer(name="Jessie", team=[abra], inventory=[potion, super_potion])
    }

    print("Available Trainers:")
    for idx, (trainer_name, trainer) in enumerate(trainers.items(), 1):
        print(f"{idx}. {trainer_name}:")
        for pokemon in trainer.team:
            print(f"  * {pokemon.name} (HP: {pokemon.health:.1f})\n    {pokemon.display_stats()}")
    player_name = input("Choose your Trainer: ")

    while player_name not in trainers:
        player_name = input("Invalid choice. Choose your Trainer: ")

    player = trainers[player_name]

    print("\nAvailable Opponents:")
    for idx, (trainer_name, trainer) in enumerate(trainers.items(), 1):
        if trainer_name != player_name:
            print(f"{idx}. {trainer_name}:")
            for pokemon in trainer.team:
                print(f"  * {pokemon.name} (HP: {pokemon.health:.1f})\n    {pokemon.display_stats()}")
    opponent_name = input("Choose your Opponent: ")

    while opponent_name not in trainers or opponent_name == player_name:
        opponent_name = input("Invalid choice. Choose your Opponent: ")

    opponent = trainers[opponent_name]

    print("\nYour Pokémon:")
    for pokemon_name in [p.name for p in player.team]:
        print(pokemon_name)
    print("\nOpponent's Pokémon:")
    for pokemon_name in [p.name for p in opponent.team]:
        print(pokemon_name)

    player.battle(opponent)

if __name__ == "__main__":
    main()
