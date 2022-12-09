
from django.shortcuts import render
import folium
import geocoder
import numpy as np
import xarray as xr
import numpy.ma as ma
import matplotlib.pyplot as plt
import branca
import os
import folium.raster_layers as rasters
#from gi.repository import Geoclue
import branca.colormap as cmp
import matplotlib.cm as cm

from branca.element import Template, MacroElement

from jinja2 import Template

class BindColormap(MacroElement):
    """Binds a colormap to a given layer.

    Parameters
    ----------
    colormap : branca.colormap.ColorMap
        The colormap to bind.
    """
    def __init__(self, layer, colormap):
        super(BindColormap, self).__init__()
        self.layer = layer
        self.colormap = colormap
        self._template = Template(u"""
        {% macro script(this, kwargs) %}
            {{this.colormap.get_name()}}.svg[0][0].style.display = 'block';
            {{this._parent.get_name()}}.on('overlayadd', function (eventLayer) {
                if (eventLayer.layer == {{this.layer.get_name()}}) {
                    {{this.colormap.get_name()}}.svg[0][0].style.display = 'block';
                }});
            {{this._parent.get_name()}}.on('overlayremove', function (eventLayer) {
                if (eventLayer.layer == {{this.layer.get_name()}}) {
                    {{this.colormap.get_name()}}.svg[0][0].style.display = 'none';
                }});
        {% endmacro %}
        """)  # noqa


def colorize(array, cmap='viridis'):
    normed_data = (array - array.min()) / (array.max() - array.min())
    cm = plt.cm.get_cmap(cmap)
    return cm(normed_data)

def plot_raster(in_path, cmap="viridis", nodata=False):
    # Create a variable for destination coordinate system
    da_dem  = xr.open_rasterio(in_path).drop('band')[0].rename({'x':'longitude', 'y':'latitude'})

    if nodata == False:
        nodata = da_dem.nodatavals[0]
    da_dem = da_dem.where(da_dem > nodata, np.nan)
    arr_dem = da_dem.values

    mlat = da_dem.latitude.values.min()
    mlon = da_dem.longitude.values.min()

    xlat = da_dem.latitude.values.max()
    xlon = da_dem.longitude.values.max()

    data = ma.masked_invalid(arr_dem)
    colored_data = colorize(data, cmap)


    return (colored_data, [[mlat, mlon], [xlat, xlon]])


def map(request):
#    clue = Geoclue.Simple.new_sync('something', Geoclue.AccuracyLevel.EXACT, None)
#    location = clue.get_location()
#    print(location.get_property('latitude'), location.get_property('longitude'))
    #if request.method == "POST":
    #    address = request.POST.get('address')
    #    print(address)
    #    if address == '':
    #        address = "ucsb"
    #    location = geocoder.osm(address)

    #else:
     #   location = geocoder.osm('ucsb')


    location = geocoder.osm('ucsb')
    lat = location.lat
    lng = location.lng

    f = folium.Figure(width="100%", height="100%")
    m = folium.Map(location=[lat, lng], zoom_start=12, control_scale=True, prefer_canvas=True).add_to(f)

    folium.Marker([lat, lng]).add_to(m)

    folium.TileLayer('Stamen Terrain', name = 'Terrain').add_to(m)
    folium.TileLayer('CartoDB Positron', name="Grey").add_to(m)

    # sample layers
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        ## live fuel moisture

    colored_data, map_bounds = plot_raster(BASE_DIR + '/static/sitemap/images/' + "lfm_.tif")
    LFM = rasters.ImageOverlay(image=colored_data,
                                      bounds=map_bounds,
                                      opacity=0.6,
                                      name="livefuelmoisture",
                                      show=False)

    lfm_colormap = branca.colormap.linear.viridis.scale(0, 100)
    lfm_colormap = lfm_colormap.to_step(index=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
    lfm_colormap.caption = 'Live Fuel Moisture (%)'

    m.add_child(LFM)
    m.add_child(lfm_colormap)
    m.add_child(BindColormap(LFM, lfm_colormap))




        ## integrated hazard


    cd, mb = plot_raster(BASE_DIR + '/static/sitemap/images/' + "ih__.tif", "viridis", nodata=1)
    IH = rasters.ImageOverlay(image=cd,
                               bounds=mb,
                               opacity=0.9,
                               name="IntegratedHazard",
                               zindex=2)
    print(mb)

    ih_colormap = branca.colormap.linear.viridis.scale(2, 5)
    ih_colormap = ih_colormap.to_step(index=[1, 2, 3, 4, 5])
    ih_colormap.caption = 'Integrated Hazard'

    m.add_child(IH)
    m.add_child(ih_colormap)
    m.add_child(BindColormap(IH, ih_colormap))



## weather

    cd, mb = plot_raster(BASE_DIR + '/static/sitemap/images/' + "kelvintemp.tif", "viridis", nodata=1)
    KT = rasters.ImageOverlay(image=cd,
                              bounds=mb,
                              opacity=0.9,
                              name="Temperature(K)",
                              show=False)

    kt_colormap = branca.colormap.linear.viridis.scale(286, 314)
#    ih_colormap = ih_colormap.to_step(index=[1, 2, 3, 4, 5])
    kt_colormap.caption = 'Temperature (K)'

    m.add_child(KT)
    m.add_child(kt_colormap)
    m.add_child(BindColormap(KT, kt_colormap))



    folium.LayerControl("topleft").add_to(m)

    m = m._repr_html_()
    context = {
        'm': m,
    }

    return render(request, "sitemap/map.html", context=context)