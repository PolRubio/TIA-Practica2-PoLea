from typing import List, Optional, Tuple
import argparse, os

from domain.coordenada import Coordenada
from domain.comanda import Comanda
from domain.restaurant import Restaurant
from domain.mapGenerator import MapGenerator
from data.data import comandes, restaurants, especialitats, tecnocampus

def hillClimbing(comandes: List[Comanda], capacitatMaxima: int, iteracionsMaximes: int = 1000) -> Tuple[List[Comanda], List[Comanda]]:
    """
    Funció que implementa l'algorisme Hill Climbing per a la resolució del problema de la motxilla.

    Args:
        comandes (List[Comanda]): Llista de comandes a lliurar.
        capacitatMaxima (int): Capacitat màxima de la motxilla.
        iteracionsMaximes (int): Nombre màxim d'iteracions.

    Returns:
        Tuple[List[Comanda], List[Comanda]]:
            - Llista de comandes programades per lliurar.
            - Llista de comandes no programades per lliurar.
    """

    def fitness(comandes: List[Comanda], capacitatMaxima: int,) -> Tuple[float, int]:
        """
        Funció que calcula el fitness d'una solució.

        Args:
            comandes (List[Comanda]): Llista de comandes a lliurar.
            capacitatMaxima (int): Capacitat màxima de la motxilla.

        Returns:
            Tuple[int, int]: Tupla amb el fitness de la solució i el nombre de comandes.
        """
        pesAcumulat: int = 0
        numComandes: int = 0
        sumCompromis: float = 0
        for comanda in comandes:
            if pesAcumulat + comanda.especialitat.pes > capacitatMaxima:
                break
            pesAcumulat += comanda.especialitat.pes
            # El compromís de les comandes es multiplica per 0.9^numComandes
            # L'objectiu és donar més pes a les comandes més urgents
            # i garantir que dintre de la solució estiguin ordenades per compromís.
            sumCompromis += comanda.especialitat.compromis * 0.9 ** numComandes 
            numComandes += 1
        return (-sumCompromis, numComandes)

    def generarVeins(comandes: List[Comanda]) -> List[List[Comanda]]:
        """
        Funció que genera veins d'una solució.

        Args:
            comandes (List[Comanda]): Llista de comandes a lliurar.

        Returns:
            List[List[Comanda]]: Llista de veins de la solució.
        """
        veins: List[List[Comanda]] = []
        for i in range(len(comandes)):
            for j in range(i + 1, len(comandes)):
                vei: List[Comanda] = comandes[:]
                vei[i], vei[j] = vei[j], vei[i]
                veins.append(vei)
        return veins
    
    solucioActual: List[Comanda] = comandes[:]
    fitnessAcutal: Tuple[float, int] = fitness(solucioActual, capacitatMaxima)
    repeticions: int = 0
    for i in range(iteracionsMaximes):
        veins: List[List[Comanda]] = generarVeins(solucioActual)
        veinsFitness: List[Tuple[Tuple[float, int], List[Comanda]]] = [(fitness(vei, capacitatMaxima), vei) for vei in veins]
        millorFitness, millorVei = max(veinsFitness, key=lambda x: x[0])
        if millorFitness > fitnessAcutal:
            solucioActual = millorVei
            fitnessAcutal = millorFitness
            repeticions = 0
        else:
            repeticions += 1
            if repeticions > iteracionsMaximes*0.1:
                break
        
    solucioFinal: List[Comanda] = []
    pesAcumulat: int = 0
    for comanda in solucioActual[:]:
        if pesAcumulat + comanda.especialitat.pes > capacitatMaxima:
            break
        pesAcumulat += comanda.especialitat.pes
        solucioFinal.append(comanda)
        solucioActual.remove(comanda)
    return solucioFinal, solucioActual

def omplirMotxilla(inici: Coordenada, comandes: List[Comanda], capacitatMaxima: int, restaurants: List[Restaurant], repetirRestaurants: bool)-> Tuple[List[Comanda], float, Coordenada, List[Comanda], List[Restaurant], List[Coordenada]]:
    """
    Funció que simula l'ompliment d'una motxilla amb comandes recollides en restaurants.

    Heurística per determinar les comandes [Hill Climbing]:
        La funció ordena la llista de comandes en funció del temps de compromís de cada comanda.
        S'assegura que la comanda amb el temps de compromís més alt sigui processada primer.
        Això ajuda a prioritzar les comandes urgents i garanteix que es lliurin a temps.
        El temps de compromís ve determinat per l'especialitat de la comanda. Cada especialitat té un temps de compromís diferent.
        La funció calcula el pes acumulat de les comandes i s'assegura que no superi la seva capacitat màxima.
    
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

    comandesProgramades: List[Comanda] = []
    comandesNoProgramades: List[Comanda] = []

    # // comandes = sorted(comandes, key=lambda comanda: comanda.especialitat.compromis)
    comandesProgramades, comandesNoProgramades = hillClimbing(comandes, capacitatMaxima)

    while len(comandesProgramades) > 0: #TODO: BFS
        comanda: Comanda = comandesProgramades.pop(0)
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

    return motxilla, distanciaRecorreguda, ubicacioActual, comandesNoProgramades, restaurants, ruta

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

    #TODO: Hill Climbing
    #? Realment cal ordenar les comandes per compromis? Ja estan ordenades de quan les hem recollit.
    #? motxilla = sorted(motxilla, key=lambda comanda: comanda.especialitat.compromis)

    while len(motxilla) > 0: #TODO: BFS
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
    print(f"Mapa guardat correctament. Ho pots veure obrint el següent enllaç: file://{outputPath}")

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