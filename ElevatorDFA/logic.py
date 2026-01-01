from typing import Set, Optional
from collections import deque


class ElevatorDFA:
    """
    DFA-based Elevator Controller
    
    States Q = {q0, q1, q2, q3, q4} representing floors 0-4
    Alphabet Σ = {b0, b1, b2, b3, b4} representing button presses
    Transition function δ: Q × Σ → Q (sequential movement only)
    """
    
    def __init__(self):
        # State space Q
        self.states: Set[str] = {'q0', 'q1', 'q2', 'q3', 'q4'}
        
        # Alphabet Σ
        self.alphabet: Set[str] = {'b0', 'b1', 'b2', 'b3', 'b4'}
        
        # Current state (initial state q₀)
        self.current_state: str = 'q0'
        
        # Target queue for sequential movement
        self.target_queue: deque = deque()
        
        # Movement state
        self.is_moving: bool = False
        self.next_state: Optional[str] = None
        
    def get_floor_number(self, state: str) -> int:
        """Extract floor number from state notation (q0 -> 0)"""
        return int(state[1])
    
    def get_state_from_floor(self, floor: int) -> str:
        """Convert floor number to state notation (0 -> q0)"""
        return f'q{floor}'
    
    def process_input(self, input_symbol: str) -> bool:
        """
        Process input from alphabet Σ
        Returns True if input is accepted and queued
        """
        if input_symbol not in self.alphabet:
            return False
        
        #Extract target floor from button input (b0 -> 0)
        target_floor = int(input_symbol[1])
        target_state = self.get_state_from_floor(target_floor)
        
        current_floor = self.get_floor_number(self.current_state)
        
        #Checking statement
        if current_floor == target_floor:
            return False
        
        if target_state in self.target_queue:
            return False
        
        #Add to queue
        self.target_queue.append(target_state)
        
        #If not moving start movement(para mag start)
        if not self.is_moving:
            self._start_next_movement()
        
        return True
    
    def _start_next_movement(self):
        """Initialize movement to next target in queue"""
        if not self.target_queue:
            self.is_moving = False
            self.next_state = None
            return
        
        target_state = self.target_queue[0]
        current_floor = self.get_floor_number(self.current_state)
        target_floor = self.get_floor_number(target_state)
        
        # Determine next sequential state
        if target_floor > current_floor:
            # Move up one floor
            self.next_state = self.get_state_from_floor(current_floor + 1)
        elif target_floor < current_floor:
            # Move down one floor
            self.next_state = self.get_state_from_floor(current_floor - 1)
        
        self.is_moving = True
    
    def step(self) -> bool:
        """
        Execute one step of the DFA transition
        Returns True if a transition occurred
        """
        if not self.is_moving or self.next_state is None:
            return False
        
        # Perform transition(current_state, implicit_input) = next_state
        self.current_state = self.next_state
        
        # Check kung na abot na sa target
        if self.target_queue and self.current_state == self.target_queue[0]:
            self.target_queue.popleft()
            
            # If more targets exist, continue
            if self.target_queue:
                self._start_next_movement()
            else:
                self.is_moving = False
                self.next_state = None
        else:
            # 
            self._start_next_movement()
        
        return True
    
    def get_current_floor(self) -> int:
        """Get current floor number"""
        return self.get_floor_number(self.current_state)
    
    def get_target_floors(self) -> list:
        """Get list of queued target floors"""
        return [self.get_floor_number(state) for state in self.target_queue]
    
    def reset(self):
        """Reset DFA to initial state"""
        self.current_state = 'q0'
        self.target_queue.clear()
        self.is_moving = False
        self.next_state = None