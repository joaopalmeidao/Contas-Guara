import pandas as pd
from datetime import datetime
import time

from module.telegram import TelegramBot


path =  'I'
excel_path = '{}:\Meu Drive\ARQUIVOS\GERENCIAL\Gerencial Guara.xlsx'.format(path)

pd.options.display.width = 0


contas_df = pd.read_excel(excel_path,sheet_name='CONTAS A PAGAR', usecols=[0, 1, 2, 3])
# contas_df = pd.DataFrame(contas_table)
# today_df = '01-07-2022'
today_df = (datetime.today().strftime('%Y-%m-%d'))

today_message = (datetime.today().strftime('%d-%m-%Y'))
# print(df[['VENCIMENTO','FORNECEDOR','COD BARRAS','VALOR']])
# Filtra o vencimento
# vencimentos=tabela.loc[tabela['VENCIMENTO']==data]
deadlines = contas_df[contas_df['VENCIMENTO'].isin(pd.date_range(today_df, today_df))]
deadlines_message = deadlines.drop(columns=['VENCIMENTO','COD BARRAS'])
len_deadlines = len(deadlines)
cod_barras = deadlines[['COD BARRAS']]

amount = deadlines[['VALOR']].sum()

amount_by_date_suplyer = contas_df.groupby(by=['FORNECEDOR', 'VENCIMENTO']).sum().groupby(level=[0]).cumsum()
amount_by_date_suplyer_total = amount_by_date_suplyer.groupby(by=['FORNECEDOR', 'VALOR']).sum().groupby(level=[0]).cumsum()

deadlines_message_formatted = deadlines_message.to_string(index=False, header=False)
amount_formatted = amount.to_string(index=False, header=False)

def send_message():

    TelegramBot.send_message(str('Oi, os {} boletos abaixo vencem {}, somando no Total: R${}'.format(len_deadlines,today_message,amount_formatted)))
    TelegramBot.send_message('{}'.format(deadlines_message_formatted))
    time.sleep(1)
    
    init_row = 0
    end_row = 1
    cont_message = 0

    # while init_row <= len_deadlines and end_row <= len_deadlines:
    while cont_message < len_deadlines:
        # for each_row in deadlines:
            
        cont_message += 1
        message_cod_barras = cod_barras.iloc[init_row:end_row]
        message_cod_barras_formatted = message_cod_barras.to_string(index=False, header=False)
        TelegramBot.send_message('{}'.format(cont_message))
        TelegramBot.send_message(str('{}'.format(message_cod_barras_formatted)))

        
        init_row += 1
        end_row += 1

        time.sleep(1)
        # print(message_deadline)
        print('Mensagem Enviada!')

def main():
    TelegramBot.load_config()
    send_message()

if __name__ == '__main__':
    main()
