import streamlit 
import os 
from mysql.connector import connect, Error

def authenticate(username , password):
    #CONNECTING DATABASE
    config = {
        'user': 'root',
        'password': 'Utkarsh@28505',
        'host': 'localhost',
        'database': 'chat_forensic',
        'auth_plugin': 'mysql_native_password'
    }
    try:
        connection = connect(**config)
        print("Connection established")
    except Error as e:
        print("An error occured in establishing connection :()", e) 
    c = connection.cursor()

    c.execute(f"SELECT password FROM authentication WHERE username = '{username}'")
    result = c.fetchall()
    if len(result)==0:
        c.close()
        return 0; 
    if(result[0][0]== password):
        c.close()
        return 1
    else : 
        c.close()
        return 0

streamlit.image("media_resources/loginpage_image.png" , width = 300)
streamlit.title("Welcome!")
streamlit.title("")
username = streamlit.text_input('Enter your username')
password = streamlit.text_input("Enter your password" , type="password")
if(streamlit.button("Login")):
    if(authenticate(username , password)==1):
        os.system("streamlit run main.py")
    elif(authenticate(username , password)==0) : 
        streamlit.error("Incorrect credentials! Please try again")