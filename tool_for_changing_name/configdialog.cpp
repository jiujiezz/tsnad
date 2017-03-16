#include "configdialog.h"
#include "ui_configdialog.h"
#include <QFile>
#include <QFileDialog>
#include <QPushButton>
#include <QMessageBox>
#include <QDebug>
#include <iostream>
using namespace std;

configDialog::configDialog(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::configDialog)
{
    ui->setupUi(this);
}


configDialog::~configDialog()
{
    delete ui;
}

void configDialog::chooseFile()
{
    int index = ui->tabWidget->currentIndex(); //判断当前是normal还是tumor
    if(index == 0)
        getFilePath(LineMap1);
    else
        getFilePath(LineMap2);
}


void configDialog::getFilePath(QMap<QString, QLineEdit *> map)
{
    QPushButton* btn= qobject_cast<QPushButton*>(sender());
    QString filePath = QFileDialog::getOpenFileName(this,
                               tr("Please choose a file"), ".",
                               tr("*.*"));
    map[btn->objectName()]->setText(filePath);
}


void configDialog::addWidgets(QString str, QLineEdit *lane, QLineEdit *part)
{
    QVector<QString> fileString;
    QMap<QString, QLineEdit *> map;
    int index = ui->tabWidget->currentIndex();
    if(index == 0){
        fileString = fileString1;
        map = LineMap1;
    }else{
        fileString = fileString2;
        map = LineMap2;
    }
    QString lane_str = lane->text();
    QString part_str = part->text();
    if(lane_str.isEmpty() || part_str.isEmpty()){
        cout<<"Empty Input!"<<endl;
        QMessageBox::warning(this,tr("Empty Inputs"),tr("Please input lane number and part number!"),
                                 QMessageBox::Yes|QMessageBox::No);
    }else{
        bool ok;
        int lane_num = lane_str.toInt(&ok, 10);
        int part_num = part_str.toInt(&ok, 10);
        int all_num = lane_num * part_num;
        //生成文件字符串
        for(int i = 1; i <= lane_num ; i ++){
            for(int j = 1; j <= part_num ; j ++){
                fileString.push_back( str + "_L" + QString::number(i, 10) + "_P" + QString::number(j, 10) );
            }
        }

        for(int i = 0; i < all_num; i ++){
            QLabel *label = new QLabel(fileString[i]);
            QLineEdit *line = new QLineEdit("");
            QPushButton *button = new QPushButton("Browse");
            line->setObjectName(fileString[i]);
            line->setEnabled(false);
            line->setFocusPolicy(Qt::NoFocus);
            button->setObjectName(fileString[i]);

            if(index == 0){
                ui->gridLayout1->addWidget(label,i,1);
                ui->gridLayout1->addWidget(line,i,2);
                ui->gridLayout1->addWidget(button,i,3);
            }else{
                ui->gridLayout2->addWidget(label,i,1);
                ui->gridLayout2->addWidget(line,i,2);
                ui->gridLayout2->addWidget(button,i,3);
            }
            map.insert(fileString[i],line);

            connect(button, SIGNAL(clicked()), this, SLOT(chooseFile()));
        }
        if(index == 0){
            fileString1 = fileString;
            LineMap1 = map;
        }else{
            fileString2 = fileString;
            LineMap2 = map;
        }
    }
}


void configDialog::on_pushButton1_clicked()
{
    addWidgets("Normal", ui->lineEdit1, ui->lineEdit2);
}


void configDialog::on_pushButton3_clicked()
{
    addWidgets("Tumor", ui->lineEdit3, ui->lineEdit4);
}


void configDialog::on_pushButton2_clicked()
{
   deleteWidgets(fileString1);
}


void configDialog::on_pushButton4_clicked()
{
   deleteWidgets(fileString2);
}


void configDialog::deleteWidgets(QVector<QString> fileString)
{
    QLayoutItem *item;
    int index = ui->tabWidget->currentIndex();
    fileString.clear();
    if(index == 0){
        while((item = ui->gridLayout1->layout()->takeAt(0)) != 0){
            //删除widget
            if(item->widget()){
                delete item->widget();
            }
        }
        fileString1 = fileString;
    }else{
        while((item = ui->gridLayout2->layout()->takeAt(0)) != 0){
            //删除widget
            if(item->widget()){
                delete item->widget();
            }
        }
        fileString2 = fileString;
    }
}


void configDialog::on_pushButton5_clicked()
{
    QVector<QString> fileString = fileString1;
    QMap<QString, QLineEdit*> LineMap = LineMap1;

    //将tab1和tab2对应的fileString和LineMap合并
    for (int i = 0; i < fileString2.size(); ++i)
        fileString.append(fileString2[i]);
    QMap<QString,QLineEdit*>::iterator iter; //遍历map
    for ( iter = LineMap2.begin(); iter != LineMap2.end(); ++iter ) {
        LineMap.insert(iter.key(),iter.value());
    }

    QSet<bool> ok;
    ok.insert(false);//当widget已被清空
    int count = fileString.size();

    for (int i = 0; i < fileString.size(); ++i){
        //cout << fileString[i].toStdString().data() << endl;
        QString path1 = LineMap[fileString[i]]->text();
        //cout << path1.toStdString().data() << endl;
        int first = path1.lastIndexOf ("/");
        int last = path1.lastIndexOf (".");
        QString str1 = path1.left (first+1);               //从左边截取
        QString str2 = path1.right (path1.length ()-last); //从右边截取

        QString path2 = str1 + fileString[i] + str2;
        if(path1.isEmpty()){
            ok.insert(false);
        }else{
            bool success = QFile::rename(path1,path2);
            ok.insert(success);
        }
    }

    cout<<ok.contains(true)<<endl;
    if(count > 0){
        if(ok.contains(true)){
            QMessageBox::warning(this,tr("Modify Successfully"),tr("You have modified selected file names Successfully!"),
                                 QMessageBox::Yes|QMessageBox::No);
        }else{
            QMessageBox::warning(this,tr("No Permission"),tr("You have no permission to modify file names, \n"
                                                             " OR you did not choose any files, \n"
                                                             " OR you have modified file names."),
                                 QMessageBox::Yes|QMessageBox::No);
        }
    }else{
        QMessageBox::warning(this,tr("ERROR"),tr("Please click 'Confirm' button and then choose filepaths!"),
                             QMessageBox::Yes|QMessageBox::No);
    }
}
