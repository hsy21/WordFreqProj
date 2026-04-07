import streamlit as st

st.title('Hello, Streamlit')

name = 'siyoon'
st.title(f'Hello, {name}.')
st.error(f'welcom to the league of draven')

"""
데이터프레임 출력 예시
magic command 확인 가능
"""
import pandas as pd
df = pd.DataFrame({
    'A' :   [1, 2, 3, 4],
    'B' :   [10, 20, 30, 40]
})

df
import time

@st.cache_data
def change_text():
    text = st.info('text가 가장 먼저 변합니다')
    time.sleep(2)
    text.success('2초가 지났습니다.')

change_text()


text = st.info('text 바뀝니다')
time.sleep(3)
text.error('5')
time.sleep(1)
text.error('4')
time.sleep(1)
text.error('3')
time.sleep(1)
text.error('2')
time.sleep(1)
text.error('1')
time.sleep(1)
text.success('짠')

