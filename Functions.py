



#plotting function to map out the location
def get_map(df):
  df = df.dropna(subset = ['lon', 'lat'])
  if df.shape[0]<15:
          map2 = folium.Map(location=[df.iloc[0].lat,df.iloc[0].lon], zoom_start=12)
  elif df.shape[0]>15:
      map2 = folium.Map(location=[df.iloc[0].lat,df.iloc[0].lon], zoom_start=2)

  #generate folium
  map2 = folium.Map(location=[df.iloc[0].lat,df.iloc[0].lon], zoom_start=12)
  folium.raster_layers.TileLayer('Open Street Map').add_to(map2)
  for i in range(0,len(df)):
      folium.Marker(
      location=[df.iloc[i].lat,df.iloc[i].lon],
          popup='hotel :' + df.iloc[i].address,
      icon=folium.Icon(icon_color='white')
  ).add_to(map2)

  return map2
