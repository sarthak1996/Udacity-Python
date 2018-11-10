import time
import pandas as pd
import numpy as np
import datetime
from os import system, name
import matplotlib.pyplot as plt


CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

info_codes = ['SEVERITY_ERROR', 'CONTINUE_GRACEFULLY']

city_helper_dict = {'C': 'chicago', 'N': 'new york city', 'W': 'washington'}
month_helper_list = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
days_helper_list = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']

filters_used = {'CITY': [], 'MONTH': [], 'DAY': [], 'VISUAL': [], 'VISUAL_SUB': []}
size = 70


def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')
    # return


def printFiltersFormatted(phase='Filter Data'):
    clear()
    clear()
    clear()
    if phase == 'Filter Data' or phase == 'Data Visualization':
        print('PS: Case sensitivity has been disabled!'.center(size, ' '))
    print(('Phase: ' + phase).center(size, ':'))
    print('Filtering data based on following params'.center(size, '='))
    print('*' * size)
    city_filter = 'Included Cities: ' + str(format_city_name(filters_used['CITY']))
    print('*' + city_filter.center(size - 2, ' ') + '*')
    month_filter = 'Included Months: ' + str(format_city_name(filters_used['MONTH']))
    print('*' + month_filter.center(size - 2, ' ') + '*')
    day_filter = 'Included Days: ' + str(format_city_name(filters_used['DAY']))
    print('*' + day_filter.center(size - 2, ' ') + '*')
    visual_filter = 'Visualization type: ' + str(filters_used['VISUAL'])
    visual_filter_sub = 'Visualization subtype: ' + str(filters_used['VISUAL_SUB'])
    if phase == 'Data Visualization':
        print('*' + visual_filter.center(size - 2, ' ') + '*')
        print('*' + visual_filter_sub.center(size - 2, ' ') + '*')
    print('*' * size)
    print('\n\n')


def validateInputs(mode, value):
    if mode.upper() == 'CITY':
        if value.upper() == '':
            return info_codes[1]
        elif value.upper() in city_helper_dict:
            return CITY_DATA[city_helper_dict[value.upper()]]
        else:
            return info_codes[0]
    elif mode.upper() == 'MONTH':
        if value.upper() == '':
            return info_codes[1]
        elif value.upper() in month_helper_list:
            return month_helper_list.index(value.upper()) + 1
        else:
            return info_codes[0]
    elif mode.upper() == 'DAY':
        if value.upper() == '':
            return info_codes[1]
        elif value.upper() in days_helper_list:
            return days_helper_list.index(value.upper())
        else:
            return info_codes[0]


def format_city_name(city):
    if type(city) is not str:
        city = '_ & _'.join(city).replace('[', '').replace('{', '').replace(']', '').replace('}', '')
    else:
        city = city.replace('[', '').replace('{', '').replace(']', '').replace('}', '')
    return ' '.join(x.replace('.csv', '').capitalize() for x in city.split('_'))


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    clear()
    clear()
    clear()
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print('\n' * 2)
    while 1:
        city = input('Enter a city for which you would like to filter the data\n1. C for Chicago\n2. N for New York\n3. W for Washington,\n4. Hit enter (to disable filtering)\n\nPS: Case sensitivity has been disabled!\n\nEnter city: ')
        city = city.upper()
        message = validateInputs('CITY', city)
        if message == info_codes[0]:
            printFiltersFormatted()
            print('ERROR'.center(size, '+'))
            print('City Mismatch!..Please enter the first letter of the city'.center(size, ' '))
            print(''.center(size, '+'))
            print('\n\n')
        elif message == info_codes[1]:
            print('Running without any filter on city...To check the data handling')
            city = None
            filters_used['CITY'].append(CITY_DATA[city_helper_dict['C']])
            filters_used['CITY'].append(CITY_DATA[city_helper_dict['N']])
            filters_used['CITY'].append(CITY_DATA[city_helper_dict['W']])
            printFiltersFormatted()
            break
        else:
            print('Using ' + format_city_name(message) + ' as city...')
            city = message
            filters_used['CITY'].append(city)
            printFiltersFormatted()
            break
        print('=' * size)
    # get user input for month (all, january, february, ... , june)
    while 1:
        print('Choose months from the below list\nor\nHit enter (to disable filtering)')
        print(month_helper_list)
        month = input('\nEnter month: ')
        month = month.upper()
        message = validateInputs('MONTH', month)
        if message == info_codes[0]:
            printFiltersFormatted()
            print('ERROR'.center(size, '+'))
            print('Month Mismatch!..Please enter only the first 3 letters of month!...'.center(size, ' '))
            print(''.center(size, '+'))
            print('\n\n')
        elif message == info_codes[1]:
            print('Running without any filter on month')
            month = None
            filters_used['MONTH'].append('ALL')
            printFiltersFormatted()
            break
        else:
            print('Using ' + month_helper_list[message - 1] + ' as month...')
            month = message
            filters_used['MONTH'].append(month_helper_list[month - 1])
            printFiltersFormatted()
            break
        print('=' * size)
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while 1:
        print('Choose days from the below list\nor\nHit enter (to disable filtering)')
        print(days_helper_list)
        day = input("\nEnter day: ")
        day = day.upper()
        message = validateInputs('DAY', day)
        if message == info_codes[0]:
            printFiltersFormatted()
            print('ERROR'.center(size, '+'))
            print('Day Mismatch!..Please enter only the first 3 letters of day!...'.center(size, ' '))
            print(''.center(size, '+'))
            print('\n\n')
        elif message == info_codes[1]:
            print('Running without any filter on day')
            day = None
            filters_used['DAY'].append('ALL')
            printFiltersFormatted()
            break
        else:
            print('Using ' + days_helper_list[message] + ' as day...')
            day = days_helper_list[message]
            filters_used['DAY'].append(day)
            printFiltersFormatted()
            break
        print('=' * size)
    return city, month, day


