from typing import Tuple
import unittest
from pathlib import Path
import tempfile
import shutil


class TestFindSrc(unittest.TestCase):

    # TODO - THIS METHOD SHOULD BE IN DS-COMMON
    @staticmethod
    def __find_src(current_path: Path) -> Tuple[Path, str]:
        """Will cycle up the current path until it finds the directory that 
        meets all sub-directories in DIRECTORY_CONSTANTS.
        
        Will return the 'src' directory as a Path object."""
        
        DIRECTORY_CONSTANTS = ["src", "notebooks", "tests"]

        # to print the path
        tree = [list(current_path.parts)[-1]]

        for parent in current_path.parents:
            tree.insert(0, list(parent.parts)[-1])
            condition = all((parent / subdir).exists() for subdir in DIRECTORY_CONSTANTS)
            if condition:
                tree_str = '.' 
                for i, subdir in enumerate(tree):
                    tree_str += ('\n' + '    '*i + f'└── {subdir}')

                return parent / "src", tree_str
        raise FileNotFoundError("Could not find the 'src' directory in the expected structure.")

    def setUp(self):
        # Create a temporary directory structure
        self.temp_dir = tempfile.mkdtemp()
        self.project_root = Path(self.temp_dir) / "project"
        self.project_root.mkdir()

        # Create required subdirectories
        for subdir in ["src", "notebooks", "tests", "data", "reports"]:
            (self.project_root / subdir).mkdir()
        
        # Simulate being in a subdirectory of notebooks
        self.current_path = self.project_root / "notebooks" / "deep"
        self.current_path.mkdir(parents=True)

        self.deeper_path = self.project_root / "notebooks" / "deep" / "deeper" / "deepest"
        self.deeper_path.mkdir(parents=True)

    def tearDown(self):
        # Clean up the temporary directory after test
        shutil.rmtree(self.temp_dir)

    def test_find_src_success(self):
        result, _ = self.__find_src(self.current_path)
        expected = self.project_root / "src"
        self.assertEqual(result, expected)

        result_deeper, _ = self.__find_src(self.deeper_path)
        self.assertEqual(result_deeper, expected)

    def test_find_src_str(self):
        _, tree_str = self.__find_src(self.current_path)
        expected = """.
└── project
    └── notebooks
        └── deep"""
        self.assertEqual(expected, tree_str)
        

        _, tree_str_deeper = self.__find_src(self.deeper_path)
        expected = """.
└── project
    └── notebooks
        └── deep
            └── deeper
                └── deepest"""
        self.assertEqual(expected, tree_str_deeper)
        


    def test_find_src_failure(self):
        # Create a completely unrelated structure
        isolated_path = Path(self.temp_dir) / "unrelated" / "nested"
        isolated_path.mkdir(parents=True)

        with self.assertRaises(FileNotFoundError):
            self.__find_src(isolated_path)

