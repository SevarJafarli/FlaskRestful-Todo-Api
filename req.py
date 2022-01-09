import requests
base = 'http://127.0.0.1:5050/'

data = [{"title": "First Task", "description": "This is first task"},
        {"title": "Second Task", "description": "This is second task"},
        {"title": "Third Task", "description": "This is third task"}
        ]

# for i in range(len(data)):

#     response = requests.post(
#         base + "tasks/" + str(i),  data[i])
#     print(response.json())


# response = requests.post(
#     base + "tasks/3", {"title": "It's third task", "description": "It's third task description", "isImportant": True})


# print(response.json())

# input()
# response = requests.get(base + "tasks/5")
# print(response.json())
# input()
# response = requests.delete(base + "tasks/0")
# print(response.json())


response = requests.get(base + "tasks")
print(response.json())