def load_data(city, month, day):
    global filters_used
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    phase = 'Load Data'
    printFiltersFormatted(phase)
    print('Loading data!!...')
    df = pd.DataFrame()
    if city is not None:
        df = pd.read_csv(city)
        df['City'] = city[0].upper()
    else:
        df1 = pd.read_csv(CITY_DATA[city_helper_dict['C']])
        df1['City'] = 'C'
        df2 = pd.read_csv(CITY_DATA[city_helper_dict['N']])
        df2['City'] = 'N'
        df3 = pd.read_csv(CITY_DATA[city_helper_dict['W']])
        df3['City'] = 'W'
        frames = [df1, df2, df3]
        df = pd.concat(frames, sort=False)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    df['day_of_week_num'] = df['day_of_week']
    df['day_of_week'] = df['day_of_week'].apply(lambda x: days_helper_list[x])

    if month is not None:
        df = df[df.month == month]
    if day is not None:
        df = df[df.day_of_week == day]
    printFiltersFormatted(phase)
    print('Done!..Loading data completed without any errors')
    print('')
    _ = input('Press enter to continue..')
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['hour'] = df['Start Time'].dt.hour
    # display the most common month
    print('Most common month is:', end=' ')
    print(month_helper_list[df['month'].mode()[0] - 1])
    # display the most common day of week
    print('Most common day of week is:', end=' ')
    print(df['day_of_week'].mode()[0])
    # display the most common start hour
    most_common_hour = df['hour'].mode()[0]
    print('Most common hour is:', end=' ')
    print(str(most_common_hour - 12) + ":00 PM" if most_common_hour > 12 else str(most_common_hour) + ":00 AM")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # print(df.columns)
    # display most commonly used start station
    print('Most commonly Used Start Station:', end=' ')
    print(df['Start Station'].mode()[0])
    # display most commonly used end station
    print('Most commonly Used End Station:', end=' ')
    print(df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    start_station_most_freq, stop_station_most_freq = df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False).index.values[0]
    print('Most frequent combination of start and stop station is: (', end=' ')
    print(start_station_most_freq + ' , ' + stop_station_most_freq, end=' ')
    print(')')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total trip duration is :', end=' ')
    print(str(df['Trip Duration'].sum()), end=' ')
    print('units.')
    # display mean travel time
    print('Average trip duration is :', end=' ')
    print('Average trip duration is : ' + str(df['Trip Duration'].mean()), end=' ')
    print('units.')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Stats for User Types in the data'.center(size, '='))
    print()
    print(df['User Type'].value_counts().to_string())
    # Display counts of gender
    print('\n')
    print('Stats for Gender in the data'.center(size, '='))
    print()
    print(df['Gender'].value_counts().to_string())
    # Display earliest, most recent, and most common year of birth
    now = datetime.datetime.now()
    print('\n')
    print('Stats for Birth year in the data'.center(size, '='))
    print('\nEarliest birth year in the data is:', end=' ')
    print(str(df['Birth Year'].min()))
    print('Most recent birth year in the data is:', end=' ')
    print(str(df['Birth Year'].max()))
    print('Closest birthday to current date is in', end=' ')
    print(str(min(df["Birth Year"], key=lambda x: abs(x - now.year))))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def visualize_user_types_in_city(df):
    df_temp = df.groupby(['City'])['User Type'].value_counts()
    df_temp = df_temp.unstack(level=1).reset_index().rename_axis(None, axis=1)
    barWidth = 0.25
    r1 = df_temp.index.values
    r2 = [x + barWidth for x in r1]
    r3 = [x + barWidth for x in r2]
    ax = plt.subplot()

    ax.bar(r1, df_temp['Customer'].values, color='blue', width=barWidth, edgecolor='white', label='Customer')
    ax.bar(r2, df_temp['Dependent'].values, color='red', width=barWidth, edgecolor='white', label='Dependent')
    ax.bar(r3, df_temp['Subscriber'].values, color='green', width=barWidth, edgecolor='white', label='Subscriber')
    plt.xticks([r + barWidth for r in range(len(r1))], df_temp['City'].values)
    ax.legend()

    for i, val in enumerate(df_temp['Customer'].values):
        plt.annotate(val, (r1[i], val + 2), xytext=(0, 5), textcoords="offset points", va='center', ha='center')
    for i, val in enumerate(df_temp['Dependent'].values):
        plt.annotate(val, (r2[i], val + 2), xytext=(0, 5), textcoords="offset points", va='center', ha='center')
    for i, val in enumerate(df_temp['Subscriber'].values):
        plt.annotate(val, (r3[i], val + 2), xytext=(0, 5), textcoords="offset points", va='center', ha='center')

    ax.autoscale_view()
    plt.show()
    # df_temp.plot.bar(x='City', y=['Customer', 'Dependent', 'Subscriber'])
    return


