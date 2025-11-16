# Import python packages
import streamlit as st
import pandas as pd
from snowflake.snowpark.functions import col,when_matched
from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.title(f"Customize your smoothie:ballon: {st.__version__}")
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
pending_orders = session.table("smoothies.public.orders").filter(col("ORDER_FILLED") == 0).collect()
if pending_orders:
    df = pd.DataFrame(pending_orders)

    # Display editable table
    editable_df = st.data_editor(df, num_rows="dynamic")

    submitted = st.button("Submit")

    if submitted:
        st.success("Someone clicked the button!", icon="👍")

        og_dataset = session.table("smoothies.public.orders")

        # Convert edited Pandas → Snowpark DataFrame
        edited_dataset = session.create_dataframe(editable_df)

        try:
            (
                og_dataset.merge(
                    edited_dataset,
                    (og_dataset["ORDER_UID"] == edited_dataset["ORDER_UID"]),
                    [
                        when_matched().update({
                            "ORDER_FILLED": edited_dataset["ORDER_FILLED"]
                        })
                    ]
                ).collect()
            )

            st.success("Order(s) updated!", icon="👍")

        except Exception as e:
            st.error("Something went wrong.")
            st.write(e)

else:
    st.success("There are no pending orders right now.", icon="👍")




