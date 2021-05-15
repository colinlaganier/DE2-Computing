# ####################################################
# DE2-COM2 Computing 2
# Individual project - TETRILING WITH MISSING PIECES
#
# Title: MAIN
# Author: Colin Laganier
# ####################################################


class Node():
    """
    Node class that creates every node of the shape tree, defining each node's data and children.
    """

    def __init__(self, data='root', children=None):
        self.data = data
        self.children = children


# Shape pieces tree to lead to shapeID
node = Node('Root', [
    Node((0, 0), [
        Node((0, 1), [
            Node((1, 0), [
                Node((1, -1), [Node(16)]),
                Node((0, 2), [Node(7)]),
                Node((2, 0), [Node(10)]),
            ]),
            Node((0, 2), [
                Node((1, 1), [Node(15)]),
                Node((1, 2), [Node(9)])
            ]),
            Node((1, 1), [
                Node((1, 2), [Node(18)]),
                Node((2, 1), [Node(6)]),
            ]),
        ]),
        Node((1, 0), [
            Node((1, -1), [
                Node((1, -2), [Node(5)]),
                Node((1, 1), [Node(13)]),
                Node((2, -1), [Node(19)])
            ]),
            Node((1, 1), [
                Node((2, 0), [Node(12)]),
                Node((2, 1), [Node(17)]),
                Node((1, 2), [Node(11)])
            ]),
            Node((2, 0), [
                Node((1, -1), [Node(14)]),
                Node((2, 1), [Node(4)]),
                Node((2, -1), [Node(8)])
            ]),
        ]),
    ]),
])

# Dictionnary with every shape's relative position of the last three node from a (0,0) point
shapes_path = {
    4: [(1, 0), (2, 0), (2, 1)],
    5: [(1, 0), (1, -1), (1, -2)],
    6: [(0, 1), (1, 1), (2, 1)],
    7: [(0, 1), (1, 0), (0, 2)],
    8: [(1, 0), (2, 0), (2, -1)],
    9: [(0, 1), (0, 2), (1, 2)],
    10: [(0, 1), (1, 0), (2, 0)],
    11: [(1, 0), (1, 1), (1, 2)],
    12: [(1, 0), (1, 1), (2, 0)],
    13: [(1, 0), (1, -1), (1, 1)],
    14: [(1, 0), (2, 0), (1, -1)],
    15: [(0, 1), (0, 2), (1, 1)],
    16: [(0, 1), (1, 0), (1, -1)],
    17: [(1, 0), (1, 1), (2, 1)],
    18: [(0, 1), (1, 1), (1, 2)],
    19: [(1, 0), (1, -1), (2, -1)]
}
run_once = False  # create a variable set to false


def Tetris(grid):
    """
    Main function that defines the solution matrix and its size, calls the matrix traversal function and returns the competed solution matrix.
    :param grid: target matrix
    """
    global num, length, width, try_solution, run_once  # variables used in multiple functions
    try_solution = grid  # define modifiable solution matrix from the target one
    if run_once:  # ensures the functin only runs once
        return
    # define dimensions of matrix variables
    width, length = len(grid[0]), len(grid)
    num = 1  # create shape number variable
    movement()
    for j in range(length):  # matrix traversal
        for i in range(width):
            if try_solution[j][i] == 1:  # if target square not identified as part of a shape
                # piece transformed into an empty tuple
                try_solution[j][i] = (0, 0)
    run_once = True
    return try_solution


def movement():
    """
    Fuctions called by the Tetris function, that traverses the solution matrix vertically and horizontally and calls the shapeCheck function to fit shapes in the grid for both of the score goals. 
    """
    global length, width, try_solution
    for j in range(length):  # matrix traversal
        for i in range(width):
            if try_solution[j][i] == 1:  # if target square is found
                # call shape fitting function, looking for a complete path (4 squares)
                shapeCheck(j, i, node, 4, 0, [])
    for j in range(length):
        for i in range(width):
            if try_solution[j][i] == 1:
                # call shape fitting function, looking for the best incomplete path (3 squares)
                shapeCheck(j, i, node, 3, 0, [])
            if try_solution[j][i] == 0:
                # transforms blank squares into an empty tuple
                try_solution[j][i] = (0, 0)


