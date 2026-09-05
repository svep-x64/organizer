from transfer import iter_files
from transfer import destination

import pathlib


def test_destination():
    rules = {
            ".txt": "/tmp/test"
    }

    test1 = pathlib.Path("/tmp/test/1/one.txt")
    assert destination(test1, rules) == pathlib.Path("/tmp/test/one.txt")

    test2 = pathlib.Path("/tmp/test/2/two.pdf")
    assert destination(test2, rules) == None

def test_iter(tmp_path):
    file1 = tmp_path / "test1.txt"
    file2 = tmp_path / ".test2.txt"
    file3 = tmp_path / "sub" / "test3.txt"
    file4 = tmp_path / "test4.txt"

    file1.write_text("test")
    file2.write_text("test")
    file3.parent.mkdir()
    file3.write_text("test")
    file4.write_text("test")

    iter1 = iter_files(tmp_path)
    test1 = {file for file in iter1}
    right1 = {file1, file4}

    assert test1 == right1

    iter2 = iter_files(tmp_path, all=True)
    test2 = {file for file in iter2}
    right2 = {file1, file2, file4}

    assert test2 == right2

    iter3 = iter_files(tmp_path, recursive=True)
    test3 = {file for file in iter3}
    right3 = {file1, file3, file4}

    assert test3 == right3
