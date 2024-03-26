import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cleaning_functions as cf
from unidecode import unidecode

def get_vintage(x):
    try: 
        if int(x[-4:]) in range(1800, 2025):
            return str(x[-4:])
    except ValueError:
        return np.nan

def uniform_strings(x): 
    '''
    Removes accents, removed all non-alphanumeric characters, outputs new string in title case
    '''
    x = unidecode(x).lower()
    output_string = ''
    for char in x: 
        if char.isspace() == True:
            output_string += char
        elif char.isalnum() == True:
            output_string += char
    output_string = re.sub(' +', ' ', output_string)
    return output_string.title().strip()

def remove_accents(x):
    return unidecode(x)

def get_wine_variety(x):
    x = x.lower()
    try: 
        if 'red' in x: 
            return 'red'
        elif 'white' in x: 
            return 'white'
        elif 'ros' in x or 'pink' in x:
            return 'rose'
        elif 'sparkling'  in x or 'champagne' in x or 'prosecco' in x or 'espumante' in x:
            return 'sparkling'
        else:
            return 'other'
    except:
        return 'error parsing' 

def get_region(country):
    # Extract region name from country column.
    from_index = country.lower().find('from')
    comma_index = country.find(',')
    if from_index!= -1 and comma_index!= -1:
        return country[from_index+5:comma_index]
    elif from_index!= -1:
        return country[from_index+5:]
    else:
        return 'unknown'


def get_country(country):
    # Extract country name from wine name columns.
    comma_index = country.find(',')
    if comma_index == -1:
        return 'unknown'
    else:
        return country.split(", ")[-1]
    

def get_grape_1(x):
    # Isolate grape varieties from countrys column 
    from_index = x.lower().find(' from')
    return x[:from_index]

def extract_string(input_str, string_list):
    input_str_list = input_str.split()
    for string in string_list:
        if string == input_str_list[-1]:
            return string.strip()
        else:
            string = string + ' ' 
            if string in input_str:
                return string.strip()
    return 'review'

def remove_varietal(x, varietals):
    '''
    Removes varietal name it finds + year (4 digits) and returns cleaned and capitalised producer name.
    Returns 'review' if no varietal is found.
    '''
    original_x = x  # Store original input for comparison
    x = cf.uniform_strings(x).strip().lower()
    varietals_to_extract = [varietal for varietal in varietals if varietal in x]
    count = 0
    for i in range(0, len(varietals_to_extract)):
        for varietal in varietals_to_extract:
            # if year still in the string
            if re.search(rf'{varietal}\s\w*\s\d{{4}}', x)!= None:
                x = re.sub(rf'{varietal}\s\w*\s\d{{4}}\w*','', x)
                count += 1

            elif re.search(rf'\d{{4}}', x) != None:
                # replace varietal names and years
                x = re.sub(rf'{varietal}\s\d{{4}}\w*', '', x)
                count += 1
            
            else: # replace varietal name only 
                x = re.sub(rf'{varietal}', '', x)
                count += 1
        
    if x == cf.uniform_strings(original_x).strip().lower() or len(varietals_to_extract) == 0:
        # if no changes were made to x
        return 'review' 
    else:
        # return cleaned and capitalised producer name
        return ' '.join(word.title() for word in x.split()).strip()
    

def get_dirty_producer(x):
    prepositions = ['of', 'de', 'la', 'di', 'qua', 'du', 'non', 'do', 'des', 'a', 'the', 'et', 'and', 'le', 
                    'del', 'dei', 'les', 'jean', 'al', 'da', 'dos', 'il', 'by', 'el', '&', 'i', 'el', 'de', 'y']
    x_words = x.split(' ')
    if x_words[1].lower() in prepositions:
        if x_words[2].lower() in prepositions:
            if x_words[3].lower() in prepositions:
                producer = x_words[0] + ' ' + x_words[1] + ' ' + x_words[2] + ' ' + x_words[3] + ' ' + x_words[4]
                return producer
            else:
                producer = x_words[0] + ' ' + x_words[1] + ' ' + x_words[2] + ' ' + x_words[3]
            return producer
        else:
            producer = x_words[0] +' ' + x_words[1] +' ' + x_words[2]
            return producer
    else:
        producer = x_words[0] + ' ' + x_words[1]
        return producer


def combine_methods(df):
    if df['producer_clean'] != 'review':
        return df['producer_clean']
    elif df['producer_varietal_removed']!= 'review' and df['producer_varietal_removed']!= '':
        return df['producer_varietal_removed']
    else:
        return df['producer_dirty']


def extract_varietal(input_str, varietal_list):
    varietal_list_lower = [i.lower() for i in varietal_list]
    output = ''
    matched_varietal =  [item for item in varietal_list_lower if item in input_str.lower()]
    for grape in matched_varietal:
        output += grape.strip() + ' '
        return cf.uniform_strings(output.strip())
    return 'unknown'


def get_grape_2(x):
    # Isolate grape varieties from countrys column using year and '- '
    x_year_removed = re.sub(rf'(19|20)[0-9][0-9]', '', x)
    output = x_year_removed
    if x == output: 
        return 'unknown'
    else:
        return output


