import requests, datetime, sys

# Functions

def get_date_time() -> tuple:
    """

    Returns:
        tuple(int, str): a tuple in the format (0, "time") where "0" is the day and time is the current military time, e.g. "15:00"

    """
    
    current_dt = datetime.datetime.now()

    current_day = current_dt.isoweekday() % 7 # mod by 7 make sure Sunday's integer value is consistent with the Food Truck API
    current_hour = current_dt.hour
    current_min = current_dt.minute
    
    current_time_str = "{}:{}".format(current_hour, current_min)

    return (current_day, current_time_str)

def build_url(current_day: int) -> str: # returns a string that represents the base Food Truck URL concatenated with any Query Parameter strings
    """

    Args:
        current_day (int): an integer representing the current day. For example, 7 represents Sunday, 1 represents Monday, etc.

    Returns:
        str: a string representing the base Food Truck URL concatenated with any query parameters

    """
        
    base_url = "http://data.sfgov.org/resource/bbb8-hzi6.json"

    # Query Params
    
    filter_by_day = "?dayorder={}".format(current_day)

    return "{}{}".format(base_url, filter_by_day)

# Main

def main():

    day, current_time = get_date_time()
    full_url = build_url(day)

    try:
        response = requests.get(full_url)

        if response.status_code == 200:
            vendors_data = response.json()
            vendors_data.sort(key = lambda x: x["applicant"]) # sort by the 'applicant' field (assuming this is the name of the Food Truck Vendor)

            index = 0 # the index of the current Vendor we are looking at
            vendors_displayed_so_far = 0
            
            display_more = True
            
            while display_more:
                try: # use a try-except statement to avoid checking the length of the entire response
                    if vendors_displayed_so_far < 10:
                        if vendors_data[index]["start24"] <= current_time <= vendors_data[index]["end24"]: # if the current time is in between a vendor's opening and closing hours
                            print("{} {}".format(vendors_data[index]["applicant"], vendors_data[index]["location"]))
                            vendors_displayed_so_far += 1
                        index += 1
                    else:
                        ask_for_input = True
                        while ask_for_input:
                            user_input = input("\nShow more rows? Enter 'Yes' or 'No' ")
                            
                            if user_input.lower() == "yes":
                                ask_for_input = False
                                vendors_displayed_so_far = 0
                            elif user_input.lower() == "no":
                                ask_for_input = False
                                display_more = False
                                
                            else:
                                print("\nYou didn't enter 'Yes' or 'No'. Try again!")
                except IndexError as e: # there are no more Food Trucks to display
                    print("\nNo more restauraunts to find. That's it!\n")
                    break
        else:
            sys.exit("Server responded with status code {} instead of 200.".format(response.status_code))

    # Exception Handling
    
    except requests.exceptions.HTTPError as e:
        print("An HTTP Error occurred with the following message: {}".format(e))
        sys.exit(1)
    except requests.exceptions.ConnectionError as e:
        print("A Connection Error occurred with the following message: {}".format(e))
        sys.exit(1)
    except requests.exceptions.ConnectTimeout as e:
        print("A Connect Timeout Error (request timed out while trying to connect to the server) occurred with the following message: {}".format(e))
        sys.exit(1)
    except requests.exceptions.ReadTimeout as e:
        print("A Read Timeout Error (server did not send any data in the allotted amount of time) occurred with the following message: {}".format(e))
        sys.exit(1)
    except requests.exceptions.URLRequired as e:
        print("A URL Required Error (invalid URL) occurred with the following message: {}".format(e))
        sys.exit(1)
    except requests.RequestException as e:
        print("An ambiguous Request Exception Error occurred: {}".format(e))
        sys.exit(1)

if __name__ == "__main__":
    main()
