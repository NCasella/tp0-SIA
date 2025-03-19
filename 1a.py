import json
import sys
import numpy as np

from src.catching import attempt_catch
from src.pokemon import PokemonFactory, StatusEffect
import matplotlib.pyplot as plt

if __name__ == "__main__":
    results = {}
    factory = PokemonFactory("pokemon.json")

    with open(f"{sys.argv[1]}", "r") as f:

        configs = json.load(f)

        for config in configs:
            ball = config["pokeball"]

            pokemon = factory.create(config["pokemon"], 100, StatusEffect.NONE, 1)

            count = 0
            results[ball]=[]
            for _ in range(100):
                ac = attempt_catch(pokemon, ball, 0)
                results[ball].append(ac)


            print(f"Catch rate for pokeball {ball}: ", count/100)

    categories=[pokeball for pokeball in results]
    values=list(results.values())

    plt.bar(categories,values)
    plt.ylim(top=100)
    plt.title(config["pokemon"])
    plt.xlabel("Pokeball type")
    plt.ylabel("Success percentage")


    np.std()

    file_name=sys.argv[1].removeprefix("configs/").removesuffix(".json")
    plt.savefig(f"1a_{file_name}.png")
