#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QMessageBox>

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
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
