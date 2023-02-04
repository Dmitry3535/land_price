from flask import request, Flask, render_template

import numpy as np
from settings import GOR_OKRUGS, MAIN_SHOSSES,CEL,REGIONS, PLACE_ALL , loc_mkad, code_categorical, get_loc_yandex
from settings import square_scaled, latitude_scaled, longitude_scaled, distance_categorical, fact_price
from keras import models

from geopy.distance import geodesic

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def home():
    context = {'main_shosses':MAIN_SHOSSES, 'gor_okrugs':GOR_OKRUGS, 'all_places':PLACE_ALL}
    return render_template('home.html', context=context)

@app.route('/predict', methods=['POST'])
def predict():
    cel = request.form["cel"]
    cel_cat = code_categorical(cel, CEL)
    region = request.form["region"]
    region_cat = code_categorical(region, REGIONS)
    gor_okrug = request.form["gor_okrug"]
    gor_okrug_cat = code_categorical(gor_okrug, GOR_OKRUGS)
    main_shosse = request.form['main_shosse']
    main_shosse_cat = code_categorical(main_shosse, MAIN_SHOSSES)
    place = request.form["place"]
    place_cat = code_categorical(place, PLACE_ALL)

    square = request.form['square']
    square_norm = np.array([square_scaled(square)])

    place_row =[ region, gor_okrug, place]
    latitude, longitude =get_loc_yandex(place_row)
    latitude_norm = np.array([latitude_scaled(latitude)])
    longitude_norm = np.array([longitude_scaled(longitude)])

    distance = round(geodesic(loc_mkad[main_shosse], [latitude, longitude]).km)
    distance_cat = np.array(distance_categorical(distance))

    vec_for_ns = np.concatenate([cel_cat, square_norm, region_cat, gor_okrug_cat, place_cat, latitude_norm, longitude_norm, main_shosse_cat, distance_cat ])
    vec_for_ns = vec_for_ns.reshape(1,vec_for_ns.shape[0])
    model = models.load_model('F:\PycharmProjects\deploy-app\model_2')
    pred = np.argmax(model.predict(vec_for_ns))

    vec_type = type(vec_for_ns)
    price = fact_price(pred)
    context_pred = {"cel":cel, "region":region, "gor_okrug":gor_okrug, "place":place, "main_shosse": main_shosse, "square":square,
                    "distance":distance, "price":price}

    return render_template('predict.html', context=context_pred, vec = vec_for_ns.shape, tvec =vec_type, lat=latitude, lon=longitude)

if __name__=='__main__':
    app.run(debug=True)

