# MTRFoodDelivery Python Project

## Visió General del Projecte

MTRFoodDelivery és un projecte de simulació basat en Python dissenyat per optimitzar el procés de recollida i lliurament de comandes de menjar des de diversos restaurants a Mataró. L'objectiu és assegurar que el menjar es lliura de manera eficient, complint amb els compromisos de temps específics per a cada tipus de cuina.

## Algoritmes

### Hill Climbing

Aquest algoritme s'utilitza en la funció `omplirMotxilla` per determinar l'ordre de recollida i lliurament de les comandes. L'algoritme selecciona iterativament la comanda amb el compromís de temps més baix fins que s'assoleix la capacitat màxima de la motxilla.

### Best-First Search

Aquest algoritme s'utilitza en les funcions `omplirMotxilla` i `entregarComandes` per determinar la comanda més propera a la ubicació actual entre les comandes de la mateixa especialitat.
L'algoritme itera per les comandes disponibles i calcula la distància entre la ubicació actual i cada comanda.
    
## Estructura del Projecte

El projecte consta dels següents components principals:

1. **Models de Domini**: Defineix entitats bàsiques com `Coordenada`, `Comanda`, `Restaurant` i `MapGenerator`.
2. **Dades**: Conté dades inicials per a comandes (`comandes`), restaurants (`restaurants`), especialitats (`especialitats`) i la ubicació inicial (`tecnocampus`).
3. **Algoritmes**: Implementa la lògica per omplir la motxilla de lliurament (`omplirMotxilla`) i lliurar les comandes (`entregarComandes`).
4. **Execució Principal**: Controla el flux de la simulació, generant mapes i seguint el procés de lliurament.

## Instal·lació

1. Clona el repositori.
2. Assegura't de tenir instal·lat Python 3.7+.
3. Instal·la els paquets necessaris si encara no estan disponibles.

### Creació d'un Entorn Virtual

Per assegurar-te que les dependències del projecte no interfereixin amb altres projectes de Python al teu sistema, es recomana utilitzar un entorn virtual. Segueix aquests passos:

1. **Crea un entorn virtual:**

    ```bash
    python -m venv venv

2. **Activa l'entorn virtual:**

     - A Windows:

         ```bash
         venv\Scripts\activate
         ```

     - A macOS i Linux:

         ```bash
         source venv/bin/activate
         ```

     Un cop activat, l'indicador de la línia de comandes canviarà per indicar que ara estàs treballant dins de l'entorn virtual.

3. **Instal·la els paquets necessaris:**

     Assegura't d'estar a l'arrel del projecte on està ubicat el fitxer `requirements.txt` amb els paquets necessaris llistats. A continuació, executa:

     ```bash
     pip install -r requirements.txt

## Ús

El script principal `delivery_simulation.py` es pot executar amb diversos arguments per personalitzar la simulació:

```bash
python delivery_simulation.py --capacitatMaxima <capacitat_maxima> --no-repetirRestaurants --outputFolder <carpeta> --outputFileName <nom_fitxer>
```

### Arguments

- `--capacitatMaxima`: Capacitat màxima de la motxilla de lliurament (per defecte: 12000 grams).
- `--no-repetirRestaurants`: Si es defineix, els restaurants no poden preparar més d'una comanda (per defecte: False).
- `--outputFolder`: Carpeta on es guardaran els mapes generats (per defecte: "out").
- `--outputFileName`: Nom del fitxer de sortida per al mapa (per defecte: "mapa.html").

## Funcionalitats

### Omplir la Motxilla (`omplirMotxilla`)

Aquesta funció simula el procés d'omplir la motxilla de lliurament amb comandes recollides de restaurants propers basant-se en les següents heurístiques:
- Prioritzar les comandes amb el compromís de temps més alt.
- Seleccionar el restaurant més proper que ofereixi l'especialitat requerida.
- No excedir la capacitat màxima de la motxilla.

**Paràmetres:**
- `inici`: Coordenades d'inici.
- `comandes`: Llista de comandes.
- `capacitatMaxima`: Capacitat màxima de la motxilla.
- `restaurants`: Llista de restaurants disponibles.
- `repetirRestaurants`: Bandera booleana per permetre repetir restaurants.

**Retorna:**
- Llista de comandes a la motxilla, distància total recorreguda, coordenades finals, comandes restants, restaurants restants i la ruta seguida.

### Lliurar Comandes (`entregarComandes`)

Aquesta funció gestiona el lliurament de comandes des de la motxilla, assegurant-se que:
- Les comandes amb el compromís de temps més alt es prioritzen.
- Dins de la mateixa especialitat, es lliura primer la comanda més propera.

**Paràmetres:**
- `inici`: Coordenades d'inici.
- `motxilla`: Llista de comandes a la motxilla pendents de lliurar.

**Retorna:**
- Distància total recorreguda, coordenades finals i la ruta seguida.

## Exemple

Aquí teniu un exemple d'execució de la simulació amb la configuració per defecte:

```bash
python delivery_simulation.py --no-repetirRestaurants
```

En executar-ho, la simulació:
- Omplirà la motxilla amb comandes evitant repetir restaurants.
- Lliurarà les comandes.
- Generarà un mapa inicial.
- Farà un seguiment i imprimirà el procés de recollida i lliurament de comandes.
- Guardarà el mapa final al fitxer de sortida especificat.

## Autors

Aquest projecte va ser desenvolupat per Pol Rubio Borrego i Lea Cornelis Martinez com a part d'una pràctica de grup per al curs "TÈCNIQUES D’INTEL·LIGÈNCIA ARTIFICIAL" al Tecnocampus Mataró. Les contribucions són benvingudes per millorar l'eficiència i la funcionalitat de la simulació.

---

Per a més detalls sobre la implementació del projecte i l'enunciat de la pràctica, consulteu el document [PDF proporcionat](practica2_2024.pdf).
