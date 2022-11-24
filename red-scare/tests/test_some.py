import networkx as nx

from redscare import Parser, RedScare


def test_P3_0():
    p = Parser("P3-0.txt", "instance-generators/handmade/")
    redscare = RedScare(p.G, p.s, p.t)

    assert not redscare.some()  # not a DAG


def test_P3_1():
    p = Parser("P3-1.txt", "instance-generators/handmade/")
    redscare = RedScare(p.G, p.s, p.t)
    assert not redscare.some()


def test_K3_0():
    p = Parser("K3-0.txt", "instance-generators/handmade/")
    redscare = RedScare(p.G, p.s, p.t)
    assert not redscare.some()  # not a DAG


def test_K3_1():
    p = Parser("K3-1.txt", "instance-generators/handmade/")
    redscare = RedScare(p.G, p.s, p.t)
    assert redscare.some()


def test_K3_2():
    p = Parser("K3-2.txt", "instance-generators/handmade/")
    redscare = RedScare(p.G, p.s, p.t)
    assert not redscare.some()


def test_vipe_1():
    G, s, t = nx.DiGraph(), "0", "3"
    G.add_node("0", red=False)
    G.add_node("1", red=True)
    G.add_node("2", red=False)
    G.add_node("3", red=False)
    G.add_edge("0", "1")
    G.add_edge("1", "2")
    G.add_edge("2", "3")

    redscare = RedScare(G, s, t)
    assert redscare.some()


def test_vipe_2():
    G, s, t = nx.DiGraph(), "0", "3"
    G.add_node("0", red=False)
    G.add_node("1", red=False)
    G.add_node("2", red=True)
    G.add_node("3", red=False)
    G.add_edge("0", "1")
    G.add_edge("1", "2")
    G.add_edge("2", "3")

    redscare = RedScare(G, s, t)
    assert redscare.some()


def test_vipe_3():
    G, s, t = nx.DiGraph(), "0", "3"
    G.add_node("0", red=False)
    G.add_node("1", red=False)
    G.add_node("2", red=False)
    G.add_node("3", red=False)
    G.add_edge("0", "1")
    G.add_edge("1", "2")
    G.add_edge("2", "3")

    redscare = RedScare(G, s, t)
    assert not redscare.some()


def test_vipe_4():
    G, s, t = nx.DiGraph(), "0", "3"
    G.add_node("0", red=False)
    G.add_node("1", red=True)
    G.add_node("2", red=True)
    G.add_node("3", red=False)
    G.add_edge("0", "1")
    G.add_edge("1", "2")
    G.add_edge("2", "3")

    redscare = RedScare(G, s, t)
    assert redscare.some()
