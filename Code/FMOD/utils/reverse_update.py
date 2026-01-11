class reverse_trigger_handler:
    past_gear = None
    def oneshot_reverse_trigger(current_gear):
        val = None
        if current_gear == -1 and reverse_trigger_handler.past_gear == None:
            val = True
        elif current_gear == -1 and reverse_trigger_handler.past_gear !=-1:
            val = True
        elif current_gear == -1 and reverse_trigger_handler.past_gear == -1:
            val = False
        reverse_trigger_handler.past_gear = current_gear
        return val