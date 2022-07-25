# input command
# 100 - add_user
# 200 - write_message
# 300 - add_friend
# 400 - show_friend_list
# 500 - show_message_list
# 600 - remove_message
# 700 - remove_friend
# 800 - remove_user
import sys
from pymongo import MongoClient
uri = "mongodb://gauss-db-swe-intern-minipjt:hhTl0FyvjfS7pYk3Wgv4VpxVa3QQTI1N6YNo6yNc39jOMYjZ2ATI6SVchJ2xYThcMRzlTLoldReTQeTrvTxrSQ==@gauss-db-swe-intern-minipjt.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@gauss-db-swe-intern-minipjt@"
client = MongoClient(uri)
db = client.sns
users = db.users
posts = db.posts

getline = sys.stdin.readline

def level_0():
    from ns_level_0 import add_user
    from ns_level_0 import write_message
    from ns_level_0 import add_friend
    from ns_level_0 import show_friend_list
    from ns_level_0 import show_message_list

    Q = int(getline())
    for q in range(Q):
        tokens = getline().split()
        cmd = int(tokens[0])

        if cmd == 100:
            user_id = str(tokens[1])
            add_user(user_id)

        elif cmd == 200:
            user_id = str(tokens[1])
            message = str(tokens[2])
            timestamp = int(tokens[3])
            write_message(user_id, message, timestamp)

        elif cmd == 300:
            user_id = str(tokens[1])
            be_followed_user_id = str(tokens[2])
            add_friend(user_id, be_followed_user_id)

        elif cmd == 400:
            user_id = str(tokens[1])
            friend_list = show_friend_list(user_id)

            print(len(friend_list), end='')
            for item in friend_list:
                print(" " + item, end='')
            print()

        elif cmd == 500:
            user_id = str(tokens[1])
            message_list = show_message_list(user_id)

            print(len(message_list), end='')
            for item in message_list:
                print(" " + item, end='')
            print()

        else:
            pass


def level_1():
    from ns_level_1 import add_user
    from ns_level_1 import write_message
    from ns_level_1 import add_friend
    from ns_level_1 import show_friend_list
    from ns_level_1 import show_message_list

    Q = int(getline())
    for q in range(Q):
        tokens = getline().split()
        cmd = int(tokens[0])

        if cmd == 100:
            user_id = str(tokens[1])
            success = add_user(user_id)
            print(success)

        elif cmd == 200:
            user_id = str(tokens[1])
            message = str(tokens[2])
            timestamp = int(tokens[3])
            success = write_message(user_id, message, timestamp)
            print(success)

        elif cmd == 300:
            user_id = str(tokens[1])
            be_followed_user_id = str(tokens[2])
            success = add_friend(user_id, be_followed_user_id)
            print(success)

        elif cmd == 400:
            user_id = str(tokens[1])
            friend_list = show_friend_list(user_id)

            print(len(friend_list), end='')
            for item in friend_list:
                print(" " + item, end='')
            print()

        elif cmd == 500:
            user_id = str(tokens[1])
            message_list = show_message_list(user_id)

            print(len(message_list), end='')
            for item in message_list:
                print(" " + item, end='')
            print()

        else:
            pass


def level_2_1():
    from ns_level_2_1 import add_user
    from ns_level_2_1 import write_message
    from ns_level_2_1 import add_friend
    from ns_level_2_1 import show_friend_list
    from ns_level_2_1 import show_message_list
    from ns_level_2_1 import remove_message
    from ns_level_2_1 import remove_friend

    Q = int(getline())
    for q in range(Q):
        tokens = getline().split()
        cmd = int(tokens[0])

        if cmd == 100:
            user_id = str(tokens[1])
            success = add_user(user_id)
            print(success)

        elif cmd == 200:
            user_id = str(tokens[1])
            message = str(tokens[2])
            timestamp = int(tokens[3])
            message_id = write_message(user_id, message, timestamp)
            print(message_id)

        elif cmd == 300:
            user_id = str(tokens[1])
            be_followed_user_id = str(tokens[2])
            success = add_friend(user_id, be_followed_user_id)
            print(success)

        elif cmd == 400:
            user_id = str(tokens[1])
            friend_list = show_friend_list(user_id)

            print(len(friend_list), end='')
            for item in friend_list:
                print(" " + item, end='')
            print()

        elif cmd == 500:
            user_id = str(tokens[1])
            message_list = show_message_list(user_id)

            print(len(message_list), end='')
            for item in message_list:
                print(" " + item, end='')
            print()

        elif cmd == 600:
            user_id = str(tokens[1])
            message_id = str(tokens[2])
            success = remove_message(user_id, message_id)
            print(success)

        elif cmd == 700:
            user_id = str(tokens[1])
            be_unfollowed_user_id = str(tokens[2])
            success = remove_friend(user_id, be_unfollowed_user_id)
            print(success)

        else:
            pass


