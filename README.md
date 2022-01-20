# skewT-logP_python

anaconda environment
conda create -n skewT-logP_Python_ubuntu_env
conda create -n skewT-logP_Python_win_env
conda env list

# activate 가상환경 시작
mac/linux
conda activate skewT-logP_Python_ubuntu_env
source activate skewT-logP_Python_ubuntu_env

windows
activate skewT-logP_Python_env

# deactivate 가상환경 종료
mac/linux
conda deactivate

windows
deactivate

# install module
conda install spyder
pip install metpy


# 가상환경 내보내기 (export)
conda env export > skewT-logP_Python_ubuntu_env.yaml
conda env export > skewT-logP_Python_win_env.yaml

# .yaml 파일로 새로운 가상환경 만들기
conda env create -f skewT-logP_Python_ubuntu_env.yaml

# 가상환경 리스트 출력
conda env list

# 가상환경 제거하기
conda env remove -n skewT-logP_Python_env  