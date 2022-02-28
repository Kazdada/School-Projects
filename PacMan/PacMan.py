############################# I M P O R T S #############################
from re import T
import sys, pygame, os
from tkinter import Scale
from unittest.mock import NonCallableMagicMock
from turtle import distance
from random import randint
from time import sleep

# INITILIAZE PYGAME
pygame.init()
pygame.joystick.init()
pygame.font.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

#########################################################################
########################### C O N S T A N T S ###########################
#########################################################################
# Colours
BLACK       = (  0,  0,  0)
WHITE       = (255,255,255)
GRAY        = ( 50, 50, 50)
DARK_GREEN  = ( 34,177, 76)
YELLOW      = (255,255,  0)
###
CLOCK = pygame.time.Clock()
###
MOVEMENT_SAFETY = 0.75
###
FONT = pygame.font.Font("misc\\zig.ttf", 64)
###
SELECTOR = pygame.image.load(f"misc\\img\\selector.png")
SELECTOR.set_colorkey(DARK_GREEN)
PACMAN = pygame.transform.rotate(pygame.image.load(f"misc\\img\\Pacman\\pacman_3.png"), 90)
#########################################################################
############################# C L A S S E S #############################
#########################################################################
class _Char_:
    def __init__(self) -> None: # Used to create all atributes of basic character
        self.images = []
        self.amount_of_images = len(self.images)
        self.size: int # Size together with position need images and that is why you can't specify them for general object
        self.position: pygame.Rect # It's rectangle, it is called position because it is mostly used for deciding positions
        self.current_image = 0
        self.image_change = 1
        self.time_for_image = time_to_update_image
        self.speed = 60 // frames

        self.last_direction = [0,0]
        self.current_direction = [0,0]
        self.wanted_direction = [0,0,0,0]
        
    # Methods that change current_direction
    def _go_left_(self) -> None:
        self.current_direction = [-self.speed, 0]
    def _go_right_(self) -> None:
        self.current_direction = [self.speed, 0]
    def _go_up_(self) -> None:
        self.current_direction = [0, -self.speed]
    def _go_down_(self) -> None:
        self.current_direction = [0, self.speed]
    # Methonds that set character's wanted_direction
    def _want_left_(self) -> None:
        self.wanted_direction = [time_to_change_direction, 0, 0, 0]
    def _want_right_(self) -> None:
        self.wanted_direction = [0, time_to_change_direction, 0, 0]
    def _want_up_(self) -> None:
        self.wanted_direction = [0, 0, time_to_change_direction, 0]
    def _want_down_(self) -> None:
        self.wanted_direction = [0, 0, 0, time_to_change_direction]
    # Methods used for character movement
    def _change_direction_(self) -> None: # Change current_direction based on wanted_direction
        for index, value in enumerate(self.wanted_direction):
            if value > 0:
                if index == 0:
                    self._go_left_()
                elif index == 1:
                    self._go_right_()
                elif index == 2:
                    self._go_up_()
                elif index == 3:
                    self._go_down_()
                break
    def _update_wanted_directions_(self) -> None: # Lower all parts of wanted_direction by 1
        for index in range(4):
            self.wanted_direction[index] -= 1
    def _move_(self) -> None: # Movement based on current_direction, also checks walls to stop the character
        self.position.x += self.current_direction[0]
        hit_list = self._wall_collision_()
        for tile in hit_list:
              if self.current_direction[0] > 0:
                  self.position.right = tile.left
              elif self.current_direction[0] < 0:
                  self.position.left = tile.right
              
        self.position.y += self.current_direction[1]
        hit_list = self._wall_collision_()
        for tile in hit_list:
            if self.current_direction[1] > 0:
                self.position.bottom = tile.top
            elif self.current_direction[1] < 0:
                self.position.top = tile.bottom
    def _wall_collision_(self) -> list: # Returns the list of all walls the character is touching
        global current_map

        hit_list = []
        for wall in current_map.walls:
            if self.position.colliderect(wall):
                hit_list.append(wall)

        return hit_list
    def square_move(self) -> None: # Movement that is more square-ish, makes it easier to move in game
        self.last_direction = self.current_direction

        self._change_direction_()

        self.position.x += self.current_direction[0]
        self.position.y += self.current_direction[1]

        hit_list = self._wall_collision_()

        if len(hit_list) > 0:
            self.position.x -= self.current_direction[0]
            self.position.y -= self.current_direction[1]
            self._update_wanted_directions_()

            self.current_direction = self.last_direction
            self._move_()
        else:
            self.wanted_direction = [0,0,0,0]
    # Methonds used for visuals of character
    def _update_image_(self) -> None: # Change current image of the animation
        if self.time_for_image <= 0:
            self.current_image += self.image_change
            self.time_for_image = time_to_update_image

            if self.current_image == self.amount_of_images - 1 or self.current_image == -self.amount_of_images:
                self.image_change = -self.image_change
                self.current_image += (self.image_change * self.amount_of_images)
        else:
            self.time_for_image -= 1
    def _load_images_(self, folder) -> None:
        for image_name in os.listdir(folder):
            new_image = pygame.image.load(f"{folder}\\{image_name}")
            self.images.append(new_image)
            self.amount_of_images = len(self.images)

        self.size = self.images[0].get_width()
        self.position = pygame.Rect(0, 0, self.size, self.size)
    def draw(self, char_screen: pygame.Surface) -> None: # Draw the player on character screen
        self._update_image_()
        self.images[self.current_image].set_colorkey(BLACK)
        char_screen.blit(self.images[self.current_image], (self.position.x, self.position.y))
    def remove(self, char_screen: pygame.Surface) -> None: # Remove the player from character screen (better than filling the whole screen with black)
        rect = pygame.Rect(self.position.x, self.position.y, self.size, self.size)
        pygame.draw.rect(char_screen, BLACK, rect)

