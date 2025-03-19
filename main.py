import json
import sys
import numpy as np
import csv

from src.catching import attempt_catch
from src.pokemon import PokemonFactory, StatusEffect

if __name__ == "__main__":
    factory = PokemonFactory("pokemon.json")

    with open("config.json", "r") as config_file:
        config = json.load(config_file)

    # constant values
    attempts: int = config["attempts"]
    noise: float = config["noise"]

    # varying parameters
    varying_level: bool = config["varying_level"]
    varying_hp: bool = config["varying_hp"]
    varying_status: bool = config["varying_status"]


    lvl: int = config["lvl"]
    lvl_steps: int = config["lvl_steps"] if varying_level else 1

    hp_percentage: float = config["hp_percentage"]
    hp_steps: int = config["hp_steps"] if varying_hp else 1

    hp_step_size = hp_percentage / hp_steps if varying_hp else 0
    lvl_step_size = lvl / lvl_steps if varying_level else 0

    config_file.close()

    # process the data
    with open(f"{sys.argv[1]}", "r") as f:

        configs = json.load(f)
        capture_rate_by_pokemon = {}

        for config in configs:

            ball = config["pokeball"]
            pokemon_name = config["pokemon"].removeprefix("configs/").removesuffix(".json")
            if (not pokemon_name in capture_rate_by_pokemon):
                capture_rate_by_pokemon[pokemon_name] = {}

            for hp_step in range(hp_steps):
                for lvl_step in range(lvl_steps):
                    current_hp = hp_percentage - (hp_step * hp_step_size)
                    current_lvl = lvl - (lvl_step * lvl_step_size)
                    pokemon = factory.create(pokemon_name, current_lvl, StatusEffect.NONE, current_hp)
                    if (not current_hp in capture_rate_by_pokemon[pokemon_name]):
                        capture_rate_by_pokemon[pokemon_name][current_hp] = {}
                    count = 0
                    for _ in range(attempts):
                        ac = attempt_catch(pokemon, ball, 0.15)
                        count += ac[0]
                    capture_rate_by_pokemon[pokemon_name][current_hp][ball] = count / attempts
    f.close()
    # export the date
    # {pokemon, {hp, {ball, rate}}}
    for pokemon, ball_by_hp in capture_rate_by_pokemon.items():
        with open(f"{pokemon}.csv", "w") as csv:
            any_hp = next(iter(ball_by_hp))
            ball_names = ball_by_hp[any_hp].keys()
            ball_names_joined=";".join(ball_names)
            csv.write(f"hp;{ball_names_joined}\n")
            for hp, values_by_ball in ball_by_hp.items():
                rates = values_by_ball.values()
                rates_joined=";".join(list(map(lambda x: f"{x:.4f}",rates)))
                csv.write(f"{hp:.4f};{rates_joined}\n")
        csv.close()
