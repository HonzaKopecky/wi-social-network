import numpy as np
import scipy.linalg as la


class SpectralCluster:
    @staticmethod
    def compute_eigen(laplacian_matrix, users):
        numpy_matrix = np.array(laplacian_matrix)
        eigen_values, _ = la.eig(numpy_matrix)
        for _, user in users.items():
            user.eigen_value = eigen_values[user.id]
        return users

    @staticmethod
    def generate_laplacian(users):
        matrix = [None] * len(users)
        for _, user in users.items():
            matrix[user.id] = [0] * len(users)
            matrix[user.id][user.id] = len(user.friends)
            for friend in user.friends:
                matrix[user.id][friend.id] = -1
        return matrix

    @staticmethod
    def divide(users_dict, level):
        users_list = list(users_dict.values())
        users_list = sorted(users_list, key=lambda user: user.eigen_value)
        return SpectralCluster.divide_inner(users_list, level)

    @staticmethod
    def divide_inner(users, level):
        if level == 0:
            return users
        index = SpectralCluster.find_divide_index(users)
        left = SpectralCluster.divide_inner(users[:index+1], level - 1)
        right = SpectralCluster.divide_inner(users[index+1:], level - 1)
        return left, right

    @staticmethod
    def find_divide_index(users):
        max_diff = -1
        index = None
        for i in range(0, len(users) - 1):
            diff = abs(users[i + 1].eigen_value - users[i].eigen_value)
            if diff > max_diff:
                max_diff = diff
                index = i
        return index

