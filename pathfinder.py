from tkinter import messagebox, Tk
import pygame
import sys

window_width = 500
window_height = 500

window = pygame.display.set_mode((window_width, window_height))

columns = 25
rows = 25

box_width = window_width // columns
box_height = window_height // rows

grid = []
queue = []
path = []

class Box:
    def __init__(self, i, j):
        self.x = i
        self.y = j
        self.start = False
        self.wall = False
        self.target = False
        self.queued = False
        self.visited = False
        self.neighbors = []
        self.prior = None


    def draw(self, win, color):
        pygame.draw.rect(win, color, (self.x * box_width + 1, self.y * box_height + 1, box_width - 2, box_height - 2))

    def set_neighbors(self):
        if self.x > 0:
            self.neighbors.append(grid[self.x - 1][self.y])
        if self.x < columns - 1:
            self.neighbors.append(grid[self.x + 1][self.y])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y - 1])
        if self.y < rows - 1:
            self.neighbors.append(grid[self.x][self.y + 1])

def initialize_game():
    grid.clear()
    queue.clear()
    path.clear()

    # Create grid
    for i in range(columns):
        arr = []
        for j in range(rows):
            arr.append(Box(i,j))
        grid.append(arr)

    # Set Neighbors
    for i in range(columns):
        for j in range(rows):
            grid[i][j].set_neighbors()


class Text():
    def __init__(self, text, size, color, x, y):
        self.text = text
        self.size = size
        self.x = x
        self.y = y
        self.color = color
    
    def draw(self, window):
        menu_font = pygame.font.Font(None, self.size)
        text_surface = menu_font.render(self.text, True, self.color)
        window.blit(text_surface, (self.x, self.y))


class Button:
    def __init__(self, color, x, y, button_width, button_height, text=None):
        self.color = color
        self.x = x
        self.y = y
        self.width = button_width
        self.height = button_height
        self.text = Text(text, 30, (0, 0, 0), x + button_width/3, y + button_height/2.5)

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        if self.text:
            self.text.draw(win)

    def isclicked(self, event) -> bool:
        if event.type != pygame.MOUSEBUTTONDOWN:
            return False

        mouse_x = pygame.mouse.get_pos()[0]
        mouse_y = pygame.mouse.get_pos()[1]
        if (self.x <= mouse_x <= self.x + self.width) and (self.y <= mouse_y <= self.y + self.height):
            return True

def popup_message(title, message):
    Tk().wm_withdraw()
    messagebox.showinfo(title, message)

def exit_event(event):
    if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def main():
    print("Log: Starting application.")
    # Initialize data (grid, queue, path, start_box)
    initialize_game()

    start_box = grid[0][0]
    start_box.start = True
    start_box.visited = True
    queue.append(start_box)

    # Create pygame window
    pygame.init()
    
    #Create menu elements
    title = Text('PathFinder Algorithm', 50, (0, 0, 0), window_width/7, 50)
    shift = 30
    start_button = Button((0, 150, 0), window_width/2 - 75, window_height/3 - 40 + shift, 150, 80, 'Start')
    rules_button = Button((0, 150, 0), window_width/2 - 75, window_height/3 + 80 + shift, 150, 80, 'Rules')
    creator = Text('By Joseph Evans', 25, (0, 0, 0), window_width/2 - 70, window_height - 50)

    # Setup conditional
    show_menu = True

    begin_search = False
    target_box_set = False
    searching = True
    target_box = None
    finished_program = False

    while True:

        # Main Menu
        while show_menu:
            for event in pygame.event.get():
                # Quit window event
                exit_event(event)

                # Start button event
                if start_button.isclicked(event):
                    show_menu = False
                
                # Rules button event
                if rules_button.isclicked(event):
                    popup_message('Rules',
                    "How to Play:\n\n" +
                    "Left-click and drag the mouse to draw walls.\n" +
                    "Right-click to choose the target box.\n" + 
                    "Press any key to start the search algorithm.\n" +
                    "Once the search has completed, you can press any key to restart the program.")

            window.fill((125, 125, 125))

            title.draw(window)
            start_button.draw(window)
            rules_button.draw(window)
            creator.draw(window)
            
            pygame.display.update()

        # Main screen
        for event in pygame.event.get():
            # Quit window event
            exit_event(event)

            # Mouse controls
            # Drag the mouse
            if (event.type == pygame.MOUSEMOTION and event.buttons[0]) or (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]

                # Draw wall
                i = x // box_width
                j = y // box_height
                grid[i][j].wall = True

            # Right-Click
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]

                i = x // box_width
                j = y // box_height
                target_box = grid[i][j]
                # Set Target
                if not target_box_set and not target_box.start and not target_box.wall:
                    target_box.target = True
                    target_box_set = True

            # Start Algorithm
            if event.type == pygame.KEYDOWN and target_box_set:
                begin_search = True

        if begin_search:
            if len(queue) > 0 and searching:
                current_box = queue.pop(0)
                current_box.visited = True
                if current_box == target_box:
                    searching = False
                    print("Log: Search finished. Found solution!")
                    while current_box.prior != start_box:
                        path.append(current_box.prior)
                        current_box = current_box.prior
                    finished_program = True
                else:
                    for neighbor in current_box.neighbors:
                        if not neighbor.queued and not neighbor.wall:
                            neighbor.queued = True
                            neighbor.prior = current_box
                            queue.append(neighbor)

            else:
                if searching:
                    print("Log: Search finished. No solution found.")
                    popup_message("No solution", "There is no solution!")
                    searching = False
                    finished_program = True

        window.fill((0, 0, 0))

        for i in range(columns):
            for j in range(rows):
                box = grid[i][j]
                box.draw(window, (125, 125, 125))

                if box.queued:
                    box.draw(window, (200, 0, 0))
                if box.visited:
                    box.draw(window, (0, 200, 0))
                if box in path:
                    box.draw(window, (0, 0, 200))


                if box.start:
                    box.draw(window, (0, 200, 200))
                if box.wall:
                    box.draw(window, (139, 69, 19))
                if box.target:
                    box.draw(window, (200, 200, 0))

        pygame.display.update()

        # Exit program update
        if finished_program:
            button_pressed = False
            for event in pygame.event.get():
                # Quit window event
                exit_event(event)

                # Keypress to restart
                if event.type == pygame.KEYDOWN:
                    button_pressed = True
                    break

            if button_pressed:
                print("Log: Keypressed. Exiting loop.")
                break
            
    
    # Restart application if loop is broken by keypress
    print("Log: Restarting application.")
    main()

        

main()

# Created by Joseph Evans