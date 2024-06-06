import pygame
import sqlite3
import time
from levels import levels  # Import levels from levels.py

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 500
TILE_SIZE = 32
BUTTON_WIDTH = 50
BUTTON_HEIGHT = 30
NEW_BOX_SCALE = 1.4
TIME_LIMIT = 60  # 60 seconds per level

BACKGROUND_MUSIC = 'assets/sounds/background.mp3'
MENU_MUSIC = 'assets/sounds/menu.wav'
SOUNDS = {
    'move': 'assets/sounds/move.wav',
    'box_move': 'assets/sounds/box_move.wav',
    'undo': 'assets/sounds/undo.wav',
    'level_complete': 'assets/sounds/level_complete.wav',
}

BUTTON_IMAGES = {
    'restart': 'assets/Menu/Buttons/Restart.png',
    'previous': 'assets/Menu/Buttons/Previous.png',
    'next': 'assets/Menu/Buttons/Next.png',
    'quit': 'assets/Menu/Buttons/Close.png',
}

TIMER_POSITION = (500, 10)  # Top-right corner
START_POSITION = [7, 8]  

player_name = ""

def display_game(selected_background, selected_box, selected_player):
    global player_name
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Sokoban')

    # Initialize pygame mixer
    pygame.mixer.init()
    pygame.mixer.music.stop()

    # Load selected assets
    background_img = pygame.image.load(selected_background)
    bg_width, bg_height = background_img.get_size()
    new_box_img = pygame.image.load(selected_box)
    player_img = pygame.image.load(selected_player)
    wall_img = pygame.image.load('assets/Terrain/bricks.png')  # Load the single brick image
    wall_img = pygame.transform.scale(wall_img, (TILE_SIZE, TILE_SIZE))  # Resize the brick image

    # Load and play background music
    pygame.mixer.music.load(BACKGROUND_MUSIC)
    pygame.mixer.music.play(-1)  # Play the music indefinitely

    # Load sound effects
    move_sound = pygame.mixer.Sound(SOUNDS['move'])
    box_move_sound = pygame.mixer.Sound(SOUNDS['box_move'])
    undo_sound = pygame.mixer.Sound(SOUNDS['undo'])
    level_complete_sound = pygame.mixer.Sound(SOUNDS['level_complete'])

    # Load and scale new box image
    new_box_size = int(TILE_SIZE * NEW_BOX_SCALE)
    new_box_img = pygame.transform.scale(new_box_img, (new_box_size, new_box_size))

    # Load and scale player image
    player_img = pygame.transform.scale(player_img, (TILE_SIZE, TILE_SIZE))

    # Load and resize button images
    restart_button_img = pygame.transform.scale(pygame.image.load(BUTTON_IMAGES['restart']), (BUTTON_WIDTH, BUTTON_HEIGHT))
    previous_button_img = pygame.transform.scale(pygame.image.load(BUTTON_IMAGES['previous']), (BUTTON_WIDTH, BUTTON_HEIGHT))
    next_button_img = pygame.transform.scale(pygame.image.load(BUTTON_IMAGES['next']), (BUTTON_WIDTH, BUTTON_HEIGHT))
    quit_button_img = pygame.transform.scale(pygame.image.load(BUTTON_IMAGES['quit']), (BUTTON_WIDTH, BUTTON_HEIGHT))

    # Track current level
    current_level = 0
    current_game_id = int(time.time())  # Unique game ID based on start time
    map_matrix = levels[current_level]
    initial_map_matrix = [row[:] for row in map_matrix]

    # Define player position (in terms of grid coordinates)
    player_pos = START_POSITION[:]
    initial_player_pos = player_pos[:]

    # Create surfaces for targets and boxes
    target_img = pygame.Surface((TILE_SIZE, TILE_SIZE))
    target_img.fill((0, 0, 0))  
    box_img = new_box_img  # Use the new box image

    # Define button size and positions
    reset_button_rect = pygame.Rect(30, 470, BUTTON_WIDTH, BUTTON_HEIGHT)
    undo_button_rect = pygame.Rect(80, 470, BUTTON_WIDTH, BUTTON_HEIGHT)
    next_button_rect = pygame.Rect(130, 470, BUTTON_WIDTH, BUTTON_HEIGHT)
    quit_button_rect = pygame.Rect(180, 470, BUTTON_WIDTH, BUTTON_HEIGHT)

    # Create font for buttons
    font = pygame.font.Font(None, 24)

    # Track player moves for undo functionality
    move_history = []
    moves_count = 0  # Track number of moves
    level_start_time = time.time()  # Track level start time

    # Function to draw buttons
    def draw_buttons():
        screen.blit(restart_button_img, reset_button_rect.topleft)
        screen.blit(previous_button_img, undo_button_rect.topleft)
        screen.blit(next_button_img, next_button_rect.topleft)
        screen.blit(quit_button_img, quit_button_rect.topleft)

    # Function to undo the last move
    def undo_move():
        nonlocal moves_count
        if move_history:
            last_move = move_history.pop()
            map_matrix[last_move['box_new_pos'][0]][last_move['box_new_pos'][1]] = last_move['box_old_val']
            map_matrix[last_move['new_pos'][0]][last_move['new_pos'][1]] = last_move['new_val']
            map_matrix[last_move['player_pos'][0]][last_move['player_pos'][1]] = 0
            player_pos[:] = last_move['player_pos']
            moves_count += 1
            undo_sound.play()  # Play undo sound

    # Function to reset the game
    def reset_game():
        nonlocal map_matrix, player_pos, moves_count, level_start_time
        map_matrix = [row[:] for row in initial_map_matrix]
        player_pos = initial_player_pos[:]
        move_history.clear()
        moves_count = 0
        level_start_time = time.time()

    # Function to move to the next level
    def next_level():
        nonlocal current_level, map_matrix, initial_map_matrix, player_pos, initial_player_pos, moves_count, level_start_time
        current_level = (current_level + 1) % len(levels)
        map_matrix = levels[current_level]
        initial_map_matrix = [row[:] for row in map_matrix]
        player_pos = START_POSITION[:]
        initial_player_pos = player_pos[:]
        move_history.clear()
        moves_count = 0
        level_start_time = time.time()

    # Function to check win condition
    def check_win_condition():
        for row in map_matrix:
            for tile in row:
                if tile == 1:  # If there's still a target without a box, game is not won
                    return False
        return True

    # Function to save score
    def save_score(level, moves, time_taken):
        conn = sqlite3.connect('sokoban_scores.db')
        c = conn.cursor()
        c.execute('INSERT INTO scores (game_id, level, moves, time, player_name) VALUES (?, ?, ?, ?, ?)',
                (current_game_id, level, moves, time_taken, player_name))
        conn.commit()
        conn.close()

    # Function to display scores on screen
    def display_scores_on_screen():
        conn = sqlite3.connect('sokoban_scores.db')
        c = conn.cursor()
        c.execute('SELECT player_name, level, moves, time FROM scores WHERE game_id = ? ORDER BY level, moves, time', (current_game_id,))
        scores = c.fetchall()
        conn.close()

        screen.fill((255, 255, 255))  # Fill the screen with white
        font = pygame.font.Font(None, 24)
        
        text_y = 50
        title_text = font.render("Player   | Level | Moves | Time", True, (0, 0, 0))
        screen.blit(title_text, (50, text_y))
        text_y += 30
        for score in scores:
            player_name = score[0] if score[0] is not None else "Unknown"
            level = score[1] if score[1] is not None else "N/A"
            moves = score[2] if score[2] is not None else "N/A"
            time_taken = score[3] if score[3] is not None else 0.0
            score_text = font.render(f"{player_name:10} | {level:5} | {moves:5} | {time_taken:.2f}", True, (0, 0, 0))
            screen.blit(score_text, (50, text_y))
            text_y += 30

        pygame.display.flip()
        pygame.time.wait(5000)  # Display the scores for 5 seconds

    # Function to display the end screen
    def end_screen():
        # Clear the previous game screen
        screen.fill((0, 0, 0))
        pygame.display.set_caption('Play Again?')

        # Load button images
        replay_button_img = pygame.image.load('assets/Menu/Buttons/Play.png')
        replay_button_img = pygame.transform.scale(replay_button_img, (80, 40))
        replay_button_rect = replay_button_img.get_rect(center=(300, 250))

        quit_button_img = pygame.image.load('assets/Menu/Buttons/Close.png')
        quit_button_img = pygame.transform.scale(quit_button_img, (80, 40))
        quit_button_rect = quit_button_img.get_rect(center=(300, 350))

        # Stop the background music
        pygame.mixer.music.stop()

        # Load and play menu background music
        pygame.mixer.music.load(MENU_MUSIC)
        pygame.mixer.music.play(-1)  # Play the music indefinitely

        # Define font
        font = pygame.font.Font(None, 50)

        def draw_end_screen():
            screen.fill((0, 0, 0))  # Black background

            end_text = font.render('Play Again?', True, (255, 255, 255))
            screen.blit(end_text, (200, 150))

            screen.blit(replay_button_img, replay_button_rect.topleft)
            screen.blit(quit_button_img, quit_button_rect.topleft)
            pygame.display.flip()

        running = True
        while running:
            draw_end_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if replay_button_rect.collidepoint(event.pos):
                        running = False
                        start_screen()
                    elif quit_button_rect.collidepoint(event.pos):
                        pygame.quit()
                        exit()
        draw_end_screen()
        pygame.display.flip()
        pygame.time.delay(10)

    # Main loop
    running = True
    while running:
        current_time = time.time()
        elapsed_time = current_time - level_start_time
        remaining_time = max(0, TIME_LIMIT - elapsed_time)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                new_pos = player_pos.copy()
                if event.key == pygame.K_UP:
                    new_pos[0] -= 1  # Move up
                elif event.key == pygame.K_DOWN:
                    new_pos[0] += 1  # Move down
                elif event.key == pygame.K_LEFT:
                    new_pos[1] -= 1  # Move left
                elif event.key == pygame.K_RIGHT:
                    new_pos[1] += 1  # Move right

                # Check if the new position is not a wall or a box with another box/wall behind it
                if map_matrix[new_pos[0]][new_pos[1]] != -1:
                    if map_matrix[new_pos[0]][new_pos[1]] == 2:  # Box
                        # Calculate box new position
                        box_new_pos = [new_pos[0] + (new_pos[0] - player_pos[0]), new_pos[1] + (new_pos[1] - player_pos[1])]
                        # Check if box can be moved to the new position
                        if map_matrix[box_new_pos[0]][box_new_pos[1]] in (0, 1):  # Empty space or target
                            # Record move for undo
                            move_history.append({
                                'player_pos': player_pos[:],
                                'new_pos': new_pos[:],
                                'new_val': map_matrix[new_pos[0]][new_pos[1]],
                                'box_new_pos': box_new_pos[:],
                                'box_old_val': map_matrix[box_new_pos[0]][box_new_pos[1]]
                            })
                            # Move box
                            if map_matrix[box_new_pos[0]][box_new_pos[1]] == 1:  # If moving to a target
                                map_matrix[box_new_pos[0]][box_new_pos[1]] = 3  # Change target to a box on target
                            else:
                                map_matrix[box_new_pos[0]][box_new_pos[1]] = 2  # Move box to the new position
                            map_matrix[new_pos[0]][new_pos[1]] = 0
                            player_pos = new_pos
                            moves_count += 1
                            box_move_sound.play()  # Play box move sound
                            # Check for win condition
                            if check_win_condition():
                                level_time = time.time() - level_start_time
                                save_score(current_level, moves_count, level_time)
                                level_complete_sound.play()  # Play level complete sound
                                if current_level == len(levels) - 1:
                                    display_scores_on_screen()
                                    end_screen()
                                    running = False
                                else:
                                    next_level()
                        else:
                            move_sound.play()  # Play move sound
                            pass
                    else:
                        # Record move for undo
                        move_history.append({
                            'player_pos': player_pos[:],
                            'new_pos': new_pos[:],
                            'new_val': map_matrix[new_pos[0]][new_pos[1]],
                            'box_new_pos': new_pos[:],
                            'box_old_val': map_matrix[new_pos[0]][new_pos[1]]
                        })
                        player_pos = new_pos
                        moves_count += 1
                        move_sound.play()  # Play move sound
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if undo_button_rect.collidepoint(event.pos):
                    undo_move()
                elif reset_button_rect.collidepoint(event.pos):
                    reset_game()
                elif next_button_rect.collidepoint(event.pos):
                    next_level()
                elif quit_button_rect.collidepoint(event.pos):
                    running = False

        if remaining_time <= 0:
            display_scores_on_screen()
            end_screen()
            running = False

        # Draw the background image repeatedly
        for y in range(0, SCREEN_HEIGHT, bg_height):
            for x in range(0, SCREEN_WIDTH, bg_width):
                screen.blit(background_img, (x, y))

        # Draw the map
        for row_index, row in enumerate(map_matrix):
            for col_index, tile in enumerate(row):
                if tile == -1:  # Wall
                    screen.blit(wall_img, (col_index * TILE_SIZE, row_index * TILE_SIZE))
                elif tile == 1:  # Target
                    screen.blit(target_img, (col_index * TILE_SIZE, row_index * TILE_SIZE))
                elif tile == 2:  # Box
                    box_x = col_index * TILE_SIZE - (new_box_size - TILE_SIZE) // 2
                    box_y = row_index * TILE_SIZE - (new_box_size - TILE_SIZE) // 2
                    screen.blit(box_img, (box_x, box_y))
                elif tile == 3:  # Box on Target
                    screen.blit(target_img, (col_index * TILE_SIZE, row_index * TILE_SIZE))
                    box_x = col_index * TILE_SIZE - (new_box_size - TILE_SIZE) // 2
                    box_y = row_index * TILE_SIZE - (new_box_size - TILE_SIZE) // 2
                    screen.blit(box_img, (box_x, box_y))

        # Draw the player
        screen.blit(player_img, (player_pos[1] * TILE_SIZE, player_pos[0] * TILE_SIZE))

        # Draw buttons
        draw_buttons()

        # Draw timer
        timer_text = font.render(f"Time left: {int(remaining_time)}", True, (0, 0, 0))
        screen.blit(timer_text, TIMER_POSITION)  # Adjusted position for the timer

        pygame.display.flip()

    pygame.quit()

