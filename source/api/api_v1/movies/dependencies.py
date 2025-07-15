from faker import Faker
from .schemas import Movie

fake_gen = Faker()

MOVIES_LIST = [
    Movie(
        movie_id=movie_id,
        name=fake_gen.sentence(nb_words=3).replace(".", ""),
        description=fake_gen.paragraph()
    ) for movie_id in range(1, 11)
]


def prefetch_movie_data(movie_id: int):
    movie: Movie | None = next((m for m in MOVIES_LIST if m.movie_id == movie_id))
    return movie


if __name__ == "__main__":
    print(MOVIES_LIST)

