import pygame
import sys
from logic import ElevatorDFA
# from assets import Elevator, DFAGraph (version 2 ginamit)

# Constants
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
FPS = 60 #not sure if nagana to

# Colors(para mas madali makita)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
DARK_GRAY = (80, 80, 80)
ELEVATOR_COLOR = (70, 130, 180)
BUTTON_COLOR = (100, 100, 250)
ACTIVE_STATE_COLOR = (255, 215, 0)
INACTIVE_STATE_COLOR = (200, 200, 200)
TEXT_COLOR = (50, 50, 50)

# Floor Y-coordinates (top to bottom)
FLOOR_COORDS = {
    4: 100,   # Floor 4 (top)
    3: 200,
    2: 300,
    1: 400,
    0: 500    # Floor 0 (bottom)
}

# Elevator shape
ELEVATOR_WIDTH = 70
ELEVATOR_HEIGHT = 70
ELEVATOR_X = 150

# Galaw
ELEVATOR_SPEED = 2.0  # pixels per frame


class ElevatorSimulation:
    """Main simulation controller integrating DFA logic with Pygame visualization"""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Elevator Simulation - DFA Architecture")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # DFA Engine
        self.dfa = ElevatorDFA()
        
        #ignore testing lang to
        # Elevator and DFA Graph Visuals
        # self.elevator = Elevator(ELEVATOR_X, list(FLOOR_COORDS.values()))
        # self.dfa_graph = DFAGraph(WINDOW_WIDTH // 2 + 200, list(FLOOR_COORDS.values())) Version 2 ginamit

        # Physical elevator position (continuous for smooth animation)
        self.elevator_y = float(FLOOR_COORDS[0])
        self.target_y = float(FLOOR_COORDS[0])
        
        # Button rectangles for click detection
        self.buttons = {}
        self._create_buttons()
        
        # DFA visualization
        self.state_positions = self._calculate_state_positions()
        
    def _create_buttons(self):
        """Create clickable button rectangles for each floor"""
        button_x = 50
        for floor in range(5):
            y = FLOOR_COORDS[floor]
            self.buttons[floor] = pygame.Rect(button_x, y - 20, 40, 40)
    
    def _calculate_state_positions(self):
        """Calculate positions for DFA state nodes on right side"""
        right_section_x = WINDOW_WIDTH // 2 + 200
        positions = {}
        
        # state position
        for floor in range(5):
            state = f'q{floor}'
            y = FLOOR_COORDS[floor]
            positions[state] = (right_section_x, y)
        
        return positions
    
    def handle_events(self):
        """Process user input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                
                # Check button clicks
                for floor, rect in self.buttons.items():
                    if rect.collidepoint(mouse_pos):
                        input_symbol = f'b{floor}'
                        self.dfa.process_input(input_symbol)
                        print(f"Button pressed: Floor {floor} (Input: {input_symbol})")
            
            if event.type == pygame.KEYDOWN:
                # Keyboard shortcuts
                if pygame.K_0 <= event.key <= pygame.K_4:
                    floor = event.key - pygame.K_0
                    input_symbol = f'b{floor}'
                    self.dfa.process_input(input_symbol)
                    print(f"Key pressed: Floor {floor} (Input: {input_symbol})")
                
                # R key to reset
                if event.key == pygame.K_r:
                    self.dfa.reset()
                    self.elevator_y = float(FLOOR_COORDS[0])
                    self.target_y = float(FLOOR_COORDS[0])
                    print("System reset to q0")
        
        return True
    
    def update(self):
        """Update physics and DFA state"""
        # Update target position based on DFA state
        current_floor = self.dfa.get_current_floor()
        self.target_y = float(FLOOR_COORDS[current_floor])
        
        # Animation movement
        if abs(self.elevator_y - self.target_y) > 0.5:
            if self.elevator_y < self.target_y:
                self.elevator_y += ELEVATOR_SPEED
            else:
                self.elevator_y -= ELEVATOR_SPEED
        else:
            self.elevator_y = self.target_y
            # Trigger DFA step
            self.dfa.step()
    
    def draw(self):
        """Render all visual elements"""
        self.screen.fill(WHITE)
        
        # Draw dividing line
        pygame.draw.line(self.screen, DARK_GRAY, 
                        (WINDOW_WIDTH // 2, 0), 
                        (WINDOW_WIDTH // 2, WINDOW_HEIGHT), 3)
        
        # Left side elevator
        self._draw_elevator_shaft()
        self._draw_elevator()
        self._draw_buttons()
        
        # Right side DFA state graph
        self._draw_dfa_graph()
        
        # Status information
        self._draw_status()
        
        pygame.display.flip()
    
    def _draw_elevator_shaft(self):
        """Draw the elevator shaft and floor markers"""
        shaft_left = ELEVATOR_X - 20
        shaft_right = ELEVATOR_X + ELEVATOR_WIDTH + 20
        
        # Shaft walls
        pygame.draw.line(self.screen, DARK_GRAY, 
                        (shaft_left, 50), (shaft_left, 550), 2)
        pygame.draw.line(self.screen, DARK_GRAY, 
                        (shaft_right, 50), (shaft_right, 550), 2)
        
        # Floor lines and labels(mga pangalan ng floors)
        for floor, y in FLOOR_COORDS.items():
            pygame.draw.line(self.screen, GRAY, 
                           (shaft_left, y), (shaft_right, y), 1)
            label = self.font.render(f"Floor {floor}", True, TEXT_COLOR)
            self.screen.blit(label, (shaft_right + 10, y - 15))
    
    def _draw_elevator(self):
        """Draw the elevator car"""
        rect = pygame.Rect(ELEVATOR_X, int(self.elevator_y) - ELEVATOR_HEIGHT // 2,
                          ELEVATOR_WIDTH, ELEVATOR_HEIGHT)
        pygame.draw.rect(self.screen, ELEVATOR_COLOR, rect)
        pygame.draw.rect(self.screen, BLACK, rect, 2)
    
    def _draw_buttons(self):
        """Draw call buttons for each floor"""
        for floor, rect in self.buttons.items():
            pygame.draw.rect(self.screen, BUTTON_COLOR, rect)
            pygame.draw.rect(self.screen, BLACK, rect, 2)
            
            # Button label
            label = self.small_font.render(str(floor), True, WHITE)
            label_rect = label.get_rect(center=rect.center)
            self.screen.blit(label, label_rect)
    
    def _draw_dfa_graph(self):
        """Draw the DFA state diagram"""
        node_radius = 40
        
        # Draw edges
        for i in range(4):
            state1 = f'q{i}'
            state2 = f'q{i+1}'
            pos1 = self.state_positions[state1]
            pos2 = self.state_positions[state2]
            pygame.draw.line(self.screen, GRAY, pos1, pos2, 2)
        
        # Draw state nodes
        for state, pos in self.state_positions.items():
            # Highlight current state(para mag yellow)
            if state == self.dfa.current_state:
                color = ACTIVE_STATE_COLOR
                pygame.draw.circle(self.screen, color, pos, node_radius + 5)
            else:
                color = INACTIVE_STATE_COLOR
            
            pygame.draw.circle(self.screen, color, pos, node_radius)
            pygame.draw.circle(self.screen, BLACK, pos, node_radius, 3)
            
            # State label
            label = self.font.render(state, True, BLACK)
            label_rect = label.get_rect(center=pos)
            self.screen.blit(label, label_rect)
    
    def _draw_status(self):
        """Draw status information"""
        status_y = WINDOW_HEIGHT - 80
        
        current_floor = self.dfa.get_current_floor()
        targets = self.dfa.get_target_floors()
        moving = "Moving" if self.dfa.is_moving else "Idle"
        
        status_text = f"Current: q{current_floor} (Floor {current_floor}) | Status: {moving}"
        if targets:
            status_text += f" | Targets: {targets}"
        
        status_surface = self.small_font.render(status_text, True, TEXT_COLOR)
        self.screen.blit(status_surface, (20, status_y))
        
        # Instructions o descriptions
        instructions = "Click buttons or press 0-4 keys | R to reset"
        instr_surface = self.small_font.render(instructions, True, TEXT_COLOR)
        self.screen.blit(instr_surface, (20, status_y + 30))
    
    def run(self):
        """Main game loop"""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()


def main():
    """Entry point"""
    sim = ElevatorSimulation()
    sim.run()


if __name__ == "__main__":
    main()