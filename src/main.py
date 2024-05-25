from typing import List, Optional, Tuple
import argparse, os

from domain.coordenada import Coordenada
from domain.comanda import Comanda
from domain.restaurant import Restaurant
from domain.mapGenerator import MapGenerator
from data.data import comandes, restaurants, especialitats, tecnocampus

def omplirMotxilla(inici: Coordenada, comandes: List[Comanda], capacitatMaxima: int, restaurants: List[Restaurant], repetirRestaurants: bool) -> Tuple[List[Comanda], float, Coordenada, List[Comanda], List[Restaurant], List[Coordenada]]:
    """
    Funció que simula l'ompliment d'una motxilla amb comandes recollides en restaurants.

    Heurística per determinar les comandes:
        La funció ordena la llista de comandes en funció del temps de compromís de cada comanda.
        S'assegura que la comanda amb el temps de compromís més alt sigui processada primer.
        Això ajuda a prioritzar les comandes urgents i garanteix que es lliurin a temps.
        El temps de compromís ve determinat per l'especialitat de la comanda. Cada especialitat té un temps de compromís diferent.
    
    Heurística per determinar els restaurants:
        La funció selecciona el restaurant més proper a la ubicació actual i que ofereixi l'especialitat amb el temps de compromís més alt.
        Itera pels restaurants disponibles i calcula la distància entre la ubicació actual i cada restaurant.
        Se selecciona el restaurant amb la distància més curta i que coincideixi amb l'especialitat.
        Si l'opció de repetir restaurants està desactivada, el restaurant seleccionat s'elimina de la llista de restaurants disponibles.
    
    Args:
        inici (Coordenada): Coordenada inicial de la ubicació actual.
        comandes (List[Comanda]): Llista de comandes a lliurar.
        capacitatMaxima (int): Capacitat màxima de la motxilla.
        restaurants (List[Restaurant]): Llista de restaurants disponibles.
        repetirRestaurants (bool): Indica si es poden repetir els restaurants visitats.
    
    Returns:
        Tuple[List[Restaurant], float, Coordenada, List[Comanda], List[Restaurant]]: 
            - Llista de restaurants a la motxilla.
            - Distància total recorreguda.
            - Coordenada final de la ubicació actual.
            - Llista de comandes no lliurades.
            - Llista de restaurants restants.
            - Llista de coordenades de la ruta.
    """
    
    ubicacioActual: Coordenada = inici
    motxilla: List[Comanda] = []
    capacitatActual: int = 0
    distanciaRecorreguda: float = 0
    ruta: List[Coordenada] = [ubicacioActual]

    comandes = sorted(comandes, key=lambda comanda: comanda.especialitat.compromis)

    while len(comandes) > 0 and capacitatActual+comandes[0].especialitat.pes <= capacitatMaxima:
        comanda: Comanda = comandes.pop(0)
        restaurant: Optional[Restaurant] = None
        distanciaMinima: float = float("inf")

        for r in restaurants:
            if r.especialitat == comanda.especialitat:
                distancia: float = ubicacioActual.distancia(r.coordenades)
                if distancia < distanciaMinima:
                    distanciaMinima = distancia
                    restaurant = r

        if restaurant is not None:
            print(f"\t\tAnem al restaurant {restaurant.nom} ({restaurant.especialitat.especialitat}) que està a {round(distanciaMinima, 2)} metres a les coordenades ({restaurant.coordenades.latitud}, {restaurant.coordenades.longitud}) a per la comanda {comanda.id} ({comanda.especialitat.especialitat}).")

            motxilla.append(comanda)
            capacitatActual += restaurant.especialitat.pes
            ubicacioActual = restaurant.coordenades
            distanciaRecorreguda += distanciaMinima
            ruta.append(ubicacioActual)

            if not repetirRestaurants:
                restaurants.remove(restaurant)
        else:
            print(f"\t\tNo hi ha cap restaurant que ofereixi la especialitat {comanda.especialitat.especialitat} a prop de la ubicació actual.")
            Exception(f"No hi ha cap restaurant que ofereixi la especialitat {comanda.especialitat.especialitat} a prop de la ubicació actual.")
    
    print(f"\t\tLa motxilla s'ha omplert amb {capacitatActual} g de {capacitatMaxima} g i s'han visitat {len(motxilla)} restaurants.")

    return motxilla, distanciaRecorreguda, ubicacioActual, comandes, restaurants, ruta

