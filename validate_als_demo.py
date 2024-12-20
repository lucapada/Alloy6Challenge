import requests
import json
API_URL = "http://localhost:8080"  # Replace with the Alloy4Fun API URL

def validate(code):
    """
    Function to validate an Alloy model. This will call the Alloy API (webService).

    :param code: the Alloy code to validate
    :type code: str
    :returns: a JSON file with {success [, errorMessage, errorLocation]}
    :rtype: dict
    """
    payload = {
        "model": code
    }
    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(f"{API_URL}/validate", data=json.dumps(payload), headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"success": False, "errorMessage": str(e)}

# Example usage
if __name__ == "__main__":
    alloy_code = """
    sig Node {
    edges: set Node
    }

    fact "Connected graph" {
    some n: Node | n.*edges = Node
    }

    fact "No self edges" {
    no iden & edges
    } 

    one sig Ball {
    -- note the var
    var loc: Node 
    } 

    pred move[b: Ball, n: Node] {
    n in b.loc.edges
    b.loc' = n
    }

    pred moved[b: Ball] {
    some n: Node | move[b, n]
    }

    pred unchanged[b: Ball] {
    b.loc = b.loc'
    }

    example1: run {
    some b: Ball |
        always moved[b]
    }
    """
    result = validate(alloy_code)
    print(result)