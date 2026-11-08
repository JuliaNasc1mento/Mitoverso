from app import db
from app.models.mito import Mito


def cadastrar_mitos():
    mitos = [
        {
            "titulo": "O Caos",
            "resumo": "O Caos é a primeira divindade primordial e o abismo vazio e ilimitado que existiu antes de tudo no universo. Ele funcionou como a origem de onde nasceram os primeiros deuses.",
            "conteudo": "Antes que o tempo abrisse seus olhos, antes que a luz ousasse nascer, existia apenas o Caos. Não um vazio frio…, mas um ser. Um titã primordial sem forma fixa, uma presença antiga demais para ser compreendida, tão vasta que preenchia tudo — e tão solitária que preenchia nada. O Caos era respiração sem corpo, pensamento sem voz. Era escuro e profundo como o primeiro silêncio. Uma divindade adormecida em si mesma, guardando no peito as sementes de tudo que um dia existiria. Durante eras incontáveis — eras que não possuíam nome — Caos permaneceu assim. Até que algo dentro dele despertou. Uma lembrança? Um sonho? Ninguém sabe. Apenas sabemos que, quando ele se moveu, mesmo que por um segundo, o universo estremeceu… e nasceu. Da vastidão viva do Caos surgiu Gaia, a Terra. Ela não brotou como um planeta pronto, mas como uma deusa que abriu os olhos pela primeira vez. Gaia sentiu seu próprio peso, sua força, e se expandiu para dar forma ao chão, às montanhas, aos vales. Onde antes havia apenas ausência, agora havia corpo, estabilidade, promessa. E, quando Gaia firmou seus pés, outra presença emergiu: Tártaro. Profundo, sombrio, antigo — tão velho quanto Gaia, tão inevitável quanto Caos. Tártaro abriu seus abismos silenciosos no coração do cosmos, guardando a escuridão que não deveria tocar o mundo da superfície. Era o contraponto perfeito: enquanto Gaia criava, Tártaro continha. Enquanto um erguia, o outro afundava. Mas Caos ainda não havia terminado. De seu próprio sopro primordial surgiu Eros, o Desejo. Não o jovem alado das liras poéticas, mas uma força brilhante e indomável. Eros era impulso, união, vontade. A centelha que fez Gaia e Tártaro conscientes de que não precisavam existir sozinhos. Graças a ele, a criação ganhou movimento. Então vieram Érebo, a escuridão profunda, e Nix, a Noite eterna. Eles caminharam juntos pela imensidão recém-nascida, tecendo véus de sombra que não traziam medo, mas repouso. De sua união surgiram Éter, a luz pura dos céus, e Hémera, o Dia suave que acompanha a aurora. Assim, pela primeira vez, o cosmos conheceu ciclos — claridade e escuridão, vigília e descanso. Gaia observou tudo isso com admiração. Ela sentia o universo crescendo ao seu redor…, mas também sentia que algo faltava. Um companheiro. Um horizonte. Alguém que a envolvesse e completasse sua presença. E foi desse desejo que seu grito se espalhou pelo vazio. Um chamado tão poderoso que ecoou no coração do próprio Caos. E o Céu nasceu. Urano, o primeiro dos céus, surgiu como um manto infinito, estendendo-se sobre Gaia, tocando-a como um par de mãos suaves e brilhantes. Ali, juntos, Terra e Céu se encontraram. E desse encontro, novos deuses, novas forças e novos destinos começaram a despertar. Assim, das profundezas do Caos — o deus adormecido, o primeiro a existir — brotou o princípio de tudo que viria depois.",
            "imagem": "img/mitos/img04 M01_40.jpg",
            "audio": "audio/mitos/Mito 01 - O Caos.mp3"
        },

    ]

    for dados in mitos:
        existe = Mito.query.filter_by(titulo=dados["titulo"]).first()

        if existe is None:
            mito = Mito(**dados)
            db.session.add(mito)

    db.session.commit()