import gridMaker
import game

radius = 5

if __name__ == '__main__':
    hexgrid = gridMaker.grid_maker(radius)
    hexgrid = gridMaker.carthesian_calculator(hexgrid, 50)
    hexgrid = gridMaker.starting_ruby(hexgrid, radius)
    game.run(hexgrid)



