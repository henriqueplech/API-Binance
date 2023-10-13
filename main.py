# Executar no terminal: pip install python-binance
from binance.client import Client
import pandas as pd  # Correção do import

# Substitua com suas próprias chaves de API
api_key = "sua_api_key"
api_secret = "sua_api_secret"

client = Client(api_key, api_secret)

# Pegar informações do trade fiat/spot
symbol = 'BTCUSDT'
info = client.get_aggregate_trades(symbol=symbol)

# Para saber a última linha de dados: print(info[-1])

# Para manipulação dos dados, crie um DataFrame
info_df = pd.DataFrame(info)  # Correção para criar o DataFrame

# Exibir os dados em um DataFrame

#manipulação dos dados
info_df['price'] = pd.to_numeric(info_df['p'])
info_df['quantity'] = pd.to_numeric(info_df['q'])
info_df['first_trade'] = pd.to_numeric(info_df['f'])
info_df['last_trade'] = pd.to_numeric(info_df['l'])
info_df['trade_time'] = pd.to_datetime(info_df['T'], unit='ms')
info_df['is_market_maker'] = info_df['m'].apply(lambda x: True if x else False)
info_df['is_best_price_match'] = info_df['M'].apply(lambda x: True if x else False)

# Exibir os dados em um DataFrame
#print(info_df)

# Salvar os dados em um arquivo JSON
info_df.to_json('info.json', orient='records')

#analise do json com pandas
df = pd.read_json('info.json')

#exibir os dados
print(df)