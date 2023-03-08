#include "ventanaesc1.h"
#include "ui_ventanaesc1.h"

ventanaEsc1::ventanaEsc1(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::ventanaEsc1)
{
    ui->setupUi(this);
}

ventanaEsc1::~ventanaEsc1()
{
    delete ui;
}
