class SpillbrettView:
    def vis_spillbrett(self, spillbrett):
        symboler = {0: '.', 1: 'T1', 2: 'M1', 3: 'T2', 4: 'M2'}
        print("\nSpillbrett:")
        for rad in spillbrett:
            print(' '.join(symboler[celle] for celle in rad))

    def vis_melding(self, melding):
        print(melding)
    
    def vis_vinner(self, spiller_id):
        print(f"\nGratulerer! {spiller_id} har vunnet spillet!")
