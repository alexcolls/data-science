from nbresult import ChallengeResultTestCase

class TestFullPipeline(ChallengeResultTestCase):
    def test_score_scaling(self):
        score = self.result.score_scaled
        self.assertGreaterEqual(score, .74)
        
    def test_score_balancing(self):
        score = self.result.score_balanced
        self.assertGreaterEqual(score, .78)
        
    def test_score_fine_tuned(self):
        score = self.result.score_tuned
        self.assertGreaterEqual(score, .8)
        