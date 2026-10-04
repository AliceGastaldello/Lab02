def carica_da_file(file_path):
    """Carica le foto dal file, creando un nuovo anno ogni volta che compare per la prima volta"""
    try:
        f = open(file_path, "r", encoding="utf-8")
    except FileNotFoundError:
        print("File non trovato. Riprova.")
        return None

    f.readline()  # Salta l'intestazione CSV
    album = {}

    for line in f:
        line = line.strip()
        if not line:
            continue
        campo = line.split(",")
        foto = {
            "codice": campo[0].strip(),
            "titolo": campo[1].strip(),
            "autore": campo[2].strip(),
            "mese": int(campo[3].strip()),
            "anno": int(campo[4].strip())
        }

        anno = foto["anno"]
        if anno not in album:
            album[anno] = []
        album[anno].append(foto)

    f.close()
    return album


def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):
    """Aggiunge una foto all'album, creando l'anno al volo se non è ancora presente"""
    try:
        f = open(file_path, "a", encoding="utf-8")
        f.write(f"{codice},{titolo},{autore},{mese},{anno}\n")
        f.close()
    except FileNotFoundError:
        return None

    nuova_foto = {
        "codice": codice,
        "titolo": titolo,
        "autore": autore,
        "mese": mese,
        "anno": anno
    }

    if anno not in album:
        album[anno] = []
    album[anno].append(nuova_foto)

    return nuova_foto


def cerca_foto(album, codice):
    for anno in album:
        for foto in album[anno]:
            if foto["codice"] == codice:
                return f'{foto["codice"]}, {foto["titolo"]}, {foto["autore"]}, {foto["mese"]}, {foto["anno"]}'
    return None

def elenco_foto_anno_per_titolo(album, anno):
    if anno not in album:
        return None
    titoli=[]
    for foto in album[anno]:
        titoli.append(foto["titolo"])

    titoli.sort()
    return titoli


def main():
    album = {}  # L'album è un dizionario (anno -> lista di foto)
    file_path = "album_fotografico.csv"

    while True:
        print("\n--- MENU ALBUM FOTOGRAFICO ---")
        print("1. Carica album da file")
        print("2. Aggiungi una nuova foto")
        print("3. Cerca una foto per codice")
        print("4. Elenco foto di un anno (ordinato per titolo)")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                risultato = carica_da_file(file_path)
                if risultato is not None:
                    album = risultato
                    print("Album caricato con successo!")
                    break

        elif scelta == "2":
            if not album and album != {}:
                print("Prima carica l'album da file.")
                continue

            codice = input("Codice della foto: ").strip()
            titolo = input("Titolo: ").strip()
            autore = input("Autore: ").strip()
            try:
                mese = int(input("Mese (1-12): ").strip())
                anno = int(input("Anno: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per mese e anno.")
                continue

            foto = aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path)
            if foto:
                print(f"Foto aggiunta con successo!")
            else:
                print("Non è stato possibile aggiungere la foto.")

        elif scelta == "3":
            if not album:
                print("L'album è vuoto.")
                continue

            codice = input("Inserisci il codice della foto da cercare: ").strip()
            risultato = cerca_foto(album, codice)
            if risultato:
                print(f"Foto trovata: {risultato}")
            else:
                print("Foto non trovata.")

        elif scelta == "4":
            if not album:
                print("L'album è vuoto.")
                continue

            try:
                anno = int(input("Inserisci l'anno da consultare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_foto_anno_per_titolo(album, anno)
            if titoli is not None:
                print(f'\nFoto del {anno}:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))
            else:
                print(f"Nessuna foto trovata per l'anno {anno}.")

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()