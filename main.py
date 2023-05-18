import re 
import pandas 
import stats 
import preprocess 
import matplotlib.pyplot as mtp
import numpy as np 
import streamlit
import pandas 

# Setting up the streamlit web app 
streamlit.sidebar.title("Chat Analyzer")
chat_uploaded_by_user = streamlit.sidebar.file_uploader("Upload a text file")

if chat_uploaded_by_user is not None:
    bytes_datafile_of_chat = chat_uploaded_by_user.getvalue()

    #decoding the extracted datafile into a utf8 format 
    data = bytes_datafile_of_chat.decode("utf-8")

    df = preprocess.preprocess(data)
    # streamlit.dataframe(df)

    userlist = list(df['user'].unique())
    userlist.sort()
    userlist.insert(0 , "overall")

    selected_user = streamlit.sidebar.selectbox("Choose a person to analyze: " , userlist)

    #if show report button is clicked 
    if(streamlit.sidebar.button("Show Report")):
        streamlit.title("Chat forensics for: " + selected_user) 
        n_messages , n_words , n_media_shared , n_links_shared = stats.stats(selected_user , df)
        c1 , c2 , c3 , c4 = streamlit.columns(4)
        with c1: 
            streamlit.header("Total messages: ")
            streamlit.title(n_messages)
        with c2: 
            streamlit.header("Total words: ")
            streamlit.title(n_words)
        with c3: 
            streamlit.header("Media files shared: ")
            streamlit.title(n_media_shared)
        with c4: 
            streamlit.header("Number of links sent: ")
            streamlit.title(n_links_shared)
        if(selected_user != "overall"):
            streamlit.dataframe(df[df["user"] == selected_user])
            streamlit.title("Most common words used: ")
            streamlit.dataframe(stats.most_used_word(df , selected_user))
            streamlit.title("Emoji's used: ")
            streamlit.dataframe(stats.get_emoji_stats(df , selected_user))



        else : 
            streamlit.dataframe(df)
        

        if selected_user == "overall":
            streamlit.title("Most active users:")
            active_df = stats.most_active_users(df)
            streamlit.dataframe(active_df)

            


