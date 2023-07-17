#formatting
'''
function_name_1 = 'reschedule_event'
arg_dict = {'START_TIME': '9am', 'END_TIME': 'until 5pm'}

'''
from datetime import datetime, timedelta
import datefinder



def match_time_date_format(arg_dict):
	'''
	change the time/date format so that can be recognized by api 
	.strftime("%Y-%m-%dT%H:%M:%S")
	'''
	if 'DURATION' in arg_dict.keys:
		duration = arg_dict['DURATION']
	else:
		duration = [0,1,0] #default duration is 1 hour

######### intentation#########

	if 'START_TIME' in arg_dict.keys:

		start_time_str = arg_dict['START_TIME']

		match_start = list(datefinder.find_dates(start_time_str))
		
		if len(match_start)!=0:
			start_time = match_start[0]
		else:
      		print('Your start time is {}, need another format'.format(start_time_str))
      		start_time = input("please enter the start time in the format HH:MM")
      		start_time = start_time.strftime("%H:%M:%S")

      	arg_dict['START_TIME'] = start_time



	if 'END_TIME' in arg_dict.keys:
		end_time_str = arg_dict['END_TIME']
		match_end   = list(datefinder.find_dates(end_time_str))

	    if len(match_end) != 0:
	      end_time = match_end[0]
	    else:
	      print('no end time matches, use duration to calculate the end time automatically')
	      
	      end_time = start_time + timedelta(days=duration[0], hours=duration[1], minutes=duration[2])
	      end_time = end_time.strftime("%H:%M:%S")
	    
	    arg_dict['END_TIME'] = end_time

	if 'DATE' in arg_dict.keys:
		date_str = arg_dict['DATE']
    	match_date = list(datefinder.find_dates(date_str)) #edge case: date = tomorrow 

		if len(match_date) != 0:
      		date = match_date[0]
      	else:
      		print(' no matched date found')
      		date = input("please enter the date in the format YYYY-MM-DD") # 'tomorrow' not match any, ask user again
      		date = date.strftime("%Y-%m-%dT")

      	arg_dict['DATE'] = date
    
    return arg_dict


def exact_date_optional(arg_dict):
	if 'DATE' in arg_dict.keys:
		date_str = arg_dict['DATE']
		# ... ...
		print('TBC: need to change from "next week" to a certain date')
	else:
		print('no "DATE" key. pass')


    return arg_dict
