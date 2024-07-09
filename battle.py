import aiohttp
import asyncio
import random

pokemon_list = [
    'pikachu', 'bulbasaur', 'charmander', 'squirtle',
    'jigglypuff', 'meowth', 'psyduck', 'machop',
    'growlithe', 'poliwag'
]

async def fetch_pokemon(session, name):
    url = f'https://pokeapi.co/api/v2/pokemon/{name}'
    async with session.get(url) as response:
        data = await response.json()
        return {
            'name': name,
            'attack': next(stat['base_stat'] for stat in data['stats'] if stat['stat']['name'] == 'attack'),
            'defense': next(stat['base_stat'] for stat in data['stats'] if stat['stat']['name'] == 'defense'),
            'speed': next(stat['base_stat'] for stat in data['stats'] if stat['stat']['name'] == 'speed')
        }

async def get_pokemon_data():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_pokemon(session, name) for name in pokemon_list]
        return await asyncio.gather(*tasks)

def calculate_strength(pokemon):
    return pokemon['attack'] + pokemon['defense'] + pokemon['speed']

def simulate_battle(pokemon1, pokemon2):
    strength1 = calculate_strength(pokemon1)
    strength2 = calculate_strength(pokemon2)

    print(f"Битва между {pokemon1['name'].capitalize()} и {pokemon2['name'].capitalize()}")
    print(f"{pokemon1['name'].capitalize()} - Атака: {pokemon1['attack']}, Защита: {pokemon1['defense']}, Скорость: {pokemon1['speed']}")
    print(f"{pokemon2['name'].capitalize()} - Атака: {pokemon2['attack']}, Защита: {pokemon2['defense']}, Скорость: {pokemon2['speed']}")
    print(f"Сила: {pokemon1['name'].capitalize()} ({strength1}) vs {pokemon2['name'].capitalize()} ({strength2})")

    if strength1 > strength2:
        print(f"{pokemon1['name'].capitalize()} побеждает!")
    elif strength2 > strength1:
        print(f"{pokemon2['name'].capitalize()} побеждает!")
    else:
        print("Ничья!")

async def main():
    pokemon_data = await get_pokemon_data()

    pokemon1, pokemon2 = random.sample(pokemon_data, 2)

    simulate_battle(pokemon1, pokemon2)

asyncio.run(main())