class Player(_Char_):
    def __init__(self) -> None: # Used to create all atributes of a player
        super().__init__()
        self._load_images_("misc\\img\\Pacman")

        self._want_left_() # Player starts by going left
        self.position.x = current_map.player_spawn_point[0]
        self.position.y = current_map.player_spawn_point[1]
        self.rotated_image = self.images[0]
        
        self.dead = False
        self._load_death_animation_()
        
    # Methods to control player input in game
    def _keyboard_movement_(self) -> bool: # Checks keyboard input and calls appropriate responses (Returns true if player wants to pause the game)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT   : self._want_left_()
                if event.key == pygame.K_RIGHT  : self._want_right_()
                if event.key == pygame.K_UP     : self._want_up_()
                if event.key == pygame.K_DOWN   : self._want_down_()
                if event.key == pygame.K_a      : self._want_left_()
                if event.key == pygame.K_d      : self._want_right_()
                if event.key == pygame.K_w      : self._want_up_()
                if event.key == pygame.K_s      : self._want_down_()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE: return True
            return False
    def _controller_buttons_(self) -> bool: # Checks controller buttons input and calls appropriate responses (Returns true if player wants to pause the game) (Only XBOX360 controller "FOR NOW")
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 7:
                    return True
    def _controller_axis_movement_(self) -> None: # Checks left controller joystick and calls appropriate responses (Only XBOX360 controller "FOR NOW")
            if event.type == pygame.JOYAXISMOTION:
                if event.axis < 2:
                    if abs(event.value) > 0.85:
                        if event.axis == 0:
                            if event.value > 0: self._want_right_()
                            else: self._want_left_()
                        else:
                            if event.value > 0: self._want_down_()
                            else: self._want_up_()
    def _controller_arrows_movement_(self) -> None: # Checks controller arrows input and calls appropriate responses (Only XBOX360 controller "FOR NOW")
            if event.type == pygame.JOYHATMOTION:
                if event.value[0] != 0 and event.value[1] == 0:
                    if event.value[0] == 1: self._want_right_()
                    else: self._want_left_()

                if event.value[0] == 0 and event.value[1] != 0:
                    if event.value[1] == 1: self._want_up_()
                    else: self._want_down_()
    def check_input(self) -> bool: # Collection of all the inputs (Returns true if player wants to pause the game)
        if self._keyboard_movement_() or self._controller_buttons_():
            return True
        _check_controlers_()
        self._controller_axis_movement_()
        self._controller_arrows_movement_()
    # Methods used for player movement
    def _boundaries_movement_(self) -> None: # Allows player to move from one side of screen to another side
        offset = 1

        if self.position.x >= current_map.small_map_size[0] - offset:
            self.position.x = -self.size + offset

        elif self.position.x <= -self.size + offset:
            self.position.x = current_map.small_map_size[0] - offset

        elif self.position.y >= current_map.small_map_size[1] - offset:
            self.position.y = -self.size + offset

        elif self.position.y <= -self.size + offset:
            self.position.y = current_map.small_map_size[1] - offset
    def square_move(self) -> bool: # Uses _Char_ square_move, adds _boundaries_movement_ and ability to collect points
        super().square_move()
        
        self._boundaries_movement_()
        self._consume_points_(self._point_collision_())
        return self._ghost_collision_() 
    # Methods for collecting points and increasing score
    def _point_collision_(self) -> list: # Checks for any points player collided with
        hit_list = []
        for point in current_map.points:
            if self.position.colliderect(point):
                hit_list.append(point)
        return hit_list

    def _ghost_collision_(self) -> bool:
        global ghosts
        for ghost in ghosts:
            if self.position.colliderect(ghost.position):
                return True
        return False

    def _consume_points_(self, hit_points: list) -> None: # Removes touched points and increases score
        global score
        global current_map

        for point in hit_points:
            current_map.points.remove(point)
            rect = pygame.Rect(point.x, point.y, self.size, self.size)
            pygame.draw.rect(current_map.point_screen, BLACK, rect)
            score += 10
    # Methods used for visuals of player character
    def _load_death_animation_(self) -> None:
        self.death_images = self.images[::-1]
        self.amount_of_death_images = self.amount_of_images
        for image_name in os.listdir("misc\\img\\PacMan Death"):
            new_image = pygame.image.load(f"misc\\img\\PacMan Death\\{image_name}")
            self.death_images.append(new_image)
            self.amount_of_death_images += 1
            
    def _update_rotation_(self, images) -> None: # Rotates current image of animation based on what direction player is going
        if self.current_direction[0] == self.speed:
            self.rotated_image = pygame.transform.rotate(images[self.current_image], 270)
        elif self.current_direction[0] == -self.speed:
            self.rotated_image = pygame.transform.rotate(images[self.current_image], 90)
        elif self.current_direction[1] == self.speed:
            self.rotated_image = pygame.transform.rotate(images[self.current_image], 180)
        elif self.current_direction[1] == -self.speed:
            self.rotated_image = pygame.transform.rotate(images[self.current_image], 0)
    def draw(self, char_screen: pygame.Surface) -> None: # Updates current image of animation, rotates it and then draws the player
        if self.dead:
            self._update_rotation_(self.death_images)
        else:
            self._update_image_()
            self._update_rotation_(self.images)
            
        char_screen.blit(self.rotated_image, (self.position.x, self.position.y))

