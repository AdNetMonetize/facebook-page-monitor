# utils/errors.py
import time
import requests

DEFAULT_RETRIES = 3
DEFAULT_DELAY = 2
DEFAULT_TIMEOUT = 10

def is_retryable_status(status_code: int) -> bool:
    """Define status HTTP que merecem retry (erros de servidor/infra)."""
    return status_code in {500, 502, 503, 504}

def call_api_with_retry(url: str, params: dict, retries: int = DEFAULT_RETRIES,
                        delay: int = DEFAULT_DELAY, timeout: int = DEFAULT_TIMEOUT):
    """
    Faz GET com retries simples para erros de rede e 5xx.
    Retorna resp.json() em caso de sucesso, ou None se todas tentativas falharem.
    """
    last_error = None

    for attempt in range(1, retries + 1):
        try:
            resp = requests.get(url, params=params, timeout=timeout)

            if resp.status_code == 200:
                return resp.json()

            if resp.status_code == 429:
                # Rate limit: aumente o delay para evitar loop agressivo
                print(f"Rate limit na tentativa {attempt}: {resp.text}")
                time.sleep(max(delay, 5))
            elif is_retryable_status(resp.status_code):
                print(f"Erro {resp.status_code} na tentativa {attempt}, retry em {delay}s")
                time.sleep(delay)
            else:
                # 4xx normalmente não são recuperáveis via retry
                print(f"Falha não recuperável ({resp.status_code}): {resp.text}")
                return None

        except requests.exceptions.RequestException as e:
            last_error = e
            print(f"Erro de rede na tentativa {attempt}: {e}. Retry em {delay}s")
            time.sleep(delay)

    print(f"Todas as tentativas falharam. Último erro: {last_error}")
    return None
