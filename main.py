import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import networkx as nx
import rbt_object


def print_tree_graphic(nodes, edges):
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


def print_tree_console(nodes, edges):
    key = nodes[0].get_key()
    print(key)

    cur_level = [key]
    next_level = []
    line = ''

    for edge in edges:
        if edge[0] in cur_level:
            line += str(edge[1]) + '\t'
            next_level += [edge[1]]
        else:
            print(line)
            line = str(edge[1]) + '\t'
            cur_level = next_level
            next_level = [edge[1]]
    print(line)
    print('\n')


def main():

    tree = rbt_object.RedBlackTree(12)

    nodes, edges = tree.export()
    # print_tree_graphic(nodes, edges)
    print_tree_console(nodes, edges)

    tree.insert_node(7)
    tree.insert_node(6)
    tree.insert_node(5)
    tree.insert_node(15)

    nodes, edges = tree.export()
    # print_tree_graphic(nodes, edges)
    print_tree_console(nodes, edges)

    tree.delete_node(tree.search(5))
    tree.delete_node(tree.search(12))

    nodes, edges = tree.export()
    # print_tree_graphic(nodes, edges)
    print_tree_console(nodes, edges)

    tree.insert_node(23)
    tree.insert_node(27)
    tree.insert_node(32)
    tree.insert_node(2)

    nodes, edges = tree.export()
    # print_tree_graphic(nodes, edges)
    print_tree_console(nodes, edges)

    print('Complete :3')


if __name__ == '__main__':
    main()
