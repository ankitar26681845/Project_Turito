import tkinter as tk
from tkinter import messagebox
import pygame
import sys
import turtle
import threading

# Function to load user data from a file
def load_users():
    try:
        with open("users.txt", "r") as file:
            users = {}
            for line in file:
                username, password = line.strip().split(",")
                users[username] = password
            return users
    except FileNotFoundError:
        return {}

# Function to save user data to a file
def save_user(username, password):
    with open("users.txt", "a") as file:
        file.write(f"{username},{password}\n")

# Function for signing up
def signup():
    username = username_entry.get()
    password = password_entry.get()

    if username == "" or password == "":
        messagebox.showwarning("Warning", "Please fill in all fields")
        return

    users = load_users()
    if username in users:
        messagebox.showwarning("Warning", "Username already exists")
    else:
        save_user(username, password)
        messagebox.showinfo("Success", "Signup successful! You can now log in.")
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)

# Function for signing in
def signin():
    username = username_entry.get()
    password = password_entry.get()

    users = load_users()
    if username in users and users[username] == password:
        messagebox.showinfo("Success", f"Welcome {username}!")
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        app.destroy()  # Close the Tkinter window
        start_game()   # Start the Pygame game
    else:
        messagebox.showwarning("Warning", "Invalid username or password")

# Function to toggle full screen for Tkinter
def toggle_fullscreen_tk():
    global fullscreen_tk
    fullscreen_tk = not fullscreen_tk
    app.attributes("-fullscreen", fullscreen_tk)
    if not fullscreen_tk:
        app.geometry("800x600")  # Set to your preferred window size
    else:
        app.geometry("")  # Fullscreen mode

# Function to toggle full screen for Pygame
def toggle_fullscreen_pg():
    global screen, fullscreen_pg
    fullscreen_pg = not fullscreen_pg
    if fullscreen_pg:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Fullscreen mode
    else:
        screen = pygame.display.set_mode((800, 600))  # Windowed mode

# Function to start the Pygame game
def start_game():
    global screen
    # Initialize Pygame
    pygame.init()

    # Constants
    global fullscreen_pg
    fullscreen_pg = False
    screen = pygame.display.set_mode((800, 600))  # Initial window size
    pygame.display.set_caption("Flying Bird with Scrolling Background")

    # Load images
    background_image = pygame.image.load('/Users/ankit/Desktop/python_Work/assignment1/background.jpg')  # Replace with your background image file
    bird_image = pygame.image.load('/Users/ankit/Desktop/python_Work/assignment1/bird.png')  # Replace with your bird image file
    bird_image = pygame.transform.scale(bird_image, (50, 50))  # Scale the bird image

    # Bird position
    bird_x = 100  # Initial horizontal position
    bird_y = 300  # Initial vertical position (adjusted for window size)
    bird_velocity = 3  # Speed of the bird's vertical movement
    bird_direction = 1  # 1 for down, -1 for up
    scroll_speed = 2    # Speed of the scrolling background

    # Main loop
    start_time = pygame.time.get_ticks()  # Start time for one minute
    running = True

    while running:
        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                toggle_fullscreen_pg()  # Toggle fullscreen on 'f' key press

        # Update bird position for up and down motion
        bird_y += bird_velocity * bird_direction

        # Change direction when the bird reaches the top or bottom
        if bird_y <= 0 or bird_y >= 600 - 50:  # Adjust for window height
            bird_direction *= -1  # Reverse direction

        # Update the bird's horizontal position to move it forward
        bird_x += 3  # Adjust the value to increase or decrease the speed of horizontal movement

        # Reset bird position if it moves off the screen
        if bird_x > 800:  # Adjust for window width
            bird_x = -50  # Reset to start from the left side of the screen

        # Update the scrolling background
        background_x = (pygame.time.get_ticks() * scroll_speed // 100) % background_image.get_width()
        screen.blit(background_image, (-background_x, 0))
        screen.blit(background_image, (-background_x + background_image.get_width(), 0))

        # Draw the bird
        screen.blit(bird_image, (bird_x, bird_y))  # Draw the bird image

        # Update the display
        pygame.display.flip()

        # Check for 1-minute duration
        if (pygame.time.get_ticks() - start_time) > 60000:  # 60000 milliseconds = 1 minute
            running = False  # Exit loop after one minute

        # Frame rate
        pygame.time.Clock().tick(60)

    # End screen with a "Thank You!" message
    screen.fill((135, 206, 250))  # Fill with sky blue color
    font = pygame.font.Font(None, 74)
    text = font.render("Thank You!", True, (255, 0, 0))
    text_rect = text.get_rect(center=(400, 300))  # Center for window size
    screen.blit(text, text_rect)
    pygame.display.flip()

    # Wait for a moment before quitting
    pygame.time.delay(2000)  # Wait for 2 seconds
    pygame.quit()

    # Start Turtle graphics for the thank you message
    threading.Thread(target=draw_thank_you).start()

def draw_heart():
    turtle.penup()
    turtle.goto(0, -50)  # Start position for the heart
    turtle.pendown()
    turtle.color("red")
    turtle.begin_fill()
    turtle.left(140)
    turtle.forward(224)
    turtle.circle(-112, 200)
    turtle.left(120)
    turtle.circle(-112, 200)
    turtle.forward(224)
    turtle.end_fill()

def draw_text():
    turtle.penup()
    turtle.goto(0, 30)  # Move to a higher position inside the heart
    turtle.pendown()
    turtle.color("white")  # Text color inside the heart
    turtle.write("Thank You!", align="center", font=("Arial", 24, "bold"))

def draw_thank_you():
    turtle.speed(10)  # Fast drawing speed
    draw_heart()      # Draw the heart shape
    draw_text()       # Write "Thank You!" inside the heart
    turtle.hideturtle()  # Hide the turtle after drawing

    # Wait for a user click to exit
    turtle.done()

# Set up the main application window
app = tk.Tk()
app.title("Login Application")

# Create frames for better layout
frame = tk.Frame(app)
frame.pack(pady=20)

# Username label and entry
username_label = tk.Label(frame, text="Username:")
username_label.grid(row=0, column=0)
username_entry = tk.Entry(frame)
username_entry.grid(row=0, column=1)

# Password label and entry
password_label = tk.Label(frame, text="Password:")
password_label.grid(row=1, column=0)
password_entry = tk.Entry(frame, show='*')
password_entry.grid(row=1, column=1)

# Signup button
signup_button = tk.Button(frame, text="Sign Up", command=signup)
signup_button.grid(row=2, column=0, pady=10)

# Signin button
signin_button = tk.Button(frame, text="Sign In", command=signin)
signin_button.grid(row=2, column=1, pady=10)

# Fullscreen toggle button for Tkinter
fullscreen_tk = False  # State variable for Tkinter fullscreen
toggle_button_tk = tk.Button(frame, text="Toggle Full Screen", command=toggle_fullscreen_tk)
toggle_button_tk.grid(row=3, columnspan=2, pady=10)

# Start the Tkinter event loop
app.geometry("800x600")  # Set initial size
app.mainloop()
