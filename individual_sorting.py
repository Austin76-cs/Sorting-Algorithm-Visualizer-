import pygame
import sort_algos
import numpy as np
import time

pygame.init()

class DrawInformation:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    BACKGROUND_COLOR = WHITE

    GRADIENTS = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192),
    ]

    FONT = pygame.font.SysFont('comicsans', 20)
    LARGE_FONT = pygame.font.SysFont('comicsans', 30)
    SIDE_PAD = 100
    TOP_PAD = 175

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualization")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        if len(lst) > 0:
            self.min_val = min(lst)
            self.max_val = max(lst)
            self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
            
            if self.max_val == self.min_val:
                self.block_height_unit = 0
            else:
                self.block_height_unit = (self.height - self.TOP_PAD) / (self.max_val - self.min_val)
        self.start_x = self.SIDE_PAD // 2

def create_starting_list(n, min_val, max_val):
    return np.random.randint(low=min_val, high=max_val + 1, size=n).tolist()

def draw(draw_info, algo_name, ascending, elapsed_time, color_positions, sorting):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.BLACK)
    draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2, 5))
    
    # Controls
    if sorting:
        controls_text = "R - Reset | SPACE - Stop"
    else:
        controls_text = "R - Reset | SPACE - Start | A - Ascending | D - Descending"
    controls = draw_info.FONT.render(controls_text, 1, draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2, 55))

    sorting_keys1 = draw_info.FONT.render("I - Insertion | B - Bubble | M - Merge | Q - Quick | H - Heap", 1, draw_info.BLACK)
    draw_info.window.blit(sorting_keys1, (draw_info.width/2 - sorting_keys1.get_width()/2, 85))
    
    sorting_keys2 = draw_info.FONT.render("X - Radix | U - Bucket | S - Selection | C - Counting", 1, draw_info.BLACK)
    draw_info.window.blit(sorting_keys2, (draw_info.width/2 - sorting_keys2.get_width()/2, 110))
    
    time_text = draw_info.FONT.render(f"Time: {elapsed_time:.2f}s", 1, draw_info.BLACK)
    draw_info.window.blit(time_text, (10, 5))

    draw_list(draw_info, color_positions)
    pygame.display.update()

def draw_list(draw_info, color_positions):
    lst = draw_info.lst
    
    clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, 
                  draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
    pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        height_val = (val - draw_info.min_val) * draw_info.block_height_unit
        y = draw_info.height - height_val
        
        color = draw_info.GRADIENTS[i % 3]
        if i in color_positions:
            color = color_positions[i]
            
        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, height_val))

def main():
    pygame.init() 
    run = True
    clock = pygame.time.Clock()

    n = 50
    min_val = 0
    max_val = 100

    lst = create_starting_list(n, min_val, max_val)
    draw_info = DrawInformation(800, 600, lst)
    
    sorting = False
    ascending = True

    sorting_algorithm = sort_algos.bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None

    start_time = 0
    elapsed_time = 0
    color_positions = {}

    while run:
        clock.tick(180)

        if sorting:
            try:
                draw_info.lst, color_positions = next(sorting_algorithm_generator)
                elapsed_time = time.time() - start_time
            except StopIteration:
                sorting = False
                color_positions = {}
        
        # Pass sorting to the draw function
        draw(draw_info, sorting_algo_name, ascending, elapsed_time, color_positions, sorting)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_ESCAPE:
                return "exit" 
            elif event.key == pygame.K_r:
                lst = create_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False
                elapsed_time = 0
                color_positions = {}

            elif event.key == pygame.K_SPACE:
                if sorting: 
                    sorting = False
                    color_positions = {}
                else: # 
                    sorting = True
                    start_time = time.time()
                    sorting_algorithm_generator = sorting_algorithm(draw_info.lst, ascending)
                    
            # Only run when not sorting
            elif not sorting:
                if event.key == pygame.K_a:
                    ascending = True
                elif event.key == pygame.K_d:
                    ascending = False
                elif event.key == pygame.K_i:
                    sorting_algorithm = sort_algos.insertion_sort
                    sorting_algo_name = "Insertion Sort"
                elif event.key == pygame.K_b:
                    sorting_algorithm = sort_algos.bubble_sort
                    sorting_algo_name = "Bubble Sort"
                elif event.key == pygame.K_m:
                    sorting_algorithm = sort_algos.merge_sort
                    sorting_algo_name = "Merge Sort"
                elif event.key == pygame.K_q:
                    sorting_algorithm = sort_algos.quick_sort
                    sorting_algo_name = "Quick Sort"
                elif event.key == pygame.K_h:
                    sorting_algorithm = sort_algos.heap_sort
                    sorting_algo_name = "Heap Sort"
                elif event.key == pygame.K_x:
                    sorting_algorithm = sort_algos.radix_sort
                    sorting_algo_name = "Radix Sort"
                elif event.key == pygame.K_u:
                    sorting_algorithm = sort_algos.bucket_sort
                    sorting_algo_name = "Bucket Sort"
                elif event.key == pygame.K_s:
                    sorting_algorithm = sort_algos.selection_sort
                    sorting_algo_name = "Selection Sort"
                elif event.key == pygame.K_c:
                    sorting_algorithm = sort_algos.counting_sort
                    sorting_algo_name = "Counting Sort"
    
    pygame.quit()
    return "exit"

if __name__ == '__main__':
    main()