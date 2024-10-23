# function_mappings.py
function_mappings = {
    "Well_informed": {
        "type": "function",
        "function": {
            "name": "do_WebSearch",
            "description": "do web search if you don't know about the information",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query"
                    }
                },
                "required": ["query"]
            }
        }
    },
    "Human_temperature": {
        "type": "function",
        "function": {
            "name": "get_temperature",
            "description": "get current temperature",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    "Human_timer": {
        "type": "function",
        "function": {
            "name": "get_time",
            "description": "get current time",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
    
    # Add more mappings as needed
}
