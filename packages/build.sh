#!/bin/bash

# Wazuh package builder
# Copyright (C) 2015, Wazuh Inc.
#
# This program is a free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public
# License (version 2) as published by the FSF - Free Software
# Foundation.
source helper_function.sh
# Function to download source code based on target
build_dir="/build_wazuh"

download_source() {
  local branch="$2"
  local local_source="$3"

  if [[ "$local_source" == "no" ]]; then
    curl -sL https://github.com/wazuh/wazuh/tarball/${branch} | tar zx
  fi
  # TODO: REMOVE DEBUG LS
  ls
}

# Function to build directories
build_directories() {
  local target="$1"
  local package_name="$2"

  mkdir -p "${build_dir}/${target}"
  source_dir="${build_dir}/${target}/${package_name}"
  cp -R wazuh* "$source_dir"
  echo "$source_dir"
}

# Function to handle future version updates
future_version() {
  local base_version="$1"
  local package_name="$2"

  local major=$(echo "$base_version" | cut -dv -f2 | cut -d. -f1)
  local minor=$(echo "$base_version" | cut -d. -f2)
  local version="${major}.30.0"
  local old_name="wazuh-${build_target}-${base_version}"
  new_name=wazuh-${build_target}-${version}

  mv "${build_dir}/${build_target}/${old_name}" "${build_dir}/${build_target}/${new_name}"
  # TODO: Check using RPM/deb what change over the -o -name "*.spec"
  find "${build_dir}/${build_target}/${new_name}" "${specs_path}" -name "*VERSION*" -o -name "*changelog*" -exec sed -i "s/${base_version}/${version}/g" {} \;
  sed -i "s/\$(VERSION)/${major}.${minor}/g" "${build_dir}/${build_target}/${new_name}/src/Makefile"
  sed -i "s/${base_version}/${version}/g" ${build_dir}/${build_target}/${new_name}/src/init/wazuh-{server,client,local}.sh
}

# Function to generate checksum and move files
post_process() {
  local file_path="$1"
  local checksum_flag="$2"
  local source_flag="$3"

  if [[ "$checksum_flag" == "yes" ]]; then
    sha512sum "$file_path" > /var/local/checksum/$(basename "$file_path").sha512
  fi

  if [[ "$source_flag" == "yes" ]]; then
    mv "$file_path" /var/local/wazuh
  fi
}

# Main script body

# Script parameters
build_target="$1"
wazuh_branch="$2"
architecture_target="$3"
jobs="$4"
package_release="$5"
directory_base="$6"
debug="$7"
checksum="$8"
wazuh_packages_branch="$9"
use_local_specs="${10}"
local_source_code="${11}"
future="${12}"

set -x

if [ -z "${package_release}" ]; then
    package_release="1"
fi

# Download source code
download_source "$build_target" "$wazuh_branch" "$local_source_code"
wazuh_version="$(cat wazuh*/src/VERSION| cut -d 'v' -f 2)"

# Build directories
package_name="wazuh-${build_target}-${wazuh_version}"
source_dir=$(build_directories "$build_target" "$package_name")

# SPECS
if [ "${use_local_specs}" = "no" ]; then
    specs_path="$(get_specs)"
else
    package_files="/specs"
    specs_path="${package_files}/SPECS"
fi

if [[ "$future" == "yes" ]]; then
  future_version "$wazuh_version" "$package_name"
fi

setup_build "$source_dir" "$specs_path" "$package_name"

if [[ "${debug}" == "yes" ]]; then
    set_debug ${sources_dir}
fi

# # Installing build dependencies
cd ${sources_dir}
mk-build-deps -ir -t "apt-get -o Debug::pkgProblemResolver=yes -y"

# Build package
if [[ "${architecture_target}" == "amd64" ]] ||  [[ "${architecture_target}" == "ppc64le" ]] || \
    [[ "${architecture_target}" == "arm64" ]]; then
    debuild --rootcmd=sudo -b -uc -us
elif [[ "${architecture_target}" == "armhf" ]]; then
    linux32 debuild --rootcmd=sudo -b -uc -us
else
    linux32 debuild --rootcmd=sudo -ai386 -b -uc -us
fi

# deb_file="wazuh-${build_target}_${wazuh_version}-${package_release}"
# if [[ "${architecture_target}" == "ppc64le" ]]; then
#   deb_file="${deb_file}_ppc64el.deb"
# else
#   deb_file="${deb_file}_${architecture_target}.deb"
# fi
# pkg_path="${build_dir}/${build_target}"

###############

# ... (other script specific logic)

# Post-processing
# post_process "$file_path" "$checksum" "$src" (optional, for rpm)




