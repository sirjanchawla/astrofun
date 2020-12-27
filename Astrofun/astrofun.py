import os
import random
import time
import turtle
import math
"""
Winsound: library works on windows operating sysytem for playing .wav files
            from the same folder.
"""
# import winsound

"""
Counter: global variable for the score
Lives: Global variable for the lives
"""
counter = 0
lives = 3
"""
Status : is used for keeping track of the different "states". which are
        "welc", "playing" 
"""

Status = "welc"
"""
We use while true  to make sure the state changes work correctly.And the welcome
screen is showed once the player dies and the score is displayed 
"""

while True:
    if Status == "welc":
        """
        Draws the welcome screen if the state is "welc"
        clearscreen() : Function redraws the blank canvas. We use this because
                        once the loop runs and the state is changed to "welc"
                        all the previously drawn materials are
        bgcolor()& bgpic(): Both these funntions are used for defining the background
                            appearance. Bgcolor texts string arguements for the default colors
                            available in python default for setting the color.Bgpic looks
                            for ".gif" file in the same folder as the file and sets the the pic
                            as layer on top of black screen
        Title(): used for setting the title of the turtle canvas / window
        ht(): used for hiding turtle.
        
        """
        turtle.clearscreen()
        turtle.title("ASTROFUN")
        turtle.bgcolor("black")
        turtle.bgpic("welcome.gif")
        turtle.ht()
        """
        The statements below are used for starting the game once the enter key is pressed.
        We wanted to used Turtle.onkey() for this method / Pygame.keys.get_pressed. But none of
        them of worked out like we wanted it to. This suggestion was taken from TA durinf office hours

        We added a new feature. entering "b" will shut doown the turtle graphics
        """
        start = input()
        if start == "b":
            turtle.bye()
        if start == "":
            Status = "playing"
        
        

        
      
            
        
        

    """
    Main loop for running game.
    Used classes and OOP (object orienated programming), (Child & parent class) and method passing to different classes.
    Class animation : Parent class
    Class shooter: child of animation class. Is used for defining tasks for The green triangle shhoter on screen.
    Class asteroids: child of animation class, Is used for defining tasks for asteroid
    Class bullets: child of animation of  class. defining tasks for bullets.
    Class Fire_crackers: Child of animation class. Defining tasks for the fire cracker event
    Class Friend: child of the animation class. Defining tasks for the health kits
    
    """

    if Status == "playing":
        turtle.clearscreen()
        turtle.fd(0)
        turtle.speed(0)
        turtle.bgcolor("black")
        turtle.ht()
        turtle.setundobuffer(1)
        turtle.tracer(0)
        turtle.bgpic("space.gif")

        asts = []
        health_kits = []
        crackers = []



        """
        Class animation:
        1)Draws the shapes according to the shapes passed as arguements and sets their initial positions
        2)Makes the shape move forward as the defined speed. 
        
        """
        class animation(turtle.Turtle):
            def __init__(self, anishape, color, stx, sty):
                turtle.Turtle.__init__(self, shape = anishape)
                self.speed(0)
                self.penup()
                self.color(color)
                self.fd(0)
                self.goto(stx, sty)
                self.speed = 1
            def move(self):
                self.fd(self.speed)

                
                
                  

        class shooter(animation):
            
            def __init__(self, anishape, color, stx, sty):
                animation.__init__(self, anishape, color, stx, sty)
                self.shapesize(stretch_wid = 0.7, stretch_len = 1.9, outline = None)
                self.speed = 3
                self.lives = 3

            """
            These function are called on up, down , left and right arrow key presses.
            
            """
            def right_turn(self):
                self.rt(45)
                
            def left_turn(self):
                self.lt(45)
                
            def mov_back(self):
                self.speed -=1
                
            def mov_forward(self):
                self.speed += 1
            
            

            

            """
            checks for collision between the two obejects using euclidean distance(improvement suggested by Zach during the demo)
            This function is also used under the bullet class.
            possible collision combinations:
            player + asteroids(asts)
            bullet + asteroids
            bullet + healthkit(health_kits)
            """
            def is_collision(self, other):
                coll_check = False
                if math.sqrt((self.xcor()- other.xcor())**2 + (self.ycor()- other.ycor())**2) <= 20:
                    coll_check = True
                    return coll_check
                else:
                    return coll_check
            """
            Constrain: used for checking the boundaries and causes the objects to rotate right 60 degress if it hits the boundary
            """
            def constrain(self):
                if self.xcor() > 290:
                    self.setx(290)
                    self.rt(55)
                if self.xcor() < -290:
                    self.setx(-290)
                    self.rt(55)
                if self.ycor() > 290:
                    self.sety(290)
                    self.rt(55)
                if self.ycor() < -290:
                    self.sety(-290)
                    self.rt(55)

        class asteroids(animation):
            def __init__(self, anishape, color, stx, sty):
                animation.__init__(self, anishape, color, stx, sty)
                self.speed = 5
                self.randeg = random.randint(0, 360) # chooses any angle for the asteroids. 
                self.setheading(self.randeg)
            
            def constrain(self):
                if self.xcor() > 290:
                    self.setx(290)
                    self.rt(60)
                if self.xcor() < -290:
                    self.setx(-290)
                    self.rt(60)
                if self.ycor() > 290:
                    self.sety(290)
                    self.rt(60)
                if self.ycor() < -290:
                    self.sety(-290)
                    self.rt(60)
            
                
            
                
            
        class Bullet(animation):
            def __init__(self, anishape, color, stx, sty):
                animation.__init__(self, anishape, color, stx, sty)
                self.shapesize(stretch_wid = 0.1, stretch_len = 0.4, outline = None)
                self.speed = 20
                self.state = "resting" # initializing the states for bullet : "restings" and "firing"
                self.goto(-900, 900) # initally the bullet is drawn out of the frame at a random location
            def fire(self):
                if self.state == "resting": # when the spacebar is pressed this function is called and the illusion of bullet moving\
                                            #out from the shooter is created 
                    
                    
                    self.goto(player.xcor(), player.ycor())
                    self.setheading(player.heading())# seheading is used setting the head of the bullet in sync with the shooter
                    self.state = "firing"
                    
            def move(self):

                if self.state == "resting":
                    self.goto(-900, 900)
                    
                
                if self.state == "firing":
                    self.fd(self.speed)# when the state is changed moves with the speed which is initialized
                """
                As soon as the bullet hits one of the borders it again goes to its intially set location
                and again is ready to be fired
                """
                if self.xcor() > 290 or self.xcor() < - 290 or self.ycor() > 290 or self.ycor() < - 290:
                    self.goto(-900, 900)
                    self.state = "resting"
                    
            def is_collision(self, other):
                coll_check = False
                if math.sqrt((self.xcor()-other.xcor())**2 + (self.ycor()-other.ycor())**2) <= 20:
                    coll_check = True
                    return coll_check
                else:
                    return coll_check
            
        """
        This function is just like the bullets function but it is only executed when there is a collision between player and asteroids.
        We use a inbuilt shape "Classic" for the bullets and we use 20 bullets. Initially the position is off all
        the bullets are drawn at random position and when there is collision the bullets can come face at any angle giving
        illusion of the fire cracker bursting.
        """
        class Fire_cracker(animation):
            def __init__(self, anishape, color, stx, sty):
                animation.__init__(self, anishape, color, stx, sty)
                self.shapesize(stretch_wid = 0.1, stretch_len = 0.1, outline = None)
                self.goto(-900, 900)
                #self.frame = 0
            def explode(self, startx, starty):
                self.goto(startx, starty)
                self.setheading(random.randint(0, 360))
            def move(self):
                self.fd(10)
            
                    
        """
        Motion defined like the asteroids sprite
        """
        class Friend(animation):
            def __init__(self, anishape, color, stx, sty):
                animation.__init__(self, anishape, color, stx, sty)
                self.shapesize(stretch_wid = 0.6, stretch_len = 0.6, outline = None)
                self.speed = 7
                self.randeg = random.randint(0, 360)
                self.setheading(self.randeg)

            def move(self):
                self.fd(self.speed)
            """
            Same purpose of the constrain function just rotates the boject towards the left
            """
            def constrain(self):
                if self.xcor() > 290:
                    self.setx(290)
                    self.lt(55)
                if self.xcor() < -290:
                    self.setx(-290)
                    self.lt(55)
                if self.ycor() > 290:
                    self.sety(290)
                    self.lt(55)
                if self.ycor() < -290:
                    self.sety(-290)
                    self.lt(55)
                
                

            

            
                    
                
                
                
                
                
                
            
        class My_game():
            def __init__(self):
                
                self.lives = 3
                
                self.draw = turtle.Turtle()# instance of turtle class
                self.score = 0
            
            def draw_frame(self): # draws the border of the game with actually showing the skething
                self.draw.speed(0)#) 0 speed shows no animation while drawing
                self.draw.color("black")#we draw a black border
                self.draw.penup()
                self.draw.goto(-300, 300)#We draw the border starting from this coordinate
                self.draw.pendown()
                for i in range(4):# we use range in 4 because our frame has 4 sides
                    self.draw.forward(600)
                    self.draw.rt(90)
                self.draw.penup()
                self.draw.ht()
                
                self.draw.pendown()
            def msg_writer(self):# updates the score. Can be seen once the turtle window is maximised.
                self.draw.undo()
                self.draw.color("White")
                score = "Enemies destroyed : {0}" .format(self.score)
               
                self.draw.penup()
                self.draw.goto(-300, 320)
                self.draw.write(score, font =("Times New Roman", 12, "bold italic"))
                
                
             
                
                
        """
        This function updates the number of lives left
        """
        def msg_writer_lives(lives):
                turtle.undo()# while undo the previous writing at that position. If we dont use this\
                                #function then it scribles the score on top of each other.
                    
                
                turtle.color("White")#The fon color
                live = "Lives left : {0}" .format(lives)
                turtle.penup()
                turtle.goto(-200,300)
                turtle.write(live, font =("Times New Roman", 12, "bold italic"))#Font size and font style        
                
        ran = My_game() # is instance of My)game class
        ran.draw_frame()
        ran.msg_writer()# Using it display the intial score
        bullet = Bullet("triangle", "red", 0, 0)#instance of Bullet class. Passed with the arguements: shape, color, and start coordinate
        player = shooter("triangle", "green", 0, 0)#instance of Shooter class. Passed with the arguements: shape, color, and start coordinate
        
        
        for ast in range(8):
            asts.append(asteroids("square", "yellow", -100, 0))# Creeates 8 asteroids of same dimensions and color , keeps track using list
        
        
        
        for  x in range(2):
            health_kits.append(Friend("circle", "blue", 100, 0))# Creates 2 health_kits of same dimensions and color, keeps track using list
        
        for i in range(20):
            crackers.append(Fire_cracker("classic", "orange", 0, 0))# Creates 20 small particles of same dimensions and color, keeps track using list


                            
        """
        These check the key presses. Work similarly to pygame.key.get_pressed.
        Calls the function with no argument when the key press is detected.
        """
        turtle.onkey(player.left_turn, "Left")
        turtle.onkey(player.right_turn, "Right")
        turtle.onkey(player.mov_forward, "Up")
        turtle.onkey(player.mov_back, "Down")
        turtle.onkey(bullet.fire, "space")
        turtle.listen()


        
        msg_writer_lives(lives)
        """
        Like traditional shooting games . The game runs until the player has three lives.
        Once the player dies , score is shown and then the game comes back to welcome screen
        """
        while lives > 0 and lives <= 3:
            turtle.update()
            time.sleep(0.017)
            
            player.move()
            player.constrain()
            
            """
            Goes through all the asteroids in the list. Makes them move and checks for collision for each of them
            """
            for ast in asts: 
                ast.move()
                ast.constrain()
                
                if player.is_collision(ast):# checks for collision if return true then\
                    player.goto(0, 0)       # the player is again drawn at the middle \             
                    lives -= 1              # resembling the original game
                    ran.lives -= 1
                    ran.msg_writer()
                    msg_writer_lives(lives)

                if bullet.is_collision(ast): 
                    ast.goto(random.randint(-270, 270), random.randint(-270, 270) ) #.goto function draws the obeject at given x & y,\
                                                                                        #in this case it choses randomly using rando.randint between -270\
                                                                                        #and 270 so that it is not drawn out of the frame
                    #winsound.PlaySound("expl.wav", winsound.SND_ASYNC)
                    os.system('aplay expl.wav&')# gives an error on VM and windows and causes a bit of lag. 
                    bullet.state = "resting"
                    ran.score +=100 # each kill counts for 100 points
                    ran.msg_writer()
                    points = ran.score
                    for expl in crackers:#causes the explosion from where the bullet is
                            expl.goto(bullet.xcor(), bullet.ycor())
                            expl.setheading(random.randint(0, 360))
                
                
                
                
                
                    
                            
                    
            
            
            for expl in crackers:# setting the motion for the fire crackers
                expl.move()
                
            bullet.move()
            """
            Goes through all the kits in the list and makes them move and checks for their collision
            """
            for kit in health_kits:
                kit.move()
                kit.constrain()
                if bullet.is_collision(kit):
                    kit.goto(random.randint(-270, 270),random.randint(-270, 270)  )
                    bullet.state = "resting"
                    if ran.lives < 3:
                        lives += 1
                        ran.lives +=1
                    ran.msg_writer()
                    msg_writer_lives(lives)
                            
                        
        """
        If the player dies that is the lives == 0
        Then it shows game over part. Shows the total score and changes the status to "welc"
        """
        if lives == 0:
            turtle.clearscreen()
            turtle.bgcolor("black")
            turtle.bgpic("game_over.gif")
            turtle.ht()
            turtle.setundobuffer(0)
            
            #turtle.penup()
            turtle.goto(-110, 0)# draws the text at the given x &y using .goto
            turtle.color("white")
            points = " Enemies destroyed : {0}" .format(points)
            
            turtle.write(points, font = ("Times New Roman", 20, "bold italic"))
            
            
            points = 0
            lives = 3

            #end = input()
            time.sleep(3)
            Status = "welc"


    

        
        
