import pandas as pd
from py2neo import Graph, Node, Relationship

# 连接到 Neo4j 数据库
graph = Graph("bolt://localhost:7687", auth=("neo4j", "123456"))

# 读取 CSV 文件
data = pd.read_csv("shanxiSpot.csv")

# 批量创建节点和关系
for index, row in data.iterrows():
    # 创建景区节点
    scenic_spot = Node("ScenicSpot",
                       name=row["景区"],
                       star_level=row["星级"],
                       rating=row["评分"],
                       price=row["价格"],
                       description=row["简介"])

    # 从地区字段中提取地点 ID（例如：晋中）
    location_id = row["地区"].split('·')[1]  # 假设地区的格式是 "山西·晋中"
    location_name = row["地区"]
    address = row["地址"]

    # 查询是否已存在该地点节点
    existing_location = graph.nodes.match("Location", name=location_id).first()

    if existing_location is None:
        # 如果不存在，创建地点节点
        location = Node("Location",
                        name=location_id,
                        address=location_name,
                        loc_detail=address)
        graph.create(location)
    else:
        # 如果存在，使用已有的节点
        location = existing_location

        # 将景区节点插入到图数据库
    graph.create(scenic_spot)

    # 创建 LOCATED_IN 关系
    located_in_relationship = Relationship(scenic_spot, "LOCATED_IN", location)
    graph.create(located_in_relationship)

print("所有景区和地点节点已成功插入到 Neo4j 图数据库中，并建立 LOCATED_IN 关系。")