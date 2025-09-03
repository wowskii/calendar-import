import json
from ics import Calendar, Event
import html



def dict_to_ics(input_file, output_file):
    """
    Reads a dictionary from input_file and writes events to an ICS file.
    """
    # Load dictionary data from file
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Create a new calendar
    calendar = Calendar()
    
    for item in data:
        event = Event()
        event_data = item["description"].split("\r\n\r\n<br />\r\n\r\n")
        event_data = [html.unescape(x.replace("<br />", " ")) for x in event_data]
        if item["eventCategory"][-3:-1] == "TD" or item["eventCategory"][-3:-1] =="TP" or item["eventCategory"][-3:-1] =="CM":
            event.name = item["eventCategory"][-3:-1] + " " + event_data[1]
            event.location = event_data[2].replace("<br />", " ")
            event.description = event_data[-1] + item["modules"][0]
        else:
            event.name = event_data[0]
            event.location = event_data[1]
            event.description = event_data[-1]
        event.begin = item["start"]
        event.end = item["end"]
    
        calendar.events.add(event)
    
    # Write calendar to ICS file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(calendar)
    



dict_to_ics('data.json', 'output.ics')