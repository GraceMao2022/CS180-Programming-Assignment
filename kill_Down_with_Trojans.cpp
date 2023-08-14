#include <iostream>
#include <fstream>
#include <vector>
#include <cstring> // For strlen

constexpr int MAX_N = 100;

struct Tile
{
    int t;
    int v;
};

void load_input_file(const std::string &file_name, int &n, int &H, std::vector<std::vector<Tile>> &tiles)
{
    std::ifstream file(file_name);
    file >> n >> H;

    // Initialize the grid
    tiles.resize(n, std::vector<Tile>(n));

    for (int i = 0; i < n * n; i++)
    {
        if (i == 0)
        {
            continue; // The initial tile is zero type with zero value
        }
        Tile tile;
        int x, y;
        file >> x >> y >> tile.t >> tile.v;
        tiles[x][y] = tile;
    }

    file.close();
}

void print_tile_data(int n, const std::vector<std::vector<Tile>> &tiles)
{
    std::cout << "Tile Types:\n";
    for (int x = 0; x < n; x++)
    {
        for (int y = 0; y < n; y++)
        {
            std::cout << "[" << tiles[x][y].t << "] ";
        }
        std::cout << '\n';
    }

    std::cout << "\nTile Values:\n";
    for (int x = 0; x < n; x++)
    {
        for (int y = 0; y < n; y++)
        {
            std::cout << "[" << tiles[x][y].v << "] ";
        }
        std::cout << '\n';
    }
}
void printMemo(const std::vector<std::vector<std::vector<std::vector<int>>>> &memo)
{
    for (int i = 0; i < memo.size(); ++i)
    {
        for (int j = 0; j < memo[i].size(); ++j)
        {
            for (int p = 0; p < memo[i][j].size(); ++p)
            {
                for (int m = 0; m < memo[i][j][p].size(); ++m)
                {
                    std::cout << "memo[" << i << "][" << j << "][" << p << "][" << m << "] = " << memo[i][j][p][m] << " ";
                }
                std::cout << std::endl;
            }
            std::cout << std::endl;
        }
        std::cout << std::endl;
    }
}
int helperFunction(int i, int j, int n, bool p, bool m, const std::vector<std::vector<Tile>> &tiles, std::vector<std::vector<std::vector<std::vector<int>>>> &memo)
{

    // Out of bounds
    if (i < 0 || j < 0 || i >= n || j >= n)
    {
        return INT_MAX;
    }

    // If this state is already calculated
    if (memo[i][j][p][m] != -1)
    {
        return memo[i][j][p][m];
    }

    // Base Case: if you've reached the end
    if (i == n - 1 && j == n - 1)
    {
        if (tiles[i][j].t == 0)
        {
            return memo[i][j][p][m] = (p ? 0 : tiles[i][j].v);
        }
        return 0;
    }

    int cost = INT_MAX;

    switch (tiles[i][j].t)
    {
    case 0:
        if (p)
        {
            int useTokenNow = std::min(
                helperFunction(i + 1, j, n, false, m, tiles, memo),
                helperFunction(i, j + 1, n, false, m, tiles, memo));

            // Save the p token for future and take the damage for the current tile
            int saveToken = tiles[i][j].v + std::min(
                                                helperFunction(i + 1, j, n, p, m, tiles, memo),
                                                helperFunction(i, j + 1, n, p, m, tiles, memo));

            cost = std::min(useTokenNow, saveToken);
        }
        else
        {
            cost = tiles[i][j].v + std::min(
                                       helperFunction(i + 1, j, n, p, m, tiles, memo),
                                       helperFunction(i, j + 1, n, p, m, tiles, memo));
        }
        break;

    case 1:
        if (m)
        {
            int useTokenNow = std::min(
                                  helperFunction(i + 1, j, n, p, false, tiles, memo),
                                  helperFunction(i, j + 1, n, p, false, tiles, memo)) -
                              2 * tiles[i][j].v;

            // Save the p token for future and take the damage for the current tile
            int saveToken = std::min(
                                helperFunction(i + 1, j, n, p, m, tiles, memo),
                                helperFunction(i, j + 1, n, p, m, tiles, memo)) -
                            tiles[i][j].v;

            cost = std::min(useTokenNow, saveToken);
        }
        else
        {
            cost = std::min(
                       helperFunction(i + 1, j, n, p, m, tiles, memo),
                       helperFunction(i, j + 1, n, p, m, tiles, memo)) -
                   tiles[i][j].v;
        }
        break;

    case 2:
        cost = std::min(
            helperFunction(i + 1, j, n, true, m, tiles, memo),
            helperFunction(i, j + 1, n, true, m, tiles, memo));
        break;

    case 3:
        cost = std::min(
            helperFunction(i + 1, j, n, p, true, tiles, memo),
            helperFunction(i, j + 1, n, p, true, tiles, memo));
        break;
    }

    cost = std::max(cost, 0);

    return memo[i][j][p][m] = cost;
}
bool DP(int n, int H, const std::vector<std::vector<Tile>> &tiles)
{
    std::vector<std::vector<std::vector<std::vector<int>>>> memo(n, std::vector<std::vector<std::vector<int>>>(n, std::vector<std::vector<int>>(2, std::vector<int>(2, -1))));
    int result = helperFunction(0, 0, n, 0, 0, tiles, memo);
    std::cout << "answer: " << result << '\n';
    // printMemo(memo);
    return (H - result) >= 0;
}

void write_output_file(const std::string &output_file_name, bool result)
{
    std::ofstream file(output_file_name);
    file << result;
    file.close();
}

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        std::cout << "Usage: " << argv[0] << " a_file_name.txt\n";
        return 1;
    }

    int n, H;
    std::vector<std::vector<Tile>> tiles;
    load_input_file(argv[1], n, H, tiles);
    print_tile_data(n, tiles);
    bool result = DP(n, H, tiles);
    std::cout << "Result: " << result << '\n';

    // Construct the output file name
    std::string output_file_name(argv[1]);
    output_file_name.insert(output_file_name.find_last_of('.'), "_out");
    std::ofstream outfile(output_file_name);
    outfile << result;
    outfile.close();

    return 0;
}
