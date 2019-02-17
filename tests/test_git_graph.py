import os
import subprocess

import git_graph.dot_graph as dg

author = "Bernard"
email = "author@cie.com"
action_date = "Sat Oct 15 11:00 2011 +0100"
os.environ["GIT_AUTHOR_NAME"] = author
os.environ["GIT_COMMITTER_NAME"] = author
os.environ["GIT_AUTHOR_EMAIL"] = email
os.environ["GIT_COMMITTER_EMAIL"] = email
os.environ["GIT_AUTHOR_DATE"] = action_date
os.environ["GIT_COMMITTER_DATE"] = action_date


def execute_bash_command(path, command):
    output, error = subprocess.Popen(command.split(), cwd=str(path), stdout=subprocess.PIPE).communicate()
    if not error:
        return output


def test_full_repo(tmp_path):
    dir1 = tmp_path / 'dir1'
    dir1.mkdir()
    file1 = dir1 / 'file1.txt'
    file1.write_text('content file1.txt v1')
    assert len(list(tmp_path.iterdir())) == 1
    assert file1.is_file()
    assert file1.read_text() == 'content file1.txt v1'

    file2 = tmp_path / 'file2.txt'
    file2.write_text('content file2.txt v1')
    assert len(list(tmp_path.iterdir())) == 2
    assert file2.is_file()
    assert file2.read_text() == 'content file2.txt v1'

    execute_bash_command(tmp_path, 'git init')
    assert len(list(tmp_path.iterdir())) == 3
    assert (tmp_path / '.git').is_dir()

    execute_bash_command(tmp_path, 'git add -A')
    execute_bash_command(tmp_path, 'git commit -m commit1')

    dg.DotGraph(str(tmp_path)).persist()

    assert len(list(tmp_path.iterdir())) == 4
    assert (tmp_path / '.gitGraph').is_dir()
    assert len(list((tmp_path / '.gitGraph').iterdir())) == 2

    dot_file_path = list((tmp_path / '.gitGraph').glob('*.dot'))[0]
    with open(dot_file_path) as dot_file:
        dot_graph = dot_file.readlines()
        dot_graph[3:-1] = sorted(dot_graph[3:-1])
        assert ''.join(dot_graph) == golden_dot_graph


golden_dot_graph = """digraph auto {
	graph [bgcolor=transparent]
	node [fixedsize=true style=filled width=0.95]
	"54378aec6a6ea34638ac687217745e574360285e" [label="54378ae" fillcolor="#9ccc66"]
	"6e414aa7e6b2bb6f8bd9fcc652ecd7a349547f92" -> "54378aec6a6ea34638ac687217745e574360285e"
	"6e414aa7e6b2bb6f8bd9fcc652ecd7a349547f92" [label="6e414aa" fillcolor="#bc9b8f"]
	"737c972823aec2a30e726cd39821edf8d4b4826b" -> "6e414aa7e6b2bb6f8bd9fcc652ecd7a349547f92"
	"737c972823aec2a30e726cd39821edf8d4b4826b" -> ecf7586c0df1003ea0a3efa5a00dc3ceaac570f8
	"737c972823aec2a30e726cd39821edf8d4b4826b" [label="737c972" fillcolor="#bc9b8f"]
	HEAD -> master
	HEAD [label=HEAD fillcolor="#e6ccff"]
	e53574e083bfb447086df95ad1214d87b6ae45c4 -> "737c972823aec2a30e726cd39821edf8d4b4826b"
	e53574e083bfb447086df95ad1214d87b6ae45c4 [label=e53574e fillcolor="#85d5fa"]
	ecf7586c0df1003ea0a3efa5a00dc3ceaac570f8 [label=ecf7586 fillcolor="#9ccc66"]
	master -> e53574e083bfb447086df95ad1214d87b6ae45c4
	master [label=master fillcolor="#9999ff"]
}
"""
