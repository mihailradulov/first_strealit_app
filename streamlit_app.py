import streamlit
import pandas

streamlit.title('My parrents New Healthy Diner')
streamlit.header('Breakfast Favorites')
streamlit.text('🥣Omega 3 & Blueberry Datmeal')
streamlit.text('🥗Kale, Spinache & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Ranged Egg')
streamlit.text('🥑🍞Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
streamlit.dataframe(my_fruit_list)