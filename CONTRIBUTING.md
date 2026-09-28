# CONTRIBUTING
This project's development workflow promotes a protected branch and release/VERSION branch. The main branch represents
the latest current release version. Here is a general overview:

feature-branch -> (protected via PR only) develop -> release/VERSION -> (tagged release) main

## DEVELOPMENT WORKFLOW
(LOCAL)
1. Fetch and update all local remote-tracking branches: `git fetch origin`
2. Switch branch (add -c if new): `git switch <branch-name>`
3. Rebase protected branch: `git rebase origin/develop`
4. Resolve any conflicts: `git add <files>` and `git rebase --continue`
5. Push to origin: `git push --force-with-lease origin/feature-name`
6. Open a PR (pull request) to squash and merge onto the protected branch

(REMOTE: For reviewer/approver & testers)
7. Review, approve, and merge (protected branch->release); a RC (release candidate) will be released for beta testers
8. Pull & test the latest release branch locally: `git checkout <branch-name> && git pull origin <branch-name>`
9. Create a RC for testers:
```
git tag -a <tag-name>-rc# -m '<short-descrption>' && git push origin <tag-name>
ex: git tag -a v0.0.2-rc1 -m 'Release for testing' && git push origin v0.0.2-rc1
```
10. Once testing is complete, merge the release to production (main):
```
(compare) release/v0.0.2 --merge--> (base) main
```
11. Create an official release tag:
```
git checkout main && git pull origin main

git tag -a <tag-name> -m '<short-description>' && git push origin <TAG_NAME>
ex: git tag -a v0.0.2 -m 'Official release v0.0.2' && git push origin v0.0.2
```
12. Clean up and repeat (verify before cleaning): `git branch -d <branch-name> && git push origin -d <branch-name>`

THANKS FOR CONTRIBUTING!!!
