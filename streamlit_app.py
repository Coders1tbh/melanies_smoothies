# Import python packages
import streamlit as st
import pandas as pd
from snowflake.snowpark.functions import col,when_matched
from snowflake.snowpark.context import get_active_session
import requests
# Write directly to the app
st.title(f"Customize your smoothie:cup_with_straw: {st.__version__}")
st.write(
  """Choose the fruit for your smoothie.
  """
)


#option = st.selectbox(
#    "What is your favourite fruit",
#    ("Bananas", "Strawberries", "Peaches"),
#)

#st.write("Your favourite fruit is: ", option)



name_on_order = st.text_input("Name of Smoothie:")
st.write("The name on your Smoothie will be", name_on_order)


session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)


ingredients_list = st.multiselect('Choose upto 5 ingredients: ', my_dataframe);
#pending_orders = session.table("smoothies.public.orders").filter(col("ORDER_FILLED") == 0).collect()



if ingredients_list:
    ingredients_string= ''



    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
#st.text(smoothiefroot_response.json())

        sf_df = st.dataframe(data = smoothiefroot_response.json(),use_container_width=True)
      
    st.write(ingredienta_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    #st.write(my_insert_stmt)

    if ingredients_string:
      session.sql(my_insert_stmt).collect()
      st.success('Your Smoothie is ordered!', icon="✅")




    
