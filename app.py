from flask import Flask
app = Flask(__name__)


def objects_from_image():
    pass

def data_from_objects():
    pass

def classification_from_data():
    pass


@app.route("/analysis")
def analyze_data():
    classification_from_data()
    return "We have, in theory, parsed the data and returned JSON"

@app.route("/image")
def analyze_image():
    return "We have, in theory, parsed the image and returned JSON"


if __name__ == "__main__":
    app.run(debug=True)