def visualize_user_types_birth_year(df):
    df_temp = df.groupby(['Birth Year'])['User Type'].value_counts()
    df_temp = df_temp.unstack(level=1).reset_index().rename_axis(None, axis=1)
    # to write plot logic here
    return


def visualize_user_counts_day_wise(df):
    df['day_in_month'] = df['Start Time'].dt.day
    df_temp = df.groupby(['day_in_month', 'month', 'day_of_week', 'day_of_week_num'])['User Type'].value_counts()
    df_temp = df_temp.unstack(level=4).reset_index().rename_axis(None, axis=1)
    df_temp = df_temp.groupby('day_of_week').mean()
    df_temp.sort_values('day_of_week_num', inplace=True)
    ax = plt.subplot()

    plt.plot(df_temp['day_of_week'].values, df_temp['Customer'].values, color='blue', label='Customer')
    plt.plot(df_temp['day_of_week'].values, df_temp['Dependent'].values, color='red', label='Dependent')
    plt.plot(df_temp['day_of_week'].values, df_temp['Subscriber'].values, color='green', label='Subscriber')

    ax.legend()
    ax.autoscale_view()
    plt.show()


def visualize_user_counts_month_wise(df):
    df_temp = df.groupby('month')['User Type'].value_counts()
    df_temp = df_temp.unstack(level=1).reset_index().rename_axis(None, axis=1)
    ax = plt.subplot()

    plt.plot(df_temp['month'].values, df_temp['Customer'].values, color='blue', label='Customer')
    plt.plot(df_temp['month'].values, df_temp['Dependent'].values, color='red', label='Dependent')
    plt.plot(df_temp['month'].values, df_temp['Subscriber'].values, color='green', label='Subscriber')

    plt.xticks(df_temp['month'].values, month_helper_list)
    ax.legend()
    ax.autoscale_view()
    plt.show()


