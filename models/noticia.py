from dataclasses import asdict, dataclass


@dataclass
class Noticia:
    titulo: str
    data: str
    ano: str
    link: str
    resumo: str
    origem: str

    def to_dict(self) -> dict:
        return asdict(self)
