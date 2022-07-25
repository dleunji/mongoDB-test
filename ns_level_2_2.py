import pymongo
import datetime
from test_main import users, posts
import copy
class Level_2_2:
    def __init__(self, users, posts):
        self.users = users
        self.posts = posts
        # cache
        self.cache_friends_per_user = {}
        self.cache_posts_per_user = {}
        
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
        last_messages = list(posts.find({"author": user_id}).sort("message_id", pymongo.DESCENDING).limit(1))
        message_id = 1

        if len(last_messages) > 0:
            message_id = last_messages[0]["message_id"] + 1
        post = {"author": user_id, "message": message, "timestamp": timestamp, "datetime": datetime.datetime.now(), "message_id": message_id}


        try:
            posts.insert_one(post)
            # update cache
            self.cache_posts_per_user.update({user_id: list(posts.find({"author": user_id}))})
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
            # update cache
            friend_list = users.find_one({"user_id": user_id})["friends"]

            self.cache_friends_per_user.update({user_id: friend_list})
            return True
        except pymongo.errors.WriteError:
            return False

    def show_friend_list(self, user_id):
        if not self.is_registered_user(user_id):
            return []

        if user_id in self.cache_friends_per_user:
            friends = self.cache_friends_per_user[user_id]

            return friends

        friend_list = users.find_one({"user_id": user_id})["friends"]
        friend_list.sort()

        # update cache
        self.cache_friends_per_user.update({user_id: friend_list})
        return friend_list

    def show_message_list(self, user_id):
        if not self.is_registered_user(user_id):
            return []

        authors = copy.deepcopy(self.show_friend_list(user_id))
        authors.append(user_id)

        messages = []

        post_list = posts.find({
            "author": {
                "$in": authors
            }
        }).sort([("timestamp", pymongo.DESCENDING), ("author", pymongo.ASCENDING),
                ("datetime", pymongo.DESCENDING)]).limit(100)
        

        for post in post_list:
            print(post["message"])
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
            # update cache
            self.cache_posts_per_user.update({user_id: list(posts.find({"author": user_id}))})
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
            # update cache
            friend_list = users.find_one({"user_id": user_id})["friends"]
            self.cache_friends_per_user.update({user_id: friend_list})
            return True
        except pymongo.errors.WriteError:
            return False