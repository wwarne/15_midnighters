import requests
from pytz import timezone
from datetime import datetime

URL = 'https://devman.org/api/challenges/solution_attempts'


def fetch_users_from_api():
    session = requests.Session()
    current_page = 1
    while True:
        params = {'page': current_page}
        print('Grabs page # {}'.format(current_page))
        page = session.get(URL, params=params).json()
        total_pages = page['number_of_pages']
        for user in page['records']:
            yield user

        if current_page >= total_pages:
            break
        current_page += 1


def is_midnighter(user_data):
    if not user_data['timestamp'] or not user_data['timezone']:
        return False
    user_tz = timezone(user_data['timezone'])
    user_time = datetime.fromtimestamp(user_data['timestamp'], tz=user_tz)
    print('Check user {} with time {}'.format(user_data['username'], user_time))
    if 0 <= user_time.hour <= 4:
        # If user submitted task from 00:00 to 04:59 - he is a midnighter. After 5 a.m. - he is an early bird.
        return True
    return False


def process_page(data):
    return {user['username'] for user in data['records'] if is_midnighter(user)}


def get_midnighters():
    return {user['username'] for user in fetch_users_from_api() if is_midnighter(user)}

if __name__ == '__main__':
    midnighters = get_midnighters()
    print('============Midnighters of Devman.org===========')
    print('Total amount of midnighters: {}'.format(len(midnighters)))
    print('The names of these slepless people:')
    for midnighter in midnighters:
        print(midnighter)
