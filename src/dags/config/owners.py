from collections import namedtuple


DagOwner = namedtuple("DagOwner", ["name", "email"])


owner = DagOwner(
    name="Desanti", email=["desanti@example.com.br"]
)
