from .models import User, LearningSession
from datetime import datetime, date, timedelta

def day_summary(user, date, udemy: bool):
    entries = LearningSession.objects.filter(user=user, udemy=udemy)
    day_complete = timedelta(seconds=0)

    for entry in entries:
        if entry.start_date.day == date.day and entry.start_date.month == date.month and entry.start_date.year == date.year:
            day_complete += entry.duration()
    summary = day_complete - timedelta(microseconds=day_complete.microseconds)
    if summary:
        return summary
    else:
        return timedelta(seconds=0)

def new_data(date):
    user1 = User.objects.first()
    user2 = User.objects.last()

    user1_udemy = day_summary(user1, date, True)
    user1_no_udemy = day_summary(user1, date, False)
    user2_udemy = day_summary(user2, date, True)
    user2_no_udemy = day_summary(user2, date, False)

    day_entry = {
        'day':date.isoformat(),
        'user1': {'udemy': user1_udemy,
                    'no_udemy':user1_no_udemy,
                    'rewards': user1_udemy.seconds//3600,
                    'rewards_no_udemy': user1_no_udemy.seconds//3600},
        'user2': {'udemy': user2_udemy,
                    'no_udemy':user2_no_udemy,
                    'rewards': user2_udemy.seconds//3600,
                    'rewards_no_udemy': user2_no_udemy.seconds//3600}
    }
    return day_entry

def get_data():
    current_data = []

    user1_summary = timedelta(seconds=0)
    user2_summary = timedelta(seconds=0)
    user1_no_udemy_summary = timedelta(seconds=0)
    user2_no_udemy_summary = timedelta(seconds=0)

    start_date = date(2020,10,14)
    end_date = date.today() 
    time_range = end_date - start_date
    date_list = [(date.today() + timedelta(days=1)) - timedelta(days=x) for x in range(time_range.days)]

    for day in date_list:
        day_data = new_data(day)
        current_data.append(day_data)
        user1 = day_data['user1']
        user2 = day_data['user2']

        user1_summary += user1['udemy']
        user2_summary += user2['udemy']
        user1_no_udemy_summary += user1['no_udemy']
        user2_no_udemy_summary += user2['no_udemy']
    
    summary_entry = {
        'user1_summary' : user1_summary,
        'user2_summary' : user2_summary,
        'user1_no_udemy_summary' : user1_no_udemy_summary,
        'user2_no_udemy_summary' : user2_no_udemy_summary
    }
    current_data[0] = summary_entry
    
    return current_data