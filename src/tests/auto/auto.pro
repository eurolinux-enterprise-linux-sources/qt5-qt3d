TEMPLATE = subdirs

SUBDIRS = \
    coretest \
    core \
    render \
    quick3d \
    cmake \
    input \
    animation \
    extras

installed_cmake.depends = cmake

for(subdir, SUBDIRS) {
    !equals(subdir, coretest) {
        $${subdir}.depends += coretest
    }
}
