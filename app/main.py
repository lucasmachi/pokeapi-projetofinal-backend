import logging
from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy import or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from .database import Base, engine, get_db
from .models import Pokemon
from .schemas import PokemonCreate, PokemonRead, PokemonUpdate

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
logger = logging.getLogger("pokeapi")

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    logger.info("PokéAPI started")
    yield

app = FastAPI(title="PokéAPI - Backend Final", description="API REST para cadastrar, consultar, atualizar e excluir Pokémon.", version="1.0.0", lifespan=lifespan)

@app.get("/", tags=["Health"])
def root():
    return {"message": "Bem-vindo à PokéAPI", "docs": "/docs", "health": "/health"}

@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}

@app.post("/pokemons", response_model=PokemonRead, status_code=status.HTTP_201_CREATED, tags=["Pokémon"], summary="Cadastrar um Pokémon")
def create_pokemon(payload: PokemonCreate, db: Session = Depends(get_db)):
    pokemon = Pokemon(**payload.model_dump())
    db.add(pokemon)
    try:
        db.commit()
        db.refresh(pokemon)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="Já existe um Pokémon com esse nome ou número da Pokédex") from exc
    logger.info("Pokemon created id=%s", pokemon.id)
    return pokemon

@app.get("/pokemons", response_model=list[PokemonRead], tags=["Pokémon"], summary="Listar Pokémon")
def list_pokemons(offset: int = Query(default=0, ge=0), limit: int = Query(default=50, ge=1, le=200), name: str | None = Query(default=None, min_length=1), pokemon_type: str | None = Query(default=None, alias="type"), db: Session = Depends(get_db)):
    query = select(Pokemon)
    if name:
        query = query.where(Pokemon.name.ilike(f"%{name.strip()}%"))
    if pokemon_type:
        query = query.where(or_(Pokemon.type_1.ilike(pokemon_type.strip()), Pokemon.type_2.ilike(pokemon_type.strip())))
    return list(db.scalars(query.order_by(Pokemon.pokedex_number).offset(offset).limit(limit)).all())

@app.get("/pokemons/{pokemon_id}", response_model=PokemonRead, tags=["Pokémon"], summary="Buscar Pokémon por ID")
def get_pokemon(pokemon_id: int, db: Session = Depends(get_db)):
    pokemon = db.get(Pokemon, pokemon_id)
    if pokemon is None:
        raise HTTPException(status_code=404, detail="Pokémon não encontrado")
    return pokemon

@app.put("/pokemons/{pokemon_id}", response_model=PokemonRead, tags=["Pokémon"], summary="Atualizar um Pokémon")
def update_pokemon(pokemon_id: int, payload: PokemonUpdate, db: Session = Depends(get_db)):
    pokemon = db.get(Pokemon, pokemon_id)
    if pokemon is None:
        raise HTTPException(status_code=404, detail="Pokémon não encontrado")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(pokemon, field, value)
    try:
        db.commit()
        db.refresh(pokemon)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="Já existe um Pokémon com esse nome ou número da Pokédex") from exc
    return pokemon

@app.delete("/pokemons/{pokemon_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Pokémon"], summary="Excluir um Pokémon")
def delete_pokemon(pokemon_id: int, db: Session = Depends(get_db)):
    pokemon = db.get(Pokemon, pokemon_id)
    if pokemon is None:
        raise HTTPException(status_code=404, detail="Pokémon não encontrado")
    db.delete(pokemon)
    db.commit()
    logger.info("Pokemon deleted id=%s", pokemon_id)
