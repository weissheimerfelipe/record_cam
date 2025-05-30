import os
import sys
import subprocess
import time
import getpass
from datetime import datetime

def verificar_instalacao():
    try:
        __import__('cv2')
        return True
    except:
        return False

def instalar_opencv():
    print("[*] Verificando instalação do OpenCV...")
    if verificar_instalacao():
        print("[+] OpenCV já está instalado")
        return True
    
    print("[*] Instalando OpenCV...")
    tentativas = [
        [sys.executable, "-m", "pip", "install", "opencv-python", "--user", "--quiet"],
        [sys.executable, "-m", "pip", "install", "opencv-python-headless", "--user", "--quiet"]
    ]
    
    for cmd in tentativas:
        try:
            subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            if verificar_instalacao():
                print("[+] OpenCV instalado com sucesso")
                return True
        except:
            continue
    
    print("[-] Falha na instalação do OpenCV")
    return False

def testar_acesso_rede(caminho_rede):
    try:
        if not os.path.exists(caminho_rede):
            print(f"[!] Pasta não encontrada: {caminho_rede}")
            return False
            
        arquivo_teste = os.path.join(caminho_rede, "teste_permissao.tmp")
        with open(arquivo_teste, 'w') as f:
            f.write("teste")
        os.remove(arquivo_teste)
        return True
    except Exception as e:
        print(f"[-] Erro ao acessar a pasta: {str(e)}")
        return False

def gravar_video():
    try:
        import cv2
        
        # 1. Configurações de gravação
        duracao = 15  # segundos
        
        # 2. Caminho de rede - MODIFIQUE AQUI COM SEU CAMINHO CORRETO
        servidor = "endereco_do_servidor"
        compartilhamento = "nome_do_compartilhamento"
        pasta = "pasta_de_video"
        caminho_rede = fr"\\{servidor}\{compartilhamento}\{pasta}"
        
        # 3. Verificação do acesso
        if not testar_acesso_rede(caminho_rede):
            raise RuntimeError(f"Não foi possível acessar: {caminho_rede}")
            
        # 4. Nome do arquivo com usuário e timestamp
        nome_usuario = getpass.getuser()  # Ou os.getenv("USERNAME")
        nome_arquivo = f"VIDEO_{nome_usuario}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
        caminho_completo = os.path.join(caminho_rede, nome_arquivo)
        
        # 5. Inicialização da câmera
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not cap.isOpened():
            raise RuntimeError("Câmera não detectada")
            
        # 6. Configuração do vídeo
        largura = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        altura = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = 30.0
        
        # 7. Cria o VideoWriter
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(caminho_completo, fourcc, fps, (largura, altura))
        
        print(f"[*] Iniciando gravação de {duracao} segundos...")
        start_time = time.time()
        
        # 8. Loop de gravação
        while (time.time() - start_time) < duracao:
            ret, frame = cap.read()
            if ret:
                out.write(frame)
        
        print(f"[+] Vídeo salvo com sucesso em:\n{caminho_completo}")

    except Exception as e:
        print(f"[-] Erro durante a gravação: {str(e)}")
    finally:
        if 'cap' in locals() and cap.isOpened():
            cap.release()
        if 'out' in locals():
            out.release()
        if 'cv2' in locals():
            cv2.destroyAllWindows()

if __name__ == "__main__":
    # 1. Instalação do OpenCV
    if not instalar_opencv():
        print("""
        [!] Não foi possível instalar o OpenCV automaticamente.
        Por favor instale manualmente com:
        python -m pip install opencv-python --user
        """)
        sys.exit(1)
    
    # 2. Execução da gravação
    gravar_video()
    
    # 3. Manter janela aberta no Windows
    if os.name == 'nt':
        input("Pressione Enter para sair...")
