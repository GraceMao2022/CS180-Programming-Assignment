import numpy as np
import scipy


def load_input_file(file_name):
    with open(file_name, 'r') as file:
        n, H = map(int, file.readline().split())
        tile_types = np.zeros((n, n), dtype=int)
        tile_values = np.zeros((n, n), dtype=int)

        for i in range(n * n):
            if i == 0:
                continue  # the initial tile is zero type with zero value
            x, y, t, v = map(int, file.readline().split())
            tile_types[x][y] = t
            tile_values[x][y] = v

    return n, H, tile_types, tile_values


def print_tile_data(tile_types, tile_values):
    print("Tile Types:")
    print(tile_types)
    print("\nTile Values:")
    print(tile_values)


def DP(n, H, tile_types, tile_values):
    memo = np.full((n, n, 3), -1)
    return DP_helper(n, H, tile_types, tile_values, 0, 0, False, False, memo)


def DP_helper(n, H, tile_types, tile_values, i, j, prev_protect, prev_mult, memo):
    # base cases
    # if health goes below 0, invalid path
    if H < 0:
        return False
    # if reached bottom right corner without dying, return true
    if (i == n and j == n-1) or (i == n-1 and j == n):
        return True
    # if out of bounds
    if i == n or j == n:
        return False
    #check memo
    
    new_health = H
    protect_status = prev_protect
    mult_status = prev_mult

    #if landed on damage tile
    if tile_types[i][j] == 0:
        #if protected
        if prev_protect:
            protect_status = False
        else:
            new_health -= tile_values[i][j]
    #if landed on healing tile
    elif tile_types[i][j] == 1:
        #if have multiplier token
        if prev_mult:
            new_health += tile_values[i][j]*2
            mult_status = False
        else:
            new_health += tile_values[i][j]
    #if landed on protection square
    elif tile_types[i][j] == 2:
        protect_status = True
    #if landed on multiplier square
    elif tile_types[i][j] == 3:
        mult_status = True

    print(str(i) + ", " + str(j) + ": Health: " + str(new_health) + " Protect status: " + str(protect_status) + " mult status: " + str(mult_status))
    #test going right
    res1 = DP_helper(n, new_health, tile_types, tile_values, i, j+1, protect_status, mult_status)
    #test going down
    res2 = DP_helper(n, new_health, tile_types, tile_values, i+1, j, protect_status, mult_status)

    return res1 or res2

    


def write_output_file(output_file_name, result):
    with open(output_file_name, 'w') as file:
        file.write(str(int(result)))


def main(input_file_name):
    n, H, tile_types, tile_values = load_input_file(input_file_name)
    print_tile_data(tile_types, tile_values)
    result = DP(n, H, tile_types, tile_values)
    print("Result: " + str(result))
    output_file_name = input_file_name.replace(".txt", "_out.txt")
    write_output_file(output_file_name, result)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python kill_Down_with_Trojans.py a_file_name.txt")
    else:
        main(sys.argv[1])
