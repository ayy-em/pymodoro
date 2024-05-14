from screeninfo import get_monitors
import datetime


# Get screen dimensions
def get_window_geometry(window_width, window_height):
    screen = get_monitors()[0]
    screen_width = screen.width
    screen_height = screen.height
    geometry_string = f"{window_width}x{window_height}+{screen_width - window_width - 50}+{screen_height - window_height - 40}"
    return geometry_string


def format_time(time_in_seconds):
    time_delta = datetime.timedelta(seconds=time_in_seconds)
    # Convert timedelta to a datetime object with a base date
    base_date = datetime.datetime(1, 1, 1) + time_delta
    # Extract hours, minutes, and seconds from the datetime object
    hours = base_date.hour
    minutes = base_date.minute
    seconds = base_date.second
    if hours != 0:
        # Format to mm:ss
        formatted_time = "{:02d}:{:02d}".format(minutes, seconds)
    else:
        # Format the time as HH:mm:ss
        formatted_time = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
    return formatted_time
