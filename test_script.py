import pytest
import pymongo
from pymongo import MongoClient
from ns_level_0 import Level_0
from ns_level_1 import Level_1
from ns_level_2_1 import Level_2_1
from ns_level_2_2 import Level_2_2
from ns_level_3 import Level_3
uri = "mongodb://gauss-db-swe-intern-minipjt:hhTl0FyvjfS7pYk3Wgv4VpxVa3QQTI1N6YNo6yNc39jOMYjZ2ATI6SVchJ2xYThcMRzlTLoldReTQeTrvTxrSQ==@gauss-db-swe-intern-minipjt.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@gauss-db-swe-intern-minipjt@"

@pytest.fixture(scope="function")
def init_db():
    client = MongoClient(uri)
    if "sns" in client.list_database_names():
        client.drop_database("sns")
    
    db = client.sns
    users = db.users 
    posts = db.posts

    # Create required indexes
    users.create_index([("user_id", pymongo.ASCENDING)], unique=True)
    indexes = pymongo.IndexModel([("timestamp", pymongo.DESCENDING), ("author", pymongo.ASCENDING),
             ("datetime", pymongo.DESCENDING)])
    posts.create_indexes([indexes])
    posts.create_index([("author", pymongo.ASCENDING)])
    posts.create_index([("message_id", pymongo.ASCENDING)])

    return client

@pytest.mark.parametrize("file_name", [("0")])
def test_level_0(init_db, file_name):
    client = init_db
    db = client.sns
    users = db.users 
    posts = db.posts

    level_0 = Level_0(users,posts)

    f_input = open(f"./tests/in{file_name}.txt")
    f_output = open(f"./tests/out{file_name}.txt")
    input = f_input.readline
    output = f_output.readline
    Q = int(input())
    for q in range(Q):
        tokens = input().split()
        cmd = int(tokens[0])

        if cmd == 100:
            user_id = str(tokens[1])
            level_0.add_user(user_id)

        elif cmd == 200:
            user_id = str(tokens[1])
            message = str(tokens[2])
            timestamp = int(tokens[3])
            level_0.write_message(user_id, message, timestamp)

        elif cmd == 300:
            user_id = str(tokens[1])
            be_followed_user_id = str(tokens[2])
            level_0.add_friend(user_id, be_followed_user_id)

        elif cmd == 400:
            user_id = str(tokens[1])
            friend_list = level_0.show_friend_list(user_id)

            result = []
            result.append(str(len(friend_list)))
    
            for item in friend_list:
                result.append(item)
            assert output().strip() == " ".join(result)

        elif cmd == 500:
            user_id = str(tokens[1])
            message_list = level_0.show_message_list(user_id)

            result = []
            result.append(str(len(message_list)))

            for item in message_list:
                result.append(item)
            assert output().strip() == " ".join(result)

        else:
            pass
    f_input.close()
    f_output.close()

@pytest.mark.parametrize("file_name", [("1")])
def test_level_1(init_db, file_name):
    client = init_db
    db = client.sns
    users = db.users 
    posts = db.posts

    level_1 = Level_1(users,posts)

    f_input = open(f"./tests/in{file_name}.txt")
    f_output = open(f"./tests/out{file_name}.txt")
    input_line = f_input.readline
    output_line = f_output.readline

    Q = int(input_line())
    for q in range(Q):
        tokens = input_line().split()
        cmd = int(tokens[0])

        if cmd == 100:
            user_id = str(tokens[1])
            success = level_1.add_user(user_id)
            assert(output_line().strip() == str(success))
            print(success)

        elif cmd == 200:
            user_id = str(tokens[1])
            message = str(tokens[2])
            timestamp = int(tokens[3])
            success = level_1.write_message(user_id, message, timestamp)
            assert(output_line().strip() == str(success))
            print(success)

        elif cmd == 300:
            user_id = str(tokens[1])
            be_followed_user_id = str(tokens[2])
            success = level_1.add_friend(user_id, be_followed_user_id)
            assert(output_line().strip() == str(success))
            print(success)

        elif cmd == 400:
            user_id = str(tokens[1])
            friend_list = level_1.show_friend_list(user_id)

            result = []
            result.append(str(len(friend_list)))
    
            for item in friend_list:
                result.append(item)
            assert output_line().strip() == " ".join(result)

        elif cmd == 500:
            user_id = str(tokens[1])
            message_list = level_1.show_message_list(user_id)

            result = []
            result.append(str(len(message_list)))

            for item in message_list:
                result.append(item)
            assert output_line().strip() == " ".join(result)

        else:
            pass

    f_input.close()
    f_output.close()

