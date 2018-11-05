class User:
    def __init__(self, id, username):
        self.id = id
        self.username = username
        self.friends = set()
        self.friendsNames = set()
        self.review = None
        self.summary = None
        self.eigen_value = None

    def add_friend(self, user):
        self.friends.add(user)
