import heapq
from typing import List, Optional, Tuple

class Coordenades:
    def __init__(self, latitud: float, longitud: float):
        self.latitud = latitud
        self.longitud = longitud

    def distancia(self, other: 'Coordenades') -> float:
        # Assuming Euclidean distance for simplicity
        return ((self.latitud - other.latitud) ** 2 + (self.longitud - other.longitud) ** 2) ** 0.5

class Especialitat:
    def __init__(self, especialitat: str, pes: float):
        self.especialitat = especialitat
        self.pes = pes

    def __eq__(self, other: 'Especialitat'):
        return self.especialitat == other.especialitat

class Comanda:
    def __init__(self, id: int, especialitat: Especialitat):
        self.id = id
        self.especialitat = especialitat

class Restaurant:
    def __init__(self, nom: str, especialitat: Especialitat, coordenades: Coordenades):
        self.nom = nom
        self.especialitat = especialitat
        self.coordenades = coordenades

def best_first_search(start: Coordenades, restaurants: List[Restaurant], comanda: Comanda) -> Tuple[float, Restaurant]:
    priority_queue: List[Tuple[float, Restaurant]] = []
    restaurant: Optional[Restaurant] = None
    # Initialize the priority queue with restaurants that match the specialty of the comanda
    for r in restaurants:
        if r.especialitat == comanda.especialitat:
            distance = start.distancia(r.coordenades)
            heapq.heappush(priority_queue, (distance, r))

    return heapq.heappop(priority_queue)

# Simulating the function call
ubicacioActual = Coordenades(0.0, 0.0)  # Example start location
especialitats = [Especialitat("pizza", 1.0), Especialitat("sushi", 0.5), Especialitat("burger", 1.5)]  # Example specialties
comandesProgramades = [Comanda(1, especialitats[0]), Comanda(2, especialitats[1])]  # Example orders
restaurants = [
    Restaurant("Pizza Place", especialitats[0], Coordenades(2.0, 2.0)),
    Restaurant("Pizza Hut", especialitats[0], Coordenades(2.0, 3.0)),
    Restaurant("Pizza Planet", especialitats[0], Coordenades(1.0, 2.0)),
    Restaurant("Sushi Spot", especialitats[1], Coordenades(2.0, 2.0)),
    Restaurant("Burger Joint", especialitats[2], Coordenades(3.0, 3.0))
]  # Example restaurants
motxilla = []
capacitatActual = 0
distanciaRecorreguda = 0
ruta = []
repetirRestaurants = False  # Adjust based on your needs

print()
while len(comandesProgramades) > 0:
    comanda = comandesProgramades.pop(0)
    _, restaurant = best_first_search(ubicacioActual, restaurants, comanda)

    if restaurant is not None:
        distanciaMinima = ubicacioActual.distancia(restaurant.coordenades)
        print(f"Anem al restaurant {restaurant.nom} ({restaurant.especialitat.especialitat}) que està a {round(distanciaMinima, 2)} metres a les coordenades ({restaurant.coordenades.latitud}, {restaurant.coordenades.longitud}) a per la comanda {comanda.id} ({comanda.especialitat.especialitat}).")

        motxilla.append(comanda)
        capacitatActual += restaurant.especialitat.pes
        ubicacioActual = restaurant.coordenades
        distanciaRecorreguda += distanciaMinima
        ruta.append(ubicacioActual)

        if not repetirRestaurants:
            restaurants.remove(restaurant)
    else:
        print(f"No hi ha cap restaurant que ofereixi la especialitat {comanda.especialitat.especialitat} a prop de la ubicació actual.")
        raise Exception(f"No hi ha cap restaurant que ofereixi la especialitat {comanda.especialitat.especialitat} a prop de la ubicació actual.")

print("Ruta completa:", ruta)
print("Distància total recorreguda:", distanciaRecorreguda)
print("Comandes en motxilla:", [comanda.id for comanda in motxilla])
print()