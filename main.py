import io
import base64
from flask import Flask, render_template, request, make_response
from calculations import calculate_distance
from geolocation import import_street_data_to_sqlite

# url = 'https://raw.githubusercontent.com/raphaelbdias/traffic/main/TrafficData.csv?token=GHSAT0AAAAAACEPSUZXJ36YCNTVOP725UUKZE5ZOCQ'
# records = requests.get(url).content

# df = pd.read_csv('TrafficData.csv')
# print(calculate_distance(df))

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def display_image():
    if request.method == "POST":
        # Get the location input from the form
        place_name = request.form["location"]

        # Call the function to import street data and retrieve the GeoDataFrame
        gdf = import_street_data_to_sqlite(place_name)
        print(gdf)

        # Convert the GeoDataFrame to an image
        image = gdf.plot(figsize=(10, 10), edgecolor="black", linewidth=0.5)

        # Save the image to a BytesIO object
        buffer = io.BytesIO()
        image.figure.savefig(buffer, format="png")
        buffer.seek(0)

        # Encode the image as base64
        image_base64 = base64.b64encode(buffer.getvalue()).decode()

        # Render the template with the image
        return render_template("image.html", image=image_base64)
    else:
        # Render the initial template with the form
        return render_template("index.html")


if __name__ == "__main__":
    app.run()
