from typing import List, Dict
import pandas as pd
from geopy.distance import geodesic

class Especialitat:
    def __init__(self, especialitat: str, compromis: int, pes: int) -> None:
        self.especialitat: str = especialitat
        self.compromis: int = compromis
        self.pes: int = pes

class Coordenada:
    def __init__(self, latitud: float, longitud: float) -> None:
        self.latitud: float = latitud
        self.longitud: float = longitud

class Comanda:
    def __init__(self, id: int, especialitat: Especialitat, carrer: str, coordenades: Coordenada) -> None:
        self.id: int = id
        self.especialitat: Especialitat = especialitat
        self.carrer: str = carrer
        self.coordenades: Coordenada = coordenades

class Restaurant:
    def __init__(self, especialitat: Especialitat, nom: str, coordenades: Coordenada) -> None:
        self.especialitat: Especialitat = especialitat
        self.nom: str = nom
        self.coordenades: Coordenada = coordenades

# Oficina de la startup
tecnocampus: Coordenada = Coordenada(41.528154350078815, 2.4346229558256196)

# Especialitats
especialitats: Dict[str, Especialitat] = {
    "AFRICANA": Especialitat("Africana", 35, 400),
    "ALEMANYA": Especialitat("Alemanya", 38, 380),
    "AMERICANA": Especialitat("Americana", 25, 425),
    "ARGENTINA": Especialitat("Argentina", 24, 450),
    "CATALANA": Especialitat("Catalana", 15, 400),
    "FRANCESA": Especialitat("Francesa", 17, 395),
    "HINDU": Especialitat("Hindú", 12, 410),
    "ITALIANA": Especialitat("Italiana", 20, 440),
    "JAPONESA": Especialitat("Japonesa", 30, 300),
    "MEXICANA": Especialitat("Mexicana", 18, 370),
    "PERUANA": Especialitat("Peruana", 16, 405),
    "TAILANDESA": Especialitat("Tailandesa", 19, 385),
    "VENEÇOLANA": Especialitat("Veneçolana", 28, 395),
    "XINESA": Especialitat("Xinesa", 32, 350)
}

# comandes i restaurants
comandes: List[Comanda] = [
    Comanda(1, especialitats["ITALIANA"], "La Riera 8", Coordenada(41.5409672844944, 2.4440583102421027)),
    Comanda(2, especialitats["JAPONESA"], "Sant Benet 8", Coordenada(41.538726781416834, 2.4409684054212284)),
    Comanda(3, especialitats["PERUANA"], "Plaça de Cuba 17", Coordenada(41.5373334545074, 2.4412580840017153)),
    Comanda(4, especialitats["AMERICANA"], "Alarona 2", Coordenada(41.536241682816986, 2.433675182406231)),
    Comanda(5, especialitats["CATALANA"], "Plaça de Catalunya 28", Coordenada(41.53892242551906, 2.4326291228807504)),
    Comanda(6, especialitats["FRANCESA"], "Via Europa 78", Coordenada(41.5436603011408, 2.432714953575982)),
    Comanda(7, especialitats["HINDU"], "Ronda dels Països Catalans 14", Coordenada(41.55342443860886, 2.437650599054971)),
    Comanda(8, especialitats["AFRICANA"], "Cirera 10", Coordenada(41.53219305728157, 2.4344512382250567)),
    Comanda(9, especialitats["CATALANA"], "Estrasburg 8", Coordenada(41.5539552447919, 2.433780967062532)),
    Comanda(10, especialitats["XINESA"], "Josep Trueta 8", Coordenada(41.55779979204186, 2.4291663535487595)),
    Comanda(11, especialitats["VENEÇOLANA"], "Pallars 8", Coordenada(41.5552014794221, 2.4622173904223486)),
    Comanda(12, especialitats["TAILANDESA"], "Foneria 20", Coordenada(41.55172272250503, 2.4528559670624053)),
    Comanda(13, especialitats["MEXICANA"], "Caputxins 15", Coordenada(41.548553800569465, 2.4438222400793252)),
    Comanda(14, especialitats["ALEMANYA"], "Aristòtil 8", Coordenada(41.55072744144044, 2.4361423535708835)),
    Comanda(15, especialitats["ARGENTINA"], "Berguedà 12", Coordenada(41.54427910655742, 2.4256064904185313)),
    Comanda(16, especialitats["CATALANA"], "Lluís Companys 15", Coordenada(41.53597092869701, 2.431851953570033)),
    Comanda(17, especialitats["ITALIANA"], "Gatasa 9", Coordenada(41.53692887976179, 2.430490776924513)),
    Comanda(18, especialitats["JAPONESA"], "Can Llopis 8", Coordenada(41.54661088286044, 2.4664993535706574)),
    Comanda(19, especialitats["AMERICANA"], "Torrent Forcat 12", Coordenada(41.55229560800715, 2.4623012805538984)),
    Comanda(20, especialitats["ITALIANA"], "Jaume Arenas 7", Coordenada(41.55275726992884, 2.4471504192576554)),
]

