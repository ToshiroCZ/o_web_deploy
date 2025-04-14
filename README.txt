OMEGA_WEB – Car Price Prediction Web Interface
==============================================

Matouš Podaný
C4b
SPŠE Ječná

Description:
------------
This is the web frontend for the Omega project. The application allows users to predict the price of a used car based on its parameters using a trained machine learning model.

The application is built using Flask (Python backend) and HTML/CSS/JavaScript (frontend). Dynamic dropdowns adjust based on previous input selections.


Usage:
------

1. Set up virtual environment and install dependencies:

    python -m venv venv
    venv\Scripts\activate       (on Windows)
    pip install -r requirements.txt

2. Make sure the following files exist in the correct locations:

    ├── model/
    │   ├── model_xgb.pkl          (trained model)
    │   ├── scaler.pkl             (StandardScaler object for numeric features)
    │   └── features.pkl           (list of expected feature columns)
    ├── maps/
    │   └── value_mapping.json     (contains lists of makes, models, etc.)
    ├── templates/
    │   └── index.html             (web interface)

3. Run the app:

    python app.py

4. Open the application in browser:

    http://127.0.0.1:5000

Main Functionality:
-------------------

- Predicts car price based on:
    * Make
    * Model
    * Year
    * Mileage
    * Fuel Type
    * Transmission
    * Engine Power
    * Body Type

- Dynamically updates the model list based on selected make.
- Automatically filters available fuel types, transmissions and body types based on selected model.

File Description:
-----------------

- app.py                – main Flask server and prediction logic
- index.html            – frontend with prediction form
- value_mapping.json    – make-model-fuel-transmission-body mappings
- model_xgb.pkl         – trained model
- scaler.pkl            – scaler to normalize numeric inputs
- features.pkl          – full list of features used for training

Additional Notes:
-----------------

- To retrain or update the model, use the script from omega_model directory.
- Always make sure that model, scaler and feature files are in sync.
- All user input is validated in the backend; any missing values will result in error.
- Fuel types are cleaned and normalized before prediction.