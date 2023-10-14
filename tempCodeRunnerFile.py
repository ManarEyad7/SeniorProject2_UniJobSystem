    
def calculate_duration(start_time, end_time):
    # Step 1: Convert to 24-hour format
    start_time = convert_to_24_hour(start_time)
    end_time = convert_to_24_hour(end_time)

    # Step 2: Convert to minutes
    start_minutes = convert_to_minutes(start_time)
    end_minutes = convert_to_minutes(end_time)

    # Step 3: Calculate duration
    if end_minutes < start_minutes:
        end_minutes += 24 * 60  # Add 24 hours' worth of minutes

    duration_minutes = end_minutes - start_minutes

    return duration_minutes

def convert_to_24_hour(time_str):
    time_str = time_str.strip()  # Remove leading and trailing spaces
    hour, minute = map(int, time_str[:-3].split(':'))
    am_pm = time_str[-2:].lower()

    if am_pm == 'pm':
        hour += 12

    return f'{hour:02d}:{minute:02d}'

def convert_to_minutes(time_str):
    hour, minute = map(int, time_str.split(':'))
    return hour * 60 + minute

def convert_minutes_to_hours(duration_minutes):
    hours = duration_minutes // 60
    minutes = duration_minutes % 60
    return hours
