from google.adk.agents import Agent
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from google.adk.tools.tool_context import ToolContext


def check_prime(tool_context: ToolContext, nums: list[int]):

    def is_prime(n: int)-> bool:
        if n <= 1:
            return False
        
        if n <=3:
            return True
        
        if n%2 == 0 or n%3 == 0:
            return False
        
        i = 5
        while i*i <= n:
            if n%i == 0 or n % (i+2) == 0:
                return False
            
            i += 6
        
        return True
    
    result = []

    for n in nums:
        result.append(f"{n}: {'prime' if is_prime(n) else 'not prime'}")
    
    return "; ".join(result)


root_agent = Agent(
    name = 'check_prime_agent',
    model = 'gemini-2.5-flash',
    description = 'Checks weather given integers are prime',
    tools = [check_prime],
    instruction = """
        You are a prime-checking specialist.
        Given a number, you will check all primary numbers present upto that number.
    """,
)

#a2a_app = to_a2a(prime_agent, port = 8081)