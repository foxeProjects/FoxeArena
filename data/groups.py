"""
Data module: All 12 World Cup 2026 groups, teams, matches and stadiums.
"""

# ---------------------------------------------------------------------------
# Helper to build a team dict
# ---------------------------------------------------------------------------
def _team(name, flag):
    return {"name": name, "flag": flag, "pts": 0, "pj": 0, "pg": 0, "pe": 0, "pp": 0, "gf": 0, "gc": 0, "dif": 0}

def _match(date, t1, f1, t2, f2, num, stadium):
    return {"date": date, "team1": t1, "flag1": f1, "team2": t2, "flag2": f2, "match_num": num, "stadium": stadium}

# ---------------------------------------------------------------------------
# GROUPS
# ---------------------------------------------------------------------------
GROUPS = {
    "A": {
        "teams": [
            _team("Mexico", "\U0001f1f2\U0001f1fd"),
            _team("Sudafrica", "\U0001f1ff\U0001f1e6"),
            _team("Corea del Sur", "\U0001f1f0\U0001f1f7"),
            _team("Republica Checa", "\U0001f1e8\U0001f1ff"),
        ],
        "matches": [
            _match("11 Jun", "Mexico", "\U0001f1f2\U0001f1fd", "Sudafrica", "\U0001f1ff\U0001f1e6", 1, "Estadio Azteca, Ciudad de Mexico"),
            _match("11 Jun", "Corea del Sur", "\U0001f1f0\U0001f1f7", "Republica Checa", "\U0001f1e8\U0001f1ff", 2, "Estadio Chivas, Guadalajara"),
            _match("18 Jun", "Republica Checa", "\U0001f1e8\U0001f1ff", "Sudafrica", "\U0001f1ff\U0001f1e6", 25, "Mercedes-Benz Stadium, Atlanta"),
            _match("18 Jun", "Mexico", "\U0001f1f2\U0001f1fd", "Corea del Sur", "\U0001f1f0\U0001f1f7", 28, "Estadio Chivas, Guadalajara"),
            _match("24 Jun", "Republica Checa", "\U0001f1e8\U0001f1ff", "Mexico", "\U0001f1f2\U0001f1fd", 53, "Estadio Azteca, Ciudad de Mexico"),
            _match("24 Jun", "Sudafrica", "\U0001f1ff\U0001f1e6", "Corea del Sur", "\U0001f1f0\U0001f1f7", 54, "Estadio BBVA, Monterrey"),
        ],
        "banner": "assets/grupoA/bannerA.png",
        "mascots": {
            "Mexico": "assets/grupoA/mexico.png",
            "Corea del Sur": "assets/grupoA/korea.png",
            "Republica Checa": "assets/grupoA/Chequia.png",
            "Sudafrica": "assets/grupoA/sudafrica.png",
        },
    },
    "B": {
        "teams": [
            _team("Canada", "\U0001f1e8\U0001f1e6"),
            _team("Bosnia y Herzegovina", "\U0001f1e7\U0001f1e6"),
            _team("Catar", "\U0001f1f6\U0001f1e6"),
            _team("Suiza", "\U0001f1e8\U0001f1ed"),
        ],
        "matches": [
            _match("12 Jun", "Canada", "\U0001f1e8\U0001f1e6", "Bosnia y Herzegovina", "\U0001f1e7\U0001f1e6", 3, "Estadio Nacional de Canada, Toronto"),
            _match("13 Jun", "Catar", "\U0001f1f6\U0001f1e6", "Suiza", "\U0001f1e8\U0001f1ed", 8, "Levi's Stadium, San Francisco"),
            _match("18 Jun", "Suiza", "\U0001f1e8\U0001f1ed", "Bosnia y Herzegovina", "\U0001f1e7\U0001f1e6", 26, "SoFi Stadium, Los Angeles"),
            _match("18 Jun", "Canada", "\U0001f1e8\U0001f1e6", "Catar", "\U0001f1f6\U0001f1e6", 27, "Estadio BC Place, Vancouver"),
            _match("24 Jun", "Suiza", "\U0001f1e8\U0001f1ed", "Canada", "\U0001f1e8\U0001f1e6", 51, "Estadio BC Place, Vancouver"),
            _match("24 Jun", "Bosnia y Herzegovina", "\U0001f1e7\U0001f1e6", "Catar", "\U0001f1f6\U0001f1e6", 52, "Lumen Field, Seattle"),
        ],
        "banner": "assets/grupoB/bannerB.png",
        "mascots": {},
    },
    "C": {
        "teams": [
            _team("Brasil", "\U0001f1e7\U0001f1f7"),
            _team("Marruecos", "\U0001f1f2\U0001f1e6"),
            _team("Haiti", "\U0001f1ed\U0001f1f9"),
            _team("Escocia", "\U0001f3f4\U000e0067\U000e0062\U000e0073\U000e0063\U000e0074\U000e007f"),
        ],
        "matches": [
            _match("13 Jun", "Brasil", "\U0001f1e7\U0001f1f7", "Marruecos", "\U0001f1f2\U0001f1e6", 7, "MetLife Stadium, Nueva Jersey"),
            _match("13 Jun", "Haiti", "\U0001f1ed\U0001f1f9", "Escocia", "\U0001f3f4\U000e0067\U000e0062\U000e0073\U000e0063\U000e0074\U000e007f", 5, "Gillette Stadium, Boston"),
            _match("19 Jun", "Brasil", "\U0001f1e7\U0001f1f7", "Haiti", "\U0001f1ed\U0001f1f9", 29, "Lincoln Financial Field, Filadelfia"),
            _match("19 Jun", "Escocia", "\U0001f3f4\U000e0067\U000e0062\U000e0073\U000e0063\U000e0074\U000e007f", "Marruecos", "\U0001f1f2\U0001f1e6", 30, "Gillette Stadium, Boston"),
            _match("24 Jun", "Escocia", "\U0001f3f4\U000e0067\U000e0062\U000e0073\U000e0063\U000e0074\U000e007f", "Brasil", "\U0001f1e7\U0001f1f7", 49, "Hard Rock Stadium, Miami"),
            _match("24 Jun", "Marruecos", "\U0001f1f2\U0001f1e6", "Haiti", "\U0001f1ed\U0001f1f9", 50, "Mercedes-Benz Stadium, Atlanta"),
        ],
        "banner": "assets/grupoC/bannerC.png",
        "mascots": {},
    },
    "D": {
        "teams": [
            _team("Estados Unidos", "\U0001f1fa\U0001f1f8"),
            _team("Paraguay", "\U0001f1f5\U0001f1fe"),
            _team("Australia", "\U0001f1e6\U0001f1fa"),
            _team("Turquia", "\U0001f1f9\U0001f1f7"),
        ],
        "matches": [
            _match("12 Jun", "Estados Unidos", "\U0001f1fa\U0001f1f8", "Paraguay", "\U0001f1f5\U0001f1fe", 4, "SoFi Stadium, Los Angeles"),
            _match("13 Jun", "Australia", "\U0001f1e6\U0001f1fa", "Turquia", "\U0001f1f9\U0001f1f7", 6, "Estadio BC Place, Vancouver"),
            _match("19 Jun", "Turquia", "\U0001f1f9\U0001f1f7", "Paraguay", "\U0001f1f5\U0001f1fe", 31, "Levi's Stadium, San Francisco"),
            _match("19 Jun", "Estados Unidos", "\U0001f1fa\U0001f1f8", "Australia", "\U0001f1e6\U0001f1fa", 32, "Lumen Field, Seattle"),
            _match("25 Jun", "Turquia", "\U0001f1f9\U0001f1f7", "Estados Unidos", "\U0001f1fa\U0001f1f8", 59, "SoFi Stadium, Los Angeles"),
            _match("25 Jun", "Paraguay", "\U0001f1f5\U0001f1fe", "Australia", "\U0001f1e6\U0001f1fa", 60, "Levi's Stadium, San Francisco"),
        ],
        "banner": "assets/grupoD/bannerD.png",
        "mascots": {},
    },
    "E": {
        "teams": [
            _team("Alemania", "\U0001f1e9\U0001f1ea"),
            _team("Curazao", "\U0001f1e8\U0001f1fc"),
            _team("Costa de Marfil", "\U0001f1e8\U0001f1ee"),
            _team("Ecuador", "\U0001f1ea\U0001f1e8"),
        ],
        "matches": [
            _match("14 Jun", "Alemania", "\U0001f1e9\U0001f1ea", "Curazao", "\U0001f1e8\U0001f1fc", 9, "NRG Stadium, Houston"),
            _match("14 Jun", "Costa de Marfil", "\U0001f1e8\U0001f1ee", "Ecuador", "\U0001f1ea\U0001f1e8", 10, "Lincoln Financial Field, Filadelfia"),
            _match("20 Jun", "Alemania", "\U0001f1e9\U0001f1ea", "Costa de Marfil", "\U0001f1e8\U0001f1ee", 33, "BMO Field, Toronto"),
            _match("20 Jun", "Ecuador", "\U0001f1ea\U0001f1e8", "Curazao", "\U0001f1e8\U0001f1fc", 34, "Arrowhead Stadium, Kansas City"),
            _match("25 Jun", "Ecuador", "\U0001f1ea\U0001f1e8", "Alemania", "\U0001f1e9\U0001f1ea", 56, "MetLife Stadium, Nueva Jersey"),
            _match("25 Jun", "Curazao", "\U0001f1e8\U0001f1fc", "Costa de Marfil", "\U0001f1e8\U0001f1ee", 55, "Lincoln Financial Field, Filadelfia"),
        ],
        "banner": "assets/grupoE/bannerE.png",
        "mascots": {},
    },
    "F": {
        "teams": [
            _team("Paises Bajos", "\U0001f1f3\U0001f1f1"),
            _team("Japon", "\U0001f1ef\U0001f1f5"),
            _team("Suecia", "\U0001f1f8\U0001f1ea"),
            _team("Tunez", "\U0001f1f9\U0001f1f3"),
        ],
        "matches": [
            _match("14 Jun", "Paises Bajos", "\U0001f1f3\U0001f1f1", "Japon", "\U0001f1ef\U0001f1f5", 11, "AT&T Stadium, Dallas"),
            _match("14 Jun", "Suecia", "\U0001f1f8\U0001f1ea", "Tunez", "\U0001f1f9\U0001f1f3", 12, "Estadio BBVA, Monterrey"),
            _match("20 Jun", "Paises Bajos", "\U0001f1f3\U0001f1f1", "Suecia", "\U0001f1f8\U0001f1ea", 35, "NRG Stadium, Houston"),
            _match("20 Jun", "Tunez", "\U0001f1f9\U0001f1f3", "Japon", "\U0001f1ef\U0001f1f5", 36, "Estadio BBVA, Monterrey"),
            _match("25 Jun", "Japon", "\U0001f1ef\U0001f1f5", "Suecia", "\U0001f1f8\U0001f1ea", 57, "Arrowhead Stadium, Kansas City"),
            _match("25 Jun", "Tunez", "\U0001f1f9\U0001f1f3", "Paises Bajos", "\U0001f1f3\U0001f1f1", 58, "AT&T Stadium, Dallas"),
        ],
        "banner": "assets/grupoF/bannerF.png",
        "mascots": {},
    },
    "G": {
        "teams": [
            _team("Belgica", "\U0001f1e7\U0001f1ea"),
            _team("Egipto", "\U0001f1ea\U0001f1ec"),
            _team("Iran", "\U0001f1ee\U0001f1f7"),
            _team("Nueva Zelanda", "\U0001f1f3\U0001f1ff"),
        ],
        "matches": [
            _match("15 Jun", "Iran", "\U0001f1ee\U0001f1f7", "Nueva Zelanda", "\U0001f1f3\U0001f1ff", 15, "SoFi Stadium, Los Angeles"),
            _match("15 Jun", "Belgica", "\U0001f1e7\U0001f1ea", "Egipto", "\U0001f1ea\U0001f1ec", 16, "Lumen Field, Seattle"),
            _match("21 Jun", "Belgica", "\U0001f1e7\U0001f1ea", "Iran", "\U0001f1ee\U0001f1f7", 39, "SoFi Stadium, Los Angeles"),
            _match("21 Jun", "Nueva Zelanda", "\U0001f1f3\U0001f1ff", "Egipto", "\U0001f1ea\U0001f1ec", 40, "Estadio BC Place, Vancouver"),
            _match("26 Jun", "Nueva Zelanda", "\U0001f1f3\U0001f1ff", "Belgica", "\U0001f1e7\U0001f1ea", 64, "Estadio BC Place, Vancouver"),
            _match("26 Jun", "Egipto", "\U0001f1ea\U0001f1ec", "Iran", "\U0001f1ee\U0001f1f7", 63, "Lumen Field, Seattle"),
        ],
        "banner": "assets/grupoG/bannerG.png",
        "mascots": {},
    },
    "H": {
        "teams": [
            _team("Espana", "\U0001f1ea\U0001f1f8"),
            _team("Cabo Verde", "\U0001f1e8\U0001f1fb"),
            _team("Arabia Saudita", "\U0001f1f8\U0001f1e6"),
            _team("Uruguay", "\U0001f1fa\U0001f1fe"),
        ],
        "matches": [
            _match("15 Jun", "Espana", "\U0001f1ea\U0001f1f8", "Cabo Verde", "\U0001f1e8\U0001f1fb", 14, "Mercedes-Benz Stadium, Atlanta"),
            _match("15 Jun", "Arabia Saudita", "\U0001f1f8\U0001f1e6", "Uruguay", "\U0001f1fa\U0001f1fe", 13, "Hard Rock Stadium, Miami"),
            _match("21 Jun", "Espana", "\U0001f1ea\U0001f1f8", "Arabia Saudita", "\U0001f1f8\U0001f1e6", 38, "Mercedes-Benz Stadium, Atlanta"),
            _match("21 Jun", "Uruguay", "\U0001f1fa\U0001f1fe", "Cabo Verde", "\U0001f1e8\U0001f1fb", 37, "Hard Rock Stadium, Miami"),
            _match("26 Jun", "Uruguay", "\U0001f1fa\U0001f1fe", "Espana", "\U0001f1ea\U0001f1f8", 66, "Estadio Chivas, Guadalajara"),
            _match("26 Jun", "Cabo Verde", "\U0001f1e8\U0001f1fb", "Arabia Saudita", "\U0001f1f8\U0001f1e6", 65, "NRG Stadium, Houston"),
        ],
        "banner": "assets/grupoH/bannerH.png",
        "mascots": {},
    },
    "I": {
        "teams": [
            _team("Francia", "\U0001f1eb\U0001f1f7"),
            _team("Senegal", "\U0001f1f8\U0001f1f3"),
            _team("Irak", "\U0001f1ee\U0001f1f6"),
            _team("Noruega", "\U0001f1f3\U0001f1f4"),
        ],
        "matches": [
            _match("16 Jun", "Francia", "\U0001f1eb\U0001f1f7", "Senegal", "\U0001f1f8\U0001f1f3", 17, "MetLife Stadium, Nueva Jersey"),
            _match("16 Jun", "Irak", "\U0001f1ee\U0001f1f6", "Noruega", "\U0001f1f3\U0001f1f4", 18, "Gillette Stadium, Boston"),
            _match("22 Jun", "Francia", "\U0001f1eb\U0001f1f7", "Irak", "\U0001f1ee\U0001f1f6", 42, "Lincoln Financial Field, Filadelfia"),
            _match("22 Jun", "Noruega", "\U0001f1f3\U0001f1f4", "Senegal", "\U0001f1f8\U0001f1f3", 41, "MetLife Stadium, Nueva Jersey"),
            _match("26 Jun", "Noruega", "\U0001f1f3\U0001f1f4", "Francia", "\U0001f1eb\U0001f1f7", 61, "Gillette Stadium, Boston"),
            _match("26 Jun", "Senegal", "\U0001f1f8\U0001f1f3", "Irak", "\U0001f1ee\U0001f1f6", 62, "BMO Field, Toronto"),
        ],
        "banner": "assets/grupoI/bannerI.png",
        "mascots": {},
    },
    "J": {
        "teams": [
            _team("Argentina", "\U0001f1e6\U0001f1f7"),
            _team("Argelia", "\U0001f1e9\U0001f1ff"),
            _team("Austria", "\U0001f1e6\U0001f1f9"),
            _team("Jordania", "\U0001f1ef\U0001f1f4"),
        ],
        "matches": [
            _match("16 Jun", "Argentina", "\U0001f1e6\U0001f1f7", "Argelia", "\U0001f1e9\U0001f1ff", 19, "Arrowhead Stadium, Kansas City"),
            _match("16 Jun", "Austria", "\U0001f1e6\U0001f1f9", "Jordania", "\U0001f1ef\U0001f1f4", 20, "Levi's Stadium, San Francisco"),
            _match("22 Jun", "Argentina", "\U0001f1e6\U0001f1f7", "Austria", "\U0001f1e6\U0001f1f9", 43, "AT&T Stadium, Dallas"),
            _match("22 Jun", "Jordania", "\U0001f1ef\U0001f1f4", "Argelia", "\U0001f1e9\U0001f1ff", 44, "Levi's Stadium, San Francisco"),
            _match("27 Jun", "Jordania", "\U0001f1ef\U0001f1f4", "Argentina", "\U0001f1e6\U0001f1f7", 70, "AT&T Stadium, Dallas"),
            _match("27 Jun", "Argelia", "\U0001f1e9\U0001f1ff", "Austria", "\U0001f1e6\U0001f1f9", 69, "Arrowhead Stadium, Kansas City"),
        ],
        "banner": "assets/grupoJ/bannerJ.png",
        "mascots": {},
    },
    "K": {
        "teams": [
            _team("Portugal", "\U0001f1f5\U0001f1f9"),
            _team("R. D. del Congo", "\U0001f1e8\U0001f1e9"),
            _team("Uzbekistan", "\U0001f1fa\U0001f1ff"),
            _team("Colombia", "\U0001f1e8\U0001f1f4"),
        ],
        "matches": [
            _match("17 Jun", "Portugal", "\U0001f1f5\U0001f1f9", "R. D. del Congo", "\U0001f1e8\U0001f1e9", 23, "NRG Stadium, Houston"),
            _match("17 Jun", "Uzbekistan", "\U0001f1fa\U0001f1ff", "Colombia", "\U0001f1e8\U0001f1f4", 24, "Estadio Azteca, Ciudad de Mexico"),
            _match("23 Jun", "Portugal", "\U0001f1f5\U0001f1f9", "Uzbekistan", "\U0001f1fa\U0001f1ff", 47, "NRG Stadium, Houston"),
            _match("23 Jun", "Colombia", "\U0001f1e8\U0001f1f4", "R. D. del Congo", "\U0001f1e8\U0001f1e9", 48, "Estadio Chivas, Guadalajara"),
            _match("27 Jun", "Colombia", "\U0001f1e8\U0001f1f4", "Portugal", "\U0001f1f5\U0001f1f9", 71, "Hard Rock Stadium, Miami"),
            _match("27 Jun", "R. D. del Congo", "\U0001f1e8\U0001f1e9", "Uzbekistan", "\U0001f1fa\U0001f1ff", 72, "Mercedes-Benz Stadium, Atlanta"),
        ],
        "banner": "assets/grupoK/bannerK.png",
        "mascots": {},
    },
    "L": {
        "teams": [
            _team("Inglaterra", "\U0001f3f4\U000e0067\U000e0062\U000e0065\U000e006e\U000e0067\U000e007f"),
            _team("Croacia", "\U0001f1ed\U0001f1f7"),
            _team("Ghana", "\U0001f1ec\U0001f1ed"),
            _team("Panama", "\U0001f1f5\U0001f1e6"),
        ],
        "matches": [
            _match("17 Jun", "Inglaterra", "\U0001f3f4\U000e0067\U000e0062\U000e0065\U000e006e\U000e0067\U000e007f", "Croacia", "\U0001f1ed\U0001f1f7", 22, "AT&T Stadium, Dallas"),
            _match("17 Jun", "Ghana", "\U0001f1ec\U0001f1ed", "Panama", "\U0001f1f5\U0001f1e6", 21, "BMO Field, Toronto"),
            _match("23 Jun", "Inglaterra", "\U0001f3f4\U000e0067\U000e0062\U000e0065\U000e006e\U000e0067\U000e007f", "Ghana", "\U0001f1ec\U0001f1ed", 45, "Gillette Stadium, Boston"),
            _match("23 Jun", "Panama", "\U0001f1f5\U0001f1e6", "Croacia", "\U0001f1ed\U0001f1f7", 46, "BMO Field, Toronto"),
            _match("27 Jun", "Panama", "\U0001f1f5\U0001f1e6", "Inglaterra", "\U0001f3f4\U000e0067\U000e0062\U000e0065\U000e006e\U000e0067\U000e007f", 67, "MetLife Stadium, Nueva Jersey"),
            _match("27 Jun", "Croacia", "\U0001f1ed\U0001f1f7", "Ghana", "\U0001f1ec\U0001f1ed", 68, "Lincoln Financial Field, Filadelfia"),
        ],
        "banner": "assets/grupoL/bannerL.png",
        "mascots": {},
    },
}

GROUP_LETTERS = list(GROUPS.keys())
