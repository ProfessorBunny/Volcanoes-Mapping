import folium
import pandas
from flask import Flask, render_template

data = pandas.read_csv("Volcanoes.txt")
map = folium.Map(location=[39.876019, -117.224121],
                 zoom_start=4, tiles="Stamen Terrain")

lat = list(data["LAT"])
lon = list(data["LON"])
num = list(data["NUMBER"])
name = list(data["NAME"])
loc = list(data["LOCATION"])
stat = list(data["STATUS"])
elev = list(data["ELEV"])
typ = list(data["TYPE"])
tf = list(data["TIMEFRAME"])


def color_producer(elevation):
    if (elevation < 2000):
        return "green"
    elif(elevation > 2000 and elevation < 3000):
        return "orange"
    else:
        return "red"
# map.add_child(folium.Marker(
#     location=[38.2, -99.1], popup="#marker", icon=folium.Icon(color="blue")))

# Better way to write the above line


fgv = folium.FeatureGroup(name="Volcanoes")
for lt, ln, num, nam, loc, stat, el, typ, tf in zip(lat, lon, num, name, loc, stat, elev, typ, tf):
    fgv.add_child(folium.Marker(
        location=[lt, ln], popup='NUMBER:{}\n NAME:{}\n LOCATION:{}\n STATUS:{}\n ELEVATION:{}\n TYPE:{}\n TIMEFRAME:{} ' .format(num, nam, loc, stat, el, typ, tf), icon=folium.Icon(color=color_producer(el))))


fgp = folium.FeatureGroup(name="Population")
fgp.add_child(folium.GeoJson(
    data=(open('world.json', 'r', encoding='utf-8-sig').read()), style_function=lambda x: {'fillColor': 'green' if x['properties']['POP2005'] < 10000000
                                                                                           else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))

map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl())

html_map = map._repr_html_()

app = Flask(__name__)


@ app.route('/')
def home():
    return render_template("home.html", volcanoes_map=html_map)


if __name__ == '__main__':
    app.run(debug=True)
