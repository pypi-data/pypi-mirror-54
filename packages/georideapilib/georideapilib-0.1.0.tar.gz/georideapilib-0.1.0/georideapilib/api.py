"""
Georide api lib
@author Matthieu DUVAL <matthieu@duval-dev.fr>
"""

import json
import urllib3

from georideapilib.objects import (
    GeorideTracker, 
    GeorideAccount, 
    GeorideUser,  
    GeorideTrackerTrip,  
    GeorideTrackerPosition, 
    GeorideSharedTrip
)

GEORIDE_API_HOST = "https://api.georide.fr"
GEORIDE_API_ENDPOINT_LOGIN = "/user/login"
GEORIDE_API_ENDPOINT_NEW_TOKEN = "/user/new-token"
GEORIDE_API_ENDPOINT_LOGOUT = "/user/logout"
GEORIDE_API_ENDPOINT_USER = "/user"
GEORIDE_API_ENDPOINT_TRAKERS = "/user/trackers"
GEORIDE_API_ENDPOINT_TRIPS = "/tracker/:trackerId/trips"
GEORIDE_API_ENDPOINT_LOCK = "/tracker/:trackerId/lock"
GEORIDE_API_ENDPOINT_UNLOCK = "/tracker/:trackerId/unlock"
GEORIDE_API_ENDPOINT_TOGGLE_LOCK = "/tracker/:trackerId/toggleLock"
GEORIDE_API_ENDPOINT_POSITIONS = "/tracker/:trackerId/trips/positions"
GEORIDE_API_ENDPOINT_TRIP_SHARE = "/tracker/:trackerId/share/trip"


def get_authorisation_token(email, password):
    """ return an authorization token """
    http = urllib3.PoolManager()
    data = {"email": email, "password": password}
    encoded_data = json.dumps(data).encode('utf-8')
    response = http.request(
        'POST', 
        GEORIDE_API_HOST + GEORIDE_API_ENDPOINT_LOGIN,
        body=encoded_data,
        headers={'Content-Type': 'application/json'})
    response_data = json.loads(response.data.decode('utf-8'))
    account = GeorideAccount.from_json(response_data)
    return account


def renew_token(token):
    """ renew the authorization token """
    http = urllib3.PoolManager()
    headers = {"Authorization": "Bearer " + token}
    response = http.request(
        'GET', 
        GEORIDE_API_HOST + GEORIDE_API_ENDPOINT_NEW_TOKEN,
        headers=headers)
    response_data = json.loads(response.data.decode('utf-8'))
    new_token = response_data['authToken']
    return new_token


def revoke_token(token):
    """ invalidate the authorization token """
    http = urllib3.PoolManager()
    headers = {"Authorization": "Bearer " + token}
    response = http.request(
        'POST', 
        GEORIDE_API_HOST + GEORIDE_API_ENDPOINT_LOGOUT,
        headers=headers)
    if response.status != 204:
        return False
    return True


def get_user(token):
    """ get the georide user info """
    http = urllib3.PoolManager()
    headers = {"Authorization": "Bearer " + token}
    response = http.request(
        'GET', 
        GEORIDE_API_HOST + GEORIDE_API_ENDPOINT_USER,
        headers=headers)
    response_data = json.loads(response.data.decode('utf-8'))
    account = GeorideUser.from_json(response_data)
    return account  

def get_trackers(token):
    """ get user trackers """
    http = urllib3.PoolManager()
    headers = {"Authorization": "Bearer " + token}
    response = http.request(
        'GET', 
        GEORIDE_API_HOST + GEORIDE_API_ENDPOINT_TRAKERS,
        headers=headers)

    response_data = json.loads(response.data.decode('utf-8'))
    trackers = []
    for json_tracker in response_data:
        trackers.append(GeorideTracker.from_json(json_tracker))
    return trackers


