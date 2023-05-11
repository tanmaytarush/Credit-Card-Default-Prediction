from flask import Flask, Response, render_template, request
from flask_cors import CORS, cross_origin
import pickle

#model_path = r'XGBOOST_Tuned.sav'

#model = joblib.load(model_path)
# Use PICKLE INSTEAD
model = pickle.load(open('XGBOOST_tuned.pkl','rb'))


app = Flask(__name__)
CORS(app)


@app.route("/", methods = [ "GET" ])
@cross_origin()
def home():
    return render_template("index.html")


@app.route("/predict", methods = [ 'POST' ])
@cross_origin()
def predict():
    if request.method == "POST":
        try:
            if request.form:
                data_req = dict(request.form)
                data = data_req.values()
                data_int=[int(i) for i in data]
                data = [list(data_int)]
                pred = model.predict(data)[0]

                # predicting the output
                result = pred
                if result == 1:
                    result = "Yes"
                else:
                    result = "No"
                return render_template('result.html', result = result)
            else:
                return ""
        except Exception as e:
            error = {'error': e}
            return render_template('404.html', error = error)
    else:
        return render_template('404.html', error = "Something went wrong!! Try again.")


if __name__ == "__main__":
    app.run(debug = True)