class _Ghost_(_Char_):
    """To create a unique ghost, create a subclass where you overwrite
        attributes:
            self.scatter_destination
            self.scatter_max
            self.chase_max
        # Make sure to call "super().__init__()" before you make those changes!
        # After you make changes to the attributes call method "_update_attributes_()", it updates remaining attributes based on those changes
        
        method:
            _chase_direction_()

        # Now everything should work nicely
    """
    def __init__(self) -> None: # Used to create all atributes of basic ghost
        super().__init__()
        # scatter_max, chase_max are attributes carrying how long does the ghost stay in scatter/chase mode
        self.scatter_max = 600
        self.chase_max = 600
        # scatter_time, chase_time are timers of current cycle, they are reset back to max after one cycle
        self.scatter_time = self.scatter_max
        self.chase_time = self.chase_max

        self.image_change = 0

        self.scatter_destination = (5, 5) # scatter destination is unique to each ghost, it determines their goal location during scatter mode
        self.destination = self.scatter_destination # destination is current goal of the ghost's path

        self.last_frame_positions = (-1, -1)
        self.cooldown = -1
        # self._want_left_()

        # self._load_images_("misc\\img\\Ghosts") # \\GhostName (\\Chaser)


        # self.position.x = current_map.ghost_spawn_points[0][0]
        # self.position.y = current_map.ghost_spawn_points[0][1]

    # Method used during creation of new ghost type
    def _update_attributes_(self) -> None:
        self.scatter_time = self.scatter_max
        self.chase_time = self.chase_max
        self.destination = self.scatter_destination
    # Methods used for movement of the ghosts
    def _chase_direction_(self, player_x: int, player_y: int) -> None: # Method determining ghost's destination during chase
        pass
    def _path_finding_(self) -> None: # Method used to determine where the ghost wants to go
        global current_map
        potential_directions = []

        if self.position.x >= self.destination[0]:
            potential_directions.append(("left", self.position.x - self.destination[0]))
        else:
            potential_directions.append(("right", self.destination[0] - self.position.x))
        if self.position.y >= self.destination[1]:
            potential_directions.append(("up", self.position.y - self.destination[1]))
        else:
            potential_directions.append(("down", self.destination[1] - self.position.y))

        if potential_directions[0][1] <= potential_directions[1][1]:
            potential_directions.pop(0)
        else:
            potential_directions.pop(1)


        if potential_directions[0][0] == "up" and self.current_direction[1] <= 0:
            self._want_up_()
        elif potential_directions[0][0] == "down" and self.current_direction[1] >= 0:
            self._want_down_()
        elif potential_directions[0][0] == "left" and self.current_direction[0] <= 0:
            self._want_left_()
        elif potential_directions[0][0] == "right" and self.current_direction[0] >= 0:
            self._want_right_()
        
        if self.position.x < 1 or self.position.x > (current_map.map_size_blocks[0] - 1)*16 or self.position.y < 1 or self.position.y > (current_map.map_size_blocks[1] - 1)*16:
            self.current_direction[0] = -self.current_direction[0]
            self.current_direction[1] = -self.current_direction[1]
            #print(self.position.x, self.position.y)

    def square_move(self, player_x: int, player_y: int) -> None: # Square move method altered to fit the ghosts
        if self.scatter_time > 0:
            self.destination = self.scatter_destination
            self.scatter_time -= 1

        elif self.chase_time > 0:
            self._chase_direction_(player_x, player_y)
            self.chase_time -= 1

        else:
            self.scatter_time = self.scatter_max
            self.chase_time = self.chase_max
        
        self._path_finding_()
        if self.position.x == self.last_frame_positions[0] and self.position.y == self.last_frame_positions[1] and self.cooldown < 0:
            x = randint(0,3)
            if x == 0 and self.current_direction[1] <= 0:
                self._want_up_()
            elif x == 1 and self.current_direction[1] >= 0:
                self._want_left_()
            elif x == 2 and self.current_direction[0] <= 0:
                self._want_down_()
            elif x == 3 and self.current_direction[0] >= 0:
                self._want_right_()

            self.cooldown = 10
        self.cooldown -= 1
        self.last_frame_positions = (self.position.x, self.position.y)

        super().square_move()

