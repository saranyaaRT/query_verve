import jwt
import datetime

METABASE_SECRET_KEY = "starship"
payload = {
    "resource": {"question": 25224},  # or "question": 123
    "params": {"filter_key": "value"},  # Dynamic filtering
    "exp": datetime.datetime.now() + datetime.timedelta(hours=3),
}
token = jwt.encode(payload, METABASE_SECRET_KEY, algorithm="HS256")
iframe_url = f"https://starship.nobroker.in/embed/dashboard/{token}#bordered=true"
print(iframe_url)

import jwt
import datetime

METABASE_SECRET_KEY = "starship"
payload = {
    "resource": {"question": 25224},  # or "question": 123
    "params": {"filter_key": "value"},  # Dynamic filtering
    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=3),
}
token = jwt.encode(payload, METABASE_SECRET_KEY, algorithm="HS256")
iframe_url = f"https://starship.nobroker.in/embed/dashboard/{token}#bordered=true"
print(iframe_url)
