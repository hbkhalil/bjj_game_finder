import numpy as np
import pandas as pd
import streamlit as st 
import pickle
from streamlit_gsheets import GSheetsConnection

clf = pickle.load(open('models/treepickle_file', 'rb'))  
# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)
  
def main(): 
    st.title("Submission Finder")
    html_temp = """
    <h2 style="color:white;text-align:center;">Submission Finder </h2>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html = True)
    
    gender = st.selectbox("Gender",["Female","Male"]) 
    weight = st.text_input("Weight","95") 
    height= st.text_input("Height","179") 
    fav_sub=st.text_input("High percentage submission")

    if st.button("Predict"): 
        
        data = {'height': int(height), 'weight': int(weight),'gender':gender }
        df=pd.DataFrame([list(data.values())], columns=[['height', 'weight','gender']])
        df['gender_num']=df['gender']=='Male'
        features=['height','weight','gender_num']
        X=df[features].to_numpy()      
        # X=scaler.transform(X)
        y=clf.predict(X)
        
        with open('Users_subs.csv','a') as fd:
            fd.write(f'{gender},{height},{weight},{fav_sub}')
            fd.write('\n')
            fd.close()

        
        st.success('Submission is {}'.format(y[0]))
      
if __name__=='__main__': 
    main()