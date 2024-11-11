import requests

def get_game_data():
    response = requests.get("https://jobfair.nordeus.com/jf24-fullstack-challenge/test")

    # Assuming `data` is your bytes object
    data_str = response.content.decode('utf-8')

    # Convert the decoded string into a list of lists of integers
    matrix = [list(map(int, line.split())) for line in data_str.strip().split('\n')]

    return matrix

def dfs_island(game_data, i, j, visited, height_sum, iteration):
    # Base case: out of bounds or already visited or zero value cell
    if i < 0 or i >= len(game_data) or j < 0 or j >= len(game_data[0]) or visited[i][j] == 1 or game_data[i][j] == 0:
        return

    # Mark the cell as visited
    visited[i][j] = 1

    # Update height_sum and iteration for this island
    height_sum[0] += game_data[i][j]
    iteration[0] += 1

    # Recursive DFS in all four directions
    dfs_island(game_data, i, j + 1, visited, height_sum, iteration)  # Right
    dfs_island(game_data, i, j - 1, visited, height_sum, iteration)  # Left
    dfs_island(game_data, i + 1, j, visited, height_sum, iteration)  # Down
    dfs_island(game_data, i - 1, j, visited, height_sum, iteration)  # Up


def find_max_island_height(game_data):
    # Initialize the visited matrix with the same size as game_data
    visited = [[0 for _ in range(len(game_data[0]))] for _ in range(len(game_data))]

    max_height = 0  # Variable to track the maximum "height" (sum/iterations)

    # Loop through each cell in the matrix
    for i in range(len(game_data)):
        for j in range(len(game_data[0])):
            # Start DFS only on unvisited, non-zero cells (new island)
            if game_data[i][j] != 0 and visited[i][j] == 0:
                # Initialize height_sum and iteration for this island
                height_sum = [0]
                iteration = [0]

                # Perform DFS on this cell to explore the entire island
                dfs_island(game_data, i, j, visited, height_sum, iteration)

                # Calculate the height metric (sum/iterations)
                current_height = height_sum[0] / iteration[0] if iteration[0] > 0 else 0

                # Update max_height if the current island has a higher value
                if current_height > max_height:
                    max_height = current_height

    # After visiting all cells, return the maximum height found
    return round(max_height, 2)


