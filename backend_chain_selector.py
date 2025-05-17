import pandas as pd
import math
import os
import sys
import numpy as np

# Código vinculado ao Frontend
def calcular_resultados(dados):
    
    # Função para encontrar o caminho csv na pasta base
    def caminho_csv(nome_arquivo):
        pasta_base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(pasta_base, nome_arquivo) 
 
    # Etapa 1: Consulta/Definição do fator de sobrecarga K0
    df_k0 = pd.read_csv(caminho_csv("K0.csv"), sep=";")
    k0=1
    if 'Tipo_choque' in dados.keys():
        if dados['Tipo_choque'] not in df_k0['Tipo_choque'].values:
            raise ValueError(f"Tipo de choque '{dados['Tipo_choque']}' não encontrado no CSV.")
        k0 = df_k0.loc[df_k0['Tipo_choque'] == dados['Tipo_choque'], 'K0'].values[0]
    
    # Etapa 2: Conversão da potência nominal N0 para kW e cálculo da Potência de Projeto Pp
    def converter_para_kw(valor, unidade):
        valor = float(valor)
        if unidade == 'CV':
            return valor * 0.7355
        elif unidade == 'hp':
            return valor * 0.7457
        return valor
    N0 = converter_para_kw(dados['N0'], dados['unidade'])
    Pp = N0 * k0

    # Etapa 3: Consulta/Definição do Tipo_Corrente
    if 'Tipo_corrente' in dados.keys():
        tipo_corrente = int(dados.get('Tipo_corrente'))
    else:
        df_tipo = pd.read_csv(caminho_csv("Tipo_Corrente.csv"), sep=";")
        menor_distancia = 10000000
        tipo_corrente=0
        for index, row in df_tipo.iterrows():
            tipo_corre = row['Tipo_corrente']
            n1 = row['n1']
            Pp_ = row['Pp']
            distancia_desse_ponto = math.sqrt(pow(n1-float(dados["n1"]),2) + pow(Pp_-Pp,2))
            if(distancia_desse_ponto<menor_distancia):
                tipo_corrente=tipo_corre
                menor_distancia=distancia_desse_ponto

    # Etapa 4: Consulta o índice da corrente selecionada na Etapa 3
    df_indice = pd.read_csv(caminho_csv("Indice.csv"), sep=";")
    df_indice['Indice'] = df_indice['Indice'].astype(int)
    linha = df_indice[df_indice['tipo_corrente_n'] == tipo_corrente]
    if not linha.empty:
        indice = linha.iloc[0]['Indice']

        # Etapa 4.1: Definição dos tipos de corrente ANSI superiores, de acordo com as correntes superiores disponíveis
        if indice < 10:
                tipo_corrente_2 = df_indice.loc[df_indice['Indice'] == indice + 1, 'tipo_corrente_n'].values
                tipo_corrente_2 = tipo_corrente_2[0] if len(tipo_corrente_2) > 0 else None

                tipo_corrente_3 = df_indice.loc[df_indice['Indice'] == indice + 2, 'tipo_corrente_n'].values
                tipo_corrente_3 = tipo_corrente_3[0] if len(tipo_corrente_3) > 0 else None

                tipo_corrente_4 = df_indice.loc[df_indice['Indice'] == indice + 3, 'tipo_corrente_n'].values
                tipo_corrente_4 = tipo_corrente_4[0] if len(tipo_corrente_4) > 0 else None  

                tipo_corrente_5 = df_indice.loc[df_indice['Indice'] == indice + 4, 'tipo_corrente_n'].values
                tipo_corrente_5 = tipo_corrente_5[0] if len(tipo_corrente_5) > 0 else None
        else:            
            if indice < 11:
                tipo_corrente_2 = df_indice.loc[df_indice['Indice'] == indice + 1, 'tipo_corrente_n'].values
                tipo_corrente_2 = tipo_corrente_2[0] if len(tipo_corrente_2) > 0 else None

                tipo_corrente_3 = df_indice.loc[df_indice['Indice'] == indice + 2, 'tipo_corrente_n'].values
                tipo_corrente_3 = tipo_corrente_3[0] if len(tipo_corrente_3) > 0 else None

                tipo_corrente_4 = df_indice.loc[df_indice['Indice'] == indice + 3, 'tipo_corrente_n'].values
                tipo_corrente_4 = tipo_corrente_4[0] if len(tipo_corrente_4) > 0 else None       

                tipo_corrente_5 = None   
            else:    
                if indice < 12:
                    tipo_corrente_2 = df_indice.loc[df_indice['Indice'] == indice + 1, 'tipo_corrente_n'].values
                    tipo_corrente_2 = tipo_corrente_2[0] if len(tipo_corrente_2) > 0 else None

                    tipo_corrente_3 = df_indice.loc[df_indice['Indice'] == indice + 2, 'tipo_corrente_n'].values
                    tipo_corrente_3 = tipo_corrente_3[0] if len(tipo_corrente_3) > 0 else None

                    tipo_corrente_4 = None

                    tipo_corrente_5 = None
                else:
                    if indice < 13:
                        tipo_corrente_2 = df_indice.loc[df_indice['Indice'] == indice + 1, 'tipo_corrente_n'].values
                        tipo_corrente_2 = tipo_corrente_2[0] if len(tipo_corrente_2) > 0 else None

                        tipo_corrente_3 = None

                        tipo_corrente_4 = None

                        tipo_corrente_5 = None
                    else:
                        tipo_corrente_2 = None

                        tipo_corrente_3 = None

                        tipo_corrente_4 = None

                        tipo_corrente_5 = None
    else:
        print("Tipo_corrente não encontrado no CSV.")
    
    # Etapa 5: Consulta dos passos da(s) corrente(s) selecionada(s) 
    df_passo = pd.read_csv(caminho_csv("Passo.csv"), sep=";")
    p = df_passo.loc[df_passo['tipo_corrente'] == tipo_corrente, 'p'].values[0]
    if tipo_corrente_2 == None:
        p_2 = 0
    else:
        df_passo_2 = pd.read_csv(caminho_csv("Passo.csv"), sep=";")
        p_2 = df_passo_2.loc[df_passo_2['tipo_corrente'] == tipo_corrente_2, 'p'].values[0]
    if tipo_corrente_3 == None:
        p_3 = 0
    else:
        df_passo_3 = pd.read_csv(caminho_csv("Passo.csv"), sep=";")
        p_3 = df_passo_3.loc[df_passo_3['tipo_corrente'] == tipo_corrente_3, 'p'].values[0]
    if tipo_corrente_4 == None:
        p_4 = 0
    else:
        df_passo_4 = pd.read_csv(caminho_csv("Passo.csv"), sep=";")
        p_4 = df_passo_4.loc[df_passo_4['tipo_corrente'] == tipo_corrente_4, 'p'].values[0]
    if tipo_corrente_5 == None:
        p_5 = 0
    else:
        df_passo_5 = pd.read_csv(caminho_csv("Passo.csv"), sep=";")
        p_5 = df_passo_5.loc[df_passo_5['tipo_corrente'] == tipo_corrente_5, 'p'].values[0]

    # Etapa 6: Definição de número de dentes da roda dentada motora z1
    z1 = int(dados.get('z1', 17))
    n1 = float(dados['n1'])
    n2 = float(dados['n2']) 
    # Para o caso de entrada obrigatória 2, onde n2 não é definido pelo usuário, o código usa a relação de transmissão para calcular n2 e evitar erro

    # Etapa 7: Cálculo número de dentes roda movida z2temp (pre arredondamento) e z2
    z2temp = (z1 * n1) / n2
    # Caso o valor de z2 seja exato, não há arredondamento para o número ímpar mais próximo
    if math.isclose(z2temp, round(z2temp), abs_tol=1e-6):
        z2 = int(z2temp)
    else:
        z2 = int(round(z2temp))
        if z2 % 2 == 0:
            z2 += 1 if z2 < z2temp else -1

    # Etapa 8: Cálculo da velocidade tangencial para cada corrente
    v = (z1 * p * n1) / 60_000
    if tipo_corrente_2 == None:
        v_2 = 0
    else:    
        v_2 = (z1 * p_2 * n1) / 60_000
    if tipo_corrente_3 == None:
        v_3 = 0
    else:    
        v_3 = (z1 * p_3 * n1) / 60_000
    if tipo_corrente_4 == None:
        v_4 = 0
    else:    
        v_4 = (z1 * p_4 * n1) / 60_000
    if tipo_corrente_5 == None:
        v_5 = 0
    else:    
        v_5 = (z1 * p_5 * n1) / 60_000

    # Etapa 9: Cálculo/Definição da distância entre centros 
    a = float(dados.get('a', 40 * p))
    if tipo_corrente_2 == None:
        a_2 = 0
    else:
        a_2 = float(dados.get('a', 40 * p_2))
    if tipo_corrente_3 == None:
        a_3 = 0
    else:
        a_3 = float(dados.get('a', 40 * p_3))
    if tipo_corrente_4 == None:
        a_4 = 0
    else:
        a_4 = float(dados.get('a', 40 * p_4))
    if tipo_corrente_5 == None:
        a_5 = 0
    else:
        a_5 = float(dados.get('a', 40 * p_5))

    # Etapas 10: Cálculo número de elos X e arredondamento para um número par
    Xtemp = (2 * a) / p + (z1 + z2) / 2 + (p / a) * (((z2 - z1) / (2 * math.pi)) ** 2)
    X = int(round(Xtemp))
    if X % 2 != 0:
        X += 1
    if tipo_corrente_2 == None:
        X_2 = 0
    else:
        Xtemp_2 = (2 * a_2) / p_2 + (z1 + z2) / 2 + (p_2 / a_2) * (((z2 - z1) / (2 * math.pi)) ** 2)
        X_2 = int(round(Xtemp_2))
        if X_2 % 2 != 0:
            X_2 += 1
    if tipo_corrente_3 == None:
        X_3 = 0
    else:
        Xtemp_3 = (2 * a_3) / p_3 + (z1 + z2) / 2 + (p_3 / a_3) * (((z2 - z1) / (2 * math.pi)) ** 2)
        X_3 = int(round(Xtemp_3))
        if X_3 % 2 != 0:
            X_3 += 1
    if tipo_corrente_4 == None:
        X_4 = 0
    else:
        Xtemp_4 = (2 * a_4) / p_4 + (z1 + z2) / 2 + (p_4 / a_4) * (((z2 - z1) / (2 * math.pi)) ** 2)
        X_4 = int(round(Xtemp_4))
        if X_4 % 2 != 0:
            X_4 += 1
    if tipo_corrente_5 == None:
        X_5 = 0
    else:
        Xtemp_5 = (2 * a_5) / p_5 + (z1 + z2) / 2 + (p_5 / a_5) * (((z2 - z1) / (2 * math.pi)) ** 2)
        X_5 = int(round(Xtemp_5))
        if X_5 % 2 != 0:
            X_5 += 1

    # Etapa 11: Cálculo da distância entre centros corrigida após arredondamento do número de elos
    acorr = (p / 4) * (X - (z1 + z2) / 2 + math.sqrt(((X - (z1 + z2) / 2) ** 2) - (2 * ((z2 - z1) / math.pi) ** 2)))
    if tipo_corrente_2 == None:
        acorr_2 = 0
    else:
        acorr_2 = (p_2 / 4) * (X_2 - (z1 + z2) / 2 + math.sqrt(((X_2 - (z1 + z2) / 2) ** 2) - (2 * ((z2 - z1) / math.pi) ** 2)))
    if tipo_corrente_3 == None:
        acorr_3 = 0
    else:
        acorr_3 = (p_3 / 4) * (X_3 - (z1 + z2) / 2 + math.sqrt(((X_3 - (z1 + z2) / 2) ** 2) - (2 * ((z2 - z1) / math.pi) ** 2)))
    if tipo_corrente_4 == None:
        acorr_4 = 0
    else:
        acorr_4 = (p_4 / 4) * (X_4 - (z1 + z2) / 2 + math.sqrt(((X_4 - (z1 + z2) / 2) ** 2) - (2 * ((z2 - z1) / math.pi) ** 2)))
    if tipo_corrente_5 == None:
        acorr_5 = 0
    else:
        acorr_5 = (p_5 / 4) * (X_3 - (z1 + z2) / 2 + math.sqrt(((X_5 - (z1 + z2) / 2) ** 2) - (2 * ((z2 - z1) / math.pi) ** 2)))

    # Etapa 12: Cálculo do comprimento da corrente
    L = (X * p) / 1000
    if tipo_corrente_2 == None:
        L_2 = 0
    else:
        L_2 = (X_2 * p_2) / 1000
    if tipo_corrente_3 == None:
        L_3 = 0
    else:
        L_3 = (X_3 * p_3) / 1000
    if tipo_corrente_4 == None:
        L_4 = 0
    else:
        L_4 = (X_4 * p_4) / 1000
    if tipo_corrente_5 == None:
        L_5 = 0
    else:
        L_5 = (X_5 * p_5) / 1000

    # Etapa 13: Cálculo dos diâmetros primitivos
    dp1 = p / math.sin(math.radians(180 / z1))
    dp2 = p / math.sin(math.radians(180 / z2))
    if tipo_corrente_2 == None:
        dp1_2 = 0
        dp2_2 = 0
    else:
        dp1_2 = p_2 / math.sin(math.radians(180 / z1))
        dp2_2 = p_2 / math.sin(math.radians(180 / z2))
    if tipo_corrente_3 == None:
        dp1_3 = 0
        dp2_3 = 0
    else:
        dp1_3 = p_3 / math.sin(math.radians(180 / z1))
        dp2_3 = p_3 / math.sin(math.radians(180 / z2))
    if tipo_corrente_4 == None:
        dp1_4 = 0
        dp2_4 = 0
    else:
        dp1_4 = p_4 / math.sin(math.radians(180 / z1))
        dp2_4 = p_4 / math.sin(math.radians(180 / z2))
    if tipo_corrente_5 == None:
        dp1_5 = 0
        dp2_5 = 0
    else:
        dp1_5 = p_5 / math.sin(math.radians(180 / z1))
        dp2_5 = p_5 / math.sin(math.radians(180 / z2))

    # Etapa 14: Carga Atuante na Corrente
    # Etapa 14.1: Cálculo do Torque transmitido (kgf.cm)
    Torque = (71620 * (N0 / 0.7457)) / n1

    # Etapa 14.2: Força tangencial 
    Ft = (2 * Torque)/ (dp1 * 0.1)
    if tipo_corrente_2 == None:
        Ft_2 = 0
    else:
        Ft_2 = (2 * Torque)/ (dp1_2 * 0.1)
    if tipo_corrente_3 == None:
        Ft_3 = 0
    else:
        Ft_3 = (2 * Torque)/ (dp1_3 * 0.1)
    if tipo_corrente_4 == None:
        Ft_4 = 0
    else:
        Ft_4 = (2 * Torque)/ (dp1_4 * 0.1)
    if tipo_corrente_5 == None:
        Ft_5 = 0
    else:
        Ft_5 = (2 * Torque)/ (dp1_5 * 0.1)

    # Etapa 14.3: Cálculo do peso da corrente por unidade de comprimento
    df_G = pd.read_csv(caminho_csv("G.csv"), sep=";")
    G = df_G.loc[df_G['tipo_corrente'] == tipo_corrente, 'G'].values[0]
    if tipo_corrente_2 == None:
        G_2 = 0
    else:    
        df_G_2 = pd.read_csv(caminho_csv("G.csv"), sep=";")
        G_2 = df_G_2.loc[df_G['tipo_corrente'] == tipo_corrente_2, 'G'].values[0]
    if tipo_corrente_3 == None:
        G_3 = 0
    else:    
        df_G_3 = pd.read_csv(caminho_csv("G.csv"), sep=";")
        G_3 = df_G_3.loc[df_G['tipo_corrente'] == tipo_corrente_3, 'G'].values[0]
    if tipo_corrente_4 == None:
        G_4 = 0
    else:    
        df_G_4 = pd.read_csv(caminho_csv("G.csv"), sep=";")
        G_4 = df_G_4.loc[df_G['tipo_corrente'] == tipo_corrente_4, 'G'].values[0]
    if tipo_corrente_5 == None:
        G_5 = 0
    else:    
        df_G_5 = pd.read_csv(caminho_csv("G.csv"), sep=";")
        G_5 = df_G_5.loc[df_G['tipo_corrente'] == tipo_corrente_5, 'G'].values[0]

    # Etapa 14.4: Cálculo da Força Centrífuga 
    S = (G * (v**2)) / 9.81
    if tipo_corrente_2 == None:
        S_2 = 0
    else:
        S_2 = (G_2 * (v_2**2)) / 9.81  
    if tipo_corrente_3 == None:
        S_3 = 0
    else:
        S_3 = (G_3 * (v_3**2)) / 9.81  
    if tipo_corrente_4 == None:
        S_4 = 0
    else:
        S_4 = (G_4 * (v_4**2)) / 9.81  
    if tipo_corrente_5 == None:
        S_5 = 0
    else:
        S_5 = (G_5 * (v_5**2)) / 9.81  

    # Etapa 14.5: Cálculo da carga de Tração Resultante 
    Ttrac = Ft + S
    if tipo_corrente_2 == None:
        Ttrac_2 = 0
    else:
        Ttrac_2 = Ft_2 * S_2
    if tipo_corrente_3 == None:
        Ttrac_3 = 0
    else:
        Ttrac_3 = Ft_3 * S_3
    if tipo_corrente_4 == None:
        Ttrac_4 = 0
    else:
        Ttrac_4 = Ft_4 * S_4
    if tipo_corrente_5 == None:
        Ttrac_5 = 0
    else:
        Ttrac_5 = Ft_5 * S_5        

    # Etapa 15: consultar Ntab
    df_ntab = pd.read_csv(caminho_csv("Ntab.csv"), sep=";")
    df_ntab_filtro = df_ntab[df_ntab['tipo_corrente'] == tipo_corrente]
    Ntab = df_ntab_filtro.iloc[(df_ntab_filtro['n1'] - n1).abs().argsort()[:1]]['Ntab'].values[0]
    if tipo_corrente_2 == None:
        Ntab_2 = 0
    else:
        df_ntab_2 = pd.read_csv(caminho_csv("Ntab.csv"), sep=";")
        df_ntab_filtro_2 = df_ntab_2[df_ntab_2['tipo_corrente'] == tipo_corrente_2]
        Ntab_2 = df_ntab_filtro_2.iloc[(df_ntab_filtro_2['n1'] - n1).abs().argsort()[:1]]['Ntab'].values[0]
    if tipo_corrente_3 == None:
        Ntab_3 = 0
    else:
        df_ntab_3 = pd.read_csv(caminho_csv("Ntab.csv"), sep=";")
        df_ntab_filtro_3 = df_ntab_3[df_ntab_3['tipo_corrente'] == tipo_corrente_3]
        Ntab_3 = df_ntab_filtro_3.iloc[(df_ntab_filtro_3['n1'] - n1).abs().argsort()[:1]]['Ntab'].values[0]
    if tipo_corrente_4 == None:
        Ntab_4 = 0
    else:
        df_ntab_4 = pd.read_csv(caminho_csv("Ntab.csv"), sep=";")
        df_ntab_filtro_4 = df_ntab_4[df_ntab_4['tipo_corrente'] == tipo_corrente_4]
        Ntab_4 = df_ntab_filtro_4.iloc[(df_ntab_filtro_4['n1'] - n1).abs().argsort()[:1]]['Ntab'].values[0]
    if tipo_corrente_5 == None:
        Ntab_5 = 0
    else:
        df_ntab_5 = pd.read_csv(caminho_csv("Ntab.csv"), sep=";")
        df_ntab_filtro_5 = df_ntab_5[df_ntab_5['tipo_corrente'] == tipo_corrente_5]
        Ntab_5 = df_ntab_filtro_5.iloc[(df_ntab_filtro_5['n1'] - n1).abs().argsort()[:1]]['Ntab'].values[0]

    # Etapas 16: Consulta fator de número de dentes K1
    df_K1 = pd.read_csv(caminho_csv("K1.csv"), sep=";", converters={'z1': int})
    K1 = df_K1.loc[df_K1['z1'] == z1, 'K1'].values[0]

    # Etapas 17.1: Consulta fator número de fileiras K2 para correntes simples
    nf = int(1)
    df_K2 = pd.read_csv(caminho_csv("K2.csv"), sep=";", converters={'nf': int})
    K2 = df_K2.loc[df_K2['nf'] == nf, 'K2'].values[0]    

    # Etapa 18.1: Cálculo dos coeficiente de segurança para corrente simples
    CS = (Ntab * K1 * K2 * 0.7457) / Pp
    if tipo_corrente_2 == None:
        CS_2 = 0
    else:
        CS_2 = (Ntab_2 * K1 * K2 * 0.7457) / Pp
    if tipo_corrente_3 == None:
        CS_3 = 0
    else:
        CS_3 = (Ntab_3 * K1 * K2 * 0.7457) / Pp
    if tipo_corrente_4 == None:
        CS_4 = 0
    else:
        CS_4 = (Ntab_4 * K1 * K2 * 0.7457) / Pp
    if tipo_corrente_5 == None:
        CS_5 = 0
    else:
        CS_5 = (Ntab_5 * K1 * K2 * 0.7457) / Pp

    # Etapa 17.2: Consulta fator número de fileiras K2 para correntes duplas
    nf = int(2)
    df_K2 = pd.read_csv(caminho_csv("K2.csv"), sep=";", converters={'nf': int})
    K2 = df_K2.loc[df_K2['nf'] == nf, 'K2'].values[0]    

    # Etapa 18.2: Cálculo dos coeficiente de segurança para corrente dupla
    CS_2f = (Ntab * K1 * K2 * 0.7457) / Pp
    if tipo_corrente_2 == None:
        CS_2_2f = 0
    else:
        CS_2_2f = (Ntab_2 * K1 * K2 * 0.7457) / Pp
    if tipo_corrente_3 == None:
        CS_3_2f = 0
    else:
        CS_3_2f = (Ntab_3 * K1 * K2 * 0.7457) / Pp
    if tipo_corrente_4 == None:
        CS_4_2f = 0
    else:
        CS_4_2f = (Ntab_4 * K1 * K2 * 0.7457) / Pp
    if tipo_corrente_5 == None:
        CS_5_2f = 0
    else:
        CS_5_2f = (Ntab_5 * K1 * K2 * 0.7457) / Pp

    # Etapa 17.3: Consulta fator número de fileiras K2 para correntes triplas
    nf = int(3)
    df_K2 = pd.read_csv(caminho_csv("K2.csv"), sep=";", converters={'nf': int})
    K2 = df_K2.loc[df_K2['nf'] == nf, 'K2'].values[0]    

    # Etapa 18.3: Cálculo dos coeficiente de segurança para corrente tripla
    CS_3f = (Ntab * K1 * K2 * 0.7457) / Pp
    if tipo_corrente_2 == None:
        CS_2_3f = 0
    else:
        CS_2_3f = (Ntab_2 * K1 * K2 * 0.7457) / Pp
    if tipo_corrente_3 == None:
        CS_3_3f = 0
    else:
        CS_3_3f = (Ntab_3 * K1 * K2 * 0.7457) / Pp
    if tipo_corrente_4 == None:
        CS_4_3f = 0
    else:
        CS_4_3f = (Ntab_4 * K1 * K2 * 0.7457) / Pp
    if tipo_corrente_5 == None:
        CS_5_3f = 0
    else:
        CS_5_3f = (Ntab_5 * K1 * K2 * 0.7457) / Pp

    # Etapa 19: Retorno dos resultados para o Frontend 
    if tipo_corrente_5 == None:
        if tipo_corrente_4 == None:
            if tipo_corrente_3 == None:
                if tipo_corrente_2 == None:
                    return {
                        "Corrente 1": {
                        "Número de dentes roda motora": z1,
                        "Número de dentes roda movida": z2,
                        "Potência de Projeto (kW)": Pp,
                        "Opção de corrente": tipo_corrente,
                        "Diâmetro primitivo roda motora (mm)": dp1,
                        "Diâmetro primitivo roda movida (mm)": dp2,
                        "Velocidade tangencial (m/s)": v,
                        "Número de elos": X,
                        "Distância entre centros": acorr,
                        "Comprimento da corrente (m)": L,
                        "Potência Limite (hp)": Ntab,
                        "CS para corrente simples": CS,
                        "CS para correntes duplas": CS_2f,
                        "CS para correntes triplas": CS_3f,
                        "Torque (kgf.cm)": Torque,
                        "Força Tangencial (kgf)": Ft,
                        "Força Centrífuga (kgf) corrente simples": S,
                        "Carga de Tração Resultante (Ft + S)": Ttrac                
                        }
                    }
                else:
                    return {
                        "Corrente 1": {
                        "Número de dentes roda motora": z1,
                        "Número de dentes roda movida": z2,
                        "Potência de Projeto (kW)": Pp,
                        "Opção de corrente": tipo_corrente,
                        "Diâmetro primitivo roda motora (mm)": dp1,
                        "Diâmetro primitivo roda movida (mm)": dp2,
                        "Velocidade tangencial (m/s)": v,
                        "Número de elos": X,
                        "Distância entre centros": acorr,
                        "Comprimento da corrente (m)": L,
                        "Potência Limite (hp)": Ntab,
                        "CS para corrente simples": CS,
                        "CS para correntes duplas": CS_2f,
                        "CS para correntes triplas": CS_3f,
                        "Torque (kgf.cm)": Torque,
                        "Força Tangencial (kgf)": Ft,
                        "Força Centrífuga (kgf) corrente simples": S,
                        "Carga de Tração Resultante (Ft + S)": Ttrac                         
                        },
                        "Corrente 2": {
                        "Número de dentes roda motora": z1,
                        "Número de dentes roda movida": z2,
                        "Potência de Projeto (kW)": Pp,
                        "Opção de corrente": tipo_corrente_2,
                        "Diâmetro primitivo roda motora (mm)": dp1_2,
                        "Diâmetro primitivo roda movida (mm)": dp2_2,
                        "Velocidade tangencial (m/s)": v_2,
                        "Número de elos": X_2,
                        "Distância entre centros": acorr_2,
                        "Comprimento da corrente (m)": L_2,
                        "Potência Limite (hp)": Ntab_2,
                        "CS para corrente simples": CS_2,
                        "CS para correntes duplas": CS_2_2f,
                        "CS para correntes triplas": CS_2_3f,
                        "Torque (kgf.cm)": Torque,
                        "Força Tangencial (kgf)": Ft_2,
                        "Força Centrífuga (kgf) corrente simples": S_2,
                        "Carga de Tração Resultante (Ft + S)": Ttrac_2  
                        }
                    }
            else:
                return {
                    "Corrente 1": {
                    "Número de dentes roda motora": z1,
                    "Número de dentes roda movida": z2,
                    "Potência de Projeto (kW)": Pp,
                    "Opção de corrente": tipo_corrente,
                    "Diâmetro primitivo roda motora (mm)": dp1,
                    "Diâmetro primitivo roda movida (mm)": dp2,
                    "Velocidade tangencial (m/s)": v,
                    "Número de elos": X,
                    "Distância entre centros": acorr,
                    "Comprimento da corrente (m)": L,
                    "Potência Limite (hp)": Ntab,
                    "CS para corrente simples": CS,
                    "CS para correntes duplas": CS_2f,
                    "CS para correntes triplas": CS_3f,
                    "Torque (kgf.cm)": Torque,
                    "Força Tangencial (kgf)": Ft,
                    "Força Centrífuga (kgf) corrente simples": S,
                    "Carga de Tração Resultante (Ft + S)": Ttrac          
                    },
                    "Corrente 2": {
                    "Número de dentes roda motora": z1,
                    "Número de dentes roda movida": z2,
                    "Potência de Projeto (kW)": Pp,
                    "Opção de corrente": tipo_corrente_2,
                    "Diâmetro primitivo roda motora (mm)": dp1_2,
                    "Diâmetro primitivo roda movida (mm)": dp2_2,
                    "Velocidade tangencial (m/s)": v_2,
                    "Número de elos": X_2,
                    "Distância entre centros": acorr_2,
                    "Comprimento da corrente (m)": L_2,
                    "Potência Limite (hp)": Ntab_2,
                    "CS para corrente simples": CS_2,
                    "CS para correntes duplas": CS_2_2f,
                    "CS para correntes triplas": CS_2_3f,
                    "Torque (kgf.cm)": Torque,
                    "Força Tangencial (kgf)": Ft_2,
                    "Força Centrífuga (kgf) corrente simples": S_2,
                    "Carga de Tração Resultante (Ft + S)": Ttrac_2    
                    },
                    "Corrente 3": {
                    "Número de dentes roda motora": z1,
                    "Número de dentes roda movida": z2,
                    "Potência de Projeto (kW)": Pp,
                    "Opção de corrente": tipo_corrente_3,
                    "Diâmetro primitivo roda motora (mm)": dp1_3,
                    "Diâmetro primitivo roda movida (mm)": dp2_3,
                    "Velocidade tangencial (m/s)": v_3,
                    "Número de elos": X_3,
                    "Distância entre centros": acorr_3,
                    "Comprimento da corrente (m)": L_3,
                    "Potência Limite (hp)": Ntab_3,
                    "CS para corrente simples": CS_3,
                    "CS para correntes duplas": CS_3_2f,
                    "CS para correntes triplas": CS_3_3f,
                    "Torque (kgf.cm)": Torque,
                    "Força Tangencial (kgf)": Ft_3,
                    "Força Centrífuga (kgf) corrente simples": S_3,
                    "Carga de Tração Resultante (Ft + S)": Ttrac_3    
                    }          
                }  
        else:
            return {
                "Corrente 1": {
                "Número de dentes roda motora": z1,
                "Número de dentes roda movida": z2,
                "Potência de Projeto (kW)": Pp,
                "Opção de corrente": tipo_corrente,
                "Diâmetro primitivo roda motora (mm)": dp1,
                "Diâmetro primitivo roda movida (mm)": dp2,
                "Velocidade tangencial (m/s)": v,
                "Número de elos": X,
                "Distância entre centros": acorr,
                "Comprimento da corrente (m)": L,
                "Potência Limite (hp)": Ntab,
                "CS para corrente simples": CS,
                "CS para correntes duplas": CS_2f,
                "CS para correntes triplas": CS_3f,
                "Torque (kgf.cm)": Torque,
                "Força Tangencial (kgf)": Ft,
                "Força Centrífuga (kgf) corrente simples": S,
                "Carga de Tração Resultante (Ft + S)": Ttrac          
                },
                "Corrente 2": {
                "Número de dentes roda motora": z1,
                "Número de dentes roda movida": z2,
                "Potência de Projeto (kW)": Pp,
                "Opção de corrente": tipo_corrente_2,
                "Diâmetro primitivo roda motora (mm)": dp1_2,
                "Diâmetro primitivo roda movida (mm)": dp2_2,
                "Velocidade tangencial (m/s)": v_2,
                "Número de elos": X_2,
                "Distância entre centros": acorr_2,
                "Comprimento da corrente (m)": L_2,
                "Potência Limite (hp)": Ntab_2,
                "CS para corrente simples": CS_2,
                "CS para correntes duplas": CS_2_2f,
                "CS para correntes triplas": CS_2_3f,
                "Torque (kgf.cm)": Torque,
                "Força Tangencial (kgf)": Ft_2,
                "Força Centrífuga (kgf) corrente simples": S_2,
                "Carga de Tração Resultante (Ft + S)": Ttrac_2    
                },
                "Corrente 3": {
                "Número de dentes roda motora": z1,
                "Número de dentes roda movida": z2,
                "Potência de Projeto (kW)": Pp,
                "Opção de corrente": tipo_corrente_3,
                "Diâmetro primitivo roda motora (mm)": dp1_3,
                "Diâmetro primitivo roda movida (mm)": dp2_3,
                "Velocidade tangencial (m/s)": v_3,
                "Número de elos": X_3,
                "Distância entre centros": acorr_3,
                "Comprimento da corrente (m)": L_3,
                "Potência Limite (hp)": Ntab_3,
                "CS para corrente simples": CS_3,
                "CS para correntes duplas": CS_3_2f,
                "CS para correntes triplas": CS_3_3f,
                "Torque (kgf.cm)": Torque,
                "Força Tangencial (kgf)": Ft_3,
                "Força Centrífuga (kgf) corrente simples": S_3,
                "Carga de Tração Resultante (Ft + S)": Ttrac_3    
                },
                "Corrente 4": {
                "Número de dentes roda motora": z1,
                "Número de dentes roda movida": z2,
                "Potência de Projeto (kW)": Pp,
                "Opção de corrente": tipo_corrente_4,
                "Diâmetro primitivo roda motora (mm)": dp1_4,
                "Diâmetro primitivo roda movida (mm)": dp2_4,
                "Velocidade tangencial (m/s)": v_4,
                "Número de elos": X_4,
                "Distância entre centros": acorr_4,
                "Comprimento da corrente (m)": L_4,
                "Potência Limite (hp)": Ntab_4,
                "CS para corrente simples": CS_4,
                "CS para correntes duplas": CS_4_2f,
                "CS para correntes triplas": CS_4_3f,
                "Torque (kgf.cm)": Torque,
                "Força Tangencial (kgf)": Ft_4,
                "Força Centrífuga (kgf) corrente simples": S_4,
                "Carga de Tração Resultante (Ft + S)": Ttrac_4              
                }
            }  
    else:
        return {
            "Corrente 1": {
            "Número de dentes roda motora": z1,
            "Número de dentes roda movida": z2,
            "Potência de Projeto (kW)": Pp,
            "Opção de corrente": tipo_corrente,
            "Diâmetro primitivo roda motora (mm)": dp1,
            "Diâmetro primitivo roda movida (mm)": dp2,
            "Velocidade tangencial (m/s)": v,
            "Número de elos": X,
            "Distância entre centros": acorr,
            "Comprimento da corrente (m)": L,
            "Potência Limite (hp)": Ntab,
            "CS para corrente simples": CS,
            "CS para correntes duplas": CS_2f,
            "CS para correntes triplas": CS_3f,
            "Torque (kgf.cm)": Torque,
            "Força Tangencial (kgf)": Ft,
            "Força Centrífuga (kgf) corrente simples": S,
             "Carga de Tração Resultante (Ft + S)": Ttrac          
            },
            "Corrente 2": {
            "Número de dentes roda motora": z1,
            "Número de dentes roda movida": z2,
            "Potência de Projeto (kW)": Pp,
            "Opção de corrente": tipo_corrente_2,
            "Diâmetro primitivo roda motora (mm)": dp1_2,
            "Diâmetro primitivo roda movida (mm)": dp2_2,
            "Velocidade tangencial (m/s)": v_2,
            "Número de elos": X_2,
            "Distância entre centros": acorr_2,
            "Comprimento da corrente (m)": L_2,
            "Potência Limite (hp)": Ntab_2,
            "CS para corrente simples": CS_2,
            "CS para correntes duplas": CS_2_2f,
            "CS para correntes triplas": CS_2_3f,
            "Torque (kgf.cm)": Torque,
            "Força Tangencial (kgf)": Ft_2,
            "Força Centrífuga (kgf) corrente simples": S_2,
            "Carga de Tração Resultante (Ft + S)": Ttrac_2    
            },
            "Corrente 3": {
            "Número de dentes roda motora": z1,
            "Número de dentes roda movida": z2,
            "Potência de Projeto (kW)": Pp,
            "Opção de corrente": tipo_corrente_3,
            "Diâmetro primitivo roda motora (mm)": dp1_3,
            "Diâmetro primitivo roda movida (mm)": dp2_3,
            "Velocidade tangencial (m/s)": v_3,
            "Número de elos": X_3,
            "Distância entre centros": acorr_3,
            "Comprimento da corrente (m)": L_3,
            "Potência Limite (hp)": Ntab_3,
            "CS para corrente simples": CS_3,
            "CS para correntes duplas": CS_3_2f,
            "CS para correntes triplas": CS_3_3f,
            "Torque (kgf.cm)": Torque,
            "Força Tangencial (kgf)": Ft_3,
            "Força Centrífuga (kgf) corrente simples": S_3,
            "Carga de Tração Resultante (Ft + S)": Ttrac_3    
            },
            "Corrente 4": {
            "Número de dentes roda motora": z1,
            "Número de dentes roda movida": z2,
            "Potência de Projeto (kW)": Pp,
            "Opção de corrente": tipo_corrente_4,
            "Diâmetro primitivo roda motora (mm)": dp1_4,
            "Diâmetro primitivo roda movida (mm)": dp2_4,
            "Velocidade tangencial (m/s)": v_4,
            "Número de elos": X_4,
            "Distância entre centros": acorr_4,
            "Comprimento da corrente (m)": L_4,
            "Potência Limite (hp)": Ntab_4,
            "CS para corrente simples": CS_4,
            "CS para correntes duplas": CS_4_2f,
            "CS para correntes triplas": CS_4_3f,
            "Torque (kgf.cm)": Torque,
            "Força Tangencial (kgf)": Ft_4,
            "Força Centrífuga (kgf) corrente simples": S_4,
            "Carga de Tração Resultante (Ft + S)": Ttrac_4              
            },
            "Corrente 5": {
            "Número de dentes roda motora": z1,
            "Número de dentes roda movida": z2,
            "Potência de Projeto (kW)": Pp,
            "Opção de corrente": tipo_corrente_5,
            "Diâmetro primitivo roda motora (mm)": dp1_5,
            "Diâmetro primitivo roda movida (mm)": dp2_5,
            "Velocidade tangencial (m/s)": v_5,
            "Número de elos": X_5,
            "Distância entre centros": acorr_5,
            "Comprimento da corrente (m)": L_5,
            "Potência Limite (hp)": Ntab_5,
            "CS para corrente simples": CS_5,
            "CS para correntes duplas": CS_5_2f,
            "CS para correntes triplas": CS_5_3f,
            "Torque (kgf.cm)": Torque,
            "Força Tangencial (kgf)": Ft_5,
            "Força Centrífuga (kgf) corrente simples": S_5,
            "Carga de Tração Resultante (Ft + S)": Ttrac_5             
            }
        }