def start_screen():
    global player_name
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Sokoban')

    # Initialize pygame mixer
    pygame.mixer.init()
    
    # Load and play menu background music
    pygame.mixer.music.load(MENU_MUSIC)
    pygame.mixer.music.play(-1)  # Play the music indefinitely

    # Load button images
    play_button_img = pygame.image.load('assets/Menu/Buttons/Play.png')
    play_button_img = pygame.transform.scale(play_button_img, (80, 40))
    play_button_rect = play_button_img.get_rect(center=(450, 410))

    # Define font
    font = pygame.font.Font(None, 40)
    small_font = pygame.font.Font(None, 40)

    # Load options for background, boxes, and player
    backgrounds = ['assets/Background/Gray.png', 'assets/Background/Blue.png', 'assets/Background/Brown.png', 'assets/Background/Green.png', 'assets/Background/Pink.png', 'assets/Background/Purple.png', 'assets/Background/Yellow.png']
    boxes = ['assets/Boxes/box1.png', 'assets/Boxes/box2.png', 'assets/Boxes/box3.png']
    players = ['assets/MainCharacters/MaskDude/jump.png', 'assets/MainCharacters/NinjaFrog/jump.png', 'assets/MainCharacters/Pinkman/jump.png', 'assets/MainCharacters/VirtualGuy/jump.png']

    selected_background = backgrounds[0]
    selected_box = boxes[0]
    selected_player = players[0]

    player_name = small_font.render('Enter your name here:', True, (0, 0, 0))
    screen.blit(player_name, (300, 250))
    input_box = pygame.Rect(350, 270, 260, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''

    def draw_options():
        screen.fill((173, 216, 230))  # Light blue background

        title_text = font.render('Welcome to Sokoban!', True, (0, 0, 0))
        screen.blit(title_text, (150, 50))

        name_prompt = small_font.render('Enter your name here:', True, (0, 0, 0))
        screen.blit(name_prompt, (250, 220))

        bg_text = small_font.render('Select Background:', True, (0, 0, 0))
        screen.blit(bg_text, (50, 100))

        # Calculate the starting x position for centering
        option_width = 50  # Width of each option image
        spacing = 10  # Spacing between options
        total_width = len(backgrounds) * option_width + (len(backgrounds) - 1) * spacing
        start_x = (400 - total_width) // 2

        for i, bg in enumerate(backgrounds):
            bg_img = pygame.image.load(bg)
            bg_img = pygame.transform.scale(bg_img, (60, 60))
            bg_rect = bg_img.get_rect(topleft=(50 + i * 80, 140))
            screen.blit(bg_img, bg_rect)
            if selected_background == bg:
                pygame.draw.rect(screen, (0, 100, 0), bg_rect, 3)

        box_text = small_font.render('Select Box:', True, (0, 0, 0))
        screen.blit(box_text, (50, 220))
        for i, box in enumerate(boxes):
            box_img = pygame.image.load(box)
            box_img = pygame.transform.scale(box_img, (60, 60))
            box_rect = box_img.get_rect(topleft=(50 + i * 80, 260))
            screen.blit(box_img, box_rect)
            if selected_box == box:
                pygame.draw.rect(screen, (0, 100, 0), box_rect, 3)

        player_text = small_font.render('Select Player:', True, (0, 0, 0))
        screen.blit(player_text, (50, 340))
        for i, player in enumerate(players):
            player_img = pygame.image.load(player)
            player_img = pygame.transform.scale(player_img, (60, 60))
            player_rect = player_img.get_rect(topleft=(50 + i * 80, 380))
            screen.blit(player_img, player_rect)
            if selected_player == player:
                pygame.draw.rect(screen, (0, 100, 0), player_rect, 3)

        screen.blit(play_button_img, play_button_rect.topleft)

        # Render the current text.
        txt_surface = font.render(text, True, color)
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        # Blit the text.
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        # Blit the input_box rect.
        pygame.draw.rect(screen, color, input_box, 2)
        
        pygame.display.flip()

    running = True
    while running:
        draw_options()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                color = color_active if active else color_inactive

                if play_button_rect.collidepoint(event.pos):
                    player_name = text  # Save the player name
                    running = False
                for i, bg in enumerate(backgrounds):
                    if pygame.Rect(50 + i * 80, 140, 60, 60).collidepoint(event.pos):
                        selected_background = bg
                for i, box in enumerate(boxes):
                    if pygame.Rect(50 + i * 80, 260, 60, 60).collidepoint(event.pos):
                        selected_box = box
                for i, player in enumerate(players):
                    if pygame.Rect(50 + i * 80, 380, 60, 60).collidepoint(event.pos):
                        selected_player = player
            elif event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        player_name = text
                        text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

    display_game(selected_background, selected_box, selected_player)

if __name__ == "__main__":
    start_screen()