from flask import Flask, render_template, request
from model.load_model import model, scaler, brand_le, default_values
import numpy as np
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    # return '<h1>Hello from Flask & Docker</h2>'
    return render_template("index.html", brands = brand_le.classes_, prediction = 0, default_values=default_values)

@app.route('/predict', methods=['POST'])
def predict():
    if not request.form['max_power']:
        max_power = default_values['max_power']
    else:
        max_power = float(request.form['max_power'])

    if not request.form['mileage']:
        mileage = default_values['mileage']
    else:
        mileage = float(request.form['mileage'])

    if not request.form['year']:
        year = default_values['year']
    else:
        year = float(request.form['year'])

    if not request.form['brand']:
        brand = default_values['brand']
    else:
        brand = brand_le.transform([request.form['brand']])

    input_features = np.array([[max_power, mileage, year, int(brand[0])]])
    input_features[:, 0: 3] = scaler.transform(input_features[:, 0: 3])

    prediction = np.exp(model.predict(input_features))
    prediction = format(prediction[0], ".2f")

    return render_template('index.html',prediction=prediction, brands = brand_le.classes_, default_values=default_values)


port_number = 8000

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=port_number)

# if __name__ == "__main__":
#     app.run(debug=True)