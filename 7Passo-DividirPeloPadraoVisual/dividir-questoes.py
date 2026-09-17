from PIL import Image
import os

def encontrar_faixa_preta(imagem, cor_alvo=(0, 0, 0), tolerancia=15, altura_base=3, margem_altura=2):
    """
    Encontra posições da faixa preta no primeiro pixel da esquerda (x=0)
    com variação de altura de 1 a 5 pixels (3 ± 2).
    """
    largura, altura = imagem.size
    pixels = imagem.load()
    
    posicoes_corte = []
    
    alt_min = max(1, altura_base - margem_altura)  # 1 pixel
    alt_max = altura_base + margem_altura          # 5 pixels
    
    y = 0
    while y < altura - alt_min:
        # Verifica quantos pixels consecutivos correspondem ao tom preto no primeiro pixel (x=0)
        altura_encontrada = 0
        
        for dy in range(alt_max):
            if y + dy >= altura:
                break
                
            pixel = pixels[0, y + dy]  # Primeiro pixel da esquerda (x = 0)
            
            if len(pixel) == 4:  # RGBA
                r, g, b, a = pixel
            else:  # RGB
                r, g, b = pixel[:3]
            
            # Verifica se é a cor preta alvo dentro da tolerância
            if (abs(r - cor_alvo[0]) <= tolerancia and 
                abs(g - cor_alvo[1]) <= tolerancia and 
                abs(b - cor_alvo[2]) <= tolerancia):
                altura_encontrada += 1
            else:
                break
        
        # Se a altura encontrada estiver no intervalo (1 a 5 pixels)
        if alt_min <= altura_encontrada <= alt_max:
            # Registra a posição de corte e o tamanho da faixa para ignorá-la na imagem cortada
            posicoes_corte.append((y, altura_encontrada))
            print(f"Padrão preto encontrado em y={y} (altura: {altura_encontrada}px)")
            
            # Avança após o padrão para remover a faixa preta do próximo corte
            y += altura_encontrada
        else:
            y += 1
    
    return posicoes_corte

def dividir_imagem_por_faixas(caminho_imagem, pasta_saida, cor_alvo):
    """
    Divide a imagem verticalmente removendo o padrão preto encontrado.
    """
    imagem = Image.open(caminho_imagem)
    largura, altura = imagem.size
    
    print(f"Imagem carregada: {largura}x{altura} pixels")
    
    posicoes_corte = encontrar_faixa_preta(imagem, cor_alvo)
    
    if not posicoes_corte:
        print("Nenhum padrão preto encontrado na imagem!")
        return
    
    print(f"Encontradas {len(posicoes_corte)} faixas para corte")
    
    os.makedirs(pasta_saida, exist_ok=True)
    
    posicao_anterior = 0
    
    for i, (posicao_corte, altura_faixa) in enumerate(posicoes_corte):
        if posicao_corte > posicao_anterior:
            # Corta do final da faixa anterior até o início do padrão atual
            area_corte = (0, posicao_anterior, largura, posicao_corte)
            secao = imagem.crop(area_corte)
            
            nome_arquivo = f"parte_{i+1:03d}.png"
            caminho_completo = os.path.join(pasta_saida, nome_arquivo)
            secao.save(caminho_completo)
            print(f"Salvo: {caminho_completo} ({secao.width}x{secao.height}px)")
        
        # Pula a faixa preta para removê-la dos recortes
        posicao_anterior = posicao_corte + altura_faixa

    # Corta a seção final (após o último padrão até o fim da imagem)
    if posicao_anterior < altura:
        area_corte = (0, posicao_anterior, largura, altura)
        secao = imagem.crop(area_corte)
        
        nome_arquivo = f"parte_{len(posicoes_corte)+1:03d}.png"
        caminho_completo = os.path.join(pasta_saida, nome_arquivo)
        secao.save(caminho_completo)
        print(f"Salvo: {caminho_completo} ({secao.width}x{secao.height}px)")

if __name__ == "__main__":
    caminho_imagem = "colunas_concatenadas_verticalmente.png"  # Atualize para sua imagem
    pasta_saida = "inteiras"                                  # Pasta de saída
    
    # Cor preta RGB (0, 0, 0)
    cor_do_padrao = (0, 0, 0)
    
    dividir_imagem_por_faixas(caminho_imagem, pasta_saida, cor_do_padrao)
    
    print("Divisão concluída!")