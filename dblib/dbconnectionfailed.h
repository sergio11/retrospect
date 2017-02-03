#ifndef DBCONNECTIONFAILED_H
#define DBCONNECTIONFAILED_H
#include <iostream>
#include <exception>
#include <stdexcept>

using namespace std;

class DBConnectionFailed : public runtime_error
{
    public:
        DBConnectionFailed();
};

#endif // DBCONNECTIONFAILED_H
