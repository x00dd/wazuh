#!/bin/bash

get_specs(){
    curl -sL https://github.com/wazuh/wazuh-packages/tarball/${wazuh_packages_branch} | tar zx
    package_files="wazuh*/debs"
    specs_path=$(find ${package_files} -type d -name "SPECS" -path "*debs*")
    echo "$specs_path"
}

setup_build(){
    sources_dir="$1"
    specs_path="$2"
    package_name="$3"

    cp -pr ${specs_path}/wazuh-${build_target}/debian ${sources_dir}/debian
    cp -p /tmp/gen_permissions.sh ${sources_dir}

    # Generating directory structure to build the .deb package
    cd ${build_dir}/${build_target} && tar -czf ${package_name}.orig.tar.gz "${package_name}"

    # Configure the package with the different parameters
    sed -i "s:RELEASE:${package_release}:g" ${sources_dir}/debian/changelog
    sed -i "s:export JOBS=.*:export JOBS=${jobs}:g" ${sources_dir}/debian/rules
    sed -i "s:export DEBUG_ENABLED=.*:export DEBUG_ENABLED=${debug}:g" ${sources_dir}/debian/rules
    sed -i "s#export PATH=.*#export PATH=/usr/local/gcc-5.5.0/bin:${PATH}#g" ${sources_dir}/debian/rules
    sed -i "s#export LD_LIBRARY_PATH=.*#export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}#g" ${sources_dir}/debian/rules
    sed -i "s:export INSTALLATION_DIR=.*:export INSTALLATION_DIR=${directory_base}:g" ${sources_dir}/debian/rules
    sed -i "s:DIR=\"/var/ossec\":DIR=\"${directory_base}\":g" ${sources_dir}/debian/{preinst,postinst,prerm,postrm}
    if [ "${build_target}" == "api" ]; then
        sed -i "s:DIR=\"/var/ossec\":DIR=\"${directory_base}\":g" ${sources_dir}/debian/wazuh-api.init
        if [ "${architecture_target}" == "ppc64le" ]; then
            sed -i "s: nodejs (>= 4.6), npm,::g" ${sources_dir}/debian/control
        fi
    fi
}

set_debug(){
    local sources_dir="$1"
    sed -i "s:dh_strip --no-automatic-dbgsym::g" ${sources_dir}/debian/rules
}