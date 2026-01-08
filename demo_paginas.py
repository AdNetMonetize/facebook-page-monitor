import requests

ACCESS_TOKEN = "EAAUBPMGT5PcBQXv968IIAo1WKLwrzwlWRMYNvyIpoZAhEuTgZCVGEcKbUb9TRVRWXO1DqKYGGNa9ldgkQq0LSpbt7KZAdeD90EfNcRBjLUBGl6DTGX480QBkpgD91NnlEeZBZCHu9ZAH6Pkz7AqMaC0VTu4xwlHljS8gJOWUnUlmYNhRGarKvIXdDbOsG5"

def listar_paginas(token):
    url = "https://graph.facebook.com/v23.0/me/accounts"
    params = {"access_token": token}
    response = requests.get(url, params=params)
    return response.json()

if __name__ == "__main__":
    paginas = listar_paginas(ACCESS_TOKEN)
    print("📋 Páginas administradas pelo usuário:")
    print(paginas)
