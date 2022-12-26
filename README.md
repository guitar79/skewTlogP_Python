# skewTlogP_Python
anaconda environment

# Windows
## 가상환경 리스트
conda env list

## 가상환경 만들기
conda create -n skewTlogP_Python_win_env

## activate 가상환경 시작
conda activate skewTlogP_Python_win_env

## deactivate 가상환경 종료
deactivate

## install module
conda install matplotlib pandas numpy jupyter
pip install metpy

## 가상환경 내보내기 (export)
conda env export > skewTlogP_Python_win_env.yaml

## .yaml 파일로 새로운 가상환경 만들기
conda env create -f skewTlogP_Python_win_env.yaml

## .yaml 파일로 가상환경 업데이트(activate 되어있을 때)
conda env update --file skewTlogP_Python_win_env.yaml

## .yaml 파일로 가상환경 업데이트(deactivate 되어있을 때)
conda env update --skewTlogP_Python_win_env envname --file skewTlogP_Python_win_env.yaml

## 가상환경 제거하기
conda env remove -n skewTlogP_Python_win_env


# ubuntu

## 가상환경 리스트 출력
conda env list

## 가상환경 만들기 
conda create -n skewTlogP_Python_ubuntu_env

## activate 가상환경 시작
conda activate skewTlogP_Python_ubuntu_env

# deactivate 가상환경 종료
conda deactivate

# install module
conda install matplotlib pandas numpy jupyter
pip install metpy

# 가상환경 내보내기 (export)
conda env export > skewTlogP_Python_ubuntu_env.yaml

# .yaml 파일로 새로운 가상환경 만들기
conda env create -f skewTlogP_Python_ubuntu_env.yaml

## .yaml 파일로 가상환경 업데이트(activate 되어있을 때)
conda env update --file skewTlogP_Python_ubuntu_env.yaml

## .yaml 파일로 가상환경 업데이트(deactivate 되어있을 때)
conda env update --skewTlogP_Python_ubuntu_env envname --file skewTlogP_Python_ubuntu_env.yaml

# 가상환경 제거하기
conda env remove -n skewTlogP_Python_ubuntu_env