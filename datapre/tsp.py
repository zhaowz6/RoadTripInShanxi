import pandas as pd
import numpy as np
from py2neo import Graph


class DistanceMatrix:
    def __init__(self, csv_file=None, neo4j_uri=None, neo4j_user=None, neo4j_password=None):
        """
        初始化 DistanceMatrix 类.

        :param csv_file: CSV 文件的路径（可选）
        :param neo4j_uri: Neo4j 数据库的 URI（可选）
        :param neo4j_user: Neo4j 数据库的用户名（可选）
        :param neo4j_password: Neo4j 数据库的密码（可选）
        """
        self.csv_file = csv_file
        self.neo4j_uri = neo4j_uri
        self.neo4j_user = neo4j_user
        self.neo4j_password = neo4j_password

        self.city_to_index = {}
        self.distance_matrix = None
        self.all_cities = []

        if self.csv_file:
            self._create_distance_matrix_from_csv()
        elif self.neo4j_uri:
            self._create_distance_matrix_from_neo4j()

    def _create_distance_matrix_from_csv(self):
        """
        从 CSV 文件中读取数据并构建距离矩阵和城市索引映射.
        """
        df = pd.read_csv(self.csv_file, encoding='utf-8')

        self.all_cities = pd.concat([df['出发景点'], df['目的景点']]).unique()
        self.city_to_index = {city: idx for idx, city in enumerate(self.all_cities)}

        num_cities = len(self.all_cities)
        self.distance_matrix = np.full((num_cities, num_cities), np.inf)

        for idx, row in df.iterrows():
            start = self.city_to_index[row['出发景点']]
            end = self.city_to_index[row['目的景点']]
            self.distance_matrix[start, end] = row['驾车距离（公里）']
            self.distance_matrix[end, start] = row['驾车距离（公里）']

        np.fill_diagonal(self.distance_matrix, 0)

    def _create_distance_matrix_from_neo4j(self):
        """
        从 Neo4j 数据库中读取数据并构建距离矩阵和城市索引映射.
        """
        graph = Graph(self.neo4j_uri, auth=(self.neo4j_user, self.neo4j_password))

        query = """  
        MATCH (a:ScenicSpot)-[r:LOCATED_IN]->(loc:Location)<-[r2:LOCATED_IN]-(b:ScenicSpot)  
        RETURN a.name AS start, b.name AS end, r2.distance AS distance  
        """

        results = graph.run(query)
        city_set = set()
        distances = []

        for record in results:
            start = record['start']
            end = record['end']
            distance = record['distance']
            city_set.add(start)
            city_set.add(end)
            distances.append((start, end, distance))

        all_cities = np.array(list(city_set))
        city_to_index = {city: idx for idx, city in enumerate(all_cities)}

        num_cities = len(all_cities)
        distance_matrix = np.full((num_cities, num_cities), np.inf)

        for start, end, distance in distances:
            start_idx = city_to_index[start]
            end_idx = city_to_index[end]
            distance_matrix[start_idx, end_idx] = distance
            distance_matrix[end_idx, start_idx] = distance

        np.fill_diagonal(distance_matrix, 0)

        return city_to_index, distance_matrix

    def get_city_to_index(self):
        print("City to Index:\n", self.city_to_index)
        return self.city_to_index

    def get_distance_matrix(self):
        return self.distance_matrix


