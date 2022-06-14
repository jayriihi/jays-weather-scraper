#taking the wind portion of wind_swell_tide_for _sesh and rewriting as a function

import pandas as pd
import datetime
import requests
from datetime import timedelta


def get_sesh_wind(date_string,duration_string):

    # specify gsheet id and sheet name for URL
    gsheetid = "1VoVcckmhysjL6u1k1nsI6aU-FaPvhr8HIwa6vKFFazE"
    sheet_name = "30_Days_Pearl_data"
    gsheet_url = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(gsheetid, sheet_name)

    #Read gsheet into dataframe, rename columns and drop unused
    df = pd.read_csv(gsheet_url, skiprows = 2 )
    df.set_index ('Date/Time', inplace = True)
    df.rename(columns= {'Date/Time' :'date_time','Unnamed: 1' : 'wind_spd' , 'Unnamed: 2' : 'wind_max','Unnamed: 3' : 'wind_dir','Unnamed: 6' : 'date_code', 'Unnamed: 7' : 'time_code'}, inplace = True)
    df.drop({'Unnamed: 4','Unnamed: 5','date_code','time_code'}, axis=1, inplace =True)

    #df = df.set_index ('date_time', inplace = True)
    df.index = pd.to_datetime(df.index)


    #df = pd.index_datetime(df)
    #df.between_time('2021/10/31 21:50', '2021/10/31 21:30')
    #type('date_time')
    #type(df.index)
    #df

    #sesh_date = datetime.date(2022,5,1)
    #sesh_start_time = datetime.time(9,38)
    #sesh_start_datetime = datetime.datetime.combine(sesh_date, sesh_start_time)
    #print('sesh_start_time is', sesh_start_datetime)

    #add duration to start time to get end time
    #sesh_duration = timedelta(hours=+1, minutes=+5)
    #print ('sesh_duration is', sesh_duration)

    sesh_start_datetime = datetime.datetime.strptime(date_string, '%Y-%m-%dT%H:%M')

    sesh_start_date_str = datetime.datetime.strftime(sesh_start_datetime, '%d %b')
    sesh_start_time_str = datetime.datetime.strftime(sesh_start_datetime, '%-I:%M %p')
    #print (sesh_start_date_str)
    #print (sesh_start_time_str)

    duration_split = duration_string.split(',')
    #print (duration_split)
    h = int(duration_split[0])
    #print (type(h))
    m = int(duration_split[1])

    #print (m)

    #add duration to start time to get end time
    sesh_duration = timedelta(hours=+(h), minutes=+(m))
    #print ('sesh_duration is', sesh_duration)

    sesh_start_datetime + sesh_duration
    sesh_end_time = sesh_start_datetime + sesh_duration
    #print('sesh_end_time is', sesh_end_time)

    string_start_time = datetime.datetime.strftime(sesh_start_datetime,"%Y-%m-%d %H:%M")
    #print(string_start_time)
    string_end_time = datetime.datetime.strftime(sesh_end_time,"%Y-%m-%d %H:%M")
    #print(string_end_time)

    #get data for session time start and end using .loc
    sesh = df.sort_index().loc[string_start_time:string_end_time]
    #print(sesh)

    # get avg wind speed during session time and round to one decimal place
    avg_wind_spd = sesh["wind_spd"].mean()
    avg_wind_spd = round(avg_wind_spd, 1) 
    #print("The avg wind speed for this session is ",avg_wind_spd)

   
    #get max wind speed during session time
    wind_max=sesh['wind_max'].max()
    #print("The max wind speed for this session is ",wind_max)

    #get min wind speed during session time
    wind_min=sesh['wind_spd'].min()
    #print("The min wind speed for this session is ",wind_min)

    avg_wind_dir = get_avg_wind_dir(sesh['wind_dir'])
    avg_wind_dir = round(avg_wind_dir)

    return [avg_wind_spd, wind_max, wind_min,sesh_start_date_str,sesh_start_time_str,h,m,avg_wind_dir,sesh]

def get_avg_wind_dir(wind_dir_series):
    
    if  (wind_dir_series > 330 ).any() or (wind_dir_series < 30).any():
        low_test = wind_dir_series.where(wind_dir_series<180)
        rollovers = (low_test+360)
        hi_test = wind_dir_series.where(wind_dir_series>180)
        all360_test = rollovers.fillna(0) + hi_test.fillna(0)
        avg_n_wind_dir = all360_test.mean()
        avg_n_wind_dir = round(avg_n_wind_dir, 0)

        if avg_n_wind_dir >360:
            avg_n_wind_dir = (avg_n_wind_dir-360)

        print("The average wind direction for this session is ",avg_n_wind_dir)
        return (avg_n_wind_dir)    
    else:
        nn_avg_wind_dir = wind_dir_series.mean()
        nn_avg_wind_dir = round(nn_avg_wind_dir, 0) 
        print("The average wind direction for this session is  ",nn_avg_wind_dir)
        return (nn_avg_wind_dir)

#print(get_sesh_wind(datetime.date(2022,5,1), datetime.time(12,00), timedelta(hours=+1, minutes=+0)))

# get avg wind direction during session time 

#get avg wind direction when wind dir goes through 360deg


'''def get_avg_wind_dir ():
    
    if (sesh['wind_dir'] > 330 ).any() or (sesh['wind_dir'] < 30).any():
        low_test = sesh['wind_dir'].where(sesh['wind_dir']<180)
        rollovers = (low_test+360)
        hi_test = sesh['wind_dir'].where(sesh['wind_dir']>180)
        all360_test = rollovers.fillna(0) + hi_test.fillna(0)
        avg_n_wind_dir = all360_test.mean()
        avg_n_wind_dir = round(avg_n_wind_dir, 0)

        if avg_n_wind_dir >360:
            avg_n_wind_dir = (avg_n_wind_dir-360)

        print("The average wind direction for this session is ",avg_n_wind_dir)
    
    else:
        nn_avg_wind_dir = sesh['wind_dir'].mean()
        nn_avg_wind_dir = round(nn_avg_wind_dir, 0) 
        print("The average wind direction for this session is  ",nn_avg_wind_dir)
    return '''
