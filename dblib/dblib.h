#ifndef DBLIB_H
#define DBLIB_H

#include <QtSql/QSqlDatabase>
#include <QtSql/QSqlError>
#include <QtSql/QSqlQuery>
#include <QVariant>
#include <list>
#include "dblib_global.h"

using namespace std;

class DBLIBSHARED_EXPORT Dblib
{

public:
    Dblib();
    list<QString> listEmployees();

private:
    list<QString> executeQuery(QString queryString);

};

#endif // DBLIB_H
