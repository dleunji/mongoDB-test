import pymongo
import datetime
from test_main import users, posts
class Level_2_1:
    def __init__(self, users, posts):
        self.users = users
        self.posts = posts
        
    def is_registered_user(self, user_id):
        if users.count_documents({"user_id": user_id}, limit = 1) == 0:
            return False
        else:
            return True
            
    def add_user(self, user_id):
        # I've created unique index on user_id
        user = {"user_id": user_id, "friends": []}
        try:
            users.insert_one(user)
            return True
        except pymongo.errors.DuplicateKeyError:
            return False
        except pymongo.errors.WriteError:
            return False

    def write_message(self, user_id, message, timestamp):
        # check whether the author is registered user
        if not self.is_registered_user(user_id):
            return 0
        # make auto increment message_id
        last_messages = list(posts.find({"author": user_id}).sort("message_id", -1).limit(1))
        message_id = 1

        if len(last_messages) > 0:
            message_id = last_messages[0]["message_id"] + 1
        post = {"author": user_id, "message": message, "timestamp": timestamp, "datetime": datetime.datetime.now(), "message_id": message_id}
        
        try:
            posts.insert_one(post)
            return message_id
        except pymongo.errors.WriteError:
            return 0

    def add_friend(self, user_id, be_followed_user_id):
        if not self.is_registered_user(user_id):
            return False
        elif not self.is_registered_user(be_followed_user_id):
            return False

        user = users.find_one({"user_id" : user_id})

        if be_followed_user_id in user["friends"]:
            return False
        try:
            users.update_one({"user_id": user_id},
                        {"$push": {
                            "friends": be_followed_user_id
                        }})
            return True
        except pymongo.errors.WriteError:
            return False

    def show_friend_list(self, user_id):
        if not self.is_registered_user(user_id):
            return []

        followed_user = users.find_one({"user_id": user_id})
        friends = followed_user['friends']
        print(friends)
        friends.sort()
        return friends

    def show_message_list(self, user_id):
        if not self.is_registered_user(user_id):
            return []

        authors = self.show_friend_list(user_id)
        authors.append(user_id)
        messages = []

        post_list = posts.find({
            "author": {
                "$in": authors
            }
        }).sort([("timestamp", pymongo.DESCENDING), ("author", pymongo.ASCENDING),
                ("datetime", pymongo.DESCENDING)]).limit(100)
        for post in post_list:
            messages.append(post["message"])

        return messages

    # New feature
    def remove_message(self, user_id, message_id):
        if not self.is_registered_user(user_id):
            return False
        message_id = int(message_id)
        post = posts.find_one({"author" : user_id, "message_id": message_id})
        if post == None:
            return False

        try:
            posts.delete_one({"author" : user_id, "message_id": message_id})
            return True
        except pymongo.errors.WriteError:
            return False

    # New feature
    def remove_friend(self, user_id, be_unfollowed_user_id):
        if not self.is_registered_user(user_id):
            return False

        elif not self.is_registered_user(be_unfollowed_user_id):
            return False

        # be_unfollowed_user_id isn't friend of user_id
        friends = users.find_one({"user_id": user_id})["friends"]
        if not be_unfollowed_user_id in friends:
            return False

        try:
            users.update_one({"user_id" : user_id}, {"$pull": {
                            "friends": be_unfollowed_user_id
                        }})
            return True
        except pymongo.errors.WriteError:
            return False
