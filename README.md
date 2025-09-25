# 🔐 Gestão de Vulnerabilidades com Open Source

Este projeto demonstra como montar um **pipeline de gestão de vulnerabilidades** utilizando **ferramentas open source**, com foco em acessibilidade para pequenas e médias empresas (PMEs).

A arquitetura integra:

- **OpenVAS (Greenbone Community Edition)** → Scanner de vulnerabilidades.  
- **n8n** → Orquestrador de automações.  
- **Zammad** → Helpdesk para abertura automática de tickets.  
- **Discord** → Canal de comunicação em tempo real para alertas críticos.  
- **Proxy Python** → Conversor de relatórios CSV em JSON para envio ao n8n.

---

## ⚙️ Arquitetura do Projeto

1. O **OpenVAS** executa varreduras e gera relatórios em formato CSV.  
2. O script [`proxy.py`](proxy.py) atua como **intermediário**, recebendo os relatórios via socket, convertendo-os em JSON e enviando ao webhook do **n8n**.  
3. O **n8n** processa os dados:
   - Faz *parse* do relatório.
   - Aplica filtro de severidade (**CVSS > 7**).
   - Em caso de vulnerabilidade crítica:
     - Cria um **ticket automaticamente no Zammad**.
     - Dispara **alerta no Discord** para a equipe de segurança.  
4. Todo o fluxo garante rastreabilidade (Zammad) e comunicação ágil (Discord).

---

## 🖥️ Componentes

### 🔸 Proxy Python
Arquivo: [`proxy.py`](proxy.py)

- Recebe conexões TCP na porta `6000`.
- Converte relatórios CSV recebidos em **lista de dicionários JSON**.
- Envia os dados para o **Webhook do n8n** (`/webhook/openvas`).

### 🔸 Fluxo n8n
Arquivo: [`OpenVAS _ Zammad + Discord ( LAB).json`](OpenVAS%20_%20Zammad%20+%20Discord%20(%20LAB).json)

- **Webhook (entrada)** → Recebe dados do proxy.
- **Split & Transform** → Normaliza campos (IP, CVSS, CVE, descrição, solução etc.).
- **Filtro CVSS > 7** → Define o nível crítico.
- **Ação 1: Zammad** → Abre chamado automático com os detalhes técnicos.  
- **Ação 2: Discord** → Envia alerta instantâneo para o canal do time de segurança.

---

## 🚀 Como Executar

### 1. Proxy
```bash
python3 proxy.py
```
- O proxy ficará aguardando conexões do **OpenVAS** em `0.0.0.0:6000`.

### 2. n8n
- Importe o fluxo `OpenVAS _ Zammad + Discord ( LAB).json` dentro do n8n.
- Configure credenciais do **Zammad** e o **Webhook URL do Discord**.

### 3. OpenVAS
- Configure o OpenVAS para enviar os relatórios CSV para o endereço e porta do **proxy**.

---

## 📊 Exemplo de Alerta no Discord

```
🚨 Vulnerabilidade crítica detectada em 192.168.1.10!
CVE: CVE-2024-12345
Severidade: 9.8 (Critical)
Descrição: Cache poisoning allows content injection for proxied requests.
```

## 🎯 Benefícios

- **Custo zero**: 100% baseado em ferramentas open source.  
- **Automação ponta a ponta**: da detecção até o tratamento.  
- **Visibilidade centralizada**: tickets no Zammad.  
- **Tempo de resposta reduzido**: alertas em tempo real no Discord.  
- **Escalável**: fácil adaptação para outros SIEMs, helpdesks e canais de comunicação.  

---

## 📌 Sobre o Projeto

Este laboratório foi criado para demonstrar como **PMEs podem implementar uma gestão de vulnerabilidades eficiente com ferramentas open source**, sem depender de soluções proprietárias e caras.

--
👤 Autor: [William Weber](https://www.linkedin.com/in/william-weber-19289390/)  
🔗 Projeto Open Source para a comunidade de **Cybersecurity**.
