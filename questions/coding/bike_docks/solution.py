import math


class BikeNetwork:
    """Dock stations with rentals and a rebalancing planner."""

    def __init__(self, stations):
        self.cap, self.n, self.active = {}, {}, set()
        for sid, (cap, bikes) in stations.items():
            if cap < 0 or bikes < 0 or bikes > cap:
                raise ValueError(f"bad station {sid}")
            self.cap[sid], self.n[sid] = cap, bikes

    def _known(self, station):
        if station not in self.cap:
            raise KeyError(station)

    def bikes(self, station):
        self._known(station)
        return self.n[station]

    def rent(self, station, rider):
        self._known(station)
        if self.n[station] == 0 or rider in self.active:
            return False
        self.n[station] -= 1
        self.active.add(rider)
        return True

    def give_back(self, station, rider):
        self._known(station)
        if rider not in self.active or self.n[station] >= self.cap[station]:
            return False
        self.n[station] += 1
        self.active.discard(rider)
        return True

    def rebalance_plan(self, low=0.2, high=0.8):
        fill = {s: self.n[s] / self.cap[s] for s in self.cap if self.cap[s]}
        give = {s: self.n[s] - math.floor(high * self.cap[s]) for s in fill if fill[s] > high}
        want = {s: math.ceil(low * self.cap[s]) - self.n[s] for s in fill if fill[s] < low}
        donors = sorted(give, key=lambda s: (-fill[s], s))
        moves = []
        for r in sorted(want, key=lambda s: (fill[s], s)):
            for d in donors:
                k = min(want[r], give[d])
                if k > 0:
                    moves.append((d, r, k))
                    want[r] -= k
                    give[d] -= k
        return moves
