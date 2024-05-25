from domain.especialitat import Especialitat
from domain.coordenada import Coordenada

class Comanda:
    def __init__(self, id: int, especialitat: Especialitat, carrer: str, coordenades: Coordenada) -> None:
        self.id: int = id
        self.especialitat: Especialitat = especialitat
        self.carrer: str = carrer
        self.coordenades: Coordenada = coordenades