from check import eq, raises, table

table(globals(), 1, lambda s, c: s.is_valid_code(c), [
    ("simple", "RIDE20", True), ("lowercase ok", "ride20", True), ("whitespace stripped", "  RIDE20 ", True),
    ("too short", "R2", False), ("too long", "RIDE2024SPRING", False), ("no digit", "RIDEFREE", False),
    ("no letter", "202420", False), ("starts with digit", "2RIDES", False), ("symbol", "RIDE-20", False),
    ("not a string", 123456, False), ("twelve chars", "ABCDEFGHIJK1", True),
])
table(globals(), 1, lambda s, c: s.normalize(c), [
    ("normalize", " ride20 ", "RIDE20"), ("normalize invalid", "bad", ValueError),
])


def book(sol):
    b = sol.PromoBook()
    b.create("RIDE20", 2, 100)
    return b


def test_p2_redeem_once(sol):
    eq(book(sol).redeem("ride20", "u1", 10), True)


def test_p2_same_user_twice(sol):
    b = book(sol)
    b.redeem("RIDE20", "u1", 10)
    eq(b.redeem("RIDE20", "u1", 11), False)


def test_p2_max_uses(sol):
    b = book(sol)
    eq([b.redeem("RIDE20", u, 1) for u in ("u1", "u2", "u3")], [True, True, False])


def test_p2_expired(sol):
    eq(book(sol).redeem("RIDE20", "u1", 100), False)


def test_p2_unknown_code(sol):
    eq(book(sol).redeem("OTHER1", "u1", 1), False)


def test_p2_invalid_code_is_false(sol):
    eq(book(sol).redeem("??", "u1", 1), False)


def test_p2_duplicate_create(sol):
    raises(ValueError, book(sol).create, " ride20", 5, 10)


def test_p2_create_invalid(sol):
    raises(ValueError, sol.PromoBook().create, "x", 5, 10)


def test_p2_failed_redeem_does_not_count(sol):
    b = book(sol)
    b.redeem("RIDE20", "u1", 500)
    eq([b.redeem("RIDE20", u, 1) for u in ("u1", "u2")], [True, True])
