import os.path
import asyncio
import re

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from pars_yt import get_stat_2
from pars_inst import inst_day, get_subs
from pars_tt import get_day

from instagrapi.exceptions import UnknownError



async def get_ids_2(week_stat, week_tg):
    creds = None
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]

    if os.path.exists("token.json"):
      creds = Credentials.from_authorized_user_file("token.json", scopes)
    if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
      else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "pars_plus_bot\google.json", scopes
        )
        creds = flow.run_local_server(port=0)
      with open("token.json", "w") as token:
        token.write(creds.to_json())

    try:
      service = build("sheets", "v4", credentials=creds)

      counter_1 = 2
      counter_2 = 2
      counter_3 = 4
      counter_4 = 6
      counter_5 = 2
      counter_graf = 4 


      id_sheet = "1K1DcaR51uatQYrVVBwIoTU3PiNnKXhUUBsI7F27Z_hQ"

      while True:
        range_country = f'A{counter_1}:H{counter_2}'
        range_accs = f'A{counter_3}:B{counter_4}'
        range_data = f'C{counter_3}:H{counter_4}'
        range_names = [
            range_country, range_accs, range_data
          ]
        

        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .batchGet(spreadsheetId=id_sheet, ranges=range_names)
            .execute()
        )
        values = result.get("valueRanges", [])

        if 'values' not in values[0]:
            all_subs, all_views, all_likes, all_comms, all_downl, all_share = all_day('B2:B100')
            range_t = f'B{counter_5}'
            value_inst = f'общие данные за:{week_tg}\nподписчики:{all_subs}\nпросмотры:{all_views}\nлайки:{all_likes}\nкоментарии:{all_comms}\nсохранения:{all_downl}\nпересылки:{all_share}'
            add_stat_telegram(range_t=range_t, value=value_inst)

            all_subs, all_views, all_likes, all_comms, all_downl, all_share = all_day('C2:C100')
            range_t = f'C{counter_5}'
            value_yt = f'общие данные за:{week_tg}\nподписчики:{all_subs}\nпросмотры:{all_views}\nлайки:{all_likes}\nкоментарии:{all_comms}\nсохранения:{all_downl}\nпересылки:{all_share}'
            add_stat_telegram(range_t=range_t, value=value_yt)

            all_subs, all_views, all_likes, all_comms, all_downl, all_share = all_day('D2:D100')
            range_t = f'D{counter_5}'
            value_tt = f'общие данные за:{week_tg}\nподписчики:{all_subs}\nпросмотры:{all_views}\nлайки:{all_likes}\nкоментарии:{all_comms}\nсохранения:{all_downl}\nпересылки:{all_share}'
            add_stat_telegram(range_t=range_t, value=value_tt)
            return value_inst, value_yt, value_tt
          
        lan = values[0]['values'][0][2]
        socials = values[1]['values']

        try:
            stats = values[2]['values']
        except KeyError:
            range_t = f'I{counter_1}:O{counter_2}'  
            add_date(range_t=range_t, date=week_stat)

            for social in socials:
                if social[0] == 'instagram':
                    
                    await asyncio.sleep(60)
                    l_in, c_in, v_in, d_v_in, d_l_in, d_c_in  = inst_day(social[1])

                    await asyncio.sleep(60)
                    subs_in = get_subs(social[1])

                    range_t = f'J{counter_graf}:O{counter_graf}'
                    add_stat_2(range_t=range_t, subs=0, views=v_in, likes=l_in, comms=c_in)

                    range_t = f'C{counter_graf}:H{counter_graf}'
                    add_stat_2(range_t=range_t, subs=subs_in, views=v_in, likes=l_in, comms=c_in)

                    range_t = f'B{counter_5}'
                    value = f'{lan}\nподписчики:0\nпросмотры:{d_v_in}\nлайки:{d_l_in}\nкоментарии:{d_c_in}\nсохранения:0\nпересылки:0'
                    add_stat_telegram(range_t=range_t, value=value)

                    print('instagram')

                elif social[0] == 'youtube':
                    counter_graf += 1
                    l_yt, v_yt, c_yt, s_yt, d_v_yt, d_l_yt, d_c_yt  = get_stat_2(social[1])

                    range_t = f'C{counter_graf}:H{counter_graf}'
                    add_stat_2(range_t=range_t, subs=s_yt, views=v_yt, likes=l_yt, comms=c_yt)

                    range_t = f'J{counter_graf}:O{counter_graf}'
                    add_stat_2(range_t=range_t, subs=0, views=v_yt, likes=l_yt, comms=c_yt)

                    range_t = f'C{counter_5}'
                    value = f'{lan}\nподписчики:0\nпросмотры:{d_v_yt}\nлайки:{d_l_yt}\nкоментарии:{d_c_yt}\nсохранения:0\nпересылки:0'
                    add_stat_telegram(range_t=range_t, value=value)
                    print('youtube')

                elif social[0] == 'tiktok':
                    counter_graf += 1
                    l_tt, c_tt, s_tt, downl_tt, v_tt, sh_tt, d_l_tt, d_c_tt, d_dow_tt, d_v_tt, d_sh_tt = await get_day(social[1], [])

                    range_t = f'C{counter_graf}:H{counter_graf}'
                    add_stat_2(range_t=range_t, subs=s_tt, views=v_tt, likes=l_tt, comms=c_tt, downl=downl_tt, share=sh_tt)

                    range_t = f'J{counter_graf}:O{counter_graf}'
                    add_stat_2(range_t=range_t, subs=0, views=v_tt, likes=l_tt, comms=c_tt, share=sh_tt, downl=downl_tt)

                    range_t = f'D{counter_5}'
                    value = f'{lan}\nподписчики:0\nпросмотры:{d_v_tt}\nлайки:{d_l_tt}\nкоментарии:{d_c_tt}\nсохранения:{d_dow_tt}\nпересылки:{d_sh_tt}'
                    add_stat_telegram(range_t=range_t, value=value)
                    print('tiktok')

            counter_1 += 5
            counter_2 += 5
            counter_3 += 5
            counter_4 += 5
            counter_5 += 1
            counter_graf += 3
            continue


        range_t = f'I{counter_1}:O{counter_2}'  
        add_date(range_t=range_t, date=week_stat)

        for social in socials:
          if social[0] == 'instagram':
              await asyncio.sleep(60)
              l_in, c_in, v_in, d_l_in, d_c_in, d_v_in  = inst_day(social[1])
              await asyncio.sleep(60)
              subs_in = get_subs(social[1])

              new_s_in = subs_in - int(stats[0][0])

              range_t = f'J{counter_graf}:O{counter_graf}'
              add_stat_2(range_t=range_t, subs=new_s_in, views=v_in, likes=l_in, comms=c_in)

              new_v_in = int(stats[0][1]) + int(v_in)
              new_l_in = int(stats[0][2]) + int(l_in)
              new_c_in = int(stats[0][5]) + int(c_in)

              range_t = f'C{counter_graf}:H{counter_graf}'
              add_stat_2(range_t=range_t, subs=subs_in, views=new_v_in, likes=new_l_in, comms=new_c_in)

              range_t = f'B{counter_5}'
              value = f'{lan}\nподписчики:{new_s_in}\nпросмотры:{d_v_in}\nлайки:{d_l_in}\nкоментарии:{d_c_in}\nсохранения:0\nпересылки:0'
              add_stat_telegram(range_t=range_t, value=value)

              print('instagram')

          elif social[0] == 'youtube':
              counter_graf += 1
              l_yt, v_yt, c_yt, s_yt, d_v_yt, d_l_yt, d_c_yt  = get_stat_2(social[1])

              range_t = f'J{counter_graf}:O{counter_graf}'
              new_s_yt = s_yt - int(stats[1][0])
              add_stat_2(range_t=range_t, subs=new_s_yt, views=v_yt, likes=l_yt, comms=c_yt)

              new_v_yt = int(stats[1][1]) + int(v_yt)
              new_l_yt = int(stats[1][2]) + int(l_yt)
              new_c_yt = int(stats[1][5]) + int(c_yt)

              range_t = f'C{counter_graf}:H{counter_graf}'
              add_stat_2(range_t=range_t, subs=s_yt, views=new_v_yt, likes=new_l_yt, comms=new_c_yt)

              range_t = f'C{counter_5}'
              value = f'{lan}\nподписчики:{new_s_yt}\nпросмотры:{d_v_yt}\nлайки:{d_l_yt}\nкоментарии:{d_c_yt}\nсохранения:0\nпересылки:0'
              add_stat_telegram(range_t=range_t, value=value)
              print('youtube')

          elif social[0] == 'tiktok':
              counter_graf += 1
              l_tt, c_tt, s_tt, downl_tt, v_tt, sh_tt, d_l_tt, d_c_tt, d_dow_tt, d_v_tt, d_sh_tt  = await get_day(social[1], [])

              new_v_tt = int(stats[1][1]) + int(v_tt)
              new_l_tt = int(stats[1][2]) + int(l_tt)
              new_dowl_tt = int(stats[1][3]) + int(v_tt)
              new_share_tt = int(stats[1][4]) + int(l_tt)
              new_c_tt = int(stats[1][5]) + int(c_tt)

              range_t = f'C{counter_graf}:H{counter_graf}'
              add_stat_2(range_t=range_t, subs=s_tt, views=new_v_tt, likes=new_l_tt, comms=new_dowl_tt, downl=new_share_tt, share=new_c_tt)

              new_s_tt = s_tt - int(stats[2][0])
              range_t = f'J{counter_graf}:O{counter_graf}'
              add_stat_2(range_t=range_t, subs=new_s_tt, views=v_tt, likes=l_tt, comms=c_tt, share=sh_tt, downl=downl_tt)

              range_t = f'D{counter_5}'
              value = f'{lan}\nподписчики:{new_s_tt}\nпросмотры:{d_v_tt}\nлайки:{d_l_tt}\nкоментарии:{d_c_tt}\nсохранения:{d_dow_tt}\nпересылки:{d_sh_tt}'
              add_stat_telegram(range_t=range_t, value=value)
              print('tiktok')

        counter_1 += 5
        counter_2 += 5
        counter_3 += 5
        counter_4 += 5
        counter_5 += 1
        counter_graf += 3

    except HttpError as err:
      print(err)
      return err


