import re

def validate_pan(pan_number):
    pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]$'
    return re.match(pattern, pan_number) is not None

def validate_driving_licence(driving_licence_number):
    pattern = r'^[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}$' # Adjust regex based on driving licence formats
    return re.match(pattern, driving_licence_number) is not None
