import datetime
import googlemaps
from twilio.rest import Client

def get_commute_duration():
    home_address = "home address"
    work_address = "work address"
    
    google_maps_api_key = "api_key"
    gmaps = googlemaps.Client(key=google_maps_api_key)
    
    directions = gmaps.directions(home_address, work_address)
    first_leg = directions[0]["legs"][0]
    duration_text = first_leg["duration"]["text"]
    
    hours = 0
    minutes = 0
    for part in duration_text.split():
        if "hour" in part:
            hours = int(part[:-5])
        elif "min" in part:
            minutes = int(part[:-4])
    
    duration = datetime.timedelta(hours=hours, minutes=minutes)
    
    return duration

def send_text_message(message):
    twilio_account_sid = "sid"
    twilio_account_token = "token"
    twilio_phone_number = "twilio_number"
    own_number = "own_number"
    
    client = Client(twilio_account_sid, twilio_account_token)
    client.messages.create(
        to = own_number,
        from_ = twilio_phone_number,
        body = message
    )

def main():
    duration = get_commute_duration()
    
    now = datetime.datetime.now()
    arrival_time = now + duration.strftime("%I:%M %p")
    
    message = (
        f"Good morning!\n\n"
        f"Estimated commute time from home to work at 9 am: {duration}\n"
        f"Leave now for work at 9 am to arrive at approximately {arrival_time}.\n"
    )
    
    send_text_message(message)