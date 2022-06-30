#Executar no terminal: pip install python-binance
from binance.client import Client #importação da biblioteca api binance
#import pandas as aspd


client = Client("ygLyQROn7y7SdNvMoJepOdhZJV4OJUPeq1hhYe2929CopY2ZqGREhnWnVy1FQMEs", "aACSH2BCvZKNwp7bbQR5vtMOJAGMvJ8SUB2Cdfw5sBF1g8sRjhRevQfu6EYpssKC")

#pegar informações do trade fiat/spot
info = client.get_aggregate_trades(symbol='BTCUSDT')

print(info)

#Para saber a ultima linha de dados: print(info[-1])

#Para manipulação dos dados retire o "#" da segunda linha e coloque: pd.DataFrame(info)
