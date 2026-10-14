from dataclasses import dataclass, field


@dataclass
class Regista:
    id: str
    name: str
    film: set = field(default_factory=set)
    interpreti: set = field(default_factory=set)
    voti: int = 0

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return self.name