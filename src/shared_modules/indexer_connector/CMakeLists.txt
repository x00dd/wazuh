cmake_minimum_required(VERSION 3.12.4)

project(indexer_connector)

enable_testing()

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_definitions(-DPROMISE_TYPE=PromiseType::NORMAL)

if (NOT SRC_FOLDER)
    get_filename_component(SRC_FOLDER     ${CMAKE_SOURCE_DIR}/../../ ABSOLUTE)
endif()

if (NOT SHARED_MODULES)
    get_filename_component(SHARED_MODULES ${CMAKE_SOURCE_DIR}/../ ABSOLUTE)
endif()

# Include directories
include_directories(include)

include_directories(${SRC_FOLDER})
include_directories(${SRC_FOLDER}/external/cJSON)
include_directories(${SRC_FOLDER}/external/nlohmann)
include_directories(${SRC_FOLDER}/external/rocksdb/include)

include_directories(${SHARED_MODULES}/utils)
include_directories(${SHARED_MODULES}/common)
include_directories(${SHARED_MODULES}/http-request/include)
include_directories(${SHARED_MODULES}/keystore/include)

# Link directories
link_directories(${SRC_FOLDER})
link_directories(${SRC_FOLDER}/external/rocksdb/build)
link_directories(${SHARED_MODULES}/http-request/build)
link_directories(${SHARED_MODULES}/keystore/build)

file(GLOB INDEXER_CONNECTOR_SRC
    "src/*.cpp"
    )

add_library(indexer_connector SHARED
    ${INDEXER_CONNECTOR_SRC}
    )

target_link_libraries(indexer_connector rocksdb urlrequest gcc_s wazuhext keystore)

set_target_properties(indexer_connector PROPERTIES
        BUILD_RPATH_USE_ORIGIN TRUE
        BUILD_RPATH "$ORIGIN/../lib"
)

add_subdirectory(testtool)
if(UNIT_TEST)
    add_subdirectory(tests)
endif()
