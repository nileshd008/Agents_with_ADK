

from __future__ import annotations
from dotenv import load_dotenv
import ast
import operator as op

from typing import Any, Dict
from google.adk.agents import LlmAgent, Agent, BaseAgent

from google.adk.a2a.utils.agent_to_a2a import to_a2a

load_dotenv()
import os

print(os.getenv('GOOGLE_API_KEY'))

_ALLOWED_BINOPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow
}

_ALLOWED_UNARYOPS = {
    ast.UAdd: op.pos,
    ast.USub: op.neg
}

def _eval_expr(node: ast.AST) -> float:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)
    
    if isinstance(node, ast.BinOp):
        op_type =  type(node.op) 
        if op_type not in _ALLOWED_BINOPS:
            raise ValueError(f"operator not allowed {op_type.__name__}")
        left = _eval_expr(node.left)
        right = _eval_expr(node.right)

        if op_type is ast.Pow and abs(right) > 1000:
            raise ValueError('Exponent too large')

        return float(_ALLOWED_BINOPS[type(node.op)])(left, right)
    
    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in _ALLOWED_UNARYOPS:
            raise ValueError(f"Unary operator not allowed: {op_type.__name__}")
        operand = _eval_expr(node.operand)
        return float(_ALLOWED_UNARYOPS[type(node.op)])(operand)
    
    raise ValueError('Unsupported expression')

def safe_calculation(expression: str):
    """
    Evaluate a simple arithmatic expression safely.
    Supported: +, -, *, /, //, %, **, parentheses, unary +/-.
    """
    try:
        parsed = ast.parse(expression, mode = 'eval')
        result = _eval_expr(parsed.body)
        return {'expression': expression, 'result': result}
    except Exception as e:
        return {'expression': expression, 'error': str(e)}
    

root_agent = Agent(
    model = 'gemini-2.5-flash',
    name = 'math_agent',
    description = "Remote A2A agent that evaluates arithmatic expression safely",
    instruction = """
    You are MathAgent, For any calculation request, ALWAYS call tool `safety_calculation` and return result.
    After receiving tool result, you MUST respond with finl plain-text answer.
    never end your response with only a tool call.
""",
   tools = [safe_calculation]
)
    

#a2a_app = to_a2a(remote_agent, port = 8001)