import pytest


def test_sles_repos(
    get_instance_repos,
    get_release_value,
    get_sles_repos,
    is_sles_sap,
    determine_architecture
):
    version = [get_release_value('VERSION'), determine_architecture()]

    sap = is_sles_sap()
    if sap:
        version.append('SAP')

    version = '-'.join(version)

    missing_repos = []
    repos = get_sles_repos(version)

    if not repos:
        pytest.fail(
            'No repos found for version {0}'.format(version)
        )

    instance_repos = get_instance_repos()

    for repo in repos:
        if repo not in instance_repos:
            missing_repos.append(repo)

    if missing_repos:
        pytest.fail(
            'Missing Repos: \n{0}'.format('\n'.join(missing_repos))
        )
