import folium


def create_map(df):


    m = folium.Map(location=[df.latitude.mean(), df.longitude.mean()], zoom_start=8, tiles='OpenStreetMap')
    for _, row in df.iterrows():

        folium.CircleMarker(
            location= [row['latitude'], row['longitude']],
            radius =4,

            popup = F' {row["label"]}, {row.startDate} , {row.endDate}',


        ).add_to(m)
    return m