# Lists
    


us_states = (
    'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware',
    'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky',
    'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri',
    'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina',
    'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota',
    'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming'
)

custom_producer_list = ['Veuve Clicquot', 'Verite', 'Altar Uco Edad Media', 
                        'Alex Gambal', 'Amapola Creek', 'Alex Foillard', 'Abbona', 
                        'Agricola De Borja Vina', 'Alain Chavy', 'Anne Pichon Sauvage', 
                        'Adamvs', 'Altos Las Hormigas ', 'Anne Amie', 'Altano', 'Alpha Omega', 
                        'Albert Boxler Edelswicker','Abreu Vineyards', 'Adriano Marco', 'Alvaro Castro Dac', 
                        'Alberto Longo', 'Ameztoi', '12 Linajes', 'Ancient Peaks', 
                        'Alessandro Gian Natale', 'Alma Negra M', '4 Kilos', 'Alphonse Mellot', 
                        'Alpha Box Dice', 'Alheit','Acinum', "1000 Stories","Fontanafredda","Fonterenza",
                        "Fonseca","Firestone","Firesteed","Gabrielskloof","Frescobaldi","Sandeman", "Samsara",
                        "Sena","Selbach","Ravines","Dugatpy", "Dows Vale", "Dows", "Sine Qua Non","Saxum","Querciabella",
                        "Gabrielskloof", "Vanderpump", "Marchandtawse","Lafargevial","Grahams","Danjeanberthoux","Cosentino", 
                        "Argentiera",   "Broadbent","Valdespino","Simonnetfebvre","Pellegrino","Ovid","Laurentperrier","Caposaldo",
                        "Broadbent", "Vivaltus","Popup Piperheidsieck","Morey-Coffinet","montirius","Marchesi","Lustau","Jansz",
                        "Guigal","e Guigal","Cockburns","Chesterkidder","Cignale","Brocard", "Timeless","Monocle","Leviathan",
                        "Gordo","Goutorbe","Futo","Episode","Croft","Cazals","caro","Calma", "Caiarossa", 
                        "Matchbook Estate","Masut Estate Vineyard","Matanzas Creek","00 Wines","Valiano","Semeli","Sclavos","Saggi",
                        "Nortico","Milenrama", "1924", "Viticcio", "Vinum Cellars", "Vivera", "Vins El Cep", "Vinos De Arganza", 
                        "Vinicola Serena Luca Paretti", "Vineyard 29", "Vincent Paris", "Vina Ventisquero", 
                        "Vina Tarapaca", "Vina Robles", "Vina Maitia", "Vina Alicia", "Vilmart Cie", 
                        "Villota", "Villa Wolf Pfalz", "Villadoria", "Villa Jolanda", "Vignoble Du Reveur", 
                        "Vigneti Vecchio", "Vigneti Massa", "Vigneti Del Sole", "Vigne Rada", 
                        "Vignai Da Duline", "Vigilance", "Vie Di Romans", "Vidalfleury", "Mollydooker", 
                        "Veuve Fourny Et Fils", "Veuve Ambal", "Verbena", "Venturini Baldini", "Vandal Gonzo", 
                        "Van Zellers", "Van Duzer", "Valravn", "Valley Vineyards", "Valley Of The Moon", 
                        "Valle Dellacate", "Val Di Toro", "Val De Mer By Patrick Piuze", "Unico Zelo", "ladoucette", 
                        "Tyler Winery", "Turnbull", "Troupis Winery", "Trig Point", "Trentadue", "Trefethen", 
                        "Toscolo Chianti", "Tornatore", "Tomaiolo Chianti", "Toad Hollow", "Tincan", "Tim Smith", 
                        "Tikal", "Tiamo", "Thistledown", "Thierry Germain", "The Winners", "The Winery Of Good Hope", 
                        "The Vice", "The Terraces", "The Hilt", "The Federalist", "The Dreaming Tree", "The Crusher", 
                        "The Chook", "The Calling", "The Boneline", "Textbook", "Teutonic", "Terrunyo", 
                        "Terroir Al Limit", "Terra Doro", "Terra Costantino", "Terlato Family Vineyards", "Terlan", 
                        "Teperberg", "Tenuta Sette", "Tenuta Santanna", "Tenuta Di Valgiano", "Tenuta Di Trinoro", 
                        "Tenuta Di Arceno", "Tenet The", "Te Pa Wines", "Taylor Fladgate", "Tatomer", "Tascante", 
                        "Tangley Oaks", "Tangent", "Talley", "Taittinger", "Tait", "Taft Street", 
                        "Tabarrini", "T Berkley", "Szigeti", "Sybille Kuntz", "Swanson", 
                        "Sur De Los Andes", "Summerland", "Suavia", "Strub Niersteiner", "Stonestreet", "Stolpman Vineyards", 
                        "Stoller", "Stewart", "Sterling", "Stephane Coquillette", "Stella Rosa", 
                        "mollydooker", "Steele", "Stave Steel", "Starborough", "Stanton Vineyards", 
                        "Standing Stone Vineyards", "Stags Leap", "Staglin", "St Supery Dollarhide", 
                        "St Innocent", "St Francis", "St Huberts", "Spy Valley", "Spring Valley", 
                        "Spring Mountain", "Source Sink", "Sonomacutrer", "Sommariva", "Somerston", 
                        "Somek Estate", "Solena Estate", "Sokol Blosser", "Snowden", "Smoking Loon", 
                        "Smith Woodhouse", "Smith Hook", "Small Vines", "Small Gully", "Skouras", 
                        "Sixto", "Six Sigma Ranch", "Sisters Run", "Simi", "Silver", "Siglo", 
                        "Sigalas", "Sierra De Tolono", "Sierra De La Demanda", "Siduri", "Shinas Estate", 
                        "Sheridan Vineyard", "Shaya", "Shaw Smith",     "Shannon Ridge", "Sextant", "Seven Hills Winery", "Sesti", "Seresin", 
                        "Serego Alighieri", "Sequoia Grove", "Sella", "Segals", "Secret Indulgence", 
                        "Secret Door", "Sebastiani North Coast", "Sean Minor", "Scribe", "Scotto Family Cellars", 
                        "Scott Harvey", "Schramsberg", "Schrader", "Schooner By Caymus", "Scholium Project", 
                        "Schlossgut Diel", "Schloss Vollrads", "Schloss Lieser", "Scharffenberger", "Schafrohlich", 
                        "Schaferfrohlich", "Scatte Peaks", "Scarpetta", "Scarecrow", "Scaia", 
                        "Savage", "Sauvion", "Sartarelli", "Santa Julia", "Santa Barbara Winery", 
                        "Sanford", "Sandrone", "Sandhi", "San Simeon", "Salvestrin", 
                        "Saintsbury", "Saints Hills", "Sager", "Sadie Family", "Sa P", 
                        "Ryme Las Brisas", "Ryan Patrick", "Rutini", "Rutherford", "Rui Roboo", 
                        "Ruggeri", "Rudi Pichler", "Routestock", "Round Pond", "Roth Estate", 
                        "Rotem Mounir", "Roscato Dolce", "Roots Run Deep", "Root 1", "Ron Rubin", 
                        "Roger Sabon", "Roger Neveu", "Rodney Strong", "Rodano", "Roco", 
                        "Roberto Voerzio", "Roberto Henriquez", "Robert Weil", "Robert Sinskey", "Robert Oatley", 
                        "Robert Foley", "Robert Craig", "Riposte", "Riofavara", "Ridge", "Ricco", "Rhys Vineyards", "Renwood", "Remoissenet", "Relax", "Reira", 
                        "Regaleali", "Recanati", "Rebholz", "Reata", "Realm Cellars", "Raymond", "Raventos", "Raricarano", 
                        "Rare Wine", "Ramon", "Ramey", "Rainer Schnaitmann", "Raen", "Radley Finch", "Racines", 
                        "R Lopez De Heia", "Qupe", "Quivira", "Quilceda Creek", "Quartz Reef", "Quady Vya", 
                        "Pursued By Bear", "Punta Crena", "Psagot", "Prost", "Principe Pallavicini", "Pride Mountain", 
                        "Powell Son", "Porter Creek", "Poppy", "Ponzi", "Pommery", "Pol Roger", "Point Ormond", 
                        "Poggio Anima", "Poderi Vaiot", "Podere Castorani", "Plungerhead Lodi", "Piperheidsieck", 
                        "Piper Sonoma", "Pinol", "Pine Ridge", "Pindar", "Pikes", "Pievalta", "Pietro Caciorgna", 
                        "Pietradolce", "Pierre Sparr", "Pierre Moncuit", "Pierre Gimonnet", "Piedrasassi", "Piattelli", 
                        "Piaggia", "Philipponnat", "Philippe Le Hardi", "Philip Togni", "Phelps Creek", "Pfeffingen", 
                        "Peyrassol", "Pewsey Vale", "Peter Paul", "Peter Michael", "Peter Dipoli", "Perus", "Pertoismoriset", 
                        "Pertinace", "Perrierjouet", "Perez Cruz", "Pepperwood Grove", "Pennerash", "Penley Estate", 
                        "Pellet Estate", "Peju Winery", "Pegaso", "Pedroncelli", "Pederzana", "Pecchenino", "Peay Vineyards", 
                        "Paxton Vineyards", "Paumanok", "Paula Kornell", "Paul Lato", "Paul K Et Fils", "Paul Cheneau", 
                        "Paul Bara", "Passopisciaro", "Pasqua", "Pascal Jolivet", "Parras Vinhos", "Parducci", 
                        "Paolo Conterno", "Panther Creek", "Palmina", "Palladio", "Pali Wine Co", "Palazzone", "Palazzo", 
                        "Pala", "Paitin", "Pahlmeyer", "Pacific Rim", "Oyster Bay", "Owen Roe", "Outpost", "Otuwhero Estates", 
                        "Oshaughnessy Howell", "Oro Bello", "One Stone Cellars", "Onehope", "Ochota Barrels", "Numanthia",  "Notorious Wines", "North By Northwest", "Nomine Renard", "No Girls", "Nino Franco", 
                        "Niner", "Nine", "Nikolaihof", "Nieto Senetiner", "Nicolasjay", "Nicolas Ulacia", 
                        "Nicolas Feuillatte", "Nickel Nickel", "Neyers", "Newton", "Newt Cellars", "Neudorf", 
                        "Natures Revenge", "My Favorite Neighbor", "Murphygoode", "Mumm", "Mullineux Family", 
                        "Mullercatoir", "Movia", "Moutard", "Mount Peak", "Mount Eden Vineyards", "Moulin De Gassac", 
                        "Mosquita Muerta", "Morlet", "Morgan", "Moorooduc Estate", "Montinore Estate", "Monticello", 
                        "Montecariano", "Monte Rio", "Montaribaldi", "Mongeardmugneret", "Monchhof", "Mommessin", 
                        "Moet Chandon", "Mocali", "Miraval", "Mirabeau", "Mionetto", "Ministry Of Vinterior", 
                        "Miner Family", "Milbrandt", "Middle Sister", "Michel Quenard", "Michel Men", "Michael Pzan", 
                        "Meyernakel", "Meurgeycroses", "Mettler Family Vineyards", "Merryvale", "Mercat", "Mer Soleil", 
                        "Menage A", "Melville", "Meadowcroft", "Mcmanis Family Vineyards",
                        "Mcguigan Wines", "Mcbride Sisters", "Maxville", "Mauritson", "Maurin", "Matthiasson", 
                        "Matthews Winery", "Matthew Fritz", "Mathilde Chapoutier De Provence", "Matchbook", 
                        "Massolino", "Masseria", "Massaya", "Mas De Gourgonnier", "Martini Rossi", "Martin Ray", 
                        "Marquis De La Tour", "Markus Huber", "Mark West", "Mark Ryan", "Maritana Vineyards", 
                        "Marietta Cellars", "Mariepierre Manciat", "Marcassin Marcassin", "Marcel Deiss", "Marc Hebrart", 
                        "Mapreco Vinho", "Manuel Acha Vino", "Mancino", "Maison Noir", "Maison Leroy", "Maison De Montille", 
                        "Maison Brotte", "Maggy Hawk", "Macrostie", "Macanita", "Mac Forbes", "Lynmar Winery", 
                        "Lve By John Legend", "Lusine", "Lunelli", "Luiano Chianti", "Lucien Albrecht", "Luc Belaire", 
                        "Lubanzi", "Louis Roederer", "Louis Martini", "Loosen Bros Dr L", "Long Meadow", "Lombardini Reggiano", 
                        "Lola Wines", "Lokoya", "Lofi Wines", "Locations By Dave", "Lobo Wines", "Llopart", 
                        "Livio Sassetti", "Liquid Farm", "Lionel Faury", "Lioco Sonoma", "Lindquist", "Ligniermichelot", 
                        "Lieb Cellars", "Levy Mcclellan", "Leon Beyer", "Leo Steen", "Lemelson", "Leeuwin Estate", "Lecole 41",
                        "Lecheneaut", "Le Vigne", "Le Rocher", "Le Potazzine", "Le Grand Courtage", "Layer Cake", 
                        "Laurenz V", "Laurent Fayolle", "Laurel Glen", "Larmandierbernier", "Larkmead", "Lapostolle", 
                        "Lanson Le", "Lange Winery", "Landmark", "Lamberti", "Lambert De Seyssel", "Lallier", 
                        "Lake Sonoma Winery", "Laherte Freres", "Lagarde", "Lagar Da Condesa", "Ladeiras Do Xil", 
                        "La Valentina", "La Serena", "La Posta", "La Playa Estate", "La Pivon", "La Marca Di San Michele", 
                        "La Lecciaia", "La Gioiosa", "La Follette", "La Crema", "La Celia", "L10 By Valentin Bianchi", 
                        "Kylie Minogue", "L Aubry Fils", "Kumeu River", "Kuleto Estate", "Kuentzbas", "Krugerrumpf", 
                        "Krugerpf", "Krug", "Koyle", "Tuck Beckstof", "Tres Sabores", "The Withers", "Koyle", 
                        "Koutsoyannopoulos", "Korbel", "Klinker Brick", "Kiryianni", "Kingston Family", "King Estate", 
                        "Kerr Cellars", "Kenwood", "Ken Wright Cellars", "Ken Forrester", "Kelby James Russell", 
                        "Keever Vineyards And Winery", "Keenan", "Keep", "Karthauserhof", "Karatta", "Kapcsandy Family", 
                        "Kamen Estate", "Kaesler", "Justin", "Juggernaut", "Joyce Vineyards", "Josh Cellars", "Joseph Swan", "Joseph Cattin", "Joseph Carr", 
                        "Jose Antonio", "Joostenberg", "John Duval", "Joel Gott", "Joao Portugal Ramos", 
                        "Jk Carriere", "Jj P Zeltinger", "Jj P Wehlener", "Jj P Graacher Himmelreich", 
                        "Jj P Bernkasteler", "Jim Barry", "Jeff Cohn Cellars", "Jeaunauxrobin", "Jeanpaul", 
                        "Jeanmaurice Raffault", "Jeanmarc Vincent", "Jeanluc Eric", "Jeanluc Colombo", 
                        "Jeanlouis Chave", "Jeanclaude Boisset", "Jeanbaptiste Adam", "Jean Pabiot", 
                        "Jean Laurent", "Jcb No", "Jax Vineyards", "Jaume Serra", "Januik Winery", 
                        "Jamieson Ranch Vineyards", "Jam Jar", "Jam Cellars", "Jacquesson", "Jacques Prieur", 
                        "Jacobs Creek", "J Vineyards", "J Lohr", "J Lassalle P", "J Christopher", "Isa And Pierre Clement", "Ironstone", 
                        "Iron Horse", "Innocent Bystander", "Ink Grade", "Infine 1939", "Inama", 
                        "Immichbatterieberg", "Illuminati", "Illahe Vineyards And Winery", "Il Poggione", "Il Palagio", 
                        "Il Molino", "Idlewild", "Hyland Estates Old Vine", "Hund Acre", "Howard Park", 
                        "Hourglass", "Horsepower Vineyards", "Hook And Ladder", "Hobo Wine", "Hobnob", 
                        "Highway 12", "High Note", "Hickinbotham", "Hexamer", "Hewitson", 
                        "Hestan Vineyards", "Hess", "Hermann J Wiemer", "Henriot", "Henri Dosnon", 
                        "Henri Champliau", "Henri Bourgeois", "Hendry", "Heitz Cellar", "Heidi Schrock", 
                        "Hearst Ranch", "Hatzidakis", "Hartford Court", "Harlan", "Hands", 
                        "Hamilton Russell", "Hamel", "Hall", "Hagafen", "Gustave Lorentz", "Gusbourne", "Gundlach Bundschu", "Gunderloch", "Guido Porro", 
                        "Gruet", "Grounded Wine Co", "Grosset", "Grgich Hills Estate", "Greg Norman Estates", 
                        "Green Chiles", "Granbazan Etiqueta", "Gran Moraine", "Gramercy Cellars", "Graham Beck", 
                        "Grace Family", "Gota Wines", "Gonzalez Byass", "Gonetmedeville", "Goldschmidt Vineyard", 
                        "Glos", "Giovanni", "Gilgal", "Gilbert", "Gianni", 
                        "Giacomo", "Ghostwriter", "Ghost", "Ghettina Franciacorta", "Georges Vernay", 
                        "Georg Breuer", "Geoffroy", "Gemstone Vineyard", "Gehricke", "Gaston Chiquet", 
                        "Gazela Vinho", "Gary Farrell", "Garciarevalo", "Garage Project", "Gamble Family Vineyards", 
                        "Gaia", "Frogs Leap", "Frias Family", "Frey", "Frei Brothers", "Freemark Abbey",
                        "Francois Roussetmartin", "Francois Pinon", "Francois Montand", "Francois Labet", 
                        "Francois Ducrot", "Francois Chidaine", "Four Vines", "Fowles Wine", "Forlorn Hope", 
                        "Forjas Del Salnes", "Forge Cellars", "Force Majeure", "Folk Machine", "Fleury Estate Winery", 
                        "Fleur De California", "Five Vintners", "Fisher Vineyards", "First Drop Mothers", "First Creek", 
                        "Fiorini", "Finca El Origen", "Finca Decero", "Finca Abril", "Filippo Grasso", "Figuiere", 
                        "Figgins", "Feudo Montoni", "Feudo Di Santa", "Fess Parker", "Faustino", 
                        "Fattoria Moretto", "Fattoria Del Cerro", "Fattoria Dianella", "Fattoria La Fiorita", "Far Niente", 
                        "Far Mountain", "Fantinel", "Fantesca", "Familia Traversa", "Familia Schroeder", 
                        "Familia Montana", "Familia Mayol", "Familia Cassone", "Fairchild", "Failla", "Eyrie",
                        "Evening Land Seven Springs", "Eva Fricke", "Etchart", "Esk Valley", "Ernest Vineyards", 
                        "Eric Texier", "Eric Chevalier", "Eppa Suprafruta", "Enroute Winery", "Empire Estate", 
                        "Emmerich Knoll", "Emmanuel Giboulot", "Emblem By Michael Mondavi", "Elouan", "Elk Cove", 
                        "Elderton", "Eisele Vineyard", "Edmunds St John", "Eden Rift", "Edaphos", 
                        "Echeverria", "E Pira", "Duvalleroy", "Duttongoldld", "Durigutti", 
                        "Dupuis", "Duo Tons De Duo", "Dunham Cellars", "Dumol", "Duemani", 
                        "Duckhorn", "Dry River Wines", "Dry Creek", "Drappier", "Dr Loosen", 
                        "Dr Konstantin", "Dr Hermann", "Dourthe La Grande", "Dora Di Paolo", "Dopff Irion", 
                        "Donnhoff", "Donnachiara", "Donati Family", "Domaine Ponsot", "Domaine Weinbach", 
                        "Domaine Thibault", "Domaine Tatsis", "Domaine Salvard", 
                        "Domaine Saint", "Domaine Roulot", "Domaine Rollin", "Domaine Rolet", "Domaine Robert", 
                        "Domaine Ponsot", "Domaine Pierre", "Domaine Pelaquie", "Domaine Paul", "Domaine Nicolas", 
                        "Domaine Parent", "Domaine Nico", "Domaine Leseurre", "Domaine Les Aphillanthes", 
                        "Domaine Laroche", "Domaine Lafond", "Domaine Jeancharles", "Domaine Jean Vullien", 
                        "Domaine Hubert", "Domaine Guillotbroux", "Domaine Goisot", "Domaine Glinavos", 
                        "Domaine Giraud", "Domaine Gerard", "Domaine Francois", "Domaine Font Du Vent", 
                        "Domaine Felettig", "Domaine Eugene Carrel Fils", "Domaine Du Pere", "Domaine Dirlercade", 
                        "Domaine De Villaine", "Domaine De Piaugier", "Domaine De Marcoux", "Domaine De Larlot",
                        "Domaine Dardhuy", "Domaine Comte", "Domaine Claude", "Domaine Chasselay", "Domaine Charles", 
                        "Domaine Chante", "Domaine Bott", "Domaine Bernard", "Doliveira", "Dog Point Vineyard", 
                        "Do Reiro", "Disznoko", "Dirupi", "Dierberg", "Dibon Cava", 
                        "Dfj Vinhos", "Deutz", "Della Vite", "Delinquente", "Delamotte", 
                        "Del Dotto", "Dehours", "Decibel Wines", "Deangelis", "De Wetshof", 
                        "Davis Family Vineyards", "Davis Bynum", "Davide Vignato", "David Franz", "David Arthur", 
                        "Davey Browne", "Dashe", "Darms Lane", "Darioush", "Daou Vineyards", 
                        "Dandelion Vineyards", "Dana Estates", "Damilano", "Cupcake Vineyards", "Cuentavinas", 
                        "Cruse Wine", "Crossbarn", "Crosby", "Crocker Starr", "Cristom", 
                        "Criss Cross", "Creek", "Crazy By Nature", "Cowboy", "Covenant", 
                        "Cousino Macul", "Courbis Cornas", "Coup De Foudre", "Cottanera Etna", "Cosse Et Maisonneuve", 
                        "Corvidae", "Correlation Wine Co", "Cooper Mountain", "Contratto", "Contino", 
                        "Conterno Fantino", "Concha Y Toro", "Concannon", "Comte Armand", "Complant", 
                        "Commanderie", "Colterenzio", "Colpetrone", "Collet", "Colene Clemens", "Colgin", "Col De Salici", "Codorniu", "Cobb Wines", 
                        "Coast Cellars", "Clover Hill", "Clos Saintjean", "Clos Sainte", "Clos Lachance", "Clos Du Val", 
                        "Clos Du Bois", "Clos Des Fous", "Clos De La Tech", "Clos Canarelli", "Clos Bellane", 
                        "Clos Amador", "Cline Ancient", "Cleto Chiarli", "Clay Shannon", "Clarendelle", "Cipresso 43", 
                        "Cigliuti", "Cic Cellars", "Christophe Mittnacht", "Chris Ringland", "Cherry Pie", 
                        "Chateau Tertre", "Chateau Tanunda Grand Barossa", "Chateau Rayas", "Chateau Hautblanville", 
                        "Chateau Fontanes", "Chateau De Rouanne", "Chateau De Plaisance", "Chateau De Lescarelle", 
                        "Chateau De La Maltroye", "Chateau De Fontenille", "Charlotte Dalton", "Charles Krug", 
                        "Charles Heidsieck", "Charles Ellner", "Charles De E", "Charles De Cazanove", "Chapter 24", 
                        "Chappellet", "Chapel Hill", "Chan De Rosas", "Champalou Vouvray", "Champagne Telmont", 
                        "Champagne Ployezjacquemart", "Champagne Palmer", "Champagne Mouzonleroux", 
                        "Champagne Legras Haas", "Champagne Leclerc Briant", "Champagne Le Mesnil De S Grand Cru", 
                        "Champagne Jl Vergnon", "Champagne Henri Giraud", "Champagne Doyard", "Champagne Bernard Remy", 
                        "Champagne Barons De Rothschild", "Champagne Agrapart Fils", "Chamisal Vineyards", "Cesconi", "Certosa Di Belriguardo", 
                        "Cerbaiona", "Caymus Suisun", "Caves Sao Joao", "Caves Roger Goulart", "Cave De Ribeauville", 
                        "Cavallotto", "Catherine Pierre", "Cataldi Madonna", "Castoro Cellars", "Castle Rock", 
                        "Castello Di Volpaia", "Castello Di Querceto", "Castello Di Neive", "Castello Di Meleto", 
                        "Castello Di Luzzano", "Castello Di Bossi", "Castagnoli Chianti", "Case Paolin", 
                        "Casanuova Delle", "Casa Smith", "Carpineto Chianti", "Carol Shelton", "Carneros", 
                        "Carmel Road", "Cardedu", "Cantine Maschio", "Cantine Lunae", "Cantine Elvio", 
                        "Cantine Cavicchioli", "Candoni", "Can Verdura", "Campriano Chianti", "Cambria", 
                        "Cakebread", "Cafe De Paris", "Ca Momi", "Ca Furlan", "Burklinwolf", "Bucklin Old Hill Ranch", 
                        "Bryn Mawr Vineyards",  "Brundlmayer", "Bruna Grimaldi", "Browne Family Vineyards", "Brown Estate", "Brotherhood", 
                        "Broadside", "Brittan", "Breathless", "Bread Butter", "Branson Coach House Coach House", 
                        "Brancott", "Boyermartenot", "Bouvet", "Boundary Breaks", "Bouchard", 
                        "Bouchaine", "Botromagno", "Botanica Wines", "Borgo Conventi", "Bonny Doon", 
                        "Bollinger", "Bodini", "Bodegas Virgen Del Galir", "Bodegas Vatan Nisia", "Bodegas Ugalde", 
                        "Bodegas Santalba", "Bodegas Renacer", "Bodegas Ramirez", "Bodegas Poniente", "Bodegas Nando Rez De Ganuza", 
                        "Bodega Pablo Fallabrino", "Bodega Noemia De Patagonia", "Bodega Monteviejo", "Bodega Malma", 
                        "Bodega Aniello", "Blue Rock", "Blandys 5", "Blackbird Vineyards", "Black Sheep", 
                        "Black Estate", "Bindi Wines", "Billecartsalmon",  "Bilahaut By Michel", "Big Smooth", "Big Basin", "Bieler Pere", "Bevan Cellars", 
                        "Bethel Heights", "Bests Great Western", "Besserat De Fon", "Berton Vineyards Metal Label", "Berlucchi", 
                        "Benziger", "Benovia Russian River", "Benjamin Romeo", "Bench Sonoma", "Bellissima", 
                        "Bellafina", "Bella Grace", "Beeslaar", "Bedrock Wine", "Beckmen", 
                        "Becklyn", "Beaux Freres", "Beaumont", "Beaulieu Vineyard", "Beau Joie", 
                        "Bastianich", "Bassermannjordan", "Barton Guestier", "Bartenura", "Barone Pizzini", 
                        "Barnard Griffin", "Barkan", "Baricci Colombaio", "Barboursville", "Banshee Sonoma", 
                        "Balletto Winery", "Baillylapierre", "Badia A Coltibuono", "Bacio Divino", "Azienda Agricola", 
                        "Azelia", "Ayres", "Avinyo", "Avaline", "Austin", 
                        "Au Contraire", "Au Bon Climat", "Astrolabe", "Ashes & Diamonds",  "Artesa", "Arrowood", "Arnot", "Arnaldo Caprai", "Armand De Brignac", "Arista Winery", "Arietta", 
                        "Argyros", "Argyle", "Aresti", "Archery Summit", "Ar Pe", "Ar Lenoble", "Anwilka", "Antucura", 
                        "Antica", "Anthony Road", "Anthill Farms", "Annabella", "Animo By Michael Mondavi", "Angels & Cowboys", 
                        "Angeline", "Anakota Helena", "Amici", "Alvaro", "Altar Uco", "Alpha Estate", "Alma Rosa", 
                        "Alkoomi", "Alfo Bertolani", "Alexander", "Alexana Terroir", "Albert Boxler", "Alberico", "Alban", 
                        "Aj Adam D", "Agusti Torello", "Agua De Piedra", "Agricola De Borja", "Adobe Road", "Adelsheim", 
                        "Adelina Wines", "Accendo Cellars", "Abbona", "Abbazia Di Novacella", "A Tribute To Grace", "A To Z", 
                        "1849", "7 Deadly",     "Agricola De Borja", "Albert Boxler", "Alfo Bertolani", "Alma Negra", "Alta Luna", 
                        "Altar Uco", "Ampelos Cellars", "Arnot", "Annabella", "Antinori", 
                        "Apaltagua", "Apothic", "Aquinas", "Argiano", "Argento", 
                        "Argentiera", "Argiolas", "Argyle", "Argyros", "Arietta", 
                        "Arnotroberts", "Arrowood", "Artadi", "Artesa", "Artuke", 
                        "Arzuaga", "Astrolabe", "Atalaya", "Auspicion", "Avaline", 
                        "Avalon", "Avignonesi", "Avinyo", "Abbotts Delaunay", "Vina Alarde", 
                        "Marques De Murrieta", "Definition", "Bodegas Hidalgo Triana",
                        "Ammazza", "Jackson Estate", "Vina Vik", "V8", "Tuck Beckstof",
                        "Terroir Al Limit", "Terora Di Paolo", "Tenshen", "Tenet",
                        "Tania Et Vincent", "Tamber Bey", 
                        "Scatte Peaks", "Salvatore Molettieri", "Rutherford",
                        "Rui Roboo Madeira", "Ruca Malen", "Round Pond", "Roscato Dolce",
                        "Rombauer", "Robert Mondavi", "Rivetto", "Ferreira", "Raricarano",
                        "R Lopez De Heia", "Quinta Do Noval", "Quinta De La Rosa",
                        "Quinta De Chocapalha", "Quinta Da Pellada", "Prayers Of Sinners",
                        "Paul K Et Fils", "Ostertag", "Once Future", "Murgo", "Montsarra",
                        "Monte Bernardi", "Meyerfonne", "Mathilde Chapoutier De Provence",
                        "Markham", "Marcassin", "Malacara", "Maison Lenvoye", "Macari",
                        "Luca", "Lofi", "Lisini", "Lini 910", "Lecole", "Le Cadeau Vineyard",
                        "Lavau", "Kinsella Estates", "Joseph Phelps", "Jonata", "Jermann",
                        "Isa And Pierre Clement", "Inglenook", "Hund Acre", "Hosmer Winery",
                        "Heritage School Vineyards", "Heritance", "Heinz Eifel", "Hamilton Russell",
                        "Gualdo Del Re", "Grossot", "Green Chiles", "Gran Sasso",
                        "Giuliano Rosati", "Ghettina Franciacorta", "Fritz Haag",
                        "Francoise Savignylesbeaune", "Enrique Foster", "Duttongoldld",
                        "Duo Tons De Duo", "Dr Paulybergweiler", "Dr Stephens Estate",
                        "Douloufakis", "Domaine Zafeirakis", "Davies", "Dalla Valle",
                        "Cuvaison", "Cune", "Clos Henri", "Cic Cellars",
                        "Chateau Maupague De Provence", "Charles De E", "Chandon",
                        "Champagne Le Mesnil De S Grand Cru", "Canardduchene", "Brendel",
                        "Bodegas Nando Rez De Ganuza", "Besserat De Fon", "Berthetbondet Du Jura",
                        "Bergstrom", "Benito Santos", "Azienda Agricola", "Alfo Bertolani",
                        "Albert Boxler", "Aj Adam", "Agricola De Borja", "4 Kilos", 
                        'domaine de la romanée-conti',
                        "Valdo", "Ulysse Collin", "Twenty Bench", "Tropical", "Tilia",
                        "Terroir Al Limit", "Tenet",  "Syltbar",
                        "Sun Goddess By Mary J Blige", "Stags Leap", "Rui", "Ruinart",
                        "Roscato Dolce", "Round Pond", "Rombauer", "Riondo",
                        "Revolution Wine Company", "Tuck Beckstof", "Tenuta Anfosso",
                        "St Supery", "Scatte Peaks", "San Polino", 'Tamarack Cellars', 'Tablas Creek',
                        "Antinori", "Nicolas Reau", "Mount Mary", "Michel Men", "Michael Pzan",
                        "Mathilde Chapoutier", "Mas Champart", "Luna Nuda", "Louis Jadot",
                        "Domaine Des Heritiers Louis Jadot", "La Playa", "Le Roi Des Pierres",
                        "Le Colture", "Le Charmel", "Lang Reed", "La Poderina", "La Marca",
                        "Jeannoel Gagnard", "J Lassalle", "Isa And Pierre Clement", "Il Borro",
                        "Hund Acre", "Hamilton Russell", "Green Chiles", "Gran Passione",
                        "Ghettina Franciacorta", "Fitvine Wine", "Duo Tons De Duo", "Domaine Humbert",
                        "Da Vinci", "Clos Dalian", "Cliff Lede", "Cic Cellars", "Chateau Gazin",
                        "Chateau Bourgneuf", "Chateau Belair", "Chateau Beauchene", "Cedar Salmon",
                        "Casa Vinicola Botter", "Carlo Giacosa", "Brick Mortar", "Booker Vineyard",
                        "Bodegas Nando Rez De Ganuza", "Bisol Jeio", "Barossa Valley", "B Kosuge",
                        "Azienda Agricola", "Alma Negra", "Altar Uco", "Albert Boxler", "4 Kilos",
                        "Domaine De La Bergerie", "Stephane Aviron", "Nicole Chanrion",
                        "Lorgeril Domaine De La Borie Blanche", "Henry Marionnet Domaine De La Charmoise",
                        "Domaine de la Charmoise Touraine", "Domaine De La Vougeraie Vougeot",
                        "Domaine De La Vougeraie Terres", "Domaine De La Vieille Julienne Chateauneufdupape",
                        "Domaine De La Taille Aux Loups", "Domaine De La Romaneeconti",
                        "Domaine De La Prebende", "Domaine De La Pousse Dor", "Domaine De La Pirolette",
                        "Domaine De La Pauline", "Domaine De La Pepiere", "Domaine De La Mordoree",
                        "Domaine De La Guilloterie", "Domaine De La Grandcour Fleurie",
                        "Domaine De La Fruitiere", "Domaine De La Damase",
                        "Domaine De La Charbonniere Chateauneufdupape", "Domaine De La Chanteleuserie Bourgueil",
                        "Domaine De La Chanade", "Domaine De La Cadette Bourgogne",
                        "Domaine De La Cadette", "Domaine De La Bongran Vireclesse",
                        "Domaine De La Bergerie", "Chateau Fuisse Julienas", 'Lail J Daniel',
                        'Domaine De La Rouge'
]

