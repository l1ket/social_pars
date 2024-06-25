from instagrapi import Client
from instagrapi.exceptions import UserNotFound, UnknownError

import time

def inst_day(name):
    all_likes = 0
    all_comm = 0
    all_views = 0
    
    try:
        cl = Client()
        cl.login(username='', password='')
        try:
            user_id = cl.user_id_from_username(name)
            medias = cl.user_clips(user_id, amount=7)
        except UserNotFound:
            return 0, 0, 0, 0, 0, 0 

        for media in medias:
            comm = media.comment_count
            likes = media.like_count
            views = media.play_count

            all_likes += likes
            all_comm += comm
            all_views += views

        return all_likes, all_comm, all_views, likes, comm, views
    except UnknownError:
        time.sleep(60)
        cl = Client()
        cl.login(username='', password='')
        try:
            user_id = cl.user_id_from_username(name)
            medias = cl.user_clips(user_id, amount=7)
        except UserNotFound:
            return 0, 0, 0, 0, 0, 0 

        for media in medias:
            comm = media.comment_count
            likes = media.like_count
            views = media.play_count

            all_likes += likes
            all_comm += comm
            all_views += views

        return all_likes, all_comm, all_views, likes, comm, views


def get_subs(name):
    try:
        cl = Client()
        cl.login(username='', password='')
        try:
            user_id = cl.user_id_from_username(name)
        except UserNotFound:
            return 0
        subs = cl.user_info(user_id=user_id).follower_count
        return subs
    except UnknownError:
        time.sleep(60)

        cl = Client()
        cl.login(username='', password='')
        try:
            user_id = cl.user_id_from_username(name)
        except UserNotFound:
            return 0
        subs = cl.user_info(user_id=user_id).follower_count
        return subs


if __name__ == '__main__':
    get_subs('zaraznow')