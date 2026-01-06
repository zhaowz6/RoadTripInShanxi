import pandas as pd
from py2neo import Graph, Node, Relationship

# 连接到 Neo4j 数据库
graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))

# 读取距离 CSV 文件
distances_data = pd.read_csv(r"./spotdis.csv",encoding='utf-8')

# 批量创建距离关系
for index, row in distances_data.iterrows():
    start_spot_name = row["出发景点"]
    end_spot_name = row["目的景点"]
    distance = row["驾车距离（公里）"]

    # 查找起始和目的地景点节点
    start_spot = graph.nodes.match("ScenicSpot", name=start_spot_name).first()
    end_spot = graph.nodes.match("ScenicSpot", name=end_spot_name).first()

    if start_spot is not None and end_spot is not None:
        # 创建距离关系
        distance_relationship = Relationship(start_spot, "DISTANCE_TO", end_spot, distance=distance)
        graph.create(distance_relationship)
    else:
        print(f"未找到景点: {start_spot_name} 或 {end_spot_name}")

print("所有距离关系已成功插入到 Neo4j 图数据库中。")