import unittest
from operations.reviewing import ProposalManager

class TestProposalManager(unittest.TestCase):

    program_content = None

    def setUp(self) -> None:
        with open('./cocktail_sort.py', 'r') as file:
            program_content = file.read()
        self.program_content = program_content

    def tearDown(self) -> None:
        self.program_content = None

    def test_find_and_replace(self):

        proposal_manager = ProposalManager(
            file_name='cocktail_sort_review.py',
            original_file=self.program_content
        )

        with open('proposal.txt', 'r') as file:
            accepted_proposals = [file.read()]

            len(accepted_proposals)

        proposal_manager.accepted_proposals = accepted_proposals 
        proposal_manager.apply_changes()
        proposal_manager.write_file()

        #self.assertCountEqual(expected, actual)

def test_suite():
    """Testing suite

    Notes
    -----
    Order of the tests is important. Can be altered if dependencies
    are respected.

    """

    suite = unittest.TestSuite()
    suite.addTest(TestProposalManager('test_find_and_replace'))

    return suite


if __name__ == '__main__':

    runner = unittest.TextTestRunner()
    runner.run(test_suite())