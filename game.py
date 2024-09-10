import pygame, sys, time, random
from pygame.surfarray import array3d 

BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)

class SnakeEnv():

    def __init__(self, width=640, height=480):

        self.width = width
        self.height = height
        self.game_window = pygame.display.set_mode((self.width, self.height))

        self.reset()

    def reset(self):
        
        self.game_window.fill(BLACK)
        self.snake_pos = [100, 50]
        self.snake_body = [[100, 50], [90, 50], [80, 50]]
        self.food_pos = self.spawn_food()
        self.food_spawn = True
        self.direction = 'RIGHT'
        self.action = self.direction
        self.score = 0
        self.steps = 0

        print("GAME RESET")

    def change_direction(self, action, direction):

        if action == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if action == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if action == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if action == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'
        
        return direction
    
    def move(self, direction, snake_pos):
        if direction == 'UP':
            snake_pos[1] -= 10
        if direction == 'DOWN':
            snake_pos[1] += 10
        if direction == 'LEFT':
            snake_pos[0] -= 10
        if direction == 'RIGHT':
            snake_pos[0] += 10
        
        return snake_pos


    def spawn_food(self):
        return [random.randrange(1, (self.width//10)) * 10, random.randrange(1, (self.height//10)) * 10]
    
    def eat(self):
        return self.food_pos == self.snake_pos
    
    def human_step(self, event):
        
        action = None

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                action = 'UP'
            if event.key == pygame.K_DOWN:
                action = 'DOWN'
            if event.key == pygame.K_LEFT:
                action = 'LEFT'
            if event.key == pygame.K_RIGHT:
                action = 'RIGHT'
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
        
        return action
    
    def display_score(self, color, font, size):

        score_font = pygame.font.SysFont(font, size)
        score_surface = score_font.render('Score : ' + str(self.score), True, color)
        score_rect = score_surface.get_rect()
        score_rect.midtop = (self.width/2, 15)
        self.game_window.blit(score_surface, score_rect)

    def game_over(self):
        # TOUCH WALL
        if self.snake_pos[0] < 0 or self.snake_pos[0] > self.width - 10:
            self.end_game()
        if self.snake_pos[1] < 0 or self.snake_pos[1] > self.height - 10:
            self.end_game()

        # TOUCH BODY
        for block in self.snake_body[1:]:
            if self.snake_pos == block:
                self.end_game()

    def end_game(self):
        
        message = pygame.font.SysFont('arial', 45)
        message_surface = message.render("GAME OVER", True, RED)
        message_rect = message_surface.get_rect()
        message_rect.midtop = (self.width/2, self.height/4)

        self.game_window.fill(BLACK)
        self.game_window.blit(message_surface, message_rect)
        self.display_score(RED, 'arial', 20)
        pygame.display.flip()
        time.sleep(3)
        pygame.quit()
        sys.exit()

snake_env = SnakeEnv(600, 600)
difficulty = 10
fps_controller = pygame.time.Clock()
check_errors = pygame.init()
pygame.display.set_caption('Snake Game')

while True:

    # Human input
    for event in pygame.event.get():
        snake_env.action = snake_env.human_step(event)

    # Check direction
    snake_env.direction = snake_env.change_direction(snake_env.action, snake_env.direction)
    snake_env.snake_pos = snake_env.move(snake_env.direction, snake_env.snake_pos)

    # Check food
    snake_env.snake_body.insert(0, list(snake_env.snake_pos))
    if snake_env.eat():
        snake_env.food_spawn = False
        snake_env.score += 1
    else:
        snake_env.snake_body.pop()

    if not snake_env.food_spawn:
        snake_env.food_pos = snake_env.spawn_food()
    
    snake_env.food_spawn = True

    # Draw snake
    snake_env.game_window.fill(BLACK)
    for pos in snake_env.snake_body:
        pygame.draw.rect(snake_env.game_window, GREEN, pygame.Rect(pos[0], pos[1], 10, 10))

    # Draw food
    pygame.draw.rect(snake_env.game_window, WHITE, pygame.Rect(snake_env.food_pos[0], snake_env.food_pos[1], 10, 10))

    # Check game over
    snake_env.game_over()

    # Update display
    snake_env.display_score(WHITE, 'arial', 20)
    pygame.display.update()
    fps_controller.tick(difficulty)
    img = array3d(snake_env.game_window)



            

        
        