from os import times
from tabnanny import check
from time import time
from urllib import request
import tweepy
from datetime import date
from datetime import datetime, timedelta
import time

CONSUMER_KEY = '3YuicmSOdpwzI7QLNjkONQTPX'
CONSUMER_SECRET = 'SbedgLSZToNl36Ec0uCu3ZP3WCwBtqsYX3qWBZQ1jUjj0nUYJf'
ACCESS_KEY = '1527672954913542148-jSdsNLpBtG0y9nddFB8urWjQPQYDfF'
ACCESS_SECRET = 'gxsbv3LS2ATahB6iAJUSFpVegiXlM0vyVEw0Pzk4S23W9'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

TIMESTAMP_FILE = "last-timestamp.txt"
RECORD_FILE = "twitter-recording.txt"

# find top tweets of a user
def top_tweets(user):
    limit = 20
    tweets = api.user_timeline(screen_name = user, count = limit, tweet_mode = 'extended')

    url_start = 'https://twitter.com/' + user + '/status/'

    likes_list = []
    tweet_list = []
    tweet_id_list = []

    first = ''
    second = ''
    third = ''

    first_id = ''
    second_id = ''
    third_id = ''

    # check today's date:
    today = date.today()
    today_day = today.strftime('%d')
    today_month = today.strftime('%m')
    if str(today_day)[0] == '0':
        today_day.replace('0','')
    if str(today_month)[0] == '0':
        today_month.replace('0','')

    # makes list of tweets, number of likes, and ids
    for tweet in tweets:
        if tweet.created_at.day == int(today_day) and tweet.created_at.month == int(today_month):
            likes_list.append(tweet.favorite_count)
            tweet_list.append(tweet.full_text)
            tweet_id_list.append(tweet.id)

    if len(likes_list) >= 3:
        templike = 0
        tempind = 0
        for index,num in enumerate(likes_list):
            if num > templike:
                templike = num
                tempind = index
        first = tweet_list[tempind]
        first_id = tweet_id_list[tempind]
        likes_list.remove(templike)
        tweet_list.remove(first)
        tweet_id_list.remove(first_id)
        templike = 0
        tempind = 0

        for index,num in enumerate(likes_list):
            if num > templike:
                templike = num
                tempind = index
        second = tweet_list[tempind]
        second_id = tweet_id_list[tempind]
        likes_list.remove(templike)
        tweet_list.remove(second)
        tweet_id_list.remove(second_id)
        templike = 0
        tempind = 0

        for index,num in enumerate(likes_list):
            if num > templike:
                templike = num
                tempind = index
        third = tweet_list[tempind]
        third_id = tweet_id_list[tempind]
        likes_list.remove(templike)
        tweet_list.remove(third)
        tweet_id_list.remove(third_id)
        templike = 0
        tempind = 0

        return 'Tweet 1:\n\n' + first + '\nLink: ' + url_start + str(first_id) + '\n\n' + 'Tweet 2:\n\n' + second + '\nLink: ' + url_start + str(second_id) + '\n\n' + 'Tweet 3:\n\n' + third + '\nLink: ' + url_start + str(third_id) + ''
    elif len(likes_list) == 2:
        templike = 0
        tempind = 0
        for index,num in enumerate(likes_list):
            if num > templike:
                templike = num
                tempind = index
        first = tweet_list[tempind]
        first_id = tweet_id_list[tempind]
        likes_list.remove(templike)
        tweet_list.remove(first)
        tweet_id_list.remove(first_id)
        templike = 0
        tempind = 0

        for index,num in enumerate(likes_list):
            if num > templike:
                templike = num
                tempind = index
        second = tweet_list[tempind]
        second_id = tweet_id_list[tempind]
        likes_list.remove(templike)
        tweet_list.remove(second)
        tweet_id_list.remove(second_id)
        templike = 0
        tempind = 0

        return 'Tweet 1: \n\n' + first + '\nLink: ' + url_start + str(first_id) + '\n\n' + 'Tweet 2:\n\n' + second + '\nLink: ' + url_start + str(second_id) + ''
    elif len(likes_list) == 1:
        templike = 0
        tempind = 0
        for index,num in enumerate(likes_list):
            if num > templike:
                templike = num
                tempind = index
        first = tweet_list[tempind]
        first_id = tweet_id_list[tempind]
        likes_list.remove(templike)
        tweet_list.remove(first)
        tweet_id_list.remove(first_id)
        templike = 0
        tempind = 0

        return 'Tweet 1: \n\n' + first + '\nLink: ' + url_start + str(first_id) + ''

# check if twitter account exists
def check_acc(username):
    try:
        test_name = api.get_user(screen_name=username)
        print(test_name.id_str)
        print(test_name.screen_name)
        return True
    except:
        print('Username does not exist')
        return False

# check last timestamp checked
def check_last_timestamp(filename):
    infile = open(filename, 'r')
    file_text = infile.readline()
    return int(file_text.strip())

