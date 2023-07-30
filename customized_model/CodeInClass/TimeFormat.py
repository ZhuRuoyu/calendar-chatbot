
# notebook version: class_format_argdict.ipynb
# class name: TimeFormat

!pip install datefinder
from datetime import datetime, timedelta, date, timezone
import datefinder

!pip install word2number
from word2number import w2n
import re
import pytz #timezone

from dateutil import parser # date



class TimeFormat:
    def __init__(self, arg_dict, timezone_want = 'America/Toronto'):
        self.arg_dict = arg_dict
        self.timezone = timezone_want
        self.fun_pool = [self.date_format,
                         self.start_time_format,
                         self.end_time_format,
                         ]

    def __extract_duration_components(self, duration_string):

      ''' the hours and mins abbr can't be recognized'''
    # Regular expression to find numbers and units in the input string
      pattern = r'(\d+|one|two|three|four|five|six|seven|eight|nine|ten)\s*(day|hour|minute)s?'
      matches = re.findall(pattern, duration_string)

      time_components = {
          'day': 0,
          'hour': 0,
          'minute': 0
      }

      for number, unit in matches:
          number = w2n.word_to_num(number) if number.isalpha() else int(number)
          unit = unit.lower()
          time_components[unit] = number

      return [time_components['day'], time_components['hour'], time_components['minute']]


    def __get_current_date_in_timezone(self, timezone_name):
    # Get the current date and time in UTC
      utc_now = datetime.utcnow()

    # Set the UTC timezone
      utc_timezone = pytz.timezone('UTC')

    # Convert the UTC time to the desired timezone
      desired_timezone = pytz.timezone(timezone_name)
      desired_date = utc_timezone.localize(utc_now).astimezone(desired_timezone).date()

      return desired_date


    def date_format(self):
      '''... need to fixed typo issue'''
      if 'DATE' in self.arg_dict.keys():

        date_str = self.arg_dict['DATE']


        # if no mis-spelling: parse it
        # if no date extracted, raise error
        date_get = parser.parse(date_str)
        self.arg_dict['DATE'] = date_get.strftime("%Y-%m-%d")

      else:
        #print('no "DATE" key, get todays date')
        date_get = self.__get_current_date_in_timezone(self.timezone)

      self.arg_dict['DATE'] = date_get.strftime("%Y-%m-%d")
      return self.arg_dict


    def start_time_format(self):

        if 'START_TIME' in self.arg_dict.keys():
          start_time_str = self.arg_dict['START_TIME']

          matches_start = list(datefinder.find_dates(start_time_str))

          while len(matches_start) == 0:
            print('Your start time is {}, need another format'.format(start_time_str))
            start_time_str = input("please enter the start time in the suggested format HH:MM")
            matches_start = list(datefinder.find_dates(start_time_str))


          # after the while loop, the len(list(matches_start))  must != 0:
          for match_start_first in matches_start: # select first time extracted
            # self.arg_dict['START_TIME'] = 'hello'


            #print('match time fist',match_start_first)
            start_time = match_start_first.strftime("%H:%M:%S")

            self.arg_dict['START_TIME'] = start_time
            break

          return self.arg_dict

    def end_time_format(self):
      #end_time = '2023-07-29 01:00:00'
      if 'END_TIME' in self.arg_dict.keys():
        print('end time given')

        end_time_str = self.arg_dict['END_TIME']
        matches_end   = list(datefinder.find_dates(end_time_str))
        print(matches_end)

      else:
        print('no end time given ')
        matches_end = []


      while (len(matches_end) == 0):
          #print('no end time matches, need to use duration to calculate the end time automatically')
          #print('variable need: "START_TIME", "DURATION", check availablity ')

          if 'START_TIME' in self.arg_dict.keys(): # by calculating

            start_time_str = self.arg_dict['START_TIME']


            # set duration
            if 'DURATION' in self.arg_dict.keys():
              duration_str = self.arg_dict['DURATION']
              duration = self.__extract_duration_components(duration_str) #return a list [day, hour, minute]

            else: #set the default duration = 0 day 1 hour 0 minutes
              duration = [0,1,0]

            # convert string-start-time to 'datetime type' with current date (strptime not working)
            start_temp = list(datefinder.find_dates(start_time_str))
            matches_end = start_temp #no meaning, just break the while loop
            for start_time in start_temp:
              break

            #end_time is already in the right format
            end_time = start_time + timedelta(days=duration[0], hours=duration[1], minutes=duration[2])
            end_time = end_time.strftime("%H:%M:%S")

            print('end time is calcuate by duration', end_time)

            self.arg_dict['END_TIME'] = end_time
            self.arg_dict['DURATION'] = duration
            print('dic return before else', end_time)
            return self.arg_dict #already return

          else: #no start time detected, need by manual input
            print('variable need: "START_TIME", "DURATION", are  unavailable, need manual input')
            end_time_str = input("please enter the end time in the suggested format HH:MM")
            matches_end = list(datefinder.find_dates(end_time_str))
            matches_end_else = matches_end

        # after while loop, make sure there is some time variable in the matches_end
        ## assign end_time from manual input
      for end_time_else in matches_end:#_else: # select first time extracted
            end_time = end_time_else.strftime("%H:%M:%S")
            break

      print('end time before assign to dict')
      self.arg_dict['END_TIME'] = end_time

      return self.arg_dict


    def format_all(self):
      for it in self.fun_pool:

        self.arg_dict = it()

      return self.arg_dict




	# if 'DATE' in arg_dict.keys:
	# 	date_str = arg_dict['DATE']
  #   	match_date = list(datefinder.find_dates(date_str)) #edge case: date = tomorrow

	# 	if len(match_date) != 0:
  #     		date = match_date[0]
  #     	else:
  #     		print(' no matched date found')
  #     		date = input("please enter the date in the format YYYY-MM-DD") # 'tomorrow' not match any, ask user again
  #     		date = date.strftime("%Y-%m-%dT")

  #     	arg_dict['DATE'] = date

  #   return arg_dict
  #       return something_else

