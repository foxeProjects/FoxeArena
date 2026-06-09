import pandas as pd
import streamlit as st
from components.styles import PROJECT_ROOT
from data.groups import GROUPS
from data.porra import _safe_int, display_match_date, load_official_results

SONGS_PATH = PROJECT_ROOT / "assets" / "wc-songs.csv"

RECIPES = {
    "Mexico": ["Tacos al pastor", "Pozole", "Chilaquiles", "Mole poblano", "Tamales", "Cochinita pibil", "Elote", "Quesadillas"],
    "Sudafrica": ["Bobotie", "Bunny chow", "Malva pudding", "Boerewors", "Chakalaka", "Biltong", "Potjiekos", "Vetkoek"],
    "Corea del Sur": ["Kimchi jjigae", "Bibimbap", "Bulgogi", "Tteokbokki", "Japchae", "Kimbap", "Samgyeopsal", "Hotteok"],
    "Republica Checa": ["Gulas", "Svíčková", "Trdelník", "Vepřo knedlo zelo", "Bramboráky", "Kulajda", "Smažený sýr", "Koláče"],
    "Canada": ["Poutine", "Tourtiere", "Butter tarts", "Nanaimo bars", "Peameal bacon sandwich", "Split pea soup", "Bannock", "Montreal smoked meat"],
    "Bosnia y Herzegovina": ["Cevapi", "Burek", "Begova corba", "Sogan-dolma", "Klepe", "Bosanski lonac", "Tufahija", "Ustipci"],
    "Catar": ["Machboos", "Harees", "Madrouba", "Thareed", "Balaleet", "Luqaimat", "Saloona", "Khanfaroosh"],
    "Suiza": ["Fondue", "Rosti", "Raclette", "Zurcher geschnetzeltes", "Älplermagronen", "Birchermuesli", "Basler leckerli", "Malakoff"],
    "Brasil": ["Feijoada", "Moqueca", "Pao de queijo", "Coxinha", "Acaraje", "Farofa", "Brigadeiro", "Vatapa"],
    "Marruecos": ["Cuscus", "Tajine", "Pastilla", "Harira", "Zaalouk", "Rfissa", "Mechoui", "Chebakia"],
    "Haiti": ["Griot", "Diri kole ak pwa", "Soup joumou", "Tassot", "Pikliz", "Legim", "Akra", "Pain patate"],
    "Escocia": ["Haggis", "Cullen skink", "Scotch pie", "Cranachan", "Arbroath smokie", "Stovies", "Clootie dumpling", "Tablet"],
    "Estados Unidos": ["Hamburguesa", "Mac and cheese", "Barbecue ribs", "Clam chowder", "Apple pie", "Buffalo wings", "Cornbread", "Jambalaya"],
    "Paraguay": ["Sopa paraguaya", "Chipa guasu", "Mbeju", "Bori bori", "Payagua mascada", "Pastel mandi'o", "Vorí vorí", "Kosereva"],
    "Australia": ["Meat pie", "Chicken parmigiana", "Lamington", "Pavlova", "Barramundi", "Anzac biscuits", "Sausage roll", "Fairy bread"],
    "Turquia": ["Kebap", "Lahmacun", "Manti", "Menemen", "Dolma", "Pide", "Baklava", "Kofte"],
    "Alemania": ["Currywurst", "Sauerbraten", "Bratwurst", "Schnitzel", "Spätzle", "Kartoffelsalat", "Pretzel", "Schwarzwälder kirschtorte"],
    "Curazao": ["Keshi yena", "Stoba", "Funchi", "Pastechi", "Kabritu stoba", "Sopi di piska", "Ayaka", "Bolo pretu"],
    "Costa de Marfil": ["Attieke", "Kedjenou", "Garba", "Aloco", "Foutou banane", "Sauce graine", "Poulet braise", "Placali"],
    "Ecuador": ["Encebollado", "Ceviche ecuatoriano", "Llapingachos", "Fanesca", "Hornado", "Seco de chivo", "Bolon de verde", "Guatita"],
    "Paises Bajos": ["Stroopwafel", "Bitterballen", "Haring", "Erwtensoep", "Poffertjes", "Kapsalon", "Stamppot", "Kroket"],
    "Japon": ["Sushi", "Ramen", "Okonomiyaki", "Takoyaki", "Katsudon", "Tempura", "Yakitori", "Dorayaki"],
    "Suecia": ["Kottbullar", "Gravlax", "Janssons frestelse", "Raggmunk", "Toast Skagen", "Kanelbullar", "Surstromming", "Semla"],
    "Tunez": ["Cuscus tunecino", "Brik", "Lablabi", "Ojja", "Makroudh", "Slata mechouia", "Mloukhia", "Fricassee"],
    "Belgica": ["Moules-frites", "Carbonnade flamande", "Gofres belgas", "Stoemp", "Waterzooi", "Speculoos", "Croquettes aux crevettes", "Chicons au gratin"],
    "Egipto": ["Koshari", "Ful medames", "Molokhia", "Mahshi", "Feteer meshaltet", "Taameya", "Hawawshi", "Umm ali"],
    "Iran": ["Chelo kebab", "Ghormeh sabzi", "Fesenjan", "Tahdig", "Dizi", "Zereshk polo", "Kuku sabzi", "Sholeh zard"],
    "Nueva Zelanda": ["Hangi", "Pavlova", "Meat pie", "Hokey pokey ice cream", "Whitebait fritters", "Rewena bread", "Lolly cake", "Roast lamb"],
    "Espana": ["Tortilla de patatas", "Paella", "Gazpacho", "Croquetas", "Fabada", "Pulpo a feira", "Patatas bravas", "Churros"],
    "Cabo Verde": ["Cachupa", "Pastel com diablo dentro", "Buzio", "Lagostada", "Xerem", "Canja de galinha", "Cuscuz de milho", "Doce de papaya"],
    "Arabia Saudita": ["Kabsa", "Mandi", "Jareesh", "Saleeg", "Mutabbaq", "Haneeth", "Samboosa", "Maamoul"],
    "Uruguay": ["Asado", "Chivito", "Milanesa", "Empanadas", "Pascualina", "Torta frita", "Dulce de leche", "Capeletis a la caruso"],
    "Francia": ["Boeuf bourguignon", "Ratatouille", "Coq au vin", "Quiche lorraine", "Croque monsieur", "Bouillabaisse", "Crepes", "Tarte tatin"],
    "Senegal": ["Thieboudienne", "Yassa poulet", "Mafe", "Pastels", "Domoda", "Fataya", "Lakh", "Thiou"],
    "Irak": ["Masgouf", "Dolma iraqui", "Quzi", "Tashreeb", "Kubba", "Makhlama", "Kleicha", "Tepsi baytinijan"],
    "Noruega": ["Farikal", "Lefse", "Rakfisk", "Kjottkaker", "Brunost", "Smalahove", "Rommegrot", "Krumkake"],
    "Argentina": ["Asado", "Empanadas", "Milanesa", "Locro", "Choripan", "Provoleta", "Humita", "Alfajores"],
    "Argelia": ["Cuscus argelino", "Chakhchoukha", "Rechta", "Mhadjeb", "Dolma", "Tajine zitoune", "Makroud", "Chorba frik"],
    "Austria": ["Wiener schnitzel", "Tafelspitz", "Apfelstrudel", "Sachertorte", "Kaiserschmarrn", "Käsespätzle", "Gulasch", "Knödel"],
    "Jordania": ["Mansaf", "Maqluba", "Musakhan", "Falafel", "Knafeh", "Galayet bandora", "Mujadara", "Zarb"],
    "Portugal": ["Bacalhau a bras", "Francesinha", "Caldo verde", "Pastel de nata", "Bifana", "Arroz de pato", "Cataplana", "Polvo a lagareiro"],
    "R. D. del Congo": ["Moambe", "Fumbwa", "Liboke", "Pondu", "Chikwangue", "Makayabu", "Madesu", "Beignets congolais"],
    "Uzbekistan": ["Plov", "Samsa", "Lagman", "Manti", "Shurpa", "Non", "Chuchvara", "Naryn"],
    "Colombia": ["Bandeja paisa", "Ajiaco", "Arepa", "Sancocho", "Empanadas colombianas", "Lechona", "Pandebono", "Buñuelos"],
    "Inglaterra": ["Fish and chips", "Shepherd's pie", "Sunday roast", "Full English breakfast", "Bangers and mash", "Steak and kidney pie", "Eton mess", "Sticky toffee pudding"],
    "Croacia": ["Peka", "Crni rizot", "Strukli", "Pasticada", "Sarma", "Cevapi", "Fritule", "Brudet"],
    "Ghana": ["Jollof rice", "Waakye", "Fufu", "Banku", "Kelewele", "Red red", "Groundnut soup", "Kenkey"],
    "Panama": ["Sancocho panameno", "Ropa vieja", "Carimanolas", "Hojaldras", "Arroz con pollo", "Tamales panamenos", "Patacones", "Bienmesabe"],
}