class TSP:
    def __init__(self, distance_matrix, city_indices, city_scores, city_prices, starting_city_idx=0,
                 learning_rate=0.1, discount_factor=0.9, epsilon=1.0,
                 epsilon_decay=0.995, min_epsilon=0.01, alpha=0.9, beta=0.2):

        self.full_distance_matrix = distance_matrix
        self.city_indices = city_indices
        self.city_scores = city_scores  # 城市的景点评分
        self.city_prices = city_prices  # 城市的景点价格
        self.num_cities = len(city_indices)
        self.starting_city_idx = city_indices[starting_city_idx]
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon
        self.alpha = alpha  # 用于调节距离和景点评分的权重
        self.beta = beta  # 用于调节价格的权重

        # 创建子距离矩阵
        self.distance_matrix = distance_matrix[np.ix_(city_indices, city_indices)]
        self.q_table = np.zeros((self.num_cities, self.num_cities))
        self.best_path = []
        self.best_path_length = np.inf

    def choose_next_city(self, current_city, visited):
        available_cities = [i for i in range(self.num_cities) if i not in visited]

        if len(available_cities) == 0:  # 如果没有可选城市，则选择起始城市
            return visited[0]  # 回到起始城市

        if np.random.rand() < self.epsilon:  # Exploration
            return np.random.choice(available_cities)
        else:  # Exploitation
            return max(available_cities, key=lambda x: self.q_table[current_city][x])

    def update_q_table(self, current_city, next_city, reward):
        # Q-learning 更新规则
        best_next_action = np.max(self.q_table[next_city])  # 获取下一个城市的最大Q值
        self.q_table[current_city][next_city] += self.learning_rate * (
                reward + self.discount_factor * best_next_action - self.q_table[current_city][next_city]
        )

    def calculate_reward(self, current_city, next_city):
        # 奖励函数设计：结合距离、景点评分和价格
        distance_reward = -self.alpha * self.distance_matrix[current_city][next_city]  # 负距离奖励
        score_reward = (1 - self.alpha) * self.city_scores[next_city]  # 景点评分奖励
        price_penalty = self.beta * self.city_prices[next_city]  # 价格惩罚，价格越高惩罚越大
        return distance_reward + score_reward - price_penalty

    def train(self, num_episodes=1000):
        for episode in range(num_episodes):
            visited = []
            current_city = 0  # Start from the first city in the submatrix
            total_distance = 0

            while len(visited) < self.num_cities:
                next_city = self.choose_next_city(current_city, visited)
                visited.append(next_city)
                total_distance += self.distance_matrix[current_city][next_city]
                reward = self.calculate_reward(current_city, next_city)  # 使用新的奖励函数
                self.update_q_table(current_city, next_city, reward)
                current_city = next_city

            # 完成一个循环（返回起始城市）
            total_distance += self.distance_matrix[current_city][0]

            # 更新最优路径，确保路径不重复并且是回路
            if total_distance < self.best_path_length:
                self.best_path_length = total_distance
                self.best_path = [self.city_indices[i] for i in visited]

                # 确保路径形成回路，不重复添加起始城市
                if self.best_path[0] != self.best_path[-1]:
                    self.best_path.append(self.best_path[0])  # 添加起始城市，确保回路

            # Decay epsilon to reduce exploration over time
            self.epsilon = max(self.epsilon * self.epsilon_decay, self.min_epsilon)

        return self.best_path, self.best_path_length


def load_city_scores_and_prices_from_neo4j(neo4j_uri, username, password):
    """
    从 Neo4j 数据库加载城市评分和价格.

    :param neo4j_uri: Neo4j 数据库的 URI
    :param username: Neo4j 数据库的用户名
    :param password: Neo4j 数据库的密码
    :return: 一个元组 (city_scores, city_prices)
    """
    # 连接到 Neo4j 数据库
    graph = Graph(neo4j_uri, auth=(username, password))

    # 查询城市评分和价格
    query = """  
    MATCH (s:ScenicSpot)  
    RETURN s.rating AS rating, s.price AS price  
    """

    results = graph.run(query)

    city_scores = []
    city_prices = []

    for record in results:
        rating = record['rating']
        price = record['price']
        city_scores.append(rating)
        city_prices.append(price)

    return city_scores, city_prices
def load_city_scores_and_prices(csv_file):
    """
    从指定的 CSV 文件加载城市评分和价格.

    :param csv_file: CSV 文件的路径
    :return: 一个元组 (city_scores, city_prices)
    """
    df = pd.read_csv(csv_file, encoding='utf-8')  # 请根据需要替换编码

    city_scores = df['评分'].tolist()
    city_prices = df['价格'].tolist()
    # print("City Scores:", city_scores)
    # print("City Prices:", city_prices)

    return city_scores, city_prices

if __name__ == '__main__':
    dm = DistanceMatrix(csv_file='景点距离.csv')
    # 从Neo4j读取
    # dm = DistanceMatrix(
    #     neo4j_uri='bolt://localhost:7687',
    #     neo4j_user='neo4j',
    #     neo4j_password='password'
    # )
    city_index = dm.get_city_to_index()
    distance_matrix = dm.get_distance_matrix()
    all_cities=dm.all_cities
    # print("\nDistance Matrix:\n", distance_matrix)

    city_scores, city_prices = load_city_scores_and_prices('A级景区评分价格.csv')
    # 传入城市编号(city_index映射)
    city_indices = [9, 1, 3, 7]

    tsp_solver = TSP(distance_matrix, city_indices, city_scores, city_prices)

    best_path, best_length = tsp_solver.train()
    # print("Best Path:", best_path)
    print("Best Path Length:", best_length)


    # 映射为城市
    best_path_cities = [all_cities[idx] for idx in best_path]

    # 输出具体的城市路径
    print("Best Path:", best_path_cities)


