import requests

response = requests.get('https://httpbin.org/get')
print(response.headers)
print(response.status_code)
print(response.text)

response = requests.post(
    'https://httpbin.org/post?kota=bdg&cabang=dakota',
    headers={
        'X-Organization': 'BRM',
        'Authorization': 'Bearer 28u9jf83hfj98shfshf7'
    },
    data={
        'name':'ini adalah nama saya',
        'umur':30
        },
    timeout=5
    )
# print(response.headers)
# print(response.status_code)
print(response.text)