class Chaser(_Ghost_):
    def __init__(self) -> None:
        super().__init__()

        self._load_images_("misc\\img\\Ghosts\\Chaser") # \\GhostName

        self.position.x = current_map.ghost_spawn_points[0][0]
        self.position.y = current_map.ghost_spawn_points[0][1]


    def _chase_direction_(self, player_x: int, player_y: int) -> None:
        self.destination = (player_x, player_y)

class SmartAss(_Ghost_):
    def __init__(self) -> None:
        super().__init__()
        self.last_x_of_player = 0
        self.last_y_of_player = 0
        self.offset = 2

        self._update_attributes_()

        self._load_images_("misc\\img\\Ghosts\\SmartAss") # \\GhostName

        self.position.x = current_map.ghost_spawn_points[0][0]
        self.position.y = current_map.ghost_spawn_points[0][1]

    def _chase_direction_(self, player_x: int, player_y: int) -> None:
        if self.last_x_of_player != player_x:
            if self.last_x_of_player - player_x < 0:
                self.destination = (player_x + self.offset, player_y)
            else:
                self.destination = (player_x - self.offset, player_y)

        elif self.last_y_of_player != player_y:
            if self.last_y_of_player - player_y < 0:
                self.destination = (player_x, player_y + self.offset)
            else:
                self.destination = (player_x, player_y - self.offset)

class Charger(_Ghost_):
    def __init__(self) -> None:
        super().__init__()
        self.scatter_max = 480
        self.chase_max = 120

        self._update_attributes_()

        self._load_images_("misc\\img\\Ghosts\\Charger") # \\GhostName

        self.position.x = current_map.ghost_spawn_points[0][0]
        self.position.y = current_map.ghost_spawn_points[0][1]


    def _chase_direction_(self, player_x: int, player_y: int) -> None:
        self.destination = (player_x, player_y)

    def square_move(self, player_x: int, player_y: int) -> None:
        if self.scatter_time > 0:
            self.speed = 0
        else:
            self.speed = 120 // frames
        super().square_move(player_x, player_y)

class LazyChaser(_Ghost_):
    def __init__(self) -> None:
        super().__init__()
        self.scatter_max = 0
        self.speed = 60 // frames

        self._update_attributes_()

        self._load_images_("misc\\img\\Ghosts\\LazyChaser") # \\GhostName

        self.position.x = current_map.ghost_spawn_points[0][0]
        self.position.y = current_map.ghost_spawn_points[0][1]

    def _chase_direction_(self, player_x: int, player_y: int) -> None:
        self.destination = (player_x, player_y)

