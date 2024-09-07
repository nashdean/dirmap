# src/dirmapper/formatter/format_instruction.py
from abc import ABC, abstractmethod

class FormatInstruction(ABC):
    @abstractmethod
    def get_instruction(self, output_type) -> str:
        pass

class MinimalistFormatInstruction(FormatInstruction):
    allowed_output_types = ['summary', 'structure']

    def get_instruction(self, output_type) -> str:
        """
        Get the format instruction for the minimalist format.
        """
        if output_type not in self.allowed_output_types:
            raise ValueError(f"Invalid output type: {output_type}")
        
        return (
            f"Format the {output_type} as follows:\n"
            ".git/                          # Git metadata\n"
            ".github/                       # GitHub CI configuration\n"
            "\tworkflows/                   # GitHub Actions workflows\n"
            ".gitignore                     # Files to ignore in Git\n"
            "LICENSE                        # License file\n"
            "Makefile                       # Automation commands\n"
            "pyproject.toml                 # Python project config\n"
            "README.md                      # Project overview\n"
            "requirements.txt               # Python dependencies\n"
            "src/                           # Source code\n"
            "tests/                         # Unit tests"
        )

# Add other format instructions similarly