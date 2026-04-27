import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
from matplotlib import font_manager, rc
from konlpy.tag import Okt

#폰트 설정
font_path = "c:/Windows/Fonts/malgun.ttf"
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)
# 그래프 마이너스 깨짐 방지
plt.rcParams['axes.unicode_minus'] = False

#제목, 너비 설정
st.set_page_config(page_title="단어 빈도수 시각화", layout="wide")

def main():
    st.title("단어 빈도수 시각화")

    #파일 입력
    with st.sidebar:

        #CSV 파일 올리기
        st.header("파일 선택")
        uploaded_file = st.file_uploader("파일을 선택하세요", type=['csv'])
        st.caption("데이터가 있는 컬럼")

        # 분석할 텍스트가 있는 컬럼 받기. 기본값 = review
        # 위에서 업로드한 파일 확안하기
        col_name = st.text_input("", value="review", label_visibility="collapsed")
        check_data_btn = st.button("데이터 파일 확인")
        
        # 구분선
        st.divider()
        

        st.header("설정")
        
        # 단어 빈도수 그래프 출력, 단어 개수는 10~50개, 기본값은 20개
        show_bar_chart = st.checkbox("빈도수 그래프", value=True)
        if show_bar_chart:
            bar_word_count = st.slider("단어 수", min_value=10, max_value=50, value=20, key='bar_slider')
        
        # 워드 클라우드, 20~500개, 기본 50
        show_wordcloud = st.checkbox("워드클라우드", value=False)
        if show_wordcloud:
            wc_word_count = st.slider("단어 수", min_value=20, max_value=500, value=50, key='wc_slider')

        # 빨간색 분석버튼    
        start_btn = st.button("분석", type="primary")

    # head()로 상위 5개만 미리보기
    if uploaded_file and check_data_btn:
        df = pd.read_csv(uploaded_file)
        st.write("데이터 미리보기 : ")
        st.dataframe(df.head())
    
    # 컬럼에 데이터가 있는지 확인하기
    if uploaded_file and start_btn:
        df = pd.read_csv(uploaded_file)
        
        if col_name in df.columns:
            # 결측치 제거, 텍스트 통합하기
            text_data = df[col_name].dropna().astype(str).tolist()
            text = " ".join(text_data)
            
            # 명사 추출, 빈도수 계산
            okt = Okt()
            words = okt.nouns(text)
            counter = Counter(words)
            st.success(f"분석결과 : ({len(text_data):,}개의 리뷰와 {len(words):,}개의 단어가 있습니다)")

            # 막대 그래프 시각화
            if show_bar_chart:
                st.subheader("빈도수 그래프")
                #bar_word_count에서 설정한 갯수만큼 추출
                top_words = counter.most_common(bar_word_count)
                
                #단어, 빈도수 분리
                if top_words:
                    words_list, counts = zip(*top_words)
                    
                    #상위 단어가 위로 오도록
                    fig, ax = plt.subplots(figsize=(10, 6))
                    ax.barh(words_list[::-1], counts[::-1])
                    ax.set_xlabel("빈도수")
                    # 그래프 출력 plt.show() 대체
                    st.pyplot(fig)

            # 워드클라우드
            if show_wordcloud:
                st.subheader("워드클라우드")

                # 객체 생성
                wc = WordCloud(
                    font_path=font_path,
                    background_color="white",
                    max_words=wc_word_count,
                    width=800, 
                    height=600
                )
                # 이미지 생성
                wc.generate_from_frequencies(counter)
                
                # natplotlib으로 화면에 표시
                fig_wc, ax_wc = plt.subplots(figsize=(10, 8))
                ax_wc.imshow(wc, interpolation="bilinear")
                ax_wc.axis("off")
                st.pyplot(fig_wc)
                
        else:
            st.error(f"업로드한 파일에 '{col_name}' 컬럼이 존재하지 않습니다.")

# (__name__ = 이 파일) main 함수 호출
if __name__ == "__main__":
    main()
