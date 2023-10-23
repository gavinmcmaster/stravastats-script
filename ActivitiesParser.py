import os
from dotenv import load_dotenv
import requests
import responses
from datetime import datetime

class ActivitiesParser:
    
    def get_access_token(self) -> str:
        # Config Settings
        client_id = os.getenv('STRAVA_CLIENT_ID')
        client_secret = os.getenv('STRAVA_CLIENT_SECRET')
        redirect_uri = 'http://localhost/'

        # Authorization URL
        request_url = f'http://www.strava.com/oauth/authorize?client_id={client_id}' \
                        f'&response_type=code&redirect_uri={redirect_uri}' \
                        f'&approval_prompt=force' \
                        f'&scope=profile:read_all,activity:read_all'

        # User prompt showing the Authorization URL
        print('Click here:', request_url)
        print('Authorize the app and copy&paste below the generated code!')
        code = input('Insert the code from the url: ')
        
        # Get the access token
        token = requests.post(url='https://www.strava.com/api/v3/oauth/token',
                            data={'client_id': client_id,
                                    'client_secret': client_secret,
                                    'code': code,
                                    'grant_type': 'authorization_code'})

        strava_token = token.json()
        return strava_token['access_token']
    
    def get_activities(self, access_token) -> list:
        activity_after = os.getenv('STRAVA_ACTIVITY_AFTER')
        activity_before = os.getenv('STRAVA_ACTIVITY_BEFORE')
        page = 1
        activities = []
        
        while True:
            activities_url = f"https://www.strava.com/api/v3/athlete/activities?" \
                f"access_token={access_token}&page={page}"
                        
            if activity_after is not None and int(activity_after) > 0:
                activities_url += f"&after={activity_after}"
    
            if activity_before is not None and int(activity_before) > 0:
                activities_url += f"&before={activity_before}"
            
            #print(activities_url)
            # TODO consider using yield to return page by page
            try:
                response = requests.get(activities_url)
                page_activities = response.json()
                
                if response.status_code == 200 and len(page_activities) > 0:
                    activities += page_activities
                    page += 1
                else:
                    if (response.status_code != 200):
                        print(f'API RESPONSE ERROR CODE: {response.status_code}')
                    break
            except Exception as err:
                print(f'Error: {err=}, {type(err)=}')
                break
            
        return activities
        
    def run(self, activities) -> None:
        #print('ActivitiesParser run')
        total_dist = 0
        elevation_gain = 0
        moving_time = 0
        count = 0
        # Put in chronological order
        date_format = '%Y-%m-%dT%H:%M:%SZ'
        activities.sort(key=lambda x: datetime.strptime(x['start_date_local'], date_format))
        
        for activity in activities:
            if activity['type'].lower() != 'ride':
                continue
            
            km = (activity['distance']/1000)
            total_dist += km
            elevation_gain += activity['total_elevation_gain']
            moving_time += activity['moving_time']
            hours = ("%.2f" % (activity['moving_time']/3600))
            distance = ("%.2f" % km)
            elevation = ("%.2f" % activity['total_elevation_gain'])
            count += 1
            date_obj = datetime.strptime(activity['start_date_local'], date_format)
            formatted_date = date_obj.strftime('%c')
            print(formatted_date + ' - ' + activity['name'] + ': distance ' + distance + \
                'km, elevation gain ' + elevation + ' metres, moving time: ' + hours + ' hours')
        print('================================================================================================')
        total_dist = "%.2f" % total_dist
        hours = ("%.2f" % (moving_time/3600))
        elevation_gain = "%.2f" % elevation_gain
        print(f"Activities count: {count}")
        print(f"Total distance: {total_dist} km")
        print(f"Total elevation gain: {elevation_gain} metres")
        print(f"Total moving time: {hours} hours")

if __name__ == "__main__":
    load_dotenv()
    ap = ActivitiesParser()
    access_token = ap.get_access_token()
    
    activities = ap.get_activities(access_token)
    if len(activities) > 0:
        ActivitiesParser().run(activities)
    