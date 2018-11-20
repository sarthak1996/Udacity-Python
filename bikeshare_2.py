import time
import pandas as pd
import numpy as np
import datetime
from os import system, name
import matplotlib.pyplot as plt
import sys

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

info_codes = ['SEVERITY_ERROR', 'CONTINUE_GRACEFULLY']

city_helper_dict = {'C': 'chicago', 'N': 'new york city', 'W': 'washington'}
month_helper_list = [
    'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT',
    'NOV', 'DEC'
]
days_helper_list = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']

filters_used = {
    'CITY': [],
    'MONTH': [],
    'DAY': [],
    'VISUAL': [],
    'VISUAL_SUB': []
}
size = 70
is_comma_separated = False
is_comma_separated_city = False
is_comma_separated_day = False
is_comma_separated_month = False

run_mode = 'main'


def clear():
    '''
    Function that clears the screen
    Args: None
    Returns: Nothing
    '''
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')
    # return


def printFiltersFormatted(phase='Filter Data'):
    '''
    Function to print formatted filters on top of terminal
    Args: (str) Phase -> displays which phase the code is going through
                    Expected values: Filter Data, Data Visualization, Load data
    Returns: Nothing
    '''
    clear()
    clear()
    clear()
    if phase == 'Filter Data' or phase == 'Data Visualization':
        print('PS: Case sensitivity has been disabled!'.center(size, ' '))
    print(('Phase: ' + phase).center(size, ':'))
    print('Filtering data based on following params'.center(size, '='))
    print('*' * size)
    city_filter = 'Included Cities: ' + str(
        format_city_name(filters_used['CITY']))
    print('*' + city_filter.center(size - 2, ' ') + '*')
    month_filter = 'Included Months: ' + str(
        format_city_name(filters_used['MONTH']))
    print('*' + month_filter.center(size - 2, ' ') + '*')
    day_filter = 'Included Days: ' + str(format_city_name(filters_used['DAY']))
    print('*' + day_filter.center(size - 2, ' ') + '*')
    visual_filter = 'Visualization type: ' + str(filters_used['VISUAL'])
    visual_filter_sub = 'Visualization subtype: ' + str(
        filters_used['VISUAL_SUB'])
    if phase == 'Data Visualization':
        print('*' + visual_filter.center(size - 2, ' ') + '*')
        print('*' + visual_filter_sub.center(size - 2, ' ') + '*')
    print('*' * size)
    print('\n\n')


def validateInputs(mode, value, validation_list=None):
    '''
        Function to validate input by user for city, month and day
        Args: (str) mode - determines which validation is fired
                    Expected values: CITY,MONTH,DAY
              (str) value - value entered by user
              (list) validation_list - validation list if values are comma separated
        Returns:
            message -> One element of info_codes or comma separated values, or correct value for user input
            (boolean) is_comma_separated -> If the input is comma separated
    '''
    global is_comma_separated
    value, is_comma_separated = validate_comma_separated_values(value, validation_list)
    if type(value) is str and value == info_codes[0]:
        return info_codes[0], None
    if is_comma_separated:
        return value, True
    if mode.upper() == 'CITY':
        if value.upper() == '':
            return info_codes[1], None
        elif value.upper() in city_helper_dict:
            return CITY_DATA[city_helper_dict[value.upper()]], None
        else:
            return info_codes[0], None
    elif mode.upper() == 'MONTH':
        if value.upper() == '':
            return info_codes[1], None
        elif value.upper() in month_helper_list:
            return month_helper_list.index(value.upper()) + 1, None
        else:
            return info_codes[0], None
    elif mode.upper() == 'DAY':
        if value.upper() == '':
            return info_codes[1], None
        elif value.upper() in days_helper_list:
            return days_helper_list.index(value.upper()), None
        else:
            return info_codes[0], None


def format_city_name(city):
    '''
    Prints city with first letter of every word capitalised with some additional formatting
    Args: (str/list) city: any string or list
    Returns: (str) every word's first letter capitalized string
    '''
    if type(city) is not str:
        city = '_,_'.join(city).replace('[', '').replace('{', '').replace(
            ']', '').replace('}', '')
    else:
        city = city.replace('[', '').replace('{', '').replace(']', '').replace(
            '}', '')
    return ' '.join(
        x.replace('.csv', '').capitalize() for x in city.split('_'))


