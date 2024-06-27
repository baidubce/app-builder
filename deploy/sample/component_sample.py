import appbuilder

component = appbuilder.Playground(prompt_template="{query}", model="ERNIE-Bot")
agent = appbuilder.AgentRuntime(component=component)
agent.serve(port=8091)
