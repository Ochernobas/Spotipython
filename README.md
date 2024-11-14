# Spotipython

**Spotipython** é uma aplicação em Python para fazer download de músicas do Spotify, com a funcionalidade adicional de editar automaticamente as tags das músicas, como Nome, Álbum e Artistas. O projeto utiliza uma interface gráfica amigável para tornar o processo de download e organização de músicas simples e acessível.

## Funcionalidades

- **Download de músicas do Spotify**: Converte automaticamente as músicas para formato mp3 a partir de links do Spotify.
- **Edição automática de tags**: As tags de Nome, Álbum e Artista são preenchidas automaticamente com base nas informações do Spotify.
- **Interface intuitiva**: Desenvolvido com a biblioteca `Customtkinter` para uma interface amigável.
  
## Tecnologias Utilizadas

O projeto foi desenvolvido em Python e faz uso das seguintes bibliotecas:

- **Customtkinter**: Para a criação de uma interface gráfica amigável e moderna.
- **Pillow**: Para manipulação de imagens, como capas de álbuns.
- **requests**: Para fazer requisições HTTP e obter informações de músicas.
- **dotenv**: Para gerenciar variáveis de ambiente, incluindo chaves de API.
- **music_tag**: Para editar as tags de metadados das músicas.
- **youtube_search_python**: Para realizar buscas de vídeos no YouTube, ajudando no processo de download.
- **pytubefix**: Para baixar o áudio dos vídeos do YouTube.
- **webbrowser**: Para abrir links externos diretamente no navegador.

- Além disso é necessário o **FFmpeg** instalado no computador para o funcionamento do código.

### Estrutura do Projeto

1. **main.py**
   - **Classe `Main`**: Controla a lógica principal do programa, conectando a interface de usuário e as diferentes funcionalidades.
     - `input_received(link)`: Recebe o link do Spotify inserido pelo usuário, confere se é um link válido e o envia à classe `Spotify`.
     - `spotify_reader()`: Cria objetos `Track` com informações da música a partir dos dados recebidos da API do Spotify.
     - `youtube_searcher()`: Encontra a URL do YouTube para cada faixa usando a classe `YoutubeSearch` e exibe as músicas na interface usando a classe `Screen`.
     - `download_tracks(requested)`: Faz o download das faixas solicitadas usando a classe `Downloader`; pode baixar uma faixa específica ou todas.
     - `delete_track(track)`: Remove uma faixa da lista e mata o Objeto respectivo.

2. **tela.py**
   - **Classe `Screen`**: Define a interface gráfica principal do programa usando `customtkinter`, gerenciando todos os componentes visuais e as interações do usuário.
     - `search()`: Obtém o link de entrada e chama o método `input_received` da classe `Main`.
     - `download(t)`: Envia à classe `Main` as músicas selecionadas para download.
     - `delete(t)`: Remove uma faixa da interface e do controle principal.
     - `draw_tracks(tracks)`: Renderiza as músicas baixadas na interface, utilizando a classe `LowerFrame`.
   - **Classe `UpperFrame`**: Gerencia o campo de entrada de link, o botão de busca e o botão de "baixar todos".
   - **Classe `LowerFrame`**: Exibe as faixas com a imagem do álbum e informações adicionais, permitindo edições rápidas e interações (como baixar ou remover faixas individualmente).

3. **spotify_track.py**
   - **Classe `Track`**: Define um objeto para armazenar informações de uma música, incluindo título, álbum, artistas, capa e URL do YouTube.
     - `handle_artists()`: Processa os nomes dos artistas para garantir que estejam no formato correto.
     - `handle_name()`: Remove caracteres proibidos do título da música para evitar erros nos nomes dos arquivos.
     - `download_image_cover()`: Baixa a imagem da capa do álbum da música.
     - `edit_values`: Recebe os valores editados pelo usuário.
     - `string_to_list`: Transforma a string de artistas em uma lista.
     - `__del__`: Deleta o Objeto.

4. **spotify_api.py**
   - **Classe `Spotify`**: Define um objeto para se comunicar com a API do Spotify.
     - `getToken` e `get_auth_header`: Fazem a autenticação com o Spotify. Código copiado do canal [Tec with Tim](https://www.youtube.com/watch?v=WAmEZBEeNmg).
     - `search_for_playlist` e `search_for_music`: Têm um funcionamento igual, fazem a requisição para a API.
     - `input`: Recebe o input do usuário e checa se é uma playlist ou música individual.

5. **youtube_search.py**
   - **Classe `YoutubeSearch`**: Realiza a busca por vídeos no YouTube usando o título e os artistas da música.
     - `getURL(track)`: Pesquisa o áudio oficial da música no YouTube e retorna o link do vídeo correspondente (Quase sempre encontra certo, mas vou adicionar a funcionalidade de editar manualmente no futuro).

6. **downloader.py**
   - **Classe `Downloader`**: Responsável por gerenciar o download, conversão e edição de tags das músicas.
     - `download_track(track)`: Faz o download do vídeo do YouTube usando a URL armazenada no objeto `Track` em MP4.
     - `convert_track(path, track)`: Usa o FFmpeg para converter o arquivo baixado de MP4 para MP3.
     - `tag_track(path, track)`: Edita as tags de metadados da música, como título, álbum e artistas, utilizando o `music_tag`.
