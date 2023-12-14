import pygit2
from datetime import datetime
import sys

geoff = 'geoff'

def pull(repo, remote_name='origin', branch='master'):
    for remote in repo.remotes:
        if remote.name == remote_name:
            remote.fetch()
            remote_master_id = repo.lookup_reference('refs/remotes/%s/%s' % (remote_name, branch)).target
            merge_result, _ = repo.merge_analysis(remote_master_id)
            # Up to date, do nothing
            if merge_result & pygit2.GIT_MERGE_ANALYSIS_UP_TO_DATE:
                print("up to date, returning")
                return
            # We can just fastforward
            elif merge_result & pygit2.GIT_MERGE_ANALYSIS_FASTFORWARD:
                print("fastforwarding")
                repo.checkout_tree(repo.get(remote_master_id))
                try:
                    master_ref = repo.lookup_reference('refs/heads/%s' % (branch))
                    master_ref.set_target(remote_master_id)
                except KeyError:
                    repo.create_branch(branch, repo.get(remote_master_id))
                repo.head.set_target(remote_master_id)
            elif merge_result & pygit2.GIT_MERGE_ANALYSIS_NORMAL:
                print("trying to merge")
                repo.merge(remote_master_id)

                if repo.index.conflicts is not None:
                    for conflict in repo.index.conflicts:
                        print('Conflicts found in:', conflict[0].path)
                    raise AssertionError('Conflicts, ahhhhh!!')

                user = repo.default_signature
                tree = repo.index.write_tree()
                commit = repo.create_commit('HEAD',
                                            user,
                                            user,
                                            'Merge!',
                                            tree,
                                            [repo.head.target, remote_master_id])
                # We need to do this or git CLI will think we are still merging.
                repo.state_cleanup()
            else:
                raise AssertionError('Unknown merge analysis result')

pygit2.option(pygit2.GIT_OPT_SET_OWNER_VALIDATION, 0)
repo = pygit2.Repository(str(sys.argv[1]))
ident = pygit2.Signature('comfyui', 'comfy@ui')
try:
    print("stashing current changes")
    repo.stash(ident)
except KeyError:
    print("nothing to stash")
backup_branch_name = 'backup_branch_{}'.format(datetime.today().strftime('%Y-%m-%d_%H_%M_%S'))
print("creating backup branch: {}".format(backup_branch_name))
repo.branches.local.create(backup_branch_name, repo.head.peel())

print("checking whether geoff is already in remotes '", repo.remotes.names, "'")
if not geoff in repo.remotes.names():
  print("need to add geoff's remote repo")
  repo.remotes.create(geoff, 'https://github.com/gmatters/ComfyUI.git')

print("checking out master branch")
branch = repo.lookup_branch('master')
ref = repo.lookup_reference(branch.name)
repo.checkout(ref)

print("pulling geoff master")
pull(repo, remote_name=geoff, branch='master')

print("Done!")

