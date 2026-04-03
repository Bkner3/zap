import json

def save_packages(json_entrada, nomes, ficheiro_saida):
    with open(json_entrada, "r", encoding="utf-8") as f:
        data = json.load(f)

    # garantir lista
    if isinstance(nomes, str):
        nomes = [nomes]

    # filtrar packages
    encontrados = [
        pkg for pkg in data["packages"]
        if pkg["name"] in nomes
    ]

    # estrutura final (opcional, mas recomendada)
    resultado = {
        "repo": data["repo"],
        "updated": data["updated"],
        "packages": encontrados
    }

    # guardar no ficheiro
    with open(ficheiro_saida, "w", encoding="utf-8") as f:
        json.dump(resultado, f, indent=2, ensure_ascii=False)