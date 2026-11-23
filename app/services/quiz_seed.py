from app import db
from app.models.quiz import Pergunta

# (nível, enunciado, A, B, C, D, correta, explicação)
# Perguntas de exemplo: troque/adicione as suas aqui e rode "flask quiz seed" de novo.
PERGUNTAS = [
    # ---------- Nível 1: Fácil ----------
    (1, "Quem era o rei dos deuses do Olimpo?",
        "Poseidon", "Zeus", "Hades", "Apolo", "B",
        "Zeus venceu os Titãs e passou a governar o céu e os outros deuses."),
    (1, "Qual deusa representa a sabedoria e a estratégia de guerra?",
        "Atena", "Afrodite", "Hera", "Deméter", "A",
        "Atena é a deusa da sabedoria e protetora da cidade de Atenas."),
    (1, "Quem governava o mundo dos mortos?",
        "Ares", "Hermes", "Hades", "Dionísio", "C",
        "Hades recebeu o submundo como seu reino na divisão do mundo entre os três irmãos."),
    (1, "Qual deus governava os mares?",
        "Zeus", "Hefesto", "Apolo", "Poseidon", "D",
        "Poseidon era o senhor dos mares e dos terremotos, e seu símbolo era o tridente."),
    (1, "Qual criatura tinha serpentes no lugar dos cabelos?",
        "Minotauro", "Medusa", "Hidra", "Quimera", "B",
        "Medusa transformava em pedra quem olhasse nos olhos dela."),

    # ---------- Nível 2: Médio ----------
    (2, "Qual Titã devorava os próprios filhos com medo de ser destronado?",
        "Atlas", "Cronos", "Jápeto", "Oceano", "B",
        "Cronos engolia os filhos ao nascerem, até que Reia escondeu Zeus."),
    (2, "Quem roubou o fogo dos deuses para entregá-lo aos humanos?",
        "Prometeu", "Epimeteu", "Hermes", "Hefesto", "A",
        "Por esse ato, Prometeu foi castigado por Zeus."),
    (2, "Quem é a mãe de Perséfone?",
        "Hera", "Reia", "Deméter", "Héstia", "C",
        "Deméter é a deusa da colheita, e o sumiço da filha explica a mudança das estações."),
    (2, "Qual herói decapitou a Medusa?",
        "Teseu", "Perseu", "Jasão", "Aquiles", "B",
        "Perseu usou o reflexo do escudo para não olhar a Medusa diretamente."),
    (2, "Quais gêmeos eram filhos de Zeus e Leto?",
        "Castor e Pólux", "Hélio e Selene", "Apolo e Ártemis", "Fobos e Deimos", "C",
        "Apolo (o Sol e a música) e Ártemis (a caça e a Lua) nasceram na ilha de Delos."),

    # ---------- Nível 3: Difícil ----------
    (3, "Quem foi o pai dos Titãs?",
        "Urano", "Caos", "Zeus", "Érebo", "A",
        "Urano (o Céu) e Gaia (a Terra) tiveram os doze Titãs."),
    (3, "O que restou dentro do jarro de Pandora depois que ela o abriu?",
        "A coragem", "A esperança", "A sabedoria", "A paz", "B",
        "Todos os males escaparam e apenas a esperança ficou no fundo do jarro."),
    (3, "De qual parte do corpo de Zeus nasceu Dionísio?",
        "Da cabeça", "Do braço", "Da coxa", "Do coração", "C",
        "Zeus costurou o bebê na própria coxa até que ele estivesse pronto para nascer."),
    (3, "Qual foi o primeiro dos doze trabalhos de Héracles?",
        "Capturar o Cérbero", "Matar o Leão de Nemeia", "Matar a Hidra de Lerna", "Limpar os estábulos de Áugias", "B",
        "O primeiro trabalho foi derrotar o Leão de Nemeia, cuja pele era impenetrável."),
    (3, "Qual monstro gigantesco desafiou Zeus e acabou preso sob o monte Etna?",
        "Equidna", "Cérbero", "Ladão", "Tifão", "D",
        "Tifão, filho de Gaia e do Tártaro, foi o último grande desafiante de Zeus."),

    # ---------- Nível 4: Lendário ----------
    (4, "Segundo a Teogonia de Hesíodo, qual foi o primeiro ser a surgir?",
        "Gaia", "Caos", "Érebo", "Eros", "B",
        "Antes de tudo veio o Caos; depois surgiram Gaia, o Tártaro e Eros."),
    (4, "Qual presente de Atena fez os atenienses a escolherem como protetora da cidade, em vez de Poseidon?",
        "Uma lança de ouro", "Uma fonte de água doce", "Uma oliveira", "Um cavalo", "C",
        "A oliveira, que dá alimento, óleo e madeira, foi considerada mais valiosa."),
    (4, "Como se chamava a mãe de Aquiles, que o mergulhou no rio Estige?",
        "Anfitrite", "Leda", "Tétis", "Hécuba", "C",
        "Tétis, uma Nereida, segurou o filho pelo calcanhar, que ficou sem proteção."),
    (4, "Que seres de cem braços foram libertados do Tártaro e lutaram ao lado de Zeus na Titanomaquia?",
        "Ciclopes", "Hecatônquiros", "Centauros", "Sátiros", "B",
        "Briareu, Coto e Giges, os Hecatônquiros, tinham cem braços e cinquenta cabeças."),
    (4, "Quem é a Titânide da memória e mãe das nove Musas?",
        "Têmis", "Reia", "Febe", "Mnemósine", "D",
        "Mnemósine teve as nove Musas com Zeus."),
]


def cadastrar_perguntas_iniciais():
    # Só cadastra o que ainda não existe, então pode rodar mais de uma vez
    novas = 0

    for nivel, enunciado, a, b, c, d, correta, explicacao in PERGUNTAS:
        ja_existe = db.session.scalar(db.select(Pergunta).filter_by(enunciado = enunciado))
        if ja_existe:
            continue

        db.session.add(Pergunta(
            nivel = nivel, enunciado = enunciado,
            opcao_a = a, opcao_b = b, opcao_c = c, opcao_d = d,
            correta = correta, explicacao = explicacao
        ))
        novas += 1

    db.session.commit()
    return novas
