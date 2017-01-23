# TSNAD
    Detecting somatic mutations and predicting tumor-specific neo-antigens

    ******************** Software Information ***********************************
    Version: Tumor_Specific_NeoAntigen_Detector 2.0
    Python Version: 2.7.11
    Finish time: April, 2016.
    Developer: Zhan Zhou, Xingzheng Lyu, Jingcheng Wu
    Copyright (C) 2015-2017 - College of Pharmaceutical Sciences, 
               Zhejiang University - All Rights Reserved 
*****************************************************************************
# How to run TSNAD
    (1) After unzipping the software, enter into TSNAD folder and give execution 
       rights to TSNAD.
       Commands:
             cd [TSNAD_path]
             chmod +x TSNAD
    (2) If loading shared libraries errors occurs, please let your system find 
       the external dynamic link libraries located in dependencies folder. 
       You can add dependencies path (~/SMD/dependencies/) in the last of 
       ld.so.config. Then let changes come into effect.
       Commands:
             chmod a+w /etc/ld.so.config
             vim /etc/ld.so.config
             /sbin/ldconfig
    (3) If you get the error “/usr/lib/x86_64-linux-gnu/libstdc++.so.6: version
       'GLIBCXX_3.4.21' not found”, you need update your gcc.
       Commands:
             sudo apt-get install gcc
