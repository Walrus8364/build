"""Resolve acceptance vs release before any registry mutation; run inside the private source clone."""
import os
from pathlib import Path
import re
import subprocess


def git(*args):
    return subprocess.check_output(['git', *args], text=True).strip()


def source_commit(ref):
    """A clone has origin/* for non-default branches; fetch the explicitly requested ref."""
    if ref.startswith('-') or any(c.isspace() for c in ref):
        raise ValueError('source_ref must be a single Git ref or commit.')
    git('fetch', '--no-tags', 'origin', ref)
    return git('rev-parse', '--verify', '--end-of-options', 'FETCH_HEAD^{commit}')


def resolve(event, ref, tag, trigger):
    if event == 'workflow_dispatch':
        if tag.startswith('v'):
            sha = git('rev-parse', '--verify', '--end-of-options', f'refs/tags/{tag}^{{commit}}')
            if ref and source_commit(ref) != sha:
                raise ValueError('Release source_ref must equal the exact release tag commit.')
        else:
            if not ref:
                raise ValueError('Acceptance requires an explicit source_ref.')
            sha = source_commit(ref)
            tag = tag or f'acceptance-{sha[:12]}'
    else:
        sha = git('rev-parse', '--verify', '--end-of-options', f'{Path(trigger).read_text().strip()}^{{commit}}')
        tags = [t for t in git('tag', '--points-at', sha, '--sort=-v:refname').splitlines() if t.startswith('v')]
        if not tags:
            raise ValueError('Triggered commit has no exact v* tag.')
        tag = tags[0]
    if not re.fullmatch(r'(v|acceptance-)[A-Za-z0-9_][A-Za-z0-9_.-]{0,115}', tag):
        raise ValueError('Invalid release or acceptance image tag.')
    return sha, tag, tag.startswith('v')


if __name__ == '__main__':
    sha, tag, release = resolve(os.environ['EVENT_NAME'], os.getenv('SOURCE_REF', ''),
                                os.getenv('MANUAL_TAG', ''), os.environ['TRIGGER_FILE'])
    subprocess.run(['git', 'checkout', '--detach', sha], check=True)
    with open(os.environ['GITHUB_OUTPUT'], 'a') as output:
        output.write(f'sha={sha}\ntag={tag}\nrelease={str(release).lower()}\n')
