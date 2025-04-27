from tkinter import *
from tkinter import Tk, PhotoImage, Label, Button
from tkinter import font
import random
import json
import os

WIDTH = 800
HEIGHT = 600
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
ENEMY_WIDTH = 40
ENEMY_HEIGHT = 40
BULLET_WIDTH = 5
BULLET_HEIGHT = 15

class galaxy_attack:
    def __init__(self, root):
        self.root = root
        self.remapping = False 
        self.remap_key = None
        
        self.running = False
        self.score = 0
        self.intruders = []
        self.bullets = []
        self.pause = False
        self.boss_key_ = False 
        self.player_name = None

        self.leaderboard = []
        self.leaderboard_file = "leaderboard.json"
        self.load_leaderboard()
        
        self.cheat_code = ['Up', 'Down']
        self.cc_input = []
        self.player_safe = False
        self.cheat_on = False

        self.difficulty_level = 1
        self.intruder_no = 0.01
        self.intruder_Speed = 3
        
        # Load images safely with error handling
        self.load_images()
        
        self.key_map = {
            'left': 'Left',
            'right': 'Right',
            'shoot': 'space',
            'pause': 'Tab',
            'up_cheat': 'Up',
            'down_cheat': 'Down',
        }
        
        self.load_key_mappings()
    
    def load_images(self):
        try:
            # Use relative paths or resource paths
            script_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Create fallback images if originals can't be loaded
            self.create_fallback_images()
            
            try:
                # Try to load original images from predefined locations
                self.shooter = self.load_image("shooter.png", 7)
                self.intruder = self.load_image("intruder.png", 14)
                self.bullet_shape = self.load_image("bullet.png", 10, zoom=2)
                self.pause_image = self.load_image("pause.png", 20)
                self.resume_image = self.load_image("resume.png", 5)
                self.work_screen = self.load_image("work_page.png", 1)
                self.bg = self.load_image("background.png", 1)
            except Exception as e:
                print(f"Error loading images: {e}")
                print("Using fallback images instead")
        except Exception as e:
            print(f"Error in image loading: {e}")
            self.create_fallback_images()
    
    def load_image(self, filename, subsample_factor, zoom=1):
        """Tries to load an image and handles errors"""
        try:
            # Try direct path first
            if os.path.exists(filename):
                img = PhotoImage(file=filename)
            else:
                # Try common directories
                common_dirs = [".", "images", "assets", "resources"]
                found = False
                for directory in common_dirs:
                    path = os.path.join(directory, filename)
                    if os.path.exists(path):
                        img = PhotoImage(file=path)
                        found = True
                        break
                
                if not found:
                    # If image not found in any default locations, use fallback
                    print(f"Could not find {filename}. Using fallback image.")
                    return self.fallback_images[filename.split('.')[0]]
            
            # Apply subsample and zoom
            img = img.subsample(subsample_factor, subsample_factor)
            if zoom > 1:
                img = img.zoom(zoom, zoom)
            return img
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            return self.fallback_images[filename.split('.')[0]]
    
    def create_fallback_images(self):
        """Creates basic fallback images if originals can't be loaded"""
        self.fallback_images = {}
        
        # Create a simple canvas for each fallback image
        canvas = Canvas(width=50, height=50)
        
        # Player ship fallback (red triangle)
        canvas.create_polygon(25, 0, 0, 50, 50, 50, fill="red")
        self.fallback_images["shooter"] = PhotoImage(canvas.postscript(colormode='color'))
        
        # Enemy fallback (green circle)
        canvas.delete("all")
        canvas.create_oval(5, 5, 45, 45, fill="green")
        self.fallback_images["intruder"] = PhotoImage(canvas.postscript(colormode='color'))
        
        # Bullet fallback (yellow rectangle)
        canvas.delete("all")
        canvas.create_rectangle(20, 10, 30, 40, fill="yellow")
        self.fallback_images["bullet"] = PhotoImage(canvas.postscript(colormode='color'))
        
        # Pause button fallback
        canvas.delete("all")
        canvas.create_rectangle(10, 10, 20, 40, fill="white")
        canvas.create_rectangle(30, 10, 40, 40, fill="white")
        self.fallback_images["pause"] = PhotoImage(canvas.postscript(colormode='color'))
        
        # Resume button fallback
        canvas.delete("all")
        canvas.create_polygon(10, 10, 10, 40, 40, 25, fill="white")
        self.fallback_images["resume"] = PhotoImage(canvas.postscript(colormode='color'))
        
        # Background fallback (black)
        canvas.config(width=WIDTH, height=HEIGHT)
        canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill="black")
        self.fallback_images["background"] = PhotoImage(canvas.postscript(colormode='color'))
        
        # Work screen fallback
        canvas.create_text(WIDTH//2, HEIGHT//2, text="WORK SCREEN", fill="white", font=("Arial", 20))
        self.fallback_images["work_page"] = PhotoImage(canvas.postscript(colormode='color'))
        
        canvas.destroy()
    
    def settings_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.canvas = Canvas(self.root, width=WIDTH, height=HEIGHT, bg="blue")
        self.canvas.pack()
        self.canvas.create_image(0, 0, image=self.bg, anchor="nw")

        self.canvas.create_text(
            WIDTH // 2,
            HEIGHT // 2 - 250,
            text="KEY REMAPPING",
            fill="white",
            font=("copperplate", 25),
            anchor="center"
        )

        # This function is revised for better key remapping
        def bind_key(key_name):
            self.remapping = True
            self.remap_key = key_name
            
            remap_text = self.canvas.create_text(
                WIDTH // 2,
                HEIGHT // 2 - 200,
                text=f"Press new key for {key_name}",
                fill="white",
                font=("copperplate", 20),
                anchor="center",
                tags="remap_text"
            )
            
            def on_key_press(event):
                if self.remapping and self.remap_key == key_name:
                    new_key = event.keysym
                    
                    # Update key_map with new key
                    self.key_map[key_name] = new_key
                    print(f"Key for {key_name} remapped to: {new_key}")
                    
                    # Save key mappings
                    self.save_key_mappings()
                    
                    # Reset remapping state
                    self.remapping = False
                    self.remap_key = None
                    
                    # Unbind the temporary key press handler
                    self.root.unbind("<KeyPress>")
                    
                    # Reload settings menu
                    self.settings_menu()
            
            # Bind temporary key press handler
            self.root.bind("<KeyPress>", on_key_press)
    
        # Show current key mappings and allow remapping
        for i, (action, key) in enumerate(self.key_map.items()):
            self.canvas.create_text(
                WIDTH // 2,
                HEIGHT // 2 - 160 + i * 30,
                text=f"{action.capitalize()}: {key}",
                fill="white",
                font=("copperplate", 20),
                anchor="center"
            )
        
            remap_button = Button(
                self.root,
                text=f"Remap {action.capitalize()}",
                command=lambda action=action: bind_key(action),
                font=("copperplate", 15),
                fg="red",
                bg="black"
            )
            remap_button.place(x=WIDTH // 2 - 100, y=HEIGHT // 2 + 50 + i * 40)

        back_button = Button(
            self.root,
            text="BACK",
            command=self.main_menu,
            font=("copperplate", 20),
            fg="red",
            bg="black"
        )
        back_button.place(x=WIDTH // 2+250, y=HEIGHT - 100)

    def load_leaderboard(self):
        try:
            with open(self.leaderboard_file, 'r') as file:
                self.leaderboard = json.load(file)

            if not isinstance(self.leaderboard, list):
                self.leaderboard = []

        except(FileNotFoundError, json.JSONDecodeError):
            self.leaderboard = []
            self.leaderboard_save()

    def leaderboard_save(self):
        # Filter out invalid entries
        self.leaderboard = [
            entry for entry in self.leaderboard
            if isinstance(entry, dict) and 'name' in entry and 'score' in entry 
            and isinstance(entry['score'], (int, float))
        ]
        
        # Sort the leaderboard by score
        self.leaderboard.sort(key=lambda x: x['score'], reverse=True)
        
        # Save to file
        try:
            with open(self.leaderboard_file, 'w') as file:
                json.dump(self.leaderboard, file)
        except Exception as e:
            print(f"Error saving leaderboard: {e}")

    def game_start(self, player_name=None):
        if player_name:
            self.player_name = player_name

        # Clearing out every widget in the frame
        for widget in self.root.winfo_children():
            widget.destroy()

        self.canvas = Canvas(self.root, width=WIDTH, height=HEIGHT)
        self.canvas.pack()
        
        # Create background
        self.canvas.create_image(0, 0, image=self.bg, anchor="nw")
       
        # Create player
        self.player = self.canvas.create_image(
             WIDTH // 2,
             HEIGHT - PLAYER_HEIGHT - 15,
             image=self.shooter,
             anchor="center"
        )
        
        # Create pause button
        self.pause_button = Button(
            self.root,
            image=self.pause_image,
            command=self.press_pause,
            padx=10,
            pady=10,
            bd=0,
            bg="black",
            relief="flat"
        )
        
        self.pause_button.place(x=WIDTH - 60, y=10)

        # Game variables
        self.player_speed = 50
        self.intruder_Speed = 3
       
        # Bind keys using the key_map
        self.bind_game_keys()

        # Reset game state
        self.running = True
        self.score = 0
        self.intruders = []
        self.bullets = []
        self.update_score()

        # Start game loop
        self.game_update()
    
    def bind_game_keys(self):
        """Bind all game control keys based on key_map"""
        # First unbind any existing bindings
        for action, key in self.key_map.items():
            self.root.unbind(f"<{key}>")
        
        # Now bind the current mappings
        self.root.bind(f"<{self.key_map['left']}>", self.move_left)
        self.root.bind(f"<{self.key_map['right']}>", self.move_right)
        self.root.bind(f"<{self.key_map['shoot']}>", self.shoot)
        self.root.bind(f"<{self.key_map['pause']}>", self.boss_key)
        self.root.bind(f"<{self.key_map['up_cheat']}>", self.up_cheat_key)
        self.root.bind(f"<{self.key_map['down_cheat']}>", self.down_cheat_key)

    def up_cheat_key(self, event):
        self.cc_input.append('Up')
        self.check_cheat_code()

    def down_cheat_key(self, event):
        self.cc_input.append('Down')
        self.check_cheat_code()

    def move_left(self, event):  
        if self.running and not self.pause:
            x, y = self.canvas.coords(self.player)
            if (x - self.player_speed > PLAYER_WIDTH // 2):
                self.canvas.move(self.player, -self.player_speed, 0)

    def move_right(self, event):
        if self.running and not self.pause:
            x, y = self.canvas.coords(self.player)
            if (x + self.player_speed < WIDTH - PLAYER_WIDTH // 2):
                self.canvas.move(self.player, self.player_speed, 0)

    def shoot(self, event):
        if self.running and not self.pause:
            x, y = self.canvas.coords(self.player)
            bullet = self.canvas.create_image(
                x,
                y - BULLET_HEIGHT,
                image=self.bullet_shape,
                anchor="center"
            )
            self.bullets.append(bullet)
        
    def intruder_img(self):
        if self.running and not self.pause:
            x = random.randint(ENEMY_WIDTH // 2, WIDTH - ENEMY_WIDTH // 2)
            intruder = self.canvas.create_image(
                x,
                0,
                image=self.intruder,
                anchor="center"
            )
            self.intruders.append(intruder)

    def press_pause(self):
        if self.pause:
            self.pause = False
            self.pause_button.config(image=self.pause_image)
            self.game_update()
        else:
            self.pause = True
            self.pause_button.config(image=self.resume_image)

    def boss_key(self, event):
        if self.boss_key_:
            self.boss_key_ = False
            self.pause = False
            
            # Show all game elements
            self.canvas.itemconfig(self.player, state="normal")
            for intruder in self.intruders:
                self.canvas.itemconfig(intruder, state="normal")
            for bullet in self.bullets:
                self.canvas.itemconfig(bullet, state="normal")
            
            # Remove work screen
            self.canvas.delete(self.work_screen_)
            self.game_update()
        else:
            self.boss_key_ = True
            self.pause = True
            
            # Hide all game elements
            self.canvas.itemconfig(self.player, state="hidden")
            for intruder in self.intruders:
                self.canvas.itemconfig(intruder, state="hidden")
            for bullet in self.bullets:
                self.canvas.itemconfig(bullet, state="hidden")
            
            # Show work screen
            self.work_screen_ = self.canvas.create_image(
                WIDTH // 2,
                HEIGHT // 2,
                image=self.work_screen,
                anchor="center"
            )

    def check_cheat_code(self):
        # Limit input sequence length
        if len(self.cc_input) > len(self.cheat_code):
            self.cc_input = self.cc_input[-len(self.cheat_code):]
        
        # Check if sequence matches cheat code
        if self.cc_input == self.cheat_code:
            self.cheat_on = True
            self.player_safe = True
            self.cc_input = []
            print("POWER MODE ACTIVATED")
            
            # Visual feedback for cheat activation
            cheat_text = self.canvas.create_text(
                WIDTH // 2, 
                HEIGHT // 2, 
                text="POWER MODE ACTIVATED!", 
                font=("Arial", 24, "bold"), 
                fill="yellow"
            )
            self.root.after(1000, lambda: self.canvas.delete(cheat_text))

        # Schedule deactivation
        self.root.after(6000, self.deactivate_cheat_code)

    def deactivate_cheat_code(self):
        if self.cheat_on:
            self.cheat_on = False
            self.player_safe = False
            print("Cheat code deactivated")
            
            # Visual feedback for deactivation
            if hasattr(self, 'canvas') and self.canvas.winfo_exists():
                deactivate_text = self.canvas.create_text(
                    WIDTH // 2, 
                    HEIGHT // 2, 
                    text="POWER MODE DEACTIVATED", 
                    font=("Arial", 18), 
                    fill="white"
                )
                self.root.after(1000, lambda: self.canvas.delete(deactivate_text))

    def dynamic_difficulty(self):
        if self.score >= 50 * self.difficulty_level:
            self.difficulty_level += 1
            self.intruder_no += 0.01
            self.intruder_Speed += 1
            self.player_speed += 5
            
            # Notify player of difficulty increase
            if hasattr(self, 'canvas') and self.canvas.winfo_exists():
                level_text = self.canvas.create_text(
                    WIDTH // 2, 
                    HEIGHT // 2, 
                    text=f"LEVEL {self.difficulty_level}!", 
                    font=("Arial", 24, "bold"), 
                    fill="red"
                )
                self.root.after(1000, lambda: self.canvas.delete(level_text))

    def game_update(self):
        if self.running and not self.pause:
            # Move bullets up
            for bullet in self.bullets[:]:
                self.canvas.move(bullet, 0, -10)
                if self.canvas.coords(bullet)[1] < 0:
                   self.canvas.delete(bullet)
                   self.bullets.remove(bullet)
            
            # Move intruders down
            for intruder in self.intruders[:]:
                self.canvas.move(intruder, 0, self.intruder_Speed)
                
                # Skip collision check if cheat mode is on
                if self.cheat_on:
                    continue
                    
                # Check if intruder reached bottom
                if self.canvas.coords(intruder)[1] > HEIGHT:
                    self.end_game()
                    return

            # Check for bullet-intruder collisions
            for bullet in self.bullets[:]:
                if bullet not in self.canvas.find_all():  # Skip if bullet was deleted
                    continue
                    
                x1, y1 = self.canvas.coords(bullet)
                for intruder in self.intruders[:]:
                    if intruder not in self.canvas.find_all():  # Skip if intruder was deleted
                        continue
                        
                    x2, y2 = self.canvas.coords(intruder)
                    if abs(x1 - x2) < ENEMY_WIDTH // 2 and abs(y1 - y2) < ENEMY_HEIGHT // 2:
                        # Remove intruder and bullet
                        self.canvas.delete(bullet)
                        self.canvas.delete(intruder)
                        
                        if bullet in self.bullets:
                            self.bullets.remove(bullet)
                        if intruder in self.intruders:
                            self.intruders.remove(intruder)
                            
                        self.score += 10
                        self.update_score()
                        break
            
            # Spawn new intruders
            if random.random() < self.intruder_no:
                self.intruder_img()

            # Update difficulty
            self.dynamic_difficulty()

            # Continue the game loop
            self.root.after(50, self.game_update)

    def update_score(self):
        self.canvas.delete("score")
        self.canvas.create_text(
            10,
            10,
            text=f"Score: {self.score}",
            fill="white",
            anchor="nw",
            font=("Arial", 20),
            tag="score"
        )

    def end_game(self):
        if not self.running:  # Prevent multiple calls
            return
            
        self.running = False
        
        # Show game over message
        self.canvas.create_text(
            WIDTH // 2,
            HEIGHT // 2 - 200,
            text="GAME OVER",
            fill="red",
            font=("copperplate", 29, "bold")
        )
        
        # Add score to leaderboard
        if isinstance(self.score, (int, float)) and self.score >= 0:
            self.leaderboard.append({'name': self.player_name, 'score': self.score})
            
            # Save and display leaderboard
            self.leaderboard_save()
            self.display_leaderboard()
            self.end_buttons()
            
    def display_leaderboard(self):
        for widget in self.root.winfo_children():
            if widget != self.canvas:  # Keep canvas but remove other widgets
                widget.destroy()
        
        if not hasattr(self, 'canvas') or not self.canvas.winfo_exists():
            self.canvas = Canvas(self.root, width=WIDTH, height=HEIGHT, bg="blue") 
            self.canvas.pack()
            self.canvas.create_image(0, 0, image=self.bg, anchor="nw")

        self.canvas.create_text(
            WIDTH // 2,
            HEIGHT // 2 - 150,
            text="LEADERBOARD",
            fill="white",
            font=("copperplate", 25),
            anchor="center",
        )
        
        # Create main menu button
        return_button = Button(
            self.root,
            text="MAIN MENU",
            command=self.main_menu,
            font=("copperplate", 20),
            fg="red",
            bg="black"
        )  
        return_button.place(x=WIDTH // 2 - 100, y=HEIGHT - 100)

        # Display the top 5 leaderboard entries
        for i, entry in enumerate(self.leaderboard[:5]):
            self.canvas.create_text(
                WIDTH // 2,
                HEIGHT // 2 - 100 + i * 30,
                text=f"{i + 1}. {entry['name']} : {entry['score']}",
                fill="white",
                font=("copperplate", 20),
                anchor="center"
            )

    def end_buttons(self):
        # Create restart button
        restart_button = Button(
            self.root,
            text="RESTART",
            command=self.restart,
            font=("copperplate", 20),
            fg="red",
            bg="black"
        )
        restart_button.place(x=WIDTH // 2 + 80, y=HEIGHT - 100)
        
        return restart_button.tkraise()

    def main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.main_menu_screen()
    
    def main_menu_screen(self):
        """Shows the main menu screen"""
        # Create background
        canvas = Canvas(self.root, width=WIDTH, height=HEIGHT)
        canvas.pack(fill=BOTH, expand=True)
        canvas.create_image(0, 0, image=self.bg, anchor="nw")
        
        # Game title
        title_design = font.Font(family="copperplate", size=50, weight="bold")
        game_name = Label(
            self.root, 
            text="A L I E N  A T T A C K", 
            font=title_design, 
            fg="red",
            bg="black"
        )
        game_name.place(x=WIDTH//2 - 350, y=60)
        
        # Player name input
        player_name_label = Label(
            self.root, 
            text="Enter your name:", 
            font=("copperplate", 30), 
            fg="red",
            bg="black"
        )
        player_name_label.place(x=WIDTH//2 - 150, y=150)
        
        player_enter = Entry(self.root, font=("copperplate", 40))
        player_enter.place(x=WIDTH//2 - 200, y=220)
        player_enter.focus()

        def on_start_click():
            name = player_enter.get().strip()
            if name:
                self.game_start(name)
            else:
                # Flash the entry to indicate it needs input
                player_enter.config(bg="red")
                self.root.after(100, lambda: player_enter.config(bg="white"))

        # Buttons
        button_font = font.Font(size=20, weight="bold", family="copperplate")
        
        start_button = Button(
            self.root, 
            text="START", 
            command=on_start_click, 
            width=10, 
            height=1, 
            font=button_font, 
            fg="red", 
            bg="black"
        )
        start_button.place(x=WIDTH//2 - 80, y=300)
        
        leaderboard_button = Button(
            self.root, 
            text="LEADERBOARD", 
            command=self.display_leaderboard, 
            width=15, 
            height=1, 
            bg="black", 
            font=button_font, 
            fg="red"
        )
        leaderboard_button.place(x=WIDTH//2 - 120, y=370)
        
        settings_button = Button(
            self.root, 
            text="SETTINGS", 
            command=self.settings_menu, 
            width=15, 
            height=1, 
            bg="black", 
            font=button_font, 
            fg="red"
        )
        settings_button.place(x=WIDTH//2 - 120, y=440)

    def restart(self):
        """Restart the game with the same player name"""
        self.score = 0
        self.intruders = []
        self.bullets = []
        self.game_start(self.player_name)

    def save_key_mappings(self):
        """Save key mappings to a file"""
        try:
            with open('key_mappings.json', 'w') as file:
                json.dump(self.key_map, file)
            print("Key mappings saved successfully")
        except Exception as e:
            print(f"Error saving key mappings: {e}")

    def load_key_mappings(self):
        """Load key mappings from a file"""
        try:
            with open('key_mappings.json', 'r') as file:
                loaded_map = json.load(file)
                # Validate the loaded mappings
                required_keys = ['left', 'right', 'shoot', 'pause', 'up_cheat', 'down_cheat']
                if all(key in loaded_map for key in required_keys):
                    self.key_map = loaded_map
                    print("Key mappings loaded successfully")
                else:
                    print("Invalid key mappings file. Using defaults.")
        except FileNotFoundError:
            print("No key mappings file found. Using default keys.")
        except json.JSONDecodeError:
            print("Invalid key mappings file. Using default keys.")

def main():
    window = Tk()
    window.title("Galaxy Attack")
    window.geometry(f"{WIDTH}x{HEIGHT}")
    window.resizable(False, False)
    
    game = galaxy_attack(window)
    game.main_menu_screen()
    
    window.mainloop()

if __name__ == "__main__":
    main()
