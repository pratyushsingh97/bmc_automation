import requests

headers = {
    'Authorization': 'Bearer eyJraWQiOiIyMDE5MDcyNCIsImFsZyI6IlJTMjU2In0.eyJpYW1faWQiOiJJQk1pZC01NTAwMDNZME4yIiwiaWQiOiJJQk1pZC01NTAwMDNZME4yIiwicmVhbG1pZCI6IklCTWlkIiwiaWRlbnRpZmllciI6IjU1MDAwM1kwTjIiLCJnaXZlbl9uYW1lIjoiUHJhdHl1c2giLCJmYW1pbHlfbmFtZSI6IlNpbmdoIiwibmFtZSI6IlByYXR5dXNoIFNpbmdoIiwiZW1haWwiOiJwcmF0eXVzaHNpbmdoQGlibS5jb20iLCJzdWIiOiJwcmF0eXVzaHNpbmdoQGlibS5jb20iLCJhY2NvdW50Ijp7InZhbGlkIjp0cnVlLCJic3MiOiIwNGZkYzYwYTdjMGM0MDRmNTBmZDM0YWFjNzlhZjQ1ZSJ9LCJpYXQiOjE1NzQ4NDE3MDAsImV4cCI6MTU3NDg0NTMwMCwiaXNzIjoiaHR0cHM6Ly9pYW0uY2xvdWQuaWJtLmNvbS9pZGVudGl0eSIsImdyYW50X3R5cGUiOiJ1cm46aWJtOnBhcmFtczpvYXV0aDpncmFudC10eXBlOnBhc3Njb2RlIiwic2NvcGUiOiJpYm0gb3BlbmlkIiwiY2xpZW50X2lkIjoiYngiLCJhY3IiOjEsImFtciI6WyJwd2QiXX0.Cv7iYSmaJ663GCrBqJiiw--wDarYJXwVuftidp2RZykOJw60BEKaHmG5egyr0SZnZBv7ccdzT_7iGxYuotL9ghz2SAc3T5B55peLWbXUCzIdPBF8IYmZlVACNIAxUV4GRUHH90rnRwF79UyFpVKKSRcxjOq2pox02--rTkzMEZDEufpzPcWSpxOvJTRi7ooNl0IH8KGbQBDq6s4-kKBEcKRSXAztg-XdLzHNuUaFke9hS6EqnwVKKRJMtpTkOgYOnG81t2TdNl_sLw2QLUbznbJot9XMCGdKaBY9sSA3jRLZnKejWAMHVxF2RpNT73dDf2rf96xxs9YVlJpFyIj93g',
    'Content-Type': 'application/json',
}

params = (
    ('account_id', '04fdc60a7c0c404f50fd34aac79af45e'),
)

data = '{\n  "name": "Awesome Developers696",\n  "description": "Group for awesome developers"\n}'

response = requests.post('https://iam.cloud.ibm.com/v2/groups', headers=headers, params=params, data=data)