class Map():
    def __init__(self, level: int = 1) -> None: # Initialze all atributes and call mathod to create the map
        self.name: str
        self.map_size_blocks: tuple # This size is measured in amount of blocks, not actual pixels
        self.small_map_size: tuple # This size is measured in pixels

        self.wall_images = []
        self.wall_size: int
        self.walls = []

        self.point_image: pygame.image
        self.point_size: int
        self.points = []

        self.wall_screen: pygame.Surface
        self.char_screen: pygame.Surface
        self.point_screen: pygame.Surface
        self.game_screen: pygame.Surface # Combination of point_screen and char_screen (in this order)

        self.player_spawn_point: tuple
        self.ghost_spawn_points = [] # List of tuples representing spawn points
        self.number_of_ghosts = 0


        self._create_map_(level)
        self.point_screen.set_colorkey(BLACK)
        self.char_screen.set_colorkey(BLACK)
    # Methods to create the map
    def _create_map_(self, level: int) -> None: # Reads file of inputted level and fills all attributes of the map   
        variables = {}
        current_level_file = os.listdir(f"levels")[level-1]

        with open(f"levels\\{current_level_file}", "r") as reader:
            while True:
                line = reader.readline()
                line.replace(" ", "")

                if line == "" or line[0] == "\n" or line[0] == "#":
                    continue # Skip empty lines

                elif line[0] == "$": # Map grid
                    # Prepare necesary atributes for grid creation
                    self._fill_up_attributes_(variables)

                    # Generation of the grid itself
                    self._generate_grid_(reader)
                    break
                else: # Only possibilty left is a variable
                    line = line.replace(" ", "").split("=")
                    variables[line[0]] = line[1][:-1]
        
        reader.close()
    def _fill_up_attributes_(self, variables: dict) -> None: # Assign data from the level file to the atributes
        # Man Name
        self.name = variables["name"]

        # Walls
        amount_of_wall_images = int(variables["amount_of_walls"])
        for i in range(1, amount_of_wall_images + 1):
            self.wall_images.append(pygame.image.load(variables[f"wall_{i}"]))
        self.wall_size = self.wall_images[0].get_width()

        # Map Size (we needed wall_size)
        self.map_size_blocks = variables["map_size_blocks"].split("x")
        self.map_size_blocks = (int(self.map_size_blocks[0]), int(self.map_size_blocks[1]))
        self.small_map_size = self.wall_size * self.map_size_blocks[0], self.wall_size * self.map_size_blocks[1]

        # Create surfaces (we needed small_map_size)
        self.wall_screen = pygame.Surface(self.small_map_size)
        self.point_screen = pygame.Surface(self.small_map_size)
        self.char_screen = pygame.Surface(self.small_map_size)
        self.game_screen = pygame.Surface(self.small_map_size)

        # Point
        self.point_image = pygame.image.load(variables["point_image"])
        self.point_size = self.point_image.get_width()
    def _generate_grid_(self, reader) -> None: # Receives the reader when map is about to generate, creates all surfaces, rects(points and wall)
        for current_y in range(0, self.map_size_blocks[1]*self.wall_size, self.wall_size):
            line = reader.readline()
            for index, value in enumerate(line[:-1]):
                current_x = index * self.wall_size
                # The following insane if statement just makes sure points are not generated in border areas
                if value == "0" and not (current_x == 0 or current_y == 0) and not (current_x == self.small_map_size[0] - self.wall_size or current_y == self.small_map_size[1] - self.wall_size):
                    offset = (self.wall_size - self.point_size) // 2
                    self.points.append(pygame.Rect(current_x+offset, current_y+offset, self.point_size, self.point_size))
                    self.point_screen.blit(self.point_image, (current_x+offset, current_y+offset))

                elif value == "P":
                    self.player_spawn_point = (current_x, current_y)

                elif value == "G":
                    self.ghost_spawn_points.append((current_x, current_y))
                    self.number_of_ghosts += 1

                elif int(value) > 0: # Anything bigger than 0 is taken as a wall TODO Redo this to add fruits and similar
                    self.walls.append(pygame.Rect(current_x, current_y, self.wall_size, self.wall_size))
                    self.wall_screen.blit(self.wall_images[int(value)-1], (current_x, current_y))
    # Method to draw the map on screen
    def draw(self, screen: pygame.Surface) -> None: # Draws the level on the screen (including points and characters)
        global game_window_size

        self.game_screen.blit(self.wall_screen, (0,0))
        self.game_screen.blit(self.point_screen, (0,0))
        self.game_screen.blit(self.char_screen, (0,0))

        self.big_game_screen = pygame.transform.scale(self.game_screen, game_window_size)
        screen.blit(self.big_game_screen, game_window_position)

