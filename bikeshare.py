import time
import pandas as pd

# import numpy as np

CITY_DATA = {
    "chicago": "chicago.csv",
    "new york city": "new_york_city.csv",
    "washington": "washington.csv",
}
MONTHS = ["january", "february", "march", "april", "may", "june"]
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]


def get_input(input_label, help_label, input_options):
    """
    Helper function used inside 'get_filters' function.

    Args:
        (str) input_label: Message to be shown to the user for the filter input.
        (str) help_label: Message sent to the user in case of wrong input.
        (dict) input_options: Dictionary of input options to be chosen.
    Returns:
        (str) inpt: input option according to the user input.
    """
    while True:
        inpt = input(input_label).lower()
        if inpt == "help":
            print(help_label)
        elif inpt in input_options:
            break
        else:
            print("Sorry, wrong input.\n" + help_label)
    return inpt


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city: Name of the city to analyze
        (str) month: Name of the month to filter by, or "all" to apply no month filter
        (str) day: Name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let's explore some US bikeshare data!")

    # Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = get_input(
        "Please enter city name or [help]: ",
        "Possible values are [chicago], [new york city], [washington] or [all].",
        CITY_DATA,
    )

    # Get user input for month (all, january, february, ... , june)
    month = get_input(
        "Please enter month or [help]: ",
        "Possible values are [january], [february], [march], [april], [june] or [all].",
        MONTHS + ["all"],
    )

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    day = get_input(
        "Please enter day or [help]: ",
        "Possible values are [sunday], [monday], [tuesday], [wednesday], [thursday], [friday], [saturday] or [all].",
        DAYS + ["all"],
    )

    print("-" * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city: Name of the city to analyze
        (str) month: Name of the month to filter by, or "all" to apply no month filter
        (str) day: Name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df: Pandas DataFrame containing city data filtered by month and day
    """

    # Load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city], index_col=0)

    # Convert the Start Time, End Time and Trip Duration columns to datetime and timedelta types.
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["End Time"] = pd.to_datetime(df["End Time"])
    df["Trip Duration"] = pd.to_timedelta(df["Trip Duration"], unit="s")

    # Extract month and day of week from Start Time to create new columns
    df["month"] = df["Start Time"].dt.month_name().str.lower()
    df["day_of_week"] = df["Start Time"].dt.day_name().str.lower()

    # Filter by month if applicable
    if month != "all":
        # filter by month to create the new dataframe
        df = df[df["month"] == month]

    # Filter by day of week if applicable
    if day != "all":
        # filter by day of week to create the new dataframe
        df = df[df["day_of_week"] == day]

    return df


def show_raw_data(df):
    """
    Function responsible to show raw data 5 rows at a time.
    Keeps asking for confirmation to show increments of 5 rows until user enters [no] to stop.
    Is executed after loading the dataset and before computing the summary statitics.

    Args:
        df: Pandas DataFrame containing city data filtered by month and day
    Returns:
        nothing
    """

    print("Would you like to see the raw data?")
    while True:
        inpt = input("Please enter [y]es or [n]o: ").lower()
        if inpt in ["y", "n", "yes", "no"]:
            break
        else:
            print("Sorry, invalid value.")
    idx = 0
    if inpt in ["y", "yes"]:
        while True:
            print(df[idx : idx + 5])
            while True:
                cont = input("Would you like to continue? [y]es or [n]o: ").lower()
                if cont in ["y", "n", "yes", "no"]:
                    break
                else:
                    print("Sorry, invalid value.")
            if cont in ["y", "yes"]:
                idx += 5
            else:
                break


def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.

    Args:
        df: Pandas DataFrame containing city data filtered by month and day
    Returns:
        nothing
    """

    print("\nCalculating The Most Frequent Times of Travel...\n")
    start_time = time.time()

    # Display the most common month
    print("The most common month is: {}.".format(df["month"].mode()[0]))

    # Display the most common day of week
    print("The most common day of week is: {}.".format(df["day_of_week"].mode()[0]))

    # Display the most common start hour
    df["hour"] = df["Start Time"].dt.hour
    print("The most common hour is: {}.".format(df["hour"].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.

    Args:
        df: Pandas DataFrame containing city data filtered by month and day
    Returns:
        nothing
    """

    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()

    # Display most commonly used start station
    print(
        "The most commonly used start station is: {}.".format(
            df["Start Station"].mode()[0]
        )
    )

    # Display most commonly used end station
    print(
        "The most commonly used end station is: {}.".format(df["End Station"].mode()[0])
    )

    # Display most frequent combination of start station and end station trip
    top_comb_start_station, top_comb_end_station = (
        df[["Start Station", "End Station"]].value_counts().index[0]
    )
    print(
        "The most frequent combination of start station and end station trip is: {} to {}.".format(
            top_comb_start_station, top_comb_end_station
        )
    )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.

    Args:
        df: Pandas DataFrame containing city data filtered by month and day
    Returns:
        nothing
    """

    print("\nCalculating Trip Duration...\n")
    start_time = time.time()

    # Display total travel time
    print("The total travel time is: {}".format(df["Trip Duration"].sum()))

    # display mean travel time
    print("The mean travel time is: {}".format(df["Trip Duration"].mean()))

    if "User Type" in df.columns:
        print("Total travel time per user category:")
        user_types_total_travel_time_dict = (
            df.groupby(by="User Type")["Trip Duration"].sum().to_dict()
        )
        for k, v in user_types_total_travel_time_dict.items():
            print("  * {}: {}".format(k, v))
        print("Mean travel time per user category:")
        user_types_mean_travel_time_dict = (
            df.groupby(by="User Type")["Trip Duration"].mean().to_dict()
        )
        for k, v in user_types_mean_travel_time_dict.items():
            print("  * {}: {}".format(k, v))

    print("Mean travel time per hour of the day:")
    hour_mean_travel_time_dict = df.groupby(by="hour")["Trip Duration"].mean().to_dict()
    for k, v in hour_mean_travel_time_dict.items():
        print("  * {}: {}".format(k, v))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def user_stats(df):
    """
    Displays statistics on bikeshare users.

    Args:
        df: Pandas DataFrame containing city data filtered by month and day
    Returns:
        nothing
    """

    print("\nCalculating User Stats...\n")
    start_time = time.time()

    # Display user types count
    if "User Type" in df.columns:
        user_types_dict = df.groupby(by="User Type")["User Type"].count().to_dict()
        print("The users category and quantity are:")
        for k, v in user_types_dict.items():
            print("  * {}: {}".format(k, v))

    # Display gender count
    if "Gender" in df.columns:
        user_gender_dict = df.groupby(by="Gender")["Gender"].count().to_dict()
        print("The number of users by gender is:")
        for k, v in user_gender_dict.items():
            print("  * {}: {}".format(k, v))

    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in df.columns:
        print(
            "The earliest user birth year is: {}.".format(int(df["Birth Year"].min()))
        )
        print(
            "The most recent user birth year is: {}.".format(
                int(df["Birth Year"].max())
            )
        )
        print(
            "The most common user birth year is: {}.".format(
                int(df["Birth Year"].mode())
            )
        )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        # df = load_data("new york city", "april", "all")

        show_raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input("\nWould you like to restart? Enter [yes] or [no]:\n").lower()
        if restart.lower() != "yes":
            break


if __name__ == "__main__":
    main()
