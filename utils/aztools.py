import requests, json

def get_fix_id(service, key):
    """Get fix id of latest document and append it by one for new document"""
    url = f"https://{service}.search.windows.net/indexes/technician-troubleshooting/docs?api-version=2023-11-01&$select=FixID&$orderby=DocumentLastUpdate desc&$top=1"
    headers = {
        "Content-Type": "application/json",
        "api-key": key
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    latest_id = data.get("value")[0].get("FixID")
    prefix = latest_id[:-4]
    number = int(latest_id[-4:]) + 1
    new_id = f"{prefix}{number:04d}"
    return new_id

def submit_document_to_backend(payload, service, key):
    """Send document to backend"""
    url = f"https://{service}.search.windows.net/indexes/technician-troubleshooting/docs/index?api-version=2023-11-01"
    headers = {
        "Content-Type": "application/json",
        "api-key": key
    }
    temp = {"@search.action": "upload"}
    temp.update(payload)
    data = {
        "value": [temp]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()