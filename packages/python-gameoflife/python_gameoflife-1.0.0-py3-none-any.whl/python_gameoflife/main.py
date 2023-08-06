import random
import sys
import pygame


size = SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
DEAD_CELL_COLOR = 0, 0, 0
ALIVE_CELL_COLOR = 255, 255, 255
CELL_SIZE = 5
MAX_FPS = 15


class GameOfLife:
    def __init__(self):
        self.game_over = False
        pygame.init()
        self.game_field = pygame.display.set_mode(size)
        self.clear_game_field()
        self.active_grid = 0
        self.last_update_completed = 0
        self.num_rows = int(SCREEN_HEIGHT / CELL_SIZE)
        self.num_cols = int(SCREEN_WIDTH / CELL_SIZE)
        self.grids = []
        self.paused = False
        self.init_grids()
        self.desire_milli_between_updates = (1.0 / MAX_FPS) * 1000.0

    def clear_game_field(self):
        """
        fill the game field with dead color
        """
        self.game_field.fill(DEAD_CELL_COLOR)

    def init_grids(self):
        """
        map the screen into a 2d array
        """
        def create_grid():
            cols = []
            for col in range(self.num_cols):
                list_of_rows = [0] * self.num_rows
                cols.append(list_of_rows)
            return cols

        self.grids.append(create_grid())
        self.grids.append(create_grid())

        self.valuation_grids(None)

    def valuation_grids(self, value=None):
        """
        value=1 -> set all cells to 1
        value=0 -> set all cells to 0
        value=None -> randomize cell values
        """
        for col in range(self.num_cols):
            for row in range(self.num_rows):
                # randomize
                if value is None:
                    self.grids[self.active_grid][col][row] = random.choice([0, 1])
                else:
                    self.grids[self.active_grid][col][row] = value

    def draw_cells(self):
        """
        fill the grid with the alive cell color if its gonna be alive
        """
        self.clear_game_field()
        for col in range(self.num_cols):
            for row in range(self.num_rows):
                if self.grids[self.active_grid][col][row] == 1:
                    rect = pygame.Rect((col * CELL_SIZE, row * CELL_SIZE),
                                       (CELL_SIZE * .99, CELL_SIZE * .99))
                    pygame.draw.rect(self.game_field, ALIVE_CELL_COLOR, rect)

        pygame.display.flip()

    def check_cell_neighbours(self, row_index, col_index):
        """
        calculated cell neighbours status
        implemented conway's rules
        """
        def get_cell(g, r, c):
            cell_value = 0
            try:
                cell_value = g[r][c]
            except:
                pass
            return cell_value

        num_alive_neighbours = 0

        grid = self.grids[self.active_grid]
        num_alive_neighbours += get_cell(grid, row_index - 1, col_index - 1)
        num_alive_neighbours += get_cell(grid, row_index - 1, col_index)
        num_alive_neighbours += get_cell(grid, row_index - 1, col_index + 1)

        num_alive_neighbours += get_cell(grid, row_index, col_index - 1)
        num_alive_neighbours += get_cell(grid, row_index, col_index + 1)

        num_alive_neighbours += get_cell(grid, row_index + 1, col_index - 1)
        num_alive_neighbours += get_cell(grid, row_index + 1, col_index)
        num_alive_neighbours += get_cell(grid, row_index + 1, col_index + 1)

        if self.grids[self.active_grid][row_index][col_index] == 1:
            if num_alive_neighbours > 3:
                return 0
            if num_alive_neighbours < 2:
                return 0
            if num_alive_neighbours == 2 or num_alive_neighbours == 3:
                return 1

        elif self.grids[self.active_grid][row_index][col_index] == 0:
            if num_alive_neighbours == 3:
                return 1

        return self.grids[self.active_grid][row_index][col_index]

    def update_generation(self):
        for c in range(self.num_cols):
            for r in range(self.num_rows):
                self.grids[self.inactive_grid()][c][r] = self.check_cell_neighbours(c, r)

        self.active_grid = self.inactive_grid()

    def inactive_grid(self):
        """
        switch between grids
        """
        return (self.active_grid + 1) % 2

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.unicode == 'c':
                    self.valuation_grids(0)
                    self.clear_game_field()
                    self.draw_cells()

                if event.unicode == 's':
                    if self.paused:
                        self.paused = False
                    else:
                        self.paused = True

                elif event.unicode == 'r':
                    self.valuation_grids(None)
                    self.draw_cells()

                elif event.unicode == 'q':
                    self.game_over = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                left, middle, right = pygame.mouse.get_pressed()
                if left == 1:
                    click_pos_x, click_pos_y = pygame.mouse.get_pos()
                    clicked_cell_x_index = click_pos_x // CELL_SIZE
                    clicked_cell_y_index = click_pos_y // CELL_SIZE
                    if self.grids[self.active_grid][clicked_cell_x_index][clicked_cell_y_index] == 1:
                        self.grids[self.active_grid][clicked_cell_x_index][clicked_cell_y_index] = 0  # make it alive
                    else:
                        self.grids[self.active_grid][clicked_cell_x_index][clicked_cell_y_index] = 1
                    self.draw_cells()

            if event.type == pygame.QUIT:
                sys.exit()

    def limit_fps(self):
        now = pygame.time.get_ticks()
        milli_since_last_update = now - self.last_update_completed

        time_to_sleep = self.desire_milli_between_updates - milli_since_last_update
        if time_to_sleep > 0:
            pygame.time.delay(int(time_to_sleep))
        self.last_update_completed = now

    def run(self):
        """
        1- handle_events
        2- draw_cells
        3- update_generation
        """
        while True:
            if self.game_over:
                return

            self.handle_events()
            if self.paused:
                continue

            self.update_generation()
            self.draw_cells()
            self.limit_fps()


def main():
    game = GameOfLife()
    game.run()


if __name__ == '__main__':
    main()