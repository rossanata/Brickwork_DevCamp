import copy

# Valid input data is presumed. Only requested validation included in the solution. No validation introduced for wrong
# combination and position of numbers, data types used, etc. as it is not included in the requirements.

# The directions used in the source code are based on the projection of the 3d brick layer as seen from above:
# right and left (horizontal), up and down (vertical)
#
#                                                           +----+----+----+----+
#          projection axis                                 / 1  / 1  / 2  / 2  /|
#         ^                                               +----+----+----+----+ |
#         |     vertical(up,  down)                      / 3  / 3  / 4  / 4  /| +
#         |   ^                                         +----+----+----+----+ |/
#         |  /                                          |    |    |    |    | +
#         | /                                           |    |    |    |    |/
#         |/                                            +----+----+----+----+
#         +-----------> horizontal(right, left)


def is_odd(num):
    if num % 2:
        return True
    else:
        return False

# Check for bricks spanning 3 rows/ columns.
def is_brick_3cells(layer):
    for i in range(len(layer)):
        for j in range(len(layer[0]) - 2):
            if layer[i][j] == layer[i][j + 1] == layer[i][j + 2]:
                return True
    for i in range(len(layer) - 2):
        for j in range(len(layer[0])):
            if layer[i][j] == layer[i + 1][j] == layer[i + 2][j]:
                return True
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


# visualize_layer function separates bricks with asterisks horizontally and with dashes vertically. It also outlines a
# border of the whole layer. The function returns multidimensional list of chars.
# Example of how output layer looks after visualize_layer function:
#     *-------------*------*------*
#     *   1      1  *   2  *   3  *
#     *-------------*      *      *
#     *   4      4  *   2  *   3  *
#     *------*------*------*------*
#     *   8  *   5  *   6      6  *
#     *      *      *-------------*
#     *   8  *   5  *   7      7  *
#     *------*------*-------------*

def visualize_layer(layer):
    # Size of temp_layer
    temp_layer_row = len(layer) * 2 + 1
    temp_layer_col = len(layer[0]) * 7 + 1
    # Create temp_layer (multidimensional list) of emtpy spaces - ' '
    temp_layer = [[' ' for _ in range(temp_layer_col)] for _ in range(temp_layer_row)]

    for row in range(len(layer)):
        for col in range(len(layer[0])):
            # Upper separator of cell
            #      ------ ------ ------ ------
            #         1      2      2      3
            #             ------ ------
            #         1      4      4      3
            #
            if row == 0 or layer[row][col] != layer[row - 1][col]:
                for i in range(1, 7):
                    temp_layer[2 * row][7 * col + i] = '-'

            # Bottom separator of cell
            #
            #         1      2      2      3
            #             ------ ------
            #         1      4      4      3
            #      ------ ------ ------ ------
            if row == len(layer) - 1 or layer[row][col] != layer[row + 1][col]:
                for i in range(1, 7):
                    temp_layer[2 * row + 2][7 * col + i] = '-'

            # Left separator of cell
            # If first column cell or if neighbouring cell on the left is different -> left separator of three '*'
            #     *      *             *
            #     *   1  *   2      2  *   3
            #     *      *             *
            #     *   1  *   4      4  *   3
            #     *      *             *
            if col == 0 or layer[row][col] != layer[row][col - 1]:
                for i in range(3):
                    temp_layer[2 * row + i][7 * col] = '*'

            # # Not first row and column cell -> top left separator '-' if neighbouring cell on the left is the same and
            # # above two cells form a brick as well
            #
            #         1      2      2      3
            #                   -
            #         1      4      4      3
            #
            if col != 0 and row != 0 and layer[row][col] == layer[row][col - 1] and \
                    layer[row - 1][col] == layer[row - 1][col - 1]:
                temp_layer[2 * row][7 * col] = '-'

            # First row cell -> top left separator '-' if neighbouring cell on the left is the same
            #                   -
            #         1      2      2      3
            #
            #         1      4      4      3
            #
            if col != 0 and row == 0 and layer[row][col] == layer[row][col - 1]:
                temp_layer[0][7 * col] = '-'

            # Last row cell -> bottom left separator '-' if neighbouring cell on the left is the same
            #
            #         1      2      2      3
            #
            #         1      4      4      3
            #                   -
            if col != 0 and row == len(layer) - 1 and layer[row][col] == layer[row][col - 1]:
                temp_layer[len(layer) * 2][7 * col] = '-'

            # Right separator of cell - only right border of entire layout needs to be covered as the rest is covered by
            # left separator
            #                                 *
            #         1      2      2      3  *
            #                                 *
            #         1      4      4      3  *
            #                                 *
            if col == len(layer[0]) - 1:
                for i in range(3):
                    temp_layer[2 * row + i][7 * col + 7] = '*'

            # Brick numeric value
            if len(str(layer[row][col])) == 2:
                temp_layer[2 * row + 1][7 * col + 3] = str(layer[row][col])[0]
                temp_layer[2 * row + 1][7 * col + 4] = str(layer[row][col])[1]
            else:
                temp_layer[2 * row + 1][7 * col + 4] = layer[row][col]

    # Convert multidimensional list - temp_layer to a string.
    result = ''
    for i in range(len(temp_layer)):
        for j in range(len(temp_layer[0])):
            result += str(temp_layer[i][j])
        result += '\n'
    return result


