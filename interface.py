import tkinter as tk
from tkinter import messagebox
import mysql.connector

def verificar_placa():
    placa = entry_placa.get().strip().upper()
    if not placa:
        messagebox.showwarning("Aviso", "Digite uma placa.")
        return

    try:
        conn = mysql.connector.connect(
            host="localhost",
            port=3307,
            user="root",
            password="root",
            database="placas_ia"
        )
        cursor = conn.cursor()
        # Verifica se a placa existe
        cursor.execute("SELECT COUNT(*) FROM placa WHERE id = %s", (placa,))
        existe = cursor.fetchone()[0]
        if existe:
            # Busca os nomes dos motoristas associados à placa
            cursor.execute("""
                SELECT m.nome
                FROM motorista m
                JOIN motorista_placa mp ON m.id = mp.motorista_id
                WHERE mp.placa_id = %s
            """, (placa,))
            motoristas = cursor.fetchall()
            if motoristas:
                nomes = "\n".join(nome for (nome,) in motoristas)
                messagebox.showinfo("Motoristas", f"Placa {placa} encontrada.\nMotoristas:\n{nomes}")
            else:
                messagebox.showinfo("Motoristas", f"Placa {placa} encontrada, mas sem motoristas associados.")
        else:
            messagebox.showinfo("Resultado", f"A placa {placa} NÃO foi encontrada.")
    except mysql.connector.Error as err:
        messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados:\n{err}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()

root = tk.Tk()
root.title("Verificar Placa de Veículo")
root.geometry("300x200")

frame = tk.Frame(root)
frame.pack(expand=True, fill="both")  # Centraliza o frame na janela

tk.Label(frame, text="Digite a placa:").pack(padx=10, pady=5)
entry_placa = tk.Entry(frame)
entry_placa.pack(padx=10, pady=5)

btn_verificar = tk.Button(frame, text="Verificar", command=verificar_placa)
btn_verificar.pack(padx=10, pady=10)

root.mainloop()