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

def fetch_text(url: str):
  try:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.35"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        soup.prettify()
        return soup.get_text()[:2000]
    else:
        msg = f"Get url failed with status code {response.status_code}.\nURL: {url}\nResponse: " \
              f"{response.text[:100]}"
        print(msg)
        return "No available content"
  except Exception as e:
      print("Get url failed with error: {}".format(e))
      return "No available content"
