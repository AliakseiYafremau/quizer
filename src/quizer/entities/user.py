from dataclasses import dataclass


@dataclass
class User:
    id: str
    name: str

    def update_name(self, name: str):
        if not isinstance(name, str):
            raise ValueError("Name must be string")
        self.name = name
