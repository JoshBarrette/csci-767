import networkx as nx
import matplotlib.pyplot as plt


def main():
    splitLines = [line.split(", ") for line in open("./graph.csv").read().split("\n")]

    edges = []
    for line in splitLines:
        parentNode = line[0]
        for i in range(1, len(line)):
            childNode = line[i]
            edges.append((parentNode, childNode))

    graph = nx.DiGraph()
    graph.add_edges_from(edges)
    pageRank = nx.pagerank(graph)

    print("Node weights:")
    for nodeName, weight in pageRank.items():
        print(f"{nodeName}: {weight}")

    nx.draw(
        graph,
        nx.planar_layout(graph),
        nodelist=list(pageRank.keys()),
        with_labels=True,
        node_color="red",
        node_size=[weight * 3000 for weight in pageRank.values()],
    )
    plt.show()


if __name__ == "__main__":
    main()