def get_trips(token, tracker_id, from_date, to_date):
    """ return all trips between two dates """
    http = urllib3.PoolManager()
    headers = {"Authorization": "Bearer " + token}
    response = http.request(
        'GET', 
        GEORIDE_API_HOST + GEORIDE_API_ENDPOINT_TRIPS.replace(':trackerId', str(tracker_id)),
        fields={'from': from_date, 'to': to_date},
        headers=headers)

    response_data = json.loads(response.data.decode('utf-8'))
    trips = []
    for json_trip in response_data:
        trips.append(GeorideTrackerTrip.from_json(json_trip))
    return trips

def get_positions(token, tracker_id, from_date, to_date):
    """ return all trips between two dates """
    http = urllib3.PoolManager()
    headers = {"Authorization": "Bearer " + token}
    response = http.request(
        'GET', 
        GEORIDE_API_HOST + GEORIDE_API_ENDPOINT_POSITIONS.replace(':trackerId', str(tracker_id)),
        fields={'from': from_date, 'to': to_date},
        headers=headers)

    response_data = json.loads(response.data.decode('utf-8'))
    positions = []
    for json_position in response_data:
        positions.append(GeorideTrackerPosition.from_json(json_position))
    return positions

def share_a_trip_by_trip_id(token, tracker_id, trip_id):
    """ share trip by trip id """
    return _share_a_trip(token, tracker_id, trip_id=trip_id)

def share_a_trip_by_date(token, tracker_id, from_date, to_date):
    """ share trips between two dates """
    return _share_a_trip(token, tracker_id, from_date=from_date, to_date=to_date)

def share_a_trip_by_trip_merge_id(token, tracker_id, trip_merged_id):
    """ share trip by trip merged id """
    return _share_a_trip(token, tracker_id, trip_merged_id=trip_merged_id)

def _share_a_trip(token, tracker_id, trip_id=None, from_date=None, # pylint: disable= R0913
                  to_date=None, trip_merged_id=None): 
    """ share trip by trib_id or between two dates or trip_merged_id """
    data = None
    if trip_id is not None:
        data = {"tripId": trip_id}
    elif from_date is not None and to_date is not None:
        data = {"from": from_date, "to": to_date}
    elif trip_merged_id is not None:
        data = {"tripMergedId": trip_merged_id}

    encoded_data = json.dumps(data).encode('utf-8')
    print("Trip data: ", encoded_data)

    http = urllib3.PoolManager()
    headers = {
        "Authorization": "Bearer " + token,
        'Content-Type': 'application/json'
    }
    response = http.request(
        'POST', 
        GEORIDE_API_HOST + GEORIDE_API_ENDPOINT_TRIP_SHARE.replace(':trackerId', str(tracker_id)),
        body=encoded_data,
        headers=headers)

    response_data = json.loads(response.data.decode('utf-8'))
    print("Trip data: ", response_data)
    return GeorideSharedTrip.from_json(response_data)

def lock_tracker(token, tracker_id):
    """ used to lock a tracker """
    http = urllib3.PoolManager()
    headers = {"Authorization": "Bearer " + token}
    response = http.request(
        'POST', 
        GEORIDE_API_HOST + GEORIDE_API_ENDPOINT_LOCK.replace(':trackerId', str(tracker_id)),
        headers=headers)
    if response.status != 204:
        return False
    return True

def unlock_tracker(token, tracker_id):
    """ used to unlock a tracker """
    http = urllib3.PoolManager()
    headers = {"Authorization": "Bearer " + token}
    response = http.request(
        'POST', 
        GEORIDE_API_HOST + GEORIDE_API_ENDPOINT_UNLOCK.replace(':trackerId', str(tracker_id)),
        headers=headers)
    if response.status != 204:
        return False
    return True

def toogle_lock_tracker(token, tracker_id):
    """ used to toggle lock a tracker """
    http = urllib3.PoolManager()
    headers = {"Authorization": "Bearer " + token}
    response = http.request(
        'POST', 
        GEORIDE_API_HOST + GEORIDE_API_ENDPOINT_TOGGLE_LOCK.replace(':trackerId', str(tracker_id)),
        headers=headers)
    response_data = json.loads(response.data.decode('utf-8'))
    return response_data['locked']

if __name__ == '__main__':
    print("Not a main module")
