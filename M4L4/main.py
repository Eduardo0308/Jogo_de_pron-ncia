import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator
import random

# ---------------------------------------------------
# Banco de palavras por idioma e dificuldade
# ---------------------------------------------------
words_by_language = {
    "português": {
        "fácil": ["gato", "cachorro", "maçã", "leite", "sol",
                   "casa", "bola", "flor", "peixe", "livro"],
        "médio": ["escola", "amigo", "janela", "amarelo", "computador",
                   "trabalho", "viagem", "cozinha", "jardim", "biblioteca"],
        "difícil": ["tecnologia", "universidade", "informação", "pronúncia", "imaginação",
                     "desenvolvimento", "responsabilidade", "extraordinário",
                     "paralelepípedo", "otorrinolaringologista"]
    },
    "inglês": {
        "fácil": ["cat", "dog", "apple", "milk", "sun",
                   "house", "ball", "flower", "fish", "book"],
        "médio": ["school", "friend", "window", "yellow", "computer",
                   "kitchen", "garden", "library", "journey", "birthday"],
        "difícil": ["technology", "university", "information", "pronunciation", "imagination",
                     "development", "responsibility", "extraordinary",
                     "entrepreneurship", "otolaryngologist"]
    },
    "espanhol": {
        "fácil": ["gato", "perro", "manzana", "leche", "sol",
                   "casa", "pelota", "flor", "pez", "libro"],
        "médio": ["escuela", "amigo", "ventana", "amarillo", "computadora",
                   "trabajo", "viaje", "cocina", "jardín", "biblioteca"],
        "difícil": ["tecnología", "universidad", "información", "pronunciación", "imaginación",
                     "desarrollo", "responsabilidad", "extraordinario",
                     "otorrinolaringólogo", "paralelepípedo"]
    },
    "francês": {
        "fácil": ["chat", "chien", "pomme", "lait", "soleil",
                   "maison", "balle", "fleur", "poisson", "livre"],
        "médio": ["école", "ami", "fenêtre", "jaune", "ordinateur",
                   "travail", "voyage", "cuisine", "jardin", "bibliothèque"],
        "difícil": ["technologie", "université", "information", "prononciation", "imagination",
                     "développement", "responsabilité", "extraordinaire",
                     "anticonstitutionnellement", "otorhinolaryngologiste"]
    },
    "italiano": {
        "fácil": ["gatto", "cane", "mela", "latte", "sole",
                   "casa", "palla", "fiore", "pesce", "libro"],
        "médio": ["scuola", "amico", "finestra", "giallo", "computer",
                   "lavoro", "viaggio", "cucina", "giardino", "biblioteca"],
        "difícil": ["tecnologia", "università", "informazione", "pronuncia", "immaginazione",
                     "sviluppo", "responsabilità", "straordinario",
                     "otorinolaringoiatra", "precipitevolissimevolmente"]
    }
}

