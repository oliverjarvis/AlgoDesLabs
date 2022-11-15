from redscare import Parser, RedScare


def test_P3_0():
    p = Parser("P3-0.txt", "instance-generators/handmade/")
    redscare = RedScare(p.G, p.s, p.t)
    assert redscare.some()


def test_P3_1():
    p = Parser("P3-1.txt", "instance-generators/handmade/")
    redscare = RedScare(p.G, p.s, p.t)
    assert not redscare.some()


def test_K3_0():
    p = Parser("K3-0.txt", "instance-generators/handmade/")
    redscare = RedScare(p.G, p.s, p.t)
    assert redscare.some()


def test_K3_1():
    p = Parser("K3-1.txt", "instance-generators/handmade/")
    redscare = RedScare(p.G, p.s, p.t)
    assert redscare.some()


def test_K3_2():
    p = Parser("K3-2.txt", "instance-generators/handmade/")
    redscare = RedScare(p.G, p.s, p.t)
    assert not redscare.some()
