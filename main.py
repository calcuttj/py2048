import pygame
import numpy as np
import sys
import random

class Tile(pygame.sprite.Sprite):
  def __init__(self, value, pos, screen):
    pygame.sprite.Sprite.__init__(self)

    #Draw white rectangle on the screen
    self.white_rect = pygame.draw.rect(
        screen, (255, 255, 255),
        pygame.Rect((pos[1]*140 + (pos[1]+1)*8),
        (pos[0]*140 + (pos[0]+1)*8),
        140, 140))
    self.font = pygame.font.SysFont('Arial', 80)

    #The font rendering will be the image of the sprite
    #Set its center to the above rectangle
    self.image = self.font.render('%i'%value, True, (0, 0, 0))
    self.rect = self.image.get_rect()
    self.rect.center = self.white_rect.center


##Might just remove this unless it ends up being more complicated
def clear_tiles_from_board(the_group, the_screen):
  the_group.empty()
  

#Make a tile on the board wherever there is a number > 0
def make_tiles(board, the_group, screen):
  for i in range(len(board)):
    for j in range(len(board)):
      if board[i][j] > 0:
        the_group.add(Tile(board[i][j], (i, j), screen))

#Make all zeros on the board -- spawn tiles on two random spaces 
def init_board():
  board = np.zeros((4,4))
  spawn(board)
  spawn(board)
  return board

def can_shift_up(board):
  rotated_board = np.rot90(board)
  return can_shift_left(rotated_board)

def shift_up(board):
  rotated_board = np.rot90(board) 
  shifted_board, score = shift_left(rotated_board)
  return (np.rot90(shifted_board, -1), score)

def can_shift_down(board):
  rotated_board = np.rot90(board, -1)
  return can_shift_left(rotated_board)

def shift_down(board):
  rotated_board = np.rot90(board, -1) 
  shifted_board, score = shift_left(rotated_board)
  return (np.rot90(shifted_board), score)

def can_shift_right(board):
  flipped_board = np.flip(board, axis=1)
  return can_shift_left(flipped_board)

def shift_right(board):
  flipped_board = np.flip(board, axis=1)
  shifted_board, score = shift_left(flipped_board)
  return (np.flip(shifted_board, axis=1), score)

#Check each row for the following
#  If all zeros -- row is unshiftable
#  If any pair -- row is shiftable
#  If any zero on left of numbered spot -- row is shiftable
#If any row is shiftable -- the whole board is shiftable
def can_shift_left(board):
  shiftable = []
  for row in board:
    if np.count_nonzero(row) == 0:
      shiftable.append(False)
    else:
      row_can_shift = False
      for i in range(1, len(row)):
        if row[i-1] == row[i] and row[i] > 0:
          row_can_shift = True
        if row[i-1] == 0 and row[i] > 0:
          row_can_shift = True
      shiftable.append(row_can_shift)
  return np.any(shiftable)

#Spawn a 2 or 4 (10% chance)
#at a random spot on the board where the space is zero
def spawn(board):
  if np.any(board == 0):
    i = random.choice(np.where(np.any(board == 0, axis=1))[0]) 
    j = random.choice(np.where(board[i] == 0)[0])
    board[i][j] = (2 if random.random() < .9 else 4)

def shift_left(board):
  new_board = []
  score = 0
  for row in board:
    trimmed_row = row[row != 0] #remove zeroes 

    i = 1
    the_len = len(trimmed_row)
    #move from left to right through the row
    while i < the_len:
      #check if there is a pair
      if trimmed_row[i-1] == trimmed_row[i]: 
        trimmed_row[i-1] *= 2 # double it
        score += trimmed_row[i-1] # add to score
        trimmed_row = np.delete(trimmed_row, i) #remove the right tile
      i += 1 #skip so we don't double count
      the_len = len(trimmed_row)

    #add zeros back in on the right
    #padded_row = np.pad(
    #    trimmed_row, (0, len(row)-len(trimmed_row)), 'constant', 
    #    constant_values=(0, 0))
    new_board.append(np.pad(
        trimmed_row, (0, len(row)-len(trimmed_row)), 'constant', 
        constant_values=(0, 0)))
  return (np.array(new_board), score)

if __name__ == '__main__':
  pygame.init()

  size = width, height = 600, 600
  black = 0, 0, 0
  speed = [0, 0]

  #Initial setup
  the_board = init_board()
  print(the_board)
  screen = pygame.display.set_mode(size)
  all_sprites = pygame.sprite.RenderUpdates()
  make_tiles(the_board, all_sprites, screen)

  #Initial drawing
  screen.fill(black)
  clear_tiles_from_board(all_sprites, screen)
  make_tiles(the_board, all_sprites, screen)
  all_sprites.draw(screen)
  pygame.display.flip()

  total_score = 0

  while True:
    update = False
    for event in pygame.event.get():
      if event.type == pygame.QUIT: sys.exit()
      elif event.type == pygame.KEYDOWN:
        if not (can_shift_left(the_board) or can_shift_right(the_board) or
                can_shift_up(the_board) or can_shift_down(the_board)):
          print('YOU LOSE')

        if np.any(the_board == 2048):
          print('YOU WIN')
          continue
        if event.key == pygame.K_LEFT and can_shift_left(the_board):
          print('Left')
          the_board, score = shift_left(the_board)
          total_score += score
          spawn(the_board)
          update = True
        elif event.key == pygame.K_RIGHT and can_shift_right(the_board):
          print('Right')
          the_board, score = shift_right(the_board)
          total_score += score
          spawn(the_board)
          update = True
        elif event.key == pygame.K_UP and can_shift_up(the_board):
          print('Up')
          the_board, score = shift_up(the_board)
          total_score += score
          spawn(the_board)
          update = True
        elif event.key == pygame.K_DOWN and can_shift_down(the_board):
          print('Down')
          the_board, score = shift_down(the_board)
          total_score += score
          spawn(the_board)
          update = True
        else: continue

        print(the_board)
        print(int(total_score))
        print()

    if update:
      screen.fill(black)
      clear_tiles_from_board(all_sprites, screen)
      make_tiles(the_board, all_sprites, screen)
      all_sprites.draw(screen)
      pygame.display.flip()
