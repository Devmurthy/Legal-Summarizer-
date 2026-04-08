import requests

url = "http://localhost:5001/api/summarize"
files = {'document': ('test.txt', 'This is a test legal document. It has a few sentences.')}
data = {'ext_num': 5, 'abs_min': 40, 'abs_max': 150, 'ocr_mode': 'Default'}

try:
    response = requests.post(url, files=files, data=data)
    print("STATUS", response.status_code)
    try:
        print("JSON", response.json())
    except:
        print("TEXT", response.text)
except Exception as e:
    print(e)
