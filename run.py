import praw
import configparser
import time
import pickledb


class C:
    W, G, R, P, Y, C = '\033[0m', '\033[92m', '\033[91m', '\033[95m', '\033[93m', '\033[36m'


def main():
    config = configparser.ConfigParser()
    config.read('conf.ini')
    reddit_user = config['REDDIT']['reddit_user']
    reddit_pass = config['REDDIT']['reddit_pass']
    client_id = config['REDDIT']['client_id']
    client_secret = config['REDDIT']['client_secret']
    target_subreddit = config['SETTINGS']['target_subreddit']
    sleep_time = int(config['SETTINGS']['sleep_time'])
    test_mode = config['SETTINGS'].getboolean('test_mode')

    db = pickledb.load('users.db', False)

    reddit = praw.Reddit(
        username=reddit_user,
        password=reddit_pass,
        client_id=client_id,
        client_secret=client_secret,
        user_agent='Invite Bot (by u/impshum)'
    )

    tm = ''
    if test_mode:
        tm = f'{C.R}TEST MODE{C.Y}'

    print(f"""{C.Y}
╦╔╗╔╦  ╦╦╔╦╗╔═╗  ╔╗ ╔═╗╔╦╗
║║║║╚╗╔╝║ ║ ║╣   ╠╩╗║ ║ ║  {tm}
╩╝╚╝ ╚╝ ╩ ╩ ╚═╝  ╚═╝╚═╝ ╩  {C.C}v1.0 {C.G}impshum{C.W}
    """)

    populate_db(db)

    for user in db.getall():
        approved = db.get(user)
        now = time.strftime("%d/%m/%Y %H:%M:%S", time.gmtime(time.time()))
        if not approved:
            if not test_mode:
                reddit.subreddit(target_subreddit).contributor.add(user)
                db.set(user, 1)
                db.dump()
            print(f'{C.P}{now} {C.G}Approved {user}{C.W}')
            if not test_mode:
                time.sleep(sleep_time)
        else:
            print(f'{C.P}{now} {C.Y}Already Approved {user}{C.W}')


def populate_db(db):
    with open('users.txt') as f:
        users = f.readlines()
    for user in users:
        user = user.strip()
        if not db.exists(user):
            db.set(user, 0)
            db.dump()
            print(f'{C.P}{C.G}Added {user} to db{C.W}')
        else:
            print(f'{C.P}{C.Y}{user} exists in db{C.W}')


if __name__ == '__main__':
    main()
