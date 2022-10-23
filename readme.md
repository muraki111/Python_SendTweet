# LINE Bot QR code

## 変更箇所
### docker-compose
```yml
container_name: 'python3-xxxx'
```

### settings.toml
```toml
[LINE]
apiURL = ''
channel_access_token = ''

[Twitter]
CONSUMER_KEY = ''
CONSUMER_SECRET = ''

ACCESS_TOKEN = ''
ACCESS_SECRET = ''

UserID = ['abcid', 'defid', 'ghgid']
```