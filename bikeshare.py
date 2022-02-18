import calendar
import time

import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filter_with_spaces(list):
    """Asks user for input and check it with the provided list."""

    list_str = ', '.join(list[:-1]) + ', or ' + list[-1]
    output = input('Would you like to see data for {}?\n'.format(list_str))

    # Change output to lowercase and remove ' ', '-', and '_'.
    output = output.lower().replace('-', '').replace('_', '').replace(' ', '')

    # Create a modified list with lowercase characters and without spaces.
    # Compare output with the first characters in each element in the modified list.
    # This allows the user to use abbreviations.
    while output not in [x.lower().replace(' ', '')[:len(output)] for x in list] or output == '':
        print('Invalid input.\n')
        output = input('Would you like to see data for {}?\n'.format(list_str))
        output = output.lower().replace('-', '').replace('_', '').replace(' ', '')
    output = list[[x.lower().replace(' ', '')[:len(output)] for x in list].index(output)]
    print('You chose {}.\n'.format(output))

    return output


def get_filter(list):
    """Asks user for input and check it with the provided list."""

    list_str = ', '.join(list[:-1]) + ', or ' + list[-1]
    output = input('Would you like to see data for {}?\n'.format(list_str)).lower()

    # Create a modified list with lowercase characters.
    # Compare output with the first characters in each element in the modified list.
    # This allows the user to use abbreviations.
    while output not in [x.lower()[:len(output)] for x in list] or output == '':
        print('Invalid input.\n')
        output = input('Would you like to see data for {}?\n'.format(list_str)).lower()
    output = list[[x.lower()[:len(output)] for x in list].index(output)]
    print('You chose {}.\n'.format(output))

    return output


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    cities = [x[:-4].replace('_', ' ').title() for x in CITY_DATA.values()]
    months = list(calendar.month_name)[1:7]
    days = list(calendar.day_name)
    filter_list = ['month', 'day', 'both', 'none']
    print('Hello! Let\'s explore some US bikeshare data!')

    # Get user input for city (chicago, new york city, washington).
    city = get_filter_with_spaces(cities)
    filter = get_filter(filter_list)

    # Get user input for month (all, january, february, ... , june) if applicable.
    if filter == 'month' or filter == 'both':
        month = get_filter(months)
    else:
        month = None

    # Get user input for day of week (all, monday, tuesday, ... sunday) if applicable.
    if filter == 'day' or filter == 'both':
        day = get_filter(days)
    else:
        day = None
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
    df = pd.read_csv(CITY_DATA[city.lower()])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month_name()
    df['Day'] = df['Start Time'].dt.day_name()
    if month:
        df = df[df['Month'] == month]
    if day:
        df = df[df['Day'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    if len(df['Month'].unique()) > 1:
        most_common_month = df['Month'].mode()[0]
        print('The most common month is {}'.format(most_common_month))

    # Display the most common day of week
    if len(df['Day'].unique()) > 1:
        most_common_day = df['Day'].mode()[0]
        print('The most common day of week is {}'.format(most_common_day))

    # Display the most common start hour
    print('The most common start hour is {}'.format(df['Start Time'].dt.hour.mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    print('The most commonly used start station is {}'.format(df['Start Station'].mode()[0]))

    # Display most commonly used end station
    print('The most commonly used end station is {}'.format(df['End Station'].mode()[0]))

    # Display most frequent combination of start station and end station trip
    most_frequent_combination = (df['Start Station'] + ' to ' + df['End Station']).mode()[0]
    print('The most frequent combination of start station and end station trip is from {}'.format(
        most_frequent_combination))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    print('The total travel time is {}'.format(df['Trip Duration'].sum()))

    # Display mean travel time
    print('The mean travel time is {}'.format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(df['User Type'].value_counts().to_frame())
    print()

    # Display counts of gender
    if 'Gender' in df.columns:
        print(df['Gender'].value_counts().to_frame())
        print()

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('The earliest year of birth is {}'.format(int(df['Birth Year'].min())))
        print('The most recent year of birth is {}'.format(int(df['Birth Year'].max())))
        print('The most common year of birth is {}'.format(int(df['Birth Year'].mode()[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(df):
    i = 0
    max_i = df.shape[0]
    n_columns = df.shape[1] - 2
    show_data = input('Would you like to see some raw data?').lower()
    while show_data in ['yes', 'y']:
        print(df.iloc[i:min(i+5, max_i), :n_columns])
        i += 5
        if i < max_i:
            show_data = input('Would you like to see some more raw data?').lower()
        else:
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
