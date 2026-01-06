import requests
import parsel
import time
import csv
from bs4 import BeautifulSoup


with open('shanxiSpot.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    fieldnames = ['景区', '星级', '地区', '地址','评分', '价格', '简介','详情页']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()  # 写入表头

    for page in range(1, 50):  # 循环爬取 9 页
        print(f'===============================正在爬取第{page}页数据内容=======================================')

        time.sleep(3)  # 等待 3 秒，避免过于频繁请求
        url = f'https://piao.qunar.com/ticket/list.htm?keyword=%E5%B1%B1%E8%A5%BF&region=&from=mpl_search_suggest&page={page}&sort=pp'

        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Cookie':'QN1=0000f7802eb468e566b89f16; QN300=organic; qunar-assist={%22version%22:%2220211215173359.925%22%2C%22show%22:false%2C%22audio%22:false%2C%22speed%22:%22middle%22%2C%22zomm%22:1%2C%22cursor%22:false%2C%22pointer%22:false%2C%22bigtext%22:false%2C%22overead%22:false%2C%22readscreen%22:false%2C%22theme%22:%22default%22}; QN205=organic; QN277=organic; QN267=09748566322090643d; csrfToken=bKuyjM8royIZldkkjdbYyuSCoZmM42A2; _i=DFiEZbV3QsiD3dX6_9Y7zmIV_0Sw; _vi=Xk94HhXElO8HZRbaMpb8-pVWzA3vNTOzgDo3jRA0C-CL81kSzPiqct0YwTkVME67rutfl0AyOeCaCieyCnr7-5Y6DnzCV1ZHukSKrwf6aGoyNm6Esfaapkhdxr3c8rF4T8LuEz5yVucAeObb-s_wy8rJEYs36SBUuYHKKRMhSRR4; QN57=17347478632140.4910067965665088; QN58=1734747863213%7C1734747863213%7C1; QN269=B21804C0BF4211EFA99E1A7FB8942F97; JSESSIONID=A49CEA3DA44FDF8A406EFFDE6F98C330; fid=101a5b68-7ce6-43d1-a3e5-875318bc3f0e; QN271=98dc3526-8c87-4ef7-985c-ebd807dbfee7; __qt=v1%7CVTJGc2RHVmtYMTllRitUT25Ec3MvOHFwNFBOaVNpVlJscmRsUTE1dEZXc1FvWjFJRndCcDRBcnhYckJBQVBvZXVVR1FhNXlxZGgvbnpoU0N0NHRZU20wWFprbG5zMkJNZkFOaFo2Sm1KQXBodlY4ZXllUFpCa09vRHBjbTNSbW14bkdETGZLMXNPNW5JTWZpNVkydUY0RTVxN2VHWUt3UnZGMExkQkgzem9vPQ%3D%3D%7C1734747876689%7CVTJGc2RHVmtYMTlaWWRjVWxUUnRJeEZrTFJsWlVyalR5MjFsK2NCbmJzMCtIUnpkRjV2WGRwQ3lyRmVzUENjaDNaSEVySklRNUx4TnhTdnJXNHZtYkE9PQ%3D%3D%7CVTJGc2RHVmtYMS9ReE1icXg5T2V1ZXdGZFVURElEcmZack54WlE4SXcwZit2T0RsQjFSZmh0dFl3cnJsaTc5dWMxV0QzVVpSZmRhUWRILzNZbGF0YTY3L2pJV2JRYlBkakU3eUdmK042eTVORFJOVXN4ZXhDYmJ1NmpSUTMyRFVMdHlmbFRFOE1VMk1sV01xQkVYNGIxZU1BWEpUdE1lUkhkQkpGaW1OeEdiREQ4ZVpFTW5mWWhxUUxDTTBqcDd1Vk8wNHdkck9HK0tNVE0vUUtjZ1dtL2NUbHdVQUJ4cm0vQXdlaUxsR2hKVDhxbFhLeUZyckNzdCszT2M0bVduNm5pVXBaOUxRaDFHNGxDbXdFNndpZlR5RFc5elF0KzVsUk84ZUdBSDVxbjFicjVYbTdhYzZtczhDUy9JT1Z4WDdUblV1UXNJQVhWMWM0VGo0MGdka2twdmlBeEJrUm5FZFRCd0JJd2krL2RSc0oxS2pFdVRCeENncHUxSW4xczJ0ZWl2V1RuaHE3SGpxM3hhdXAzNFZMUWhRaG9rNDNEeHZscmFFN3NFVVdydUJVSGd2QjYwL2w4b3Z5TVNrT0ZZK2wvV2VKd2tDamlZT01mc2JEaWVoWXczNDZuNTcxUUUwdVh1dDNObWR4NHFGZXR2QkNxOURBWXBaY0x6TjZtNlB2allUT0UweVgzaGp1bGxacGJYYzhQS05SVE5hdC8vWTU2S084THNjZjhHWFVtbFRlZFo1Vk5TeDJiQWtIaDlpcTJVVW11T1N1SnkvZGJvcHMwcFFMSGZKNktDMnRmQjF6MWNjNG1OMTFxVkNqSjNHUmhTUmpaRUtSRjVBSURiT2taNDBOWmY3TFMwc3pxbDdBRVNPS0tNMjdjVUl4MU0rdm03akZuV21qMzdlVXVDQzhlYlNZTWxWdkZYSHk0K3RFeXJES29wMm10U3lYdlhyN3FodEQ1RXBSOWhBOUpmTGZ2d3ovcEorUkQrbXB3NDFaeHFhZEQvRGVVOUJNZTRa'

        }

        response = requests.get(url=url, headers=headers)
        selector = parsel.Selector(response.text)

        # 找到每个景点的元素
        lis = selector.css('#search-list .sight_item')

        for li in lis:
            title = li.css('.name::text').get()  # 景区
            print(title)
            level = li.css('.level::text').get()  # 星级
            area = li.css('.area a::text').get()  # 地区
            # hot = li.css('.product_star_level em::attr(title)').get().replace('热度: ', '')  # 热度
            # hot = int(float(hot) * 100)
            address = li.css('.address span::attr(title)').get()  # 地址
            print(address)
            price = li.css('.sight_item_price em::text').get()  # 价格
            # hot_num = li.css('.hot_num::text').get()  # 销量
            intro = li.css('.intro::text').get()  # 简介
            href = li.css('.name::attr(href)').get()  # 详情页
            href = 'https://piao.qunar.com' + href
            print(href)

            response = requests.get(href)

            if response.status_code == 200:
                # 步骤 3: 解析 HTML
                soup = BeautifulSoup(response.content, 'html.parser')

                # 提取 ID 为 mp-description-commentscore 的内容
                comments_score = soup.find(id='mp-description-commentscore')
                # comments_count=soup.find(cls='mp-descriptioncount')
                # print(comments_count)

                # a_tag = comments_count.find('a')  # 查找第一个 <a> 标签
                # comments_count = a_tag.text.strip()  # 链接文本

                # 确认是否找到该内容
                if comments_score:
                    rate=comments_score.text.strip()
                    # count=comments_count.text.strip()
                else:
                    rate='暂未评分'

            dit = {
                '景区': title,
                '星级': level,
                '地区': area,
                # '销量': hot_num,
                '地址': address,
                '评分': rate,
                # '评论量':count,

                '价格': price,
                '简介': intro,
                '详情页': href,
            }
            writer.writerow(dit)  # 写入每个景区的数据

