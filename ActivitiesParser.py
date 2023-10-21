import os
import json
from dotenv import load_dotenv


class ActivitiesParser:
    def __init__(self, src_path):
        self._src_path = src_path

    def run(self):
        #print('ActivitiesParser run')
        f = open(self._src_path)
        activities = json.load(f)
        total_dist = 0
        elevation_gain = 0
        moving_time = 0
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
            print(activity['start_date_local'])
            print(activity['name'] + ': distance ' + distance + 'km, elevation gain ' + elevation + ' metres, moving time: ' + hours + ' hours')
        print('================================================================================================')
        total_dist = "%.2f" % total_dist
        hours = ("%.2f" % (moving_time/3600))
        print(f"Total distance: {total_dist} km")
        print(f"Total elevation gain: {elevation_gain} metres")
        print(f"Total moving time: {hours} hours")
        
        f.close()
        



if __name__ == "__main__":
    load_dotenv()
    ActivitiesParser(os.getenv('activities')).run()