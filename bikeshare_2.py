import time
import pandas as pd
import numpy as np
from collections import Counter
from termcolor import colored, cprint
import matplotlib.pyplot as plt
from plotnine import *
#from simple_colors import *

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

M_Dict = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june':6}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    cprint('Hello! Let\'s explore some US bikeshare data!', 'red', 'on_white',
           attrs=['dark', 'underline'])
    
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cprint('\nYou are required to enter one of these cities to explore; chicago, new york city, washington',
           'red', 'on_white', attrs=['blink'])

    city_names = ['chicago', 'new york city', 'washington']
    while True:
         city = cprint("Enter the city you want to explore: ", 'blue', attrs=['bold'])
         city = input()
         city = str(city).lower()
         found_city = False
         for i in city_names:
             if city == i:
                 found_city = True
         if found_city:
             break
         else:
             print('City is invalid, please enter chicago, new york city or washington')
       

    # get user input for month (all, january, february, ... , june)
    cprint("\nEnter either of these months to explore; [all, january, february,....., june]", 'red',
           'on_white',attrs=['blink'])
    
    month_names = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    while True:
         month = cprint("Enter the month you want to explore: ", 'blue', attrs=['bold'])
         month = input()
         month = str(month).lower()
         found_month = False
         for i in month_names:
             if month == i:
                 found_month = True
         if found_month:
             break
         else:
             print("Month is invalid, please enter ['all', 'january', 'february', 'march', 'april', 'may', 'june']")
    
    
    # get user input for day of week (all, monday, tuesday, ... sunday)    
    cprint("\nEnter either of these days to explore; [all, monday, tuesday,........,sunday]", 
           'red', 'on_white', attrs=['blink'])
    
    week_data = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'] 
    while True:
         day = cprint("Enter the day of the week you want to explore: ", 'blue',
                     attrs=['bold'])
         day = input()
         day = str(day).lower()
         found_day = False
         for i in week_data:
             if day == i:
                 found_day = True
         if found_day:
             break
         else:
             print("Day of week is invalid, please enter ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']")
    

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    
    #Covert Start Time column to datetime and splits it into month and weekday
    df = pd.read_csv(CITY_DATA[city])
    df.fillna(method='ffill', inplace = True)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name() #others use day_name()
    df['hour'] = df['Start Time'].dt.hour
   
    # filter by month if applicable
    if month != 'all':
       # use the index of the month dictionary to get the corresponding int
       df = df.loc[df['month'] == M_Dict[month]]


    # filter by day of week if applicable
    if day != 'all':
       df = df.loc[df['day_of_week'] == day.capitalize()]
    
    #Displays 5 lines of data based on user input
    while True:
        cprint('\nWould you like to see first 5 lines of the data? Enter yes or no.\n',
           'red', 'on_white', attrs=['blink'])
        View_Data = input()
        if View_Data.lower() != 'yes':
            break
        else:
            print(df.iloc[ :5])
        
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    cprint('\nCalculating The Most Frequent Times of Travel...\n', 'red', 'on_white', attrs=['blink'])
    start_time = time.time()
    
    # display the most common month
    split_it = df['month']
    Counters = Counter(split_it)
    most_occur = Counters.most_common(1) 
    print('Most common month is:\n[Month, Frequency]:', most_occur) 
    

    # display the most common day of week
    split_it = df['day_of_week']
    Counters = Counter(split_it)    
    most_occur = Counters.most_common(1)    
    print('\nThe travel mostly done on:\n[Day, Frequency]:', most_occur) 
    
  

    # display the most common start hour 
    split_it = df['hour'] 
    Counters = Counter(split_it)
    most_occur = Counters.most_common(1) 
    print('\nThe Start Hour is mostly:\n[Hour, Frequency]:', most_occur)
    print('.'*40)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    
    cprint('\nCalculating The Most Popular Stations and Trip...\n', 'red', 'on_white', attrs=['blink'])
    start_time = time.time()
        
    # display most commonly used start station  
    split_it = df['Start Station']
    Counters = Counter(split_it)
    most_occur = Counters.most_common(1) 
    print('Most common start station is:\n', most_occur) 
        
    # display most commonly used end station 
    split_it = df['End Station']
    Counters = Counter(split_it)
    most_occur = Counters.most_common(1) 
    print('\nMost common end station is:\n', most_occur) 

    # display most frequent combination of start station and end station trip
    Concate = df['End Station'] + ',' + ' ' + df['Start Station']
    Counters = Counter(Concate)
    most_occur = Counters.most_common(1) 
    print('\nMost common end and start stations are:\n', most_occur)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    cprint('\nCalculating Trip Duration...\n', 'red', 'on_white', attrs=['blink'])
    start_time = time.time()

    # display total travel time
    total_time = np.sum(df['Trip Duration'])
    print('\nTotal travel time is:' , total_time)

    # display mean travel time
    mean_time = np.mean(df['Trip Duration'])
    print('\nThe average travel time is:' , mean_time)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    #Ploting boxplot to identify for descriptives on trip_duration
    #green_diamond = dict(markerfacecolor='g', marker='D')
    '''fig1, ax1 = plt.subplots()
    ax1.set_title('Boxplot on Trip Duration')
    ax1.set_xlabel('Trip Duration')
    ax1.boxplot(df['Trip Duration'], ylim(50, 20000), showfliers=False, patch_artist=True)'''
    

def user_stats(df):
    """Displays statistics on bikeshare users."""

    cprint('\nCalculating User Stats...\n', 'red', 'on_white', attrs=['blink'])
    start_time = time.time()

    # Display counts of user types
    count_user = df['User Type'].value_counts()
    
    #count_user = np.count(df['User Type'])
    print('\nThe number of users are:\n', count_user)
    days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    df['day_of_week'] = pd.Categorical(df['day_of_week'], categories=days, ordered=True)

    # Create pointplots for three columns setting colors
    p = (ggplot(df)
         + geom_point(aes('day_of_week', 'Trip Duration', color='User Type'))+ ylim(0,20000))
    print(p)
    
    # Display counts of gender
    try:
        Gender_Count = df['Gender'].value_counts()
        print('\nThe number of male and females are:\n', Gender_Count)
        
        # Display earliest, most recent, and most common year of birth
        earliest_DOB = np.min(df['Birth Year'])
        Recent_DOB = np.max(df['Birth Year'])
        split_it = df['Birth Year']
        Counters = Counter(split_it)
        most_occur = Counters.most_common(1)
        print('\nThe earliest Birth Year is:\n', earliest_DOB)
        print('\nThe most recent Birth Year is:\n', Recent_DOB)
        print('\nThe most common Birth Year is:\n', most_occur)
    except KeyError:
        print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
