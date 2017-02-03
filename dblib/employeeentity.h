#ifndef EMPLOYEEENTITY_H
#define EMPLOYEEENTITY_H

#include<string>

using namespace std;

class EmployeeEntity
{

public:
    int getEmpNo() const
    { return emp_no; }

    void setEmpNo(int newEmpNo) {
        this->emp_no = newEmpNo;
    }

    string getFirstName() const
    { return first_name; }

    void setFirstName(string newFirstName) {
        this->first_name = newFirstName;
    }

    string getLastName() const
    { return last_name; }

    void setLastName(string newLastName) {
        this->last_name = newLastName;
    }

private:
    int emp_no;
    string first_name;
    string last_name;
};

#endif // EMPLOYEEENTITY_H
