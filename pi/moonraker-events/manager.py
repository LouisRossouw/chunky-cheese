from states.idle import IdleState
from states.printing import PrintingState
from states.heating import HeatingState

STATE_MAPPING = {
    'idle': IdleState,
    'printing': PrintingState,
    'heating': HeatingState,
    'ready': IdleState,
}

class LedManager:
    def __init__(self, renderer):
        self.renderer = renderer
        self.active_state_name = None
        self.active_state = None
        
        # Set default state of the lights
        self.set_state('idle')

    def set_state(self, state_name):
        if self.active_state_name == state_name:
            return

        print(f"LED Manager state transition: {self.active_state_name} -> {state_name}")
        self.active_state_name = state_name

        state_class = STATE_MAPPING.get(state_name, IdleState)
        self.active_state = state_class()
        self.active_state.apply(self)

    def segment(self, name):
        """Returns the segment associated with a name."""
        return self.renderer.segments.get(name)

    def update(self, state):
        # Retrieve printer state name (e.g. idle or printing)
        print_state = state.print_state.lower() if state.print_state else 'idle'
        
        # If printing, dynamically check if we are heating up to target temperatures
        if print_state == 'printing':
            is_heating_bed = state.target_heater_bed_temperature > 0 and state.heater_bed_temperature < (state.target_heater_bed_temperature - 2.0)
            is_heating_extruder = state.target_extruder_temperature > 0 and state.extruder_temperature < (state.target_extruder_temperature - 2.0)
            
            if is_heating_bed or is_heating_extruder:
                print_state = 'heating'
                
        self.set_state(print_state)


        
