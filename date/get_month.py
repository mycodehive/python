"""
Description : This program prints the calendar of a given month.
Location : https://github.com/sahuni/python
Date : 2024.12.23
"""
import calendar

def print_month_calendar(year, month):
    try:
        # Create a plain text calendar
        cal = calendar.TextCalendar(calendar.SUNDAY)
        # Format the month as a string
        month_str = cal.formatmonth(year, month)
        print(month_str)
    except IndexError:
        print("Invalid month. Please enter a month between 1 and 12.")

if __name__ == "__main__":
    year = int(input("Enter year: "))
    month = int(input("Enter month: "))
    print_month_calendar(year, month)