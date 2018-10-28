from model.user import User
from model.product import Product
from model.review import Review


def parse_user(line, file):
    name = line.split()[1]
    new_user = User(name)
    names = file.readline().replace('friends:\t', '').split('\t')
    new_user.friendsNames = set(names)
    new_user.summary = parse_line('summary', file)
    new_user.review = parse_line('review', file)
    return new_user


def connect_friends(user, dictionary):
    for name in user.friendsNames:
        if name not in dictionary:
            continue
        else:
            user.add_friend(dictionary[name])


def parse_product(first, file):
    product_id = first.split()[1]
    review = parse_review(file)
    return Product(product_id, review)


def parse_review(file):
    review = Review()
    review.user_id = parse_line('review/userId', file)
    review.profile_name = parse_line('review/profileName', file)
    review.helpfulness = parse_line('review/helpfulness', file)
    review.score = parse_line('review/score', file)
    review.time = parse_line('review/time', file)
    review.summary = parse_line('review/summary', file)
    review.text = parse_line('review/text', file)
    return review


def parse_line(line_key, file):
    line = file.readline()
    if line.startswith(line_key):
        value = line.split()[1]
    else:
        print('Line does not start with proper key.')
    if value == '*':
        value = None
    return value


users = dict()

with open('./data/reviews') as file:
    for cnt, line in enumerate(file):
        if line.startswith('user: '):
            user = parse_user(line, file)
            users[user.username] = user

for name, user in users.items():
    connect_friends(user, users)

print(users['abbey'].review)

products = []
with open('./data/training') as file:
    for cnt, line in enumerate(file):
        if line.startswith('product/productId: '):
            product = parse_product(line, file)
            products.append(product)

print(len(products))

