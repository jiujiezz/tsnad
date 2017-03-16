#ifndef CONFIGDIALOG_H
#define CONFIGDIALOG_H

#include <QWidget>
#include <QLineEdit>
#include <QPushButton>
#include <QGridLayout>
namespace Ui {
class configDialog;
}

class configDialog : public QWidget
{
    Q_OBJECT

public:
    explicit configDialog(QWidget *parent = 0);
    ~configDialog();
    void addWidgets(QString str, QLineEdit *lane, QLineEdit *part);

public slots:
    void chooseFile();
    void getFilePath(QMap<QString, QLineEdit*> map);
    void deleteWidgets(QVector<QString> fileString);

private slots:
    void on_pushButton1_clicked();
    void on_pushButton2_clicked();
    void on_pushButton3_clicked();
    void on_pushButton4_clicked();
    void on_pushButton5_clicked();

private:
    Ui::configDialog *ui;
    QVector<QString> fileString1,fileString2; //如果改为指针？
    QMap<QString, QLineEdit*> LineMap1,LineMap2;
};

#endif // CONFIGDIALOG_H