def visualize_data(df):
    phase = 'Data Visualization'
    choice = input('\n\nWould you like to visualize the data? We have some awesome predefined visualizations!!(yes/no)')
    if choice != 'yes':
        return
    _ = input('Press Enter to continue!!..Warning screen will be cleared once a key is pressed!!')
    printFiltersFormatted(phase)
    while True:
        print('Here are some awesome visualizations:')
        print('\t1. User Count level')
        print('\t2. User Type level')
        print('\t3. To exit')
        print('\nType in "desc 1" for description of choice 1, "desc 2" for choice 2\n\tor\nSimply type 1 to select choice 1')
        print("\nPS: Don't include quotations")
        choice = input('Enter your choice: ')
        options = ['desc 1', 'desc 2', '1', '2', '3']
        choice = choice.lower()
        if(choice not in options):
            printFiltersFormatted(phase)
            print('ERROR'.center(size, '+'))
            print('Incorrect choice!'.center(size, ' '))
            print('Please choose from options below'.center(size, ' '))
            print(str(options).center(size, ' '))
            print(''.center(size, '+'))
            print('\n\n')
        elif options.index(choice) < 2:
            if(options.index(choice) == 0):
                print('Visualize user counts Month wise, Day wise, Hour wise!!')
            else:
                print('Visualize user types city wise!!')
            _ = input('Press Enter to continue!!..')
            printFiltersFormatted(phase)
            continue
        else:
            if options.index(choice) == 2:
                filters_used['VISUAL'].append('User Count')
                printFiltersFormatted(phase)
                while True:
                    print('Choose from one below:\n1. Month wise\n2. Day wise\n3. Hour wise\n4. To exit visualization')
                    choice_2 = input('Enter your choice (1 or 2 or 3 or 4): ')
                    if choice_2 == '1':
                        filters_used['VISUAL_SUB'].append('Month wise')
                        printFiltersFormatted(phase)
                        visualize_user_counts_month_wise(df)
                        filters_used['VISUAL_SUB'] = []
                        printFiltersFormatted(phase)
                    elif choice_2 == '2':
                        filters_used['VISUAL_SUB'].append('Day wise')
                        printFiltersFormatted(phase)
                        visualize_user_counts_day_wise(df)
                        filters_used['VISUAL_SUB'] = []
                        printFiltersFormatted(phase)
                    elif choice_2 == '3':
                        # write function
                        break
                    elif choice_2 == '4':
                        filters_used['VISUAL'] = []
                        printFiltersFormatted(phase)
                        break
                    else:
                        printFiltersFormatted(phase)
                        print('ERROR'.center(size, '+'))
                        print('Incorrect choice!!.. Please enter 1 or 2 or 3 or 4'.center(size, ' '))
                        print(''.center(size, '+'))
                        print('\n\n')
            if options.index(choice) == 3:
                filters_used['VISUAL'].append('User Type')
                printFiltersFormatted(phase)
                visualize_user_types_in_city(df)
                filters_used['VISUAL'] = []
                printFiltersFormatted(phase)
            if options.index(choice) == 4:
                filters_used['VISUAL'] = []
                break

    return


def main():
    global filters_used
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        print('\nWish to see the raw data? Hit "Enter" to see and "No" to move on!!')
        ch1 = input('Enter Choice:')
        if ch1 == '':
            print(df.head())
        _ = input('Continuing to next phase!!! Press Enter to continue')
        # print(df.columns)
        printFiltersFormatted('Stat Calculation')
        print('*' * size)
        print('*' + ('Time Stats'.center(size - 2, " ")) + '*')
        print('*' * size)
        time_stats(df)
        print('*' * size)
        print('*' + ('Station Stats'.center(size - 2, " ")) + '*')
        print('*' * size)
        station_stats(df)
        print('*' * size)
        print('*' + ('Trip Duration Stats'.center(size - 2, " ")) + '*')
        print('*' * size)
        trip_duration_stats(df)
        print('*' * size)
        print('*' + ('User Stats'.center(size - 2, " ")) + '*')
        print('*' * size)
        user_stats(df)

        visualize_data(df.copy())

        print('\n')
        print('=' * size)
        print('Done'.center(size, '*'))
        print('=' * size)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            clear()
            clear()
            clear()
            print('Successful exit!'.center(size, '-'))
            print('Thanks for using this tool!! Hope you gained some insight on the data')
            break
        filters_used = {'CITY': [], 'MONTH': [], 'DAY': [], 'VISUAL': [], 'VISUAL_SUB': []}
        clear()
        clear()
        clear()


if __name__ == "__main__":
    main()