DEFAULT_RECIPES = ["Especial local", "Guiso tradicional", "Comida callejera", "Sopa popular", "Parrilla nacional", "Pan tradicional", "Dulce tipico", "Postre nacional"]


def country_slug(country: str) -> str:
    return str(country).strip().lower().replace(".", "").replace(" ", "-")


def all_countries() -> list[str]:
    countries = []
    for group in GROUPS.values():
        for team in group.get("teams", []):
            countries.append(team["name"])
    return countries


def find_country(country: str) -> dict | None:
    requested = str(country).strip().lower()
    requested_slug = country_slug(country)
    for group_letter, group in GROUPS.items():
        for team in group.get("teams", []):
            name = team["name"]
            if name.lower() == requested or country_slug(name) == requested_slug:
                return {"name": name, "flag": team.get("flag", ""), "group": group_letter, "slug": country_slug(name)}
    return None


@st.cache_data(ttl=60)
def load_country_songs() -> pd.DataFrame:
    if not SONGS_PATH.exists():
        return pd.DataFrame(columns=["pais", "song_name", "url"])
    return pd.read_csv(SONGS_PATH).fillna("")


def get_country_song(country: str) -> dict:
    songs = load_country_songs()
    if songs.empty:
        return {"song_name": "", "url": ""}
    rows = songs[songs["pais"].astype(str).str.lower() == str(country).lower()]
    if rows.empty:
        return {"song_name": "", "url": ""}
    row = rows.iloc[0]
    return {"song_name": str(row.get("song_name", "")).strip(), "url": str(row.get("url", "")).strip()}


