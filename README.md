# # Gravação de Vídeo e Armazenamento em Rede

Este script em Python foi desenvolvido para realizar a gravação de vídeos a partir de uma câmera conectada ao computador e armazená-los em uma pasta compartilhada em rede. O vídeo gerado será salvo com um nome único, que inclui o nome do usuário e a data/hora da gravação.

## Funcionalidades

- Verifica e instala automaticamente o OpenCV (se necessário).
- Verifica se é possível acessar a pasta compartilhada em rede.
- Grava um vídeo com duração de 15 segundos (configurável).
- Salva o vídeo gerado na pasta de rede especificada.
- Usa a câmera conectada ao computador para capturar o vídeo.

## Requisitos

- Python 3.x
- Pacote OpenCV (`opencv-python` ou `opencv-python-headless`)

## Como Usar

1. **Instalar dependências**: O script verifica automaticamente se o OpenCV está instalado. Caso contrário, ele tenta instalá-lo. Se não for possível instalar, você pode instalar manualmente usando o seguinte comando:

   ```bash
   python -m pip install opencv-python --user
