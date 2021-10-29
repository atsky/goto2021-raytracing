# goto2021-raytracing

Материалы для школы GOTO 2021

Для реализации Ray tracing мы предлагаем использовать Python или С++. Если вы совсем не знакомы с С++ можно писать на Python работать будет медленнее. Если вы очень хотите, есть возможно писать на вашем любимом языке, но для этого вы должны отлично знать этот язык.

## Python

https://github.com/atsky/goto2021-raytracing/tree/main/template-python

Для установки билиотек рекомендуется использовать miniconda 
https://docs.conda.io/en/latest/miniconda.htm


### Windows
Можно восстановить среду из файла `environment.yml`
```
cd template-python
conda env create -f environment.yml
```
Или просто установить нужные пакеты
```
conda install numpy numba matplotlib scikit-image
```

```
python main.py
```

### Ubuntu Linux
```
sudo apt-get install python3-tk
sudo apt-get install python3-pil python3-pil.imagetk
```

```
pip3 install numpy
pip3 install numba
pip3 install scikit-image
pip3 install matplotlib
pip3 install pillow
```

### MacOS

Можно восстановить среду из файла `environment.yml`
```
cd template-python
conda env create -f environment.yml
```
Или просто установить нужные пакеты
```
conda install numpy numba matplotlib scikit-image
```

```
python main.py
```


## CPP
Шаблон для С++ находится тут. 
https://github.com/atsky/goto2021-raytracing/tree/main/template-cpp

Для его работы нужен OpenGL. Инструкции по установке
### Windows
TODO

### Ubuntu Linux


```
sudo apt-get install libgl1-mesa-dev
sudo apt-get install libglfw3-dev
sudo apt-get install libglew-dev
```

### MacOS

TODO
