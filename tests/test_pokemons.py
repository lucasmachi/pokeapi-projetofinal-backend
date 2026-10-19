def payload(**overrides):
    data = {"pokedex_number": 25, "name": "Pikachu", "type_1": "Electric", "type_2": None, "hp": 35, "attack": 55, "defense": 40, "special_attack": 50, "special_defense": 50, "speed": 90, "generation": 1}
    data.update(overrides)
    return data

def test_root_and_health(client):
    assert client.get("/").status_code == 200
    assert client.get("/health").json()["status"] == "ok"

def test_create_and_get_pokemon(client):
    created = client.post("/pokemons", json=payload())
    assert created.status_code == 201
    pokemon_id = created.json()["id"]
    response = client.get(f"/pokemons/{pokemon_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Pikachu"

def test_list_and_filter(client):
    client.post("/pokemons", json=payload())
    client.post("/pokemons", json=payload(pokedex_number=1, name="Bulbasaur", type_1="Grass", type_2="Poison"))
    assert len(client.get("/pokemons").json()) == 2
    assert client.get("/pokemons", params={"name": "pika"}).json()[0]["name"] == "Pikachu"
    assert client.get("/pokemons", params={"type": "Grass"}).json()[0]["name"] == "Bulbasaur"

def test_duplicate_conflict(client):
    client.post("/pokemons", json=payload())
    response = client.post("/pokemons", json=payload(pokedex_number=26))
    assert response.status_code == 409

def test_update_pokemon(client):
    pokemon_id = client.post("/pokemons", json=payload()).json()["id"]
    response = client.put(f"/pokemons/{pokemon_id}", json={"name": "Raichu", "attack": 90})
    assert response.status_code == 200
    assert response.json()["name"] == "Raichu"
    assert response.json()["attack"] == 90

def test_delete_pokemon(client):
    pokemon_id = client.post("/pokemons", json=payload()).json()["id"]
    assert client.delete(f"/pokemons/{pokemon_id}").status_code == 204
    assert client.get(f"/pokemons/{pokemon_id}").status_code == 404

def test_missing_pokemon_returns_404(client):
    assert client.get("/pokemons/999").status_code == 404
    assert client.put("/pokemons/999", json={"name": "Missingno"}).status_code == 404
    assert client.delete("/pokemons/999").status_code == 404

def test_validation_rejects_invalid_data(client):
    assert client.post("/pokemons", json=payload(pokedex_number=0)).status_code == 422
    assert client.post("/pokemons", json=payload(hp=-1)).status_code == 422
