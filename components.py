from fasthtml.common import *
from dataclasses import dataclass


@dataclass
class ProjectCard:
    icon: str
    title: str
    description: str
    endpoint: str

    def __ft__(self):
        return Div(
            A(
                Div(
                    Div(self.icon, cls="text-primary text-2xl mr-3 transition-colors duration-300 group-hover:text-text_primary"),
                    H3(
                        self.title,
                        cls="text-lg font-semibold transition-colors duration-300 group-hover:text-primary",
                    ),
                    cls="flex items-center mb-2",
                ),
                P(self.description, cls="text-sm text-gray-600"),
                href=self.endpoint,  # Use the endpoint for the link
                cls="block",
            ),
            cls="project-card bg-white border border-gray-200 rounded-lg p-4 mb-4 transition-all duration-300 hover:border-primary hover:shadow-md group",
        )