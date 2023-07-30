# time formatting
#!pip install datefinder
import datefinder

start_time = "16 Jul 7 PM"
end_time = "July 10 am"
end_time2 = "last 2 hours" #duration / not exact time -> need to solve duration issue


match_start = datefinder.find_date(start_time) #find_dates() = find all;  find_date = find one
match_end = datefinder.find_date(start_time)

if match:
	print(match) #[datetime.datetime(2023, 7, 16, 19, 0)]

formatted_start_time = match_start.strftime("%Y-%m-%dT%H:%M:%S")