def get_country_recipes(country: str) -> list[str]:
    return RECIPES.get(country, DEFAULT_RECIPES)


def get_country_matches(country: str) -> list[dict]:
    matches = []
    results_df = load_official_results()
    result_scores = {}
    if not results_df.empty:
        for _, row in results_df.iterrows():
            result_scores[int(row["match_num"])] = (_safe_int(row.get("score1")), _safe_int(row.get("score2")))

    for group_letter, group in GROUPS.items():
        for match in group.get("matches", []):
            if match["team1"] != country and match["team2"] != country:
                continue
            opponent = match["team2"] if match["team1"] == country else match["team1"]
            score1, score2 = result_scores.get(match["match_num"], (None, None))
            matches.append({
                "match_num": match["match_num"],
                "group": group_letter,
                "date": match["date"],
                "team1": match["team1"],
                "team2": match["team2"],
                "opponent": opponent,
                "stadium": match["stadium"],
                "score1": score1,
                "score2": score2,
                "is_group_match": True,
            })
    if not results_df.empty:
        existing = {match["match_num"] for match in matches}
        excluded = {"1O GRUPO", "2O GRUPO", "MEJOR 3O", "PODIO", "BONUS"}
        requested = str(country).strip().lower()
        for _, row in results_df.iterrows():
            match_num = _safe_int(row.get("match_num"))
            group = str(row.get("group", "")).strip()
            group_key = group.upper()
            team1 = str(row.get("team1", "")).strip()
            team2 = str(row.get("team2", "")).strip()
            if match_num is None or match_num in existing or group_key in excluded:
                continue
            if team1.lower() != requested and team2.lower() != requested:
                continue
            score1 = "" if pd.isna(row.get("score1")) else str(row.get("score1", "")).strip()
            opponent = team2 if team1.lower() == requested else team1
            matches.append({
                "match_num": match_num,
                "group": group,
                "date": display_match_date(match_num, row.get("date", "")),
                "team1": team1,
                "team2": team2,
                "opponent": opponent,
                "stadium": "",
                "score1": score1 if score1 else None,
                "score2": None,
                "is_group_match": False,
            })
    return sorted(matches, key=lambda item: item["match_num"])
