from datetime import datetime, timedelta
import datefinder



###############################

def call_google_calendar_func(arg_dict = arg_dict_1_formatted, function_name = function_name_1,flag_add_new_info = False):
	
	options = {
	'create_event': create_event(arg_dict),
	'delete_event': delete_event(arg_dict),
    'get_calendar_events': get_calendar_events(arg_dict),
    'get_free_busy_info': get_free_busy_info(arg_dict),
    'update_event': update_event(arg_dict),
    'reschedule_event': reschedule_event(arg_dict)
    }

	if flag_add_new_info == True:
		print('need more information')
		
	else: # all required arguments are here
		if function_name in options:
			options[function_name]()
		else:
			print('no function called')

###############################
###############################



def create_event(arg_dict):
	#NEW! duration=[0,1,0]
	#['summary', 'start_time', 'end_time', 'location'] 
	summary = arg_dict['SUMMARY']
	start_time = arg_dict['START_TIME']
	end_time = arg_dict['END_TIME']
	location = [arg_dict['location'] if 'LOCATION' in arg_dict]

    event = {
        'summary': summary,
        'location': location,
        
        'start': {
            'dateTime': start_time, 
            'timeZone': 'America/Toronto',
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'America/Toronto',
        },

    }

    result = service.events().insert(calendarId='primary', body=event).execute()
    #'status': 'confirmed'

    return result['status'] 



def delete_event(arg_dict):
    # 'event_id'
    event_id = arg_dict['EVENT_ID']


    # if event_id == '': #get event id by calling get_event function
    # 	events = get_calendar_events(date, start_time = '00:00:00', end_time = '23:59:59')



    result = calendar_service.events().delete(calendarId='primary', eventId=event_id).execute()
    return result['status']





def get_calendar_events(arg_dict):



	date = arg_dict['date']
	start_time = [arg_dict['START_TIME'] if 'START_TIME' in arg_dict]
	end_time = [arg_dict['END_TIME'] if 'END_TIME' in arg_dict]
	

    events_result = calendar_service.events().list(
        calendarId='primary',
        # timeMin=f'{date}T00:00:00Z',
        # timeMax=f'{date}T23:59:59Z',
        timeMin=f'{date}T{start_time}Z',
        timeMax=f'{date}T{end_time}Z',
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])

    formatted_events = []
    for event in events:
        formatted_event = {
            "summary": event['summary'],
            "start_time": event['start'].get('dateTime', event['start'].get('date')),
            "location": event.get('location', 'N/A'),
        }
        formatted_events.append(formatted_event)
	return formatted_events



def get_free_busy_info(arg_dict):
	start_time = arg_dict['START_TIME']
	end_time = arg_dict['END_TIME']


    free_busy_query = {
        "timeMin": start_time,
        "timeMax": end_time,
        "items": [{"id": "primary"}],
    }

    free_busy_info = calendar_service.freebusy().query(body=free_busy_query).execute()
    return free_busy_info



############# function not ready############# 
def update_event(event_id, summary=None, start_time=None, end_time=None, location=None):
    """Update an event in Google Calendar"""
    event = calendar_service.events().get(calendarId='primary', eventId=event_id).execute()

    if summary:
        event['summary'] = summary
    if start_time:
        event['start']['dateTime'] = start_time
    if end_time:
        event['end']['dateTime'] = end_time
    if location:
        event['location'] = location

    updated_event = calendar_service.events().update(calendarId='primary', eventId=event_id, body=event).execute()
    return json.dumps({"event_id": updated_event['id'], "summary": updated_event['summary'], "status": "updated"})


def reschedule_event(event_id, start_time, end_time):
    """Reschedule an event in Google Calendar"""
    return update_event(event_id, start_time=start_time, end_time=end_time)