def validate_comma_separated_values(values, validation_list):
    '''
    Function to check if values are comma separated and valid inputs.
    Args : (str) values: comma separated values
           (list) validation_list: list to check if values are valid
    Return:
        (list/str) An element from info_codes or list of values or value itself if not comma separated
        (boolean) if values is comma separated and valid
    '''
    validation_list = set(validation_list)
    if ',' in values:
        values = values.split(',')
        values = set(values)
        if values.issubset(validation_list):
            return list(values), True
        return info_codes[0], False
    else:
        return values, False


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    global is_comma_separated_month, is_comma_separated_day, is_comma_separated_city, is_comma_separated
    clear()
    clear()
    clear()
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print('\n' * 2)
    while 1:
        city = input(
            'Enter a city for which you would like to filter the data\n1. C for Chicago\n2. N for New York\n3. W for Washington,\n4. Hit enter (to disable filtering)\nYou can also enter comma separated values(example:C,N)\n\nPS: Case sensitivity has been disabled!\n\nEnter city: '
        )
        city = city.upper()
        message, is_comma_separated_city = validateInputs('CITY', city, list(city_helper_dict.keys()))

        if type(message) is str and message == info_codes[0]:
            printFiltersFormatted()
            print('ERROR'.center(size, '+'))
            print('City Mismatch!..Please enter the first letter of the city'.
                  center(size, ' '))
            print(''.center(size, '+'))
            print('\n\n')
        elif type(message) is str and message == info_codes[1]:
            city = None
            filters_used['CITY'].append(CITY_DATA[city_helper_dict['C']])
            filters_used['CITY'].append(CITY_DATA[city_helper_dict['N']])
            filters_used['CITY'].append(CITY_DATA[city_helper_dict['W']])
            printFiltersFormatted()
            break
        else:
            if is_comma_separated_city:
                print('Using ' + format_city_name(message) + ' as city...')
                city = message
                for c in city:
                    filters_used['CITY'].append(city_helper_dict[c])
            else:
                print('Using ' + format_city_name(message) + ' as city...')
                city = message
                filters_used['CITY'].append(city)
            printFiltersFormatted()
            break
        print('=' * size)
    # get user input for month (all, january, february, ... , june)
    while 1:
        print(
            'Choose months from the below list\nor\nHit enter (to disable filtering)'
        )
        print('\nYou can also enter comma separated values(example:Jan,Feb)')
        print(month_helper_list)
        month = input('\nEnter month: ')
        month = month.upper()
        message, is_comma_separated_month = validateInputs('MONTH', month, month_helper_list)
        if type(message) is str and message == info_codes[0]:
            printFiltersFormatted()
            print('ERROR'.center(size, '+'))
            print(
                'Month Mismatch!..Please enter only the first 3 letters of month!...'.
                center(size, ' '))
            print(''.center(size, '+'))
            print('\n\n')
        elif type(message) is str and message == info_codes[1]:
            print('Running without any filter on month')
            month = None
            filters_used['MONTH'].append('ALL')
            printFiltersFormatted()
            break
        else:
            if is_comma_separated_month:
                print('Using ' + format_city_name(message) + ' as month...')
                for m in message:
                    print(m)
                    filters_used['MONTH'].append(m)
                month = list(map(month_helper_list.index, message))
            else:
                print('Using ' + month_helper_list[message - 1] + ' as month...')
                month = message
                filters_used['MONTH'].append(month_helper_list[month - 1])
            printFiltersFormatted()
            break
        print('=' * size)
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while 1:
        print(
            'Choose days from the below list\nor\nHit enter (to disable filtering)'
        )
        print('\nYou can also enter comma separated values(example:Mon,Tue)')
        print(days_helper_list)
        print('\nYou can also enter comma separated values(example:Mon,Tue)')
        day = input("\nEnter day: ")
        day = day.upper()
        message, is_comma_separated_day = validateInputs('DAY', day, days_helper_list)
        if type(message) is str and message == info_codes[0]:
            printFiltersFormatted()
            print('ERROR'.center(size, '+'))
            print(
                'Day Mismatch!..Please enter only the first 3 letters of day!...'.
                center(size, ' '))
            print(''.center(size, '+'))
            print('\n\n')
        elif type(message) is str and message == info_codes[1]:
            print('Running without any filter on day')
            day = None
            filters_used['DAY'].append('ALL')
            printFiltersFormatted()
            break
        else:
            if is_comma_separated_day:
                print('Using ' + format_city_name(message) + ' as day...')
                for d in message:
                    filters_used['DAY'].append(d)
                day = message
            else:
                print('Using ' + days_helper_list[message] + ' as day...')
                day = days_helper_list[message]
                filters_used['DAY'].append(day)
            printFiltersFormatted()
            break
        print('=' * size)
    log('Exiting from get_filters with retvals:' + str(city) + ',' + str(month) + ',' + str(day))
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
    log('Entering load_data with :' + str(city) + ',' + str(month) + ',' + str(day))
    phase = 'Load Data'
    printFiltersFormatted(phase)
    print('Loading data!!...')
    df = pd.DataFrame()
    if city is not None:
        if is_comma_separated_city:
            df = []
            for city_alpha in city:
                df_temp = pd.read_csv(CITY_DATA[city_helper_dict[city_alpha]])
                df_temp['City'] = city_alpha
                if 'Gender' not in df_temp.columns:
                    df_temp['Gender'] = 'Not known'
                if 'Birth Year' not in df_temp.columns:
                    df_temp['Birth Year'] = 0
                df.append(df_temp)
            df = pd.concat(df, sort=False)
        else:
            df = pd.read_csv(city)
            df['City'] = city[0].upper()
    else:
        df1 = pd.read_csv(CITY_DATA[city_helper_dict['C']])
        df1['City'] = 'C'
        df2 = pd.read_csv(CITY_DATA[city_helper_dict['N']])
        df2['City'] = 'N'
        df3 = pd.read_csv(CITY_DATA[city_helper_dict['W']])
        df3['City'] = 'W'
        if 'Gender' not in df3.columns:
            df3['Gender'] = 'Not known'
        if 'Birth Year' not in df3.columns:
            df3['Birth Year'] = 0
        frames = [df1, df2, df3]
        df = pd.concat(frames, sort=False)
    log('After city filter')
    log(df.City.value_counts())
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    df['day_of_week_num'] = df['day_of_week']
    df['day_of_week'] = df['day_of_week'].apply(lambda x: days_helper_list[x])
    log(df['month'].value_counts())
    log(df['day_of_week'].value_counts())
    log(df['day_of_week_num'].value_counts())
    if is_comma_separated_month or is_comma_separated_day:
        df['is_included_in_filters'] = 0

    if month is not None:
        if is_comma_separated_month:
            log('Inside month filter loop.')
            for month_alpha in month:
                log(month_alpha)
                df.loc[df['month'] == month_alpha + 1, 'is_included_in_filters'] = 1
        else:
            df = df[df.month == month]
    if is_comma_separated_month:
        df = df[df.is_included_in_filters == 1]
        df['is_included_in_filters'] = 0
    log(df)
    if day is not None:
        if is_comma_separated_day:
            log('Inside day filter loop.')
            for day_alpha in day:
                log(day_alpha)
                df.loc[df['day_of_week'] == day_alpha, 'is_included_in_filters'] = 1
        else:
            df = df[df.day_of_week == day]
    log(df)
    if is_comma_separated_day:
        df = df[df.is_included_in_filters == 1]
    log('After month and day filter')
    log(df.month.value_counts())
    log(df.day_of_week.value_counts())
    log(None, wait=True)
    printFiltersFormatted(phase)
    print('Done!..Loading data completed without any errors')
    print('')
    _ = input('Press enter to continue..')
    # log(df)
    df.reset_index(inplace=True)
    # log('After reset_index')
    # log(df)
    df.drop('index', inplace=True, axis='columns')
    # log('After index column drop')
    # log(df)
    log(None, wait=True)
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
    print(
        str(most_common_hour - 12) + ":00 PM"
        if most_common_hour > 12 else str(most_common_hour) + ":00 AM")

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
    start_station_most_freq, stop_station_most_freq = df.groupby(
        ['Start Station',
         'End Station']).size().sort_values(ascending=False).index.values[0]

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
    total_dur = round(df['Trip Duration'].sum())

    total_dur_minute, total_dur_second = divmod(total_dur, 60)
    total_dur_hour, total_dur_minute = divmod(total_dur_minute, 60)
    total_dur_formatted_string = ''
    if total_dur_hour > 0:
        total_dur_formatted_string += ' {} hours'.format(total_dur_hour)
    if total_dur_minute > 0:
        total_dur_formatted_string += ' {} minutes'.format(total_dur_minute)
    if total_dur_second > 0:
        total_dur_formatted_string += ' {} seconds'.format(total_dur_second)
    total_dur_formatted_string += '.'

    print(total_dur_formatted_string)
    # display mean travel time

    print('Average trip duration is approximately :', end=' ')
    avg_dur = round(df['Trip Duration'].mean())

    avg_dur_minute, avg_dur_second = divmod(avg_dur, 60)
    avg_dur_hour, avg_dur_minute = divmod(avg_dur_minute, 60)
    avg_dur_formatted_string = ''
    if avg_dur_hour > 0:
        avg_dur_formatted_string += ' {} hours'.format(avg_dur_hour)
    if avg_dur_minute > 0:
        avg_dur_formatted_string += ' {} minutes'.format(avg_dur_minute)
    if avg_dur_second > 0:
        avg_dur_formatted_string += ' {} seconds'.format(avg_dur_second)
    avg_dur_formatted_string += '.'

    print(avg_dur_formatted_string)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    if 'Gender' not in df.columns:
        df['Gender'] = 'Not known'
    if 'Birth Year' not in df.columns:
        df['Birth Year'] = 0
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
    log(df)
    print('\nEarliest birth year in the data is:', end=' ')
    min_birth_year = int(df['Birth Year'].min())
    max_birth_year = int(df['Birth Year'].max())
    recent_birth_year = int(min(df["Birth Year"], key=lambda x: abs(x - now.year)))
    print(str(min_birth_year if min_birth_year != 0 else 'N.A.'))
    print('Most recent birth year in the data is:', end=' ')
    print(str(max_birth_year if max_birth_year != 0 else 'N.A.'))
    print('Closest birthday to current date is in', end=' ')
    print(str(recent_birth_year if recent_birth_year != 0 else 'N.A.'))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def plot_grouped_bar3(r1,
                      values,
                      colors,
                      labels,
                      xticks,
                      x_ax_label,
                      y_ax_label,
                      width=0.15,
                      display_val_over_bar=True,
                      xticks_rot=90):
    '''
    Function to plot a bar graph which has 3 bars in one group.
    Args: (list) r1 -> numeric values on x
          (list) values -> values on y
          (list) colors -> colors for the bars
          (list) xticks -> x-tick labels
          (str) x_ax_label -> x axis label
          (str) y_ax_label -> y axis label
          (float) width -> width of bar
          (boolean) display_val_over_bar -> boolean to toggle display of value of bar over bar
          (float) xticks_rot -> rotation of xtick labels in degrees
    Returns: Nothing
    '''
    ax = plt.subplot
    r2 = [x + width for x in r1]
    r3 = [x + width for x in r2]
    ax = plt.subplot()
    ax.bar(r1, values[0], color=colors[0], width=width, label=labels[0])
    ax.bar(r2, values[1], color=colors[1], width=width, label=labels[1])
    ax.bar(r3, values[2], color=colors[2], width=width, label=labels[2])
    plt.xticks(
        [r + width for r in range(len(r1))], xticks, rotation=xticks_rot)
    ax.legend()
    plt.xlabel(x_ax_label)
    plt.ylabel(y_ax_label)

    if display_val_over_bar:
        ytick_label, _ = plt.yticks()
        height = ytick_label[len(ytick_label) - 1] / len(ytick_label) / 5
        for i, val in enumerate(values[0]):
            val = int(val)
            if val == 0:
                continue

            plt.annotate(
                val, (r1[i], val + height),
                xytext=(0, 0),
                textcoords="offset points",
                va='center',
                ha='center')
        for i, val in enumerate(values[1]):
            val = int(val)
            if val == 0:
                continue

            plt.annotate(
                val, (r2[i], val + height),
                xytext=(0, 0),
                textcoords="offset points",
                va='center',
                ha='center')
        for i, val in enumerate(values[2]):
            val = int(val)
            if val == 0:
                continue

            plt.annotate(
                val, (r3[i], val + height),
                xytext=(0, 0),
                textcoords="offset points",
                va='center',
                ha='center')
    ax.autoscale_view()
    plt.show()


