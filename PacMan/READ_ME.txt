LAST UPDATED: 28-02-2022

User manual
===================
Controls:
	Menus:
		Moving Up 		[W/Arrow Up]

		Moving Down 	[S/Arrow Down]

		Confirm 		[Enter/Spacebar]
			Used to select options in menus

		Cancel/Back		[ESC]
			Cancel in main menu closes the program
			In different menu, returns you back to main menu

		Toggle Fullscreen [F11]
			Screen turns black for a second but everything works fine.
	Game:
		Moving Up 		[W/Arrow Up]
		Moving Down 	[S/Arrow Down]
		Moving Left 	[A/Arrow Left]
		Moving Right 	[D/Arrow Right]

		Quit [ESC]
			Returns you back to main menu and saves your current score into highscores file.

		Toggle Fullscreen [F11]
			Screen turns black for a second but everything works fine.


???		Controller controls, I implemented controls for XBOX360 controller. Other controllers are not currently supported.
		Movement 		[Left Joistic]
		Moving Up 		[Arrow Up]
		Moving Down 	[Arrow Down]
		Moving Left 	[Arrow Left]
		Moving Right 	[Arrow Right]
		Confirm		[A]
		Cancel		[B]

Special notes:
	Settings menu is just visual, pressing Enter sends you back to main menu on purpose.
	Highscores in menu does nothing, highscore.txt file, keeps track of all your scores. So you can check your highscores there.

	Currently there are only 4 levels that rotate in a cycle. Level 1 -> 2 -> 3 -> 4 -> 1... and so on.
	I wanted to add more levels. I made a quite nice and easy system for creating levels. I will explain further down.

	Pink Ghost was meant to go a bit slower but I became lazy and unmotivaded to do it.
	Ghosts were done in a hurry and are not very smart.
	Ghost that spawn in levels is random, making it more interesting.

	I want to create a "Campaign" basically a level selection where player gets 0-3 stars based on how well he performs in each level.
	And endless mode which would be very similar to current state of the game but more random.

???	Even though this is only school project I might continue and fix these mistakes later on.


Ghosts:
	Chaser:
		Red ghost, switches between chasing the player and being scatter (going to upper left corner)
	Charger:
		Green ghost, always chases but after few seconds falls asleep. After waking up he starts charging again. (I love this one)
	Smart Ass:
		Blue ghost, tries to predict where the player will go and go there. (He suffered the most from the rushed development)
	Lazy Chaser:
		Pink ghost, always chases. In later versions I would like to halve his speed (More info in programmer manual)
		Lazy stands for both his speed and his creation :)



Programmer manual
===================
I wanted to make it even better but when I got past 1000 lines I decided to pause it there.
I tried to comment all over the programm, even rewrote entire program twice in order to make in easier to read.
I am unsure about parts that I did recently since they were felt a bit rushed but I didn't abandon commenting.

I don't plan on explaining how pygame works, but my use in this program is not very difficult and I hope my explanation will be enough.
Structure of the program:
	Imports and pygame init
	Few constants
	Classes:
		Char (Characters, player and ghosts templates, contains moving methods, visual methods, basically everything that both ghosts and player need)
		Player (Keeps everything needed for player here, player inputs during game, pacman visuals)
		Ghosts (General template for ghost)
		Chaser (Variation of the ghost)
		SmartAss (Variation of the ghost)
		Charger (Variation of the ghost)
		LazyChaser (Variation of the ghost)
		Map (Used to create map and keep all Surfaces needed to draw level properly together)
		Menu (Used to keep all information about certain menu in one place and lots of useful methods for menu creation and player input in menus)
		PopUpMenu (NOT USED CURRENTLY, It is not finished, idea was to ask player if he really wants to quit or save highscore)
		InfoSurface (Used for showing level name, player lives and score during game)
	Functions:
		check_controlers(When controller gets disconnected or new controller connected you have to redo init of all controllers)
		load_settings(Reads misc\settings.txt file and fills variables with proper values)
		calculate_variables(Used after loading in order to calculate remaining variables needed to run the program)
		respawn (Respawns player and ghosts, used in game function)
		menu (Takes Menu object and runs in loop, most menu related are in Menu class, menu function returns integer based on what player chooses)
		game (Prepares map, player, ghosts for current level, depending on index given to it, checks for input, draws characters, display them, remove them after so the traces don't remain)
	Variable Declarations
	Main loop

How program operates:
	First thing we do is read misc\settings.txt file (I wanted to allow player change resolution in settings menu, that is why explicit file exists)
	Declare all global variables
	Prepare the window, changing window icon, changin icon name
	
	Create menus, main menu and settings menu
	Launch the main loop
	Which starts the menu function of main menu
	If player chooses to go into settings menu:
		Start menu function of settings menu
		There is nothing much here, I didn't implement change of settings yet
	If player chooses to quit:
		Just exit the program
	If player chooses to play the game launch game function:
		Prepare map, player, ghosts for current level
		Starts game loop