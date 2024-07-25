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
            '<find:>\ndef cocktailSort(a):\n<replace:>\ndef cocktail_sort(a: list) -> None:\n<find:>\na = [5, 1, 4, 2, 8, 0, 2]\ncocktailSort(a)\nprint("Sorted array is:")\nfor i in range(len(a)):\n    print("% d" % a[i])\n<replace:>\na = [5, 1, 4, 2, 8, 0, 2]\ncocktail_sort(a)\nprint("Sorted array is:", a)\n<message:>\nI\'ve made a few changes to your code. First, I\'ve renamed the function to `cocktail_sort` to follow Python\'s naming conventions. I\'ve also added a type hint to the function signature to indicate that it modifies the input list in-place and doesn\'t return anything. Finally, I\'ve simplified the printing of the sorted array. Instead of looping through the array and printing each element individually, you can just print the entire array at once.', '<find:>\nwhile (swapped == True):\n<replace:>\nwhile swapped:\n<find:>\nif (swapped == False):\n    break\n<replace:>\nif not swapped:\n    break\n<find:>\nif (a[i] > a[i + 1]):\n<replace:>\nif a[i] > a[i + 1]:\n<find:>\nstart = start + 1\n<replace:>\nstart += 1\n<message:>\nI've made a few changes to make your code more Pythonic. \n\n1. In Python, you don't need to compare a boolean to `True` or `False` directly. You can use the boolean itself as the condition in an `if` statement or a `while` loop.\n\n2. For incrementing or decrementing a variable, you can use the `+=` or `-=` operators, which are more concise and easier to read.\n\n3. Removed unnecessary parentheses around conditions in `if` statements. In Python, parentheses are not required around conditions in `if` statements unless they are used for grouping.']
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