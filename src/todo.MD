# MAIN TODOS OF SHORTCUT MAPPER

## CURRENT STATUS - 25.8.2024

	ANY KEY OR MOUSE EVENTS BLOCKED AFTER A HOTKEY IS USED...

	TIME IN RECORDED EVENTS - SHOULD BE RELATIVE / SPED UP 
		STEP SIZE

	HOW TO MAKE GUI BUILDING AND MANAGEMENT EASIER - PYTHON? 

	in same session seems to work for shortcut - but not the json loaded version
		compare 

		but the keyboard no longer works in the program? 

	error in deleting shortcuts



	CURRENT ERROR: 
	Mapping: =======================
        Shortcut:strg+f Action:alt,t,s
		Hotkey: strg+f
		Event: {'_type': 'KeyboardEvent', 'data': {'event_type': 'down', 'scan_code': 56, 'time': 1721745457.213577, 'device': None, 'is_keypad': False, 'modifiers': None, 'name': 'alt'}}
		Error in keyboard hook:
		Traceback (most recent call last):
		File "C:\Users\Cole\GitHub\SHORTCUT_MAPPER\src\keyboard\_winkeyboard.py", line 547, in low_level_keyboard_handler
			should_continue = process_key(event_type, vk, scan_code, is_extended)
							^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
		File "C:\Users\Cole\GitHub\SHORTCUT_MAPPER\src\keyboard\_winkeyboard.py", line 535, in process_key
			return callback(KeyboardEvent(event_type=event_type, scan_code=scan_code or -vk, name=name, is_keypad=is_keypad))
				^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
		File "C:\Users\Cole\GitHub\SHORTCUT_MAPPER\src\keyboard\__init__.py", line 282, in direct_callback
			callback(event) for callback in self.blocking_hotkeys[hotkey]
			^^^^^^^^^^^^^^^
		File "C:\Users\Cole\GitHub\SHORTCUT_MAPPER\src\keyboard\__init__.py", line 741, in <lambda>
			) or (event_type == e.event_type and callback())
												^^^^^^^^^^
		File "C:\Users\Cole\GitHub\SHORTCUT_MAPPER\src\keys.py", line 270, in hotkey_react
			keyboard.play(hotkey.events, speed_factor=5)
		File "C:\Users\Cole\GitHub\SHORTCUT_MAPPER\src\keyboard\__init__.py", line 1204, in play
			print("Time:", event.time)
						^^^^^^^^^^
		AttributeError: 'dict' object has no attribute 'time'


## NOTES

THE COMPLEX SHORTCUTS I HAVE CREATED DONT SEEM TO WORK - SEEMS TO NEED MORE OF A PAUSE BETWEEN STROKES

WHAT ABOUT RECORDING / THEN TRANSFORMING - ADDING JUST THE REQUIRED AMOUNT OF BUFFER - REDUCING UNNECESSARY STROKES


NEED TO ADD ABILITY TO IMPLEMENT PYTHON OR BATCH / PS FILES AFTER KEY SEQUENCES 

WHAT ABOUT MOUSE ACTIONS? 


## TODOS

DOCUMENT THE REQUIREMENTS OF THE APP 

ADD TESTS TO THE PROGRAM

LANGUAGE OF KEYBOARD - CAN LEAVE AS IS FOR NOW - DOESNT SUPPORT MULTI-LANGUAGE USERS

ADD NOTE TO SAVE SHORTCUTS ON THE SET PAGE / OR SAVE AUTOMATICALLY ON EACH CONFIRM OK 

compare text version of hotkey to recorded version - how to mimic / recreate

