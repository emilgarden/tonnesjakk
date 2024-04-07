class TønnesjakkController:
    def __init__(self, spillbrett, view):
        self.spillbrett = spillbrett
        self.view = view

    def håndter_input(self, spiller_id):
        while True:
            valg = input(f"Spiller {spiller_id}, velg en handling ([i]ntroduser, [f]lytt, [p]lasser, [v]is, [q]avslutt): ").lower()
            if valg == 'i':
                self.introduser_brikke(spiller_id)
            elif valg == 'f':
                self.flytt_brikke(spiller_id)
            elif valg == 'p':
                self.plasser_melkespann(spiller_id)
            elif valg == 'v':
                self.view.vis_spillbrett(self.spillbrett.spillbrett)
            elif valg == 'q':
                print("Avslutter spillet.")
                break
            else:
                print("Ugyldig valg, prøv igjen.")

    def introduser_brikke(self, spiller_id):
        kolonne = int(input("Velg kolonne (0-5) for å introdusere brikke: "))
        if self.spillbrett.introduser_brikke(spiller_id, kolonne):
            print("Brikke introdusert.")
        else:
            print("Kunne ikke introdusere brikke. Prøv igjen.")

    def flytt_brikke(self, spiller_id):
        fra_posisjon = tuple(map(int, input("Fra posisjon (rad,kolonne): ").split(',')))
        til_posisjon = tuple(map(int, input("Til posisjon (rad,kolonne): ").split(',')))
        if self.spillbrett.flytt_tonne(spiller_id, fra_posisjon, [til_posisjon]):
            print("Brikke flyttet.")
        else:
            print("Kunne ikke flytte brikke. Prøv igjen.")

    def plasser_melkespann(self, spiller_id):
        posisjon = tuple(map(int, input("Posisjon for melkespann (rad,kolonne): ").split(',')))
        if self.spillbrett.plasser_melkespann(spiller_id, posisjon):
            print("Melkespann plassert.")
        else:
            print("Kunne ikke plassere melkespann. Prøv igjen.")
