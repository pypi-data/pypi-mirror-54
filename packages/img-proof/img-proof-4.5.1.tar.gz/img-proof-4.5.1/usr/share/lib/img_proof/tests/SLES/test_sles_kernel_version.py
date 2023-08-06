def test_sles_kernel_version(host, get_release_value):
    version = get_release_value('VERSION')
    assert version
    version = version.split('-SP')
    config = host.run('sudo zcat /proc/config.gz')
    assert 'CONFIG_SUSE_VERSION={}\n'.format(version[0]) in config.stdout
    if len(version) > 1:
        assert 'CONFIG_SUSE_PATCHLEVEL={}\n'.format(
                version[1]) in config.stdout
