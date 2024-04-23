from flask import Flask, render_template, request, redirect
from flask_cors import CORS, cross_origin
import pickle
import pandas as pd
import numpy as np

app = Flask(__name__)
car = pd.read_csv("Cleaned_Car_data.csv")
model = pickle.load(open("LinearRegressionModel.pkl", "rb"))


@app.route("/")
def index():
    companies = sorted(car["company"].unique())
    companies.insert(0, "Select Company")
    car_models = sorted(car["name"].unique())
    year = sorted(car["year"].unique(), reverse=True)
    fuel_type = car["fuel_type"].unique()
    return render_template(
        "index.html",
        companies=companies,
        car_models=car_models,
        years=year,
        fuel_types=fuel_type,
    )


@app.route("/predict", methods=["POST"])
@cross_origin()
def predict():

    company = request.form.get("company")

    car_model = request.form.get("car_models")
    year = request.form.get("year")
    fuel_type = request.form.get("fuel_type")
    driven = request.form.get("kilo_driven")

    prediction = model.predict(
        pd.DataFrame(
            columns=["name", "company", "year", "kms_driven", "fuel_type"],
            data=np.array([car_model, company, year, driven, fuel_type]).reshape(1, 5),
        )
    )
    print(prediction)

    return str(np.round(prediction[0], 2))


if __name__ == "__main__":
    app.run(debug=True)