restaurants: List[Restaurant] = [
    Restaurant("Katsumi Sushi", "Plaça d'Espanya 18", especialitats.JAPONESA, Coordenada(41.54464720858636, 2.4416859615824085)),
    Restaurant("Il Colosseo Trattoria Italiana", "Esteve Albert 77", especialitats.ITALIANA, Coordenada(41.54593024438207, 2.4365111670620565)),
    Restaurant("Sèsam Negre", "Rambla 40", especialitats.JAPONESA, Coordenada(41.537135125747554, 2.443674134596929)),
    Restaurant("Lumber Restaurant", "Cuba 19", especialitats.AMERICANA, Coordenada(41.53714750357814, 2.441086024733921)),
    Restaurant("Su. Cocina Japonesa", "Pujol 6", especialitats.JAPONESA, Coordenada(41.5392884295936, 2.445284795897865)),
    Restaurant("Ca La Ceci", "Avinguda del Maresme 327", especialitats.PERUANA, Coordenada(41.53710342616571, 2.4495552958977345)),
    Restaurant("La Pentola", "Pujol 27", especialitats.ITALIANA, Coordenada(41.5396125426612, 2.4458779093893295)),
    Restaurant("Leks Thai", "Avinguda del Maresme 247", especialitats.TAILANDESA, Coordenada(41.53510316172104, 2.4467790958976243)),
    Restaurant("Taller de Pizzes Matarò", "Plaça de les Tereses", especialitats.ITALIANA, Coordenada(41.53836814606081, 2.442328938225434)),
    Restaurant("La Cuina del Cel", "Sant Francesc d'Assís 7", especialitats.CATALANA, Coordenada(41.54173956711455, 2.4461042382256295)),
    Restaurant("Roma Bella", "Barcelona 24", especialitats.ITALIANA, Coordenada(41.53877101772313, 2.4457867345974798)),
    Restaurant("Breton Creperie", "Pujol 47", especialitats.FRANCESA, Coordenada(41.53966888146739, 2.446585367061709)),
    Restaurant("Som Terra Restaurant", "Avinguda del Maresme 259", especialitats.CATALANA, Coordenada(41.535338692221444, 2.4470666382252495)),
    Restaurant("Dem DIk", "Churruca 57", especialitats.AFRICANA, Coordenada(41.53432132593146, 2.444637838225209)),
    Restaurant("Bar Europa", "Camí Ral de la Mercè 468", especialitats.CATALANA, Coordenada(41.53603315952693, 2.442483724733865)),
    Restaurant("Mueta", "Via Europa 17", especialitats.ITALIANA, Coordenada(41.54146870729321, 2.4347118382256325)),
    Restaurant("Ohana Manos Japonesas", "Sant Benet 5", especialitats.JAPONESA, Coordenada(41.53862071472015, 2.441257624733986)),
    Restaurant("Villanueva", "Jaume I 69", especialitats.CATALANA, Coordenada(41.53728965656242, 2.4235712382253842)),
    Restaurant("El Quiosc de Can Carreras", "Cuba 22", especialitats.AMERICANA, Coordenada(41.53768187106671, 2.439798851716858)),
    Restaurant("Restaurante Tokyo to", "Camí Ral de la Mercè 600", especialitats.JAPONESA, Coordenada(41.5332504660919, 2.4388760670613268)),
    Restaurant("La Morera", "Avinguda del Maresme 507", especialitats.CATALANA, Coordenada(41.540939808672526, 2.4555642382256084)),
    Restaurant("Roti - Indian Kitchen", "Cuba 59", especialitats.HINDÚ, Coordenada(41.53652672873163, 2.4419799769242956)),
    Restaurant("Worldburg", "Ronda dels Països Catalans 35", especialitats.AMERICANA, Coordenada(41.55435761628667, 2.439695167062555)),
    Restaurant("Peix & Chips", "Cuba 50", especialitats.CATALANA, Coordenada(41.53729451062742, 2.4405324958977372)),
    Restaurant("LeBoel", "Barcelona 19", especialitats.ITALIANA, Coordenada(41.53880765298093, 2.4457449824063815)),
    Restaurant("Dolce Vita", "Port de Mataró Local", especialitats.ITALIANA, Coordenada(41.53219425336816, 2.446834513542146)),
    Restaurant("Piazza Italia", "Via Europa 45", especialitats.ITALIANA, Coordenada(41.54302471513448, 2.433063180553343)),
    Restaurant("Bunker Mataro", "Sant Benet 19", especialitats.CATALANA, Coordenada(41.53853261494995, 2.4407813382254706)),
    Restaurant("Bululú Beach Mataró", "Passeig del Callao", especialitats.MEXICANA, Coordenada(41.53740877948377, 2.4513349958977257)),
    Restaurant("La Lluna", "Cuba 92", especialitats.ITALIANA, Coordenada(41.53643301319498, 2.4415900382253644)),
    Restaurant("Gelatiamo Mataró", "Parc Estrasburg 5", especialitats.ITALIANA, Coordenada(41.554777443937844, 2.433533795898745)),
    Restaurant("Pizzeria La Piccola", "Torrent 1", especialitats.ITALIANA, Coordenada(41.54067341818605, 2.440359724734154)),
    Restaurant("Sport House", "Llauder 138", especialitats.AMERICANA, Coordenada(41.533215634855175, 2.437747880552781)),
    Restaurant("Hapo Mataró", "Consol Nogueras 1", especialitats.JAPONESA, Coordenada(41.54425695992392, 2.4359413535705174)),
    Restaurant("Frankfurt's", "La Riera 50", especialitats.AMERICANA, Coordenada(41.54012141688526, 2.444735805761813)),
    Restaurant("Chipotlin", "Solís 1", especialitats.MEXICANA, Coordenada(41.54115164745028, 2.4510308958979476)),
    Restaurant("Restaurant Caliu", "Via Europa 26", especialitats.CATALANA, Coordenada(41.54163429769361, 2.4356969535703543)),
    Restaurant("Pizzeria Lluis", "Baixada Escaletes 2", especialitats.ITALIANA, Coordenada(41.53903934422724, 2.4471524093893096)),
    Restaurant("Granja Caralt", "La Riera 91", especialitats.CATALANA, Coordenada(41.54095580863068, 2.4440770670617726)),
    Restaurant("Nou Daxana", "Jaume Balmes 35", especialitats.CATALANA, Coordenada(41.53613649024019, 2.4472060535700466)),
    Restaurant("Bàltic", "Dinamarca 32", especialitats.AMERICANA, Coordenada(41.54612798429978, 2.430001095898259)),
    Restaurant("Dolç & Salat", "Ronda President Macià 18", especialitats.CATALANA, Coordenada(41.533717268524995, 2.437835680552798)),
    Restaurant("Restaurante Asiatico Sheng", "Via Europa 45", especialitats.XINESA, Coordenada(41.542888203591204, 2.433084638225704)),
    Restaurant("Parrilla Argentina Bariloche", "Ronda Mossèn Jacint Verdaguer 31", especialitats.ARGENTINA, Coordenada(41.54386303104852, 2.4357107247343075)),
    Restaurant("Dulce Bakery", "Iluro 42", especialitats.AMERICANA, Coordenada(41.53689828094192, 2.439746282406275)),
    Restaurant("Espressione Mataro", "Alemanya 50", especialitats.ARGENTINA, Coordenada(41.54486946483929, 2.4304387769272773)),
    Restaurant("Arepados Mataró", "Camí Ral de la Mercè 50", especialitats.VENEÇOLANA, Coordenada(41.53518895474587, 2.441372480552906)),
    Restaurant("Restaurante Macgyver", "Ronda Creu de Pedra 25", especialitats.CATALANA, Coordenada(41.55492913734824, 2.445897176930784)),
    Restaurant("Restaurant Oliva", "Plaça de la Muralla 5", especialitats.CATALANA, Coordenada(41.539430090418996, 2.4481656382255053)),
    Restaurant("Nova Rosaleda", "Altafulla 32", especialitats.CATALANA, Coordenada(41.53945151255366, 2.4390968535702324)),
    Restaurant("El Raco de Jabugo", "La Rambla 20", especialitats.CATALANA, Coordenada(41.537665448179965, 2.4439348228806472)),
    Restaurant("Espai culinari Cafè de Mar", "Santa Rita 1", especialitats.CATALANA, Coordenada(41.53575502007947, 2.447354080552949)),
    Restaurant("El Pirata", "Port de Mataró 8", especialitats.CATALANA, Coordenada(41.5309262612138, 2.4449362958973393)),
    Restaurant("Otto Sport Bar", "Ronda Frederic Mistral 14", especialitats.ALEMANYA, Coordenada(41.55106676957816, 2.4390659958985474)),
    Restaurant("Twister", "Ronda Mossèn Jacint Verdaguer 73", especialitats.CATALANA, Coordenada(41.54514647456461, 2.437272405763572)),
    Restaurant("El Fanalet", "Sant Cristòfor, 15", especialitats.ITALIANA, Coordenada(41.53944750421106, 2.447086095897898)),
    Restaurant("La Taula de Mataro", "Na Pau 5", especialitats.ITALIANA, Coordenada(41.54017486512463, 2.447023905761776)),
    Restaurant("Nambu Tekki", "El Torrent 49", especialitats.CATALANA, Coordenada(41.539356243361425, 2.4417596805531447)),
    Restaurant("MásQMenos", "Plaça de Santa Anna 6", especialitats.CATALANA, Coordenada(41.53844272141184, 2.4445503535701727)),
    Restaurant("Rustik", "Port de Mataró", especialitats.CATALANA, Coordenada(41.53101425574082, 2.4449785805526436)),
    Restaurant("Classic Coffee", "Plaça de Santa Anna 5", especialitats.CATALANA, Coordenada(41.538446144156936, 2.4445080535701553)),
    Restaurant("El Montadito Del Centre", "La Rambla 24", especialitats.CATALANA, Coordenada(41.53754512559153, 2.443928638225382)),
    Restaurant("Auto d'Ara", "Avinguda de Cabrera 36", especialitats.CATALANA, Coordenada(41.52361052134397, 2.4280699958969367)),
    Restaurant("Yokki", "Ronda del President Irla 28", especialitats.JAPONESA, Coordenada(41.53195592564781, 2.439545022880373)),
    Restaurant("El Doge Pizzeria Ristorante", "Passeig Marítim 250", especialitats.ITALIANA, Coordenada(41.54122102317959, 2.458249019253706)),
    Restaurant("Kristal Serfran", "Pablo Iglesias 36", especialitats.AMERICANA, Coordenada(41.53384159593934, 2.4305239958975458)),
    Restaurant("Ke D Ke", "Ronda Mossèn Jacint Verdaguer 55", especialitats.CATALANA, Coordenada(41.54458130580683, 2.4366386922719068)),
    Restaurant("Frankfurt La Canica Azul", "Ronda Mossèn Jacint Verdaguer 43", especialitats.AMERICANA, Coordenada(41.55397119487552, 2.40100729465889)),
    Restaurant("Alsus", "Ronda Països Catalans 86", especialitats.CATALANA, Coordenada(41.55475653782008, 2.4418767480945114)),
    Restaurant("Restaurant Yami", "Camí Ral de la Mercè", especialitats.JAPONESA, Coordenada(41.53518895474587, 2.4414046670614464)),
    Restaurant("Braseria Alamo", "Energia 50", especialitats.CATALANA, Coordenada(41.554982514811726, 2.4500655400796565)),
    Restaurant("Restaurant Scorpio", "Ronda Sant Oleguer 25", especialitats.ITALIANA, Coordenada(41.55166938068827, 2.4423778112432926)),
    Restaurant("Alla Vitta Veloce Pizzeria", "Alemanya 33", especialitats.ITALIANA, Coordenada(41.54492983853537, 2.4308996824067117)),
    Restaurant("Sesam Negre Expres", "Via Europa 83", especialitats.JAPONESA, Coordenada(41.54398197731273, 2.432272948090816)),
    Restaurant("Birrateka", "Avinguda del Maresme 347", especialitats.CATALANA, Coordenada(41.53751127919101, 2.4500923093891918)),
    Restaurant("RedCup Mataró", "Batista i Roca 63", especialitats.MEXICANA, Coordenada(41.53233567396886, 2.423961438225085)),
    Restaurant("Pizzeria Carlos Mataró", "Alemanya 1", especialitats.ITALIANA, Coordenada(41.54655034158848, 2.4313809904193517)),
    Restaurant("Mestolo", "Ronda Barceló 2", especialitats.ITALIANA, Coordenada(41.534050964203416, 2.440560495897554)),
    Restaurant("Rosita", "Plaça Santa Anna", especialitats.CATALANA, Coordenada(41.538121476352245, 2.4447740247339658)),
    Restaurant("Atlantida", "Estrasburg 5", especialitats.ITALIANA, Coordenada(41.554777443937844, 2.433533795898745)),
    Restaurant("Pizzeria Catània", "Sant Isidor 78", especialitats.ITALIANA, Coordenada(41.54347796214908, 2.439684024734263)),
    Restaurant("Omnia Cafe-Bar", "Palmerola 4", especialitats.CATALANA, Coordenada(41.53860711852714, 2.4414085192527155)),
]

