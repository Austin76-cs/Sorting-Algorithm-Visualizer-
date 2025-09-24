import pygame

class Launcher:
    def __init__(self):
        pygame.init()
        self.width = 600
        self.height = 400
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Sorting Algorithm Visualizer - Launcher")
        
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.BLUE = (0, 0, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.GRAY = (128, 128, 128)
        
        self.LARGE_FONT = pygame.font.SysFont('comicsans', 36)
        self.FONT = pygame.font.SysFont('comicsans', 24)
        self.SMALL_FONT = pygame.font.SysFont('comicsans', 16)
        
        self.options = [
            ("Individual Algorithm Visualization", "individual_sorting.py"),
            ("Algorithm Comparison Mode", "algorithm_comparison.py"),
            ("Exit", None)
        ]
        
        self.selected_option = 0
        
    def draw(self):
        self.window.fill(self.WHITE)
        
        title = self.LARGE_FONT.render("Sorting Algorithm Visualizer", 1, self.BLACK)
        self.window.blit(title, (self.width/2 - title.get_width()/2, 50))
        
        subtitle = self.FONT.render("Choose a mode:", 1, self.BLACK)
        self.window.blit(subtitle, (self.width/2 - subtitle.get_width()/2, 100))
        
        # Draw menu options
        for i, (option_text, _) in enumerate(self.options):
            color = self.BLUE if i == self.selected_option else self.BLACK
            text = self.FONT.render(option_text, 1, color)
            x = self.width/2 - text.get_width()/2
            y = 150 + i * 50
            self.window.blit(text, (x, y))
            
            # Draw arrow for selected option
            if i == self.selected_option:
                arrow = self.FONT.render(">", 1, self.BLUE)
                self.window.blit(arrow, (x - 30, y))
        
        instructions = [
            "Use UP/DOWN arrows to navigate",
            "Press ENTER to select",
            "Press ESC to exit"
        ]
        
        for i, instruction in enumerate(instructions):
            text = self.SMALL_FONT.render(instruction, 1, self.GRAY)
            self.window.blit(text, (20, self.height - 80 + i * 20))
        
        pygame.display.update()
    
    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self.options[self.selected_option][1]
            elif event.key == pygame.K_ESCAPE:
                return "exit"
        return None
    
    def run(self):
        while True:
            clock = pygame.time.Clock()
            running = True
            
            while running:
                clock.tick(300)
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    else:
                        result = self.handle_events(event)
                        if result == "exit":
                            return  # Exit the entire launcher
                        elif result:
                            # Launch the selected program
                            pygame.quit()
                            if result == "individual_sorting.py":
                                import individual_sorting
                                individual_sorting.main()  # This will return "exit" when ESC is pressed
                            elif result == "algorithm_comparison.py":
                                import algorithm_comparison
                                algorithm_comparison.main()
                            # Return to launcher after program exits
                            pygame.init()
                            self.__init__()
                            break  # Break out of inner loop to restart launcher
                
                if running:
                    self.draw()
            
            if not running:
                break
        
        pygame.quit()

if __name__ == '__main__':
    launcher = Launcher()
    launcher.run()
