import pathlib
import subprocess


def execute_git_command(path, command):
    is_repo = pathlib.Path(path + '/.git').is_dir()
    if not is_repo:
        print('Not a git repository')
        return []
    bash_command = 'git -C ' + path + ' ' + command
    output, error = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE).communicate()
    if not error:
        output = output.decode('utf-8')
        return output.splitlines()
    else:
        print('Not a git command')
        return []


def read_git_file(path, sha1_file):
    return execute_git_command(path, 'cat-file -p ' + sha1_file)


def get_git_references(path):
    references = [line.split() for line in execute_git_command(path, 'for-each-ref')]
    lbr = 'refs/heads/'
    local_branches = [(ref[2][len(lbr):], ref[0]) for ref in references if ref[2].startswith(lbr)]
    rbr = 'refs/remotes/'
    remotes = [(ref[2][len(rbr):], ref[0]) for ref in references if ref[2].startswith(rbr)]
    tr = 'refs/tags/'
    tags = [(ref[2][len(tr):], ref[0]) for ref in references if ref[2].startswith(tr)]
    return local_branches, remotes, tags


def get_git_objects(path):
    objects = [line.split() for line in execute_git_command(path, 'cat-file --batch-check --batch-all-objects')]
    blobs = [obj[0] for obj in objects if obj[1] == 'blob']
    trees = [obj[0] for obj in objects if obj[1] == 'tree']
    commits = [obj[0] for obj in objects if obj[1] == 'commit']
    annotated_tags = [obj[0] for obj in objects if obj[1] == 'tag']
    return blobs, trees, commits, annotated_tags


def get_git_heads(path):
    lines = execute_git_command(path, 'branch -avv --abbrev=0')
    heads = [line for line in lines if line.startswith('* ')]
    return heads
