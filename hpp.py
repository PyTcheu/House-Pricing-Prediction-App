import streamlit as st
import streamlit.components.v1 as stc

from eda_app import *
from ml_app import *

html_temp = """
		<div style="background-color:#3872fb;padding:10px;border-radius:10px">
		<h1 style="color:white;text-align:center;">House Pricing Prediction Sao Paulo </h1>
		</div>
		"""


def main():
    st.title('Main App')
    stc.html(html_temp)

    menu = ['Home','EDA','Predict Price','About']
    choice = st.sidebar.selectbox('Menu', menu)

    if choice == 'Home':
        st.subheader('Home')

    elif choice == 'EDA':
        run_eda_app()
    elif choice ==  'Predict Price':
        run_ml_app()
    elif choice == 'About':
        pass

if __name__ == '__main__':
    main()