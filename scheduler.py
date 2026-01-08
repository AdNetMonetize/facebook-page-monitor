import time
import subprocess

PYTHON_PATH = r"C:\Users\diego\PycharmProjects\Monitoramento de Páginas do Facebook com Alertas no Slack\.venv\Scripts\python.exe"
MAIN_PATH = r"C:\Users\diego\PycharmProjects\Monitoramento de Páginas do Facebook com Alertas no Slack\main.py"


def run_main_every_5_minutes():
    while True:
        print("⏰ Executando main.py...")
        try:
            subprocess.run([PYTHON_PATH, MAIN_PATH], check=True)
            print("✅ Execução concluída.")
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao executar main.py: {e}")

        print("🔄 Aguardando 5 minutos para próxima execução...\n\n\n")
        time.sleep(10)


if __name__ == "__main__":
    run_main_every_5_minutes()
