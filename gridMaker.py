import numpy as np

def grid_maker(radius):
    hexgrid = []
    rad = radius
    q = -rad
    r = -rad
    while q <= rad:
        r = -rad
        while r <= rad:
            s = -q - r
            if abs(s) <= rad:
                hexgrid.append({"cubeidentifier":[q, r, s]})
            r += 1
        q += 1

    return hexgrid

def carthesian_calculator(hexgrid, hexsize):
    hexpoints_modifier = [
                            [hexsize * 0, hexsize * 1],
                            [hexsize * float((1 / 2) * np.sqrt(3)), hexsize * (1 / 2)],
                            [hexsize * float((1 / 2) * np.sqrt(3)), hexsize * -(1 / 2)],
                            [hexsize * 0, hexsize * -1],
                            [hexsize * float(-(1 / 2) * np.sqrt(3)), hexsize * -(1 / 2)],
                            [hexsize * float(-(1 / 2) * np.sqrt(3)), hexsize * (1 / 2)],
                        ]


    size = 50
    for hexagon in hexgrid:
        hexagon["color"] = "purple"
        q = hexagon["cubeidentifier"][0]
        r = hexagon["cubeidentifier"][1]
        x = float((size * q * np.sqrt(3)) + (size * r * np.sqrt(3)/2)) + 720
        y = float((size * r * 3/2)) + 450
        cart = [x, y]
        hexagon["carthesian"] = cart
        # print(hexagon)
        points = []
        for mod in hexpoints_modifier:
            points.append([x + y for x, y in zip(cart, mod)])
        hexagon["points"] = points
        hexagon["state"] = "empty"
        hexagon["waslast"] = 0
        # print(hexagon)
    return hexgrid

def starting_ruby(hexgrid, radius):
    starting_rubies = [[-radius, radius, 0], [0, radius, -radius], [radius, 0, -radius]]
    starting_pearls = [[-radius, 0, radius], [0, -radius, radius], [radius, -radius, 0]]
    for hexagon in hexgrid:
        if hexagon["cubeidentifier"] in starting_rubies:
            hexagon["state"] = "ruby"
            # hexagon["color"] = "red"
        elif hexagon["cubeidentifier"] in starting_pearls:
            hexagon["state"] = "pearl"
            # hexagon["color"] = "blue"
        else:
            hexagon["state"] = "empty"
    return hexgrid
