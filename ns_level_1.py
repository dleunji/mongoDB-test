
import pymongo
import datetime

class Level_1:
    def __init__(self, users, posts):
        self.users = users
        self.posts = posts

    def is_registered_user(self, user_id):
        if self.users.count_documents({"user_id": user_id}, limit = 1) == 0:
            return False
        else:
            return True

    def add_user(self, user_id):
        # I've created unique index on user_id
        user = {"user_id": user_id, "friends": []}
        try:
            self.users.insert_one(user)
            return True
        except pymongo.errors.DuplicateKeyError:
            return False
        except pymongo.errors.WriteError:
            return False


    def write_message(self, user_id, message, timestamp):
        # check whether the author is registered user
        if not self.is_registered_user(user_id):
            return False

        post = {"author": user_id, "message": message, "timestamp": timestamp, "datetime": datetime.datetime.now()}
        try:
            self.posts.insert_one(post)
            return True
        except pymongo.errors.WriteError:
            return False

    def add_friend(self, user_id, be_followed_user_id):
        if not self.is_registered_user(user_id):
            return False
        elif not self.is_registered_user(be_followed_user_id):
            return False

        user = self.users.find_one({"user_id" : user_id})

        if be_followed_user_id in user["friends"]:
            return False

        try:
            self.users.update_one({"user_id": user_id},
                        {"$push": {
                            "friends": be_followed_user_id
                        }})
            return True
        except pymongo.errors.WriteError:
            return False
        

    def show_friend_list(self, user_id):
        if not self.is_registered_user(user_id):
            return []

        followed_user = self.users.find_one({"user_id": user_id})
        friends = followed_user['friends']

        friends.sort()
        return friends

    def show_message_list(self, user_id):
        if not self.is_registered_user(user_id):
            return []

        authors = self.show_friend_list(user_id)
        authors.append(user_id)
        messages = []
        # Sort by timestamp in descending order, user_id in ascending order, and most recent.
        # _id isn't incremental, so I used datetime to check the order of creation
        post_list = self.posts.find({
            "author": {
                "$in": authors
            }
        }).sort([("timestamp", pymongo.DESCENDING), ("author", pymongo.ASCENDING),
                ("datetime", pymongo.DESCENDING)]).limit(100)
        for post in post_list:
            messages.append(post['message'])

        return messages
