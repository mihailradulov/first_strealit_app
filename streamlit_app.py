import streamlit
import pandas
import snowflake.connector
import requests
from urllib.error import URLError

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
def get_fruityvice_data(this_fruit_choice):
     fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
     fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
     return fruityvice_normalized

streamlit.header('FruityVice Fruite Advice!')

try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
    if not fruit_choice:
        streamlit.error('Please select a fruit to get information.')
    else:
            
            streamlit.dataframe(get_fruityvice_data(fruit_choice))
    streamlit.write('The user entered ', fruit_choice)
except URLError as e:
    streamlit.error

# Snowflake related function
def get_fruit_load_list():
     my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
     with my_cnx.cursor() as my_cur:
          my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
          my_cnx.close()
          return my_cur.fetchall()

streamlit.header('View Our Fruit List - Add Your Favorites!')
# Add a button to load the fruits list
if streamlit.button('Get Fruit Load List'):
     streamlit.dataframe(get_fruit_load_list())

# Allow the end user to add fruit to the list
def insert_row_snowflake(new_fruit):
     my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
     with my_cnx.cursor() as my_cur:
          my_cur.execute("insert into public.fruit_load_list values ('" + new_fruit + "')")
          my_cnx.close()
          return 'Thanks for adding ' + new_fruit

add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add fruit to the list'):
     streamlit.write(insert_row_snowflake(add_my_fruit))
     
