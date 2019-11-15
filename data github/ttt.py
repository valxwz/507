'''
SI 507 Fall 2018 Homework 1
'''

# Create board - Setup the data structure for storing board data
#the data structure would be a list of 9 spaces


# Loop until game is over
    
    # Step 1: Print board
    '''
    This function will take in current board data and print out the board in the console as shown 
    in the instructions.
    parameter: board_data - a data structure used for holding current moves on the board
    return: None
    '''
    def print_board(board_data):
        pass

    # Step 2: 
    '''
    this function will take the input of the x's direction and insert the "x" into the board data at the right position.
    In this function, the direction will be changed from text to numbers. For example, the NW would be changed to number 1. 
    parameter: x_direction - input of which direction user wants to move "x" to, board_data - the current board data
    '''
    
    def move_x(board_data, x_direction):
        pass

    

    
    # Step 3:
    '''
    this function will take the input of the o's direction and insert the "o" into the data at the right position.
    In this function, the direction will be changed from text to numbers. For example, the NW would be changed to number 1. 
    parameter: o_direction - input of which direction user wants to move "o" to, board_data - the current board data
    return: none
    '''
    
 
    def move_o(board_data, o_direction):
        pass


    # Step 4: 
    '''
    this function will check if the space user choose is available to insert data.
    parameter: board_data - the current board data, direction: the direction user input for either "x" or "o" '''

    def isSpaceFree(board_data, direction):
        pass


    # Step 5: Determine if game is over
    '''
    Take in the current board data and determine if one player wins the game or the game draws. If the game is over,
    terminate the loop, or continue the loop.
    parameter: board_data - current board data
    return: information about current game status
    '''

    def determine_over(board_data):
        pass
