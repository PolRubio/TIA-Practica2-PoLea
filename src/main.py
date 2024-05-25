from typing import List, Dict, Optional, Tuple

from domain.coordenada import Coordenada
from domain.comanda import Comanda
from domain.restaurant import Restaurant
from domain.especialitat import Especialitat
from domain.mapGenerator import MapGenerator

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

if __name__ == "__main__":
    # Variables globals
    CAPACITATMAXIMA = 12*10**3

    # Oficina de la startup
    tecnocampus: Coordenada = Coordenada(41.528154350078815, 2.4346229558256196)

    # Especialitats
    especialitats: Dict[str, Especialitat] = {
        "AFRICANA":   Especialitat("Africana",   35, 400, "red"),
        "ALEMANYA":   Especialitat("Alemanya",   38, 380, "darkred"),
        "AMERICANA":  Especialitat("Americana",  25, 425, "orange"),
        "ARGENTINA":  Especialitat("Argentina",  24, 450, "beige"),
        "CATALANA":   Especialitat("Catalana",   15, 400, "green"),
        "FRANCESA":   Especialitat("Francesa",   17, 395, "darkgreen"),
        "HINDU":      Especialitat("Hindu",      12, 410, "lightgreen"),
        "ITALIANA":   Especialitat("Italiana",   20, 440, "blue"),
        "JAPONESA":   Especialitat("Japonesa",   30, 300, "darkblue"),
        "MEXICANA":   Especialitat("Mexicana",   18, 370, "cadetblue"),
        "PERUANA":    Especialitat("Peruana",    16, 405, "lightblue"),
        "TAILANDESA": Especialitat("Tailandesa", 19, 385, "purple"),
        "VENEÇOLANA": Especialitat("Veneçolana", 28, 395, "darkpurple"),
        "XINESA":     Especialitat("Xinesa",     32, 350, "pink")
    }

    # Comandes i Restaurants
    comandes: List[Comanda] = [
        Comanda(1,  especialitats["ITALIANA"],   "La Riera 8",                    Coordenada(41.5409672844944,   2.4440583102421027)),
        Comanda(2,  especialitats["JAPONESA"],   "Sant Benet 8",                  Coordenada(41.538726781416834, 2.4409684054212284)),
        Comanda(3,  especialitats["PERUANA"],    "Plaça de Cuba 17",              Coordenada(41.5373334545074,   2.4412580840017153)),
        Comanda(4,  especialitats["AMERICANA"],  "Alarona 2",                     Coordenada(41.536241682816986, 2.433675182406231)),
        Comanda(5,  especialitats["CATALANA"],   "Plaça de Catalunya 28",         Coordenada(41.53892242551906,  2.4326291228807504)),
        Comanda(6,  especialitats["FRANCESA"],   "Via Europa 78",                 Coordenada(41.5436603011408,   2.432714953575982)),
        Comanda(7,  especialitats["HINDU"],      "Ronda dels Països Catalans 14", Coordenada(41.55342443860886,  2.437650599054971)),
        Comanda(8,  especialitats["AFRICANA"],   "Cirera 10",                     Coordenada(41.53219305728157,  2.4344512382250567)),
        Comanda(9,  especialitats["CATALANA"],   "Estrasburg 8",                  Coordenada(41.5539552447919,   2.433780967062532)),
        Comanda(10, especialitats["XINESA"],     "Josep Trueta 8",                Coordenada(41.55779979204186,  2.4291663535487595)),
        Comanda(11, especialitats["VENEÇOLANA"], "Pallars 8",                     Coordenada(41.5552014794221,   2.4622173904223486)),
        Comanda(12, especialitats["TAILANDESA"], "Foneria 20",                    Coordenada(41.55172272250503,  2.4528559670624053)),
        Comanda(13, especialitats["MEXICANA"],   "Caputxins 15",                  Coordenada(41.548553800569465, 2.4438222400793252)),
        Comanda(14, especialitats["ALEMANYA"],   "Aristòtil 8",                   Coordenada(41.55072744144044,  2.4361423535708835)),
        Comanda(15, especialitats["ARGENTINA"],  "Berguedà 12",                   Coordenada(41.54427910655742,  2.4256064904185313)),
        Comanda(16, especialitats["CATALANA"],   "Lluís Companys 15",             Coordenada(41.53597092869701,  2.431851953570033)),
        Comanda(17, especialitats["ITALIANA"],   "Gatasa 9",                      Coordenada(41.53692887976179,  2.430490776924513)),
        Comanda(18, especialitats["JAPONESA"],   "Can Llopis 8",                  Coordenada(41.54661088286044,  2.4664993535706574)),
        Comanda(19, especialitats["AMERICANA"],  "Torrent Forcat 12",             Coordenada(41.55229560800715,  2.4623012805538984)),
        Comanda(20, especialitats["ITALIANA"],   "Jaume Arenas 7",                Coordenada(41.55275726992884,  2.4471504192576554))
    ]

    restaurants: List[Restaurant] = [
        Restaurant("Katsumi Sushi", "Plaça d'Espanya 18",                              especialitats["JAPONESA"],   Coordenada(41.54464720858636,  2.4416859615824085)),
        Restaurant("Il Colosseo Trattoria Italiana", "Esteve Albert 77",               especialitats["ITALIANA"],   Coordenada(41.54593024438207,  2.4365111670620565)),
        Restaurant("Sèsam Negre", "Rambla 40",                                         especialitats["JAPONESA"],   Coordenada(41.537135125747554, 2.443674134596929)),
        Restaurant("Lumber Restaurant", "Cuba 19",                                     especialitats["AMERICANA"],  Coordenada(41.53714750357814,  2.441086024733921)),
        Restaurant("Su. Cocina Japonesa", "Pujol 6",                                   especialitats["JAPONESA"],   Coordenada(41.5392884295936,   2.445284795897865)),
        Restaurant("Ca La Ceci", "Avinguda del Maresme 327",                           especialitats["PERUANA"],    Coordenada(41.53710342616571,  2.4495552958977345)),
        Restaurant("La Pentola", "Pujol 27",                                           especialitats["ITALIANA"],   Coordenada(41.5396125426612,   2.4458779093893295)),
        Restaurant("Leks Thai", "Avinguda del Maresme 247",                            especialitats["TAILANDESA"], Coordenada(41.53510316172104,  2.4467790958976243)),
        Restaurant("Taller de Pizzes Matarò", "Plaça de les Tereses",                  especialitats["ITALIANA"],   Coordenada(41.53836814606081,  2.442328938225434)),
        Restaurant("La Cuina del Cel", "Sant Francesc d'Assís 7",                      especialitats["CATALANA"],   Coordenada(41.54173956711455,  2.4461042382256295)),
        Restaurant("Roma Bella", "Barcelona 24",                                       especialitats["ITALIANA"],   Coordenada(41.53877101772313,  2.4457867345974798)),
        Restaurant("Breton Creperie", "Pujol 47",                                      especialitats["FRANCESA"],   Coordenada(41.53966888146739,  2.446585367061709)),
        Restaurant("Som Terra Restaurant", "Avinguda del Maresme 259",                 especialitats["CATALANA"],   Coordenada(41.535338692221444, 2.4470666382252495)),
        Restaurant("Dem DIk", "Churruca 57",                                           especialitats["AFRICANA"],   Coordenada(41.53432132593146,  2.444637838225209)),
        Restaurant("Bar Europa", "Camí Ral de la Mercè 468",                           especialitats["CATALANA"],   Coordenada(41.53603315952693,  2.442483724733865)),
        Restaurant("Mueta", "Via Europa 17",                                           especialitats["ITALIANA"],   Coordenada(41.54146870729321,  2.4347118382256325)),
        Restaurant("Ohana Manos Japonesas", "Sant Benet 5",                            especialitats["JAPONESA"],   Coordenada(41.53862071472015,  2.441257624733986)),
        Restaurant("Villanueva", "Jaume I 69",                                         especialitats["CATALANA"],   Coordenada(41.53728965656242,  2.4235712382253842)),
        Restaurant("El Quiosc de Can Carreras", "Cuba 22",                             especialitats["AMERICANA"],  Coordenada(41.53768187106671,  2.439798851716858)),
        Restaurant("Restaurante Tokyo to", "Camí Ral de la Mercè 600",                 especialitats["JAPONESA"],   Coordenada(41.5332504660919,   2.4388760670613268)),
        Restaurant("La Morera", "Avinguda del Maresme 507",                            especialitats["CATALANA"],   Coordenada(41.540939808672526, 2.4555642382256084)),
        Restaurant("Roti - Indian Kitchen", "Cuba 59",                                 especialitats["HINDU"],      Coordenada(41.53652672873163,  2.4419799769242956)),
        Restaurant("Worldburg", "Ronda dels Països Catalans 35",                       especialitats["AMERICANA"],  Coordenada(41.55435761628667,  2.439695167062555)),
        Restaurant("Peix & Chips", "Cuba 50",                                          especialitats["CATALANA"],   Coordenada(41.53729451062742,  2.4405324958977372)),
        Restaurant("LeBoel", "Barcelona 19",                                           especialitats["ITALIANA"],   Coordenada(41.53880765298093,  2.4457449824063815)),
        Restaurant("Dolce Vita", "Port de Mataró Local",                               especialitats["ITALIANA"],   Coordenada(41.53219425336816,  2.446834513542146)),
        Restaurant("Piazza Italia", "Via Europa 45",                                   especialitats["ITALIANA"],   Coordenada(41.54302471513448,  2.433063180553343)),
        Restaurant("Bunker Mataro", "Sant Benet 19",                                   especialitats["CATALANA"],   Coordenada(41.53853261494995,  2.4407813382254706)),
        Restaurant("Bululú Beach Mataró", "Passeig del Callao",                        especialitats["MEXICANA"],   Coordenada(41.53740877948377,  2.4513349958977257)),
        Restaurant("La Lluna", "Cuba 92",                                              especialitats["ITALIANA"],   Coordenada(41.53643301319498,  2.4415900382253644)),
        Restaurant("Gelatiamo Mataró", "Parc Estrasburg 5",                            especialitats["ITALIANA"],   Coordenada(41.554777443937844, 2.433533795898745)),
        Restaurant("Pizzeria La Piccola", "Torrent 1",                                 especialitats["ITALIANA"],   Coordenada(41.54067341818605,  2.440359724734154)),
        Restaurant("Sport House", "Llauder 138",                                       especialitats["AMERICANA"],  Coordenada(41.533215634855175, 2.437747880552781)),
        Restaurant("Hapo Mataró", "Consol Nogueras 1",                                 especialitats["JAPONESA"],   Coordenada(41.54425695992392,  2.4359413535705174)),
        Restaurant("Frankfurt's", "La Riera 50",                                       especialitats["AMERICANA"],  Coordenada(41.54012141688526,  2.444735805761813)),
        Restaurant("Chipotlin", "Solís 1",                                             especialitats["MEXICANA"],   Coordenada(41.54115164745028,  2.4510308958979476)),
        Restaurant("Restaurant Caliu", "Via Europa 26",                                especialitats["CATALANA"],   Coordenada(41.54163429769361,  2.4356969535703543)),
        Restaurant("Pizzeria Lluis", "Baixada Escaletes 2",                            especialitats["ITALIANA"],   Coordenada(41.53903934422724,  2.4471524093893096)),
        Restaurant("Granja Caralt", "La Riera 91",                                     especialitats["CATALANA"],   Coordenada(41.54095580863068,  2.4440770670617726)),
        Restaurant("Nou Daxana", "Jaume Balmes 35",                                    especialitats["CATALANA"],   Coordenada(41.53613649024019,  2.4472060535700466)),
        Restaurant("Bàltic", "Dinamarca 32",                                           especialitats["AMERICANA"],  Coordenada(41.54612798429978,  2.430001095898259)),
        Restaurant("Dolç & Salat", "Ronda President Macià 18",                         especialitats["CATALANA"],   Coordenada(41.533717268524995, 2.437835680552798)),
        Restaurant("Restaurante Asiatico Sheng", "Via Europa 45",                      especialitats["XINESA"],     Coordenada(41.542888203591204, 2.433084638225704)),
        Restaurant("Parrilla Argentina Bariloche", "Ronda Mossèn Jacint Verdaguer 31", especialitats["ARGENTINA"],  Coordenada(41.54386303104852,  2.4357107247343075)),
        Restaurant("Dulce Bakery", "Iluro 42",                                         especialitats["AMERICANA"],  Coordenada(41.53689828094192,  2.439746282406275)),
        Restaurant("Espressione Mataro", "Alemanya 50",                                especialitats["ARGENTINA"],  Coordenada(41.54486946483929,  2.4304387769272773)),
        Restaurant("Arepados Mataró", "Camí Ral de la Mercè 50",                       especialitats["VENEÇOLANA"], Coordenada(41.53518895474587,  2.441372480552906)),
        Restaurant("Restaurante Macgyver", "Ronda Creu de Pedra 25",                   especialitats["CATALANA"],   Coordenada(41.55492913734824,  2.445897176930784)),
        Restaurant("Restaurant Oliva", "Plaça de la Muralla 5",                        especialitats["CATALANA"],   Coordenada(41.539430090418996, 2.4481656382255053)),
        Restaurant("Nova Rosaleda", "Altafulla 32",                                    especialitats["CATALANA"],   Coordenada(41.53945151255366,  2.4390968535702324)),
        Restaurant("El Raco de Jabugo", "La Rambla 20",                                especialitats["CATALANA"],   Coordenada(41.537665448179965, 2.4439348228806472)),
        Restaurant("Espai culinari Cafè de Mar", "Santa Rita 1",                       especialitats["CATALANA"],   Coordenada(41.53575502007947,  2.447354080552949)),
        Restaurant("El Pirata", "Port de Mataró 8",                                    especialitats["CATALANA"],   Coordenada(41.5309262612138,   2.4449362958973393)),
        Restaurant("Otto Sport Bar", "Ronda Frederic Mistral 14",                      especialitats["ALEMANYA"],   Coordenada(41.55106676957816,  2.4390659958985474)),
        Restaurant("Twister", "Ronda Mossèn Jacint Verdaguer 73",                      especialitats["CATALANA"],   Coordenada(41.54514647456461,  2.437272405763572)),
        Restaurant("El Fanalet", "Sant Cristòfor, 15",                                 especialitats["ITALIANA"],   Coordenada(41.53944750421106,  2.447086095897898)),
        Restaurant("La Taula de Mataro", "Na Pau 5",                                   especialitats["ITALIANA"],   Coordenada(41.54017486512463,  2.447023905761776)),
        Restaurant("Nambu Tekki", "El Torrent 49",                                     especialitats["CATALANA"],   Coordenada(41.539356243361425, 2.4417596805531447)),
        Restaurant("MásQMenos", "Plaça de Santa Anna 6",                               especialitats["CATALANA"],   Coordenada(41.53844272141184,  2.4445503535701727)),
        Restaurant("Rustik", "Port de Mataró",                                         especialitats["CATALANA"],   Coordenada(41.53101425574082,  2.4449785805526436)),
        Restaurant("Classic Coffee", "Plaça de Santa Anna 5",                          especialitats["CATALANA"],   Coordenada(41.538446144156936, 2.4445080535701553)),
        Restaurant("El Montadito Del Centre", "La Rambla 24",                          especialitats["CATALANA"],   Coordenada(41.53754512559153,  2.443928638225382)),
        Restaurant("Auto d'Ara", "Avinguda de Cabrera 36",                             especialitats["CATALANA"],   Coordenada(41.52361052134397,  2.4280699958969367)),
        Restaurant("Yokki", "Ronda del President Irla 28",                             especialitats["JAPONESA"],   Coordenada(41.53195592564781,  2.439545022880373)),
        Restaurant("El Doge Pizzeria Ristorante", "Passeig Marítim 250",               especialitats["ITALIANA"],   Coordenada(41.54122102317959,  2.458249019253706)),
        Restaurant("Kristal Serfran", "Pablo Iglesias 36",                             especialitats["AMERICANA"],  Coordenada(41.53384159593934,  2.4305239958975458)),
        Restaurant("Ke D Ke", "Ronda Mossèn Jacint Verdaguer 55",                      especialitats["CATALANA"],   Coordenada(41.54458130580683,  2.4366386922719068)),
        Restaurant("Frankfurt La Canica Azul", "Ronda Mossèn Jacint Verdaguer 43",     especialitats["AMERICANA"],  Coordenada(41.55397119487552,  2.40100729465889)),
        Restaurant("Alsus", "Ronda Països Catalans 86",                                especialitats["CATALANA"],   Coordenada(41.55475653782008,  2.4418767480945114)),
        Restaurant("Restaurant Yami", "Camí Ral de la Mercè",                          especialitats["JAPONESA"],   Coordenada(41.53518895474587,  2.4414046670614464)),
        Restaurant("Braseria Alamo", "Energia 50",                                     especialitats["CATALANA"],   Coordenada(41.554982514811726, 2.4500655400796565)),
        Restaurant("Restaurant Scorpio", "Ronda Sant Oleguer 25",                      especialitats["ITALIANA"],   Coordenada(41.55166938068827,  2.4423778112432926)),
        Restaurant("Alla Vitta Veloce Pizzeria", "Alemanya 33",                        especialitats["ITALIANA"],   Coordenada(41.54492983853537,  2.4308996824067117)),
        Restaurant("Sesam Negre Expres", "Via Europa 83",                              especialitats["JAPONESA"],   Coordenada(41.54398197731273,  2.432272948090816)),
        Restaurant("Birrateka", "Avinguda del Maresme 347",                            especialitats["CATALANA"],   Coordenada(41.53751127919101,  2.4500923093891918)),
        Restaurant("RedCup Mataró", "Batista i Roca 63",                               especialitats["MEXICANA"],   Coordenada(41.53233567396886,  2.423961438225085)),
        Restaurant("Pizzeria Carlos Mataró", "Alemanya 1",                             especialitats["ITALIANA"],   Coordenada(41.54655034158848,  2.4313809904193517)),
        Restaurant("Mestolo", "Ronda Barceló 2",                                       especialitats["ITALIANA"],   Coordenada(41.534050964203416, 2.440560495897554)),
        Restaurant("Rosita", "Plaça Santa Anna",                                       especialitats["CATALANA"],   Coordenada(41.538121476352245, 2.4447740247339658)),
        Restaurant("Atlantida", "Estrasburg 5",                                        especialitats["ITALIANA"],   Coordenada(41.554777443937844, 2.433533795898745)),
        Restaurant("Pizzeria Catània", "Sant Isidor 78",                               especialitats["ITALIANA"],   Coordenada(41.54347796214908,  2.439684024734263)),
        Restaurant("Omnia Cafe-Bar", "Palmerola 4",                                    especialitats["CATALANA"],   Coordenada(41.53860711852714,  2.4414085192527155))
    ]


    input("\nPrem ENTER per començar a recollir comandes...")

    repetirRestaurants: bool = input("Un restaurant pot preparar més d'una comanda? (s/n) ").lower() == "s"

    comandesRestants: List[Comanda] = comandes.copy()
    ubicacioActual: Coordenada = tecnocampus
    restaurantsNoVisitats: List[Restaurant] = restaurants.copy()
    distanciaTotal: float = 0
    numeroRecollides: int = 0
    
    mapa = MapGenerator(tecnocampus, comandes, restaurants, especialitats)
    mapa.generateInitialMap()

    print("Mapa generat correctament")

    while len(comandesRestants) > 0:
        numeroRecollides += 1
        print(f"\tAnem a recollir comandes fins a omplir la motxilla.")
        motxilla, distancia, ubicacioActual, comandesRestants, restaurantsNoVisitats, ruta = omplirMotxilla(ubicacioActual, comandesRestants, 1000, restaurantsNoVisitats, repetirRestaurants)
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
    outputPath = mapa.save()
    print(f"Mapa guardat correctament. Ho pots veure fent obrint el següent enllaç: file://{outputPath}")