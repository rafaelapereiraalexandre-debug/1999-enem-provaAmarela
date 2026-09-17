"""
Propósito: concatenar verticalmente as imagens da pasta sem-bordas-externas
Autor: Alexandre Nassar de Peder
Criação: 02/10/2025
Atualização: 03/06/2026
"""

from PIL import Image
import os
import re

pasta_imagens = "sem-bordas-externas"
pasta_saida = "."
os.makedirs(pasta_saida, exist_ok=True)

# Função para extrair o número da página e ordenar numericamente
def get_sort_key(nome_arquivo):
    match = re.search(r'pagina_enem_(\d+)\.png', nome_arquivo)
    if match:
        return int(match.group(1))
    return 0

# Pegar e ordenar as imagens numericamente (2, 3, 4, ..., 19)
arquivos = [f for f in os.listdir(pasta_imagens) if f.endswith('.png')]
arquivos.sort(key=get_sort_key)

# Abrir todas as imagens na ordem correta
imagens = []
for arquivo in arquivos:
    caminho = os.path.join(pasta_imagens, arquivo)
    imagens.append(Image.open(caminho))
    print(f"Adicionando: {arquivo}")

# Encontrar a largura máxima para alinhar todas as imagens
largura_max = max(img.width for img in imagens)

# Concatenar verticalmente
altura_total = sum(img.height for img in imagens)
imagem_final = Image.new('RGB', (largura_max, altura_total), (255, 255, 255))

y = 0
for img in imagens:
    imagem_final.paste(img, (0, y))
    y += img.height

# Salvar a imagem concatenada
caminho_saida = os.path.join(pasta_saida, 'colunas_concatenadas_verticalmente.png')
imagem_final.save(caminho_saida)

print("\nImagens concatenadas na ordem correta!")
print(f"Resultado salvo em: {caminho_saida}")