def entregarComandes(inici: Coordenada, motxilla: List[Comanda]) -> Tuple[float, Coordenada, List[Coordenada]]:
    """
    Funció que simula l'entrega de comandes a partir d'una motxilla de restaurants.

    Heurística per determinar les comandes:
        La funció ordena la llista de comandes en funció del temps de compromís de cada comanda.
        De las comandes de la mateixa especialitat, ergo amb el mateix temps de compromís, s'entrega la comanda més propera.

    
    Args:
        inici (Coordenada): Coordenada inicial de la ubicació actual.
        motxilla (List[Restaurant]): Llista de restaurants a la motxilla.
        comandes (List[Comanda]): Llista de comandes a lliurar.
    
    Returns:
        Tuple[float, Coordenada, List[Comanda]]: 
            - Distància total recorreguda.
            - Coordenada final de la ubicació actual.
            - Llista de coordenades de la ruta.
    """

    ubicacioActual: Coordenada = inici
    distanciaRecorreguda: float = 0
    ruta: List[Coordenada] = [ubicacioActual]

    motxilla = sorted(motxilla, key=lambda comanda: comanda.especialitat.compromis)

    while len(motxilla) > 0:
        comanda: Comanda = motxilla[0]
        distanciaMinima: float = float("inf")

        for r in motxilla:
            if r.especialitat == comanda.especialitat:
                distancia: float = ubicacioActual.distancia(r.coordenades)
                if distancia < distanciaMinima:
                    distanciaMinima = distancia
                    comanda = r

        print(f"\t\tAnem a lliurar la comanda {comanda.id} ({comanda.especialitat.especialitat}) que està a {round(distanciaMinima, 2)} metres a les coordenades ({comanda.coordenades.latitud}, {comanda.coordenades.longitud}).")

        ubicacioActual = comanda.coordenades
        distanciaRecorreguda += distanciaMinima
        ruta.append(ubicacioActual)

        motxilla.remove(comanda)

    print(f"\t\tTotes les comandes han estat lliurades correctament i s'han recorregut {round(distanciaRecorreguda, 2)} metres.")

    return distanciaRecorreguda, ubicacioActual, ruta

def main(capacitatMaxima: int, repetirRestaurants: bool, outputFolder: str, outputFileName: str) -> None:
    comandesRestants: List[Comanda] = comandes.copy()
    ubicacioActual: Coordenada = tecnocampus
    restaurantsNoVisitats: List[Restaurant] = restaurants.copy()
    distanciaTotal: float = 0
    numeroRecollides: int = 0
    
    mapa = MapGenerator(tecnocampus, comandes, restaurants, especialitats, outputFolder)
    mapa.generateInitialMap()

    print("Mapa generat correctament")

    while len(comandesRestants) > 0:
        numeroRecollides += 1
        print(f"\tAnem a recollir comandes fins a omplir la motxilla.")
        motxilla, distancia, ubicacioActual, comandesRestants, restaurantsNoVisitats, ruta = omplirMotxilla(ubicacioActual, comandesRestants, capacitatMaxima, restaurantsNoVisitats, repetirRestaurants)
        distanciaTotal += distancia
        mapa.afegirRuta(ruta, f"Recollida número {numeroRecollides}", "blue")
        
        print(f"\tQueden {len(comandesRestants)} comandes per recollir.")
        print()
        print(f"\tAnem a entregar les comandes recollides.")
        
        distancia, ubicacioActual, ruta = entregarComandes(ubicacioActual, motxilla)
        distanciaTotal += distancia
        mapa.afegirRuta(ruta, f"Lliurament número {numeroRecollides}", "red")

        print()
        print()

    distanciaTotal += ubicacioActual.distancia(tecnocampus)
    mapa.afegirRuta([ubicacioActual, tecnocampus], "Tornada a l'oficina", "green")

    print(f"Totes les comandes han estat recollides i entregades correctament. En total s'han recorregut {round(distanciaTotal/10**3, 2)} kilometres.")
    outputPath = mapa.save(outputFileName)
    print(f"Mapa guardat correctament. Ho pots veure fent obrint el següent enllaç: file://{outputPath}")

if __name__ == "__main__":
    # argparse
    parser = argparse.ArgumentParser(description="Simulador de l'ompliment d'una motxilla amb comandes recollides en restaurants i l'entrega de les comandes.")
    
    parser.add_argument("--no-repetirRestaurants", dest="repetirRestaurants", action="store_false", default=True, help="No permet als restaurants preparar més d'una comanda.")
    parser.add_argument("--capacitatMaxima", type=int, default=12000, help="Capacitat màxima de la motxilla.")
    parser.add_argument("--outputFolder", type=str, default=os.path.join(os.path.dirname(__file__), "out"), help="Carpeta on es guardaran els mapes generats.")
    parser.add_argument("--outputFileName", type=str, default="mapa.html", help="Nom del fitxer on es guardarà el mapa generat.")
    
    args = parser.parse_args()

    input("\nPrem ENTER per començar a recollir comandes...")
    main(args.capacitatMaxima, args.repetirRestaurants, args.outputFolder, args.outputFileName)