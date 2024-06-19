import requests
from config import DEX_API_URL, WALLET_ADDRESSES, CHAT_ID

def send_alert(context, message):
    context.bot.send_message(chat_id=CHAT_ID, text=message)


def monitor_wallets_and_notify(context):
    for wallet in WALLET_ADDRESSES:
      response = requests.get(f"{DEX_API_URL}/{wallet}")
      if response.status_code == 200:
        date = response.json()
        transactions = data.get('transactions', [])
        for tx in transactions:
          message = f"Trade Alert!\nWallet: {wallet}\nTransaction: {tx['tx']}\nDetails: {tx}"
          send_alert(context, message)


if __name__ == '__main__':
  class FakeContext:
    class Bot:
      def send_message(self, chat_id, text):
          print(f"Message to {chat_id}: {text}")

    bot = Bot()

  monitor_wallets_and_notify(FakeContext())