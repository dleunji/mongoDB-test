import pymongo
import datetime

class Level_0:
    def __init__(self, users, posts):
        self.users = users
        self.posts = posts

    # Register user
    def add_user(self, user_id):
        # It is guaranteed that user_id is unique
        user = {"user_id": user_id, "friends": []}
        self.users.insert_one(user)
    # Post
    def write_message(self, user_id, message, timestamp):
        post = {"author": user_id, "message": message, "timestamp": timestamp, "datetime": datetime.datetime.now()}
        self.posts.insert_one(post)


    # Add friend
    def add_friend(self, user_id, be_followed_user_id):
        # be_followed_user_id will be a friend of user_id
        self.users.update_one({"user_id": user_id},
                        {"$push": {
                            "friends": be_followed_user_id
                        }})

    # Show user's friends
    def show_friend_list(self, user_id):
        followed_user = self.users.find_one({"user_id": user_id})
        friends = followed_user['friends']
        friends.sort()
        return friends


    # Show users' posts
    def show_message_list(self, user_id):
        messages = []
        authors = self.show_friend_list(user_id)
        authors.append(user_id)
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