# ---------------------------------------------------
# Banco de frases por idioma e dificuldade
# ---------------------------------------------------
phrases_by_language = {
    "português": {
        "fácil": ["o gato dorme", "eu gosto de suco", "hoje está sol",
                   "o livro é meu", "a casa é grande"],
        "médio": ["eu fui para a escola", "meu amigo chegou cedo",
                   "a janela está aberta", "o jantar ficou pronto",
                   "nós vamos viajar amanhã"],
        "difícil": ["a tecnologia mudou a nossa forma de comunicação",
                     "a universidade oferece cursos de graduação e pós-graduação",
                     "a pronúncia correta exige bastante prática diária",
                     "o desenvolvimento sustentável é um desafio mundial",
                     "a responsabilidade individual afeta toda a sociedade"]
    },
    "inglês": {
        "fácil": ["the cat sleeps", "i like juice", "today is sunny",
                   "the book is mine", "the house is big"],
        "médio": ["i went to school", "my friend arrived early",
                   "the window is open", "dinner is ready",
                   "we will travel tomorrow"],
        "difícil": ["technology has changed the way we communicate",
                     "the university offers undergraduate and graduate courses",
                     "correct pronunciation requires a lot of daily practice",
                     "sustainable development is a global challenge",
                     "individual responsibility affects the whole society"]
    },
    "espanhol": {
        "fácil": ["el gato duerme", "me gusta el jugo", "hoy hace sol",
                   "el libro es mío", "la casa es grande"],
        "médio": ["fui a la escuela", "mi amigo llegó temprano",
                   "la ventana está abierta", "la cena está lista",
                   "vamos a viajar mañana"],
        "difícil": ["la tecnología cambió nuestra forma de comunicación",
                     "la universidad ofrece cursos de grado y posgrado",
                     "la pronunciación correcta requiere mucha práctica diaria",
                     "el desarrollo sostenible es un desafío mundial",
                     "la responsabilidad individual afecta a toda la sociedad"]
    },
    "francês": {
        "fácil": ["le chat dort", "j'aime le jus", "il fait soleil aujourd'hui",
                   "le livre est à moi", "la maison est grande"],
        "médio": ["je suis allé à l'école", "mon ami est arrivé tôt",
                   "la fenêtre est ouverte", "le dîner est prêt",
                   "nous allons voyager demain"],
        "difícil": ["la technologie a changé notre façon de communiquer",
                     "l'université propose des cours de licence et de master",
                     "la prononciation correcte demande beaucoup de pratique quotidienne",
                     "le développement durable est un défi mondial",
                     "la responsabilité individuelle affecte toute la société"]
    },
    "italiano": {
        "fácil": ["il gatto dorme", "mi piace il succo", "oggi c'è il sole",
                   "il libro è mio", "la casa è grande"],
        "médio": ["sono andato a scuola", "il mio amico è arrivato presto",
                   "la finestra è aperta", "la cena è pronta",
                   "domani viaggeremo"],
        "difícil": ["la tecnologia ha cambiato il nostro modo di comunicare",
                     "l'università offre corsi di laurea e post-laurea",
                     "la pronuncia corretta richiede molta pratica quotidiana",
                     "lo sviluppo sostenibile è una sfida globale",
                     "la responsabilità individuale riguarda tutta la società"]
    }
}

# Código de idioma exigido pelo Google Speech Recognition
codigos_reconhecimento = {
    "português": "pt-BR",
    "inglês": "en-US",
    "espanhol": "es-ES",
    "francês": "fr-FR",
    "italiano": "it-IT"
}

# Pontos ganhos de acordo com a dificuldade da fase
pontos_por_dificuldade = {
    "fácil": 1,
    "médio": 2,
    "difícil": 3
}

duration = 5        # segundos de gravação
sample_rate = 44100
total_rodadas = 5    # usado no modo normal

# ---------------------------------------------------
# Ordem das fases do jogo e quantas palavras por fase
# ---------------------------------------------------
ordem_das_fases = ["fácil", "médio", "difícil"]
palavras_por_fase = 3
acertos_para_passar_de_fase = 2  # precisa acertar pelo menos 2 de 3 pra avançar

# ---------------------------------------------------
# Escolha do modo de jogo (uma vez, no início)
# ---------------------------------------------------
print("=== Jogo de Pronúncia ===\n")

modo = input("Escolha o modo (normal, fase, frase): ").strip().lower()

if modo != "normal" and modo != "fase" and modo != "frase":
    print("Modo inválido!")
    exit()

# ---------------------------------------------------
# Escolha do idioma (uma vez, no início)
# ---------------------------------------------------

idioma = input("Escolha o idioma (português, inglês, espanhol, francês, italiano): ").strip().lower()

if idioma == "português":
    lista_de_niveis = words_by_language["português"]
elif idioma == "inglês":
    lista_de_niveis = words_by_language["inglês"]
elif idioma == "espanhol":
    lista_de_niveis = words_by_language["espanhol"]
elif idioma == "francês":
    lista_de_niveis = words_by_language["francês"]
elif idioma == "italiano":
    lista_de_niveis = words_by_language["italiano"]
else:
    print("Idioma inválido!")
    exit()

# Mesma lógica, só que buscando no banco de frases (usado no modo "frase")
if idioma == "português":
    lista_de_frases = phrases_by_language["português"]
elif idioma == "inglês":
    lista_de_frases = phrases_by_language["inglês"]
elif idioma == "espanhol":
    lista_de_frases = phrases_by_language["espanhol"]
elif idioma == "francês":
    lista_de_frases = phrases_by_language["francês"]
elif idioma == "italiano":
    lista_de_frases = phrases_by_language["italiano"]

