from domain.especialitat import Especialitat
from domain.coordenada import Coordenada

class Restaurant:
    def __init__(self, nom: str, carrer: str, especialitat: Especialitat, coordenades: Coordenada) -> None:
        self.nom: str = nom
        self.carrer: str = carrer
        self.especialitat: Especialitat = especialitat
        self.coordenades: Coordenada = coordenades