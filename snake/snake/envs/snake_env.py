import pygame, sys, time, random
from pygame.surfarray import array3d 
from pygame import display

import numpy as np
import gymnasium as gym
from gymnasium import error, spaces, utils
from gymnasium.utils import seeding

BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)

class SnakeEnv(gym.Env):

    def __init__(self):
        
        self.action_space = spaces.Discrete(4)
        self.width = 200
        self.height = 200
        self.game_window = pygame.display.set_mode((self.width, self.height))

        self.reset()
        
        self.STEP_LIMIT = 1000
        self.sleep = 0


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

        img = array3d(display.get_surface())
        img = np.swapaxes(img, 0, 1)
        return img

    @staticmethod
    def change_direction(action, direction):

        if action == 0 and direction != 'DOWN':
            direction = 'UP'
        if action == 1 and direction != 'UP':
            direction = 'DOWN'
        if action == 2 and direction != 'RIGHT':
            direction = 'LEFT'
        if action == 3 and direction != 'LEFT':
            direction = 'RIGHT'
        
        return direction
    
    @staticmethod
    def move(direction, snake_pos):
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
    
    def step(self, action):

        scoreholder = self.score
        reward = 0
        self.direction = SnakeEnv.change_direction(action, self.direction)
        self.snake_pos = SnakeEnv.move(self.direction, self.snake_pos)
        self.snake_body.insert(0, list(self.snake_pos))

        reward = self.food_handler() # reward handler

        self.update_game_state() # update the env after the action

        reward, terminated = self.game_over(reward)
        truncated = terminated

        obs = self.get_image_array_from_game()

        self.steps += 1
        info = {'score': self.score, 'steps': self.steps, 'action': action}


        
        return obs, reward, terminated, truncated, info
    
    def food_handler(self):
        if self.eat():
            self.score += 1
            self.food_spawn = False
            reward = 1
        else:
            self.snake_body.pop()
            reward = 0
        
        if not self.food_spawn: 
            self.food_pos = self.spawn_food()
        self.food_spawn = True

        return reward
    
    def get_image_array_from_game(self):
        img = array3d(display.get_surface())
        img = np.swapaxes(img, 0, 1)
        return img

    def update_game_state(self):
        self.game_window.fill(BLACK)
        for pos in self.snake_body:
            pygame.draw.rect(self.game_window, GREEN, pygame.Rect(pos[0], pos[1], 10, 10))  

    def game_over(self, reward):
        # TOUCH WALL
        if self.snake_pos[0] < 0 or self.snake_pos[0] > self.width - 10:
            return -1, True
        if self.snake_pos[1] < 0 or self.snake_pos[1] > self.height - 10:
            return -1, True

        # TOUCH BODY
        for block in self.snake_body[1:]:
            if self.snake_pos == block:
                return -1, True
        
        if self.steps >= self.STEP_LIMIT:
            return 0, True
        
        return reward, False
    
    def render(self, mode='human'):
        if mode == 'human':
            display.update()
    
    def close(self):
        pass