def level_3():
    from ns_level_3 import add_user
    from ns_level_3 import write_message
    from ns_level_3 import add_friend
    from ns_level_3 import show_friend_list
    from ns_level_3 import show_message_list
    from ns_level_3 import remove_message
    from ns_level_3 import remove_friend
    from ns_level_3 import remove_user

    Q = int(getline())
    for q in range(Q):
        tokens = getline().split()
        cmd = int(tokens[0])

        if cmd == 100:
            user_id = str(tokens[1])
            success = add_user(user_id)
            print(success)

        elif cmd == 200:
            user_id = str(tokens[1])
            message = str(tokens[2])
            timestamp = int(tokens[3])
            message_id = write_message(user_id, message, timestamp)
            print(message_id)

        elif cmd == 300:
            user_id = str(tokens[1])
            be_followed_user_id = str(tokens[2])
            success = add_friend(user_id, be_followed_user_id)
            print(success)

        elif cmd == 400:
            user_id = str(tokens[1])
            friend_list = show_friend_list(user_id)

            print(len(friend_list), end='')
            for item in friend_list:
                print(" " + item, end='')
            print()

        elif cmd == 500:
            user_id = str(tokens[1])
            message_list = show_message_list(user_id)

            print(len(message_list), end='')
            for item in message_list:
                print(" " + item, end='')
            print()

        elif cmd == 600:
            user_id = str(tokens[1])
            message_id = str(tokens[2])
            success = remove_message(user_id, message_id)
            print(success)

        elif cmd == 700:
            user_id = str(tokens[1])
            be_unfollowed_user_id = str(tokens[2])
            success = remove_friend(user_id, be_unfollowed_user_id)
            print(success)

        elif cmd == 800:
            user_id = str(tokens[1])
            success = remove_user(user_id)
            print(success)

        else:
            pass


def level_4():
    from ns_level_4 import add_user
    from ns_level_4 import write_message
    from ns_level_4 import add_friend
    from ns_level_4 import show_friend_list
    from ns_level_4 import show_message_list
    from ns_level_4 import remove_message
    from ns_level_4 import remove_friend
    from ns_level_4 import remove_user

    Q = int(getline())
    for q in range(Q):
        tokens = getline().split()
        cmd = int(tokens[0])

        if cmd == 100:
            user_id = str(tokens[1])
            success = add_user(user_id)
            print(success)

        elif cmd == 200:
            user_id = str(tokens[1])
            message = str(tokens[2])
            timestamp = int(tokens[3])
            message_id = write_message(user_id, message, timestamp)
            print(message_id)

        elif cmd == 300:
            user_id = str(tokens[1])
            be_followed_user_id = str(tokens[2])
            success = add_friend(user_id, be_followed_user_id)
            print(success)

        elif cmd == 400:
            user_id = str(tokens[1])
            count = int(tokens[2])
            first = True if str(tokens[3]) == "True" else False
            partial_friend_list = show_friend_list(user_id, count, first)

            print(len(partial_friend_list), end='')
            for item in partial_friend_list:
                print(" " + item, end='')
            print()

        elif cmd == 500:
            user_id = str(tokens[1])
            message_list = show_message_list(user_id)

            print(len(message_list), end='')
            for item in message_list:
                print(" " + item, end='')
            print()

        elif cmd == 600:
            user_id = str(tokens[1])
            message_id = str(tokens[2])
            success = remove_message(user_id, message_id)
            print(success)

        elif cmd == 700:
            user_id = str(tokens[1])
            be_unfollowed_user_id = str(tokens[2])
            success = remove_friend(user_id, be_unfollowed_user_id)
            print(success)

        elif cmd == 800:
            user_id = str(tokens[1])
            success = remove_user(user_id)
            print(success)

        else:
            pass


def main():
    # level_0()

#    level_1()
    level_2_1()
#    level_3()
#    level_4()

if __name__ == "__main__":
    main()