def visualize_user_types_in_city(df):
    '''
    Plot graph between total number of user types and city
    '''
    df['User Type'] = df['User Type'].fillna('Unknown')
    df_temp = df.groupby(['City'])['User Type'].value_counts()
    df_temp = df_temp.unstack(level=1).reset_index().rename_axis(None, axis=1)
    df_temp = df_temp.fillna(0)
    # print(df_temp)
    df_temp.loc[df_temp['City'] == 'C', 'City'] = 'Chicago'
    df_temp.loc[df_temp['City'] == 'W', 'City'] = 'Washington'
    df_temp.loc[df_temp['City'] == 'N', 'City'] = 'New York City'
    log(df_temp)
    for i in ['Customer', 'Dependent', 'Subscriber', 'Unknown']:
        if i not in df_temp.columns:
            df_temp[i] = 0
    plot_grouped_bar3(
        df_temp.index.values, [
            df_temp['Customer'].values, df_temp['Dependent'].values,
            df_temp['Subscriber'].values
        ], ['red', 'green', 'blue'], ['Customer', 'Dependent', 'Subscriber'],
        df_temp['City'].values,
        xticks_rot=0,
        x_ax_label='Cities',
        y_ax_label='Number of users')
    return


def visualize_user_counts_day_wise(df):
    '''
    Plot graph between average number of user types on days
    '''
    df['day_in_month'] = df['Start Time'].dt.day
    log('Inside visualize_user_counts_day_wise')
    df['User Type'] = df['User Type'].fillna('Unknown')
    log(df)
    # assumption data is provided for all days
    # Average is taken on the data provided not the actual days between min(start_time) and max(end_time)
    total_day_count_df = df.groupby(['day_of_week', 'month', 'day_in_month'])['day_of_week'].count()
    total_day_count_df = total_day_count_df.unstack(level=[1, 2]).reset_index().fillna(0)
    total_day_count_df.columns = list(range(len(total_day_count_df.columns)))
    total_day_count_df.set_index(0, inplace=True)
    total_day_count_df = total_day_count_df.gt(0).sum(axis='columns')
    total_day_count_df.index.name = 'day_of_week'
    df_temp = df.groupby(
        ['day_in_month', 'month', 'day_of_week',
         'day_of_week_num'])['User Type'].value_counts()
    df_temp = df_temp.unstack(level=4).reset_index().rename_axis(None, axis=1)
    df_temp = df_temp.groupby('day_of_week').sum()
    log(df_temp)
    log(total_day_count_df)
    df_temp = df_temp.div(total_day_count_df, axis=0).fillna(0)
    log(df_temp)

    df_temp.reset_index(inplace=True)
    for i in ['Customer', 'Dependent', 'Subscriber', 'Unknown']:
        if i not in df_temp.columns:
            df_temp[i] = 0
    for i, day in enumerate(days_helper_list):
        if day not in df_temp.day_of_week.values:
            df_temp.loc[df_temp.shape[0]] = [
                day, None, None, i, None, None, None, None
            ]
    df_temp.sort_values('day_of_week_num', inplace=True)
    df_temp = df_temp.fillna(0).reset_index()
    log(df_temp)

    plot_grouped_bar3(
        df_temp.index.values, [
            df_temp['Customer'].values, df_temp['Dependent'].values,
            df_temp['Subscriber'].values
        ], ['red', 'green', 'blue'], ['Customer', 'Dependent', 'Subscriber'],
        df_temp['day_of_week'].values,
        display_val_over_bar=False,
        x_ax_label='Days',
        y_ax_label='Average number of users')


