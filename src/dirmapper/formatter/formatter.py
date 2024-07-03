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
