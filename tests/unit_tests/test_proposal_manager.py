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

        proposal_manager.accepted_proposals = [
            '<find:>\ndef cocktailSort(a):\n<replace:>\ndef cocktailSort(a: List[int]) -> None:\n<message:>\nTo print each element of a list on a new line, we can use the \'join()\' function. It\'s more efficient than looping through the list and printing each element individually. Also, using \'map()\' function to convert elements of list to string is a cleaner approach.' 
        ]

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