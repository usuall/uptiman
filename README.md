# uptiman

-----------------
# python 가상환경 생성
python -m venv .venv

#가상환경으로 진입
$PROJECT_HOME/.venv/Scripts/activate

# pip 업그레이드
python -m pip install --upgrade pip
 
# image-match 설치
git clone https://github.com/ascribe/image-match.git

cd image-match
pip install numpy
pip install scipy
pip install .


# html-similarity 설치
pip install html-similarity

-------------------------
# 크롬 드라이버 다운로드
https://chromedriver.chromium.org/downloads

# 셀레니움 다운로드
pip install selenium
pip install requests

-- optional
pip install gtts
pip install playsound
