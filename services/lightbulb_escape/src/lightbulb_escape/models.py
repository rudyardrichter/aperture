import abc
import logging
import random as r
import sys
import typing as t
from dataclasses import dataclass, field

import numpy as np

log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler(sys.stdout))
# run this to enable logging
# logging.root.setLevel(logging.INFO)


class Simulation(abc.ABC):
    @abc.abstractmethod
    def simulate(self) -> int:
        ...

    def simulate_n_runs(self, n: int) -> tuple[float, float]:
        results = [self.simulate() for _ in range(n)]
        return (np.mean(results), np.std(results))


class FlatWithCounter(Simulation):
    def __init__(self, n_prisoners: int) -> None:
        self.n_prisoners = n_prisoners

    def simulate(self) -> int:
        cycles = 0
        counter_count = 1
        lightbulb_on = False
        prisoner_toggled_on_already = set()
        while True:
            cycles += 1
            prisoner = r.randint(0, self.n_prisoners - 1)
            # arbitarily signify 0 as the counter
            match (
                prisoner == 0,
                lightbulb_on,
                prisoner in prisoner_toggled_on_already,
            ):
                case (True, True, _):
                    log.info("█ => ░    Counter +1")
                    lightbulb_on = False
                    counter_count += 1
                case (True, False, _):
                    log.info("░ => ░    Counter in but bulb off")
                case (False, True, False):
                    log.info(f"█ => █    Prisoner {prisoner} can't turn on bulb")
                case (False, False, True):
                    log.info(f"░ => ░    Prisoner {prisoner} already turned on bulb")
                case (False, False, False):
                    log.info(f"░ => ░    Prisoner {prisoner} turned on lightbulb")
                    lightbulb_on = True
                case _:
                    pass
            if counter_count == self.n_prisoners:
                break
        log.info(f"Escaped after {cycles} cycles")
        return cycles


@dataclass
class Prisoner:
    layer: int
    turned_on_bulb: bool = False
    count: int = 1
    pretend_to_be_phases: list[int] = field(default_factory=list)


@dataclass
class PrisonerLeaf(Prisoner):
    pass


@dataclass
class PrisonerAggregator(Prisoner):
    pass


@dataclass
class PrisonerTop(PrisonerAggregator):
    pass


class KTree(Simulation):
    def __init__(
        self,
        n_prisoners: int,
        tree_factor_k: int,
        n_days_per_phase: int,
    ) -> None:
        self.k = tree_factor_k
        self.n_prisoners = n_prisoners
        self.n_days_per_phase = n_days_per_phase
        self._initialize_layers()

    def _initialize_layers(self) -> None:
        # TODO: clean up math
        n_prisoners_at_layer = 1
        total = 1
        while n_prisoners_at_layer * self.k < self.n_prisoners:
            n_prisoners_at_layer *= self.k
            total += n_prisoners_at_layer
        remainder = self.n_prisoners - total
        self.layers: list[list[Prisoner]] = [
            [PrisonerLeaf(layer=0) for _ in range(n_prisoners_at_layer + remainder)]
        ]
        i_layer = 1
        while n_prisoners_at_layer > self.k:
            n_prisoners_at_layer //= self.k
            self.layers.append(
                [PrisonerAggregator(layer=i_layer) for _ in range(n_prisoners_at_layer)]
            )
            i_layer += 1
        self.layers.append([PrisonerTop(layer=i_layer)])
        self.prisoners_flat = [p for layer in self.layers for p in layer]
        self.lightbulb_on = False

    def _choose_random_prisoner(self) -> Prisoner:
        return self.prisoners_flat[r.randint(0, self.n_prisoners - 1)]

    def simulate(self) -> int:
        self._initialize_layers()
        cycles = 0
        n_phases = len(self.layers)
        while True:
            for i_phase in range(n_phases - 1):
                log.info(f"PHASE {i_phase}")
                done, add_cycles = self._simulate_phase(i_phase)
                cycles += add_cycles
                if done:
                    return cycles

    def _simulate_phase(self, i_phase: int) -> tuple[bool, int]:
        done = False
        cycles = 0
        for _ in range(self.n_days_per_phase):
            done = self._simulate_day(i_phase)
            cycles += 1
            if done:
                return (done, cycles)
        # Must take 1 day to reset lightbulb between phases. Today's prisoner
        # then pretends to belong to this phase one additional time
        if self.lightbulb_on:
            self.lightbulb_on = False
            prisoner = self._choose_random_prisoner()
            if (
                prisoner.layer == i_phase + 1
                and prisoner.count < (self.k + 1) ** prisoner.layer
            ):
                new_count = prisoner.count + (self.k + 1) ** (prisoner.layer - 1)
                log.info(f"█ => ░    {prisoner} reset and counted -> {new_count}")
                prisoner.count = new_count
            else:
                prisoner.pretend_to_be_phases.append(i_phase)
                log.info(
                    f"█ => ░    {prisoner} reset bulb betwen phases; backlog {prisoner.pretend_to_be_phases}"
                )
        return (done, cycles + 1)

    def _simulate_day(self, i_phase: int) -> bool:
        """Return true if prisoners escape."""
        prisoner = self._choose_random_prisoner()
        # If this prisoner is meant to re-count in this phase, also turn on bulb
        if i_phase in prisoner.pretend_to_be_phases and not self.lightbulb_on:
            log.info(f"░ => █    {prisoner} pretended to be in layer {i_phase}")
            self.lightbulb_on = True
            prisoner.pretend_to_be_phases.remove(i_phase)
        # Prisoners at layer i_phase turn on bulb if they can be counted
        elif prisoner.layer == i_phase:
            # "Leaf" prisoners are on layer 0 so count 1 satisfies this
            should_turn_on_bulb = prisoner.count == (self.k + 1) ** prisoner.layer
            match (self.lightbulb_on, should_turn_on_bulb, prisoner.turned_on_bulb):
                case (True, True, False):
                    log.debug(f"█ => █    {prisoner} can't turn on bulb")
                case (True, _, _):
                    log.debug(f"█ => █    {prisoner} in, no-op")
                case (False, True, True):
                    log.debug(f"░ => ░    {prisoner} already turned on bulb")
                case (False, True, False):
                    log.info(f"░ => █    {prisoner} turned on bulb")
                    self.lightbulb_on = True
                    prisoner.turned_on_bulb = True
                case _:
                    log.debug(f"░ => ░    {prisoner} in, no-op")
        # Prisoners at layer i_phase + 1 turn off bulb and count
        elif prisoner.layer == i_phase + 1:
            should_turn_off_bulb = prisoner.count < (self.k + 1) ** prisoner.layer
            match (self.lightbulb_on, should_turn_off_bulb):
                case (True, True):
                    new_count = prisoner.count + (self.k + 1) ** (prisoner.layer - 1)
                    log.info(f"█ => ░    {prisoner} count -> {new_count}")
                    prisoner.count = new_count
                    self.lightbulb_on = False
                case (True, False):
                    log.debug(f"█ => █    {prisoner} already full count")
                case (False, _):
                    log.debug(f"░ => ░    {prisoner} can't add count")
        return prisoner.count == self.n_prisoners
