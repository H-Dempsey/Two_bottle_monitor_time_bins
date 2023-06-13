import pandas as pd
import numpy as np
import os

def replace_values(val,new_val):
    return(new_val)
def remove_prefix(val):
    return(int(val[2:]))
def last_nonnan_item(list1):
    if list1 is None:
        return(np.nan)
    nonnan_list = [num for num in list1 if pd.isna(num)==False]
    if len(nonnan_list) == 0:
        return(np.nan)
    else:
        return(nonnan_list[-1])
def add(val,time):
    return(val+time)

def clean_data(df):
    
    df = df.rename(columns={
        'MM:DD:YYYY hh:mm:ss':'Time',' LeftCount':'LeftCount',' LeftDuration':'LeftDuration',
        ' RightCount':'RightCount',' RightDuration':'RightDuration'})
    keep_cols = ['Time','LeftCount','LeftDuration','RightCount','RightDuration']
    df = df[keep_cols]
    df['Time'] = pd.to_datetime(df['Time'])

    return(df)

def edit_start_and_end_times(df, inputs):
    
    # Find the start and end times, if use initiation poke or use first/last 
    # timestamps is selected.          
    for time in ['Start time', 'End time']:
        
        if inputs[time+' type'] == 'Use custom time':
            # Convert the string to a datetime object.
            inputs[time] = pd.to_datetime(inputs[time])
        
        if time == 'Start time':
            if inputs[time+' type'] == 'Use first timestamp':
                inputs[time] = df.at[0,"Time"]
                    
        if time == 'End time':
            if inputs[time+' type'] == 'Use last timestamp':
                inputs[time] = df.at[len(df)-1,"Time"]
        
    # If the end time is before the first data point or the start time is after 
    # the last data point, throw an error.
    if inputs['End time'] < df.at[0,"Time"]:
        raise ValueError('\nThe end time is before the first data point in file '+inputs['Filename']+'.')
    elif inputs['Start time'] > df.at[len(df)-1,"Time"]:
        raise ValueError('\nThe start time is after the last data point in file '+inputs['Filename']+'.')
        
    return(inputs)

def remove_data_outside_window(df, inputs):
    
    # Remove the data before the start time and after the end time.
    del_indices = []
    for i in range(len(df)):
        if df.at[i,"Time"] < inputs['Start time']:
            del_indices.append(i)
        if df.at[i,"Time"] > inputs['End time']:
            del_indices.append(i)
    df = df.drop(del_indices)
    df.index = list(range(len(df)))
    
    return(df)
    
def find_time_bins(df, inputs):
    
    # Find the time bins.
        
    # Add a time column with the minutes since the start time.
    for i in range(len(df)):
        df.at[i,"Time (mins)"] = (df.at[i,"Time"]-inputs['Start time']).total_seconds() / 60
        
    # Create a list of the time bins.
    duration_mins = (inputs['End time'] - inputs['Start time']).total_seconds() / 60
    time_bins_labels = list(np.arange(0, duration_mins + inputs['Time bin (mins)'], inputs['Time bin (mins)']))
    time_bins_mins = [-inputs['Time bin (mins)']] + time_bins_labels
    
    # Add the bins to the dataframe.
    df['Time bins (mins)'] = pd.cut(df['Time (mins)'], time_bins_mins, 
                                    labels=time_bins_labels, right=True)
    
    # Group the data into time bins. At each bin, list all the values for pellet count for example.
    possible_cols = ['Time bins (mins)','LeftCount','LeftDuration','RightCount','RightDuration']
    output_cols = [col for col in possible_cols if col in df.columns]
    df_bins = df[output_cols].groupby("Time bins (mins)").agg(list)
    
    # For each bin, display the last non-nan value in each list.
    data_cols = output_cols.copy()
    data_cols.remove("Time bins (mins)")
    for col in data_cols:
        df_bins[col] = df_bins[col].apply(last_nonnan_item)
        
    # Fill in the nan values for empty lists.
    df_bins = df_bins.fillna(method="ffill")
    df_bins = df_bins.fillna(0)
    
    return(df_bins)

def add_additional_columns(df_ind, inputs):
    
    # Add in the columns for the time bins in minutes.  
    df_ind.insert(0, 'Time bins (mins)', df_ind.index)
    
    # Add in the corresponding columns for the dates and times.
    # If the number of rows in the dataframe is 0, return empty date and time
    # columns.
    float_index = df_ind.index
    if len(float_index) == 0:
        date_time_col = pd.DataFrame(columns=['Date','Time'])
    else:
        date_time_col = pd.Series(list(float_index))
        date_time_col = date_time_col.apply(pd.to_timedelta, unit='m')
        date_time_col = date_time_col.apply(add, time=inputs['Start time'])
        date_time_col = date_time_col.apply(pd.to_datetime).dt.round('1s')
        date = pd.Series(date_time_col.dt.date, name='Date')
        time = pd.Series(date_time_col.dt.time, name='Time')
        date_time_col = pd.concat([date,time], axis=1)
        date_time_col.index = list(float_index)
    df_ind = pd.concat([date_time_col, df_ind], axis=1)
    
    return(df_ind)

def analyse_FED_file(inputs):
    
    # Import the raw data.
    import_destination = os.path.join(inputs['Import location'], inputs['Filename'])
    df = pd.read_csv(import_destination)
    
    # Clean the data.
    df = clean_data(df)
    
    # Edit the start and end times.
    inputs = edit_start_and_end_times(df, inputs)
    
    # Remove the data before the start time and after the end time.
    df = remove_data_outside_window(df, inputs)
    
    # Find the time bins.
    df_bins = find_time_bins(df, inputs)
    
    # Add more columns to each dataframe.
    # These are time bins, date, time and pellet count changes.
    df_bins     = add_additional_columns(df_bins, inputs)
    
    # Export the data.
    export_name = 'Time bins for '+inputs['Filename'][:-4]+'.csv'
    export_destination = os.path.join(inputs['Export location'], export_name)
    df_bins.to_csv(export_destination, index=False)
        
    return(df_bins)
