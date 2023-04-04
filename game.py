#Modules needed
import pygame
import random
import copy

#initialise pygame
pygame.init()

#Game Variables setup
WIDTH = 500
HEIGHT = 550
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Water Sort Puzzle Game!')
fps = 100
timer = pygame.time.Clock()
font = pygame.font.Font(pygame.font.get_default_font(),24)
new_game = True
#random level could have 10-14 tubes, always two will be empty
tubes =10
tube_colors = []
color_choices = ['red','orange','light blue','pink','purple','dark green','yellow','brown','dark blue','white','light green','dark gray']
selected = False
select_rect = 100
dest_rect=100

#generate new level when initialised
def generate_start():
    tubes_num = random.randint(10,14)
    tubes_colors = []
    COLORS = []
    for i in range(tubes_num):
        tubes_colors.append([])
        if i < tubes_num-2:
            for j in range(4):
                COLORS.append(i)
    for i in range(tubes_num -2):
        for j in range(4):
            color = random.choice(COLORS)
            tubes_colors[i].append(color)
            COLORS.remove(color)
    print(tube_colors, tubes_num)
    return tubes_num , tubes_colors 

#tube drawing on screen with colored rectangles inside
def draw_tubes(tubes_num, tube_cols):
    tube_boxes = []
    if tubes % 2 == 0:
        tubes_per_row = tubes_num // 2
        offset = False
    else:
        tubes_per_row = tubes_num // 2 +1
        offset = True
    spacing = WIDTH / tubes_per_row
    for i in range(tubes_per_row):
        for j in range(len(tube_cols[i])):
            pygame.draw.rect(screen, color_choices[tube_cols[i][j]],[5+spacing*i, 200 -50*j,65,50],0,3)
        box = pygame.draw.rect(screen, 'blue',[5+spacing*i, 50,65,200],5,3)
        if select_rect == i:
            pygame.draw.rect(screen, 'green',[5+spacing*i, 50,65,200],3,3)
        tube_boxes.append(box)
    if offset:
        for i in range(tubes_per_row-1):
            for j in range(len(tube_cols[i + tubes_per_row])):
                 pygame.draw.rect(screen, color_choices[tube_cols[i + tubes_per_row][j]],[(spacing*0.5)+5+spacing*i, 450 -(50*j),65,50],0,3)
            box = pygame.draw.rect(screen, 'blue',[(spacing*0.5)+5+spacing*i, 300,65,200],5,3)
            if select_rect == i + tubes_per_row:
                pygame.draw.rect(screen, 'green',[(spacing*0.5)+5+spacing*i, 300,65,200],3,3)
            tube_boxes.append(box)

    else:
        for i in range(tubes_per_row):
            for j in range(len(tube_cols[i + tubes_per_row])):
                 pygame.draw.rect(screen, color_choices[tube_cols[i + tubes_per_row][j]],[5+spacing*i, 450 -(50*j),65,50],0,3)
            box = pygame.draw.rect(screen, 'blue',[5+spacing*i, 300,65,200],5,3)
            if select_rect == i + tubes_per_row:
                pygame.draw.rect(screen, 'green',[5+spacing*i, 300,65,200],3,3)
            tube_boxes.append(box)
    return tube_boxes

#determine the top colour of the selected tube and the destination tube
#and then check how long a chain of that color to move
def calc_move(colors, selected_rect, destination):
    chain = True
    length = 1
    color_on_top = 100
    color_to_move = 100
    if len(colors[selected_rect])>0:
        color_to_move = colors[selected_rect][-1]
        for i in range(1,len(colors[selected_rect])):
            if chain:
                if colors[selected_rect][-1-i]== color_to_move:
                    length += 1
                else:
                    chain = False
    if 4>len(colors[destination]):
        if len(colors[destination])==0:
            color_on_top = color_to_move
        else:
            color_on_top = colors[destination][-1]
    if color_on_top == color_to_move:
        for i in range(length):
            if len(colors[destination])<4:
                if len(colors[selected_rect])>0:
                    colors[destination].append(color_on_top)
                colors[selected_rect].pop(-1)
    return colors


#check if victory conditions are met
def check_victory(colors):
    won = True
    for i in range(len(colors)):
        if len(colors[i])>0:
            if len(colors[i])!= 4:
                won = False
            else:
                main_color = colors[i][-1]
                for j in range(len(colors[i])):
                    if colors[i][j]!= main_color:
                        won = False
    return won

#main Game Loop
run = True
while run:
    screen.fill('black')
    timer.tick(fps)

    #generate new board/tubes on new game conditions
    if new_game:
        tubes, tube_colors = generate_start()
        initial_colors = copy.deepcopy(tube_colors)
        new_game = False
    else:
        tube_rects = draw_tubes(tubes, tube_colors)
    win = check_victory(tube_colors)


    #event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                tube_colors = copy.deepcopy(initial_colors)
            elif event.key == pygame.K_RETURN:
                new_game = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not selected:
                for item in range(len(tube_rects)):
                    if tube_rects[item].collidepoint(event.pos):
                        selected = True
                        select_rect = item
            else:
                for item in range(len(tube_rects)):
                    if tube_rects[item].collidepoint(event.pos):
                        dest_rect = item
                        tube_colors = calc_move(tube_colors,select_rect,dest_rect)
                        selected = False
                        select_rect = 100

    #draw Victory! Restart Message 
    if win:
        victory_text = font.render("You WIN!! Press Enter for a new Board!",True, 'white')
        screen.blit(victory_text,(30,265))
    restart_text = font.render("Stuck? Space-Restart, Enter-New Board",True,"white")
    screen.blit(restart_text,(10,10))

    
    pygame.display.flip()
pygame.quit()



