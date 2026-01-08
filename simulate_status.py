import sqlite3
import json

DB_PATH = "states.db"
PAGE_ID = "1009328928911914"

def simulate_change(new_values: dict):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Busca o JSON atual
    cursor.execute("SELECT state_json FROM page_states WHERE page_id = ?", (PAGE_ID,))
    row = cursor.fetchone()

    if not row:
        print("❌ Nenhum estado encontrado para essa página.")
        return

    current_state = json.loads(row[0])

    # Atualiza os campos desejados
    current_state.update(new_values)

    # Salva de volta no banco
    cursor.execute(
        "UPDATE page_states SET state_json = ? WHERE page_id = ?",
        (json.dumps(current_state, ensure_ascii=False), PAGE_ID)
    )

    conn.commit()
    conn.close()
    print(f"✅ Estado da página {PAGE_ID} atualizado com {new_values}")

if __name__ == "__main__":
    print("Escolha uma opção de simulação:")
    print("1 - Bloquear página")
    print("2 - Restringir página")
    print("3 - Desativar página")
    print("4 - Ativar página")

    choice = input("Digite o número da opção: ")

    if choice == "1":
        simulate_change({"verification_status": "disabled"})
    elif choice == "2":
        simulate_change({"verification_status": "unverified"})
    elif choice == "3":
        simulate_change({"is_published": False})
    elif choice == "4":
        simulate_change({"is_published": True})
    else:
        print("❌ Opção inválida.")
