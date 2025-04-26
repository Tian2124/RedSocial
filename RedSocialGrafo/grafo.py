from collections import deque

class Graph:
    def __init__(self):
        self.adj_list = {}

    def add_user(self, user):
        if user not in self.adj_list:
            self.adj_list[user] = []

    def add_friendship(self, user1, user2):
        self.add_user(user1)
        self.add_user(user2)
        if user2 not in self.adj_list[user1]:
            self.adj_list[user1].append(user2)
        if user1 not in self.adj_list[user2]:
            self.adj_list[user2].append(user1)

    def get_friends(self, user):
        return self.adj_list.get(user, [])

    def suggest_friends_bfs(self, user):
        visited = set()
        queue = deque([(user, 0)])
        suggestions = []

        while queue:
            current, level = queue.popleft()
            if level > 2:
                break
            visited.add(current)
            for neighbor in self.adj_list.get(current, []):
                if neighbor not in visited:
                    queue.append((neighbor, level + 1))
                    if level == 1 and neighbor != user and neighbor not in self.adj_list[user]:
                        suggestions.append(neighbor)

        return list(set(suggestions))
