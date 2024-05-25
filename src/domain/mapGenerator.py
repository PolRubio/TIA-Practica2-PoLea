from typing import Dict, List
import pandas as pd
import folium
import folium.plugins as folium_plugins

from coordenada import Coordenada
from comanda import Comanda
from restaurant import Restaurant
from especialitat import Especialitat

class MapGenerator:
    def __init__(self, tecnocampus: Coordenada, comandes: List[Comanda], restaurants: List[Restaurant], especialitats: Dict[str, Especialitat]):
        self.tecnocampus: Coordenada = tecnocampus
        self.comandes: List[Comanda] = comandes
        self.restaurants: List[Restaurant] = restaurants
        self.especialitats: Dict[str, Especialitat] = especialitats

    def puntMig(self) -> List[float]:
        coordenades = [comanda.coordenades for comanda in self.comandes] + [restaurant.coordenades for restaurant in self.restaurants]
        df = pd.DataFrame([(coordenada.latitud, coordenada.longitud) for coordenada in coordenades], columns=["latitud", "longitud"])
        punt_mig = df.mean()
        return [punt_mig["latitud"], punt_mig["longitud"]]

    def generateMap(self, html_file: str = "mapa.html") -> None:
        mapa = folium.Map(location=self.puntMig(), zoom_start=14)
        folium.Marker([self.tecnocampus.latitud, self.tecnocampus.longitud],
                      icon=folium.Icon(color='gray', icon='flag'),
                      popup="Tecnocampus").add_to(mapa)

        all_marcadors = folium.FeatureGroup("Totes les parades").add_to(mapa)

        grups_especialitats = {}
        for especialitat in self.especialitats.values():
            grups_especialitats[especialitat.especialitat] = folium_plugins.FeatureGroupSubGroup(all_marcadors, especialitat.especialitat)
            grups_especialitats[especialitat.especialitat].add_to(mapa)

        for comanda in self.comandes:
            folium.Marker([comanda.coordenades.latitud, comanda.coordenades.longitud],
                          icon=folium.Icon(color=comanda.especialitat.color_marcador, icon='home'),
                          popup=f"Comanda {comanda.id} - {comanda.especialitat.especialitat}").add_to(grups_especialitats[comanda.especialitat.especialitat])

        for restaurant in self.restaurants:
            folium.Marker([restaurant.coordenades.latitud, restaurant.coordenades.longitud],
                          icon=folium.Icon(color=restaurant.especialitat.color_marcador, icon='cutlery'),
                          popup=f"Restaurant {restaurant.nom} - {restaurant.especialitat.especialitat}").add_to(grups_especialitats[restaurant.especialitat.especialitat])

        folium.LayerControl().add_to(mapa)
        mapa.save(html_file)