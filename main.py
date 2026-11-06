from mcp.server.mcpserver import MCPServer

server = MCPServer("job-tracker")

@server.tool()
async def ping() -> str:
    """Check that the job-tracker server is reachable.

    Returns:
        'pong'.
    """
    return "pong"
    
if __name__ == "__main__":
    server.run()