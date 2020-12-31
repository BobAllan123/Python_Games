# Space Invaders by Bob Allan

import turtle
import os
import random
import pygame

# Set up the screen
window = turtle.Screen()
window.bgcolor("black")
window.title("Space Invaders by Bob Allan")
window.bgpic("space_invaders_background.gif")
window.tracer(0) # This shuts off automatic updates for the window

# Register the shapes
window.register_shape("invader.gif")
window.register_shape("player.gif")

# Draw border
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.penup()
border_pen.setposition(-300, -300)
border_pen.pendown()
border_pen.pensize(3)

for side in range(4):
    border_pen.fd(600)
    border_pen.lt(90)

border_pen.hideturtle()

# Set the score
score = 0

# Draw the score
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setposition(-290, 275)
scorestring = f"Score: {score}"
score_pen.write(scorestring, False, align="left", font=("Arial", 20, "normal"))
score_pen.hideturtle()

# Create a player turtle
player = turtle.Turtle()
player.color("blue")
player.shape("player.gif")
player.penup()
player.speed(0)
player.setposition(0, -250)
player.setheading(90)
player.speed = 0

# Choose the number of enemies
number_of_enemies = 30
# Create an empty list of enemies
enemies = []
# Add enemies to the list
for i in range(number_of_enemies):
    enemies.append(turtle.Turtle())

enemy_start_x = -225
enemy_start_y = 250
enemy_number = 0

# Create the enemy
for enemy in enemies:
    enemy.color("red")
    enemy.shape("invader.gif")
    enemy.penup()
    enemy.speed(0)
    x = enemy_start_x + (50 * enemy_number)
    y = enemy_start_y
    enemy.setposition(x, y)
    enemy_number += 1
    if enemy_number == 10:
        enemy_start_y -= 50
        enemy_number = 0

enemyspeed = 0.2

# Create the player's bullet
bullet = turtle.Turtle()
bullet.color("yellow")
bullet.shape("triangle")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(0.5, 0.5)
bullet.hideturtle()

bulletspeed = 7
bulletstate = "ready"

#Move the player left and right
def move_left():
    player.speed = -3

def move_right():
    player.speed = 3

def move_player():
    x = player.xcor()
    x += player.speed
    if x > 280:
        x = 280
    if x < -280:
        x = -280
    player.setx(x)

def fire_bullet():
    # Declare bulletstate as a global if it needs changing
    global bulletstate
    if bulletstate == "ready":
        # os.system("afplay laser.wav&")
        pygame.init()
        playSound('laser.wav')
        bulletstate = "fire"
        # Move the bullet to just above the player
        x = player.xcor()
        y = player.ycor() + 10
        bullet.setposition(x, y)
        bullet.showturtle()

def isCollision(turtle1, turtle2):
    return turtle1.distance(turtle2) < 15

def playSound(filename):
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

# Create keyboard bindings
window.listen()
window.onkeypress(move_left, "Left")
window.onkeypress(move_right, "Right")
window.onkeypress(fire_bullet, "space")

game_over = False

while not game_over:
    window.update() # Manually updating the window
    move_player()

    for enemy in enemies:

        # Ends game if enemy gets to the level of the player
        if enemy.ycor() <= -250:
            game_over = True
            print("Game Over")
            break

        # Move the enemy
        x = enemy.xcor()
        x += enemyspeed
        enemy.setx(x)

        # Move the enemy back and down when he bumps a wall
        if enemy.xcor() > 280 or enemy.xcor() < -280:
            # Move all of the enemies down at the same time
            for en in enemies:
                en.sety(en.ycor()-40)
            # Reverse enemy direction
            enemyspeed *= -1

        # Check for a collision between the bullet and the enemy
        if isCollision(bullet, enemy):
            os.system("afplay explosion.wav&")
            # Reset the bullet
            bulletstate = "ready"
            bullet.hideturtle()
            bullet.setposition(0, -400)
            # Reset the enemy
            x = random.randint(-200, 200)
            y = random.randint(100, 250)
            enemy.setposition(0, 10000)
            score += 10
            scorestring = f"Score: {score}"
            score_pen.clear()
            score_pen.write(scorestring, False, align="left", font=("Arial", 20, "normal"))
            score_pen.hideturtle()

        # Check for a collision between the enemy and the player
        if isCollision(enemy, player):
            enemy.hideturtle()
            player.hideturtle()
            print("Game Over")
            game_over = True

    # Move the bullet
    if bulletstate == "fire":
        bullet.sety(bullet.ycor() + bulletspeed)

    # Check to see if the bullet has gone to the top
    if bullet.ycor() > 275:
        bulletstate = "ready"
        bullet.hideturtle()


delay = input("Press enter to finish.")


