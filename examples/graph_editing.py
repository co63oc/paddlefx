import paddle

from paddlefx import symbolic_trace


def net(x, y):
    return x + y


traced_layer = symbolic_trace(net)
graph = traced_layer.graph

print("Before editing:")
graph.print_tabular()

for node in graph.nodes:
    if node.op == 'call_function':
        break

with graph.inserting_after(node):
    new_node = graph.create_node(
        node.op, paddle.add, args=(node.args[0], node.args[0]), kwargs={}
    )
    node.replace_all_uses_with(new_node)
graph.erase_node(node)

print("After editing:")
graph.print_tabular()