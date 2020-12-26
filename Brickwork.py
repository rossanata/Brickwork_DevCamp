import copy


# The directions used in the source code are based on the projection of the 3d brick layer as seen from above:
# right and left (horizontal), up and down (vertical)
#
#                                      vertical(up,  down)
#     +----+----+----+----+           ^
#    / 1  / 1  / 2  / 2  /|          /
#   +----+----+----+----+ |         /
#  / 3  / 3  / 4  / 4  /| +        /
# +----+----+----+----+ |/        +-----------> horizontal(right, left)
# |    |    |    |    | +
# |    |    |    |    |/
# +----+----+----+----+


def is_odd(num):
    if num % 2:
        return True
    else:
        return False


# Check if brick can lie on the current cell and the neighbouring cell on the right side of current cell
# row is row index of current cell
# col is column index of current cell
def is_horizontal_brick_allowed(layer_one, layer_two, row, col):
    if col + 1 < len(layer_one[0]):
        if layer_one[row][col] != layer_one[row][col + 1] and \
                layer_two[row][col + 1] == 0:
            return True


# Check if brick can lie on the current cell and the neighbouring cell on the bottom side of current cell
# row is row index of current cell
# col is column index of current cell
def is_vertical_brick_allowed(layer_one, layer_two, row, col):
    if row + 1 < len(layer_one):
        if layer_one[row][col] != layer_one[row + 1][col]:
            if layer_two[row + 1][col] == 0:
                return True


# Verify that all cells of the second layer are filled
def is_layer_2_complete(layer_two):
    is_complete = True
    for i in range(len(layer_two)):
        for j in range(len(layer_two[0])):
            if layer_two[i][j] == 0:
                is_complete = False
                return is_complete
    return is_complete


# find_second_layer function finds possible layout of the second layer or returns None if impossible to do so.
# It traverses through the first layer, represented by a multidimensional list, starting from the top-left cell.
# layer_1 is base input layer, represented by multidimensional list
# layer_2 is layer with the same size as layer one, initially filled with zeros in every single cell. It shows current
# state of layer two throughout the recursions.
# row is row index of current cell, the initial value of row must be zero
# col is column index of current cell, the initial value of col must be zero
# brick_number is unique id of the brick, the initial value of brick_number must be one


def find_second_layer(layer_1, layer_2, row=0, col=0, brick_number=1):
    while row < len(layer_2):
        while col < len(layer_2[0]):
            if layer_2[row][col] == 0:
                # The function checks if a brick can lie both in horizontal and vertical direction. If both directions
                # are allowed recursion is used in order to check both scenarios for a possible solution.
                if is_horizontal_brick_allowed(layer_1, layer_2, row, col) and \
                        is_vertical_brick_allowed(layer_1, layer_2, row, col):
                    # recursion
                    # go horizontal
                    layer_3 = copy.deepcopy(layer_2)
                    layer_3[row][col] = brick_number
                    layer_3[row][col + 1] = brick_number
                    success_layer = find_second_layer(layer_1, layer_3, row, col + 2, brick_number + 1)
                    if success_layer:
                        return success_layer
                    # go vertical
                    layer_2[row][col] = brick_number
                    layer_2[row + 1][col] = brick_number
                    success_layer = find_second_layer(layer_1, layer_2, row, col + 1, brick_number + 1)
                    if success_layer:
                        return success_layer
                # If both directions are not allowed the function checks if only one direction is allowed and proceeds
                # with laying the new brick at layer two(writing the respective brick number at the current cell and the
                # neighbouring cell allowed).
                elif is_horizontal_brick_allowed(layer_1, layer_2, row, col):
                    layer_2[row][col] = brick_number
                    layer_2[row][col + 1] = brick_number
                    brick_number += 1
                    col += 2
                    if is_layer_2_complete(layer_2):
                        return layer_2
                elif is_vertical_brick_allowed(layer_1, layer_2, row, col):
                    layer_2[row][col] = brick_number
                    layer_2[row + 1][col] = brick_number
                    brick_number += 1
                    col += 1
                    if is_layer_2_complete(layer_2):
                        return layer_2
                else:
                    col += 1
                    if is_layer_2_complete(layer_2):
                        return layer_2
            else:
                col += 1
                if is_layer_2_complete(layer_2):
                    return layer_2
        if is_layer_2_complete(layer_2):
            return layer_2
        row += 1
        col = 0
    # No solution found
    return None


# Main function that handles the assignment input and output
def main():
    (rows_count, columns_count) = [int(x) for x in input().split()]

    if is_odd(rows_count):
        print('\nRows count is not an even number.')
    elif is_odd(columns_count):
        print('\nColumns count is not an even number.')
    elif rows_count > 100:
        print('\nRows count should be less than 100.')
    elif columns_count > 100:
        print('\nColumns count should be less than 100.')
    else:
        layer_1 = []
        for _ in range(rows_count):
            current_row = [int(x) for x in input().split()]
            layer_1.append(current_row)

        empty_layer = [[0 for _ in range(columns_count)] for _ in range(rows_count)]
        success_layer = find_second_layer(layer_1, empty_layer)
        if success_layer:
            print(success_layer)
        else:
            print('No solution found')
            exit(-1)


if __name__ == '__main__':
    main()

# 1) Validate there are no bricks spanning 3 rows/columns.
# 2) Surround each brick of the second layer with asterisk and/ or dash symbols - `*`
# and/ or `-`. There should be a single line of symbols between two bricks.
#     -----------------           ^
#     - 1   1 - 2 - 3 -
#     ---------   -   -
#     - 4   4 - 2 - 3 -
#     -----------------
#
#     *-----------*-----*-----*           ^
#     *  1     1  *  2  *  3  *
#     *-----------*     *     *
#     *  4     4  *  2  *  3  *
#     *-----------*-----*-----*
# 3)Unittests
