from typing import List, Dict

def get_pressed_status(event):
    result: Dict[str, List|str] = {}

    for part in str(event).split():

        if 'state=' in part:
            state_value: str = part.split('=')[1]
            state_value: str = state_value.rstrip('>')

            if '|' in state_value:
                result['state'] = state_value.split('|')

            elif state_value != '0x40000':
                result['state'] = [state_value]

        if 'keysym=' in part:
            key_value: str = part.split('=')[1]
            key_value: str = key_value.rstrip('>')
            result["key"] = key_value

    return result