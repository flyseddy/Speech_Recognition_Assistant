import random

def father():
    """Method that randomizes the dad responses each time"""
    list_of_dad_responses = ['My Creator is named Sedrick and he is my dad', 
    'My creator is named Sedrick but people also call him fly seddy']
    dad_response = random.choice(list_of_dad_responses)
    return dad_response

def mother():
    """Method that randomizes the mom responses each time"""
    list_of_mom_responses = ['One lucky woman out there', 
    'You may never know but Sedrick is my dad',
    'Her name starts with ... Ha ha gotcha']
    mom_response = random.choice(list_of_mom_responses)
    return mom_response

