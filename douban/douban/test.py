import requests

url = "https://movie.douban.com/subject/26985127/comments"
headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}
response = requests.get(url, headers = headers)
print(response.status_code)