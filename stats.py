import emoji
from collections import Counter
import pandas 

def get_emoji_stats(df, selected_user):
    df = df[df['user'] == selected_user]
    emojis = []
    for i in df['message']:
        emojis.extend([c for c in i if emoji.is_emoji(c)])
    df_new = pandas.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    df_new = df_new.rename(columns = {0: "Emoji" , 1: "Times used" })
    return df_new



def most_used_word(df , selected_user):
    df = df[df['user']==selected_user]
    words = []
    for msg in df['message']:
        for word in msg.lower().split():
                words.append(word)
    most_common = pandas.DataFrame(Counter(words).most_common(20))
    most_common = most_common.rename(columns={0: 'Word', 1: 'Times Used'})
    return most_common

def stats(selected_user , df):
    # getting stats for particular person 
    if(selected_user != "overall"):
        df = df[df['user']== selected_user]
    
    #counting number of messages sent 
    number_of_messages_sent_all_time = len(df)

    #words sent 
    words = []
    for i in df['message']:
        words.extend(i.split())

    #number of media sent 
    n_media_shared = len(df[df['message'].str.contains("omitted")])
    print(n_media_shared)
    

    #number of links shared
    n_links_shared = len(df[df["message"].str.contains("https")]) + len(df[df["message"].str.contains("http")]) +  len(df[df["message"].str.contains("www")])
    
    return number_of_messages_sent_all_time , len(words) , n_media_shared , n_links_shared

def most_active_users(df):
    return df['user'].value_counts()
    