# update timestamp to last checked
def update_last_timestamp(filename,timestamp):
    outfile = open(filename, 'w')
    outfile.write(timestamp)
    outfile.close()

# check dms received and distinguish cancellations from requests
def check_received_dms():
    messages = api.get_direct_messages()
    my_name = 'mjdunat'
    my_user = api.get_user(screen_name=my_name)
    my_id = my_user.id_str

    dms_received_list = []

    for message in reversed(messages):
        if message.message_create['target']['recipient_id'] == my_id:
            dms_received_list.append(message)

    # Respond to messages
    for message in dms_received_list:
        if check_acc(message.message_create['message_data']['text']) == True:
            sender_id = message.message_create['sender_id']
            account_to_search = message.message_create['message_data']['text'].strip('@')
            timestamp = message.created_timestamp
            if int(timestamp) > check_last_timestamp(TIMESTAMP_FILE):
                text = 'Starting updates from ' + str(account_to_search)
                direct_message = api.send_direct_message(sender_id,text)
                update_last_timestamp(TIMESTAMP_FILE,timestamp)
        elif (str(message.message_create['message_data']['text']).split()[0].strip().lower() == 'cancel') and (check_acc(str(message.message_create['message_data']['text']).strip().split()[1].strip().lower()) == True):
            sender_id = message.message_create['sender_id']
            account_to_cancel = message.message_create['message_data']['text'].split()[1]
            timestamp = message.created_timestamp
            if int(timestamp) > check_last_timestamp(TIMESTAMP_FILE):
                text = 'Cancelling updates from ' + str(account_to_cancel)
                direct_message = api.send_direct_message(sender_id,text)
                update_last_timestamp(TIMESTAMP_FILE,timestamp)
    
    dms_requests_list = []

    for dm in dms_received_list:
        if check_acc(dm.message_create['message_data']['text']) == True:
            sender_id = dm.message_create['sender_id']
            account_to_search = dm.message_create['message_data']['text'].strip('@')
            timestamp = dm.created_timestamp
            temp_dict = {'sender':sender_id, 'account':account_to_search, 'timestamp':timestamp}
            dms_requests_list.append(temp_dict)

    dms_cancelled_list = []

    for dm in dms_received_list:
        if (str(dm.message_create['message_data']['text']).split()[0].strip().lower() == 'cancel') and (check_acc(str(dm.message_create['message_data']['text']).strip().split()[1].strip().lower()) == True):
            sender_id = dm.message_create['sender_id']
            account_to_cancel = dm.message_create['message_data']['text'].split()[1]
            timestamp = dm.created_timestamp
            temp_dict = {'sender':sender_id, 'account':account_to_cancel, 'timestamp':timestamp}
            dms_cancelled_list.append(temp_dict)
    
    return_list = [dms_requests_list,dms_cancelled_list]

    return return_list

# update the list of users and accounts to send updates to
def request_record(request_dict_list):
    not_cancelled_list = request_dict_list[0]
    cancelled_list = request_dict_list[1]

    infile = open("twitter-recording.txt",'r')
    info_list_init = infile.readlines()

    info_list = []

    for info in info_list_init:
        info_stripped = info.strip('\n')
        info_split = info_stripped.split('-')
        info_dict = {'sender':info_split[0],'account':info_split[1],'timestamp':info_split[2]}
        info_list.append(info_dict)

    for active_dict in not_cancelled_list:
        if active_dict not in info_list:
            info_list.append(active_dict)
    
    for cancel_dict in cancelled_list:
        for record_dict in info_list:
            if record_dict['sender'] == cancel_dict['sender'] and record_dict['account'] == cancel_dict['account'] and record_dict['timestamp'] < cancel_dict['timestamp']:
                info_list.remove(record_dict)
    infile.close()

    outfile = open('twitter-recording.txt','w')
    for dict in info_list:
        outfile.write(dict['sender'] + '-' + dict['account'] + '-' + dict['timestamp'] + '\n')

    outfile.close()

# main method to call
def main():
    dms_received = check_received_dms()
    request_record(dms_received)

    present_day = datetime.now()
    tomorrow = present_day + timedelta(1)
    current_time = present_day.strftime('%H')

    infile = open('time-recording.txt','r')
    file_day = infile.readline()
    infile.close()

    if int(present_day.day) == int(file_day) and int(current_time) == 13:
        infile = open('twitter-recording.txt','r')
        request_list = infile.readlines()
        for request in request_list:
            request_stripped = request.strip('\n')
            request_split = request_stripped.split('-')
            sender = request_split[0]
            account = request_split[1]
            text = top_tweets(account)
            send_message = api.send_direct_message(sender,text)
        outfile = open('time-recording.txt','w')
        outfile.write(str(tomorrow.day))
        outfile.close()

