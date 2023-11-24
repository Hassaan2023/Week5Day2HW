from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return 'Welcome to the Pokemon App!'

@app.route('/pokemon', methods=['GET', 'POST'])
def pokemon():
    if request.method == 'POST':
        pokemon_name = request.form['pokemon_name']
        api_url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}'
        response = requests.get(api_url)

        if response.status_code == 200:
            pokemon_data = response.json()

            # Extracting additional properties
            name = pokemon_data['name']
            hp = next(stat['base_stat'] for stat in pokemon_data['stats'] if stat['stat']['name'] == 'hp')
            defense = next(stat['base_stat'] for stat in pokemon_data['stats'] if stat['stat']['name'] == 'defense')
            attack = next(stat['base_stat'] for stat in pokemon_data['stats'] if stat['stat']['name'] == 'attack')
            front_shiny = pokemon_data['sprites']['front_shiny']
            ability = pokemon_data['abilities'][0]['ability']['name']  # Choosing the first ability

            return render_template('pokemon_info.html', name=name, hp=hp, defense=defense, attack=attack,
                                   front_shiny=front_shiny, ability=ability)
        else:
            return f'Error: Unable to fetch information for {pokemon_name.capitalize()}'

    return render_template('pokemon_form.html')

if __name__ == '__main__':
    app.run(debug=True)

