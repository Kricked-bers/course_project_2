import requests
import datetime

date = datetime.datetime.now()
print(date.date())
day = "-".join([str(date.date().year), str(date.date().month), '0'+str(date.date().day-1)])
url =
r = requests.get(url)
data = r.json()

print(data)