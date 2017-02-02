#include "mainwindow.h"
#include "logindialog.h"
#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    LoginDialog login;
    int result;
    do {
        result = login.exec();
        qInfo( "Login performed ");
    } while(result != LoginDialog::Success);

    MainWindow w;
    w.show();
    return a.exec();
}
