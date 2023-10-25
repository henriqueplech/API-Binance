from binance.client import Client
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from datetime import datetime

# Substitua com suas próprias chaves de API
api_key = "ygLyQROn7y7SdNvMoJepOdhZJV4OJUPeq1hhYe2929CopY2ZqGREhnWnVy1FQMEs"
api_secret = "aACSH2BCvZKNwp7bbQR5vtMOJAGMvJ8SUB2Cdfw5sBF1g8sRjhRevQfu6EYpssKC"

client = Client(api_key, api_secret)

# Pegar informações do trade fiat/spot
symbol = 'BTCUSDT'
info = client.get_aggregate_trades(symbol=symbol)

# Transformar os dados em um DataFrame
info_df = pd.DataFrame(info)
info_df['trade_time'] = pd.to_datetime(info_df['T'], unit='ms')

# Calcular o preço após 5 minutos
info_df['future_price'] = info_df['trade_time'].apply(lambda x: client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1MINUTE, limit=5, startTime=int(x.timestamp() * 1000))[-1][4])

# Manipulação dos dados
info_df['price'] = pd.to_numeric(info_df['p'])
info_df['quantity'] = pd.to_numeric(info_df['q'])
info_df['first_trade'] = pd.to_numeric(info_df['f'])
info_df['last_trade'] = pd.to_numeric(info_df['l'])
info_df['is_market_maker'] = info_df['m'].apply(lambda x: True if x else False)
info_df['is_best_price_match'] = info_df['M'].apply(lambda x: True if x else False)

# Preparar os dados para treinamento do modelo
X = info_df[['price', 'quantity', 'first_trade', 'last_trade', 'is_market_maker', 'is_best_price_match']]
y = info_df['future_price']

# Dividir os dados em treinamento e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Treinar um modelo de regressão linear
model = LinearRegression()
model.fit(X_train, y_train)

# Fazer previsões
predictions = model.predict(X_test)

# Exibir as previsões e os preços reais
for i, prediction in enumerate(predictions):
    print(f"Previsão: {prediction}, Preço Real: {y_test.iloc[i]}")

# Para fazer uma previsão do preço 5 minutos após a última entrada nos dados, você pode usar o modelo treinado e os dados mais recentes.
# Por exemplo:
latest_data = X.iloc[-1].values.reshape(1, -1)
future_price_prediction = model.predict(latest_data)
print(f"Previsão do preço 5 minutos no futuro: {future_price_prediction[0]}")
