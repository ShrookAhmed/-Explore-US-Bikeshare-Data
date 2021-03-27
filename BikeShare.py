import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    print("Enter Chicago or New york city or Washington...\n")
    city=input("Please enter city to analyze: \n").lower()
    while city not in CITY_DATA.keys():
        print("Please check your input...\n")
        print("Enter Chicago or New york city or Washington...\n")
        city=input().lower() 
    MONTH_DATA = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'all': 7}
    print('remember availabe months are between Januaray and June')
    month=input("Please enter month to filter by or all to apply nofilter: \n").lower()
    
    while month not in MONTH_DATA.keys():
        print("Invalid input please check you enter valid input and remember availabe months are between Januaray and June")
        month=input().lower()
    DAY_LIST = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    print(DAY_LIST)
    day=input('please enter day to filter by or all to apply no filter: \n').lower()
    while day not in DAY_LIST:
        print("invalid day try again..\n")
        day = input().lower()
      
   

    print('-'*40)
    return city, month, day

    " " 
def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no dneway filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df=pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].apply(lambda x: x.month)
    df['day_of_week'] = df['Start Time'].apply(lambda x: x.strftime('%A').lower())
    months=['january','february','march','april','may','june']
    if month != 'all':
        month=months.index(month)+1
        df = df[df['month'] == month]

        
    if day != 'all':
       df = df[df['day_of_week'] == day]
    
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("Consider Months form Jan to June is 1:6")
    print('Common Month is',df['month'].mode()[0])

    # display the most common day of week
    print()
    print('Common day is',df['day_of_week'].mode()[0])

    # display the most common start hour
    df['Hour']=df['Start Time'].dt.hour
    print()
    print('Common start hour is',df['Hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_trip =df['Start Station'].mode()[0]
    print("Most Commonly Used Start Station is:",common_trip)

    # display most commonly used end station
    common_end_trip=df['End Station'].mode()[0]
    print("Most Commonly Used End Station is:",common_end_trip)

    # display most frequent combination of start station and end station trip
    df['Full Destination']= df['Start Station'].str.cat(df['End Station'],sep=' to ')
    common_destination=df['Full Destination'].mode()[0]
    print("Most Common Destination:",common_destination)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time=df['Trip Duration'].sum()
    minute, second = divmod(total_time, 60)
    hour, minute = divmod(minute, 60)
    minute=round(minute,1)
    second=round(second,1)

    print("Total time for trip take {} hour {} mins {} sec".format(hour,minute,second))
    
    # display mean travel time
    avg_time=df['Trip Duration'].mean()
    min,sec=divmod(avg_time, 60)
    min=round(min,1)
    sec=round(sec,1)
    if min>60:
        hour,min=divmod(min,60)
        min=round(min,1)
        print("Average time for trip is {} hour {} mins {} sec".format(hour,min,sec))
    else:
        print("Average time for trip is  {} mins {} sec".format(min,sec))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type=df.groupby(['User Type']).size()
    print("Counts of user types",user_type)

    # Display counts of gender
    if 'Gender' in df:
        gender_type=df.groupby(['Gender']).size()
        print("Count of each gender:\n",gender_type)
    else:
        print("Gender iis not available")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        
        common_year=int(df['Birth Year'].mode()[0])
        recent_year=int(df['Birth Year'].max())
        earliest_year=int(df['Birth Year'].min())
        print("Earliest year of birth is",earliest_year)
        print("Most common year of birth",common_year)
        print("Most recent year of birth ",recent_year)
    else:
       print(" Birth year is not available")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_rawdata(df):
    """Display row data based on user's opnion"""
    check = input("Would you like to see row data? Enter yes or no\n").lower()
    start_point =0
    if check =='yes':
     while True:
             print(df.iloc[start_point:start_point+5])
             print('---------------------------------------')
             start_point+=5
             check_more=input("Would you like to see more? Enter yes or no\n").lower()
             if check_more == 'no':
                   break
        
def main():
    while True:
        city, month, day = get_filters()
       
        df = load_data(city, month, day)
       # print(df.head())
        display_rawdata(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() == 'no':
            break
        if restart.lower() != 'yes' and restart.lower() != 'no':
            print("You entered invalid input O.o\n")
            print("Enter yes or no.\n")
            restart = input().lower()


if __name__ == "__main__":
	main()


