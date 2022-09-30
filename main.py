import pygame
import numpy as np
import sys
import random

class Tile(pygame.sprite.Sprite):
  def __init__(self, value, pos):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.image.load("%itile.png"%value)
    self.rect = self.image.get_rect()
    self.rect.left = (pos[1]*140 + (pos[1]+1)*10)
    self.rect.top = (pos[0]*140 + (pos[0]+1)*10)
    #TODO -- add valid list of numbers

def clear_tiles_from_board(the_group, the_screen):
  #the_group.clear(the_screen, (0, 0, 0))
  the_group.empty()
  

def make_tiles(board, the_group):
  for i in range(len(board)):
    for j in range(len(board)):
      if board[i][j] > 0:
        the_group.add(Tile(board[i][j], (i, j)))

def init_board():
  board = np.zeros((4,4))
  p1 = (random.randint(0, 3), random.randint(0, 3))
  same = True
  while same:
    p2 = (random.randint(0, 3), random.randint(0, 3))
    if p1 != p2: same = False
    else: print('Retrying', p1, p2)
  board[p1[0], p1[1]] = 2
  board[p2[0], p2[1]] = 2
  return board

#def draw_board(screen, board):

def can_shift_up(board):
  rotated_board = np.rot90(board)
  return can_shift_left(rotated_board)

def shift_up(board):
  rotated_board = np.rot90(board) 
  shifted_board = shift_left(rotated_board)
  return np.rot90(shifted_board, -1)

def can_shift_down(board):
  rotated_board = np.rot90(board, -1)
  return can_shift_left(rotated_board)

def shift_down(board):
  rotated_board = np.rot90(board, -1) 
  shifted_board = shift_left(rotated_board)
  return np.rot90(shifted_board)

def can_shift_right(board):
  flipped_board = np.flip(board, axis=1)
  return can_shift_left(flipped_board)

def shift_right(board):
  flipped_board = np.flip(board, axis=1)
  shifted_board = shift_left(flipped_board)
  return np.flip(shifted_board, axis=1)

def can_shift_left(board):
  shiftable = []
  for row in board:
    if np.count_nonzero(row) == 0:
      shiftable.append(False)
    else:
      row_can_shift = False
      for i in range(1, len(row)):
        #print(row[i-1], row[i])
        if row[i-1] == row[i] and row[i] > 0:
          row_can_shift = True
        if row[i-1] == 0 and row[i] > 0:
          row_can_shift = True
      shiftable.append(row_can_shift)
  return np.any(shiftable)
  #print(shiftable)

def spawn(board):
  if np.any(board == 0):
    i = random.choice(np.where(np.any(board == 0, axis=1))[0]) 
    j = random.choice(np.where(board[i] == 0)[0])
    board[i][j] = 2

def shift_left(board):
  new_board = []
  for row in board:
    trimmed_row = row[row != 0]
    #print(trimmed_row)

    i = 1
    the_len = len(trimmed_row)
    while i < the_len:
    #for i in range(1, len(trimmed_row)):
      #print(trimmed_row[i-1], trimmed_row[i])
      if trimmed_row[i-1] == trimmed_row[i]:
        trimmed_row[i-1] *= 2
        trimmed_row = np.delete(trimmed_row, i)
      i += 1
      the_len = len(trimmed_row)
        #break

    padded_row = np.pad(trimmed_row, (0, len(row)-len(trimmed_row)), 'constant', constant_values=(0, 0))
    #print(padded_row)
    new_board.append(padded_row)
  return np.array(new_board)

if __name__ == '__main__':
  pygame.init()

  size = width, height = 600, 600
  black = 0, 0, 0
  speed = [0, 0]

  #the_board = np.zeros(4, 4)
  the_board = init_board()
  print(the_board)

  screen = pygame.display.set_mode(size)
  all_sprites = pygame.sprite.RenderUpdates()
  make_tiles(the_board, all_sprites)
  #first_tile = Tile(2, (0, 0))
  #ball = pygame.image.load("intro_ball.gif")
  #ballrect = ball.get_rect()

  score = 0

  while True:
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
          the_board = shift_left(the_board)
          spawn(the_board)
        elif event.key == pygame.K_RIGHT and can_shift_right(the_board):
          print('Right')
          the_board = shift_right(the_board)
          spawn(the_board)
        elif event.key == pygame.K_UP and can_shift_up(the_board):
          print('Up')
          the_board = shift_up(the_board)
          spawn(the_board)
        elif event.key == pygame.K_DOWN and can_shift_down(the_board):
          print('Down')
          the_board = shift_down(the_board)
          spawn(the_board)
        else: continue

        print(the_board)
        print(score)
        print()

    screen.fill(black)
    #screen.blit(first_tile.tile, first_tile.rect)
    clear_tiles_from_board(all_sprites, screen)
    make_tiles(the_board, all_sprites)
    all_sprites.draw(screen)
    pygame.display.flip()
