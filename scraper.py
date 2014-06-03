import json
import urllib

api_key = open(".freebase_api_key").read()
service_url = 'https://www.googleapis.com/freebase/v1/mqlread'
query = [{
  "type": "/type/namespace",
  "id": "/authority/nces/ipeds",
  "key": [{}],
  "keys": [{}]
}]
params = {
        'query': json.dumps(query),
        'key': api_key
}
url = service_url + '?query=' + params['query']  + '&cursor'
print url
response = json.loads(urllib.urlopen(url).read())
result = response['result']
for key in result[0]['keys']:
  print key
print len(result[0]['keys'])
print response