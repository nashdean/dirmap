import json
from abc import ABC, abstractmethod

class Formatter(ABC):
    @abstractmethod
    def format(self, data) -> str:
        pass

class PlainTextFormatter(Formatter):
    def format(self, data: str) -> str:
        return data

class HTMLFormatter(Formatter):
    def format(self, data: str) -> str:
        return f"<html><body><pre>{data}</pre></body></html>"

class JSONFormatter(Formatter):
    def format(self, data) -> str:
        # Format the data as JSON
        if isinstance(data, dict):
            return json.dumps(data, indent=4)
        elif isinstance(data, str):
            return json.dumps(json.loads(data), indent=4)
        else:
            raise ValueError("Data must be a dictionary or a JSON string to format as JSON")

class MinimalistFormatter(Formatter):
    def format(self, data: str) -> str:
        # Implement minimalist formatting logic
        return data

# class TabbedListFormatter(Formatter):
#     def format(self, data: str) -> str:
#         # Implement tabbed list formatting logic
#         return data

# class TableFormatter(Formatter):
#     def format(self, data: str) -> str:
#         # Implement table formatting logic
#         return data

# class BulletPointFormatter(Formatter):
#     def format(self, data: str) -> str:
#         # Implement bullet point formatting logic
#         return data

# class TreeFormatter(Formatter):
#     def format(self, data: str) -> str:
#         # Implement tree formatting logic
#         return data
