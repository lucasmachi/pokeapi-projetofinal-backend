from sqlalchemy import CheckConstraint, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base

class Pokemon(Base):
    __tablename__ = "pokemons"
    __table_args__ = (
        CheckConstraint("pokedex_number > 0", name="ck_pokemon_pokedex_positive"),
        CheckConstraint("hp >= 0 AND attack >= 0 AND defense >= 0 AND special_attack >= 0 AND special_defense >= 0 AND speed >= 0", name="ck_pokemon_stats_nonnegative"),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    pokedex_number: Mapped[int] = mapped_column(Integer, unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(80), unique=True, index=True, nullable=False)
    type_1: Mapped[str] = mapped_column(String(30), nullable=False)
    type_2: Mapped[str | None] = mapped_column(String(30), nullable=True)
    hp: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    attack: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    defense: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    special_attack: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    special_defense: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    speed: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    generation: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
