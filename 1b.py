import sys
import os
import json

from src.pokemon import PokemonFactory

if __name__ == "__main__":

  factory = PokemonFactory("pokemon.json")
  directory = os.fsencode(sys.argv[1])

  for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".json"):
      with open(filename, "r") as file_config:
        configs = json.load(file_config)
        for config in configs:
          ball = config["pokeball"]
          pokemon_name = config["pokemon"]
          pokemon = factory.create(pokemon_name, 100, StatusEffect.NONE, 1)