@pytest.mark.parametrize("file_name", [("2")])
def test_level_2_1(init_db, file_name):
    client = init_db
    db = client.sns
    users = db.users 
    posts = db.posts

    level_2 = Level_2_1(users,posts)

    f_input = open(f"./tests/in{file_name}.txt")
    f_output = open(f"./tests/out{file_name}.txt")
    input_line = f_input.readline
    output_line = f_output.readline

    Q = int(input_line())
    for q in range(Q):
        tokens = input_line().split()
        cmd = int(tokens[0])

        if cmd == 100:
            user_id = str(tokens[1])
            success = level_2.add_user(user_id)
            assert(output_line().strip() == str(success))

        elif cmd == 200:
            user_id = str(tokens[1])
            message = str(tokens[2])
            timestamp = int(tokens[3])
            message_id = level_2.write_message(user_id, message, timestamp)
            assert(output_line().strip() == str(message_id))

        elif cmd == 300:
            user_id = str(tokens[1])
            be_followed_user_id = str(tokens[2])
            success = level_2.add_friend(user_id, be_followed_user_id)
            assert(output_line().strip() == str(success))
            print(success)

        elif cmd == 400:
            user_id = str(tokens[1])
            friend_list = level_2.show_friend_list(user_id)

            result = []
            result.append(str(len(friend_list)))
    
            for item in friend_list:
                result.append(item)
            assert output_line().strip() == " ".join(result)

        elif cmd == 500:
            user_id = str(tokens[1])
            message_list = level_2.show_message_list(user_id)

            result = []
            result.append(str(len(message_list)))

            for item in message_list:
                result.append(item)
            assert output_line().strip() == " ".join(result)

        elif cmd == 600:
            user_id = str(tokens[1])
            message_id = str(tokens[2])
            success = level_2.remove_message(user_id, message_id)
            assert(output_line().strip() == str(success))
            print(success)

        elif cmd == 700:
            user_id = str(tokens[1])
            be_unfollowed_user_id = str(tokens[2])
            success = level_2.remove_friend(user_id, be_unfollowed_user_id)
            assert(output_line().strip() == str(success))
            print(success)
            
        else:
            pass

    f_input.close()
    f_output.close()

@pytest.mark.parametrize("file_name", [("2")])
def test_level_2_2(init_db, file_name):
    client = init_db
    db = client.sns
    users = db.users 
    posts = db.posts

    level_2 = Level_2_2(users,posts)

    f_input = open(f"./tests/in{file_name}.txt")
    f_output = open(f"./tests/out{file_name}.txt")
    input_line = f_input.readline
    output_line = f_output.readline

    Q = int(input_line())
    for q in range(Q):
        tokens = input_line().split()
        cmd = int(tokens[0])

        if cmd == 100:
            user_id = str(tokens[1])
            success = level_2.add_user(user_id)
            assert(output_line().strip() == str(success))

        elif cmd == 200:
            user_id = str(tokens[1])
            message = str(tokens[2])
            timestamp = int(tokens[3])
            message_id = level_2.write_message(user_id, message, timestamp)
            assert(output_line().strip() == str(message_id))

        elif cmd == 300:
            user_id = str(tokens[1])
            be_followed_user_id = str(tokens[2])
            success = level_2.add_friend(user_id, be_followed_user_id)
            assert(output_line().strip() == str(success))

        elif cmd == 400:
            user_id = str(tokens[1])
            friend_list = level_2.show_friend_list(user_id)

            result = []
            result.append(str(len(friend_list)))
    
            for item in friend_list:
                result.append(item)
            assert output_line().strip() == " ".join(result)

        elif cmd == 500:
            user_id = str(tokens[1])
            message_list = level_2.show_message_list(user_id)

            result = []
            result.append(str(len(message_list)))

            for item in message_list:
                result.append(item)
            assert output_line().strip() == " ".join(result)

        elif cmd == 600:
            user_id = str(tokens[1])
            message_id = str(tokens[2])
            success = level_2.remove_message(user_id, message_id)
            assert(output_line().strip() == str(success))

        elif cmd == 700:
            user_id = str(tokens[1])
            be_unfollowed_user_id = str(tokens[2])
            success = level_2.remove_friend(user_id, be_unfollowed_user_id)
            assert(output_line().strip() == str(success))
            
        else:
            pass

    f_input.close()
    f_output.close()

@pytest.mark.parametrize("file_name", [("3")])
def test_level_3(init_db, file_name):
    client = init_db

    level_3 = Level_3(client)

    f_input = open(f"./tests/in{file_name}.txt")
    f_output = open(f"./tests/out{file_name}.txt")
    input_line = f_input.readline
    output_line = f_output.readline

    Q = int(input_line())
    for q in range(Q):
        tokens = input_line().split()
        cmd = int(tokens[0])

        if cmd == 100:
            user_id = str(tokens[1])
            success = level_3.add_user(user_id)
            assert(output_line().strip() == str(success))

        elif cmd == 200:
            user_id = str(tokens[1])
            message = str(tokens[2])
            timestamp = int(tokens[3])
            message_id = level_3.write_message(user_id, message, timestamp)
            assert(output_line().strip() == str(message_id))

        elif cmd == 300:
            user_id = str(tokens[1])
            be_followed_user_id = str(tokens[2])
            success = level_3.add_friend(user_id, be_followed_user_id)
            assert(output_line().strip() == str(success))

        elif cmd == 400:
            user_id = str(tokens[1])
            friend_list = level_3.show_friend_list(user_id)

            result = []
            result.append(str(len(friend_list)))
    
            for item in friend_list:
                result.append(item)
            assert output_line().strip() == " ".join(result)

        elif cmd == 500:
            user_id = str(tokens[1])
            message_list = level_3.show_message_list(user_id)

            result = str(len(message_list))

            result = []
            result.append(str(len(message_list)))

            for item in message_list:
                result.append(item)
            assert output_line().strip() == " ".join(result)

        elif cmd == 600:
            user_id = str(tokens[1])
            message_id = str(tokens[2])
            success = level_3.remove_message(user_id, message_id)
            assert(output_line().strip() == str(success))

        elif cmd == 700:
            user_id = str(tokens[1])
            be_unfollowed_user_id = str(tokens[2])
            success = level_3.remove_friend(user_id, be_unfollowed_user_id)
            assert(output_line().strip() == str(success))
        
        elif cmd == 800:
            user_id = str(tokens[1])
            success = level_3.remove_user(user_id)
            assert(output_line().strip() == str(success))

        else:
            pass

    f_input.close()
    f_output.close()

