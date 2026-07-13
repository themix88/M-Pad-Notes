# Maintainer: Miran Kljun <miran.kljun@gmail.com>

pkgname=m-pad
pkgver=1.0
pkgrel=1
pkgdesc="A lightweight text companion."
arch=('any')
url="https://github.com/themix88/M-Pad"
license=('GPL3')
depends=('python' 'python-pyqt6')
source=("git+https://github.com/themix88/M-Pad.git")
md5sums=('SKIP')

package() {
    cd "${srcdir}/M-Pad"

    # Install the application code
    install -d "${pkgdir}/opt/${pkgname}"
    install -Dm644 main.py "${pkgdir}/opt/${pkgname}/main.py"

    # Create executable wrapper
    install -d "${pkgdir}/usr/bin"
    echo '#!/bin/sh' > "${pkgdir}/usr/bin/m-pad"
    echo 'exec python /opt/m-pad/main.py "$@"' >> "${pkgdir}/usr/bin/m-pad"
    chmod 755 "${pkgdir}/usr/bin/m-pad"

    # Install desktop file and license
    install -Dm644 m-pad.desktop "${pkgdir}/usr/share/applications/m-pad.desktop"
    install -Dm644 LICENSE "${pkgdir}/usr/share/licenses/${pkgname}/LICENSE"
}