while True:
    main()
    time.sleep(15 * 60)
    # change to time.sleep(15 * 60), was 3


# def check_received():
#     messages = api.get_direct_messages()
#     my_name = 'mjdunat'
#     my_user = api.get_user(screen_name=my_name)
#     my_id = my_user.id_str

#     dms_received_list = []

#     for message in messages:
#         if message.message_create['target']['recipient_id'] == my_id:
#             dms_received_list.append(message)
    
#     dms_requests_list = []

#     for dm in dms_received_list:
#         if check_acc(dm.message_create['message_data']['text']) == True:
#             sender_id = dm.message_create['sender_id']
#             account_to_search = dm.message_create['message_data']['text']
#             timestamp = dm.created_timestamp
#             temp_dict = {'sender':sender_id, 'account':account_to_search, 'not_cancelled':True, 'timestamp':timestamp}
#             dms_requests_list.append(temp_dict)

#     dms_cancelled_list = []

#     for dm in dms_received_list:
#         if (str(dm.message_create['message_data']['text']).strip().split()[0].strip().lower() == 'cancel') and (check_acc(str(dm.message_create['message_data']['text']).strip().split()[1].strip().lower()) == True):
#             sender_id = dm.message_create['sender_id']
#             account_to_cancel = dm.message_create['message_data']['text']
#             timestamp = dm.created_timestamp
#             temp_dict = {'sender':sender_id, 'account':account_to_cancel, 'not_cancelled':False, 'timestamp':timestamp}
#             dms_cancelled_list.append(temp_dict)
    
#     for cancel_dict in dms_cancelled_list:
#         cancel_found = False
#         for request_dict in dms_requests_list:
#             if request_dict['sender'] == cancel_dict['sender'] and request_dict['account'] == cancel_dict['account'] and request_dict['timestamp'] < cancel_dict['timestamp']:
#                 request_dict['not_cancelled'] = False
#                 cancel_found = True
#             if cancel_found == False:
#                 dms_requests_list.append(cancel_dict)

#     return dms_requests_list
# print(check_received())

# def record_requests(dm_dict_list):
#     infile = open('twitter-recording.txt','r')
#     info_list = infile.readlines()

#     not_cancelled_list = []
#     cancelled_list = []

#     for dict in dm_dict_list:
#         if dict['not_cancelled'] == True:
#             not_cancelled_list.append(dict)
#         elif dict['not_cancelled'] == False:
#             cancelled_list.append(dict)

#     return_list = []

#     for line in info_list:
#         split_line = line.split('-')
#         sender_id = split_line[0]
#         account_to_search = split_line[1]
#         timestamp = split_line[2]
#         for dict in dm_dict_list:
#             if dict['sender'] == sender_id and dict['account'] == account_to_search and dict['not_cancelled'] == True:
#                 this = 0

    # for dict in dm_dict_list:





# def check_dms():
#     messages = api.get_direct_messages()
#     # print(messages[0].message_create['target']['recipient_id'])

#     # find my id
#     my_name = 'mjdunat'
#     my_user = api.get_user(screen_name=my_name)
#     my_id = my_user.id_str

#     customer_dict = {}

#     print('timestamp:')
#     print(messages[0].created_timestamp)
#     print('end')

#     for message in messages:
#         if message.message_create['target']['recipient_id'] == my_id:
#             if check_acc(message.message_create['message_data']['text']) == True:
#                 sender_id = message.message_create['sender_id']
#                 account_to_search = message.message_create['message_data']['text']
#                 timestamp = message.created_timestamp
#                 temp_dict = {'account':account_to_search,'not_cancelled':True, 'timestamp':timestamp}
#                 if sender_id not in customer_dict.keys():
#                     customer_dict[sender_id] = [temp_dict]
#                 else:
#                     customer_dict[sender_id].append(temp_dict)
#     for message in messages:
#         if message.message_create['target']['recipient_id'] == my_id:
#             if (str(message.message_create['message_data']['text']).strip().split()[0].strip().lower() == 'cancel') and (check_acc(str(message.message_create['message_data']['text']).strip().split()[1].strip().lower()) == True):
#                 sender_id = message.message_create['sender_id']
#                 cancel_acc = str(message.message_create['message_data']['text']).strip().split()[1].strip()
#                 temp_dict = {'account':cancel_acc,'not_cancelled':False}
#                 if sender_id in customer_dict.keys():
#                     for key in customer_dict.keys():
#                         if key == sender_id:
#                             account_found = False
#                             for item in customer_dict[key]:
#                                 if item['account'] == cancel_acc:
#                                     account_found = True
#                                     item['not_cancelled'] = False
#                             if account_found == False:
#                                 customer_dict[sender_id].append(temp_dict)
#                 else:
#                     temp_dict = {'account':cancel_acc,'not_cancelled':False}
#                     customer_dict[sender_id] = temp_dict
#     return customer_dict
# print(check_dms())