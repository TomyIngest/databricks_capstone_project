- [🟡 Git ](#-git-)
  - [Creating a repository](#creating-a-repository)
  - [Checking commands](#checking-commands)
  - [Comparing changes](#comparing-changes)
  - [Staging and committing workflow](#staging-and-committing-workflow)
  - [Undoing changes \& Time travelling](#undoing-changes--time-travelling)
  - [Stashing](#stashing)
  - [Branching](#branching)
  - [Merging](#merging)
    - [Merging scenarios](#merging-scenarios)
  - [Git configuration](#git-configuration)
  - [Hidden files \& folders](#hidden-files--folders)
- [🟡 GitHub ](#-github-)
  - [Connections terminology](#connections-terminology)
  - [Remote connections](#remote-connections)
  - [Fetching \& pulling](#fetching--pulling)

<br><br>

# 🟡 Git <br>

<br>

## Creating a repository

| Command | What it does |
| --- | --- |
| `git init` | Turns the current folder into a new, empty Git repository: it creates a hidden `.git` folder where Git stores the full history, branches and config. Files already in the folder are **not** tracked yet. You still have to `git add` and `git commit` them. Run it once, in the project's root folder. `git init <folder>` creates the folder and initializes it in one step. |
| `git clone <url>` | Downloads an existing repository (e.g. from GitHub) to your PC with its full history, into a new folder named after the repo. The link back to the source is saved as the remote `origin`, so `git pull` / `git push` work right away. E.g. `git clone https://github.com/user/repo.git`. `git clone <url> <folder>` clones into a folder name you choose. Use `git clone <url> .` to clone into the current (empty) folder. |

<br>

## Checking commands

| Command | What it does |
| --- | --- |
| `git status` | Shows the current state of the working tree: which branch you're on, which files are modified, which are staged (ready to commit) and which are untracked (new files Git doesn't follow yet). Changes nothing, so it's always safe to run. Run it before `git add` / `git commit` to see what will go in. |
| `git log` | Shows the commit history of the current branch, newest first. Each entry lists the commit hash (unique ID), author, date and commit message. Long output opens in a pager: scroll with the arrow keys or `Space`, quit with `q`. |
| `git log --oneline` | Short version of `git log`: one commit per line, with the shortened hash and the message only. Handy for a quick overview of the history or for copying a commit hash. |
| `git branch` | Lists the local branches. The current branch is marked with `*`. `git branch <name>` creates a new branch, but doesn't switch to it. |
| `git branch -a` | Lists **all** branches: local ones plus the remote-tracking ones (shown as `remotes/origin/...`). Works offline: it only shows what Git already knows from the last `git fetch` / `git pull` / `git clone`. To see branches that someone just created on GitHub, run `git fetch` first. |
| `git branch -v` | Lists the local branches together with the last commit on each (short hash + message). Handy for a quick look at what each branch is at. `git branch -vv` also shows which remote branch each one tracks and whether it's ahead/behind (e.g. `[origin/main: behind 2]`). |

<br>

## Comparing changes

| Command | What it does |
| --- | --- |
| `git diff` | Shows changes in your files that are **not staged yet**: working tree vs staging area. Removed lines start with `-` (red), added lines with `+` (green). Once you `git add` a file, its changes disappear from here. New untracked files aren't shown. Long output opens in a pager: quit with `q`. |
| `git diff HEAD` | Shows **all** changes since the last commit, staged and unstaged together: working tree vs last commit. `HEAD` = the last commit on the branch you're on. |
| `git diff HEAD <file_name>` | Same as `git diff HEAD`, but only for one file. |
| `git diff --staged` | Shows changes that are **staged**, i.e. exactly what goes into the next commit: staging area vs last commit. Run it before `git commit` as a final check. Same as `git diff --cached`. |
| `git diff --staged <file_name>` | Same as `git diff --staged`, but only for one file. |
| `git diff branch1..branch2` | Compares the last commits of two branches: what you'd have to change to get from `branch1` to `branch2`. Lines only in `branch2` show as `+`, lines only in `branch1` as `-`; swapping the order swaps them. E.g. `git diff main..feature` = how `feature` differs from `main` right now. If `main` got new commits since `feature` was created, those show up too (as `-`). Your files aren't touched. |
| `git diff commit1..commit2` | Compares two commits, using their hashes from `git log --oneline`, e.g. `git diff a1b2c3d..f9e8d7c`. Same `+` / `-` logic as with branches: older commit first shows what changed since then. |

<br>

## Staging and committing workflow

| Command | What it does |
| --- | --- |
| `git add <file>` | Stages a file: puts its current content into the staging area, i.e. "this goes into the next commit". Works for new files (starts tracking them) and for modified ones. Edit the file again after `git add` and you have to add it again, otherwise the commit takes the version from the time of `git add`. Several files at once: `git add a.py b.py`, or a whole folder: `git add src/`. |
| `git add .` | Stages **everything** in the current folder and its subfolders: new, modified and deleted files. Files listed in `.gitignore` are skipped. Run from the repo's root to stage the whole project. Check `git status` first so nothing unwanted goes in. |
| `git commit` | Saves the staged changes as a new commit (a snapshot in the history). Without `-m` it opens a text editor for the commit message; save and close it to finish the commit. Which editor opens is set by `git config core.editor`: with `code --wait` it's a VS Code tab (write the message, save, close the tab); the default is Vim (`Esc`, then `:wq` + `Enter`). Only staged changes go in; unstaged ones stay in your files for later. |
| `git commit -m "message"` | Commits with the message written straight in the command, no editor. The usual way. Keep the message short and say what changed, e.g. `git commit -m "Add bronze layer pipeline"`. |
| `git commit -am "message"` | Shortcut for `git add` + `git commit -m` in one step: stages all **modified and deleted tracked** files and commits them. **Doesn't** include new (untracked) files; those still need `git add` first. |
| `git commit --amend` | Fixes the **last** commit: replaces it with a new one (new hash) instead of adding another commit. Fix the message: `git commit --amend -m "Correct message"` (without `-m` it opens the editor with the old message). Add a forgotten file: `git add <file>`, then `git commit --amend --no-edit` (`--no-edit` = keep the message, no editor). Use it **only on commits that aren't pushed yet**: amending a pushed commit makes your branch differ from GitHub, so a normal `git push` fails and you'd need a force push that rewrites history for everyone. For pushed commits make a new commit with the fix instead. |
| `git rm --cached <file>` | Removes a file from the **cache** (the index / staging area, i.e. the list of files Git tracks) and keeps it on disk. Used to stop tracking a file that's already committed, because `.gitignore` alone doesn't work on files Git already tracks. Always combine it with `.gitignore`: **1.** `git rm --cached <file>`, **2.** add the file to `.gitignore`, **3.** `git commit`. Without step 2 the file shows up as untracked and the next `git add .` adds it back. The file still stays in older commits. For a folder add `-r`: `git rm -r --cached <folder>`. |

<br>

## Undoing changes & Time travelling

| Term | What it is |
| --- | --- |
| `HEAD` | A pointer to **where you are now**. Normally it points to a **branch** (e.g. `main`), and the branch points to its last commit, so `HEAD` = the last commit of the branch you're on. When you commit, the branch moves forward and `HEAD` moves with it. With `git checkout <commit_hash>` you can point `HEAD` straight at an older commit instead of a branch: this is called **detached HEAD**. You can look around and run the code as it was back then, but new commits made there don't belong to any branch and get lost when you switch away (keep them by creating a branch: `git switch -c <branch_name>`). Go back with `git switch main`. <pre>normal:    A ── B ── C   ← main ← HEAD<br><br>detached:  A ── B ── C   ← main<br>                ↑<br>               HEAD</pre> |

| Command | What it does |
| --- | --- |
| `git checkout <commit_hash>/HEAD~n` | Time travel: moves `HEAD` to an older commit (detached HEAD) and your files change to how they were at that point. Pick the commit either by hash from `git log --oneline` (e.g. `git checkout a1b2c3d`) or by counting back from where you are: `HEAD~1` = one commit back, `HEAD~3` = three commits back. Just for looking around; your branch doesn't change. Commit or stash your changes first. Back to the present: `git switch main`. |
| `git restore <file_name>` | Throws away the unstaged changes in a file and returns it to the last committed (or staged) version. **Can't be undone**: the uncommitted changes are gone. For all files use `.` instead of the file name: `git restore .` (new untracked files aren't touched). |
| `git restore --staged <file_name>` | Unstages a file, the opposite of `git add`. The changes stay in the file, they just won't go into the next commit. For all files use `.` instead of the file name: `git restore --staged .`. |
| `git restore --source <commit_hash>/HEAD~n <file_name>` | Brings back a file as it was in an older commit, using either a hash or `HEAD~n`, e.g. `git restore --source a1b2c3d app.py`. Only your file changes: `HEAD` and the branch stay where they are, so it shows up as modified; commit it if you want to keep the old version. Overwrites uncommitted changes in that file. For all files use `.` instead of the file name (tracked files that didn't exist yet in that commit are removed). |
| `git reset <commit_hash>` | Moves the branch back to that commit: the commits after it disappear from the branch, but **their changes stay in your files** (unstaged), so you can fix and commit them again. **Rewrites history**: use it only on commits that aren't pushed yet. <pre>before:  A ── B ── C ── D   (main)<br>git reset B<br>after:   A ── B             (main)     changes from C, D stay in files</pre> |
| `git reset --hard <commit_hash>` | Same, but also **throws away the changes**: your files match that commit exactly. The commits after it and all uncommitted changes are gone. The most dangerous command here; double-check the hash and use it only on commits that aren't pushed. <pre>before:  A ── B ── C ── D   (main)<br>git reset --hard B<br>after:   A ── B             (main)     C, D and uncommitted changes gone</pre> |
| `git reflog` | Like `git log`, but lists **every place `HEAD` has been**, including commits that disappeared from `git log` (after `git reset --hard`, a deleted branch, `--amend`...). Find the lost commit's hash there and go back with `git reset --hard <commit_hash>`. Only local, and only for committed work: uncommitted changes can't be rescued. <pre>before:  A ── B             (main)     C, D gone after git reset --hard B<br>git reflog                             ← still lists D with its hash<br>git reset --hard D<br>after:   A ── B ── C ── D   (main)</pre> |
| `git revert <commit_hash>` | Undoes a commit by creating a **new commit** with the opposite changes. The original commit stays in the history, so nothing is rewritten: the **safe way to undo pushed commits**. Opens the editor with a message (`Revert "..."`); save and close it. Can stop on a conflict, resolved like in a merge. <pre>before:  A ── B ── C ── D        (main)<br>git revert C<br>after:   A ── B ── C ── D ── C'  (main)     C' = undoes C</pre> |
| `git revert -n <commit_hash>` | Same, but **without committing** (`-n` = no commit): the opposite changes are only applied to your files and staged. Lets you revert several commits and then make one commit for all of them, or adjust the result first. Revert from the newest to the oldest. <pre>before:  A ── B ── C ── D        (main)<br>git revert -n D                  ← staged only, no commit<br>git revert -n C                  ← added to the staged changes<br>git commit -m "Revert C and D"<br>after:   A ── B ── C ── D ── R   (main)     R = undoes C + D</pre> |

<br>

## Stashing

| Command | What it does |
| --- | --- |
| `git stash list` | Lists all saved stashes, newest on top as `stash@{0}`, then `stash@{1}` etc. Each line shows the branch it was made on and its message. The numbers shift when you add or remove a stash, so check the list before using a number. |
| `git stash` | Puts your uncommitted changes (staged and unstaged) aside and resets your files to the last commit, so you have a clean working tree. Handy when you need to switch branches or pull, but your work isn't ready to commit. New untracked files are **not** stashed; add `-u` to include them. |
| `git stash -m "message"` | Same as `git stash`, but with your own description, e.g. `git stash -m "half-done silver layer"`. It shows in `git stash list`, so you know what each stash holds; without it you only see the last commit's message. |
| `git stash show -p stash@{n}` | Shows what's inside a stash before you bring it back: the full changes in the same `-` / `+` format as `git diff` (`-p` = patch). Without `-p` you get only a summary of changed files. Without `stash@{n}` it shows the newest one. |
| `git stash pop` | Brings back the newest stash (`stash@{0}`) into your files **and removes it** from the list. If it conflicts with your current files, Git keeps the stash in the list so nothing is lost. |
| `git stash apply` | Brings back the newest stash, but **keeps it** in the list. Useful when you want to apply the same changes to more branches. |
| `git stash apply stash@{n}` | Brings back a specific stash, e.g. `git stash apply stash@{2}`, with the number from `git stash list`. Keeps it in the list. |
| `git stash drop stash@{n}` | Deletes one stash from the list without applying it. Without `stash@{n}` it deletes the newest one. |
| `git stash clear` | Deletes **all** stashes at once. Can't be undone, so check `git stash list` first. |

<br>

## Branching

| Command | What it does |
| --- | --- |
| `git branch <branch_name>` | Creates a new branch starting from the commit you're on now. You **stay** on the current branch; switch to the new one with `git switch <branch_name>`. A branch is just a movable pointer to a commit, so creating one is instant and costs nothing. |
| `git switch <branch_name>` | Switches to an existing branch: your files change to that branch's version and new commits go there. Uncommitted changes come along if they don't clash with the target branch; if they would be overwritten, Git refuses, so commit them first. Works for a branch that exists only on the remote too: after `git fetch`, `git switch feature-x` creates a local `feature-x` linked to `origin/feature-x`. |
| `git switch -` | Switches back to the branch you were on before, like the "back" button. Run it again to jump back and forth between two branches. |
| `git switch -c <branch_name>` | Creates a new branch **and** switches to it in one step (`-c` = create). Same as `git branch <branch_name>` + `git switch <branch_name>`. The usual way to start work on something new. |
| `git branch -d <branch_name>` | Deletes a branch (`-d` = delete), safely: Git refuses if the branch has commits that aren't merged anywhere yet, so you can't lose work by accident. You can't delete the branch you're on; switch to another one first. Deletes only the local branch, not the one on GitHub. |
| `git branch -D <branch_name>` | Force-deletes a branch, **even with unmerged commits**. Those commits are then lost from the branch. Use it when you're sure you don't need the work, e.g. a failed experiment. |
| `git branch -m <new_branch_name>` | Renames the branch you're on (`-m` = move). To rename a different branch: `git branch -m <old_name> <new_name>`. Renames only the local branch; the branch on GitHub keeps its old name. |

<br>

## Merging

| Command | What it does |
| --- | --- |
| `git merge <branch_name>` | Merges the given branch **into the branch you're on**. So switch to the target first, then merge, e.g. `git switch main` → `git merge feature`. If both branches changed the same lines, Git stops with a conflict: fix the marked spots in the files, then `git add` + `git commit` to finish the merge. |
| `git merge --no-ff <branch_name>` | Merges and **always** creates a merge commit, even when a fast-forward would be possible (`--no-ff` = no fast-forward). A fast-forward just moves the pointer, so the history looks as if the branch never existed; with `--no-ff` you can still see where the branch started and where it was merged. Opens the editor for the merge commit message; add `-m "message"` to skip it. |
| `git merge --squash <branch_name>` | Takes all the changes from the branch and stages them as **one** set of changes, without committing. Finish with `git commit -m "message"` yourself. The whole branch ends up as a single commit on your branch, and its individual commits don't appear in the history. Handy for a branch full of small "fix" / "wip" commits. Git doesn't record it as a merge, so `git branch -d` on that branch refuses afterwards; delete it with `-D`. <pre>before:  A ── B ── E          (main)<br>              \\<br>               C ── D         (feature)<br><br>after:   A ── B ── E ── S     (main)     S = changes from C + D<br>              \\<br>               C ── D         (feature)</pre> |
| `git rebase <branch_name>` | Not a merge, but an alternative to it: moves your branch's commits **on top of** the last commit of the given branch, as if you had started your work from there. All commits are kept, but they get **new hashes** (`C'`, `D'`). Afterwards the merge is a fast-forward, so the history stays straight with no merge commit. Steps: **1.** `git switch feature`, **2.** `git rebase main` (or `master`), **3.** `git switch main`, **4.** `git merge feature`. On a conflict Git stops at that commit: fix the file, `git add` it, then `git rebase --continue` (or `git rebase --abort` to cancel). **Never rebase commits that are already pushed and used by others**: the new hashes rewrite history, same as `--amend`. <pre>before:  A ── B ── E          (main)<br>              \\<br>               C ── D         (feature)<br><br>after:   A ── B ── E ── C' ── D'   (main, feature)</pre> |
| `git merge --abort` | Cancels a merge that stopped on a conflict and returns everything to the state before `git merge`. Use it when you don't want to resolve the conflict right now. |

<br>

### Merging scenarios

| Scenario | What happens |
| --- | --- |
| **Fast-forward** | Happens when the branch you merge **into** (e.g. `main`) has **no new commits** since the other branch was created from it. Git doesn't combine anything: it just moves the `main` pointer forward to the branch's last commit. No merge commit, and it **can never conflict**, because only one side changed. As soon as `main` gets even one new commit (e.g. a commit that only adds a new file), the history has diverged and it's no longer a fast-forward. Only commits count; uncommitted changes don't. <br><br> Example: merging `feature` → into `main` (`git switch main`, then `git merge feature`). `main` had no new commits after `B`, so Git just moves `main` forward from `B` to `D`: <pre>before:  A ── B             (main)<br>              \\<br>               C ── D       (feature)<br><br>after:   A ── B ── C ── D   (main, feature)</pre> |
| **Three-way**<br>**(NO&#8209;CONFLICT)** | Happens when **both** branches have new commits since they split (the history has diverged), so Git can't just move the pointer. It compares **three** commits: the **merge base** (the common ancestor where the branches split), the last commit on `main` and the last commit on the other branch. File by file: changed on one side only → that change is taken; both sides changed **different** lines → both changes are combined automatically. Git then creates a **merge commit** (`M`) with two parents. The editor opens with a default message (`Merge branch 'feature'`); just save and close it. <br><br> Example: merging `feature` → into `main` (`git switch main`, then `git merge feature`). `main` got commit `E` after the split at `B`, so Git combines `E` and `D` into the new merge commit `M`: <pre>before:  A ── B ── E        (main)<br>              \\<br>               C ── D       (feature)<br><br>after:   A ── B ── E ── M   (main)<br>              \\        /<br>               C ── D       (feature)</pre> |
| **Three-way**<br>**(CONFLICT)** | Happens when both branches have new commits (three-way) **and** both changed the **same thing** since the merge base. Git can't tell which version is right, so it **stops** the merge before creating `M` and marks the conflicting files (`git status` lists them under `Unmerged paths`). You decide what the result should be, then `git add` the file + `git commit` (or `git merge --continue`) creates `M`. Or cancel everything with `git merge --abort`. `HEAD` in Git's messages = the branch you're on (`main`). <br><br> **Example 1: content conflict.** Both branches changed the **same lines** of `edit.txt`: <pre>before:  A ── B ── E        (main)     E: changes line 3 of edit.txt<br>              \\<br>               C ── D       (feature)  D: changes line 3 of edit.txt</pre> `git merge feature` stops with `CONFLICT (content): Merge conflict in edit.txt` and writes both versions into the file: <pre>&lt;&lt;&lt;&lt;&lt;&lt;&lt; HEAD<br>line 3 from main<br>=======<br>line 3 from feature<br>&gt;&gt;&gt;&gt;&gt;&gt;&gt; feature</pre> Edit the file to the final version, delete the markers, then `git add edit.txt` + `git commit`: <pre>after:   A ── B ── E ── M   (main)<br>              \\        /<br>               C ── D       (feature)</pre> <br> **Example 2: modify/delete conflict.** `feature` deleted `automation.py`, while `main` modified it: <pre>before:  A ── B ── E        (main)     E: modifies automation.py<br>              \\<br>               C ── D       (feature)  D: deletes automation.py</pre> `git merge feature` stops with `CONFLICT (modify/delete): automation.py deleted in feature and modified in HEAD`. Choose one: keep the file → `git add automation.py`, or delete it → `git rm automation.py`. Then `git commit` creates the merge commit `M`, same "after" as in Example 1. |

<br>

## Git configuration

| Command | What it does |
| --- | --- |
| `git config --list` | Lists all Git settings that apply in the current place (`key=value`, one per line). Long output opens in a pager: quit with `q`. Add `--show-origin` to see which file each setting comes from (global `~/.gitconfig` or the repo's `.git/config`). The same key can appear more than once; the last one wins. |
| `--global` vs `--local` | Where a setting is stored and what it applies to. `--global` = all your repositories on this PC, stored in `~/.gitconfig` (`C:\Users\<you>\.gitconfig` on Windows). `--local` = only the current repository, stored in `.git/config`; it's the default when you write neither. Local overrides global, so e.g. a work repo can use a different e-mail than the rest. |
| `git config <key>` | Shows the value of one setting, e.g. `git config core.editor` or `git config user.email`. Prints nothing if it's not set. |
| `git config --global user.name "Name"` | Sets the author name written into every commit you make. Shows up in `git log` and on GitHub. Doesn't need to match your GitHub username. |
| `git config --global user.email "email"` | Sets the author e-mail written into every commit. GitHub links commits to your account by this e-mail, so use one that's added to your GitHub account. Without `user.name` and `user.email` Git usually refuses to commit (`Please tell me who you are`). |
| `git config --global core.editor "code --wait"` | Sets VS Code as the editor Git opens for commit messages (e.g. `git commit` without `-m`) and other text input. `--global` = applies to all your repositories on this PC (stored in `~/.gitconfig`). `--wait` = Git waits until you close the VS Code tab before it continues; without it Git would take an empty message right away and abort the commit. Needs the `code` command on PATH (VS Code adds it on install). |
| `git config --global init.defaultBranch main` | New repositories created with `git init` start with a branch named `main` instead of the old default `master`. Matches GitHub, where new repos use `main`. Doesn't rename branches in existing repos. |

<br>

## Hidden files & folders

| File / Folder | What it does |
| --- | --- |
| `.git` | Hidden folder in the repository's root, created by `git init` or `git clone`. It **is** the repository: it holds the full history (all commits), branches, remotes and config. Your project files around it are the **working tree**: the current checked-out version you work with. Never edit it by hand. Git ignores it automatically: it's never committed and doesn't need to be in `.gitignore`. Deleting it removes all Git history, and the folder becomes a plain folder again (your files stay). Hidden by default; in VS Code it's hidden in the Explorer too. |
| `.gitignore` | Text file listing files and folders Git should **not** track, one pattern per line, e.g. `.venv/`, `__pycache__/`, `*.log`, `.env`. Ignored files don't show up in `git status` and can't be added by accident. Usually sits in the repo's root and applies to the whole project; a `.gitignore` in a subfolder applies only to that folder and below. It's committed to the repo, so the rules apply to everyone who clones it. Only works for files that aren't tracked yet; an already committed file has to be removed from tracking first with `git rm --cached <file>`. |

<br><br>

# 🟡 GitHub <br>

<br>

## Connections terminology

- **Remote** = **where**: a named link (name + URL) to a whole repository somewhere else, stored in `.git/config`. One repo can have several, e.g. `origin` → GitHub and `azure` → Azure DevOps. Each one is a separate repository; they don't sync by themselves, you push to each one separately.
- **Upstream** = the **default where for one branch**: its connection to one remote branch (e.g. `main` → `origin/main`), where a plain `git push` / `git pull` goes. Each branch has at most one; any other remote has to be named in the command.

```
   Local
 ┌──────────────────────────────────┐        GitHub
 │  local repository                │        ┌──────────────────────────────┐
 │                                  │        │  github.com/tomas/repo.git   │
 │  branch main                     │        │                              │
 │    upstream = origin/main ═══════╪══════► │    main                      │
 │                                  │        └──────────────────────────────┘
 │  remotes:                        │                       ▲
 │    origin ───────────────────────┼───────────────────────┘
 │                                  │        Azure DevOps
 │    azure  ───────────────────────┼──────┐ ┌──────────────────────────────┐
 │                                  │      └►│  dev.azure.com/.../repo      │
 └──────────────────────────────────┘        │                              │
                                             │    main                      │
                                             └──────────────────────────────┘
```

| Situation | Upstream set automatically? |
| --- | --- |
| `git clone` | ✅ **Yes, but only for the default branch** (`main`). Git creates a local `main` linked to `origin/main`. The other branches from GitHub exist only as `origin/...` remote-tracking branches. |
| `git switch <branch>` for a branch that exists only on GitHub | ✅ **Yes.** Git creates a local branch linked to `origin/<branch>`. |
| `git switch -c <branch>`, i.e. a new branch you created yourself | ❌ **No.** It doesn't exist on GitHub yet, so there's nothing to link to. Set it on the first push: `git push -u origin <branch>`. |
| `git init` + `git remote add origin <url>` | ❌ **No.** The remote is added, but no branch is linked to it. Do the first push with `-u`: `git push -u origin main`. |

<br>

## Remote connections

| Command | What it does |
| --- | --- |
| `git remote` | Lists the names of the remotes (links to repositories on GitHub) this repo knows, usually just `origin`. After `git clone` the `origin` remote is set up automatically; after `git init` the list is empty until you add one. |
| `git remote -v` | Same, but with the URLs (`-v` = verbose). Each remote shows twice, once for `fetch` and once for `push`. Handy to check where your `git push` actually goes. |
| `git branch -vv` | Lists the local branches with their last commit and the remote branch each one is linked to (its **upstream**), plus whether it's ahead/behind, e.g. `[origin/main: ahead 1, behind 2]`. A branch without `[...]` has no upstream yet, so a plain `git push` won't work on it. Ahead/behind is based on the last `git fetch`. |
| `git remote add <name> <url>` | Links your local repo to a repo on GitHub under a name you choose, e.g. `git remote add origin https://github.com/user/repo.git`. `origin` is the usual name for the main remote. Typical after `git init` + creating an empty repo on GitHub. Only saves the link; nothing is uploaded yet. |
| `git remote rename <old> <new>` | Renames a remote, e.g. `git remote rename origin github`. Its remote-tracking branches are renamed too (`origin/main` → `github/main`). |
| `git remote remove <name>` | Removes the link to a remote. Nothing is deleted on GitHub and your local branches and commits stay; only the connection and its `origin/...` branches go away. |
| `git branch -dr <remote>/<branch>` | Deletes one **remote-tracking branch** from your PC, e.g. `git branch -dr origin/utilities` (`-d` = delete, `-r` = remote). The branch on GitHub stays, and so does the remote. Handy for cleaning up a branch that was already deleted on GitHub. If it still exists there, it comes back with the next `git fetch`. |
| `git push <remote> <branch>` | Uploads the commits of a local branch to the remote, e.g. `git push origin main`. If the branch doesn't exist on GitHub yet, it's created. Only commits are pushed, not uncommitted changes. If GitHub has commits you don't have, the push is rejected: `git pull` first, then push again. |
| `git push -u <remote> <branch>` | Same, and also sets the **upstream** (`-u` = `--set-upstream`): links the local branch to the remote one. From then on, a plain `git push` / `git pull` on that branch is enough, no names needed. Do it once per branch, usually on its first push. Check the link with `git branch -vv`. |

<br>

## Fetching & pulling

| Command | What it does |
| --- | --- |
| `git branch -r` | Lists only the **remote-tracking branches** (`origin/main`, `origin/feature`...), i.e. Git's local copies of the branches on GitHub. Unlike `git branch -a`, which shows local and remote ones together. |
| `git switch <branch>` | After `git clone` or `git fetch`, the branches from GitHub exist on your PC only as remote-tracking branches (`origin/<branch>`): read-only bookmarks you don't work on directly. `git switch <branch>` with the plain name (no `origin/`) creates a **local branch** from `origin/<branch>`, links it to it (upstream) and switches to it, so you can commit and `git push` / `git pull` right away. |
| `git checkout <remote>/<branch>` | Switches straight to the remote-tracking branch, e.g. `git checkout origin/feature`. That's a **detached HEAD**: fine for looking around, but commits made there don't belong to any branch. To work on the branch use `git switch <branch>` instead. |
| `git fetch` | Downloads the latest changes from the remote (e.g. GitHub): new commits and new branches. It **doesn't** touch your files or your local branch; it only updates the remote-tracking branches (`origin/main` etc.). After it, `git status` tells you whether you're behind the remote (e.g. `Your branch is behind 'origin/main' by 2 commits`). Safe to run anytime: it never overwrites anything. Unlike `git pull`, which fetches **and** merges the changes into your branch. Without a name it fetches from the current branch's upstream remote, or `origin`. |
| `git fetch <remote>` | Same, but from the remote you name, e.g. `git fetch origin`. With just one remote it's the same as plain `git fetch`; it matters when you have more (e.g. `git fetch upstream`). |
| `git fetch <remote> <branch>` | Fetches only one branch, e.g. `git fetch origin main`, and updates just `origin/main`. Faster when the repo has many branches and you need only one. |
| `git fetch --prune` | Fetches as usual and also deletes the remote-tracking branches (`origin/...`) whose branch no longer exists on GitHub. Cleans up all of them at once, unlike `git branch -dr`, which removes one. Your local branches aren't touched, even if their upstream is gone (`git branch -vv` then shows `[origin/...: gone]`). |
| `git pull` | `git fetch` + `git merge` in one step: downloads the new commits of the current branch's upstream and merges them into your branch, so **your files change**. Needs an upstream (set by `git clone`, `git switch <branch>` or `git push -u`). If both you and GitHub have new commits, it's a three-way merge and can end with a conflict. Commit or stash your changes first. |
| `git pull <remote> <branch>` | Pulls a specific branch from a specific remote into the branch you're on, regardless of the upstream. E.g. on `feature`: `git pull origin main` merges the latest `main` from GitHub into `feature`, a common way to keep a feature branch up to date. |

<br>