class Menu:
    def __init__(self, image, options: list) -> None:
        self.image = image
        self.image_size = image.get_width()
        self.options = options
        self.amount_of_options = len(self.options)
        self.current_option = 0
        self.confirm = False
        self.go_back = False
        self.joystick_timer = 0

        self.texts = self._create_texts_()
        self.visual = self._create_visual_()
    def _move_up_(self) -> None:
        self.current_option = (self.current_option - 1) % self.amount_of_options
    def _move_down_(self) -> None:
        self.current_option = (self.current_option + 1) % self.amount_of_options
    def _create_texts_(self) -> list:
        texts = []
        for option in self.options:
            texts.append(FONT.render(option, True, WHITE))
        return texts
    def _create_image_(self):
        self.image_surface = pygame.Surface((self.image_size, self.image_size))
        self.image_surface.blit(self.image, (0, 0))
        self.image_surface = pygame.transform.scale(self.image_surface, (300,300))
    def _create_selection_(self):
        self.selection_surface = pygame.Surface((600, 400))
        for index in range(self.amount_of_options):
            self.selection_surface.blit(self.texts[index], (8, 100*index))
    def _create_visual_(self) -> None:
        self._create_image_()
        self._create_selection_()

        visual = pygame.Surface((800, 800))
        visual.blit(self.image_surface, (300,0))
        visual.blit(self.selection_surface, (200,400))

        return visual
    def _keyboard_keys_(self):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP     : self._move_up_()
            if event.key == pygame.K_DOWN   : self._move_down_()
            if event.key == pygame.K_w      : self._move_up_()
            if event.key == pygame.K_s      : self._move_down_()
            if event.key == pygame.K_RETURN : self.confirm = True
            if event.key == pygame.K_SPACE  : self.confirm = True
            if event.key == pygame.K_ESCAPE : self.go_back = True
    def _controller_buttons_(self) -> None:
        if event.type == pygame.JOYBUTTONUP:
            if event.button == 0:
                self.confirm = True
            if event.button == 1:
                self.go_back = True
    def _controller_axis_movement_(self) -> None:
        if event.type == pygame.JOYAXISMOTION:
            if self.joystick_timer < 0 and event.axis < 2:
                if abs(event.value) > 0.85:
                    if event.axis == 1:
                        if event.value > 0: self._move_down_()
                        else: self._move_up_()
                        self.joystick_timer = int(frames * 0.85)
    def _controller_arrows_movement_(self) -> None:
        if event.type == pygame.JOYHATMOTION:
            if event.value[0] == 0 and event.value[1] != 0:
                if event.value[1] == 1: self._move_up_()
                else: self._move_down_()

    def check_input(self) -> int:
        _check_controlers_()
        self._controller_buttons_()
        self._keyboard_keys_()
        self._controller_arrows_movement_()
        self._controller_axis_movement_()

        if self.go_back == True:
            self.current_option = self.amount_of_options - 1
            self.confirm = True

        if self.confirm == True:
            self.confirm = False
            return self.current_option

        self.joystick_timer -= 1
        return -1
    def draw_selector(self) -> None:
        self.visual.blit(SELECTOR, (84, 416 + 100*self.current_option))
    def remove_selector(self) -> None:
        black_rect = pygame.Surface((32,32))
        self.visual.blit(black_rect, (84, 416 + 100*self.current_option))
        
