from abc import ABCMeta, abstractmethod
from optimeed.core.options import Option_class


class InterfaceObjCons(Option_class, metaclass=ABCMeta):
    """Interface class for objectives and constraints. The objective is to MINIMIZE and the constraint has to respect VALUE <= 0"""

    @abstractmethod
    def compute(self, theMachine):
        """
        Get the value of the objective or the constraint. The objective is to MINIMIZE and the constraint has to respect VALUE <= 0

        :param theMachine: Input machine that has already been evaluated
        :return: float.
        """
        pass

    def get_name(self):
        return "Objective / constraint"

    def __str__(self):
        return self.get_name()
