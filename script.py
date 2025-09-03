import json
from ics import Calendar, Event
import html
from datetime import datetime
from zoneinfo import ZoneInfo  # Python 3.9+
import tzdata



def dict_to_ics(input_file, output_file):
    """
    Reads a dictionary from input_file and writes events to an ICS file.
    """
    # Load dictionary data from file
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Create a new calendar
    calendar = Calendar()
    paris_tz = ZoneInfo("Europe/Paris")
    
    for item in data:
        if "description" not in item or "eventCategory" not in item or not item.get("start") or not item.get("end"):
            continue  # skip incomplete entries
        event = Event()
        event_data = item["description"].split("\r\n\r\n<br />\r\n\r\n")
        event_data = [html.unescape(x.replace("<br />", " ")) for x in event_data]
        if item["eventCategory"][-3:-1] in ("TD", "TP", "CM"):
            event.name = item["eventCategory"][-3:-1] + " " + event_data[1]
            event.location = event_data[2].replace("<br />", " ")
            event.description = event_data[-1] + item["modules"][0]
        else:
            event.name = event_data[0]
            event.location = event_data[1]
            event.description = event_data[-1]
        event.begin = datetime.fromisoformat(item["start"]).replace(tzinfo=paris_tz)
        event.end = datetime.fromisoformat(item["end"]).replace(tzinfo=paris_tz)
        calendar.events.add(event)
    
    # Write calendar to ICS file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(calendar)
    



dict_to_ics('data.json', 'output.ics')