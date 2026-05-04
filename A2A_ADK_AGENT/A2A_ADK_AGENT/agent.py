
from __future__ import annotations

from google.adk.agents.llm_agent import Agent

import warnings
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent, AGENT_CARD_WELL_KNOWN_PATH
warnings.filterwarnings("ignore", category=UserWarning, module=".*google\\.adk.*")

rp = "http://localhost:8001"

math_remote = RemoteA2aAgent(
    name = 'math_remote',
    description = "remote math (A2A) agent that evelautes arithmatic expressions",
    agent_card = f"{rp}{AGENT_CARD_WELL_KNOWN_PATH}"
)

root_agent = Agent(
    model = "gemini-2.5-flash",
    name = "host_agent",
    description = 'Host ADK Agent that delegates math to as remote A2A agent',
    instruction = """
you are HostAgent. if the user asks for any calculation or expresison evaluation, delegate to sub-agent `math_remote`. otherwise, answer normally.

""",
sub_agents =[math_remote]
)