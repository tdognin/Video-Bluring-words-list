# Comprehensive Git Synchronization Guide

## Repository Information
- **Target Repository**: `git@github.com:tdognin/Video-Bluring-words-list.git`
- **Current Remote**: Points to `https://github.com/tdognin/Tetris.git` (needs to be updated)
- **Local Project**: `/Users/tdognin/Documents/tdognin/MyVideos project`

---

## ⚠️ IMPORTANT: Current Status

Your local repository is currently connected to the **wrong remote repository** (Tetris instead of Video-Bluring-words-list). This guide will help you:
1. Update the remote URL to the correct repository
2. Synchronize your local changes with the correct remote
3. Ensure both repositories are fully up to date

---

## Step-by-Step Synchronization Process

### Step 1: Check Current Remote Configuration

```bash
# View current remote repositories
git remote -v
```

**Expected Output** (before fix):
```
origin  https://tdognin:ghp_...@github.com/tdognin/Tetris.git (fetch)
origin  https://tdognin:ghp_...@github.com/tdognin/Tetris.git (push)
```

---

### Step 2: Update Remote URL to Correct Repository

**Option A: Using SSH (Recommended)**
```bash
# Update the remote URL to use SSH
git remote set-url origin git@github.com:tdognin/Video-Bluring-words-list.git
```

**Option B: Using HTTPS with Token**
```bash
# Update the remote URL to use HTTPS with your personal access token
git remote set-url origin https://tdognin:YOUR_GITHUB_TOKEN@github.com/tdognin/Video-Bluring-words-list.git
```

**Verify the change:**
```bash
git remote -v
```

**Expected Output** (after fix):
```
origin  git@github.com:tdognin/Video-Bluring-words-list.git (fetch)
origin  git@github.com:tdognin/Video-Bluring-words-list.git (push)
```

---

### Step 3: Verify SSH Connection (if using SSH)

```bash
# Test SSH connection to GitHub
ssh -T git@github.com
```

**Expected Output:**
```
Hi tdognin! You've successfully authenticated, but GitHub does not provide shell access.
```

**If SSH fails**, you may need to:
1. Generate SSH keys: `ssh-keygen -t ed25519 -C "your_email@example.com"`
2. Add the key to ssh-agent: `eval "$(ssh-agent -s)" && ssh-add ~/.ssh/id_ed25519`
3. Add the public key to GitHub: Copy `~/.ssh/id_ed25519.pub` and add it to GitHub Settings > SSH Keys

---

### Step 4: Check Current Branch and Status

```bash
# Check which branch you're on
git branch

# Check the status of your working directory
git status

# View commit history
git log --oneline -10
```

---

### Step 5: Fetch Latest Changes from Remote

```bash
# Fetch all branches and tags from the remote repository
git fetch origin

# View all branches (local and remote)
git branch -a

# View what changed in the remote
git log HEAD..origin/main --oneline
```

**What this does:**
- Downloads all commits, files, and refs from the remote repository
- Does NOT modify your working directory or current branch
- Allows you to see what's different before merging

---

### Step 6: Compare Local and Remote Changes

```bash
# See differences between local and remote main branch
git diff main origin/main

# See a summary of file changes
git diff --stat main origin/main

# View commits that are in remote but not in local
git log main..origin/main --oneline

# View commits that are in local but not in remote
git log origin/main..main --oneline
```

---

### Step 7: Synchronize Changes (Choose One Method)

#### Method A: Merge (Preserves Complete History)

```bash
# Merge remote changes into your local branch
git merge origin/main

# If merge is successful, you'll see:
# "Already up to date" or "Fast-forward" or a merge commit message
```

**Advantages:**
- Preserves complete history
- Shows when branches were merged
- Safer for collaborative work

#### Method B: Rebase (Creates Linear History)

```bash
# Rebase your local commits on top of remote commits
git rebase origin/main

# If rebase is successful, your commits will be replayed on top of remote changes
```

**Advantages:**
- Creates a cleaner, linear history
- Easier to follow commit progression
- Better for feature branches

**⚠️ Warning:** Don't rebase commits that have already been pushed to a shared repository.

---

### Step 8: Resolve Merge Conflicts (If Any)

If you encounter conflicts during merge or rebase:

#### For Merge Conflicts:

```bash
# View files with conflicts
git status

# Open conflicted files and look for conflict markers:
# <<<<<<< HEAD
# Your changes
# =======
# Remote changes
# >>>>>>> origin/main

# After resolving conflicts in each file:
git add <resolved-file>

# Complete the merge
git commit -m "Merge remote changes and resolve conflicts"
```

