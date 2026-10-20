import time

from check import eq, raises


def test_p1_hit(sol):
    c = sol.LRUCache(2)
    c.put("a", 1)
    eq(c.get("a"), 1)


def test_p1_miss(sol):
    eq(sol.LRUCache(2).get("a"), None)


def test_p1_evicts_lru(sol):
    c = sol.LRUCache(2)
    c.put("a", 1); c.put("b", 2); c.put("c", 3)
    eq((c.get("a"), c.get("b"), c.get("c")), (None, 2, 3))


def test_p1_get_refreshes(sol):
    c = sol.LRUCache(2)
    c.put("a", 1); c.put("b", 2); c.get("a"); c.put("c", 3)
    eq((c.get("a"), c.get("b")), (1, None))


def test_p1_put_refreshes(sol):
    c = sol.LRUCache(2)
    c.put("a", 1); c.put("b", 2); c.put("a", 10); c.put("c", 3)
    eq((c.get("a"), c.get("b")), (10, None))


def test_p1_len(sol):
    c = sol.LRUCache(3)
    for k in "abcde":
        c.put(k, k)
    eq(len(c), 3)


def test_p1_bad_capacity(sol):
    raises(ValueError, sol.LRUCache, 0)


def test_p1_fast(sol):
    c = sol.LRUCache(1000)
    t0 = time.perf_counter()
    for i in range(50000):
        c.put(i % 1500, i)
        c.get(i % 700)
    eq(time.perf_counter() - t0 < 1.0, True, msg="100k ops should take well under a second")


def test_p2_fresh(sol):
    c = sol.TTLCache(2, 10)
    c.put("a", 1, 0)
    eq(c.get("a", 9.9), 1)


def test_p2_expired(sol):
    c = sol.TTLCache(2, 10)
    c.put("a", 1, 0)
    eq(c.get("a", 10), None)


def test_p2_read_does_not_extend(sol):
    c = sol.TTLCache(2, 10)
    c.put("a", 1, 0); c.get("a", 9)
    eq(c.get("a", 11), None)


def test_p2_put_resets_ttl(sol):
    c = sol.TTLCache(2, 10)
    c.put("a", 1, 0); c.put("a", 2, 8)
    eq(c.get("a", 15), 2)


def test_p2_expired_dropped_before_lru(sol):
    c = sol.TTLCache(2, 10)
    c.put("old", 1, 0); c.put("b", 2, 5); c.get("old", 6); c.put("c", 3, 12)
    eq((c.get("b", 12), c.get("c", 12)), (2, 3))


def test_p2_lru_when_nothing_expired(sol):
    c = sol.TTLCache(2, 100)
    c.put("a", 1, 0); c.put("b", 2, 1); c.get("a", 2); c.put("c", 3, 3)
    eq((c.get("a", 4), c.get("b", 4)), (1, None))


def test_p2_stats(sol):
    c = sol.TTLCache(2, 10)
    c.put("a", 1, 0); c.get("a", 1); c.get("a", 20); c.get("zz", 1)
    eq(c.stats(), {"hits": 1, "misses": 2})
