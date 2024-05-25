from geopy.distance import geodesic

class Coordenada:
    def __init__(self, latitud: float, longitud: float) -> None:
        self.latitud: float = latitud
        self.longitud: float = longitud
    
    def distancia(self, altre: "Coordenada") -> float:
        return geodesic((self.latitud, self.longitud), (altre.latitud, altre.longitud)).meters