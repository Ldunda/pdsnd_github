import time
import pandas as pd
import numpy as np
import math
import csv

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

def get_filters():
    """
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    city = ""
    month = ""
    day = 0
    filter_time = ""

    while city not in ['washington', 'new york', 'chicago']:
        city = input("Would you like to see data for Chicago, New York, or Washington?").lower() # get user input for city (chicago, new york city, washington).

    print("Looks like you want to hear about", city.title(), "! If this is not true, restart the program now!\n")

    while filter_time not in ["both", "none", "month", "day"]:
        filter_time = input("Would you like to filter the data by month, day, both, or not all? Type \"none\" for no time fiter.").lower()

    if filter_time == "month":
        while month not in ["january", "februray", "march", "april", "may", "june"]:
            month = input("Which moth? January, February, March, April, May, or June?").lower() # get user input for month (all, january, february, ... , june)
    elif filter_time == "day":
        while True:
            try:
                day = int(input("Which day? Please type your response as an integer (e.g., 1=Monday).")) # get user input for day of week (all, monday, tuesday, ... sunday)
                if day > 0 and day <= 7:
                    break
            except:
                print("Please enter a valid integer for the day of the week.")
    elif filter_time == "both":
        while month not in ["january", "february", "march", "april", "may", "june"]:
            month = input("Which moth? January, February, March, April, May, or June?").lower() # get user input for month (all, january, february, ... , june)
        while day < 1 or day > 7:
            day = int(input("Which day? Please type your response as an integer (e.g., 1=Monday)."))

     HINT: Use a while loop to handle invalid inputs

    print('-' * 40)
    return city, month, day, filter_time

def load_data(city, month, day, filter_time):
    print(filter_time)
    if city == "new york":
        city = "new york city"

    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    months = ['january', 'february', 'march', 'april', 'may', 'june']

    if filter_time == "both":
        month = months.index(month) + 1
        day = day - 1
        df = df[(df['Start Time'].dt.weekday == day) & (df['Start Time'].dt.month == month)]
    elif filter_time == "month":
        month = months.index(month) + 1
        df = df[df['Start Time'].dt.month == month]
    elif filter_time == "day":
        day = day - 1
        df = df[df['Start Time'].dt.weekday == day]

    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    months = ['January', 'February', 'March', 'April', 'May', 'June']

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_month = df['Start Time'].dt.month.mode()[0]
    print('Most popular month: ', months[most_month-1])

    # display the most common day of week
    most_week_day = int(df['Start Time'].dt.weekday.mode())
    print('Most popular day: ', days[most_week_day-1])

    # display the most common start hour
    most_hour = df['Start Time'].dt.hour.mode()[0]
    print('Most popular hour of day: ', most_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_start_station = df['Start Station'].mode()[0]
    print('Most commonly used start station: ', most_start_station)

    # display most commonly used end station
    most_end_station = df['End Station'].mode()[0]
    print('Most commonly used end station: ', most_end_station)

    # display most frequent combination of start station and end station trip
    most_startend_station = (df['Start Station'] + ' - ' + df['End Station']).mode()[0]
    print('Most commonly used start and end station duo: ', most_startend_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration = df['Trip Duration'].sum()
    print('Total Travel time: ', total_duration, ' sn')

    # display mean travel time
    print('Mean Travel Time: ', df['Trip Duration'].mean(), ' sn')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_user_type = df['User Type'].value_counts()
    print(count_user_type, "\n")

    if 'Gender' in df:
        # Display counts of gender
        count_gender = df['Gender'].value_counts()
        print(count_gender, "\n")

        # Display earliest, most recent, and most common year of birth
        oldest = df['Birth Year'].min()
        youngest = df['Birth Year'].max()
        most_birth_year = df['Birth Year'].mode()[0]
        print('Oldest, Youngest and most popular year of birth, respectively:\n ', oldest, youngest, most_birth_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def main():
    while True:
        city, month, day, filter_time = get_filters()
        df = load_data(city, month, day, filter_time)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        data_view = ""

        if city == "new york":
            city = "new york city"

        while data_view not in ["yes", "no"]:
            data_view = input("Would you like to view individual trip data? Type 'yes' or 'no'.\n").lower() # get user input for see raw data

        file = open(CITY_DATA[city], newline='')
        reader = csv.DictReader(file)

        while data_view == "yes":
            for i, row in enumerate(reader):
                if i % 5 == 0 and i > 0:
                    data_view = input("Would you like to view individual trip data? Type 'yes' or 'no'.\n").lower() # get user input for see more raw data
                    if data_view != "yes":
                        break
                print(row)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()