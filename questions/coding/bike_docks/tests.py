from check import eq, raises

NET = {"a": (10, 1), "b": (10, 10), "c": (5, 0)}


def test_p1_rent(sol):
    n = sol.BikeNetwork(NET)
    eq((n.rent("a", "r1"), n.bikes("a")), (True, 0))


def test_p1_rent_empty(sol):
    eq(sol.BikeNetwork(NET).rent("c", "r1"), False)


def test_p1_one_rental_per_rider(sol):
    n = sol.BikeNetwork(NET)
    n.rent("b", "r1")
    eq((n.rent("b", "r1"), n.bikes("b")), (False, 9))


def test_p1_return(sol):
    n = sol.BikeNetwork(NET)
    n.rent("b", "r1")
    eq((n.give_back("c", "r1"), n.bikes("c")), (True, 1))


def test_p1_return_full(sol):
    n = sol.BikeNetwork(NET)
    n.rent("a", "r1")
    eq(n.give_back("b", "r1"), False)


def test_p1_return_without_rental(sol):
    eq(sol.BikeNetwork(NET).give_back("c", "r1"), False)


def test_p1_rent_after_return(sol):
    n = sol.BikeNetwork(NET)
    n.rent("b", "r1"); n.give_back("c", "r1")
    eq(n.rent("b", "r1"), True)


def test_p1_unknown_station(sol):
    raises(KeyError, sol.BikeNetwork(NET).rent, "zz", "r1")


def test_p1_unknown_bikes(sol):
    raises(KeyError, sol.BikeNetwork(NET).bikes, "zz")


def test_p1_overfull_rejected(sol):
    raises(ValueError, sol.BikeNetwork, {"a": (2, 3)})


def test_p1_negative_rejected(sol):
    raises(ValueError, sol.BikeNetwork, {"a": (2, -1)})


def test_p2_simple_plan(sol):
    eq(sol.BikeNetwork(NET).rebalance_plan(), [("b", "c", 1), ("b", "a", 1)])


def test_p2_balanced(sol):
    eq(sol.BikeNetwork({"a": (10, 5), "b": (10, 5)}).rebalance_plan(), [])


def test_p2_multiple_donors(sol):
    net = {"r": (20, 0), "d1": (10, 9), "d2": (10, 10)}
    eq(sol.BikeNetwork(net).rebalance_plan(), [("d2", "r", 2), ("d1", "r", 1)])


def test_p2_not_enough_bikes(sol):
    net = {"r1": (10, 0), "r2": (10, 1), "d": (10, 9)}
    eq(sol.BikeNetwork(net).rebalance_plan(), [("d", "r1", 1)])


def test_p2_does_not_apply(sol):
    n = sol.BikeNetwork(NET)
    n.rebalance_plan()
    eq((n.bikes("b"), n.bikes("c")), (10, 0))


def test_p2_custom_thresholds(sol):
    net = {"a": (10, 4), "b": (10, 6)}
    eq(sol.BikeNetwork(net).rebalance_plan(low=0.5, high=0.5), [("b", "a", 1)])
