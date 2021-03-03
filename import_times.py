import datetime
import json
import re


from zeiray.taskray import TaskRay

from zeiray.timeular import Timeular

def get_user_time_range():
    # You probably want last week.
    now = datetime.datetime.now()
    one_day = datetime.timedelta(days=1) # Want the end of yesterday
    yesterday = now - one_day
    yesterday.replace(hour = 0, minute=0, second=0, microsecond=0)

    start_time = yesterday
    txt = input("Enter start date YYYY-MM-DD [{}]: ".format(start_time.strftime("%Y-%m-%d")))
    if txt != '':
        start_time = datetime.datetime.strptime(txt, "%Y-%m-%d")
        
    end_time = yesterday
    txt = input("Enter end date YYYY-MM-DD [{}]: ".format(end_time.strftime("%Y-%m-%d")))
    if txt != '':
        end_time = datetime.datetime.strptime(txt, "%Y-%m-%d")
    end_time = end_time.replace(hour = 23, minute=59, second=59)
    return start_time, end_time


def init_timeular():
    # Read credentials
    with open('./timeular_creds.json') as json_file:
        data = json.load(json_file)
        apikey_value = data['apiKey']
        apisecret_value = data['apiSecret']

    timeular = Timeular(apikey_value, apisecret_value)
    return timeular    

# Return a dictionary key=activity ID value = taskray ID
def get_activities(timeular):
    raw_activities = timeular.activities.get()["activities"]
    activities = {}
    for activity in raw_activities:
        name = activity["name"]
        # Extract the Taskray ID from the name. The name will be something like
        # [#14141] [#ZDblah] Do some work [TR#a080800001X7Dii]
        m = re.match(r".*\[TR#(\w+)\]", name)
        if m is None:
            print(f"Unable to find TaskRay task ID in activity {name}")
        
        activities[activity["id"]] = m.group(1)
    return activities

# Returns a list of Time Entries
def get_entries(timeular, start_time, end_time):
    # Timestamp must match this format:
    # 2016-12-31T23:59:58.987"}
    start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%S.000")
    end_time_str = end_time.strftime("%Y-%m-%dT%H:%M:%S.000")
    print(f"Time string format {start_time_str}")
    entries = timeular.time_entries.get_in_range(start_time_str, end_time_str)["timeEntries"]
    return entries

def select_entries(entries):
    # Remove entries that have already been uploaded to TaskRay
    
    new_entries = list()
    for entry in entries:
        note_text = entry["note"]["text"]
        if note_text is None or "TRImported" not in note_text:
            new_entries.append(entry)

    return new_entries

def main():
    # Get user input
    start_time, end_time = get_user_time_range()

    # Slightly bizarre use of str here to print exactly what'll be requested from the API.
    print(f"start_time {str(start_time)} end_time {str(end_time)}")

    # Retrieve time entries for these ranges from the timeular API
    timeular = init_timeular()

    activities = get_activities(timeular)

    entries = get_entries(timeular, start_time, end_time)
    entries = select_entries(entries)

    tr = TaskRay()
    tr.login()

    for entry in entries:
        started_time = datetime.datetime.strptime(entry["duration"]["startedAt"][:-4], "%Y-%m-%dT%H:%M:%S")
        ended_time = datetime.datetime.strptime(entry["duration"]["stoppedAt"][:-4], "%Y-%m-%dT%H:%M:%S")
        task = activities[entry["activityId"]]

        success = tr.create_time_entry(task, started_time, ended_time)

        if success:
            patch_entry = {"note" : {"text" : "TRImported"}}
            response = timeular.time_entries.patch(entry["id"], patch_entry)
            print(response)
    

if __name__ == '__main__':
    main()