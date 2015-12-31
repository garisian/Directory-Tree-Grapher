import os
import os.path
from Node import *
import pygame
import tkFileDialog
import user_options
from Tkinter import *

def draw_rect(coord, screen, screen_size, root, all_info):
    ''' ((a, b), screen, (x, y), node, list) => None.
    Updates the screen with rectangles that corresponds
    to the files within root and while white boarders are drawn
    around the directories.'''

    root.get_rect(coord, screen_size)
    #print rects.values()
    for child in root.children:
        #if node is a directory and has children, recurse
        if not isinstance(child, File):
            #info[0], etc contain information we got from get_rect about
            #the rectangle for node
            draw_rect((child.x, child.y), screen, \
                      (child.height, child.width), child, all_info)
            pygame.draw.rect(screen, (255, 255, 255), \
                    (child.x, child.y, child.width, child.height), 2)

        #if node is not a directory, i.e. is just a file, draw its
        #rectangle directly
        else:
            pygame.draw.rect(screen, child.color, (child.x, child.y, \
                                            child.width, child.height))
            all_info.append(child)
    # update the screen with all new rectangles and white borders
    pygame.display.flip()

    return all_info


def find_path(all_info, coordinates):
    '''(list, 2-tuple of ints) -> str
    Return the path name contained in coordinates'''
    for item in all_info:
        if item.x <= coordinates[0] <= (item.x + item.width) \
           and item.y <= coordinates[1] <= (item.y + item.height):
            return item.key

def create_legend(root, screen, sc, d):
    '''(Node, screen, (x_start, y_start), [list of files and directories]
    Print the file and directories as a hierarchy on the screen'''
    counter = 0
    multiplcation_factor = sc[0] / float( len(d))
    text_size = sc[0] / float(len(d) )
    if text_size > 15:
        text_size = 15
    font = pygame.font.Font(None, int(text_size))
    for item in d:
        text_surface = font.render(item, 0, white)
        text_pos = (sc[1], 0 + counter * multiplcation_factor)
        screen.blit(text_surface, text_pos)
        counter += 1
    pygame.display.flip()


def initialize(screen_size, sc):
    ''''''
    screen = pygame.display.set_mode(screen_size)
    root_directory = tkFileDialog.askdirectory(\
        title="Select a Python Directory ...",  initialdir=".")
    pygame.display.set_caption("Memory Map of Current File Path: " + \
                               str(root_directory))
    root = Directory(str(root_directory))
    root.build_tree()
    root.fix_sizes()
    names = root.get_names(0, [])
    all_children = draw_rect((0, 0), screen, sc, root, [])

    return screen, all_children, names, root

def find_node(root, coordinate):

    if root:
        for child in root.children:
            if child.x <= coordinate[0] <= (child.x + child.width) \
               and child.y <= coordinate[1] <= (child.y + child.height):
                return child

if __name__ == '__main__':  ###DO WE NEED COMMENTS IN MAIN??
    prompt = user_options.UserPrompt()
    prompt.mainloop()
    screen_size = (prompt.width, prompt.height)
    has_legend = prompt.has_legend
    can_zoom = prompt.can_zoom

    white = (255, 255, 255)
    black = (0, 0, 0)
    pygame.init()
    #screen_size = (1000, 600) #make the user choose the screen size

    if has_legend:
        sc = (screen_size[1] - 30, screen_size[0] - 400)
    else:
        sc = (screen_size[1] - 30, screen_size[0])
                                 #must be greater than 600,600
    screen, all_children, names, root = initialize(screen_size, sc)

    running = True
    while running:
        zoom_node = root
        if has_legend:
            create_legend(zoom_node, screen, sc, names)

        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, black, (0, sc[0], sc[1] + 400, 30))
            # Get a font and use it render the text to a Surface.
            font = pygame.font.Font(None, 30)
            current_path = find_path(all_children, event.pos)
            if not current_path:
                report = ''
            else:
                report = current_path
            text_surface = font.render('(%s)'\
                                      % report, 1, white)
            # Where to blit the text_surface:
            #the screen height - the font height.
            text_pos = (0, sc[0])
            screen.blit(text_surface, text_pos)
        elif can_zoom and event.type == pygame.MOUSEBUTTONUP:
            current_coordinate = pygame.mouse.get_pos()
            zoom_node = find_node(zoom_node, current_coordinate)
            if zoom_node: #and not isinstance(zoom_node, File):
                suball_children = draw_rect((0, 0), screen, sc, zoom_node, [])
                pygame.draw.rect(screen, (0, 0, 0), (sc[1], 0, 400, sc[0]))
                pygame.display.set_caption(\
                        "Memory Map of Current File Path: %s" % zoom_node.key)
                root = zoom_node
                names = root.get_names(0, [])
        elif event.type == pygame.KEYDOWN and event.key == 114:
            current_path = find_path(all_children, pygame.mouse.get_pos())
            rename_req = user_options.Rename()
            rename_req.mainloop()
            if current_path:
                os.rename(current_path, rename_req.new_name)
            else:
                tkMessageBox.showerror("No Path Error", \
                    "Please position the mouse over a valid file ")






        pygame.display.flip()
    pygame.display.quit()