# Ordenar las recogidas por tiempo de entrega y distancia desde el Tecnocampus
def ordenar_recogidas(pedidos, restaurantes, initial_location):
    recogidas = []
    for especialidad, grupo in pd.DataFrame(pedidos).groupby("Especialidad"):
        restaurante = restaurantes[especialidad]
        grupo = grupo.sort_values(by="Especialidad")
        for _, pedido in grupo.iterrows():
            distancia = geodesic(initial_location, restaurante["Coordenadas"]).kilometers
            recogidas.append((pedido["Id"], especialidad, restaurante["Nombre"], restaurante["Coordenadas"], distancia))
    recogidas.sort(key=lambda x: x[4])
    return recogidas

# Ordenar las entregas por especialidad y distancia desde la ubicación actual del repartidor
def ordenar_entregas(pedidos, initial_location):
    entregas = []
    for especialidad, grupo in pd.DataFrame(pedidos).groupby("Especialidad"):
        grupo["Distancia"] = grupo["Coordenadas"].apply(lambda x: geodesic(initial_location, x).kilometers)
        grupo = grupo.sort_values(by="Distancia")
        for _, pedido in grupo.iterrows():
            entregas.append((pedido["Id"], especialidad, pedido["Calle"], pedido["Coordenadas"], pedido["Distancia"]))
    entregas.sort(key=lambda x: x[4])
    return entregas

# Imprimir las paradas y estados
def imprimir_paradas_estados(recogidas, entregas):
    print("Recogidas:")
    for recogida in recogidas:
        print(f"Recoger pedido {recogida[0]} de especialidad {recogida[1]} en {recogida[2]} ({recogida[3]})")

    print("\nEntregas:")
    for entrega in entregas:
        print(f"Entregar pedido {entrega[0]} de especialidad {entrega[1]} en {entrega[2]} ({entrega[3]})")

# Ordenar las recogidas y entregas
recogidas = ordenar_recogidas(pedidos, restaurantes, initial_location)
entregas = ordenar_entregas(pedidos, initial_location)

# Imprimir los resultados
imprimir_paradas_estados(recogidas, entregas)

# print the detailed and complete info of the first comanda
print(f"Comanda {comandes[0].id}: {comandes[0].especialitat.especialitat} - {comandes[0].carrer} - {comandes[0].coordenades.latitud} - {comandes[0].coordenades.longitud}")