class PopUpMenu(): # Right now does nothing in the actual program, just wrote it for something I wanted to do but didn't have time or energy to do.
    def __init__(self, question: str, option_1: str, option_2: str) -> None:
        self.question = question
        self.option_1 = option_1
        self.option_2 = option_2
        self.current_option = 0
        self.confirm = False
        self.back = False
        self.option_len = max(len(option_1), len(option_2)) * FONT.size
        self.window_size_x = int(len(question) * FONT.size)

        self._create_visuals_()
        self._run_()
        
    def _create_visuals_(self) -> None:
        self.pop_up_screen = pygame.surface.Surface((int(self.window_size_x * 1.2),100))
        self._create_question_()
        self._create_options_()

        self.pop_up_screen.blit(self.question, (int(self.window_size_x * 1.2) - self.window_size_x) // 2, 10)
        self._run_()

    def _create_question_(self) -> None: # Convert string question into actual fonted text
        self.question = FONT.render(self.question, True, YELLOW)

    def _create_options_(self) -> None: # Convert string options into actual fonted text
        self.option_1 = FONT.render(self.option_1, True, YELLOW)
        self.option_2 = FONT.render(self.option_2, True, YELLOW)

    def _keyboard_keys_(self):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT  : self.current_option = 0 # TODO change this
            if event.key == pygame.K_RIGHT : self.current_option = 0 # TODO change this
            if event.key == pygame.K_RETURN: self.confirm = True
            if event.key == pygame.K_ESCAPE: self.back = True
    def _controller_buttons_(self) -> None:
        if event.type == pygame.JOYBUTTONUP:
            if event.button == 0:
                self.confirm = True
            if event.button == 1:
                self.back = True
    def _controller_axis_movement_(self) -> None:
        if event.type == pygame.JOYAXISMOTION:
            if self.joystick_timer < 0 and event.axis < 2:
                if abs(event.value) > 0.85:
                    if event.axis == 0:
                        if event.value > 0: self.current_option = 0 # TODO change this
                        else: self.current_option = 0 # TODO change this
                        self.joystick_timer = int(frames * 0.85)
    def _controller_arrows_movement_(self) -> None:
        if event.type == pygame.JOYHATMOTION:
            if event.value[0] != 0 and event.value[1] == 0:
                if event.value[1] == 1: self.current_option = 0 # TODO change this
                else: self.current_option = 0 # TODO change this

    def _check_input_(self) -> int:
        _check_controlers_()
        self._controller_buttons_()
        self._keyboard_keys_()
        self._controller_arrows_movement_()
        self._controller_axis_movement_()

    def _draw_(self) -> None:
        pass

    def _run_(self) -> int:
        while True:
            CLOCK.tick(frames)

            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

                choice = self._check_input_()
                if choice:
                    return choice


            self._draw_()


            pygame.display.flip()

class InfoSurface(): # Used for showing map name, score and lives
    def __init__(self, type: str, text: str = None, icon: pygame.Surface = None, amount_of_icons: int = 0) -> None:
        if type == "text":
            self.text = FONT.render(text, True, WHITE)
            self._create_screen_text_()
        elif type == "icon":
            self.icon = icon
            self.amount_of_icons = amount_of_icons
            self._create_screen_images_()
        
    def _create_screen_text_(self) -> None:
        self.surface = pygame.Surface((512, 64))
        self.surface.blit(self.text, (0, 0))

        self.surface = pygame.transform.scale(self.surface, (256,32))

    def _create_screen_images_(self) -> None:
        self.surface = pygame.Surface((128, 16))
        for i in range(self.amount_of_icons):
            self.surface.blit(self.icon, (i*20, 0))

        self.surface = pygame.transform.scale(self.surface, (256,32))
#########################################################################
########################### F U N C T I O N S ###########################
#########################################################################
# Technical functions (used to create and keep everything working)
def _check_controlers_() -> None: # Reinitialzes controllers if controller is disconnected or new one is connected
    global joysticks
    if event.type == pygame.JOYDEVICEADDED or event.type == pygame.JOYDEVICEREMOVED:
        joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
def load_settings(display: bool = 0, audio: bool = 0, controls: bool = 0) -> None: # Read setting.txt and adjust selected setting category
    global frames
    global window_res
    global window_size
    global fullscreen
    global gameplay_volume
    global music_volume

    settings = {}
    read_lines = display
    with open(f"misc\\settings.txt", "r") as reader:
        line = reader.readline()
        while True:
            line = reader.readline()
            line.replace(" ", "")
            if line == "" or line[0] == "\n" or line[0] == "#":
                continue
            
            elif line[0] == "$":
                if line[1:-1] == "Display" and display:
                    read_lines = True
                elif line[1:-1] == "Audio" and audio:
                    read_lines = True
                elif line[1:-1] == "Controls" and controls:
                    read_lines = True
                elif line == "$$$All$$$\n":
                    break
                else:
                    read_lines = False
            elif read_lines:
                line = line.replace(" ", "").split("=")
                settings[line[0]] = line[1]
    reader.close()

    if display:
        frames = int(settings["frames"])
        window_res = settings["window_res"].split("x")
        window_res = (int(window_res[0]), int(window_res[1]))
        window_size = settings["window_size"].split("x")
        window_size = (int(window_size[0]), int(window_size[1]))
        fullscreen = int(settings["fullscreen"])
    if audio:
        gameplay_volume = int(settings["gameplay_volume"])
        music_volume = int(settings["music_volume"])
    if controls:
        pass
def calculate_variables() -> None: # Calculate variable depending on data from settings
    global game_window_size, game_window_position, score, time_to_update_image
    global time_to_change_direction, frames, window_res, window_size

    game_window_size = (3 * window_size[0] // 4, 3 * window_size[1] // 4)
    game_window_position = (window_size[0] - game_window_size[0]) // 2, (window_size[1] - game_window_size[1]) // 2
    score = 0

    time_to_update_image = frames // 4
    time_to_change_direction = frames // MOVEMENT_SAFETY

def respawn(player: Player, ghosts: list) -> None:
    global current_map

    player.position.x = current_map.player_spawn_point[0]
    player.position.y = current_map.player_spawn_point[1]
    player.current_image = 0
    player._go_left_()
    for i in range(len(ghosts)):
        ghosts[i].position.x = current_map.ghost_spawn_points[i][0]
        ghosts[i].position.y = current_map.ghost_spawn_points[i][1]

# Main loop functions (Game + Menus)
def menu(menu: Menu) -> int:
    global screen
    global event
    global window_size

    menu.confirm = False
    menu.go_back = False

    screen.fill(BLACK)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11: pygame.display.toggle_fullscreen()

            choice = menu.check_input()
            if choice > -1:
                return choice

        menu.draw_selector()
        big_map = pygame.transform.scale(menu.visual, (window_size[0]//3, (window_size[1]//3) * 2))
        menu.remove_selector()

        screen.blit(big_map, (window_size[0]//3, window_size[1]//6))

        pygame.display.flip()

def game(level: int) -> int: # Actual Pacman game, inputted integer is an index of a level that will generate
    global current_map
    global score
    global screen
    global event
    global lives
    global ghosts

    current_map = Map(level)
    player = Player()
    ghosts = []

    map_name = InfoSurface(type="text", text=current_map.name)
    live_board = InfoSurface(type="icon", icon=pygame.transform.rotate(player.images[1], 90), amount_of_icons= lives)
    scoreboard = InfoSurface(type="text", text=f"{score}")


    for i in range(current_map.number_of_ghosts):
        x = randint(0,3)
        if x == 0:
            ghosts.append(Chaser())
        elif x == 1:
            ghosts.append(LazyChaser())
        elif x == 2:
            ghosts.append(Charger())
        elif x == 3:
            ghosts.append(SmartAss())

        ghosts[i].position.x = current_map.ghost_spawn_points[i][0]
        ghosts[i].position.y = current_map.ghost_spawn_points[i][1]

    wait = False

    def _draw_characters_() -> None:
        player.draw(current_map.char_screen)
        for ghost in ghosts:
            ghost.draw(current_map.char_screen)
    
    def _remove_characters_() -> None:
        player.remove(current_map.char_screen)
        for ghost in ghosts:
            ghost.remove(current_map.char_screen)

    def _death_animation_(player: Player) -> None:
        player.dead = True
        player.current_image = 0
        waiting_frames = 0
        while True:
            CLOCK.tick(frames)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

            if waiting_frames <= 0:     
                waiting_frames = 30
                player.current_image += 1
                if player.current_image == player.amount_of_death_images:
                    player.dead = False
                    player.current_image = 0
                    break
            else: waiting_frames -= 1
                
            _draw_characters_()
            current_map.draw(screen)
            _remove_characters_()

            pygame.display.flip()
    
    def _save_highscore_() -> None:
        global score

        highscores = open("Highscores.txt", "w")
        highscores.write(f"YOU      {score}")
        highscores.close()

    def _display_info_screns_() -> None:
        global window_size
        offset = 2
        x_change = 256
        y_change = 32

        screen.blit(map_name.surface, (offset, offset))
        screen.blit(scoreboard.surface, (window_size[0] - x_change - offset, offset))
        screen.blit(live_board.surface, (offset, window_size[1] - y_change - offset))

    def _game_over_() -> None:
        global lives
        global score

        lives = 3
        _save_highscore_()
        score = 0

    while True:
        CLOCK.tick(frames)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11: pygame.display.toggle_fullscreen()
                if event.key == pygame.K_F10: return 0

            if player.check_input():
                _game_over_()
                return -1
                

        if player.square_move(): # Returns True if player touches ghost after moving
            lives -= 1
            live_board = InfoSurface(type="icon", icon=player.images[0], amount_of_icons= lives)
            _death_animation_(player)
            if lives < 1:
                _game_over_()
                return -1
            respawn(player, ghosts)
            wait = True
        
        scoreboard = InfoSurface(type="text", text=f"{score:0>9}")

        if current_map.points == []:
            return 0
        
        for ghost in ghosts:
            ghost.square_move(player.position.x, player.position.y)

        _draw_characters_()
        _display_info_screns_()
        current_map.draw(screen)
        _remove_characters_()

        pygame.display.flip()

        if wait:
            sleep(2)
            wait = False
        

#########################################################################
########################### M A I N   C O D E ###########################
#########################################################################
#LOAD UP SETTINGS
frames: int
window_res: tuple
window_size: tuple
fullscreen: bool
gameplay_volume: int
music_volume: int
load_settings(1,1,0) #TODO add controls into settings and then load them by changing 0->1
#############################################
# CALCULATE REMAINING VARIABLES
game_window_size: tuple
game_window_position: tuple
time_to_update_image: int
time_to_change_direction: int
score: int
lives: int = 3
ghosts = []
level_limit = len(os.listdir(f"levels"))
# print(level_limit)
event = "EVENT FOR GAME" # Just need to create global variable event, will be used for player inputs
monitor_size = pygame.display.Info()
calculate_variables()
#############################################
# SCREEN SETUP, (Includes icon and window name)
screen = pygame.display.set_mode(window_size)
if fullscreen: pygame.display.toggle_fullscreen()
pygame.display.set_caption("PacMan")
icon = pygame.image.load("misc\\img\\Pacman\\Pacman_3.png")
icon = pygame.transform.rotate(icon, 270)
icon.set_colorkey(BLACK)
pygame.display.set_icon(icon)
#############################################
# MAIN LOOP
main_menu = Menu(PACMAN, ["START GAME", "HIGHSCORES", "SETTINGS", "QUIT"])
settings_menu = Menu(PACMAN, ["GAMEPLAY", "DISPLAY", "AUDIO"])
while True: # Whole game loop
    i = 1
    choice = menu(main_menu)
    while choice == 0:
        choice = game(i % level_limit) # Works because I can use -1 index
        i += 1
    if choice == 2:
        menu(settings_menu)
        settings_menu.current_option = 0
    if choice == 3: sys.exit()
    # current_menu = main_menu
    # current_popup = main_menu_popup
    #
    # choice = current_menu.show()
    # if choice == 0:
    #   score = 0
    #   current_popup = game_pop_up
    #   while choice == 0:
    #         current_map = Map("filename")
    #         choice = game()
    #         if choice == -1:
    #             gameover()
    # if choice == 1:
    #     highscore()
    # elif choice == 2:
    #     current_menu = setting_menu
    #     current_menu.show()
    # elif choice == 3:
    #     sys.exit()
    #
    #