INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_TRAFFIC_GEN traffic_gen)

FIND_PATH(
    TRAFFIC_GEN_INCLUDE_DIRS
    NAMES traffic_gen/api.h
    HINTS $ENV{TRAFFIC_GEN_DIR}/include
        ${PC_TRAFFIC_GEN_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    TRAFFIC_GEN_LIBRARIES
    NAMES gnuradio-traffic_gen
    HINTS $ENV{TRAFFIC_GEN_DIR}/lib
        ${PC_TRAFFIC_GEN_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/traffic_genTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(TRAFFIC_GEN DEFAULT_MSG TRAFFIC_GEN_LIBRARIES TRAFFIC_GEN_INCLUDE_DIRS)
MARK_AS_ADVANCED(TRAFFIC_GEN_LIBRARIES TRAFFIC_GEN_INCLUDE_DIRS)