#### For Rebase Conflicts:

```bash
# View files with conflicts
git status

# Resolve conflicts in each file

# After resolving:
git add <resolved-file>

# Continue the rebase
git rebase --continue

# Or abort if needed:
git rebase --abort
```

**Conflict Resolution Tools:**
```bash
# Use VS Code's built-in merge tool
code <conflicted-file>

# Or use Git's merge tool
git mergetool

# View the conflict in different ways
git diff --ours <file>    # Your changes
git diff --theirs <file>  # Remote changes
```

---

### Step 9: Push Local Commits to Remote

```bash
# Push your changes to the remote repository
git push origin main

# If you rebased and need to force push (use with caution):
git push origin main --force-with-lease
```

**⚠️ Important Notes:**
- `--force-with-lease` is safer than `--force` as it checks if remote has changed
- Only force push if you're sure no one else has pushed to the branch
- Regular `git push` should work if you used merge instead of rebase

---

### Step 10: Verify Synchronization

```bash
# Fetch and check status
git fetch origin
git status

# Should show: "Your branch is up to date with 'origin/main'"

# Verify commit history matches
git log --oneline -10
git log origin/main --oneline -10

# Check that local and remote are identical
git diff main origin/main
# Should show no output if fully synchronized
```

---

## Complete Synchronization Workflow (Quick Reference)

```bash
# 1. Update remote URL
git remote set-url origin git@github.com:tdognin/Video-Bluring-words-list.git

# 2. Verify remote
git remote -v

# 3. Check current status
git status

# 4. Fetch remote changes
git fetch origin

# 5. Compare changes
git log HEAD..origin/main --oneline

# 6. Merge or rebase (choose one)
git merge origin/main
# OR
git rebase origin/main

# 7. Resolve conflicts if any (see Step 8)

# 8. Push local changes
git push origin main

# 9. Verify synchronization
git status
```

---

## Common Scenarios and Solutions

### Scenario 1: Remote Has New Commits, Local Has No Changes

```bash
git fetch origin
git merge origin/main  # Fast-forward merge
# Result: Local is updated with remote commits
```

### Scenario 2: Local Has New Commits, Remote Unchanged

```bash
git push origin main
# Result: Remote is updated with local commits
```

### Scenario 3: Both Have Different Commits (Diverged)

```bash
git fetch origin
git merge origin/main  # Creates merge commit
# OR
git rebase origin/main  # Replays local commits on top
git push origin main
```

### Scenario 4: Accidentally Committed to Wrong Branch

```bash
# Create a new branch with current changes
git branch feature-branch

# Reset current branch to remote
git reset --hard origin/main

# Switch to new branch
git checkout feature-branch
```

### Scenario 5: Need to Undo Last Commit

```bash
# Undo commit but keep changes
git reset --soft HEAD~1

# Undo commit and discard changes
git reset --hard HEAD~1

# Undo pushed commit (creates new commit)
git revert HEAD
git push origin main
```

---

## Best Practices

### 1. **Always Fetch Before Starting Work**
```bash
git fetch origin
git status
```

### 2. **Commit Often with Clear Messages**
```bash
git add <files>
git commit -m "feat: Add video blurring feature for specific words"
```

### 3. **Pull Before Push**
```bash
git pull origin main  # Equivalent to fetch + merge
git push origin main
```

### 4. **Use Branches for Features**
```bash
git checkout -b feature/new-blur-algorithm
# Make changes
git commit -m "Implement new blur algorithm"
git push origin feature/new-blur-algorithm
```

### 5. **Keep Commits Atomic**
- One logical change per commit
- Makes it easier to revert if needed
- Improves code review process

### 6. **Review Changes Before Committing**
```bash
git diff                    # Unstaged changes
git diff --staged          # Staged changes
git status                 # Overview
```

---

## Troubleshooting

### Issue: "Permission denied (publickey)"

**Solution:**
```bash
# Check SSH keys
ls -la ~/.ssh

# Generate new SSH key if needed
ssh-keygen -t ed25519 -C "your_email@example.com"

# Add key to ssh-agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Copy public key and add to GitHub
cat ~/.ssh/id_ed25519.pub
```

### Issue: "fatal: refusing to merge unrelated histories"

**Solution:**
```bash
# Allow merging unrelated histories
git merge origin/main --allow-unrelated-histories
```

### Issue: "Your branch and 'origin/main' have diverged"