def visualize_user_counts_month_wise(df):
    '''
    Plot graph between total number of user types in months
    '''
    df_temp = df.groupby('month')['User Type'].value_counts()
    df['User Type'] = df['User Type'].fillna('Unknown')
    df_temp = df_temp.unstack(level=1).reset_index().rename_axis(None, axis=1)
    log(df_temp)
    for i in ['Customer', 'Dependent', 'Subscriber', 'Unknown']:
        if i not in df_temp.columns:
            df_temp[i] = 0
    log(df_temp)
    for month in range(len(month_helper_list)):
        if (month + 1) not in df_temp.month.values:
            df_temp.loc[df_temp.shape[0]] = [month + 1, None, None, None, None]
    df_temp.sort_values('month', inplace=True)
    df_temp['month'] = df_temp['month'].apply(int)
    df_temp = df_temp.fillna(0).reset_index()
    # print(df_temp)
    log(df_temp)

    plot_grouped_bar3(
        df_temp.month.values - 1, [
            df_temp['Customer'].values, df_temp['Dependent'].values,
            df_temp['Subscriber'].values
        ], ['red', 'green', 'blue'], ['Customer', 'Dependent', 'Subscriber'],
        month_helper_list,
        width=0.25,
        display_val_over_bar=False,
        x_ax_label='Months',
        y_ax_label='Number of users')


