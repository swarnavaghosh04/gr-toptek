find_package(PkgConfig)

PKG_CHECK_MODULES(PC_GR_TOPTEK gnuradio-toptek)

FIND_PATH(
    GR_TOPTEK_INCLUDE_DIRS
    NAMES gnuradio/toptek/api.h
    HINTS $ENV{TOPTEK_DIR}/include
        ${PC_TOPTEK_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    GR_TOPTEK_LIBRARIES
    NAMES gnuradio-toptek
    HINTS $ENV{TOPTEK_DIR}/lib
        ${PC_TOPTEK_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/gnuradio-toptekTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(GR_TOPTEK DEFAULT_MSG GR_TOPTEK_LIBRARIES GR_TOPTEK_INCLUDE_DIRS)
MARK_AS_ADVANCED(GR_TOPTEK_LIBRARIES GR_TOPTEK_INCLUDE_DIRS)
