class Spillbrett:
    def __init__(self):
        self.brett_storrelse = 6
        self.spillbrett = [[0 for _ in range(self.brett_storrelse)] for _ in range(self.brett_storrelse)]
        self.spiller_brikker = {'spiller1': [-1, -1, -1, -1], 'spiller2': [-1, -1, -1, -1]}  # Brikker som venter på å bli introdusert
        self.melkespann_posisjoner = {'spiller1': None, 'spiller2': None}
        self.oppdater_spillbrett()

    def oppdater_spillbrett(self):
        # Nullstill spillbrettet
        for rad in range(self.brett_storrelse):
            for kol in range(self.brett_storrelse):
                self.spillbrett[rad][kol] = 0
                
        # Oppdater med spillerbrikker
        for spiller_id, brikker in self.spiller_brikker.items():
            for brikke in brikker:
                if brikke != -1:
                    rad, kol = brikke
                    self.spillbrett[rad][kol] = 1  # Eller bruk forskjellige tall for å skille mellom spillere

        # Oppdater med melkespann
        for posisjon in self.melkespann_posisjoner.values():
            if posisjon is not None:
                rad, kol = posisjon
                self.spillbrett[rad][kol] = 2

    def introduser_brikke(self, spiller_id, kolonne):
        if spiller_id not in self.spiller_brikker:
            print(f"Ugyldig spiller_id: {spiller_id}")
            return False

        # Bestem start rad basert på spiller_id
        start_rad = 0 if spiller_id == 'spiller1' else self.brett_storrelse - 1

        # Sjekk om kolonnen er gyldig og om det er plass til å introdusere en ny brikke
        if 0 <= kolonne < self.brett_storrelse and self.spillbrett[start_rad][kolonne] == 0:
            # Finn første tilgjengelige brikke som venter på å bli introdusert
            for i, brikke_status in enumerate(self.spiller_brikker[spiller_id]):
                if brikke_status == -1:  # Brikken venter på å bli introdusert
                    self.spiller_brikker[spiller_id][i] = (start_rad, kolonne)  # Oppdaterer brikken til å være på brettet
                    self.spillbrett[start_rad][kolonne] = 1  # Eller en annen representasjon av spillerens brikke
                    self.oppdater_spillbrett() # Oppdaterer spillbrettet
                    return True
            print("Alle brikker er allerede introdusert.")
        else:
            print(f"Kolonnen {kolonne} er full eller ugyldig.")
        return False

    def flytt_tonne(self, spiller_id, fra_posisjon, til_posisjon):
        if spiller_id not in self.spiller_brikker:
            print(f"Ugyldig spiller_id: {spiller_id}")
            return False

        fra_rad, fra_kol = fra_posisjon
        til_rad, til_kol = til_posisjon

        # Sjekk om startposisjonen inneholder spillerens brikke
        if (fra_rad, fra_kol) not in self.spiller_brikker[spiller_id]:
            print("Det er ingen av dine brikker på startposisjonen.")
            return False

        # Sjekk at målposisjonen er innenfor brettet
        if not (0 <= til_rad < self.brett_storrelse and 0 <= til_kol < self.brett_storrelse):
            print("Målposisjonen er utenfor brettet.")
            return False

        # Beregn bevegelsesvektoren
        delta_rad = til_rad - fra_rad
        delta_kol = til_kol - fra_kol

        # Sjekk at bevegelsen er gyldig (ett felt i hvilken som helst retning, eller hopping over en brikke)
        if abs(delta_rad) > 1 or abs(delta_kol) > 1:
            print("Du kan kun flytte en brikke ett felt om gangen, eller hoppe over en brikke.")
            return False

        # Sjekk at målposisjonen er ledig (eller at det er et gyldig hopp)
        if self.spillbrett[til_rad][til_kol] != 0 and (abs(delta_rad) != 1 or abs(delta_kol) != 1):
            print("Målposisjonen er opptatt.")
            return False

        # Utfør bevegelsen
        self.spillbrett[fra_rad][fra_kol] = 0
        self.spillbrett[til_rad][til_kol] = 1  # Eller en annen representasjon av spillerens brikke
        self.spiller_brikker[spiller_id][self.spiller_brikker[spiller_id].index((fra_rad, fra_kol))] = (til_rad, til_kol)
        self.oppdater_spillbrett() # Oppdaterer spillbrettet

        return True


    def plasser_melkespann(self, spiller_id, posisjon):
        if spiller_id not in self.spiller_brikker:
            print(f"Ugyldig spiller_id: {spiller_id}")
            return False

        rad, kol = posisjon

        # Sjekk at posisjonen er innenfor brettet
        if not (0 <= rad < self.brett_storrelse and 0 <= kol < self.brett_storrelse):
            print("Posisjonen er utenfor brettet.")
            return False

        # Sjekk at posisjonen er ledig
        if self.spillbrett[rad][kol] != 0:
            print("Posisjonen er allerede opptatt.")
            return False

        # Sjekk at spilleren ikke allerede har plassert melkespannet
        if self.melkespann_posisjoner[spiller_id] is not None:
            print(f"{spiller_id} har allerede plassert sitt melkespann.")
            return False

        # Plasser melkespannet og oppdater spillbrettet og melkespann_posisjoner
        self.spillbrett[rad][kol] = 2  # Anta at 2 representerer et melkespann
        self.melkespann_posisjoner[spiller_id] = posisjon
        self.oppdater_spillbrett() #Oppdaterer spillbrettet

        return True


    def sjekk_gyldig_trekk(self, fra_posisjon, til_posisjon):
        fra_rad, fra_kol = fra_posisjon
        til_rad, til_kol = til_posisjon

        # Sjekk at begge posisjonene er innenfor brettet
        if not (0 <= fra_rad < self.brett_storrelse and 0 <= fra_kol < self.brett_storrelse):
            return False, "Startposisjonen er utenfor brettet."
        if not (0 <= til_rad < self.brett_storrelse and 0 <= til_kol < self.brett_storrelse):
            return False, "Sluttposisjonen er utenfor brettet."

        # Sjekk at målposisjonen ikke er opptatt av et melkespann
        for spiller_id, posisjon in self.melkespann_posisjoner.items():
            if posisjon == til_posisjon:
                return False, "Målposisjonen er blokkert av et melkespann."

        # Beregn bevegelsesvektoren
        delta_rad = til_rad - fra_rad
        delta_kol = til_kol - fra_kol

        # Sjekk at bevegelsen er innenfor ett felt i alle retninger eller et gyldig hopp
        if abs(delta_rad) > 1 or abs(delta_kol) > 1:
            # For hopp, sjekk at det er over en annen brikke
            if abs(delta_rad) != 2 and abs(delta_kol) != 2:
                return False, "Ugyldig trekk, kan kun bevege ett felt eller hoppe over en brikke."
            midt_rad = fra_rad + delta_rad // 2
            midt_kol = fra_kol + delta_kol // 2
            if self.spillbrett[midt_rad][midt_kol] == 0:
                return False, "Ingen brikke å hoppe over."

        # Sjekk at målposisjonen er ledig
        if self.spillbrett[til_rad][til_kol] != 0:
            return False, "Målposisjonen er allerede opptatt."

        return True, "Trekket er gyldig."


    def sjekk_vinner(self):
        # Sjekk for spiller1
        spiller1_vunnet = all(brikke[0] == self.brett_storrelse - 1 for brikke in self.spiller_brikker['spiller1'] if brikke != -1)
        if spiller1_vunnet:
            return 'spiller1'

        # Sjekk for spiller2
        spiller2_vunnet = all(brikke[0] == 0 for brikke in self.spiller_brikker['spiller2'] if brikke != -1)
        if spiller2_vunnet:
            return 'spiller2'

        # Hvis ingen har vunnet enda
        return None


    def vis_spillbrett(self):
        symboler = {0: '.', 1: 'T', 2: 'M'}  # Anta at '.' representerer tomme celler, 'T' for tønner, og 'M' for melkespann
        
        # Oppdaterer først spillbrettet basert på spiller_brikker og melkespann_posisjoner
        for rad in range(self.brett_storrelse):
            for kol in range(self.brett_storrelse):
                self.spillbrett[rad][kol] = 0  # Setter alle celler til tomme først
        
        for spiller_id, brikker in self.spiller_brikker.items():
            for brikke in brikker:
                if brikke != -1:  # Hvis brikken er introdusert på brettet
                    rad, kol = brikke
                    self.spillbrett[rad][kol] = 1  # Markerer posisjonen som en tønne

        for posisjon in self.melkespann_posisjoner.values():
            if posisjon is not None:
                rad, kol = posisjon
                self.spillbrett[rad][kol] = 2  # Markerer posisjonen som et melkespann
        
        # Printer spillbrettet
        print("Spillbrett:")
        for rad in self.spillbrett:
            for celle in rad:
                print(symboler[celle], end=' ')
            print()  # Ny linje etter hver rad

