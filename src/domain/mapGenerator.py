from typing import Dict, List
import pandas as pd
import folium
import folium.plugins as folium_plugins
import os

from domain.coordenada import Coordenada
from domain.comanda import Comanda
from domain.restaurant import Restaurant
from domain.especialitat import Especialitat

class MapGenerator:
    def __init__(self, tecnocampus: Coordenada, comandes: List[Comanda], restaurants: List[Restaurant], especialitats: Dict[str, Especialitat], output_folder: str = os.path.join(os.path.dirname(__file__), "out")):
        self.tecnocampus: Coordenada = tecnocampus
        self.comandes: List[Comanda] = comandes
        self.restaurants: List[Restaurant] = restaurants
        self.especialitats: Dict[str, Especialitat] = especialitats
        self.mapa = folium.Map(location=self.puntMig(), zoom_start=14)
        self.output_folder = output_folder
        os.makedirs(output_folder, exist_ok=True)

    def puntMig(self) -> List[float]:
        coordenades = [comanda.coordenades for comanda in self.comandes] + [restaurant.coordenades for restaurant in self.restaurants]
        df = pd.DataFrame([(coordenada.latitud, coordenada.longitud) for coordenada in coordenades], columns=["latitud", "longitud"])
        punt_mig = df.mean()
        return [punt_mig["latitud"], punt_mig["longitud"]]

    def generateInitialMap(self) -> folium.Map:
        folium.Marker([self.tecnocampus.latitud, self.tecnocampus.longitud],
                      icon=folium.Icon(color='gray', icon='flag'),
                      popup="Tecnocampus").add_to(self.mapa)

        all_marcadors = folium.FeatureGroup("Totes les parades").add_to(self.mapa)

        grups_especialitats = {}
        for especialitat in self.especialitats.values():
            grups_especialitats[especialitat.especialitat] = folium_plugins.FeatureGroupSubGroup(all_marcadors, especialitat.especialitat)
            grups_especialitats[especialitat.especialitat].add_to(self.mapa)

        for comanda in self.comandes:
            folium.Marker([comanda.coordenades.latitud, comanda.coordenades.longitud],
                          icon=folium.Icon(color=comanda.especialitat.color_marcador, icon='home'),
                          popup=f"Comanda {comanda.id} - {comanda.especialitat.especialitat}").add_to(grups_especialitats[comanda.especialitat.especialitat])

        for restaurant in self.restaurants:
            folium.Marker([restaurant.coordenades.latitud, restaurant.coordenades.longitud],
                          icon=folium.Icon(color=restaurant.especialitat.color_marcador, icon='cutlery'),
                          popup=f"Restaurant {restaurant.nom} - {restaurant.especialitat.especialitat}").add_to(grups_especialitats[restaurant.especialitat.especialitat])

        folium.LayerControl().add_to(self.mapa)

        return self.mapa
    
    def afegirRuta(self, coordenades: List[Coordenada], nom: str , color: str) -> None:       
        folium_plugins.AntPath([[coordenada.latitud, coordenada.longitud] for coordenada in coordenades], color=color, weight=2.5, opacity=1, dash_array=[10, 20], delay=800, reverse= False, paused= False, show_popup= False, popup_options= None, tooltip_options= None, name=nom).add_to(self.mapa)

    def save(self, html_file: str = "mapa.html") -> str:
        output_path = os.path.join(self.output_folder, html_file)
        self.mapa.save(output_path)
        return output_path
