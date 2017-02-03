#include "mainwindow.h"
#include "ui_mainwindow.h"

using namespace std;

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    QTextStream cout(stdout);
    //Dblib* dblib = new Dblib;
    try {

        list<EmployeeEntity> employees;
        EmployeeEntity emp1;

        emp1.setEmpNo(1);
        emp1.setFirstName("Sergio");
        emp1.setLastName("Sánchez");

        employees.push_back(emp1);

        EmployeeEntity emp2;
        emp2.setEmpNo(2);
        emp2.setFirstName("Manuel");
        emp2.setLastName("Martín");

        employees.push_back(emp2);

        //cout << "Se han obtenido " << employees.size() << " empleados" << endl;
        ui->tableWidget->setColumnCount(3);
        for(EmployeeEntity emp: employees) {
            const int currentRow = ui->tableWidget->rowCount();
            ui->tableWidget->setRowCount(currentRow + 1);
            QTableWidgetItem* empNoCell = new QTableWidgetItem;
            empNoCell->setText(QString::number(emp.getEmpNo()));
            ui->tableWidget->setItem(currentRow, 0, empNoCell);
            QTableWidgetItem* firstNameCell = new QTableWidgetItem;
            firstNameCell->setText(QString::fromUtf8(emp.getFirstName().c_str()));
            ui->tableWidget->setItem(currentRow, 1, firstNameCell);
            QTableWidgetItem* lastNameCell = new QTableWidgetItem;
            lastNameCell->setText(QString::fromUtf8(emp.getLastName().c_str()));
            ui->tableWidget->setItem(currentRow, 2, lastNameCell);
        }
    } catch (const DBConnectionFailed &e) {
        qInfo("DBConnectionFailed");
        qInfo(e.what());
    }

}

MainWindow::~MainWindow()
{
    delete ui;
}


void MainWindow::on_actionExit_triggered()
{
    QMessageBox msgBox(this);
    msgBox.setIcon(QMessageBox::Question);
    msgBox.setWindowTitle(tr("Pythonthusiast"));
    msgBox.setText(tr("Are you sure you want to quit?"));
    msgBox.setStandardButtons(QMessageBox::No|QMessageBox::Yes);
    msgBox.setDefaultButton(QMessageBox::Yes);

    if(msgBox.exec()==QMessageBox::Yes)
    {
        qApp->quit();
    }
}

void MainWindow::on_actionAbout_triggered()
{
    QMessageBox msgBox(this);
    msgBox.setMinimumWidth(400);
    msgBox.setMinimumHeight(400);
    QPixmap logo(":/images/icono_app.png");
    QPixmap logoScaled = logo.scaled(QSize(100, 100),  Qt::KeepAspectRatio);
    msgBox.setIconPixmap(logoScaled);
    msgBox.setWindowTitle(tr("Pythonthusiast"));
    msgBox.setText(tr("Well Watson, isn't it obvious to you that Qt rocks?"));
    msgBox.setStandardButtons(QMessageBox::Ok);
    msgBox.exec();
}
