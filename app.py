import time
import urllib.parse

import streamlit as st

st.set_page_config(page_title="나만의 시그니처 핏 찾기", page_icon="👗", layout="centered")

st.markdown(
    """
    <style>
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .stApp { background-color: #F9F8F6; }
    h1, h2, h3 { color: #2C3E50; }
    [data-testid="stImage"] img {
        border-radius: 16px;
        animation: fadeIn 0.9s ease-out;
    }
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 16px !important;
        animation: fadeIn 0.6s ease-out;
    }
    .stButton > button, .stLinkButton > a {
        border-radius: 999px !important;
    }
    button[kind="primary"] {
        background-color: #C96B4B !important;
        border-color: #C96B4B !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("나만의 시그니처 핏 찾기")
st.caption("AI 맞춤 스타일 취향 진단")

st.image(
    "https://images.unsplash.com/photo-1668952135120-7d997b1b3778"
    "?fm=jpg&q=80&w=1200&auto=format&fit=crop&ixlib=rb-4.1.0",
    use_container_width=True,
)
st.caption("8가지 질문에 답하면, 당신만의 시그니처 핏을 찾아드려요 ✨")

progress_placeholder = st.empty()

st.divider()

# Q1. 성별
with st.container(border=True):
    st.subheader("🙋 Q1. 성별을 알려주세요")
    gender = st.radio(
        label="성별 선택",
        options=["여성", "남성", "상관없음"],
        index=None,
        horizontal=True,
        label_visibility="collapsed",
    )

# Q2. 연령대
with st.container(border=True):
    st.subheader("🎂 Q2. 연령대를 알려주세요")
    age_group = st.selectbox(
        label="연령대 선택",
        options=[
            "10대",
            "20대 초반",
            "20대 후반",
            "30대 초반",
            "30대 후반",
            "40대 초반",
            "40대 후반",
            "50대 이상",
        ],
        index=None,
        placeholder="연령대를 선택해주세요",
        label_visibility="collapsed",
    )

# Q3. 체형
with st.container(border=True):
    st.subheader("📐 Q3. 체형에 가장 가까운 것을 선택해주세요")
    body_type = st.radio(
        label="체형 선택",
        options=["슬림한 편", "보통 체형", "볼륨감 있는 체형"],
        index=None,
        horizontal=True,
        label_visibility="collapsed",
    )

# Q4. 선호하는 실루엣과 핏
with st.container(border=True):
    st.subheader("🧥 Q4. 선호하는 실루엣과 핏은 무엇인가요?")
    silhouette = st.radio(
        label="실루엣과 핏 선택",
        options=[
            "여유롭고 편안한 오버사이즈 핏",
            "단정하고 바디라인을 살려주는 슬림/정장 핏",
            "자연스럽게 떨어지는 레귤러/스트레이트 핏",
            "짧고 간결한 크롭 기장 핏",
            "넉넉하고 볼륨감 있는 와이드/벌룬 핏",
        ],
        index=None,
        label_visibility="collapsed",
    )

# Q5. 가장 중요하게 생각하는 패션 디테일
with st.container(border=True):
    st.subheader("✨ Q5. 가장 중요하게 생각하는 패션 디테일은 무엇인가요?")
    detail = st.radio(
        label="패션 디테일 선택",
        options=[
            "미니멀리즘 (군더더기 없는 심플함)",
            "클래식 & 테일러드 (각이 잡힌 고급스러운 마감)",
            "캐주얼 & 유니크 (소재나 스티치 등의 독특한 포인트)",
            "로맨틱 & 페미닌 (러플, 레이스 등 여성스러운 디테일)",
            "스포티 & 액티브 (기능성 소재, 로고 포인트, 스트리트 무드)",
        ],
        index=None,
        label_visibility="collapsed",
    )

# Q6. 선호하는 메인 컬러 계열
COLOR_SWATCH_HEX = {
    "뉴트럴 어스 (베이지, 카키, 브라운 계열)": ["#C8A27C", "#8B7355", "#5C4033"],
    "모노크롬 (블랙, 화이트, 그레이 계열)": ["#1A1A1A", "#FFFFFF", "#9B9B9B"],
    "소프트 파스텔 (은은한 톤온톤 계열)": ["#F7D9D9", "#D9E8F5", "#FDF0DC"],
    "딥 볼드 (네이비, 와인 등 깊은 색감)": ["#1B2A4A", "#5C1A2E"],
    "비비드 포인트 (레드, 옐로우 등 선명한 원색)": ["#E63946", "#F4A300"],
    "라이트 뉴트럴 (화이트, 아이보리, 그레이지 톤)": ["#FFFFFF", "#F5F0E6", "#D9D2C5"],
}
with st.container(border=True):
    st.subheader("🎨 Q6. 선호하는 메인 컬러 계열은 무엇인가요?")
    color = st.selectbox(
        label="메인 컬러 계열 선택",
        options=list(COLOR_SWATCH_HEX.keys()),
        index=None,
        placeholder="컬러 계열을 선택해주세요",
        label_visibility="collapsed",
    )
    if color:
        swatches = "".join(
            f'<span style="display:inline-block;width:28px;height:28px;'
            f'border-radius:50%;margin-right:8px;border:1px solid #ddd;'
            f'background:{hex_code};"></span>'
            for hex_code in COLOR_SWATCH_HEX[color]
        )
        st.markdown(swatches, unsafe_allow_html=True)

# Q7. 주로 입는 상황(TPO)
with st.container(border=True):
    st.subheader("📍 Q7. 주로 어떤 상황에서 입을 옷을 찾으시나요?")
    occasion = st.radio(
        label="착용 상황 선택",
        options=[
            "데일리 캐주얼",
            "오피스/출근룩",
            "데이트·모임",
            "특별한 행사 (웨딩·파티)",
            "여행/아웃도어",
            "운동/액티비티",
        ],
        index=None,
        label_visibility="collapsed",
    )

# Q8. 예상 예산대
with st.container(border=True):
    st.subheader("💰 Q8. 예상 예산대를 알려주세요")
    budget = st.selectbox(
        label="예산대 선택",
        options=["10만원 이하", "10~30만원", "30~50만원", "50만원 이상"],
        index=None,
        placeholder="예산대를 선택해주세요",
        label_visibility="collapsed",
    )

answers = [gender, age_group, body_type, silhouette, detail, color, occasion, budget]
answered_count = sum(1 for a in answers if a)
progress_placeholder.progress(
    answered_count / len(answers), text=f"진단 진행률 {answered_count}/{len(answers)} 🧵"
)

st.divider()


# ---- 결과 이미지 갤러리 (무료 스톡 이미지 고정 링크, 검색 API 미사용) ----
# 컬러 계열별로 미리 골라 둔 패션 매거진 스타일 사진 5장을 매핑해 둔다.
# (실루엣/디테일은 프롬프트와 코멘트 문구에 반영되고, 사진은 컬러 계열 기준으로 매칭된다.)

SILHOUETTE_KEYS = {
    "여유롭고 편안한 오버사이즈 핏": "oversized",
    "단정하고 바디라인을 살려주는 슬림/정장 핏": "slim",
    "자연스럽게 떨어지는 레귤러/스트레이트 핏": "regular",
    "짧고 간결한 크롭 기장 핏": "crop",
    "넉넉하고 볼륨감 있는 와이드/벌룬 핏": "wide",
}

DETAIL_KEYS = {
    "미니멀리즘 (군더더기 없는 심플함)": "minimal",
    "클래식 & 테일러드 (각이 잡힌 고급스러운 마감)": "classic",
    "캐주얼 & 유니크 (소재나 스티치 등의 독특한 포인트)": "casual",
    "로맨틱 & 페미닌 (러플, 레이스 등 여성스러운 디테일)": "romantic",
    "스포티 & 액티브 (기능성 소재, 로고 포인트, 스트리트 무드)": "sporty",
}

COLOR_KEYS = {
    "뉴트럴 어스 (베이지, 카키, 브라운 계열)": "earth",
    "모노크롬 (블랙, 화이트, 그레이 계열)": "mono",
    "소프트 파스텔 (은은한 톤온톤 계열)": "pastel",
    "딥 볼드 (네이비, 와인 등 깊은 색감)": "bold",
    "비비드 포인트 (레드, 옐로우 등 선명한 원색)": "vivid",
    "라이트 뉴트럴 (화이트, 아이보리, 그레이지 톤)": "light",
}

_UNSPLASH = "https://images.unsplash.com/photo-{id}?fm=jpg&q=75&w=900&auto=format&fit=crop&ixlib=rb-4.1.0{ixid}"

# 컬러 계열(key) -> 미리 정의된 패션 매거진 스타일 사진 목록(Mapping Object)
PHOTO_GALLERY = {
    "earth": [
        _UNSPLASH.format(id="1668952135120-7d997b1b3778", ixid=""),
        _UNSPLASH.format(id="1681860317538-12f5b396c1bf", ixid=""),
        _UNSPLASH.format(id="1617733401065-c7bdf0b33417", ixid=""),
        _UNSPLASH.format(id="1779406167603-d0afe0a4cdd7", ixid=""),
        _UNSPLASH.format(id="1617875827710-9afb3fbee447", ixid=""),
    ],
    "mono": [
        _UNSPLASH.format(id="1603189343302-e603f7add05a", ixid=""),
        _UNSPLASH.format(id="1552393700-42696fb89bfa", ixid=""),
        _UNSPLASH.format(id="1553614186-5fc725ac6396", ixid=""),
        _UNSPLASH.format(id="1504903953708-1a3669833567", ixid=""),
        _UNSPLASH.format(id="1657815929003-b97cc426cb3d", ixid=""),
    ],
    "pastel": [
        _UNSPLASH.format(id="1775701662950-746e52b943e5", ixid="&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8cGFzdGVsJTIwZmFzaGlvbiUyMGVkaXRvcmlhbCUyMG91dGZpdHxlbnwwfHwwfHx8MA%3D%3D"),
        _UNSPLASH.format(id="1660407135986-e095cfaae04b", ixid="&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8cGFzdGVsJTIwZmFzaGlvbiUyMGVkaXRvcmlhbCUyMG91dGZpdHxlbnwwfHwwfHx8MA%3D%3D"),
        _UNSPLASH.format(id="1660407216718-9b5573b65adb", ixid="&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NHx8cGFzdGVsJTIwZmFzaGlvbiUyMGVkaXRvcmlhbCUyMG91dGZpdHxlbnwwfHwwfHx8MA%3D%3D"),
        _UNSPLASH.format(id="1571605570827-d1bf28fadc76", ixid="&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8cGFzdGVsJTIwZmFzaGlvbiUyMGVkaXRvcmlhbCUyMG91dGZpdHxlbnwwfHwwfHx8MA%3D%3D"),
        _UNSPLASH.format(id="1610643560547-b1af75503f7c", ixid="&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTR8fHBhc3RlbCUyMGZhc2hpb24lMjBlZGl0b3JpYWwlMjBvdXRmaXR8ZW58MHx8MHx8fDA%3D"),
    ],
    "bold": [
        _UNSPLASH.format(id="1580478491436-fd6a937acc9e", ixid="&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8bmF2eSUyMGJ1cmd1bmR5JTIwZmFzaGlvbiUyMGVkaXRvcmlhbCUyMGNvYXR8ZW58MHx8MHx8fDA%3D"),
        _UNSPLASH.format(id="1632862504328-2911b280eaf6", ixid="&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8bmF2eSUyMGJ1cmd1bmR5JTIwZmFzaGlvbiUyMGVkaXRvcmlhbCUyMGNvYXR8ZW58MHx8MHx8fDA%3D"),
        _UNSPLASH.format(id="1610362506361-4ce9cc842583", ixid="&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTZ8fG5hdnklMjBidXJndW5keSUyMGZhc2hpb24lMjBlZGl0b3JpYWwlMjBjb2F0fGVufDB8fDB8fHww"),
        _UNSPLASH.format(id="1739808914849-01ba195c4f93", ixid="&ixid=M3wxMjA3fDB8MHxzZWFyY2h8OHx8bmF2eSUyMGNvYXQlMjBmYXNoaW9uJTIwZWRpdG9yaWFsJTIwbW9kZWx8ZW58MHx8MHx8fDA%3D"),
        _UNSPLASH.format(id="1550872199-63f4382fe925", ixid="&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8bmF2eSUyMGJ1cmd1bmR5JTIwZmFzaGlvbiUyMGVkaXRvcmlhbCUyMGNvYXR8ZW58MHx8MHx8fDA%3D"),
    ],
    "vivid": [
        _UNSPLASH.format(id="1767570279727-d94ee690b036", ixid="&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8dml2aWQlMjByZWQlMjB5ZWxsb3clMjBmYXNoaW9uJTIwZWRpdG9yaWFsfGVufDB8fDB8fHww"),
        _UNSPLASH.format(id="1647314962114-f5df86bec1f2", ixid="&ixid=M3wxMjA3fDB8MHxzZWFyY2h8N3x8dml2aWQlMjByZWQlMjB5ZWxsb3clMjBmYXNoaW9uJTIwZWRpdG9yaWFsfGVufDB8fDB8fHww"),
        _UNSPLASH.format(id="1642448864113-aeff7150f3b2", ixid="&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTB8fHZpdmlkJTIwcmVkJTIweWVsbG93JTIwZmFzaGlvbiUyMGVkaXRvcmlhbHxlbnwwfHwwfHx8MA%3D%3D"),
        _UNSPLASH.format(id="1653152703557-b87c17954ed0", ixid="&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MjB8fHZpdmlkJTIwcmVkJTIweWVsbG93JTIwZmFzaGlvbiUyMGVkaXRvcmlhbHxlbnwwfHwwfHx8MA%3D%3D"),
        _UNSPLASH.format(id="1718227696369-7a4aaec5316e", ixid="&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTl8fHZpdmlkJTIwcmVkJTIweWVsbG93JTIwZmFzaGlvbiUyMGVkaXRvcmlhbHxlbnwwfHwwfHx8MA%3D%3D"),
    ],
    "light": [
        _UNSPLASH.format(id="1754680837239-cfe387461287", ixid="&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8YWxsJTIwd2hpdGUlMjBpdm9yeSUyMGZhc2hpb24lMjBlZGl0b3JpYWwlMjBtaW5pbWFsfGVufDB8fDB8fHww"),
        _UNSPLASH.format(id="1745962978498-13fac949e357", ixid="&ixid=M3wxMjA3fDB8MHxzZWFyY2h8N3x8YWxsJTIwd2hpdGUlMjBpdm9yeSUyMGZhc2hpb24lMjBlZGl0b3JpYWwlMjBtaW5pbWFsfGVufDB8fDB8fHww"),
        _UNSPLASH.format(id="1779153996944-5b87e1ac3845", ixid="&ixid=M3wxMjA3fDB8MHxzZWFyY2h8OHx8YWxsJTIwd2hpdGUlMjBpdm9yeSUyMGZhc2hpb24lMjBlZGl0b3JpYWwlMjBtaW5pbWFsfGVufDB8fDB8fHww"),
        _UNSPLASH.format(id="1665029511896-fb9ed115a800", ixid="&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTF8fGFsbCUyMHdoaXRlJTIwaXZvcnklMjBmYXNoaW9uJTIwZWRpdG9yaWFsJTIwbWluaW1hbHxlbnwwfHwwfHx8MA%3D%3D"),
        _UNSPLASH.format(id="1621036382228-d728f0d09e33", ixid="&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTZ8fGFsbCUyMHdoaXRlJTIwaXZvcnklMjBmYXNoaW9uJTIwZWRpdG9yaWFsJTIwbWluaW1hbHxlbnwwfHwwfHx8MA%3D%3D"),
    ],
}


# 남성 선택 시 노출할 남성 모델 사진 갤러리 (컬러 계열별, 여성 갤러리와 동일한 키 구조)
MALE_PHOTO_GALLERY = {
    "earth": [
        _UNSPLASH.format(id="1619603364937-8d7af41ef206", ixid=""),
        _UNSPLASH.format(id="1619603364904-c0498317e145", ixid=""),
        _UNSPLASH.format(id="1614594955631-e977926ea681", ixid=""),
        _UNSPLASH.format(id="1719418271955-79273259772d", ixid=""),
    ],
    "mono": [
        _UNSPLASH.format(id="1608235882291-02e3b888f3ee", ixid=""),
        _UNSPLASH.format(id="1610419923009-f0a50c304f10", ixid=""),
        _UNSPLASH.format(id="1634275964869-45a16e0afcad", ixid=""),
        _UNSPLASH.format(id="1620053508057-67807dd6b250", ixid=""),
    ],
    "pastel": [
        _UNSPLASH.format(id="1720276679055-2a72007237bc", ixid=""),
        _UNSPLASH.format(id="1664543030885-886de74e826b", ixid=""),
        _UNSPLASH.format(id="1720276661098-d57981e5536e", ixid=""),
        _UNSPLASH.format(id="1562070304-ed6c65e1d838", ixid=""),
    ],
    "bold": [
        _UNSPLASH.format(id="1754051410158-4af2044cd87e", ixid=""),
        _UNSPLASH.format(id="1562844747-5e44876b58c0", ixid=""),
        _UNSPLASH.format(id="1544440175-99557be975a0", ixid=""),
        _UNSPLASH.format(id="1667829071175-4997f09843cc", ixid=""),
    ],
    "vivid": [
        _UNSPLASH.format(id="1761662826131-5b78816de0be", ixid=""),
        _UNSPLASH.format(id="1584190810197-75f679c058fb", ixid=""),
        _UNSPLASH.format(id="1762743412345-a31d94cd5a88", ixid=""),
        _UNSPLASH.format(id="1601027847853-ea31bd3d5787", ixid=""),
    ],
    "light": [
        _UNSPLASH.format(id="1645786183846-571b5236d7f4", ixid=""),
        _UNSPLASH.format(id="1693071433903-41260e7f07e2", ixid=""),
        _UNSPLASH.format(id="1755105259798-f42f86c16f61", ixid=""),
        _UNSPLASH.format(id="1693071093573-9e8e342aebeb", ixid=""),
    ],
}


def get_look_gallery(gender_label, color_label):
    color_key = COLOR_KEYS.get(color_label, "earth")
    if gender_label == "남성":
        return MALE_PHOTO_GALLERY.get(color_key, MALE_PHOTO_GALLERY["earth"])
    return PHOTO_GALLERY.get(color_key, PHOTO_GALLERY["earth"])


# ---- 구매 사이트 안내 (검색 API 미사용, 쇼핑몰 검색 페이지로 바로 연결) ----

SIL_QUERY = {
    "oversized": "오버사이즈",
    "slim": "슬림 정장",
    "regular": "레귤러 스트레이트",
    "crop": "크롭",
    "wide": "와이드 벌룬",
}
DET_QUERY = {
    "minimal": "미니멀",
    "classic": "클래식 테일러드",
    "casual": "캐주얼 유니크",
    "romantic": "로맨틱 페미닌",
    "sporty": "스포티 액티브",
}
COL_QUERY = {
    "earth": "베이지 카키 브라운",
    "mono": "블랙 화이트 그레이",
    "pastel": "파스텔",
    "bold": "네이비 와인",
    "vivid": "비비드 레드 옐로우",
    "light": "화이트 아이보리",
}


def build_shopping_query(silhouette_label, detail_label, color_label, gender_label, occasion_label):
    sil = SIL_QUERY.get(SILHOUETTE_KEYS.get(silhouette_label), "")
    det = DET_QUERY.get(DETAIL_KEYS.get(detail_label), "")
    col = COL_QUERY.get(COLOR_KEYS.get(color_label), "")
    gender_term = "" if gender_label == "상관없음" else gender_label
    return f"{gender_term} {col} {det} {sil} {occasion_label} 코디".strip()


def build_curated_shop_query(silhouette_label, detail_label, gender_label):
    # SSF샵/W컨셉처럼 검색엔진이 단순한 편집몰은 키워드가 많으면(색상·상황·"코디" 포함)
    # 결과가 0건으로 나오는 경우가 있어, 성별+실루엣+디테일 위주의 짧은 쿼리를 별도로 사용한다.
    sil = SIL_QUERY.get(SILHOUETTE_KEYS.get(silhouette_label), "")
    det = DET_QUERY.get(DETAIL_KEYS.get(detail_label), "")
    gender_term = "" if gender_label == "상관없음" else gender_label
    return f"{gender_term} {sil} {det}".strip()


def get_shopping_links(silhouette_label, detail_label, color_label, gender_label, occasion_label):
    query = build_shopping_query(silhouette_label, detail_label, color_label, gender_label, occasion_label)
    curated_query = build_curated_shop_query(silhouette_label, detail_label, gender_label)
    encoded = urllib.parse.quote(query)
    curated_encoded = urllib.parse.quote(curated_query)
    return [
        ("무신사에서 보기", f"https://www.musinsa.com/search/musinsa/integration?q={encoded}"),
        ("SSF샵에서 보기", f"https://www.ssfshop.com/search/result?keyword={curated_encoded}"),
        ("W컨셉에서 보기", f"https://display.wconcept.co.kr/search?keyword={curated_encoded}"),
        ("네이버 쇼핑에서 보기", f"https://search.shopping.naver.com/search/all?query={encoded}"),
        ("구글에서 더 찾아보기", f"https://www.google.com/search?q={urllib.parse.quote(query + ' 구매')}"),
    ]


TONE_AND_MANNER = "모던한, 감성적인, 신뢰감 있는, 정돈된, 프리미엄한"


def build_prompt():
    return (
        f"성별: {gender}\n"
        f"연령대: {age_group}\n"
        f"체형: {body_type}\n"
        f"실루엣과 핏: {silhouette}\n"
        f"패션 디테일: {detail}\n"
        f"메인 컬러 계열: {color}\n"
        f"주로 입는 상황: {occasion}\n"
        f"예상 예산대: {budget}\n"
        f"위 취향 조합에 어울리는 맞춤 의류 스타일링 이미지와, "
        f"스타일리스트의 추천 코멘트를 작성해줘.\n"
        f"톤앤매너: {TONE_AND_MANNER} 분위기를 반영해줘."
    )


def build_image_prompt():
    return (
        f"패션 룩북 스타일의 고화질 스타일링 이미지를 생성해줘.\n"
        f"모델 특성: {gender}, {age_group}, {body_type}\n"
        f"실루엣과 핏: {silhouette}\n"
        f"패션 디테일: {detail}\n"
        f"메인 컬러 계열: {color}\n"
        f"촬영 콘셉트: {occasion}에 어울리는 무드\n"
        f"톤앤매너: {TONE_AND_MANNER} 분위기가 느껴지는 스튜디오 조명과 "
        f"미니멀한 배경으로 표현해줘."
    )


# 결과 보기 버튼
if st.button("결과 보기", use_container_width=True, type="primary"):
    if not all(answers):
        st.warning("모든 항목을 선택해주세요.")
    else:
        image_prompt = build_image_prompt()

        with st.spinner("이미지를 생성하는 중입니다..."):
            time.sleep(1.5)  # TODO: 실제 이미지 생성 API 연동 전까지의 임시 로딩 표시
            gallery = get_look_gallery(gender, color)

        st.balloons()
        st.subheader("🎉 당신을 위한 매칭 스타일")
        st.caption(
            f"{gender} · {age_group} · {body_type} 취향에 맞춘 "
            f"{silhouette.split(' ')[-1]} · {detail.split(' ')[0]} 스타일링입니다."
        )
        cols = st.columns(3)
        for idx, url in enumerate(gallery):
            with cols[idx % 3]:
                st.image(url, use_container_width=True)

        st.divider()

        st.subheader("🛍️ 이 스타일, 여기서 구매해보세요")
        st.caption("선택하신 취향 키워드로 각 쇼핑몰의 검색 결과 페이지로 바로 연결됩니다.")
        shopping_links = get_shopping_links(silhouette, detail, color, gender, occasion)
        shop_cols = st.columns(3)
        for idx, (label, url) in enumerate(shopping_links):
            with shop_cols[idx % 3]:
                st.link_button(label, url, use_container_width=True)

        st.divider()

        st.code(image_prompt, language="text")

        prompt = build_prompt()
        st.code(prompt, language="text")
