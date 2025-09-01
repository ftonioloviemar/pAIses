import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

db = SQLAlchemy()

class Country(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    initial_letter: Mapped[str] = mapped_column(String(1), nullable=False)
    flag_code: Mapped[str] = mapped_column(String(2), nullable=False)
    difficulty: Mapped[str] = mapped_column(String, nullable=False)

class Ranking(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    player_name: Mapped[str] = mapped_column(String(50), nullable=False)
    country_name: Mapped[str] = mapped_column(String, nullable=False)
    time_spent: Mapped[float] = mapped_column(Float, nullable=False)
    attempts: Mapped[int] = mapped_column(Integer, nullable=False)
    difficulty: Mapped[str] = mapped_column(String, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    city: Mapped[str] = mapped_column(String(100), nullable=True)

def get_countries_data():
    return [
        {"name": "Afeganistão", "alpha-2": "AF"},
        {"name": "África do Sul", "alpha-2": "ZA"},
        {"name": "Albânia", "alpha-2": "AL"},
        {"name": "Alemanha", "alpha-2": "DE"},
        {"name": "Andorra", "alpha-2": "AD"},
        {"name": "Angola", "alpha-2": "AO"},
        {"name": "Antígua e Barbuda", "alpha-2": "AG"},
        {"name": "Arábia Saudita", "alpha-2": "SA"},
        {"name": "Argélia", "alpha-2": "DZ"},
        {"name": "Argentina", "alpha-2": "AR"},
        {"name": "Armênia", "alpha-2": "AM"},
        {"name": "Austrália", "alpha-2": "AU"},
        {"name": "Áustria", "alpha-2": "AT"},
        {"name": "Azerbaijão", "alpha-2": "AZ"},
        {"name": "Bahamas", "alpha-2": "BS"},
        {"name": "Bahrein", "alpha-2": "BH"},
        {"name": "Bangladesh", "alpha-2": "BD"},
        {"name": "Barbados", "alpha-2": "BB"},
        {"name": "Bélgica", "alpha-2": "BE"},
        {"name": "Belize", "alpha-2": "BZ"},
        {"name": "Benin", "alpha-2": "BJ"},
        {"name": "Bielorrússia", "alpha-2": "BY"},
        {"name": "Bolívia", "alpha-2": "BO"},
        {"name": "Bósnia e Herzegovina", "alpha-2": "BA"},
        {"name": "Botsuana", "alpha-2": "BW"},
        {"name": "Brasil", "alpha-2": "BR"},
        {"name": "Brunei", "alpha-2": "BN"},
        {"name": "Bulgária", "alpha-2": "BG"},
        {"name": "Burkina Faso", "alpha-2": "BF"},
        {"name": "Burundi", "alpha-2": "BI"},
        {"name": "Butão", "alpha-2": "BT"},
        {"name": "Cabo Verde", "alpha-2": "CV"},
        {"name": "Camarões", "alpha-2": "CM"},
        {"name": "Camboja", "alpha-2": "KH"},
        {"name": "Canadá", "alpha-2": "CA"},
        {"name": "Catar", "alpha-2": "QA"},
        {"name": "Cazaquistão", "alpha-2": "KZ"},
        {"name": "Chade", "alpha-2": "TD"},
        {"name": "Chile", "alpha-2": "CL"},
        {"name": "China", "alpha-2": "CN"},
        {"name": "Chipre", "alpha-2": "CY"},
        {"name": "Colômbia", "alpha-2": "CO"},
        {"name": "Comores", "alpha-2": "KM"},
        {"name": "Congo", "alpha-2": "CG"},
        {"name": "Coreia do Norte", "alpha-2": "KP"},
        {"name": "Coreia do Sul", "alpha-2": "KR"},
        {"name": "Costa do Marfim", "alpha-2": "CI"},
        {"name": "Costa Rica", "alpha-2": "CR"},
        {"name": "Croácia", "alpha-2": "HR"},
        {"name": "Cuba", "alpha-2": "CU"},
        {"name": "Dinamarca", "alpha-2": "DK"},
        {"name": "Djibuti", "alpha-2": "DJ"},
        {"name": "Dominica", "alpha-2": "DM"},
        {"name": "Egito", "alpha-2": "EG"},
        {"name": "El Salvador", "alpha-2": "SV"},
        {"name": "Emirados Árabes Unidos", "alpha-2": "AE"},
        {"name": "Equador", "alpha-2": "EC"},
        {"name": "Eritreia", "alpha-2": "ER"},
        {"name": "Eslováquia", "alpha-2": "SK"},
        {"name": "Eslovênia", "alpha-2": "SI"},
        {"name": "Espanha", "alpha-2": "ES"},
        {"name": "Essuatíni", "alpha-2": "SZ"},
        {"name": "Estados Unidos", "alpha-2": "US"},
        {"name": "Estônia", "alpha-2": "EE"},
        {"name": "Etiópia", "alpha-2": "ET"},
        {"name": "Fiji", "alpha-2": "FJ"},
        {"name": "Filipinas", "alpha-2": "PH"},
        {"name": "Finlândia", "alpha-2": "FI"},
        {"name": "França", "alpha-2": "FR"},
        {"name": "Gabão", "alpha-2": "GA"},
        {"name": "Gâmbia", "alpha-2": "GM"},
        {"name": "Gana", "alpha-2": "GH"},
        {"name": "Geórgia", "alpha-2": "GE"},
        {"name": "Granada", "alpha-2": "GD"},
        {"name": "Grécia", "alpha-2": "GR"},
        {"name": "Guatemala", "alpha-2": "GT"},
        {"name": "Guiana", "alpha-2": "GY"},
        {"name": "Guiné", "alpha-2": "GN"},
        {"name": "Guiné Equatorial", "alpha-2": "GQ"},
        {"name": "Guiné-Bissau", "alpha-2": "GW"},
        {"name": "Haiti", "alpha-2": "HT"},
        {"name": "Honduras", "alpha-2": "HN"},
        {"name": "Hungria", "alpha-2": "HU"},
        {"name": "Iêmen", "alpha-2": "YE"},
        {"name": "Ilhas Marshall", "alpha-2": "MH"},
        {"name": "Ilhas Salomão", "alpha-2": "SB"},
        {"name": "Índia", "alpha-2": "IN"},
        {"name": "Indonésia", "alpha-2": "ID"},
        {"name": "Irã", "alpha-2": "IR"},
        {"name": "Iraque", "alpha-2": "IQ"},
        {"name": "Irlanda", "alpha-2": "IE"},
        {"name": "Islândia", "alpha-2": "IS"},
        {"name": "Israel", "alpha-2": "IL"},
        {"name": "Itália", "alpha-2": "IT"},
        {"name": "Jamaica", "alpha-2": "JM"},
        {"name": "Japão", "alpha-2": "JP"},
        {"name": "Jordânia", "alpha-2": "JO"},
        {"name": "Kiribati", "alpha-2": "KI"},
        {"name": "Kuwait", "alpha-2": "KW"},
        {"name": "Laos", "alpha-2": "LA"},
        {"name": "Lesoto", "alpha-2": "LS"},
        {"name": "Letônia", "alpha-2": "LV"},
        {"name": "Líbano", "alpha-2": "LB"},
        {"name": "Libéria", "alpha-2": "LR"},
        {"name": "Líbia", "alpha-2": "LY"},
        {"name": "Liechtenstein", "alpha-2": "LI"},
        {"name": "Lituânia", "alpha-2": "LT"},
        {"name": "Luxemburgo", "alpha-2": "LU"},
        {"name": "Macedônia do Norte", "alpha-2": "MK"},
        {"name": "Madagascar", "alpha-2": "MG"},
        {"name": "Malásia", "alpha-2": "MY"},
        {"name": "Malawi", "alpha-2": "MW"},
        {"name": "Maldivas", "alpha-2": "MV"},
        {"name": "Mali", "alpha-2": "ML"},
        {"name": "Malta", "alpha-2": "MT"},
        {"name": "Marrocos", "alpha-2": "MA"},
        {"name": "Maurício", "alpha-2": "MU"},
        {"name": "Mauritânia", "alpha-2": "MR"},
        {"name": "México", "alpha-2": "MX"},
        {"name": "Mianmar", "alpha-2": "MM"},
        {"name": "Micronésia", "alpha-2": "FM"},
        {"name": "Moçambique", "alpha-2": "MZ"},
        {"name": "Moldávia", "alpha-2": "MD"},
        {"name": "Mônaco", "alpha-2": "MC"},
        {"name": "Mongólia", "alpha-2": "MN"},
        {"name": "Montenegro", "alpha-2": "ME"},
        {"name": "Namíbia", "alpha-2": "NA"},
        {"name": "Nauru", "alpha-2": "NR"},
        {"name": "Nepal", "alpha-2": "NP"},
        {"name": "Nicarágua", "alpha-2": "NI"},
        {"name": "Níger", "alpha-2": "NE"},
        {"name": "Nigéria", "alpha-2": "NG"},
        {"name": "Noruega", "alpha-2": "NO"},
        {"name": "Nova Zelândia", "alpha-2": "NZ"},
        {"name": "Omã", "alpha-2": "OM"},
        {"name": "Países Baixos", "alpha-2": "NL"},
        {"name": "Palau", "alpha-2": "PW"},
        {"name": "Panamá", "alpha-2": "PA"},
        {"name": "Papua-Nova Guiné", "alpha-2": "PG"},
        {"name": "Paquistão", "alpha-2": "PK"},
        {"name": "Paraguai", "alpha-2": "PY"},
        {"name": "Peru", "alpha-2": "PE"},
        {"name": "Polônia", "alpha-2": "PL"},
        {"name": "Portugal", "alpha-2": "PT"},
        {"name": "Quênia", "alpha-2": "KE"},
        {"name": "Quirguistão", "alpha-2": "KG"},
        {"name": "Reino Unido", "alpha-2": "GB"},
        {"name": "República Centro-Africana", "alpha-2": "CF"},
        {"name": "República Tcheca", "alpha-2": "CZ"},
        {"name": "República Democrática do Congo", "alpha-2": "CD"},
        {"name": "República Dominicana", "alpha-2": "DO"},
        {"name": "Romênia", "alpha-2": "RO"},
        {"name": "Ruanda", "alpha-2": "RW"},
        {"name": "Rússia", "alpha-2": "RU"},
        {"name": "Samoa", "alpha-2": "WS"},
        {"name": "Santa Lúcia", "alpha-2": "LC"},
        {"name": "São Cristóvão e Nevis", "alpha-2": "KN"},
        {"name": "São Marinho", "alpha-2": "SM"},
        {"name": "São Tomé e Príncipe", "alpha-2": "ST"},
        {"name": "São Vicente e Granadinas", "alpha-2": "VC"},
        {"name": "Senegal", "alpha-2": "SN"},
        {"name": "Sérvia", "alpha-2": "RS"},
        {"name": "Serra Leoa", "alpha-2": "SL"},
        {"name": "Seychelles", "alpha-2": "SC"},
        {"name": "Singapura", "alpha-2": "SG"},
        {"name": "Síria", "alpha-2": "SY"},
        {"name": "Somália", "alpha-2": "SO"},
        {"name": "Sri Lanka", "alpha-2": "LK"},
        {"name": "Sudão", "alpha-2": "SD"},
        {"name": "Sudão do Sul", "alpha-2": "SS"},
        {"name": "Suécia", "alpha-2": "SE"},
        {"name": "Suíça", "alpha-2": "CH"},
        {"name": "Suriname", "alpha-2": "SR"},
        {"name": "Tailândia", "alpha-2": "TH"},
        {"name": "Taiwan", "alpha-2": "TW"},
        {"name": "Tadjiquistão", "alpha-2": "TJ"},
        {"name": "Tanzânia", "alpha-2": "TZ"},
        {"name": "Timor-Leste", "alpha-2": "TL"},
        {"name": "Togo", "alpha-2": "TG"},
        {"name": "Tonga", "alpha-2": "TO"},
        {"name": "Trinidad e Tobago", "alpha-2": "TT"},
        {"name": "Tunísia", "alpha-2": "TN"},
        {"name": "Turcomenistão", "alpha-2": "TM"},
        {"name": "Turquia", "alpha-2": "TR"},
        {"name": "Tuvalu", "alpha-2": "TV"},
        {"name": "Ucrânia", "alpha-2": "UA"},
        {"name": "Uganda", "alpha-2": "UG"},
        {"name": "Uruguai", "alpha-2": "UY"},
        {"name": "Uzbequistão", "alpha-2": "UZ"},
        {"name": "Vanuatu", "alpha-2": "VU"},
        {"name": "Vaticano", "alpha-2": "VA"},
        {"name": "Venezuela", "alpha-2": "VE"},
        {"name": "Vietnã", "alpha-2": "VN"},
        {"name": "Zâmbia", "alpha-2": "ZM"},
        {"name": "Zimbábue", "alpha-2": "ZW"}
    ]

def init_db(app):
    with app.app_context():
        # db.drop_all() # Removed to prevent data loss
        db.create_all()
        
        easy_countries = [
            "Brasil", "Estados Unidos", "Argentina", "Portugal", "Espanha", "França", "Alemanha", "Itália", "Japão", "China", "Canadá", "México", "Reino Unido"
        ]
        medium_countries = [
            "Chile", "Colômbia", "Peru", "Uruguai", "Paraguai", "Venezuela", "África do Sul", "Austrália", "Nova Zelândia", "Índia", "Rússia", "Egito", "Nigéria", "Suécia", "Noruega", "Finlândia", "Dinamarca", "Países Baixos", "Bélgica", "Suíça", "Áustria", "Grécia", "Turquia", "Arábia Saudita", "Emirados Árabes Unidos", "Israel", "Coreia do Sul", "Tailândia", "Vietnã", "Indonésia"
        ]

        # Check if countries are already populated
        # This logic needs to be updated to handle existing countries and new difficulty column
        # For now, it will only add countries if the table is empty.
        # A separate migration step is needed to add 'difficulty' to existing countries.
        if Country.query.first() is None:
            countries_data = get_countries_data()
            for country_data in countries_data:
                country_name = country_data["name"]
                difficulty = "hard" # Default to hard
                if country_name in easy_countries:
                    difficulty = "easy"
                elif country_name in medium_countries:
                    difficulty = "medium"

                country = Country(
                    name=country_name,
                    initial_letter=country_data["name"][0].upper(),
                    flag_code=country_data["alpha-2"].lower(),
                    difficulty=difficulty
                )
                db.session.add(country)
            db.session.commit()
            print("Database populated with countries and difficulties.")
        else:
            print("Database already populated.")