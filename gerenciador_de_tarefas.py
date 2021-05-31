import pygame
import psutil
import platform
import time

BRANCO = (255,255,255)
PRETO = (0,0,0)
LARANJA = (246,130,0)
VERMELHO = (230,0,0)
AZUL = (0,0,255)

pygame.init()
largura_tela, altura_tela = 1024, 600
tela = pygame.display.set_mode((largura_tela, altura_tela))
tela.fill(BRANCO)


def mostra_texto(texto, pos, cor, cent=False):
    font = pygame.font.SysFont('calibri', 22, bold=True)
    text = font.render(f"{texto}", 1, cor)
    if cent:
        textpos = text.get_rect(center=pos,)
        tela.blit(text, textpos)
    else:
        tela.blit(text, pos)

def desenha_abas():
    aba0 = pygame.Rect(1, 0, 254, 50)
    pygame.draw.rect(tela, PRETO, aba0)
    mostra_texto("CPU",(128,25), BRANCO, cent=True)

    aba1 = pygame.Rect(256, 0, 255, 50)
    pygame.draw.rect(tela, PRETO, aba1)
    mostra_texto("Memória",(384,25), BRANCO, cent=True)

    aba2 = pygame.Rect(512, 0, 255, 50)
    pygame.draw.rect(tela, PRETO, aba2)
    mostra_texto("Rede",(640,25), BRANCO, cent=True)

    aba3 = pygame.Rect(768, 0, 255, 50)
    pygame.draw.rect(tela, PRETO, aba3)
    mostra_texto("ABA TRÊS",(896,25), BRANCO, cent=True)
    return [aba0, aba1, aba2, aba3]

def mostra_uso_disco():
    disco = psutil.disk_usage('.')
    larg = largura_tela - 2*20
    pygame.draw.rect(tela, AZUL, (20, 260, larg, 50))
    larg = larg*disco.percent/100
    pygame.draw.rect(tela, VERMELHO, (20, 260, larg, 50))
    total = format_memory(disco.total)
    texto_barra = "Uso de Disco (Total: " + str(total) + " GB):"
    mostra_texto(texto_barra, (20,240), PRETO)

def mostra_uso_memoria():
    mem = psutil.virtual_memory()
    larg = largura_tela - 2*20
    pygame.draw.rect(tela, AZUL, (20, 370, larg, 50))
    larg = larg*mem.percent/100
    pygame.draw.rect(tela, VERMELHO, (20, 370, larg, 50))
    total = format_memory(mem.total)
    texto_barra = "Uso de Memória (Total: " + str(total) + " GB):"
    mostra_texto(texto_barra, (20,350), PRETO)

def format_memory(info):
    return round(info/(1024*1024*1024), 2)

def cpu():
    processador = platform.processor()
    plat = platform.node()
    text = f"Processador:   {processador}"
    mostra_texto(text,(20,120), PRETO)
    text = f"Plataforma:     {plat}"
    mostra_texto(text,(20,150), PRETO)

def mostra_uso_cpu():
    capacidade = psutil.cpu_percent(interval=0)
    larg = largura_tela - 2*20
    pygame.draw.rect(tela, AZUL, (20, 260, larg, 50))
    larg = larg*capacidade/100
    pygame.draw.rect(tela, VERMELHO, (20, 260, larg, 50))
    texto_barra = "Uso da CPU:"
    mostra_texto(texto_barra, (20,240), PRETO)

def memoria():
    disco = psutil.disk_usage('.')
    text = f"Total:{format_memory(disco.total):19} GB"
    mostra_texto(text,(20,120), PRETO)
    text = f"Em uso:{format_memory(disco.used):15} GB"
    mostra_texto(text,(20,140), PRETO)
    text = f"Livre: {format_memory(disco.free):19} GB"
    mostra_texto(text,(20,160), PRETO)
    text = f"Percentual de Disco Usado:   {disco.percent:}%"
    mostra_texto(text,(20,200), PRETO)

def rede():
    dic_interfaces = psutil.net_if_addrs()
    ip = dic_interfaces['Wi-Fi'][1].address
    text = f"Endereço IP:   {ip}"
    mostra_texto(text,(20,120), PRETO)

def mostra_conteudo(i):
    if i==0:
        cpu()
        mostra_uso_cpu()
        time.sleep(1)

    elif i==1:
        memoria()
        mostra_uso_disco()
        mostra_uso_memoria()

    elif i==2:
        rede()

terminou = False
i=0
texto='Aba zero'
while not terminou:
    abas = desenha_abas()
    mostra_texto("Projeto de Bloco", (512, 70), PRETO, cent=True)
    #mostra_texto(texto,(512,94),PRETO, cent=True)
    mostra_conteudo(i)


    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminou = True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                for index, aba in enumerate(abas):
                    if aba.collidepoint(pos):
                        if index==0:
                            i=0
                        elif index==1:
                            i=1
                        elif index==2:
                            i=2
                            texto=f"Clicou na aba {index}"
                        else:
                            i=3
                            texto=f"Clicou na aba {index}"

    pygame.display.update()
    tela.fill(BRANCO)
pygame.display.quit()
pygame.quit()
