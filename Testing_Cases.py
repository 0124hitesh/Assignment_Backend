import requests
from requests.auth import HTTPBasicAuth

BASE = "http://127.0.0.1:5000/"

data = [{"name" : "abc", "email" : "abcc@gmail.com","phone" : 1236547890},
        {"name" : "xyz", "email" : "xyzz@gmail.com","phone" : 7896540213},
        {"name" : "pqr", "email" : "pqrr@gmail.com","phone" : 5467890132},
        ]

username = "hitesh"
password = "hitesh_xyz"

#PUT request
print("Request with No_authentication/No_credentials")
response = requests.put(BASE + "/contact/",data = data[0])
print(response.json())

print("\n")
print("Request with wrong credentials")
response = requests.put(BASE + "/contact/",data = data[0],auth = HTTPBasicAuth("hiteshhh", password))
print(response.json())

print("\n")
print("PUT request - ADD ALL CONTACTS")
for i in range(len(data)):
    response = requests.put(BASE + "/contact/",data = data[i],auth = HTTPBasicAuth(username, password))
    print(response.json())
print("\n")



#GET Request
print("\n")
print("GET request with only Email in params")
res = requests.get(BASE + "/contact/?email=" + data[0]['email'],auth = HTTPBasicAuth(username, password))
print(res.json())

print("\n")
print("GET request with only name in params")
res = requests.get(BASE + "/contact/?name=" + data[0]['name'],auth = HTTPBasicAuth(username, password))
print(res.json())

print("\n")
print("GET request with both name and email in params")
res = requests.get(BASE + "/contact/?email=" + data[0]['email'] +"&name=" + data[0]['name'],auth = HTTPBasicAuth(username, password))
print(res.json())



#Update/Patch Request
print("\n")
print("UPDATE")
response = requests.patch(BASE + "/contact/" + "abcc@gmail.com",{"name" : "ABC_Updated"},auth = HTTPBasicAuth(username, password))
print(response.json())



#Delete Request
print("\n")
print("DELETE")
response = requests.delete(BASE + "/contact/pqr@gmail.com",auth = HTTPBasicAuth(username, password))
print(response.json())

# print("Result after all CRUD operations")
# res = requests.get(BASE + "/contact/?email=" + "jai@gmail.com",auth = HTTPBasicAuth(username, password))
# print(res.json())