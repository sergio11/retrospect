#ifndef DBLIB_GLOBAL_H
#define DBLIB_GLOBAL_H

#include <QtCore/qglobal.h>

#if defined(DBLIB_LIBRARY)
#  define DBLIBSHARED_EXPORT Q_DECL_EXPORT
#else
#  define DBLIBSHARED_EXPORT Q_DECL_IMPORT
#endif

#endif // DBLIB_GLOBAL_H
