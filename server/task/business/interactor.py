from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date
from typing import Type, Tuple

from .repository import TaskRepository, Task, Category


@dataclass
class TaskInputData:
    """Input DTO to service with contain data of the task"""
    name: str
    description: str
    deadline: date
    category_id: int = ...


class TaskInteractor(ABC):
    """Interface of interaction with task business logics"""

    def __init__(self, repository: Type[TaskRepository]):
        self.tasks = repository()

    @abstractmethod
    def get(self, identity: int, account_id: int) -> Task:
        """Getting Task from system.
        :raises NotFoundError: the Task by ID associated with the Account was not found."""

    @abstractmethod
    def get_by_category(self, category_id: int, account_id: int) -> Tuple[Task, ...]:
        """Get tasks from category.
        :raises NotFoundError: the Category by ID associated with the Account was not found."""

    @abstractmethod
    def get_all(self, account_id: int) -> Tuple[Task, ...]:
        """Get tasks for account.
        :raises NotFoundError: the Account was not found."""

    @abstractmethod
    def create(self, account_id: int, data: TaskInputData) -> int:
        """Create new Task to Category from external data.
        :raises NotFoundError: the Category by ID associated with the Account was not found."""

    @abstractmethod
    def update(self, identity: int, account_id: int, data: TaskInputData) -> None:
        """Updating Task in the system by received data.
        :raises NotFoundError: the Task by ID associated with the Account was not found."""

    @abstractmethod
    def move_to_category(self, identity: int, category_id: int, account_id: int):
        """Move Task to another Category.
        :raises NotFoundError: the Task by ID associated with the Category and Account was not found."""

    @abstractmethod
    def delete(self, identity: int, account_id: int) -> None:
        """Deleting Task from the system.
        :raises NotFoundError: the Task by ID associated with the Account was not found."""
