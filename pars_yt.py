import datetime
import sqlite3

from googleapiclient.discovery import build
# from sheets import get_ids

key = ''


def get_stat_2(nick):
    all_likes = 0
    all_views = 0
    all_comm = 0

    youtube = build('youtube', 'v3',  
                developerKey=key) 

    ch_request = youtube.search().list(
        part="snippet",
        maxResults=1,
        q=nick,
        type="channel"
    )

    ch_response = ch_request.execute() 
    id_yt = ch_response['items'][0]['snippet']['channelId'] 

    request = youtube.search().list(
    part="snippet",
    channelId=id_yt,
    maxResults=7,
    order="date"
        )
    response = request.execute()

    lst_ids = ''

    for i in range(0, len(response['items'])):
        video_id = response['items'][i]['id']['videoId']
        lst_ids += f'{video_id},'

    request = youtube.videos().list(
    part="statistics",
    id=lst_ids
        )  
    response = request.execute()

    for i in response['items']:
        all_views += int(i['statistics']['viewCount'])
        all_likes += int(i['statistics']['likeCount'])
        all_comm += int(i['statistics']['commentCount'])
    
        last_day_v = int(i['statistics']['viewCount'])
        last_day_l = int(i['statistics']['likeCount'])
        last_day_c = int(i['statistics']['commentCount'])
    
    request = youtube.channels().list(
        part="statistics",
        id=id_yt
    )
    response = request.execute()
    subs = response['items'][0]['statistics']['subscriberCount']

    return all_likes, all_views, all_comm, int(subs), last_day_v, last_day_l, last_day_c



def change_week(new_date):
    connection = sqlite3.connect('dates.db')
    cursor = connection.cursor()

    cursor.execute('UPDATE dates SET date_week = ?', (new_date,))

    connection.commit()
    connection.close()


if __name__ == '__main__':
    x = get_stat_2('zaraznow')
    print(x)
