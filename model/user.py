class User:
    def __init__(self, username):
        self.username = username
        self.friends = set()
        self.friendsNames = set()
        self.review = None
        self.summary = None

    def add_friend(self, user):
        self.friends.add(user)
