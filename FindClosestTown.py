from functools import partial
from geopy.geocoders import Nominatim
import pandas as pd
import folium
import numpy as np
import webbrowser
import os
import platform
import subprocess

class FindClosestTown():

    adress : str
    
    def __init__(self, adress : str):
        self.adress = adress 
        self.geolocator = Nominatim(user_agent="ProjDavia")  
        self.geocode = partial(self.geolocator.geocode, language="fr")
        self.location = self.geocode(self.adress)
        self.reverse = partial(self.geolocator.reverse, language="fr")

    def find_closest_town_hall(self):
        town_hall_data = pd.read_csv("data_mairies.csv")
        min_dist2 = np.inf
        for i, (latitude, longitude) in enumerate(zip(town_hall_data['latitude'],town_hall_data['longitude'])):
            if (latitude-self.location.latitude)**2 + (longitude-self.location.longitude)**2 < min_dist2:
                min_dist2 = (latitude-self.location.latitude)**2 + (longitude-self.location.longitude)**2
                minlat = latitude
                minlong = longitude
                index = i
        return (self.reverse(str(minlat) + "," + str(minlong)), town_hall_data.iloc[index])
    
        
    def open_html_in_small_window(file_path, window_width=800, window_height=600):
        """
    Ouvre un fichier HTML existant dans une fenêtre de navigateur de taille réduite.
    
    Parameters:
    - file_path (str): Chemin complet vers le fichier HTML à ouvrir
    - window_width (int): Largeur souhaitée de la fenêtre en pixels (par défaut 800)
    - window_height (int): Hauteur souhaitée de la fenêtre en pixels (par défaut 600)
    """
        # Vérifier que le fichier existe
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"Le fichier {file_path} n'existe pas")
    
        # Construire l'URL du fichier local
        file_url = f"file://{os.path.abspath(file_path)}"
    
        # Systèmes Windows: essayer d'ouvrir avec des paramètres spécifiques
        if platform.system() == 'Windows':
            try:
                # Essayer d'utiliser Microsoft Edge en mode app (plus contrôlable)
                edge_path = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
                if os.path.exists(edge_path):
                    subprocess.Popen([edge_path, "--app=" + file_url, 
                                 f"--window-size={window_width},{window_height}"])
                    return
            except:
                pass
    
        # Sur macOS, on peut utiliser l'option -g pour ouvrir en arrière-plan
        elif platform.system() == 'Darwin':  # macOS
            try:
                subprocess.run(['open', '-a', 'Safari', file_path])
                return
            except:
                pass
    
        # Solution par défaut pour tous les systèmes - ouvre avec le navigateur par défaut
        # (sans contrôle précis de la taille)
        webbrowser.open(file_url)

    

    def find_print_closest_hall(adress : str):
        """
        This function identifies the closest town hall to a given address.

        Function details:
        - **Input**: A string representing the address.
        - **Output**:
            1. **Printed Location**: The address of the closest town hall.
            2. **Saved Map**: A visual map displaying both the input address and the closest town hall.
            3. **Return Values**: 
                - A `geopy.location.Location` object representing the town hall's coordinates.
                - A Pandas Series containing all relevant details about the town hall.
        """
        fct = FindClosestTown(adress)
        cth, column = fct.find_closest_town_hall()
        print("Your adress :", fct.location)
        print("The closest town hall", cth)
        legende_town_hall : str = "\n".join([column['nom'], column['adresse_courriel'], column['website']])
        m = folium.Map((fct.location.latitude,fct.location.longitude), tiles="cartodb positron")
        folium.Marker(
            location=[cth.latitude, cth.longitude],
            tooltip="Mairie",
            popup=legende_town_hall,
            icon=folium.Icon(color="green"),
        ).add_to(m)

        folium.Marker(
            location=[fct.location.latitude, fct.location.longitude],
            tooltip="Votre adresse",
            popup=fct.adress,
            icon=folium.Icon(color="red"),
        ).add_to(m)

        m.fit_bounds([[fct.location.latitude, fct.location.longitude], 
                 [cth.latitude, cth.longitude]])
        
        m.save("map.html")
        FindClosestTown.open_html_in_small_window("map.html", 600, 400)
        return (cth, column)


if __name__ == "__main__":
    FindClosestTown.find_print_closest_hall("93 bis avenue achille peretti")