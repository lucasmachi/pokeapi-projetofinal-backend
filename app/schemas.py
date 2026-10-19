from pydantic import BaseModel, ConfigDict, Field, StringConstraints
from typing import Annotated

PokemonName = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=80)]
PokemonType = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=30)]

class PokemonBase(BaseModel):
    pokedex_number: int = Field(gt=0, examples=[25])
    name: PokemonName = Field(examples=["Pikachu"])
    type_1: PokemonType = Field(examples=["Electric"])
    type_2: PokemonType | None = Field(default=None, examples=[None])
    hp: int = Field(default=0, ge=0, le=999)
    attack: int = Field(default=0, ge=0, le=999)
    defense: int = Field(default=0, ge=0, le=999)
    special_attack: int = Field(default=0, ge=0, le=999)
    special_defense: int = Field(default=0, ge=0, le=999)
    speed: int = Field(default=0, ge=0, le=999)
    generation: int = Field(default=1, ge=1, le=9)

class PokemonCreate(PokemonBase):
    pass

class PokemonUpdate(BaseModel):
    pokedex_number: int | None = Field(default=None, gt=0)
    name: PokemonName | None = None
    type_1: PokemonType | None = None
    type_2: PokemonType | None = None
    hp: int | None = Field(default=None, ge=0, le=999)
    attack: int | None = Field(default=None, ge=0, le=999)
    defense: int | None = Field(default=None, ge=0, le=999)
    special_attack: int | None = Field(default=None, ge=0, le=999)
    special_defense: int | None = Field(default=None, ge=0, le=999)
    speed: int | None = Field(default=None, ge=0, le=999)
    generation: int | None = Field(default=None, ge=1, le=9)

class PokemonRead(PokemonBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
