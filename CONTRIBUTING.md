# CONTRIBUTING

## DEVELOPMENT WORKFLOW
(Developer)
1. Get the latest codebase: `git checkout main && git pull origin main`
2. Create a new feature, fix, or release branch:
```
# Feature branch
git checkout -b feature/<DESCRIPTION>
ex: git checkout -b feature/add-dark-mode

# Feature branch
git checkout -b fix/<ISS#>-<DESCRIPTION>
ex: git checkout -b fix/123-bad-redirect

# Release branch
git checkout -b release/v<x.x.x>
ex: git checkout -b release/v0.0.2
```
3. Push to remote: `git push -u origin <BRANCH_NAME>`
4. Develop, add, commit, and push to remote
5. Open a PR (pull request) to merge into a release branch:
```
(compare) feature/add-dark-mode --merge--> (base) release/v0.0.2
```
(For reviewer/approver & testers)

6. Review, approve, and merge (feat->release); a RC (release candidate) will be released for beta testers
7. Pull & test the latest release branch locally: `git checkout <BRANCH_NAME> && git pull origin <BRANCH_NAME>`
8. Create a RC for testers:
```
git tag -a <TAG_NAME>-rc# -m '<SHORT_DESCRIPTION>' && git push origin <TAG_NAME>
ex: git tag -a v0.0.2-rc1 -m 'Release for testing' && git push origin v0.0.2-rc1
```
9. Once testing is complete, merge the release to production (main):
```
(compare) release/v0.0.2 --merge--> (base) main
```
10. Create an official release tag:
```
git checkout main && git pull origin main

git tag -a <TAG_NAME> -m '<SHORT_DESCRIPTION>' && git push origin <TAG_NAME>
ex: git tag -a v0.0.2 -m 'Official release v0.0.2' && git push origin v0.0.2
```
11. Clean up and repeat (verify before cleaning): `git branch -d <BRANCH_NAME> && git push origin -d <BRANCH_NAME>`

THANKS FOR CONTRIBUTING!!!
