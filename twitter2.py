import urllib.request
import urllib.parse
import urllib.error
import twurl
import json
import ssl


def find_in_json(js, info):
    """
    returns info about user in json file
    (json-file, str) -> generator
    """
    i = 1
    for u in js['users']:
        yield str(i) + '. ' + u['screen_name']
        i += 1
        if u[info] == "":
            yield '  (No ' + info + ' found)'
            continue
        yield '  ' + u[info]


def get_json(acct, friends_num):
    """
    Returns a json-file with information about user
    (str) -> json-file
    """
    TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    # if friends_num:
    #     url = twurl.augment(TWITTER_URL,
    #                         {'screen_name': acct, 'count': friends_num})
    # else:
    #     url = twurl.augment(TWITTER_URL,
    #                         {'screen_name': acct})
    # print('Retrieving', url)
    url = twurl.augment(TWITTER_URL,
                        {'screen_name': acct, 'count': friends_num})
    connection = urllib.request.urlopen(url, context=ctx)
    data = connection.read().decode()
    js = json.loads(data, encoding='utf-8')
    return js


def get_info():
    """
    Returns information from user
    (None) -> str
    """
    print('')
    acct = input('Enter Twitter Account:')
    if (len(acct) < 1):
        return
    num_info = input(
        'Type 1 for name, 2 for description, 3 for location, \
4 for number of followers, 5 for numbers of following: ')
    lst = ['1', '2', '3', '4', '5']
    if num_info not in lst:
        return
    info_list = ['name', 'description', 'location', 'followers_count', 'friends_count']
    info = info_list[lst.index(num_info)]
    friends_num = input('Type number of friends you want to display: ')
    if friends_num.isdigit() is False:
        return
    return acct, info, friends_num


def main():
    """
    the main function of this module
    """
    while True:
        try:
            acct, info, friends_num = get_info()
        except:
            break
        js = get_json(acct, str(friends_num))
        with open('data.json', 'a', encoding='utf-8') as outfile:
            json.dump(js, outfile)
        print('')
        users = find_in_json(js, info)
        for u in users:
            print(u)


if __name__ == '__main__':
    main()
