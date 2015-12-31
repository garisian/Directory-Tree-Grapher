# Directory-Tree-Grapher

This program takes a directory and creates a graph based on how much memory each subfile/directory uses. 

The program prompts the user to enter the dimension of the to-be-displayed graph and requests the user to select any valid directory.

The program recursively goes through every file in the directory, taking the allocated memory and draws a rectangle. The ratio between each rectangle's area to it's parent rectangle is the same ratio as the memory it occupies in the directory.

The user is also given options to show a legend of all the file/directories that have been graphed along with the ability to choose whether to display the filename when hovering over the respective colored block.

There is an additional feature allowing the user to "zoom" into a sub directory; essentially making another graph for a new path.
