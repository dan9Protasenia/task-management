from abc import ABC, abstractmethod


class AbstractRepository(ABC):
    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_by_id(self, project_id):
        pass

    @abstractmethod
    def create(self, project):
        pass

    @abstractmethod
    def update(self, project):
        pass

    @abstractmethod
    def delete(self, project):
        pass
