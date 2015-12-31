from random import *
import os
import os.path

class Node(object):
    '''A node in a tree.'''

    def __init__(self, k):
        '''(Node, object) -> NoneType
        Create a Node with key k and no children.'''

        self.key = k
        self.children = []


class Directory(Node):
    '''A directory'''

    def __init__(self, k):
        '''(Directory, str, int) -> NoneType'''

        Node.__init__(self, k)
        self.size = self.get_size()
        self.shortname = os.path.basename(self.key)
        self.count = 0


    def get_size(self):
        '''(File) -> int
        Return the size of the File.'''

        return os.path.getsize(self.key)

    def build_tree(self):
        '''(Directory) -> Directory
        Print the list of files and directories in directory d, recursively,
        prefixing each with indentation.'''

        #root = Directory(d, os.path.getsize(d))

        for filename in os.listdir(self.key):
            subitem = os.path.join(self.key, filename)
            #if str subitem is a directory, add the subroot of its files trees
            #recursively
            if os.path.isdir(subitem):
                subitem = Directory(subitem)
                subitem.build_tree()
                self.children.append(subitem)
            else:
                next = File(subitem)
                self.children.append(next)


    def fix_sizes(self):
        '''Add the sizes of all subchildren to root'''

        for child in self.children:
            if isinstance(child, Directory):
                child.fix_sizes()
            self.size += child.size


    def get_rect(self, coord, dims):
        '''(2-tuple of ints, 2-tuple of ints, Node) -> list of tuples
        coord is the top left coordinates, dims is (width, height), root
        is the root of the subtree containing the directory and files of this
        directory'''
        coord = list(coord)

        if dims[1] >= dims[0]:
            div = dims[0]
            other = dims[1]
            inc = [1, 0]
        else:
            div = dims[1]
            other = dims[0]
            inc = [0, 1]

        for child in self.children:
            sub1 = (child.size / float(self.size)) * other
            child.x = coord[0]
            child.y = coord[1]

            if div == dims[0]:
                child.height = div
                child.width = sub1

            else:
                child.height = sub1
                child.width = div

            coord[0] += sub1 * inc[0]
            coord[1] += sub1 * inc[1]

    def get_names(self, count, names):

        names.append("            " * count + self.shortname)
        count += 1
        for item in self.children:
            names += (item.get_names(count, []))
        return names


class File(Directory):
    '''a file'''

    def __init__(self, k):
        '''(File, str, 3-tuple of ints, int) -> NoneType'''

        Directory.__init__(self, k)
        self.color = (randint(0, 255), randint(0, 255), randint(0, 255))
