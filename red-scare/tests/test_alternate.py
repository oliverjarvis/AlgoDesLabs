import networkx as nx

from redscare import Parser, RedScare


def test_vipe_1():
    """0->1R->2->3R"""
    G, s, t = nx.DiGraph(), "0", "3"
    G.add_node("0", red=False)
    G.add_node("1", red=True)
    G.add_node("2", red=False)
    G.add_node("3", red=True)
    G.add_edge("0", "1")
    G.add_edge("1", "2")
    G.add_edge("2", "3")

    redscare = RedScare(G, s, t)
    assert redscare.alternate()


def test_vipe_2():
    """0->1->2R->3"""
    G, s, t = nx.DiGraph(), "0", "3"
    G.add_node("0", red=False)
    G.add_node("1", red=False)
    G.add_node("2", red=True)
    G.add_node("3", red=False)
    G.add_edge("0", "1")
    G.add_edge("1", "2")
    G.add_edge("2", "3")

    redscare = RedScare(G, s, t)
    assert not redscare.alternate()


def test_vipe_3():
    """0->1->2->3"""
    G, s, t = nx.DiGraph(), "0", "3"
    G.add_node("0", red=False)
    G.add_node("1", red=False)
    G.add_node("2", red=False)
    G.add_node("3", red=False)
    G.add_edge("0", "1")
    G.add_edge("1", "2")
    G.add_edge("2", "3")

    redscare = RedScare(G, s, t)
    assert not redscare.alternate()


def test_vipe_4():
    """0->1R->2R->3"""
    G, s, t = nx.DiGraph(), "0", "3"
    G.add_node("0", red=False)
    G.add_node("1", red=True)
    G.add_node("2", red=True)
    G.add_node("3", red=False)
    G.add_edge("0", "1")
    G.add_edge("1", "2")
    G.add_edge("2", "3")

    redscare = RedScare(G, s, t)
    assert not redscare.alternate()