codigo_reconhecimento = codigos_reconhecimento[idioma]

recognizer = sr.Recognizer()
translator = Translator()
pontuacao_total = 0

# ---------------------------------------------------
# MODO NORMAL - dificuldade fixa escolhida no início, 5 rodadas
# ---------------------------------------------------
if modo == "normal":

    dif = input("Escolha a dificuldade (fácil, médio, difícil): ").strip().lower()

    if dif == "fácil":
        palavras_disponiveis = lista_de_niveis["fácil"]
    elif dif == "médio":
        palavras_disponiveis = lista_de_niveis["médio"]
    elif dif == "difícil":
        palavras_disponiveis = lista_de_niveis["difícil"]
    else:
        print("Dificuldade inválida!")
        exit()

    pontos_da_rodada = pontos_por_dificuldade[dif]

    print(f"\nVamos jogar {total_rodadas} rodadas em {idioma} (nível {dif})!\n")

    for rodada in range(1, total_rodadas + 1):
        palavra_sorteada = random.choice(palavras_disponiveis)

        print(f"--- Rodada {rodada}/{total_rodadas} ---")
        print(f"Fale a palavra: {palavra_sorteada}")
        input("Pressione Enter quando estiver pronto para gravar...")

        print("Gravando...")
        recording = sd.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype="int16"
        )
        sd.wait()

        wav.write("output.wav", sample_rate, recording)
        print("Gravação concluída, reconhecendo...")

        try:
            with sr.AudioFile("output.wav") as source:
                audio = recognizer.record(source)

            texto_falado = recognizer.recognize_google(audio, language=codigo_reconhecimento)
            texto_falado_normalizado = texto_falado.strip().lower()
            palavra_normalizada = palavra_sorteada.strip().lower()

            print(f"Você disse: {texto_falado}")

            if texto_falado_normalizado == palavra_normalizada:
                print(f"✅ Acertou! +{pontos_da_rodada} ponto(s)\n")
                pontuacao_total += pontos_da_rodada
            else:
                print(f"❌ Errou! A palavra era '{palavra_sorteada}'\n")

        except sr.UnknownValueError:
            print("A fala não pôde ser reconhecida. Rodada sem pontos.\n")
        except sr.RequestError as e:
            print(f"Erro no serviço de reconhecimento: {e}\n")

    print("=== Fim de jogo! ===")
    print(f"Pontuação final: {pontuacao_total} de {total_rodadas * pontos_da_rodada} pontos possíveis")

    if pontuacao_total == total_rodadas * pontos_da_rodada:
        print("🏆 Pontuação perfeita! Parabéns!")
    elif pontuacao_total >= (total_rodadas * pontos_da_rodada) / 2:
        print("👏 Muito bem, continue treinando!")
    else:
        print("💪 Continue praticando, você vai melhorar!")