def visualize_user_counts_hour_wise(df):
    '''
    Plot graph between average number of user types at hours
    '''
    df['day_in_month'] = df['Start Time'].dt.day
    df['User Type'] = df['User Type'].fillna('Unknown')
    total_hour_count_df = df.groupby(['hour', 'month', 'day_in_month'])['hour'].count()
    total_hour_count_df = total_hour_count_df.unstack(level=[1, 2]).reset_index().fillna(0)
    total_hour_count_df.columns = list(range(len(total_hour_count_df.columns)))
    total_hour_count_df.set_index(0, inplace=True)
    total_hour_count_df = total_hour_count_df.gt(0).sum(axis='columns')
    total_hour_count_df.index.name = 'hour'
    df['day_in_month'] = df['Start Time'].dt.day
    df_temp = df.groupby(['day_in_month', 'month',
                          'hour'])['User Type'].value_counts()
    df_temp = df_temp.unstack(level=3).reset_index().rename_axis(None, axis=1)

    df_temp = df_temp.groupby('hour').sum().fillna(0)
    df_temp.reset_index(inplace=True)
    hours = list(range(24))
    log(df_temp)
    for i in ['Customer', 'Dependent', 'Subscriber', 'Unknown']:
        if i not in df_temp.columns:
            df_temp[i] = 0
    for i, hour in enumerate(hours):
        if hour not in df_temp.hour.values:
            df_temp.loc[df_temp.shape[0]] = [
                hour, None, None, None, None, None, None
            ]
    df_temp.set_index('hour', inplace=True)
    log(df_temp)
    log(total_hour_count_df)
    df_temp = df_temp.div(total_hour_count_df, axis=0).fillna(0)
    log(df_temp)
    df_temp = df_temp.fillna(0).reset_index()
    log(df_temp)
    df_temp.sort_values('hour', inplace=True)

    log(df_temp)

    plot_grouped_bar3(
        df_temp.hour.values, [
            df_temp['Customer'].values, df_temp['Dependent'].values,
            df_temp['Subscriber'].values
        ], ['red', 'green', 'blue'], ['Customer', 'Dependent', 'Subscriber'],
        hours,
        display_val_over_bar=False,
        x_ax_label='Hours',
        y_ax_label='Average number of users')


