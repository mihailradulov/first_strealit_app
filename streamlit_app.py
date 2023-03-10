import streamlit
import pandas
import snowflake.connector
import requests
from urllib.error import URLError

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])

streamlit.title('My parrents New Healthy Diner')
streamlit.header('Breakfast Favorites')
streamlit.text('🥣Omega 3 & Blueberry Datmeal')
streamlit.text('🥗Kale, Spinache & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Ranged Egg')
streamlit.text('🥑🍞Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

# New section to display fruityvice API response
streamlit.header('FruityVice Fruite Advice!')

try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
    if not fruit_choice:
        streamlit.error('Please select a fruit to get information.')
    else:
            fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
            # Takes JSON response and normalize it and dataframe it
            fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
            streamlit.dataframe(fruityvice_normalized)
    streamlit.write('The user entered ', fruit_choice)
except URLError as e:
    streamlit.error



streamlit.stop()
# Open cursor with snowflake data
my_cur = my_cnx.cursor()
my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.text("The fruit load list contains:")
streamlit.dataframe(my_data_rows)

addFruit = streamlit.text_input('What fruit would you like to add?')
streamlit.write('Thanks for adding ', addFruit)
