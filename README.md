# SKEWT-LOGP_python

anaconda environment
conda create -n SKEWT-LOGP_Python_ubuntu_env python=3.9
conda create -n SKEWT-LOGP_Python_win_env python=3.9
conda env list

# activate 가상환경 시작
mac/linux
source activate SKEWT-LOGP_Python_ubuntu_env
conda activate SKEWT-LOGP_Python_ubuntu_env

windows
activate SKEWT-LOGP_Python_env

# deactivate 가상환경 종료
mac/linux
conda deactivate

windows
deactivate

# install module
conda install spyder
pip install opencv-python


# 가상환경 내보내기 (export)
conda env export > SKEWT-LOGP_Python_ubuntu_env.yaml
conda env export > SKEWT-LOGP_Python_win_env.yaml

# .yaml 파일로 새로운 가상환경 만들기
conda env create -f SKEWT-LOGP_Python_ubuntu_env.yaml

# 가상환경 리스트 출력
conda env list

# 가상환경 제거하기
conda env remove -n SKEWT-LOGP_Python_env  