words_by_level = {
    "fácil": [
        "gato", "cachorro", "maçã", "leite", "sol",
        "casa", "bola", "flor", "peixe", "livro",
        "mesa", "porta", "água", "pão", "lua"
    ],
    "médio": [
        "casa", "escola", "amigo", "janela", "amarelo",
        "computador", "trabalho", "viagem", "cozinha", "jardim",
        "biblioteca", "montanha", "felicidade", "aniversário", "vizinho"
    ],
    "difícil": [
        "tecnologia", "universidade", "informação", "pronúncia", "imaginação",
        "desenvolvimento", "responsabilidade", "extraordinário", "circunstância", "aproximadamente",
        "eletrocardiograma", "inconstitucionalidade", "paralelepípedo", "hipopótamo", "otorrinolaringologista"
    ]
}


dif = input("Dificuldade:"(words_by_level))

if dif == "fácil":
    print(words_by_level("fácil"))