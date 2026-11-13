- [🟡 Git ](#-git-)
  - [Creating a repository](#creating-a-repository)
  - [Checking commands](#checking-commands)
  - [Comparing changes](#comparing-changes)
  - [Staging and committing workflow](#staging-and-committing-workflow)
  - [Branching](#branching)
  - [Merging](#merging)
    - [Merging scenarios](#merging-scenarios)
  - [Git configuration](#git-configuration)
  - [Hidden files \& folders](#hidden-files--folders)

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
| `git status` | Shows the current state of the working folder: which branch you're on, which files are modified, which are staged (ready to commit) and which are untracked (new files Git doesn't follow yet). Changes nothing, so it's always safe to run. Run it before `git add` / `git commit` to see what will go in. |
| `git log` | Shows the commit history of the current branch, newest first. Each entry lists the commit hash (unique ID), author, date and commit message. Long output opens in a pager: scroll with the arrow keys or `Space`, quit with `q`. |
| `git log --oneline` | Short version of `git log`: one commit per line, with the shortened hash and the message only. Handy for a quick overview of the history or for copying a commit hash. |
| `git branch` | Lists the local branches. The current branch is marked with `*`. `git branch <name>` creates a new branch, but doesn't switch to it. |
| `git branch -a` | Lists **all** branches: local ones plus the remote-tracking ones (shown as `remotes/origin/...`). Works offline: it only shows what Git already knows from the last `git fetch` / `git pull` / `git clone`. To see branches that someone just created on GitHub, run `git fetch` first. |
| `git branch -v` | Lists the local branches together with the last commit on each (short hash + message). Handy for a quick look at what each branch is at. `git branch -vv` also shows which remote branch each one tracks and whether it's ahead/behind (e.g. `[origin/main: behind 2]`). |
| `git fetch` | Downloads the latest changes from the remote (e.g. GitHub): new commits and new branches. It **doesn't** touch your files or your local branch; it only updates the remote-tracking branches (`origin/main` etc.). After it, `git status` tells you whether you're behind the remote (e.g. `Your branch is behind 'origin/main' by 2 commits`). Safe to run anytime: it never overwrites anything. Unlike `git pull`, which fetches **and** merges the changes into your branch. |

<br>

## Comparing changes

| Command | What it does |
| --- | --- |
| `git diff` | Shows changes in your files that are **not staged yet**: working folder vs staging area. Removed lines start with `-` (red), added lines with `+` (green). Once you `git add` a file, its changes disappear from here. New untracked files aren't shown. Long output opens in a pager: quit with `q`. |
| `git diff HEAD` | Shows **all** changes since the last commit, staged and unstaged together: working folder vs last commit. `HEAD` = the last commit on the branch you're on. |
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
| `.git` | Hidden folder in the repository's root, created by `git init` or `git clone`. It **is** the repository: it holds the full history (all commits), branches, remotes and config. Your project files around it are just the current working copy. Never edit it by hand. Git ignores it automatically: it's never committed and doesn't need to be in `.gitignore`. Deleting it removes all Git history, and the folder becomes a plain folder again (your files stay). Hidden by default; in VS Code it's hidden in the Explorer too. |
| `.gitignore` | Text file listing files and folders Git should **not** track, one pattern per line, e.g. `.venv/`, `__pycache__/`, `*.log`, `.env`. Ignored files don't show up in `git status` and can't be added by accident. Usually sits in the repo's root and applies to the whole project; a `.gitignore` in a subfolder applies only to that folder and below. It's committed to the repo, so the rules apply to everyone who clones it. Only works for files that aren't tracked yet; an already committed file has to be removed from tracking first with `git rm --cached <file>`. |

<br><br>