# ---------------------------------------------------
# MODO FASE - progride fácil → médio → difícil
# ---------------------------------------------------
elif modo == "fase":

    fase_alcancada = "nenhuma"

    print(f"\nVamos começar em {idioma}! Passe pelas fases fácil → médio → difícil.\n")

    for fase in ordem_das_fases:
        dif = fase
        palavras_disponiveis = lista_de_niveis[dif]
        pontos_da_rodada = pontos_por_dificuldade[dif]

        palavras_da_fase = random.sample(palavras_disponiveis, palavras_por_fase)
        acertos_na_fase = 0

        print(f"\n### FASE: {dif.upper()} ###")
        print(f"Você precisa acertar pelo menos {acertos_para_passar_de_fase} de {palavras_por_fase} palavras para avançar.\n")

        for rodada in range(1, palavras_por_fase + 1):
            palavra_sorteada = palavras_da_fase[rodada - 1]

            print(f"--- Palavra {rodada}/{palavras_por_fase} ---")
            print(f"Fale a palavra: {palavra_sorteada}")
            input("Pressione Enter quando estiver pronto para gravar...")

            print("Gravando...")
            recording = sd.rec(
                int(duration * sample_rate),
                samplerate=sample_rate,
                channels=1,
                dtype="int16"
            )
            sd.wait()

            wav.write("output.wav", sample_rate, recording)
            print("Gravação concluída, reconhecendo...")

            try:
                with sr.AudioFile("output.wav") as source:
                    audio = recognizer.record(source)

                texto_falado = recognizer.recognize_google(audio, language=codigo_reconhecimento)
                texto_falado_normalizado = texto_falado.strip().lower()
                palavra_normalizada = palavra_sorteada.strip().lower()

                print(f"Você disse: {texto_falado}")

                if texto_falado_normalizado == palavra_normalizada:
                    print(f"✅ Acertou! +{pontos_da_rodada} ponto(s)\n")
                    pontuacao_total += pontos_da_rodada
                    acertos_na_fase += 1
                else:
                    print(f"❌ Errou! A palavra era '{palavra_sorteada}'\n")

            except sr.UnknownValueError:
                print("A fala não pôde ser reconhecida. Rodada sem pontos.\n")
            except sr.RequestError as e:
                print(f"Erro no serviço de reconhecimento: {e}\n")

        print(f"Fim da fase {dif}: {acertos_na_fase}/{palavras_por_fase} acertos.")

        if acertos_na_fase >= acertos_para_passar_de_fase:
            fase_alcancada = dif
            print(f"🎉 Fase '{dif}' concluída! Avançando...\n")
        else:
            print(f"💀 Você não conseguiu acertos suficientes na fase '{dif}'. Fim de jogo!\n")
            break
    else:
        # Executa apenas se o for terminar sem 'break', ou seja, passou por todas as fases
        print("🏆 Parabéns, você concluiu todas as fases do jogo!\n")

    print("=== Fim de jogo! ===")
    print(f"Idioma: {idioma}")
    print(f"Última fase concluída: {fase_alcancada}")
    print(f"Pontuação total: {pontuacao_total}")

# ---------------------------------------------------
# MODO FRASE - dificuldade fixa escolhida no início, 5 rodadas com frases
# ---------------------------------------------------
elif modo == "frase":

    dif = input("Escolha a dificuldade (fácil, médio, difícil): ").strip().lower()

    if dif == "fácil":
        frases_disponiveis = lista_de_frases["fácil"]
    elif dif == "médio":
        frases_disponiveis = lista_de_frases["médio"]
    elif dif == "difícil":
        frases_disponiveis = lista_de_frases["difícil"]
    else:
        print("Dificuldade inválida!")
        exit()

    pontos_da_rodada = pontos_por_dificuldade[dif]

    print(f"\nVamos jogar {total_rodadas} rodadas em {idioma} (nível {dif})!\n")

    for rodada in range(1, total_rodadas + 1):
        frase_sorteada = random.choice(frases_disponiveis)

        print(f"--- Rodada {rodada}/{total_rodadas} ---")
        print(f"Fale a frase: {frase_sorteada}")
        input("Pressione Enter quando estiver pronto para gravar...")

        print("Gravando...")
        recording = sd.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype="int16"
        )
        sd.wait()

        wav.write("output.wav", sample_rate, recording)
        print("Gravação concluída, reconhecendo...")

        try:
            with sr.AudioFile("output.wav") as source:
                audio = recognizer.record(source)

            texto_falado = recognizer.recognize_google(audio, language=codigo_reconhecimento)
            texto_falado_normalizado = texto_falado.strip().lower()
            frase_normalizada = frase_sorteada.strip().lower()

            print(f"Você disse: {texto_falado}")

            if texto_falado_normalizado == frase_normalizada:
                print(f"✅ Acertou! +{pontos_da_rodada} ponto(s)\n")
                pontuacao_total += pontos_da_rodada
            else:
                print(f"❌ Errou! A frase era '{frase_sorteada}'\n")

        except sr.UnknownValueError:
            print("A fala não pôde ser reconhecida. Rodada sem pontos.\n")
        except sr.RequestError as e:
            print(f"Erro no serviço de reconhecimento: {e}\n")

    print("=== Fim de jogo! ===")
    print(f"Pontuação final: {pontuacao_total} de {total_rodadas * pontos_da_rodada} pontos possíveis")

    if pontuacao_total == total_rodadas * pontos_da_rodada:
        print("🏆 Pontuação perfeita! Parabéns!")
    elif pontuacao_total >= (total_rodadas * pontos_da_rodada) / 2:
        print("👏 Muito bem, continue treinando!")
    else:
        print("💪 Continue praticando, você vai melhorar!")