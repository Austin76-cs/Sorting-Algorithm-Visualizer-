import pygame
import sort_algos
import numpy as np
import time
import threading
from collections import defaultdict

class ComparisonMode:
    def __init__(self, width, height):
        self.width = width
        self.height = height + 100 
        self.window = pygame.display.set_mode((width, self.height))
        pygame.display.set_caption("Sorting Algorithm Comparison")
        
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)
        self.PURPLE = (128, 0, 128)
        self.ORANGE = (255, 165, 0)
        self.CYAN = (0, 255, 255)
        self.PINK = (255, 192, 203)
        
        self.algorithm_colors = {
            'Bubble Sort': self.RED,
            'Insertion Sort': self.GREEN,
            'Merge Sort': self.BLUE,
            'Quick Sort': self.YELLOW,
            'Heap Sort': self.PURPLE,
            'Radix Sort': self.ORANGE,
            'Bucket Sort': self.CYAN,
            'Selection Sort': self.PINK,
            'Counting Sort': (255, 100, 100)  # Light red
        }
        
        self.FONT = pygame.font.SysFont('comicsans', 16)
        self.LARGE_FONT = pygame.font.SysFont('comicsans', 24)
        self.SMALL_FONT = pygame.font.SysFont('comicsans', 12)
        
        self.algorithms = {
            'Bubble Sort': sort_algos.bubble_sort,
            'Insertion Sort': sort_algos.insertion_sort,
            'Merge Sort': sort_algos.merge_sort,
            'Quick Sort': sort_algos.quick_sort,
            'Heap Sort': sort_algos.heap_sort,
            'Radix Sort': sort_algos.radix_sort,
            'Bucket Sort': sort_algos.bucket_sort,
            'Selection Sort': sort_algos.selection_sort,
            'Counting Sort': sort_algos.counting_sort
        }
        
        # State : Start at array size 50 with 0-1000 ranged
        self.array_size = 50  
        self.min_val = 0
        self.max_val = 1000
        self.running = False
        self.completed_algorithms = set()
        self.timing_data = defaultdict(list)
        self.current_times = {}  
        self.start_time = 0
        
        # Create initial array
        self.reset_array()
        
    def reset_array(self):
        self.lst = np.random.randint(low=self.min_val, high=self.max_val + 1, size=self.array_size).tolist()
        self.completed_algorithms = set()
        self.current_times = {}
        self.running = False
        
    def run_algorithm(self, algorithm_name, algorithm_func, lst):
        start_time = time.time()
        try:
            step_count = 0
            for step_lst, color_positions in algorithm_func(lst, True):  # Always ascending
                if not self.running:  # Check if we should stop
                    break
                step_count += 1
                # Update every 2 steps
                if step_count % 2 == 0:
                    current_time = time.time() - start_time
                    self.current_times[algorithm_name] = current_time
                    self.timing_data[algorithm_name].append(current_time)
                    time.sleep(0.00001)

        except Exception as e:
            print(f"Error in {algorithm_name}: {e}")
        finally:
            self.completed_algorithms.add(algorithm_name)
            
    def start_comparison(self):
        if self.running:
            return
            
        self.running = True
        self.completed_algorithms = set()
        self.current_times = {}
        self.timing_data = defaultdict(list)
        self.start_time = time.time()
        
        # Start each algorithm in its own thread
        threads = []
        for name, func in self.algorithms.items():
            thread = threading.Thread(
                target=self.run_algorithm,
                args=(name, func, self.lst.copy())
            )
            thread.daemon = True
            thread.start()
            threads.append(thread)
    
    def stop_comparison(self):
        self.running = False
        
    def draw(self):
        self.window.fill(self.WHITE)
        
        title = self.LARGE_FONT.render("Sorting Algorithm Comparison", 1, self.BLACK)
        self.window.blit(title, (self.width/2 - title.get_width()/2, 10))
        
        # Controls
        controls_text = "R - Reset | SPACE - Start/Stop | +/- - Array Size (±50) | ,/. - Max Value (±100)"
        controls = self.FONT.render(controls_text, 1, self.BLACK)
        self.window.blit(controls, (self.window.get_width()/2 - controls.get_width()/2, 50))
        
        # Array size display
        size_text = self.FONT.render(f"Array Size: {self.array_size}", 1, self.BLACK)
        self.window.blit(size_text, (10, 80))
        
        # Range display
        range_text = self.FONT.render(f"Range: {self.min_val}-{self.max_val}", 1, self.BLACK)
        self.window.blit(range_text, (10, 110))
        
        # Status
        status = "Running" if self.running else "Stopped"
        status_text = self.FONT.render(f"Status: {status}", 1, self.BLACK)
        self.window.blit(status_text, (10, 125))
        
        # Draw timing chart
        self.draw_timing_chart()
        
        # Draw algorithm status
        self.draw_algorithm_status()
        
        pygame.display.update()
    
    def draw_timing_chart(self):
        """Draw a simple timing chart"""
        chart_x = 10
        chart_y = 150
        chart_width = self.width - 20
        chart_height = 400  
        
        # Draw chart background
        pygame.draw.rect(self.window, (240, 240, 240), (chart_x, chart_y, chart_width, chart_height))
        pygame.draw.rect(self.window, self.BLACK, (chart_x, chart_y, chart_width, chart_height), 2)
        
        # Draw axes
        pygame.draw.line(self.window, self.BLACK, (chart_x, chart_y + chart_height), (chart_x + chart_width, chart_y + chart_height), 2)
        pygame.draw.line(self.window, self.BLACK, (chart_x, chart_y), (chart_x, chart_y + chart_height), 2)
        
        #Draw timing lines for each algorithm
        if self.timing_data:
            max_time = max(max(times) for times in self.timing_data.values()) if any(self.timing_data.values()) else 1
            max_time = max(max_time, 0.1)  # Avoid division by zero
            
            for i, (algorithm, times) in enumerate(self.timing_data.items()):
                if not times:
                    continue
                    
                color = self.algorithm_colors.get(algorithm, self.BLACK)
                
                # Draw timing line
                for j in range(1, len(times)):
                    x1 = chart_x + (j - 1) * chart_width / max(len(times) - 1, 1)
                    y1 = chart_y + chart_height - (times[j - 1] / max_time) * chart_height
                    x2 = chart_x + j * chart_width / max(len(times) - 1, 1)
                    y2 = chart_y + chart_height - (times[j] / max_time) * chart_height
                    pygame.draw.line(self.window, color, (x1, y1), (x2, y2), 2)
        
        # Chart labels
        chart_title = self.FONT.render("Execution Time (seconds)", 1, self.BLACK)
        self.window.blit(chart_title, (chart_x + chart_width/2 - chart_title.get_width()/2, chart_y - 25))
    
    def draw_algorithm_status(self):
        """Draw the status of each algorithm"""
        start_x = 10
        start_y = 570 
        
        for i, (algorithm, color) in enumerate(self.algorithm_colors.items()):
            y_pos = start_y + i * 25 
            
            # Algo name
            pygame.draw.rect(self.window, color, (start_x, y_pos, 20, 20))
            name_text = self.FONT.render(algorithm, 1, self.BLACK)
            self.window.blit(name_text, (start_x + 30, y_pos + 2))
            
            # Current time
            if algorithm in self.current_times:
                time_text = f"{self.current_times[algorithm]:.3f}s"
            elif algorithm in self.completed_algorithms:
                time_text = "Completed"
            else:
                time_text = "Waiting"
                
            time_display = self.FONT.render(time_text, 1, self.BLACK)
            self.window.blit(time_display, (start_x + 200, y_pos + 2))
            
            # Status indicator
            if algorithm in self.completed_algorithms and self.running:
                status_color = self.GREEN
            elif algorithm in self.current_times:
                status_color = self.YELLOW
            else:
                status_color = self.RED
                
            pygame.draw.circle(self.window, status_color, (start_x + 350, y_pos + 10), 8)
    
    def handle_events(self, event):
        #Handle user input events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "exit"
            elif event.key == pygame.K_r:
                self.reset_array()
            elif event.key == pygame.K_SPACE:
                if self.running:
                    self.stop_comparison()
                else:
                    self.start_comparison()
            elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                self.array_size = min(self.array_size + 50, 3000)  # 50 increment
                if not self.running:
                    self.reset_array()
            elif event.key == pygame.K_MINUS:
                self.array_size = max(self.array_size - 50, 50)  # 50 decrement
                if not self.running:
                    self.reset_array()
            elif event.key == pygame.K_COMMA:
                self.max_val = max(100, self.max_val - 100)  # Decrease max value by 100, minimum 100
                if not self.running:
                    self.reset_array()
            elif event.key == pygame.K_PERIOD:
                self.max_val = min(10000, self.max_val + 100)  # Increase max value by 100, maximum 10000
                if not self.running:
                    self.reset_array()

def main():
    pygame.init()
    clock = pygame.time.Clock()
    
    comparison = ComparisonMode(1000, 800) 
    running = True
    
    frame_count = 0
    while running:
        clock.tick(180) #tick rate
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                result = comparison.handle_events(event)
                if result == "exit":
                    running = False
        
        frame_count += 1
        if frame_count % 2 == 0:
            comparison.draw()
    
    pygame.quit()

if __name__ == '__main__':
    main()
