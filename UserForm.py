import streamlit as st

with st.form(key="form"):
    name = st.text_input(label="이름")
    age = st.text_input(label="나이")
    submit = st.form_submit_button(label="제출")
    
    if submit:
        # 브라우저 화면에 출력
        st.write(f"이름: {name}")
        st.write(f"나이: {age}")
        
        # 터미널 창에 출력
        print("제출 되었습니다.")