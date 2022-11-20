# Snow Days
Welcome to Snow Days! This is a fun little project graphically displaying the first snow dates per winter season for reporting weather stations throughout the continental United States. You can clone this repository and run it locally, or you can run it online using Google Colaboratory: https://colab.research.google.com/github/garretts-hub/Snow-Days/blob/main/Snow%20Days%20Display.ipynb <br>

The `Snow Days Display.ipynb` notebook allows you to select a winter season (indicated by the year at the start of winter) and generate an interactive map of stations that have observed snow by the date. Use the slider to progress the map in time.:<br>
<img src="https://github.com/garretts-hub/Snow-Days/blob/main/images/map_sample.PNG" alt="Stations having observed snow prior to Dec. 19, 2019." title="Sample Map" width=auto>
<br><br>
For this notebook to work, your Jupyter environment must have the following packages installed:
- pandas
- geopandas
- shapely
- ipywidgets
<br><br>
All weather data for this notebook was obtained using the Global Historical Climatology Network daily (GHCNd) dataset. This publicly available dataset integrates daily climate summaries from land stations around the globe for more than a century: 
https://www.ncei.noaa.gov/products/land-based-station/global-historical-climatology-network-daily 