def shapeCheck(j, i, node, goal, score=0, path=[]):
    """
    Function that verifies if shape piece coordinates from the tree fit with the target squares of the matrix and calls a following function to modify the solution matrix with the results. If shape piece fits in target matrix then a point will be added to the score. Greedy algorithm that places the first result found.
    :param j: solution matrix row number
    :param i: solution matrix collumn number
    :param node: current node of the tree being explored by the function
    :param goal: number of fitted pieces desired (4-perfect fit, 3-missing & excess piece)
    :param score: number of pieces fitted on target square in solution matrix by current traversing
    :param path: current path to a certain node
    """
    global num, length, width, try_solution
    if score < goal:  # until path is complete
        for child in node.children:  # iterate over the children of the tree
            if child.data == None:
                break
            if type(child.data) != tuple:
                continue  # if the shapeID node is reached jump to the next iteration
            y, x = child.data  # separates the coordinates of the shape piece
            # verifies that the shape piece would fit inside the matrix
            if ((j+y) < length) and ((i+x) < width) and (i+x) >= 0:
                if goal == 4:
                    if try_solution[j+y][i+x] == 1:
                        score += 1  # increases the score for every fitting piece
                        # checks the children of the piece
                        shapeCheck(j, i, child, goal, score, path)
                else:
                    if path:
                        # calls pathChecking function if path list is not empty
                        pathCheck(path, node.children, score)
                    if try_solution[j+y][i+x] == 1:
                        score += 1
                        # increases the score for every fitting piece and adds its coordinates to the path list
                        path.append(child)
                    else:
                        continue
                    # recursively checks each child from each node
                    shapeCheck(j, i, child, goal, score, path)
    else:
        combinePath(j, i, node.children[0])  # calls solution placing function
        num += 1  # increments the shape number for every shape that is placed in the solution matrix


def pathCheck(path, children, score):
    """
    Function removes the points awarded from previous pieces fit that did not lead to a score of 3 by verifying if previous children from one node is in the path.
    :param path: list of the nodes that fit in the target matrix
    :param children: list of all the children from one node
    :param score: number of pieces fitted on target square in solution matrix by current traversing
    """
    if path[-1] in children:
        path.pop(-1)
        score -= 1  # deducts one point if final piece of the list is unsuccessful child of the node and removes it from the list
        # recursively checks if another node needs to be removed from the list
        pathCheck(path, children, score)


def combinePath(j, i, shapeID):
    """
    Function verifies if any shape is overwritting previously added shapes and if any piece is 
    outside of the matrix and places the shapeID and number of the correct pieces in the solution 
    matrix. The errors commonly originate from a shape piece that obtained a score of 3 despite 
    have a point deducted for one of its pieces not verifying the constraints.
    :param j: solution matrix row number
    :param i: solution matrix collumn number
    :param shapeID: shapeID node, with its associated shape number (shapeID.data) 
    """
    global num, length, width, try_solution
    if type(shapeID.data) != int:
        # iterates recursively to obtain the piece shapeID
        combinePath(j, i, shapeID.children[0])
    else:
        # iterates in shapes_path list
        for block in shapes_path[shapeID.data]+[(0, 0)]:
            y, x = block  # separates the coordinates of the shape piece
            if ((j+y) > length-1) or ((i+x) > width-1) or ((i+x) < 0):
                num -= 1  # deduct one from the shape number counter as the shape will not be added
                break
            if type(try_solution[j+y][i+x]) == tuple:
                if try_solution[j+y][i+x][0] != 0:
                    num -= 1  # verifies shapeID and shape number
                    break
            if block == (0, 0):  # last piece is reached
                for piece in shapes_path[shapeID.data]+[(0, 0)]:
                    try_solution[j+piece[0]][i+piece[1]
                                             ] = (shapeID.data, num)  # places shapeID
                break