# find_second_layer function finds possible layout of the second layer or returns None if impossible to do so.
# It traverses through the first layer, represented by a multidimensional list, starting from the top-left cell.
# layer_1 is base input layer, represented by multidimensional list
# layer_2 is layer with the same size as layer one, initially filled with zeros in every single cell. It shows current
# state of layer two throughout the recursions.
# row is row index of current cell, the initial value of row must be zero
# col is column index of current cell, the initial value of col must be zero
# brick_number is unique id of the brick, the initial value of brick_number must be one
def find_second_layer(layer_1, layer_2, row=0, col=0, brick_number=1):
    if row < len(layer_2):
        if col < len(layer_2[0]):
            if layer_2[row][col] == 0:
                # The function checks if a brick can lie in horizontal or vertical direction. In case it is allowed, it
                # proceeds with laying the new brick at layer two(writing the respective brick number at the current
                # cell and the neighbouring cell allowed). Recursion is used in order to check all scenarios for a
                # possible solution.
                if is_horizontal_brick_allowed(layer_1, layer_2, row, col):
                    layer_3 = copy.deepcopy(layer_2)
                    layer_3[row][col] = brick_number
                    layer_3[row][col + 1] = brick_number
                    success_layer = find_second_layer(layer_1, layer_3, row, col + 2, brick_number + 1)
                    if success_layer:
                        return success_layer

                if is_vertical_brick_allowed(layer_1, layer_2, row, col):
                    layer_2[row][col] = brick_number
                    layer_2[row + 1][col] = brick_number
                    success_layer = find_second_layer(layer_1, layer_2, row, col + 1, brick_number + 1)
                    if success_layer:
                        return success_layer
                # No solution found
                return None
            else:
                success_layer = find_second_layer(layer_1, layer_2, row, col + 1, brick_number)
                if success_layer:
                    return success_layer
        else:
            success_layer = find_second_layer(layer_1, layer_2, row + 1, 0, brick_number)
            if success_layer:
                return success_layer
    else:
        if is_layer_2_complete(layer_2):
            return layer_2
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

        if is_brick_3cells(layer_1):
            print('\nThere are bricks spanning 3 rows/columns.')
        else:
            empty_layer = [[0 for _ in range(columns_count)] for _ in range(rows_count)]
            success_layer = find_second_layer(layer_1, empty_layer)
            if success_layer:
                print(visualize_layer(success_layer))
            else:
                print('No solution found')
                exit(-1)


if __name__ == '__main__':
    main()
