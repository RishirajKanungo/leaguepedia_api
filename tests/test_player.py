import unittest
from unittest.mock import Mock, patch
import sys
sys.path.insert(0, '/Users/rishirajkanungo/Documents/GitHub/leaguepedia_api/') # add path to import a player
# from ..scripts.Player import Player
from scripts.Player import Player
MockPlayer = Mock()
MockPlayer.getName.return_value = 'Doublelift'
MockPlayer.getTeam.return_value = '100 Thieves'
MockPlayer.getDateJoined.return_value = ''
MockPlayer.getRoles.return_value = 'ADC'
MockPlayer.getRole.return_value = 'ADC'
MockPlayer.getKillsInSplit.return_value = 104
MockPlayer.getDeathsInSplit.return_value = 0
MockPlayer.getAssistsInSplit.return_value = 0
MockPlayer.getKDAInSplit.return_value = 4.5
MockPlayer.getCSPM.return_value = 10
MockPlayer.getChampsPlayed.return_value = 7
MockPlayer.getWinRate.return_value = '60%'
MockPlayer.getDPM.return_value = 712.3
MockPlayer.getGoldPerMinute.return_value = 455
MockPlayer.getGoldPercentage.return_value = 25.4
MockPlayer.getRecord.return_value = '12W - 8L'


class TestPlayer(unittest.TestCase):
    
    # def testRecord(self):
    #     player = Player('Doublelift')
    #     self.assertEqual(player.getName(), 'Doublelift')
    #     self.assertEqual(player.getTeam(), '')
    #     self.assertEqual(player.getDateJoined(), '')
    #     self.assertEqual(player.getRoles(), '')
    #     self.assertEqual(player.getRole(), '')
    
    # def testWinRate(self):
    #     player = Player('Doublelift')
    #     self.assertEqual(player.getWinRate('LCS 2023 Summer'), 0.0)
    
    def testKDA(self):
        print('hi')
    #     player = Player('Doublelift')
    
    