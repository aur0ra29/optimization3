import numpy as np

# Function to print the transportation table
def PrintTable(S, C, D):
    # Function to display the transportation table
    # S: Supply vector, C: Cost matrix, D: Demand vector
    num_s = len(S)
    num_d = len(D)
    
    # Printing column headers for destinations
    print(f"{'Sources/Destinations':<20}", end="")
    for j in range(num_d):
        print(f"{'Destination ' + str(j + 1):<15}", end="")
    print("Supply")

    # Print separator line
    print("-" * 50)

    # Print cost matrix and supply vector
    for i in range(num_s):
        print(f"{'Source ' + str(i + 1):<20}", end="")
        for j in range(num_d):
            print(f"{C[i][j]:<15}", end="")
        print(S[i])

    # Print separator line
    print("-" * 50)

    # Print demand vector
    print("Demand" + " " * 15, end="")
    for j in range(num_d):
        print(f"{D[j]:<15}", end="")
    print("\n")

# Function to find the cell in the matrix with the smallest value
def fi(matrix):
    # Find the cell with the smallest value in the matrix
    if not matrix or not matrix[0]:
        return None  # Empty matrix

    min_v = float('inf')
    min_c = None

    # Iterate through each element in the matrix
    ok = 0
    for i, row in enumerate(matrix):
        for j, value in enumerate(row):
            if (value < 0):
                ok = 1
            # Check if the current value is smaller than the current minimum
            if value < min_v:
                min_v = value
                min_c = (i, j)

    return min_c, ok

# Function implementing Russell's approximation method
def Russel(s_v, dem_v, cost_matrix):
    # Russell's approximation method for solving transportation problem
    col = [max(row) for row in cost_matrix]
    row = [max(column) for column in zip(*cost_matrix)]
    c_m = [[element for element in row] for row in cost_matrix]
    n = len(c_m)
    m = len(c_m[0])
    for i in range(n):
        for j in range(m):
            c_m[i][j] = c_m[i][j] - (row[j] + col[i])
    zero_matrix = [[0 for _ in range(m)] for _ in range(n)]
    ok = 1
    while (ok == 1):
        coord, ok = fi(c_m)
        if (ok == 0):
            break
        r = coord[0]
        c = coord[1]
        if (s_v[r] >= dem_v[c]):
            zero_matrix[r][c] = dem_v[c]
            s_v[r] = s_v[r] - dem_v[c]
            dem_v[c] = 0
            for i in range(n):
                c_m[i][c] = 1
        else:
            zero_matrix[r][c] = s_v[r]
            dem_v[c] = dem_v[c] - s_v[r]
            s_v[r] = 0
            for i in range(m):
                c_m[r][i] = 1

    print("using Russell's approximation method:")
    print_allocation(zero_matrix)

    s = 0
    for i in range(n):
        for j in range(m):
            s = s + zero_matrix[i][j] * cost_matrix[i][j]
    print("cost", s)

# Function to find the difference for Vogel's method
def findDiff(cost_matrix):
    rowDiff = []
    colDiff = []
    for i in range(len(cost_matrix)):
        arr = cost_matrix[i][:]
        arr.sort()
        rowDiff.append(arr[1] - arr[0])
    col = 0
    while col < len(cost_matrix[0]):
        arr = []
        for i in range(len(cost_matrix)):
            arr.append(cost_matrix[i][col])
        arr.sort()
        col += 1
        colDiff.append(arr[1] - arr[0])
    return rowDiff, colDiff

