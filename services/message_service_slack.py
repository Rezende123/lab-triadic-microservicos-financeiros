import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# DEFINE O CLIENT QUE VAI SER CONSUMIDO
client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))

def upload_arquivo_slack(nome_arquivo, caminho, titulo):
  with open(caminho, 'rb') as f:
    conteudo = f.read()
    # REALIZA O UPLOAD DO ARQUIVO
    new_file = client.files_upload(
      title=titulo,
      filename=nome_arquivo,
      content=conteudo,
    )
    file_url = new_file.get("file").get("permalink")
    envia_mensagem_slack(f"{titulo} - {file_url}")


def envia_mensagem_slack(mensagem):
  # ID DO CANAL PARA QUAL SERÁ ENVIADA A MENSAGEM
  channel_id = os.environ.get("CHANNEL_ID_CONTAS_A_PAGAR")

  try:
    # ENVIA A MENSAGEM
    result = client.chat_postMessage(
      channel=channel_id,
      text=mensagem
    )
    # PRINTA O RESULTADO DA MENSAGEM
    print(result)

  except SlackApiError as e:
    # PRINTA O ERRO NO ENVIO DA MENSAGEM
    print(f"Error: {e}")