def visualize_data(df):
    '''
    Function to call all the visualization functions with input handling
    '''
    phase = 'Data Visualization'
    choice = input(
        '\n\nWould you like to visualize the data? We have some awesome predefined visualizations!!(yes/no)'
    )
    if choice.lower() != 'yes':
        return
    print('[WARNING]: Visualization with filters would lead to filtered out values to be defaulted to 0!!')
    _ = input(
        '\nPress Enter to continue!!..Warning screen will be cleared once a key is pressed!!'
    )
    printFiltersFormatted(phase)
    while True:
        print('Here are some awesome visualizations:')
        print('\t1. User Count level')
        print('\t2. User Type level')
        print('\t3. To exit')
        print(
            '\nType in "desc 1" for description of choice 1, "desc 2" for choice 2\n\tor\nSimply type 1 to select choice 1'
        )
        print("\nPS: Don't include quotations")
        choice = input('Enter your choice: ')
        options = ['desc 1', 'desc 2', '1', '2', '3']
        choice = choice.lower()
        if (choice not in options):
            printFiltersFormatted(phase)
            print('ERROR'.center(size, '+'))
            print('Incorrect choice!'.center(size, ' '))
            print('Please choose from options below:'.center(size, ' '))
            print(str(options).center(size, ' '))
            print(''.center(size, '+'))
            print('\n\n')
        elif options.index(choice) < 2:
            if (options.index(choice) == 0):
                print(
                    'Visualize user counts Month wise, Day wise, Hour wise!!')
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
                    print(
                        'Choose from one below:\n1. Month wise\n2. Day wise\n3. Hour wise\n4. To exit visualization'
                    )
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
                        filters_used['VISUAL_SUB'].append('Hour wise')
                        printFiltersFormatted(phase)
                        visualize_user_counts_hour_wise(df)
                        filters_used['VISUAL_SUB'] = []
                        printFiltersFormatted(phase)

                    elif choice_2 == '4':
                        filters_used['VISUAL'] = []
                        printFiltersFormatted(phase)
                        break
                    else:
                        printFiltersFormatted(phase)
                        print('ERROR'.center(size, '+'))
                        print(
                            'Incorrect choice!!.. Please enter 1 or 2 or 3 or 4'.
                            center(size, ' '))
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
        try:
            df = load_data(city, month, day)
        except FileNotFoundError:
            print('ERROR'.center(size, '+'))
            print('Could not read the files specified!!..'.center(size, ' '))
            print('Please check the path!!'.center(size, ' '))
            print(''.center(size, '+'))
            print('\n\n')
            print('Exiting!!')
            return
        except:
            print('ERROR'.center(size, '+'))
            print('Load failed!!..'.center(size, ' '))
            print(('Exception: ' + sys.exc_info()[0].__name__).center(size, ' '))
            print(''.center(size, '+'))
            print('\n\n')
            print('Exiting!!')
            return
        if not (df.empty):
            log(df)
            print(
                '\nWish to see the raw data? Hit "Enter" to see and "No" to move on!!'
            )
            ch1 = input('Enter Choice:')
            if ch1 == '':
                print(df.head())
            _ = input('\nContinuing to next phase!!! Press Enter to continue')
            # print(df.columns)
            printFiltersFormatted('Stat Calculation')
            print('PS: There may be more than one most or least populars! We are only displaying one of them\n')
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
        else:
            printFiltersFormatted()
            print('ERROR'.center(size, '+'))
            print(
                'Unfortunately no data was found for the above chosen filters!!'.
                center(size, ' '))
            print(''.center(size, '+'))
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
            print(
                'Thanks for using this tool!! Hope you gained some insight on the data'
            )
            break
        filters_used = {
            'CITY': [],
            'MONTH': [],
            'DAY': [],
            'VISUAL': [],
            'VISUAL_SUB': []
        }
        is_comma_separated = False
        is_comma_separated_city = False
        is_comma_separated_day = False
        is_comma_separated_month = False
        df = None
        clear()
        clear()
        clear()


def log(message, wait=False):
    '''
    This method prints or waits till the input is entered only when testing the code
    '''
    if run_mode == 'test' and wait:
        input(message)
    elif run_mode == 'test':
        print(message)
    return


if __name__ == "__main__":
    run_mode = 'main'
    if len(sys.argv) == 2:
        if sys.argv[1] == 'test':
            run_mode = sys.argv[1]
            CITY_DATA = {'chicago': 'test_data/chicago.csv',
                         'new york city': 'test_data/new_york_city.csv',
                         'washington': 'test_data/washington.csv'}
    main()
