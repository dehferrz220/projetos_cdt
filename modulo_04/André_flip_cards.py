""" 
 Primicia - Jogo de cartas Viradas com Pygame

"""
import pygame
#bibliotecas padrão
import random
#Bibliotecas Do sistema
import time 
#Bibliotecas do sistema - contador
import os
# Biblotecas do salvamento (pontuação)
import sys
#Função para resolver caminhos de recursos

def resolver_caminho_recurso(caminho_relativo):
    try: 
        base_path = sys.MEIPASS
    except Exception: 
        base_path = os.path.abspath (".")
    return os.path.join(base_path, caminho_relativo)

pygame.init()
LARGURA,ALTURA = 800,600
COR_FUNDO =( 20,20,20)
COR_TEXTO =( 20,20,20) 
caminho_imagens = "imagens"
NOMES_IMAGENS = [
"1.png", "2.png", "3.png", "4.png", "5.png", 
"6.png", "7.png", "8.png", "9.png", "10.png", 
]
VERSO_NOME = "verso_flip.png"

JANELA = pygame.display.set_mode ((LARGURA,ALTURA))
pygame.display.set_caption ("JOGO DA MEMÓRIA PYGAME")
RELOGIO = pygame.time.Clock()

TAMANHO_CARTA = (100,100)
ALTURA_PLACAR = 50
AREA_JOGO_Y = ALTURA_PLACAR

caminho_verso = resolver_caminho_recurso(os.path.join(caminho_imagens, VERSO_NOME))
try:
    VERSO_CARTA_IMG = pygame.image.load(caminho_verso)
    VERSO_CARTA_IMG = pygame.transform.scale(VERSO_CARTA_IMG, TAMANHO_CARTA)
except pygame.error as e:
    print(f"ERRO: Não foi possível carregar o verso da carta: {e}")
    exit()

dados_imagens = []
for nome_arquivo in NOMES_IMAGENS:

    img_path = resolver_caminho_recurso (os.path.join(caminho_imagens,nome_arquivo))
    try:
        imagem_surface = pygame.image.load()
        imagem_surface = pygame.transform.scale(imagem_surface, TAMANHO_CARTA)
        dados_imagens.append((imagem_surface, nome_arquivo))
    except pygame.error as e:
        print(f"AVISO: Imagem {nome_arquivo} não carregada: {e}")
        
todas_imagens_com_id = dados_imagens * 2 
random.shuffle(todas_imagens_com_id)


class Carta:
    def __init__(self, imagem_e_id, x, y):
        self.imagem_frente = imagem_e_id[0]
        self.id_par = imagem_e_id[1]
        self.imagem_verso = VERSO_CARTA_IMG
        self.rect = pygame.Rect(x, y, TAMANHO_CARTA[0], TAMANHO_CARTA[1])
        self.virada = False
        self.encontrada = False

    def desenhar(self, janela):
        """Desenha a carta na tela, mostrando a frente ou o verso."""
        if self.virada:
            janela.blit(self.imagem_frente, self.rect)
        elif not self.encontrada:
            janela.blit(self.imagem_verso, self.rect)


def criar_cartas():
    """Cria e organiza as cartas na tela com layout centralizado e espaço para placar."""
    cartas = []
    
    # Parâmetros de Layout
    cartas_por_linha = 4 
    espacamento = 15     
    num_colunas = cartas_por_linha
    
    # Calcular a largura total usada e a margem para centralizar
    largura_usada = num_colunas * TAMANHO_CARTA[0] + (num_colunas - 1) * espacamento
    margem_x_inicial = (LARGURA - largura_usada) // 2
    
    # A margem Y é ajustada para começar abaixo da área do placar
    margem_y_inicial = AREA_JOGO_Y + 20 
    
    for i, img_e_id in enumerate(todas_imagens_com_id):
        linha = i // cartas_por_linha
        coluna = i % cartas_por_linha
        
        # Posição X
        x = margem_x_inicial + coluna * (TAMANHO_CARTA[0] + espacamento)
        
        # Posição Y
        y = margem_y_inicial + linha * (TAMANHO_CARTA[1] + espacamento)
        
        cartas.append(Carta(img_e_id, x, y))
        
    return cartas

def desenhar_texto(texto, tamanho, cor, x, y):
    
    caminho_fonte = None
    
    try:
        fonte = pygame.font.Font(None, tamanho) 
    except Exception:
        
        try:
            caminho_relativo_fonte = os.path.join(pygame.base.get_data_path(), 'freesansbold.ttf')
            caminho_fonte = resolver_caminho_recurso(caminho_relativo_fonte)
            fonte = pygame.font.Font(caminho_fonte, tamanho)
        except Exception:
            fonte = pygame.font.SysFont("Arial", tamanho)
            
    superficie_texto = fonte.render(texto, True, cor)
    retangulo_texto = superficie_texto.get_rect(center=(x, y))
    JANELA.blit(superficie_texto, retangulo_texto)



def game_loop():
    cartas = criar_cartas()
    viradas = []
    pontos = 0
    jogo_rodando = True
    ultima_jogada = time.time()
    aguardando_verificacao = False
    
    while jogo_rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jogo_rodando = False
            
            # Tratamento de clique
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if not aguardando_verificacao:
                    for carta in cartas:
                        if carta.rect.collidepoint(evento.pos) and not carta.virada and not carta.encontrada:
                            carta.virada = True
                            viradas.append(carta)
                            
                            if len(viradas) == 2:
                                aguardando_verificacao = True
                                ultima_jogada = time.time()

    
        if aguardando_verificacao and time.time() - ultima_jogada > 1.0:
            if viradas[0].id_par == viradas[1].id_par:
                pontos += 10
                viradas[0].encontrada = True
                viradas[1].encontrada = True
            else:
                viradas[0].virada = False
                viradas[1].virada = False
                
            viradas = []
            aguardando_verificacao = False
            
      
        cartas_encontradas = sum(1 for carta in cartas if carta.encontrada)
        if cartas_encontradas == len(cartas):
            JANELA.fill(COR_FUNDO)
            desenhar_texto("Fim de Jogo!", 80, COR_TEXTO, LARGURA // 2, ALTURA // 2 - 50)
            desenhar_texto(f"Sua Pontuação Final: {pontos}", 40, COR_TEXTO, LARGURA // 2, ALTURA // 2 + 20)
            pygame.display.flip()
            time.sleep(3)
            jogo_rodando = False

        
        JANELA.fill(COR_FUNDO)
        
        # 1. Desenhar Cartas
        for carta in cartas:
            carta.desenhar(JANELA) 
        
        # 2. Desenhar o Placar (Contador na parte de cima)
        pygame.draw.rect(JANELA, (10, 10, 10), (0, 0, LARGURA, ALTURA_PLACAR)) # Retângulo de fundo
        
        placar_x = LARGURA // 2
        placar_y = ALTURA_PLACAR // 2
        desenhar_texto(f"Pontuação: {pontos}", 30, COR_TEXTO, placar_x, placar_y)

        pygame.display.flip()
        RELOGIO.tick(60)

    pygame.quit()

if __name__ == "__main__":
    game_loop()