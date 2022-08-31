import asyncio
from poke_env import PlayerConfiguration
from poke_env.player import RandomPlayer, Player
from poke_env import ServerConfiguration, environment
import time
import ty
import random

team = """
Zapdos @ Leftovers
Ability: Pressure
EVs: 252 SpA / 4 SpD / 252 Spe
Timid Nature
IVs: 0 Atk
- Discharge
- Heat Wave
- Hidden Power [Ice]
- Roost

Mew @ Leftovers
Ability: Synchronize
EVs: 240 HP / 56 Def / 8 SpA / 140 SpD / 64 Spe
Bold Nature
IVs: 0 Atk
- Stealth Rock
- Will-O-Wisp
- Soft-Boiled
- Psychic

Scizor-Mega (M) @ Scizorite
Ability: Light Metal
EVs: 248 HP / 120 Def / 124 SpD / 16 Spe
Impish Nature
- Bullet Punch
- U-turn
- Roost
- Defog

Garchomp (M) @ Choice Scarf
Ability: Rough Skin
EVs: 252 Atk / 4 SpD / 252 Spe
Jolly Nature
- Outrage
- Earthquake
- Toxic
- Dragon Claw

Amoonguss (F) @ Black Sludge
Ability: Regenerator
EVs: 248 HP / 44 Def / 216 SpD
Calm Nature
IVs: 0 Atk
- Spore
- Giga Drain
- Hidden Power [Fire]
- Toxic

Greninja-Ash @ Choice Specs
Ability: Battle Bond
EVs: 252 SpA / 4 SpD / 252 Spe
Timid Nature
- Water Shuriken
- Hydro Pump
- Dark Pulse
- Spikes
"""

# If your server is accessible at my.custom.host:5432, and your authentication
# endpoint is authentication-endpoint.com/action.php?
my_server_config= ServerConfiguration(
    "vibe.impassivedev.com:8000",
    "http://vibe.impassivedev.com.psim.us/action.php?"
)

# You can now use my_server_config with a Player object

class Mimic(Player):
    def choose_move(self, battle):

        opp = battle.opponent_active_pokemon
        types = []
        types.append(str(opp.type_1).split(" ")[0].capitalize())
        if opp.type_2:
            types.append(str(opp.type_2).split(" ")[0].capitalize())

        w = ty.get_weaknesses(types)['weaknesses']
        r = ty.get_weaknesses(types)['resistances']

        ww = []
        www = []
        rr = []
        for i in dict.keys(w):
            if w[i] == 2:
                ww.append(i.lower())
            if w[i] == 4:
                www.append(i.lower())
        for i in dict.keys(r):
            if r[i] == 0:
                rr.append(i.lower())

        if battle.available_moves:
            best_moves = []
            for i in battle.available_moves:
                print("XXXX")
                print(i)
                print("XXXX")
                ttype = str(i.type).split(" ")[0].lower()
                if len(www) != 0:
                    if ttype in www and i.base_power != 0:
                        best_moves.append(i)
                elif len(www) == 0 and len(ww) != 0:
                    if ttype in ww and i.base_power != 0:
                        best_moves.append(i)
            
            if len(best_moves) == 0:
                for i in battle.available_moves:
                    active = battle.active_pokemon
                    if str(active.type_1).split(" ")[0].lower() not in rr:
                        if i.base_power != 0 and str(i.type).split(" ")[0].lower() == str(active.type_1).split(" ")[0].lower():
                            return self.create_order(i)
                    elif i.base_power != 0 and str(i.type).split(" ")[0].lower() not in rr:
                        return self.create_order(i)
            if len(best_moves) == 1:
                return self.create_order(best_moves[0])
            elif len(best_moves) > 1:
                return self.create_order(random.choice(best_moves))
        else:
            return self.choose_random_move(battle)

        


async def main():
    player = Mimic(
        player_configuration=PlayerConfiguration("XXXXXX", "XXXXXX"),
        server_configuration=my_server_config, 
        battle_format='gen7ou',
        team=team
    )

    # Accepting one challenge from any user
    await player.accept_challenges(None, 2)



if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())