**Solution:**
```bash
# Option 1: Merge
git merge origin/main

# Option 2: Rebase
git rebase origin/main

# Option 3: Reset to remote (⚠️ loses local commits)
git reset --hard origin/main
```

### Issue: Merge Conflicts Are Too Complex

**Solution:**
```bash
# Abort the merge/rebase
git merge --abort
# OR
git rebase --abort

# Try a different strategy or resolve manually
```

### Issue: Pushed Wrong Commits

**Solution:**
```bash
# If no one else has pulled:
git reset --hard HEAD~1
git push origin main --force-with-lease

# If others have pulled (safer):
git revert HEAD
git push origin main
```

---

## Additional Git Commands Reference

### Viewing History
```bash
git log --graph --oneline --all --decorate
git log --author="tdognin"
git log --since="2 weeks ago"
git log --grep="blur"
git show <commit-hash>
```

### Stashing Changes
```bash
git stash                    # Save changes temporarily
git stash list              # View stashed changes
git stash pop               # Apply and remove latest stash
git stash apply             # Apply but keep stash
git stash drop              # Remove latest stash
```

### Branch Management
```bash
git branch                   # List local branches
git branch -a               # List all branches
git branch -d feature-name  # Delete local branch
git push origin --delete feature-name  # Delete remote branch
```

### Tagging
```bash
git tag v1.0.0              # Create lightweight tag
git tag -a v1.0.0 -m "Version 1.0.0"  # Annotated tag
git push origin v1.0.0      # Push tag to remote
git push origin --tags      # Push all tags
```

---

## Security Notes

### 1. **Never Commit Sensitive Data**
- API keys, passwords, tokens
- Use `.gitignore` to exclude sensitive files
- Use environment variables instead

### 2. **Remove Accidentally Committed Secrets**
```bash
# Remove file from history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch path/to/secret/file" \
  --prune-empty --tag-name-filter cat -- --all

# Force push (⚠️ rewrites history)
git push origin --force --all
```

### 3. **Use SSH Keys Instead of HTTPS Tokens**
- More secure
- No need to enter credentials repeatedly
- Can be revoked independently

---

## Automation Scripts

### Daily Sync Script
```bash
#!/bin/bash
# save as: sync-repo.sh

echo "🔄 Syncing repository..."

# Fetch latest changes
git fetch origin

# Check if there are changes
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse @{u})
BASE=$(git merge-base @ @{u})

if [ $LOCAL = $REMOTE ]; then
    echo "✅ Already up to date"
elif [ $LOCAL = $BASE ]; then
    echo "⬇️  Pulling changes..."
    git pull origin main
elif [ $REMOTE = $BASE ]; then
    echo "⬆️  Pushing changes..."
    git push origin main
else
    echo "⚠️  Diverged - manual intervention needed"
    exit 1
fi

echo "✅ Sync complete!"
```

### Pre-commit Hook
```bash
#!/bin/bash
# save as: .git/hooks/pre-commit

# Check for debugging statements
if git diff --cached | grep -E "console.log|debugger|pdb.set_trace"; then
    echo "❌ Found debugging statements. Please remove them."
    exit 1
fi

# Run tests
npm test || exit 1

echo "✅ Pre-commit checks passed"
```

---

## Summary Checklist

- [ ] Update remote URL to correct repository
- [ ] Verify SSH/HTTPS connection
- [ ] Check current branch and status
- [ ] Fetch latest changes from remote
- [ ] Compare local and remote changes
- [ ] Merge or rebase changes
- [ ] Resolve any conflicts
- [ ] Push local commits to remote
- [ ] Verify synchronization is complete
- [ ] Test that everything works

---

## Quick Command Reference Card

| Task | Command |
|------|---------|
| Check remote | `git remote -v` |
| Update remote | `git remote set-url origin <url>` |
| Fetch changes | `git fetch origin` |
| Merge changes | `git merge origin/main` |
| Rebase changes | `git rebase origin/main` |
| Push changes | `git push origin main` |
| Check status | `git status` |
| View diff | `git diff main origin/main` |
| View log | `git log --oneline -10` |
| Abort merge | `git merge --abort` |
| Abort rebase | `git rebase --abort` |

---

## Support and Resources

- **GitHub Documentation**: https://docs.github.com
- **Git Documentation**: https://git-scm.com/doc
- **Pro Git Book**: https://git-scm.com/book/en/v2
- **GitHub SSH Setup**: https://docs.github.com/en/authentication/connecting-to-github-with-ssh

---

**Last Updated**: 2026-02-22  
**Repository**: Video-Bluring-words-list  
**Author**: tdognin