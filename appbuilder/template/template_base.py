import os
from appbuilder.core.agent import AgentRuntime

class AppTemplateBase(AgentRuntime):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    pass