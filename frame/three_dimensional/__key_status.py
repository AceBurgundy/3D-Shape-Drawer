from typing import Dict, List
from tkinter import Event

def get_key_status(event: Event):
    """
    Filters data returned by CTk Key Press event

    Arguments:
        event (Event): A Tkinter event object representing the key press event.
    """
    result: Dict[str, List|str] = {}

    for part in str(event).split():

        if 'state=' in part:
            state_value: str = part.split('=')[1]
            state_value = state_value.rstrip('>')

            if '|' in state_value:
                result['state'] = state_value.split('|')

            elif state_value != '0x40000' and state_value != 'Mod1':
                result['state'] = [state_value]

        if 'keysym=' in part:
            key_value: str = part.split('=')[1]
            key_value = key_value.rstrip('>')
            result["key"] = key_value

    return result
