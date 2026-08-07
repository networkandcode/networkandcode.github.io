import httpx


def fetch_fruits(fruit: str):
    url = f"https://api.example.com/api/fruit/{fruit}"

    with httpx.Client() as client:
        response = client.get(url, timeout=10.0)
        response.raise_for_status()

        fruits_data = response.json()
        return fruits_data


def greet_user(user: str):
    return f"Hello {user}"
