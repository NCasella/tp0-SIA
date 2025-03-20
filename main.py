import json
import sys
import numpy as np
import csv
import os

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

    pokemon_status = StatusEffect if varying_status else [StatusEffect.NONE]

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

            for lvl_step in range(lvl_steps):
                current_lvl = lvl - (lvl_step * lvl_step_size)
                if (not current_lvl in capture_rate_by_pokemon[pokemon_name]):
                    capture_rate_by_pokemon[pokemon_name][current_lvl] = {}
                for current_status in pokemon_status:
                    if (not current_status in capture_rate_by_pokemon[pokemon_name][current_lvl]):
                        capture_rate_by_pokemon[pokemon_name][current_lvl][current_status] = {}
                    for hp_step in range(hp_steps):
                        current_hp = hp_percentage - (hp_step * hp_step_size)
                        if (not current_hp in capture_rate_by_pokemon[pokemon_name][current_lvl][current_status]):
                            capture_rate_by_pokemon[pokemon_name][current_lvl][current_status][current_hp] = {}
                        pokemon = factory.create(pokemon_name, current_lvl, current_status, current_hp)
                        count = 0
                        for _ in range(attempts):
                            ac = attempt_catch(pokemon, ball, noise)
                            count += ac[0]
                        capture_rate_by_pokemon[pokemon_name][current_lvl][current_status][current_hp][ball] = count / attempts
    f.close()
    # export the date
    # {pokemon, {hp, {ball, rate}}}
    os.makedirs("output", exist_ok=True)
    for pokemon, lvl_status_hp_ball in capture_rate_by_pokemon.items():
        with open(f"output/{pokemon}{"_" if varying_level or varying_status or varying_hp else ""}{"l" if varying_level else ""}{"s" if varying_status else ""}{"h" if varying_hp else ""}.csv", "w") as csv:
            any_lvl = next(iter(lvl_status_hp_ball))
            any_status = next(iter(lvl_status_hp_ball[any_lvl]))
            any_hp = next(iter(lvl_status_hp_ball[any_lvl][any_status]))
            header = f"{"level;" if varying_level else ""}{"status;" if varying_status else ""}{"hp;" if varying_hp else ""}{";".join(lvl_status_hp_ball[any_lvl][any_status][any_hp].keys())}"
            csv.write(f"{header}\n")
            for level, status_hp_ball in lvl_status_hp_ball.items():
                for status, values_by_ball in status_hp_ball.items():
                    for hp, values_by_ball in values_by_ball.items():
                        rates = ";".join(list(map(lambda x: f"{x:.4f}", values_by_ball.values())))
                        csv.write(f"{f"{level:.0f};" if varying_level else ""}{f"{str(status).removeprefix(f"{StatusEffect.__name__}.")};" if varying_status else ""}{f"{hp:.4f};" if varying_hp else ""}{rates}\n")
        csv.close()
