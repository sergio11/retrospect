#include "dblib.h"
#include <dbconnectionfailed.h>

Dblib::Dblib()
{}

list<QString> Dblib::executeQuery(QString queryString) {

    list<QString> result;

    QSqlDatabase db = QSqlDatabase::addDatabase("QMYSQL3");
    db.setHostName("localhost");
    db.setPort(8889);
    db.setDatabaseName("employees");
    db.setUserName("root");
    db.setPassword("");


    if(!db.open()) {
        throw DBConnectionFailed();
    }

    QSqlQuery query;
    query.exec(queryString);
    while (query.next()) {
        QString fistName = query.value(2).toString();
        result.push_back(fistName);
    }
    db.close();

    result.push_back("Sergio");
    result.push_back("Manuel");
    result.push_back("Another User");

    return result;
}

list<QString> Dblib::listEmployees()
{
    return executeQuery("SELECT * FROM employees");
}
