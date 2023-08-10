import numpy as np
import scipy
import sys

#np.set_printoptions(threshold=sys.maxsize)


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
    #if player initially has neg health, return False
    if H < 0:
        return False
    memo = np.full((n, n, 2, 2), np.nan)
    result = DP_helper(n, H, tile_types, tile_values, 0, 0, 0, 0, memo)
    if result > H or np.isnan(memo[0][0][0][0]):
        return False
    
    return True

def DP_helper(n, H, tile_types, tile_values, i, j, prev_protect, prev_mult, memo):
    # base cases
    # if reached bottom right corner, return 0
    if (i == n and j == n-1) or (i == n-1 and j == n):
        return 0
    # if out of bounds
    if i == n or j == n:
        return np.inf
    #check memo
    if not np.isnan(memo[i][j][prev_protect][prev_mult]):
        return memo[i][j][prev_protect][prev_mult]
    
    res1 = np.inf
    res2 = np.inf
    res3 = np.inf
    res4 = np.inf

    #if landed on protection square
    if tile_types[i][j] == 2:
        #protect_status = True
        #test going right
        res1 = DP_helper(n, H, tile_types, tile_values, i, j+1, 1, prev_mult, memo)
        #test going down
        res2 = DP_helper(n, H, tile_types, tile_values, i+1, j, 1, prev_mult, memo)
    #if landed on multiplier square
    elif tile_types[i][j] == 3:
        #test going right
        res1 = DP_helper(n, H, tile_types, tile_values, i, j+1, prev_protect, 1, memo)
        #test going down
        res2 = DP_helper(n, H, tile_types, tile_values, i+1, j, prev_protect, 1, memo)
     #if landed on damage tile
    elif tile_types[i][j] == 0:
        #if protected
        if prev_protect:
            #test going right and protect on current tile
            res1 = DP_helper(n, H, tile_types, tile_values, i, j+1, 0, prev_mult, memo)
            #test going down and protect on current tile
            res2 = DP_helper(n, H, tile_types, tile_values, i+1, j, 0, prev_mult, memo)
            #test going right and dont use protect
            res3 = DP_helper(n, H - tile_values[i][j], tile_types, tile_values, i, j+1, prev_protect, prev_mult, memo) + tile_values[i][j]
            #test going down and dont use protect
            res4 = DP_helper(n, H - tile_values[i][j], tile_types, tile_values, i+1, j, prev_protect, prev_mult, memo) + tile_values[i][j]
        else:
            #test going right and not protecting
            res3 = DP_helper(n, H - tile_values[i][j], tile_types, tile_values, i, j+1, prev_protect, prev_mult, memo) + tile_values[i][j]
            #test going down and not protecting
            res4 = DP_helper(n, H - tile_values[i][j], tile_types, tile_values, i+1, j, prev_protect, prev_mult, memo) + tile_values[i][j]
    #if landed on healing tile
    elif tile_types[i][j] == 1:
        #if have multiplier token
        if prev_mult:
            #test going right and multiplier on current tile
            res1 = DP_helper(n, H + tile_values[i][j]*2, tile_types, tile_values, i, j+1, prev_protect, 0, memo) - tile_values[i][j]*2
            #test going down and multiplier on current tile
            res2 = DP_helper(n, H + tile_values[i][j]*2, tile_types, tile_values, i+1, j, prev_protect, 0, memo) - tile_values[i][j]*2
            #test going right and dont use multiplier
            res3 = DP_helper(n, H + tile_values[i][j], tile_types, tile_values, i, j+1, prev_protect, prev_mult, memo) - tile_values[i][j]
            #test going down and dont use multiplier
            res4 = DP_helper(n, H + tile_values[i][j], tile_types, tile_values, i+1, j, prev_protect, prev_mult, memo) - tile_values[i][j]        
        else:
            #test going right and not use multiplier
            res3 = DP_helper(n, H + tile_values[i][j], tile_types, tile_values, i, j+1, prev_protect, prev_mult, memo) - tile_values[i][j]
            #test going down and not use multiplier
            res4 = DP_helper(n, H + tile_values[i][j], tile_types, tile_values, i+1, j, prev_protect, prev_mult, memo) - tile_values[i][j]

    memo[i][j][prev_protect][prev_mult] = max(min(res1,res2,res3,res4),0)
    return memo[i][j][prev_protect][prev_mult]
    


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
