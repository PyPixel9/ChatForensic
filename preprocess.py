import re 
import pandas 

def cleanse_data(df):
    df = df[df['message'] != '']
    df = df[~df['message'].str.contains("joined using this group's invite link")]
    df = df[~df['message'].str.contains("image omitted")]
    df = df.reset_index(drop=True)
    return df 

def split_date_time(text):
    text = text.split(',')
    date , time = text[0] , text[1]
    time = time.split('PM')
    time = time[0].strip()
    date = date.split('[')
    date = date[1].strip()
    return date + " " + time 

def preprocess(data):
    # splitting each line's data into date and the actual message sent 
    # format of msg: 
    # [28/07/22, 9:52:48 PM] ~ Parth Kaushal: this is a sample message out here
    date_time = r'\[\d{1,2}/\d{2}/\d{2,4},\s\d{1,2}:\d{1,2}:\d{1,2}\s(?:AM|PM)\]\s~\s'
    messages = re.split(date_time , data)[1:]
    dates = re.findall(date_time , data)
    # creating a pandas dataframe for it 
    df = pandas.DataFrame(
        {'user_messages' : messages, 
         'message_date' : dates}
        )
    df['message_date'] = df['message_date'].apply(lambda text : split_date_time(text))
    df.rename(columns = {'message_date' : 'date'} , inplace= True)
    #splitting each user's message into the user's name and their message in sperate columns of the dataframe 
    users = []
    messages = []
    for message in df['user_messages']:
        msg = re.split( '([\w\W]+?):\s' , message)
        if(len(msg) > 1):
            users.append(msg[1])
            messages.append(msg[2])
        else : 
            users.append("notification") 
            messages.append(msg[0])
    df['user'] = users 
    #removing \n from each message
    for i in range(0 , len(messages)):
        messages[i] = messages[i][:-1]
    df['message'] = messages 
    df = df.drop(['user_messages'] , axis = 1)
    df = df[['message' , 'date' , 'user']]
    for i in range(0 , len( df['date'])):
        df['date'][i] = df['date'][i][0:16] 

    # breaking to date , month , hour , minute , day , year
    df['month'] = pandas.to_datetime(df['date']).dt.month_name()
    df['year'] = pandas.to_datetime(df['date']).dt.year 
    df['day'] = pandas.to_datetime(df['date']).dt.day 
    df['day_name'] = pandas.to_datetime(df['date']).dt.day_name()
    df['hour'] = pandas.to_datetime(df['date']).dt.hour 
    df['minute'] = pandas.to_datetime(df['date']).dt.minute 
    df['date'] = pandas.to_datetime(df['date']).dt.date 

    df = cleanse_data(df)

    df = df[['user', 'date', 'day', 'day_name', 'month', 'year', 'hour', 'minute', 'message']]
    
    return df 