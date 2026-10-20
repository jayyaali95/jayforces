import time

from check import eq, raises


def books(cal, pairs):
    return [cal.book(s, e) for s, e in pairs]


def test_p1_basic(sol):
    eq(books(sol.Calendar(), [(10, 20), (15, 25), (20, 30)]), [True, False, True])


def test_p1_touching(sol):
    eq(books(sol.Calendar(), [(1, 3), (3, 5), (0, 1)]), [True, True, True])


def test_p1_inside(sol):
    eq(books(sol.Calendar(), [(0, 10), (2, 3)]), [True, False])


def test_p1_covering(sol):
    eq(books(sol.Calendar(), [(2, 3), (0, 10)]), [True, False])


def test_p1_sorted_bookings(sol):
    c = sol.Calendar()
    books(c, [(5, 6), (1, 2), (3, 4)])
    eq(c.bookings(), [(1, 2), (3, 4), (5, 6)])


def test_p1_invalid(sol):
    raises(ValueError, sol.Calendar().book, 5, 5)


def test_p1_failed_not_stored(sol):
    c = sol.Calendar()
    books(c, [(0, 5), (4, 8)])
    eq(c.bookings(), [(0, 5)])


def test_p1_fast(sol):
    c = sol.Calendar()
    t0 = time.perf_counter()
    for i in range(2000):
        c.book(i * 2, i * 2 + 1)
        c.book(i * 2, i * 2 + 3)
    eq((len(c.bookings()), time.perf_counter() - t0 < 1), (2000, True))


def test_p2_double(sol):
    eq(books(sol.PoolCalendar(2), [(10, 20), (15, 25), (18, 22)]), [True, True, False])


def test_p2_disjoint_overlaps_ok(sol):
    eq(books(sol.PoolCalendar(2), [(0, 10), (0, 3), (5, 10)]), [True, True, True])


def test_p2_triple_at_point(sol):
    eq(books(sol.PoolCalendar(2), [(0, 10), (5, 15), (9, 11)]), [True, True, False])


def test_p2_touching_pool(sol):
    eq(books(sol.PoolCalendar(1), [(0, 5), (5, 10), (2, 3)]), [True, True, False])


def test_p2_three_cars(sol):
    eq(books(sol.PoolCalendar(3), [(0, 9)] * 4), [True, True, True, False])


def test_p3_cancel(sol):
    c = sol.Calendar()
    books(c, [(0, 5)])
    eq((c.cancel(0, 5), c.book(1, 2)), (True, True))


def test_p3_cancel_missing(sol):
    eq(sol.Calendar().cancel(0, 5), False)


def test_p3_pool_cancel(sol):
    p = sol.PoolCalendar(1)
    books(p, [(0, 5)])
    eq((p.cancel(0, 5), p.cancel(0, 5), p.book(0, 5)), (True, False, True))


def test_p3_free(sol):
    c = sol.Calendar()
    books(c, [(2, 4), (6, 7)])
    eq(c.free(0, 10), [(0, 2), (4, 6), (7, 10)])


def test_p3_free_clipped(sol):
    c = sol.Calendar()
    books(c, [(0, 4), (8, 12)])
    eq(c.free(2, 10), [(4, 8)])


def test_p3_free_none(sol):
    c = sol.Calendar()
    books(c, [(0, 10)])
    eq(c.free(0, 10), [])
