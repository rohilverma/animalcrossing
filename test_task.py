from unittest import TestCase, main
from threads_vs_processes import task

# Tiny UT class to explore functionality
class TestTask(TestCase):

    def test1(self):
        resp = task()
        self.assertEqual(resp, None)

    def test2(self):
        self.assertEqual("foo".upper(), "FOO")

if __name__ == "__main__":
    main()
