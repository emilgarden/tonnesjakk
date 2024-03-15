import unittest
from src.game.model import Spillbrett


class TestSpillbrett(unittest.TestCase):

    def setUp(self):
        """Opprett en ny spillbrett-instans for hver test"""
        self.spill = Spillbrett()

    def test_introduser_brikke(self):
        """Test at en brikke kan introduseres korrekt"""
        self.assertTrue(self.spill.introduser_brikke('spiller1', 0))
        # Sjekk at brikken faktisk er plassert på brettet
        self.assertEqual(self.spill.spillbrett[0][0], 1)

    def test_flytt_tonne(self):
        """Test at en brikke kan flyttes korrekt"""
        self.spill.introduser_brikke('spiller1', 0)  # Forutsetter at dette fungerer som forventet
        self.assertTrue(self.spill.flytt_tonne('spiller1', (0, 0), (0, 1)))
        # Sjekk at brikken har blitt flyttet
        self.assertEqual(self.spill.spillbrett[0][1], 1)
        self.assertEqual(self.spill.spillbrett[0][0], 0)

    def test_sjekk_vinner(self):
        """Test at vinnerdeteksjon fungerer"""
        self.spill.spiller_brikker['spiller1'] = [(5, i) for i in range(4)]  # Plasserer alle spiller1 sine brikker på motsatt side
        self.spill.oppdater_spillbrett()  # Oppdater spillbrettet basert på endringene
        vinner = self.spill.sjekk_vinner()
        self.assertEqual(vinner, 'spiller1')

if __name__ == '__main__':
    unittest.main()