def add_stat_2(range_t, subs=0, views=0, likes=0, downl=0, share=0, comms=0):
    creds = None
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]

    if os.path.exists("token.json"):
      creds = Credentials.from_authorized_user_file("token.json", scopes)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
      else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "pars_plus_bot\google.json", scopes
        )
        creds = flow.run_local_server(port=0)
      # Save the credentials for the next run
      with open("token.json", "w") as token:
        token.write(creds.to_json())

    try:
          body = {
                  'values' : [
                  [subs, views, likes, downl, share, comms] # строка 
              ]
            }
          service = build("sheets", "v4", credentials=creds)

          counter_1 = 4
          counter_2 = 6
          counter_3 = 1
          counter_4 = 2

          id_sheet = "1K1DcaR51uatQYrVVBwIoTU3PiNnKXhUUBsI7F27Z_hQ"
          sheet = (
             service.spreadsheets()
             .values()
             .update(
                spreadsheetId=id_sheet,
                range=f"данные!{range_t}",
                valueInputOption="RAW",
                body=body).execute()
          )
    except HttpError as err:
      print(err)


def add_date(range_t, date):
    creds = None
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]


    if os.path.exists("token.json"):
      creds = Credentials.from_authorized_user_file("token.json", scopes)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
      else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "pars_plus_bot\google.json", scopes
        )
        creds = flow.run_local_server(port=0)
      # Save the credentials for the next run
      with open("token.json", "w") as token:
        token.write(creds.to_json())

    try:
          body = {
                  'values' : [
                  [date] # строка 
              ]
            }
          service = build("sheets", "v4", credentials=creds)

          counter_1 = 4
          counter_2 = 6
          counter_3 = 1
          counter_4 = 2

          id_sheet = "1K1DcaR51uatQYrVVBwIoTU3PiNnKXhUUBsI7F27Z_hQ"
          sheet = (
             service.spreadsheets()
             .values()
             .update(
                spreadsheetId=id_sheet,
                range=f"данные!{range_t}",
                valueInputOption="RAW",
                body=body).execute()
          )

    except HttpError as err:
      print(err)


