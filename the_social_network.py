from model.user import User
from model.product import Product
from model.review import Review
from lib.spectral_clustering import SpectralCluster
import pickle


def parse_user(cnt, line, file):
    name = line.split(':')[1].strip()
    new_user = User(cnt, name)
    names = file.readline().replace('friends:\t', '').split('\t')
    new_user.friendsNames = set(names)
    new_user.summary = parse_line('summary', file)
    new_user.review = parse_line('review', file)
    return new_user


def connect_friends(users):
    for _, user in users.items():
        for name in user.friendsNames:
            if name not in users:
                continue
            else:
                user.add_friend(users[name])
    return users


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


def save_users(users, path):
    f = open(path, "wb")
    pickle.dump(users, f)
    f.close()


def load_users(path):
    f = open(path, "rb")
    users = pickle.load(f)
    users = connect_friends(users)
    return users


# users = dict()
#
# with open('./data/reviews') as file:
#     for cnt, line in enumerate(file):
#         if line.startswith('user: '):
#             user = parse_user(len(users), line, file)
#             users[user.username] = user
#         if len(users) == 100:
#             break
#
# connect_friends(users)
#
# laplacian_matrix = SpectralCluster.generate_laplacian(users)
# eigen_users = SpectralCluster.compute_eigen(laplacian_matrix, users)
#
# save_users(eigen_users, 'out/100users')

users = load_users('out/users')

print(len(users))
left, right = SpectralCluster.divide(users, 1)

print(len(left))
print(len(right))

# products = []
# with open('./data/training') as file:
#     for cnt, line in enumerate(file):
#         if line.startswith('product/productId: '):
#             product = parse_product(line, file)
#             products.append(product)
#
# print(len(products))

