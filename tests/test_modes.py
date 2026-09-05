from modes import OverwriteRun
from modes import RenameRun
from modes import Run

import parse_config
import arguments

import pathlib
import pytest


def test_run(tmp_path: pathlib.Path):
    rules = {
        ".txt": tmp_path / "text",
    }
    ignore = {}
    config = parse_config.TestConfig(rules=rules, ignore=ignore)

    src_dir = tmp_path / "source"
    src_dir.mkdir()

    file1 = src_dir / "test1.txt"
    file2 = src_dir / "test2.pdf"
    file3 = src_dir / ".test3.txt"
    file4 = src_dir / "sub" / "test4.txt"

    file1.write_text("test")
    file2.write_text("test")
    file3.write_text("test")
    file4.parent.mkdir()
    file4.write_text("test")

    test_arguments = [str(src_dir)]

    arg_parser = arguments.Parser()
    args = arg_parser.parse_args(test_arguments)
    
    run = Run(config, args)
    run.run()

    right1 = rules[".txt"] / "test1.txt"

    assert file1.exists() == False
    assert right1.exists() == True
    assert file2.exists() == True
    assert file3.exists() == True
    assert file4.exists() == True

    file5 = src_dir / "test1.txt"
    file5.write_text("test2")

    run.run()

    assert file5.exists() == True
    assert right1.exists() == True
    assert right1.read_text() == "test"

    test2_arguments = [str(src_dir), "--all", "--recursive"]
    args2 = arg_parser.parse_args(test2_arguments)

    run2 = Run(config, args2)
    run2.run()

    right3 = rules[".txt"] / ".test3.txt"
    right4 = rules[".txt"] / "test4.txt"

    assert file3.exists() == False
    assert right3.exists() == True
    assert file4.exists() == False
    assert right4.exists() == True

def test_skip_run(tmp_path: pathlib.Path):
    rules = {
        ".txt": tmp_path / "text"
    }
    ignore = {}
    config = parse_config.TestConfig(rules=rules, ignore=ignore)

    src_dir = tmp_path / "source"
    src_dir.mkdir()

    file1 = src_dir / "test.txt"
    file2 = src_dir / "sub" / "test.txt"
    file3 = src_dir / "sub" / "sub" / "test.txt"
    file4 = src_dir / "sub" / "sub" / "sub" / "test.txt"

    file1.write_text("test1")
    file2.parent.mkdir()
    file2.write_text("test2")
    file3.parent.mkdir()
    file3.write_text("test3")
    file4.parent.mkdir()
    file4.write_text("test4")

    test_arguments = [str(src_dir), "--recursive"]

    arg_parser = arguments.Parser()
    args = arg_parser.parse_args(test_arguments)

    run = Run(config, args)
    run.run()

    assert file1.exists() == False
    assert file2.exists() == True 
    assert file3.exists() == True 
    assert file4.exists() == True 

    right1 = rules[".txt"] / "test.txt"
    assert right1.exists() == True
    assert right1.read_text() == "test1"

def test_rename_run(tmp_path):
    rules = {
        ".txt": tmp_path / "text"
    }
    ignore = {}
    config = parse_config.TestConfig(rules=rules, ignore=ignore)

    src_dir = tmp_path / "source"
    src_dir.mkdir()

    file1 = src_dir / "test.txt"
    file2 = src_dir / "sub" / "test.txt"
    file3 = src_dir / "sub" / "sub" / "test.txt"
    file4 = src_dir / "sub" / "sub" / "sub" / "test.txt"

    file1.write_text("test1")
    file2.parent.mkdir()
    file2.write_text("test2")
    file3.parent.mkdir()
    file3.write_text("test3")
    file4.parent.mkdir()
    file4.write_text("test4")

    test_arguments = [str(src_dir), "--recursive"]

    arg_parser = arguments.Parser()
    args = arg_parser.parse_args(test_arguments)

    run = RenameRun(config, args)
    run.run()

    right1 = rules[".txt"] / "test.txt"
    right2 = rules[".txt"] / "test_1.txt"
    right3 = rules[".txt"] / "test_2.txt"
    right4 = rules[".txt"] / "test_3.txt"

    assert file1.exists() == False
    assert file2.exists() == False
    assert file3.exists() == False
    assert file4.exists() == False
    
    assert right1.exists() == True
    assert right2.exists() == True
    assert right3.exists() == True
    assert right4.exists() == True

def test_overwrite_run(tmp_path):
    rules = {
        ".txt": tmp_path / "text"
    }
    ignore = {}
    config = parse_config.TestConfig(rules=rules, ignore=ignore)

    src_dir = tmp_path / "source"
    src_dir.mkdir()

    file1 = src_dir / "test.txt"
    file2 = src_dir / "sub" / "test.txt"
    file3 = src_dir / "sub" / "sub" / "test.txt"
    file4 = src_dir / "sub" / "sub" / "sub" / "test.txt"

    file1.write_text("test1")
    file2.parent.mkdir()
    file2.write_text("test2")
    file3.parent.mkdir()
    file3.write_text("test3")
    file4.parent.mkdir()
    file4.write_text("test4")

    test_arguments = [str(src_dir), "--recursive"]

    arg_parser = arguments.Parser()
    args = arg_parser.parse_args(test_arguments)

    run = OverwriteRun(config, args)
    run.run()

    assert file1.exists() == False
    assert file2.exists() == False
    assert file3.exists() == False
    assert file4.exists() == False

    right1 = rules[".txt"] / "test.txt"

    assert right1.exists() == True
    assert right1.read_text() == "test4"
