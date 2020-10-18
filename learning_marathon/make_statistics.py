import json
from .models import User, LearningSession
import datetime
import os
import re
from pytz import timezone


def day_summary(user, date, udemy: bool):
    entries = LearningSession.objects.filter(user=user, udemy=udemy)
    day_complete = datetime.timedelta(seconds=0)

    for entry in entries:
        if entry.start_date.day == date.day and entry.start_date.month == date.month and entry.start_date.year == date.year:
            day_complete += entry.duration()
    summary = day_complete - datetime.timedelta(microseconds=day_complete.microseconds)
    if summary:
        return summary 
    else:
        return datetime.timedelta(seconds=0)

def new_data(date):
    user1 = User.objects.first()
    user2 = User.objects.last()

    day_entry = {
        'day':date.isoformat(),
        'user1':str(day_summary(user1, date, True)),
        'user1_no_udemy':str(day_summary(user1, date, False)),
        'user2':str(day_summary(user2, date, True)),
        'user2_no_udemy':str(day_summary(user2, date, False)),
        'user1_rewards':str(day_summary(user1, date, True).seconds//3600),
        'user1_no_udemy_rewards':str(day_summary(user1, date, False).seconds//3600),
        'user2_rewards':str(day_summary(user2, date, True).seconds//3600),
        'user2_no_udemy_rewards':str(day_summary(user2, date, False).seconds//3600)
    }
    return day_entry

def add_daily_summary(new_data):
    with open (os.path.join(os.path.dirname(__file__),'learning_sessions.json')) as json_file:
        data = json.load(json_file)
        learning_sessions = data['learning_sessions']
        learning_sessions.append(new_data)

    with open (os.path.join(os.path.dirname(__file__),'learning_sessions.json'), 'w') as json_file:
        json.dump(data, json_file)


def update():
    with open (os.path.join(os.path.dirname(__file__),'learning_sessions.json')) as json_file:
        data = json.load(json_file)
        last_update = data['learning_sessions'][-1]['day']
        if ((datetime.date.fromisoformat(last_update).day != (datetime.date.today().day - 1)) and datetime.datetime.now(tz=timezone('Europe/Warsaw')).hour > 6):
            new_entry = new_data(datetime.date.today() - datetime.timedelta(days=1))
            add_daily_summary(new_entry)

def get_data():
    with open (os.path.join(os.path.dirname(__file__),'learning_sessions.json')) as json_file:
        data = json.load(json_file)
        learning_sessions = data['learning_sessions']
        for session in learning_sessions:
            time_user1 = datetime.datetime.strptime(session['user1'],"%H:%M:%S")
            duration = datetime.timedelta(hours=time_user1.hour, minutes=time_user1.minute, seconds=time_user1.second)
            session['user1'] = duration
            session['user1_rewards'] = int(session['user1_rewards'])

            time_user1_no_udemy = datetime.datetime.strptime(session['user1_no_udemy'],"%H:%M:%S")
            duration_no_udemy = datetime.timedelta(hours=time_user1_no_udemy.hour, minutes=time_user1_no_udemy.minute, seconds=time_user1_no_udemy.second)
            session['user1_no_udemy'] = duration_no_udemy
            session['user1_no_udemy_rewards'] = int(session['user1_no_udemy_rewards'])

            time_user2 = datetime.datetime.strptime(session['user2'],"%H:%M:%S")
            duration = datetime.timedelta(hours=time_user2.hour, minutes=time_user2.minute, seconds=time_user2.second)
            session['user2'] = duration
            session['user2_rewards'] = int(session['user2_rewards'])

            time_user2_no_udemy = datetime.datetime.strptime(session['user2_no_udemy'],"%H:%M:%S")
            duration_no_udemy = datetime.timedelta(hours=time_user2_no_udemy.hour, minutes=time_user2_no_udemy.minute, seconds=time_user2_no_udemy.second)
            session['user2_no_udemy'] = duration_no_udemy
            session['user2_no_udemy_rewards'] = int(session['user2_no_udemy_rewards'])

    return learning_sessions