# Function implementing Vogel's approximation method
def vogel(supply, demand, cost_matrix):
    # Vogel's approximation method for solving transportation problem
    n = len(cost_matrix)
    m = len(cost_matrix[0])
    INF = 10 ** 3

    ans = 0
    num_rows = len(supply)
    num_cols = len(demand)
    allocations = [[0] * num_cols for _ in range(num_rows)]
    while max(supply) != 0 or max(demand) != 0:
        row, col = findDiff(cost_matrix)
        maxi1 = max(row)
        maxi2 = max(col)
        if (maxi1 >= maxi2):
            for ind, val in enumerate(row):
                if (val == maxi1):
                    mini1 = min(cost_matrix[ind])
                    for ind2, val2 in enumerate(cost_matrix[ind]):
                        if (val2 == mini1):
                            mini2 = min(supply[ind], demand[ind2])
                            ans += mini2 * mini1
                            allocations[ind][ind2] = mini2
                            supply[ind] -= mini2
                            demand[ind2] -= mini2
                            if (demand[ind2] == 0):
                                for r in range(n):
                                    cost_matrix[r][ind2] = INF
                            else:
                                cost_matrix[ind] = [INF for i in range(m)]
                            break
                    break
        else:
            for ind, val in enumerate(col):
                if (val == maxi2):
                    mini1 = INF
                    for j in range(n):
                        mini1 = min(mini1, cost_matrix[j][ind])

                    for ind2 in range(n):
                        val2 = cost_matrix[ind2][ind]
                        if val2 == mini1:
                            mini2 = min(supply[ind2], demand[ind])
                            ans += mini2 * mini1
                            allocations[ind2][ind] = mini2
                            supply[ind2] -= mini2
                            demand[ind] -= mini2
                            if (demand[ind] == 0):
                                for r in range(n):
                                    cost_matrix[r][ind] = INF
                            else:
                                cost_matrix[ind2] = [INF for i in range(m)]
                            break
                    break

    print("using Vogel's approximation method")
    print_allocation(allocations)
    print("cost:", ans)

# Function implementing the North-West corner method
def northWestCorner(cost_matrix, supply, demand):
    # North-West corner method for solving transportation problem
    num_suppliers = len(supply)
    num_consumers = len(demand)

    alloc = [[0 for _ in range(num_consumers)] for _ in range(num_suppliers)]

    i, j = 0, 0

    while i < num_suppliers and j < num_consumers:
        quant = min(supply[i], demand[j])

        alloc[i][j] = quant

        supply[i] -= quant
        demand[j] -= quant

        if supply[i] == 0:
            i += 1
        else:
            j += 1

    return alloc

# Function to print the allocations
def print_allocation(alloc):
    print("[")
    for row in alloc:
        print(row, "_")
    print("]")

# Main function
if __name__ == "__main__":
    # User inputs supply, cost matrix, and demand
    supply = [float(x) for x in input("Enter the vector of sources: ").split()]
    assert len(supply) == 3, "The length of the supply vector must be 3"
    assert all(x >= 0 for x in supply), "All elements in the supply vector must be greater than or equal to zero."

    print("Enter the cost matrix:")
    cost_matrix = [[float(x) for x in input().split()] for _ in range(3)]
    assert all(x > 0 for row in cost_matrix for x in row), "All elements in the cost matrix must be greater than zero."
    assert len(cost_matrix) == 3 and len(cost_matrix[0]) == 4, "The dimensions of the cost matrix must be 3x4"

    demand = [float(x) for x in input("Enter the vector of demand: ").split()]
    assert len(demand) == len(cost_matrix[0]), "The length of the demand vector must be 4"
    assert all(x >= 0 for x in demand), "All elements in the demand vector must be greater than or equal to zero."

    # Copying the inputs for different methods
    NORTHSUPLY = supply[:]
    VogelSupply = supply[:]
    RusellSupply = supply[:]
    NorthDemand = demand[:]
    vogelDemand = demand[:]
    demandR = demand[:]
    cost_matrixN = [row[:] for row in cost_matrix]
    cost_matrixV = [row[:] for row in cost_matrix]
    cost_matrixR = [row[:] for row in cost_matrix]

    # Printing the transportation table
    PrintTable(supply, cost_matrix, demand)
    print("The problem is unbalanced." if sum(supply) != sum(demand) else "The problem is balanced.")

    # North-West Corner method
    alloc = northWestCorner(cost_matrixN, NORTHSUPLY, NorthDemand)
    cost = 0

    print("Using North-West corner method")
    print_allocation(alloc)
    for i in range(len(alloc)):
        for j in range(len(alloc[0])):
            cost = cost + alloc[i][j] * cost_matrix[i][j]
    print("Cost:", cost)

    # Vogel's approximation method
    vogel(VogelSupply, vogelDemand, cost_matrixV)

    # Russell's approximation method
    Russel(RusellSupply, demandR, cost_matrixR)
