import pymongo
import datetime
from test_main import users, posts

class Level_3:
    def __init__(self, client):
        self.client = client

        self.users = client.sns.users
        self.posts = client.sns.posts
        
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
        post_list = posts.find({
            "author": {
                "$in": authors
            }
        }).sort([("timestamp", pymongo.DESCENDING), ("author", pymongo.ASCENDING),
                ("datetime", pymongo.DESCENDING)]).limit(100)
        for post in post_list:
            messages.append(post["message"])

        return messages

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

    def remove_user(self, user_id):
        if not self.is_registered_user(user_id):
            return False

        # Transaction is added from 4.0
        with self.client.start_session() as session:
            with session.start_transaction():
                # 1. Delete user from other users' friend list
                follower_list = self.users.find({"friends" : user_id})
                for follower in follower_list:
                    self.remove_friend(follower["user_id"],user_id)

                # 2. Delete the user's info
                self.users.delete_one({"user_id": user_id})

                # 3. Delete posts the user wrote.
                self.posts.delete_many({"author": user_id})
                return True
        return False    
