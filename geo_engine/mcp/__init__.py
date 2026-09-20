"""
Model Context Protocol (MCP) Server for Geo-Engine.
Enables external LLM agents to invoke live engine capabilities via standard JSON-RPC 2.0 over stdio.
"""

from .server import GeoEngineMCPServer, run_stdio_server

__all__ = ["GeoEngineMCPServer", "run_stdio_server"]
