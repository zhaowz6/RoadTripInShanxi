from django.http import JsonResponse

from .Enum import spot_mapping
from .utils import DistanceMatrix, TSP, load_city_scores_and_prices  # 导入新建的映射函数
from django.views.decorators.csrf import csrf_exempt
from urllib.parse import urlparse, parse_qs

@csrf_exempt  # 如果你不使用 CSRF 保护，这个装饰器可以禁用 CSRF 检查
def solve_tsp(request):
    # 处理 GET 请求
    url = request.build_absolute_uri()  # 返回请求的完整 URL，包括协议、域名和路径
    parsed_url = urlparse(url)  # 解析 URL

    # 获取查询字符串参数（返回字典形式）
    query_params = parse_qs(parsed_url.query)

    # 访问参数，parse_qs 返回的是一个字典，值为列表
    strategy = query_params.get('strategy', [None])[0]
    start_end_point = query_params.get('start_end_point', [None])[0]
    pass_points = query_params.get('pass_points', [None])[0]

    # 打印调试
    print(f"Strategy: {strategy}")
    print(f"Start-End Point: {start_end_point}")
    print(f"Pass Points: {pass_points}")

    # 假设 pass_points 是一个逗号分隔的字符串
    pass_points_list = pass_points.split(',')

    # 获取景点名称到索引的映射
    csv_file = 'shanxi5ASpot.csv'
    pass_points_indices = []
    start_index=[spot_mapping[start_end_point]]
    for point in pass_points_list:
        point = point.strip()  # 去除空格
        index = spot_mapping[point]
        pass_points_indices.append(index)

       # 打印结果
    print(f"Pass Points Indices: {pass_points_indices}")

    # 获取 CSV 文件的路径或 Neo4j URI等参数
    csv_file = 'spotdis.csv'
    csv_file2='shanxi5ASpot.csv'
    # 创建 DistanceMatrix 对象
    dm = DistanceMatrix(csv_file=csv_file)

    # 获取城市的索引和距离矩阵
    way_points=start_index+pass_points_indices
    distance_matrix = dm.get_distance_matrix()
    all_cities = dm.all_cities

    city_scores, city_prices=load_city_scores_and_prices(csv_file2)
    # 创建 TSP 求解器
    tsp_solver = TSP(distance_matrix, way_points, city_scores, city_prices)

    # 训练模型
    best_path, best_length = tsp_solver.train()

    # 映射回城市名
    best_path_cities = [all_cities[idx] for idx in best_path]

    print(best_path_cities)
    return JsonResponse({
        'best_path': best_path_cities,
        'best_length': best_length
    })
