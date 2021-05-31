import pygame
import psutil
import platform

BRANCO = (255,255,255)
PRETO = (0,0,0)
LARANJA = (246,130,0)
VERMELHO = (230,0,0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)

pygame.init()
largura_tela, altura_tela = 1024, 800
tela = pygame.display.set_mode((largura_tela, altura_tela))
tela.fill(BRANCO)
terminou = False

def mostra_texto(texto, pos, cor):
    font = pygame.font.Font(None, 24)
    text = font.render(f"{texto}", 1, cor)
    textpos = text.get_rect(center=pos,)
    tela.blit(text, textpos)

def desenha_abas():
    aba0 = pygame.Rect(0, 0, 255, 50)
    pygame.draw.rect(tela, PRETO, aba0)
    mostra_texto("Memória",(128,25), BRANCO)

    aba1 = pygame.Rect(256, 0, 255, 50)
    pygame.draw.rect(tela, PRETO, aba1)
    mostra_texto("CPU",(384,25), BRANCO)

    aba2 = pygame.Rect(512, 0, 255, 50)
    pygame.draw.rect(tela, PRETO, aba2)
    mostra_texto("Disco",(640,25), BRANCO)

    aba3 = pygame.Rect(768, 0, 256, 50)
    pygame.draw.rect(tela, PRETO, aba3)
    mostra_texto("Redes",(896,25), BRANCO)
    return [aba0, aba1, aba2, aba3]

def mostra_uso_memoria():
    mem = psutil.disk_usage('.')
    larg = largura_tela - 2*20
    pygame.draw.rect(tela, AZUL, (20, 250, larg, 70))
    larg = larg*mem.percent/100
    pygame.draw.rect(tela, VERMELHO, (20, 250, larg, 70))
    total = round(mem.total/(1024*1024*1024),2)
    font = pygame.font.Font(None, 24)
    texto_barra = "Uso de Memória (Total: " + str(total) + "GB):"
    text = font.render(texto_barra, 1, PRETO)
    textpos = (20, 230)
    tela.blit(text, textpos)

def mostra_uso_cpu():
    capacidade = psutil.cpu_percent(interval=0)
    percentual = capacidade/100
    larg = largura_tela - 2*20
    pygame.draw.rect(tela, AZUL, (20, 260, larg, 50))
    larg = larg*percentual
    pygame.draw.rect(tela, VERMELHO, (20, 260, larg, 50))
    texto_barra = f"Uso da CPU: {percentual*100:.2f} %"
    mostra_texto(texto_barra, (120,240), PRETO)

def format_memory(info):
    return round(info/(1024*1024*1024), 2)

def disco():
    mostra_texto("Disco",(512,100),PRETO)
    disco = psutil.disk_usage('.')
    text = f"Total:   {format_memory(disco.total)} GB"
    mostra_texto(text,(90, 120),PRETO)
    text = f"Em uso:  {format_memory(disco.used)} GB"
    mostra_texto(text, (100, 140), PRETO)
    text = f"Livre:   {format_memory(disco.free)} GB"
    mostra_texto(text, (92, 160), PRETO)
    text = f"Percentual de Disco Usado: {disco.percent}%"
    mostra_texto(text, (160, 180), PRETO)

def ram():
    mostra_texto("Memória", (512,100), PRETO)
    mem = psutil.virtual_memory()
    total = round(mem.total/(1024*1024*1024), 2)
    text = f"Memória Total: {total} GB"
    mostra_texto(text, (160,180), PRETO)
    larg = largura_tela - 2*20
    pygame.draw.rect(tela, AZUL, (20, 250, larg, 70))
    larg = larg*mem.percent/100
    pygame.draw.rect(tela, VERMELHO, (20, 250, larg, 70))
    text = f"Percentual Usado: {mem.percent:.2f} %"
    mostra_texto(text, (180, 200), PRETO)
    font = pygame.font.Font(None, 24)
    texto_barra = "Uso de Memória (Total: " + str(total) + "GB):"
    text = font.render(texto_barra, 1, PRETO)
    textpos = (20, 230)
    tela.blit(text, textpos)

def cpu():
    mostra_texto("CPU",(512,100),PRETO)
    processador = platform.processor()
    nome = platform.node()
    plataforma = platform.platform()
    sistema = platform.system()
    text = f"Processador: {processador}. "
    mostra_texto(text, (300, 160), PRETO)
    text = f"Nome: {nome}. " 
    mostra_texto(text, (150, 180), PRETO)
    text = f"Plataforma: {plataforma}. "
    mostra_texto(text, (200, 220), PRETO)
    text = f"Sistema: {sistema}. "
    mostra_texto(text, (120, 200), PRETO)

def redes():
    dic_interfaces = psutil.net_if_addrs()
    endereco_ip = dic_interfaces['Wi-Fi'][1].address
    text = f"Endereço IP:   {endereco_ip}"
    mostra_texto(text,(180,200), PRETO)

while not terminou:
    abas = desenha_abas()
    mostra_texto("Projeto de Bloco - Gerenciador de Tarefas",(512,70),PRETO)
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminou = True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                #tela.fill(BRANCO)
                for index, aba in enumerate(abas):
                    if aba.collidepoint(pos):
                        tela.fill(BRANCO)
                        #mostra_texto(f"Clicou na aba {index}",(512,94),PRETO)
                        if index == 0:
                            ram()
                        if index == 1:
                            cpu()
                            mostra_uso_cpu()
                        if index == 2:
                            disco()
                            mostra_uso_memoria()
                        if index == 3:
                            redes()
    pygame.display.update()
pygame.display.quit()
pygame.quit()