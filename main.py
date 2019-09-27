import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import networkx as nx
import rbt_object

from colorama import init, Fore, Style


def print_tree_graphic(tree):
    nodes, edges = tree.export()
    g = nx.DiGraph()
    for node in nodes:
        color = node.get_color().lower()
        g.add_node(str(node.get_key()), color=color, shape='circle')
    for edge in edges:
        if edge[0] >= 0 and edge[1] >= 0:
            g.add_edge(str(edge[0]), str(edge[1]), color='black')
    a = nx.nx_agraph.to_agraph(g)
    a.layout('dot')
    a.draw('out.png')
    img = mpimg.imread('out.png')
    plt.imshow(img)
    plt.show()


def print_tree_console(tree):
    nodes, edges = tree.export()
    key = nodes[0].get_key()
    if nodes[0].get_color() == 'RED':
        print(Fore.RED + str(key) + Style.RESET_ALL)
    else:
        print(str(key))

    cur_level = [key]
    next_level = []

    for edge in edges:
        if edge[0] in cur_level:
            if edge[1] != -1:
                if tree.search(edge[1]).get_color() == 'RED':
                    print(Fore.RED + str(edge[1]) + Style.RESET_ALL, end='\t')
                else:
                    print(str(edge[1]), end='\t')
            else:
                print(str(edge[1]), end='\t')
            next_level += [edge[1]]
        else:
            print('\n', end='')
            if edge[1] != -1:
                if tree.search(edge[1]).get_color() == 'RED':
                    print(Fore.RED + str(edge[1]) + Style.RESET_ALL, end='\t')
                else:
                    print(str(edge[1]), end='\t')
            else:
                print(str(edge[1]), end='\t')
            cur_level = next_level
            next_level = [edge[1]]
    print('\n')


def main():
    init(convert=True)
    tree = rbt_object.RedBlackTree(12)

    # print_tree_graphic(tree)
    print_tree_console(tree)

    tree.insert_node(7)
    tree.insert_node(6)
    tree.insert_node(5)
    tree.insert_node(15)

    # print_tree_graphic(tree)
    print_tree_console(tree)

    tree.delete_node(tree.search(5))
    tree.delete_node(tree.search(12))

    # print_tree_graphic(tree)
    print_tree_console(tree)

    tree.insert_node(23)
    tree.insert_node(27)
    tree.insert_node(32)
    tree.insert_node(2)

    # print_tree_graphic(tree)
    print_tree_console(tree)

    print('Complete :3')


if __name__ == '__main__':
    main()
