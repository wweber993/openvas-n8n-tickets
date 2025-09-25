import socket
import requests
import csv
import io
import json

# Configurações
HOST = "0.0.0.0"   # escuta em todas as interfaces do proxy
PORT = 6000        # porta que o Greenbone vai enviar os relatórios
N8N_WEBHOOK = "http://192.168.10.48:5678/webhook/openvas"  # Webhook do n8n

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"[+] Proxy aguardando conexões em {HOST}:{PORT}")

    while True:
        conn, addr = s.accept()
        data = conn.recv(65535)
        if data:
            try:
                # Decodifica os bytes recebidos para string CSV
                csv_data = data.decode("utf-8", errors="ignore")

                # Lê CSV em memória e transforma em lista de dicionários
                reader = csv.DictReader(io.StringIO(csv_data))
                rows = list(reader)

                # Envia pro n8n em JSON
                res = requests.post(N8N_WEBHOOK, json=rows)

                print(f"[+] Recebidos {len(data)} bytes de {addr[0]}, convertidos para {len(rows)} registros e enviados ao n8n (status={res.status_code})")
            except Exception as e:
                print(f"[!] Erro ao converter/enviar: {e}")
        conn.close()
