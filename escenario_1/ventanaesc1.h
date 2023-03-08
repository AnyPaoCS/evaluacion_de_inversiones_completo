#ifndef VENTANAESC1_H
#define VENTANAESC1_H

#include <QMainWindow>

namespace Ui {
class ventanaEsc1;
}

class ventanaEsc1 : public QMainWindow
{
    Q_OBJECT

public:
    explicit ventanaEsc1(QWidget *parent = nullptr);
    ~ventanaEsc1();

private:
    Ui::ventanaEsc1 *ui;
};

#endif // VENTANAESC1_H
