"""
Flask aplikace pro predikci ceny automobilu na základě vstupních parametrů.
Používá předem natrénovaný model (např. XGBoost), normalizaci a mapování hodnot.
"""

from flask import Flask, render_template, request, jsonify
from datetime import datetime
import pandas as pd
import numpy as np
import json
import joblib
import os

app = Flask(__name__)

# === Načtení modelu, scaleru a sloupců ===
# Tyto soubory vznikly během fáze trénování modelu
model = joblib.load("model/model_xgb.pkl")  # Trénovaný regresní model
scaler = joblib.load("model/scaler.pkl")    # Normalizační scaler
expected_columns = joblib.load("model/features.pkl")  # Očekávané vstupní sloupce

# === Načtení mapování hodnot ===
# Mapy pro dropdowny
with open("maps/value_mapping.json", "r", encoding="utf-8") as f:
    value_map = json.load(f)

# === Definice typů proměnných ===
categorical_features = ['make', 'model', 'fuel_type', 'transmission', 'body_type']
numeric_features = ['year', 'mileage', 'engine_power']

@app.route("/", methods=["GET", "POST"])
def index():
    """
    Hlavní stránka s formulářem a predikcí ceny.
    Při GET se zobrazí formulář.
    Při POST se zpracuje vstup a vrátí se odhad ceny.
    """
    predicted_price = None

    if request.method == "POST":
        try:
            # Sběr dat z formuláře
            input_data = {
                "make": request.form["make"],
                "model": request.form["model"],
                "year": int(request.form["year"]),
                "mileage": int(request.form["mileage"]),
                "fuel_type": request.form["fuel_type"],
                "transmission": request.form["transmission"],
                "engine_power": int(request.form["engine_power"]),
                "body_type": request.form["body_type"]
            }

            # Převod do DataFrame
            df = pd.DataFrame([input_data])

            # One-hot encoding + doplnění chybějících sloupců
            df = pd.get_dummies(df)
            df = df.reindex(columns=expected_columns, fill_value=0)

            # Normalizace číselných vstupů
            df[numeric_features] = scaler.transform(df[numeric_features])

            # Predikce
            prediction = model.predict(df)
            predicted_price = round(prediction[0])

        except Exception as e:
            print("Chyba při predikci:", e)

    # Zobrazení stránky s výsledkem nebo formulářem
    return render_template("index.html", predicted_price=predicted_price, values=value_map, current_year=datetime.now().year)


@app.route("/get_models")
def get_models():
    """
    Endpoint, který vrátí modely pro danou značku (značka se získá z query parametru).
    """
    make = request.args.get("make")
    models = value_map["make_model_map"].get(make, [])
    return jsonify(models)


@app.route("/get_options")
def get_options():
    """
    Endpoint, který vrátí paliva, převodovky a karoserie podle vybraného modelu.
    """
    model = request.args.get("model")
    return jsonify({
        "fuel_types": value_map["model_fuel_types"].get(model, []),
        "transmissions": value_map["model_transmissions"].get(model, []),
        "body_types": value_map["model_body_types"].get(model, [])
    })


if __name__ == "__main__":
    app.run(debug=True)