def add_stat_telegram(range_t, value):
    creds = None
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]

    if os.path.exists("token.json"):
      creds = Credentials.from_authorized_user_file("token.json", scopes)
    if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
      else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "pars_plus_bot\google.json", scopes
        )
        creds = flow.run_local_server(port=0)
      with open("token.json", "w") as token:
        token.write(creds.to_json())

    try:
          body = {
                  'values' : [
                  [value] # строка 
              ]
            }
          service = build("sheets", "v4", credentials=creds)

          counter_1 = 4
          counter_2 = 6
          counter_3 = 1
          counter_4 = 2
          id_sheet = "1K1DcaR51uatQYrVVBwIoTU3PiNnKXhUUBsI7F27Z_hQ"
          sheet = (
             service.spreadsheets()
             .values()
             .update(
                spreadsheetId=id_sheet,
                range=f"телеграм!{range_t}",
                valueInputOption="RAW",
                body=body).execute()
          )
    except HttpError as err:
      print(err)


def all_day(range_stat):
    creds = None
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]

    if os.path.exists("token.json"):
      creds = Credentials.from_authorized_user_file("token.json", scopes)
    if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
      else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "pars_plus_bot\google.json", scopes
        )
        creds = flow.run_local_server(port=0)
      with open("token.json", "w") as token:
        token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId='1K1DcaR51uatQYrVVBwIoTU3PiNnKXhUUBsI7F27Z_hQ', range=f'телеграм!{range_stat}')
            .execute()
        )

        values = result.get("values", [])
        
        subs = 0
        likes = 0
        views = 0
        comms = 0
        downl = 0
        share = 0

        for value in values:
              values_split = re.split(":|\n", value[0])
              subs += int(values_split[2])
              views += int(values_split[4])
              likes += int(values_split[6])
              comms += int(values_split[8])
              downl += int(values_split[10])
              share += int(values_split[12])
        return subs, likes, views, comms, downl, share
    
    except HttpError as err:
      print(err)


if __name__ == "__main__":
  print(all_day('D2:D100'))
