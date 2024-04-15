import streamlit as st
import plotly.express as px
from request import get_data, get_city

st.header('Weather Forecast')
user_input = st.text_input('Place: ')
days = st.slider('Forecast days', min_value=1, max_value=5, help='Select nr of days')
option = st.selectbox('Select data to view', ('Temperature', 'Sky'))
city = get_city(user_input)


if city:
    st.subheader(f'{option} in the next {days} days in {city["name"]}')
    values = get_data(city['lat'], city['lon'], days)

    if option == 'Sky':
        col1, col2, col3 = st.columns(3)
        skies = [data['weather'][0]['main'] for data in values]
        dates = [data['dt_txt'] for data in values]
        img_list = [f'WeatherForecast/imgs/{sky.lower()}.png' for sky in skies]
        with col1:
            s1 = skies[::3]
            d1 = dates[::3]
            for i, path in enumerate(img_list[::3]):
                st.image(path, width=150)
                st.write(s1[i])
                st.write(d1[i])
        with col2:
            s2 = skies[1::3]
            d2 = dates[1::3]
            for i, path in enumerate(img_list[1::3]):
                st.image(path, width=150)
                st.write(s2[i])
                st.write(d2[i])
        with col3:
            s3 = skies[2::3]
            d3 = dates[2::3]
            for i, path in enumerate(img_list[2::3]):
                st.image(path, width=150)
                st.write(s3[i])
                st.write(d3[i])

    if option == 'Temperature':
        temps = [data['main']['temp'] for data in values]
        dates = [data['dt_txt'] for data in values]
        figure = px.line(x=dates, y=temps, labels={'x': 'Date', 'y': 'Temperature'})
        st.plotly_chart(figure)
else:
    st.write('Enter a valid place name')


if __name__ == '__main__':
    print('PyCharm')
