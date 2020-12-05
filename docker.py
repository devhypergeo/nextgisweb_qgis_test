from ngwdocker import PackageBase
from ngwdocker.base import AppImage
from ngwdocker.util import git_ls_files


class Package(PackageBase):
    pass


@AppImage.on_apt.handler
def on_apt(event):
    event.add_key("https://qgis.org/downloads/qgis-2020.gpg.key")
    event.add_repository("deb https://qgis.org/ubuntu-ltr $(lsb_release -sc) main")
    
    event.package(
        'build-essential', 'cmake',
        'libqgis-dev', 'qt5-image-formats-plugins',
        # Package qgis-providers-common is required to get standard icons working.
        # TODO: Don't install package with its dependecies, just download it and
        # extract files to /usr/share/qgis/svg.
        'qgis-providers-common',
    )


@AppImage.on_package_files.handler
def on_package_files(event):
    if event.package.name == 'nextgisweb_qgis':
        event.files.extend(git_ls_files(event.package.path / 'qgis_headless'))


@AppImage.on_virtualenv.handler
def on_virtualenv(event):
    event.before_install('$NGWROOT/env/bin/pip install --no-cache-dir package/nextgisweb_qgis/qgis_headless')  # NOQA: E501


@AppImage.on_config.handler
def on_config(event):
    event.image.config_set('qgis', 'svg_path', '/usr/share/qgis/svg')