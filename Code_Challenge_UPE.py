import requests, json

# Get access token
base = "http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/"
access = base + "session"
header = {'content-type': 'application/x-www-form-urlencoded'}
UID = {'uid': '304990072'}
r = requests.post(access, UID, header)
ACCESS_TOKEN = json.loads(r.text)["token"]
detail = base + "game?token=" + ACCESS_TOKEN


# maze size
def get_maze_size():
    r = requests.get(detail, header)
    return json.loads(r.text)["maze_size"]

# status
def get_status():
    r = requests.get(detail, header)
    return json.loads(r.text)["status"]

# current location
def get_current_location():
    r = requests.get(detail, header)
    return json.loads(r.text)["current_location"]

# level completed
def get_level_completed():
    r = requests.get(detail, header)
    return json.loads(r.text)["levels_completed"]

# total level
def get_total_level():
    r = requests.get(detail, header)
    return json.loads(r.text)["total_levels"]

# move
def move(dir):
    action = {'action': dir}
    r = requests.post(detail, action, header)
    return json.loads(r.text)["result"]



# actual algorithm
def find_path(current):
	x = current[0]
	y = current[1]
	print(get_current_location())
	if visited[x][y] == 1:
		return False
	visited[x][y] = 1
	if y-1 >= 0 and visited[x][y-1] == 0:
		result = move("UP")
		if result == "END":
			return True
		if result == "OUT_OF_BOUNDS" or result == "WALL":
			visited[x][y-1] = 1
		if result == "SUCCESS":
			if find_path((x,y-1)):
				return True
			else:
				move("DOWN")

	if y+1 < maze_size[1] and visited[x][y+1] == 0:
		result = move("DOWN")
		if result == "END":
			return True
		if result == "OUT_OF_BOUNDS" or result == "WALL":
			visited[x][y+1] = 1
		if result == "SUCCESS":
			if find_path((x,y+1)):
				return True
			else:
				move("UP")

	if x-1 >= 0 and visited[x-1][y] == 0:
		result = move("LEFT")
		if result == "END":
			return True
		if result == "OUT_OF_BOUNDS" or result == "WALL":
			visited[x-1][y] = 1
		if result == "SUCCESS":
			if find_path((x-1,y)):
				return True
			else:
				move("RIGHT")

	if x+1 < maze_size[0] and visited[x+1][y] == 0:
		result = move("RIGHT")
		if result == "END":
			return True
		if result == "OUT_OF_BOUNDS" or result == "WALL":
			visited[x+1][y] = 1
		if result == "SUCCESS":
			if find_path((x+1,y)):
				return True
			else:
				move("LEFT")

	return False

# call of the functions

status = get_status()
print(status)
print(get_total_level())

while status != "FINISHED":
	maze_size = get_maze_size();
	print(get_level_completed())
	visited = [[0 for i in range(maze_size[1])] for j in range(maze_size[0])]
	#print("Hi")
	find_path(get_current_location())
	status = get_status()
	print(status)
	if status == "GAME_OVER" or status == "NONE":
		msg = "QAQ"
		print(msg)
		break
print("success!!!")

		
    



