import abc
import logging
import sys
import typing as t

import numpy as np

log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler(sys.stdout))
# logging.root.setLevel(logging.INFO)


class Solution(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def for_n_prisoners(cls, n: int) -> "Solution":
        """Construct an instance of this solver for n prisoners."""

    @property
    @abc.abstractmethod
    def n_prisoners(self) -> int:
        """Return the number of prisoners this instance is for."""

    @abc.abstractmethod
    def guesses(self, answers: np.ndarray, i_prisoner: int) -> np.ndarray:
        """Return an array with the given prisoner's guesses."""

    def _check_prisoner_i(
        self,
        answers: np.ndarray,
        i_prisoner: int,
    ) -> bool:
        """Return whether the given prisoner guesses correctly."""
        return (answers[self.guesses(answers, i_prisoner)] == i_prisoner).any()

    def simulate(self) -> bool:
        """Return true if prisoners escape."""
        answers = np.random.permutation(range(self.n_prisoners))
        guesses = np.array([self.guesses(answers, i) for i in range(self.n_prisoners)])
        log.info(f"answers: {answers}")
        for i, guess in enumerate(guesses):
            log.info(f"{i}: {guess}")
        return all(self._check_prisoner_i(answers, i) for i in range(self.n_prisoners))

    def simulate_n_times(self, n: int) -> float:
        return [self.simulate() for _ in range(n)].count(True) / float(n)


class IterateAdd(Solution):
    def __init__(self, n: int) -> None:
        self._n_prisoners = n

    @classmethod
    def for_n_prisoners(cls, n: int) -> "IterateAdd":
        return cls(n)

    @property
    def n_prisoners(self) -> int:
        return self._n_prisoners

    def guesses(self, answers: np.ndarray, i_prisoner: int) -> np.ndarray:
        result = [i_prisoner]
        # # this one equates to evenly distributed:
        # while len(result) < self._n_prisoners // 2:
        #     guess = result[-1]
        #     while guess in result:
        #         guess = (guess + answers[result[-1]] + 1) % self._n_prisoners
        #         if guess in result:
        #             while guess in result:
        #                 guess = (guess + 1) % self._n_prisoners
        #     result.append(guess)
        # so does this one:
        while len(result) < self._n_prisoners // 2:
            guess = (sum(result) + answers[result[-1]]) % self._n_prisoners
            while guess in result:
                guess = (guess + 1) % self._n_prisoners
            result.append(guess)
        return np.array(result, dtype=int)


class FollowIndex(Solution):
    def __init__(self, n: int) -> None:
        self._n_prisoners = n

    @classmethod
    def for_n_prisoners(cls, n: int) -> "FollowIndex":
        return cls(n)

    @property
    def n_prisoners(self) -> int:
        return self._n_prisoners

    def guesses(self, answers: np.ndarray, i_prisoner: int) -> np.ndarray:
        result = [i_prisoner]
        while len(result) < self._n_prisoners // 2:
            guess = answers[result[-1]]
            while guess in result:
                guess = (guess + 1) % self._n_prisoners
            result.append(guess)
        return np.array(result, dtype=int)
