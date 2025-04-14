from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/pokemon')
def get_pokemon():
    query = request.args.get('query', '').strip().lower()
    if not query:
        return jsonify({'error': 'No Pokémon name provided'}), 400

    url = f'https://pokeapi.co/api/v2/pokemon/{query}'
    response = requests.get(url)

    if response.status_code != 200:
        return jsonify({'error': 'Pokémon not found'}), 404

    return jsonify(response.json())

@app.route('/api/evolution')
def get_evolution_chain():
    query = request.args.get('query', '').strip().lower()
    if not query:
        return jsonify({'error': 'No Pokémon name provided'}), 400

    # Step 1: Get Pokémon species info
    species_url = f'https://pokeapi.co/api/v2/pokemon-species/{query}'
    species_response = requests.get(species_url)
    if species_response.status_code != 200:
        return jsonify({'error': 'Species info not found'}), 404

    species_data = species_response.json()
    evo_chain_url = species_data['evolution_chain']['url']

    # Step 2: Get evolution chain data
    evo_response = requests.get(evo_chain_url)
    if evo_response.status_code != 200:
        return jsonify({'error': 'Evolution chain not found'}), 404

    return jsonify(evo_response.json())

if __name__ == '__main__':
    app.run(debug=True)
