<!-- BAS Metadata Library release issue template -->

<!--
Set issue title to 'X.X.X release' e.g. '0.8.0 release'
-->

For all releases:

1. [x] create a release issue
2. [ ] create a merge request from release issue
3. [ ] close the release in `CHANGELOG.md`
4. [ ] bump the package version using `poetry version`
5. [ ] push changes, merge the merge request into `main` and tag with version
6. [ ] create a new GitLab release, using the change log entry as release notes
7. [ ] link the GitLab release to the milestone and [PyPi package](https://pypi.org/project/bas-metadata-library)
8. [ ] close the GitLab milestone for the release
9. [ ] if needed, create a new milestone for the next release
