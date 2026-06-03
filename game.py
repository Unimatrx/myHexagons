import pygame
import numpy as np
pygame.init()
screen = pygame.display.set_mode((1280, 900))
clock = pygame.time.Clock()
running = True


def run(hexgrid):
    hexgrid = hexgrid
    running = True
    player = "ruby"
    # player = switch_player(player)
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                mousepos = pygame.mouse.get_pos()
                player = find_hex(hexgrid, mousepos, player)

        screen.fill("white")

        draw_board(hexgrid)

        pygame.display.flip()

        clock.tick(60)



    pygame.quit()

def switch_player(player):
    if player == "ruby":
        player = "pearl"
    elif player == "pearl":
        player = "ruby"
    print(player)
    return player


def find_hex(hexgrid, mousepos, player):
    for hexagon in hexgrid:
        xdist = hexagon["carthesian"][0] - mousepos[0]
        ydist = hexagon["carthesian"][1] - mousepos[1]
        distance = np.sqrt(xdist ** 2 + ydist ** 2)
        if distance <= 50 * (1/2)*np.sqrt(3):
            # print(player)
            # print(hexagon["cubeidentifier"])
            if hexagon["state"] == "empty":
                clear_neighbours(hexgrid)
            elif hexagon["state"] == "ruby" or hexagon["state"] == "pearl":
                if hexagon["state"] == player:
                    clear_neighbours(hexgrid)
                    hexagon["waslast"] = 1
                    draw_neighbours(hexgrid, hexagon["cubeidentifier"])
            elif hexagon["state"] == "range1":
                make_token(hexgrid, hexagon["cubeidentifier"])
                player = switch_player(player)
            elif hexagon["state"] == "range2":
                jump_token(hexgrid, hexagon["cubeidentifier"])
                player = switch_player(player)
    return player

def make_token(hexgrid, target):
    for hexagon in hexgrid:
        if hexagon["waslast"] == 1:
            activecolor = hexagon["state"]
    # print(activecolor)
    for hexagon in hexgrid:
        if hexagon["cubeidentifier"] == target:
            hexagon["state"] = activecolor
    convert_neighbours(hexgrid, target, activecolor)
    for hexagon in hexgrid:
        hexagon["waslast"] = 0

    clear_neighbours(hexgrid)
    return hexgrid

def jump_token(hexgrid, target):
    for hexagon in hexgrid:
        if hexagon["waslast"] == 1:
            activecolor = hexagon["state"]
    # print(activecolor)
    for hexagon in hexgrid:
        if hexagon["cubeidentifier"] == target:
            hexagon["state"] = activecolor
        convert_neighbours(hexgrid, target, activecolor)
    for hexagon in hexgrid:
        if hexagon["waslast"] == 1:
            hexagon["state"] = "empty"
            hexagon["waslast"] = 0
    # convert_neighbours(hexgrid, target)
    clear_neighbours(hexgrid)
    return hexgrid


def find_neighbours(hexgrid, target):
    neighbours = [[1, -1, 0],
                  [1, 0, -1],
                  [0, 1, -1],
                  [0, -1, 1],
                  [-1, 1, 0],
                  [-1, 0, 1],
                  ]

    neighboursrange1 = []
    neighboursrange2 = []
    for neighbour in neighbours:
        neighboursrange1.append([x + y for x, y in zip(neighbour, target)])

    for hexagon in neighboursrange1:
        for neighbour in neighbours:
            neighbour_2 = [x + y for x, y in zip(neighbour, hexagon)]
            if (neighbour_2 not in neighboursrange2 and
                neighbour_2 not in neighboursrange1 and
                neighbour_2 != target):
                neighboursrange2.append(neighbour_2)
    return neighboursrange1, neighboursrange2

def draw_neighbours(hexgrid, target):
    neighboursrange1, neighboursrange2 = find_neighbours(hexgrid, target)
    for hexagon in hexgrid:
        if hexagon["state"] == "empty":
            if hexagon["cubeidentifier"] in neighboursrange1:
                hexagon["state"] = "range1"
            elif hexagon["cubeidentifier"] in neighboursrange2:
                hexagon["state"] = "range2"
            else:
                hexagon["color"] = "purple"
    return hexgrid

def convert_neighbours(hexgrid, target, activecolor):
    if activecolor == "ruby":
        inactivecolor = "pearl"
    elif activecolor == "pearl":
        inactivecolor = "ruby"
    neighboursrange1, neighboursrange2 = find_neighbours(hexgrid, target)
    for hexagon in hexgrid:
        if hexagon["cubeidentifier"] in neighboursrange1:
            if hexagon["state"] == inactivecolor:
                hexagon["state"] = activecolor
    return hexgrid


def clear_neighbours(hexgrid):
    for hexagon in hexgrid:
        if hexagon["state"] != "ruby" and hexagon["state"] != "pearl":
            hexagon["state"] = "empty"

def draw_board(hexgrid):
    for hexagon in hexgrid:
        if hexagon["state"] == "ruby":
            hexagon["color"] = "red"
        elif hexagon["state"] == "pearl":
            hexagon["color"] = "blue"
        elif hexagon["state"] == "range1":
            hexagon["color"] = "green"
        elif hexagon["state"] == "range2":
            hexagon["color"] = "yellow"
        else:
            hexagon["color"] = "purple"
        pygame.draw.polygon(screen, hexagon["color"], hexagon["points"], 0)
