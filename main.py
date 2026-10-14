
import streamlit as st
import html

# ==========================================
# 1. 페이지 설정
# ==========================================
st.set_page_config(
    page_title="MBTI 단짝 포켓몬 찾기",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ==========================================
# 2. 따뜻한 크림 · 노란색 디자인
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');

:root {
    --cream: #fff9e9;
    --yellow: #ffdf78;
    --brown: #493b2c;
}

.stApp {
    background: var(--cream);
    color: var(--brown);
}

header[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 850px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3, p, div, button {
    color: var(--brown);
}

.hero {
    text-align: center;
    padding: 22px 8px 28px;
}

.hero-badge {
    display: inline-block;
    background: var(--yellow);
    border-radius: 30px;
    padding: 7px 18px;
    font-size: 15px;
    font-weight: bold;
    margin-bottom: 16px;
}

.hero-title {
    font-family: 'Jua', sans-serif;
    font-size: clamp(34px, 7vw, 54px);
    font-weight: 900;
    line-height: 1.3;
    letter-spacing: -1px;
    margin: 0;
}

.hero-subtitle {
    font-size: 17px;
    color: #85745f;
    margin-top: 14px;
}

.section-heading {
    font-size: 25px;
    font-weight: 900;
    margin: 15px 0 5px;
}

.section-caption {
    color: #85745f;
    font-size: 15px;
    margin-bottom: 18px;
}

.stButton > button {
    background: #fffdf7;
    border: 2px solid #f0e6d3;
    border-radius: 15px;
    min-height: 54px;
    width: 100%;
    font-size: 18px;
    font-weight: 800;
    transition: all .2s ease;
}

.stButton > button:hover {
    background: #fff0b9;
    border-color: #e7bd4d;
    transform: translateY(-2px);
}

.result-card {
    background: linear-gradient(180deg, #fff0b7, #fffdf5);
    border: 2px solid #f0d477;
    border-radius: 27px;
    padding: 25px 20px;
    text-align: center;
    margin-top: 18px;
    animation: popin .55s ease-out;
}

@keyframes popin {
    0% { opacity: 0; transform: scale(.94) translateY(12px); }
    70% { transform: scale(1.015); }
    100% { opacity: 1; transform: scale(1) translateY(0); }
}

.result-label {
    display: inline-block;
    background: white;
    border-radius: 30px;
    padding: 6px 16px;
    font-size: 15px;
    font-weight: bold;
}

.pokemon-image {
    display: block;
    width: min(100%, 260px);
    height: 230px;
    object-fit: contain;
    margin: 10px auto;
    filter: drop-shadow(0 9px 5px rgba(100, 70, 20, .12));
}

.pokemon-name {
    font-family: 'Jua', sans-serif;
    font-size: clamp(30px, 6vw, 42px);
    font-weight: 900;
    margin: 0;
}

.pokemon-en {
    color: #85745f;
    font-size: 17px;
    margin-top: 2px;
}

.type-pill {
    display: inline-block;
    margin: 10px 4px 5px;
    background: white;
    border: 1px solid #edd48c;
    border-radius: 22px;
    padding: 5px 14px;
    font-weight: bold;
    font-size: 15px;
}

.info-card {
    background: white;
    border-radius: 18px;
    padding: 19px;
    text-align: left;
    margin-top: 15px;
    border: 1px solid #f2e8d5;
}

.info-title {
    font-size: 20px;
    font-weight: 900;
    margin-bottom: 7px;
}

.info-text {
    font-size: 16px;
    line-height: 1.85;
    color: #655644;
    margin: 0;
}

.match-card {
    background: #ffe8df;
    border-color: #f4c9ba;
}

.match-type {
    display: inline-block;
    background: white;
    border: 2px solid #f2c1b2;
    border-radius: 12px;
    padding: 4px 15px;
    font-size: 23px;
    font-weight: 900;
    margin: 5px 0 10px;
}

.celebration {
    text-align: center;
    padding: 15px 5px 5px;
    font-size: 23px;
    font-weight: 900;
    animation: sparkle 1s ease-in-out infinite alternate;
}

@keyframes sparkle {
    from { transform: scale(1); }
    to { transform: scale(1.035); }
}

.footer {
    text-align: center;
    color: #9b8b75;
    font-size: 13px;
    padding: 28px 5px 5px;
}

div[data-testid="stAlert"] {
    border-radius: 14px;
}

@media (max-width: 600px) {
    .block-container {
        padding: 1rem 1rem 2rem;
    }

    .stButton > button {
        min-height: 48px;
        font-size: 15px;
    }

    .result-card {
        padding: 20px 12px;
    }

    .pokemon-image {
        height: 200px;
    }
}

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: .01ms !important;
        transition-duration: .01ms !important;
    }
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. 포켓몬 데이터
# 이미지 출처: PokeAPI 공개 스프라이트 저장소
# ==========================================
POKEMON = {
    "INTJ": {
        "ko": "뮤츠",
        "en": "Mewtwo",
        "id": 150,
        "types": ["에스퍼"],
        "features": "뛰어난 지능과 강력한 초능력을 가진 전설의 포켓몬.",
        "reason": "깊이 생각하고 큰 그림을 그리는 전략가와 닮았어요. "
                  "혼자 분석하며 자신만의 목표를 향해 나아가는 모습이 잘 어울려요.",
        "mate": "ENFP",
        "mate_reason": "차분한 계획과 자유로운 상상력이 만나 새로운 가능성을 발견할 수 있어요."
    },
    "INTP": {
        "ko": "메타몽",
        "en": "Ditto",
        "id": 132,
        "types": ["노말"],
        "features": "다른 포켓몬의 모습으로 변신할 수 있는 신비로운 포켓몬.",
        "reason": "호기심이 많고 다양한 가능성을 탐구하는 모습이 닮았어요. "
                  "독특한 관점으로 문제를 바라보는 창의적인 성격과 잘 어울려요.",
        "mate": "ENTJ",
        "mate_reason": "깊이 있는 분석과 과감한 추진력이 서로에게 좋은 자극이 될 수 있어요."
    },
    "ENTJ": {
        "ko": "리자몽",
        "en": "Charizard",
        "id": 6,
        "types": ["불꽃", "비행"],
        "features": "하늘을 날며 강력한 불꽃을 사용하는 포켓몬.",
        "reason": "목표를 정하고 힘차게 나아가는 리더의 모습이 닮았어요. "
                  "어려운 상황에서도 해결책을 찾으려는 자신감이 잘 어울려요.",
        "mate": "INTP",
        "mate_reason": "결단력과 분석력이 만나 서로의 생각을 넓혀 줄 수 있어요."
    },
    "ENTP": {
        "ko": "루카리오",
        "en": "Lucario",
        "id": 448,
        "types": ["격투", "강철"],
        "features": "파동을 감지하고 상대의 마음까지 읽을 수 있는 포켓몬.",
        "reason": "새로운 방법을 탐구하고 틀에 얽매이지 않는 모습이 닮았어요. "
                  "재미있는 아이디어를 실제 도전으로 이어 가는 성격과 잘 어울려요.",
        "mate": "INFJ",
        "mate_reason": "톡톡 튀는 아이디어와 깊이 있는 통찰이 만나 서로의 시야를 넓힐 수 있어요."
    },
    "INFJ": {
        "ko": "가디안",
        "en": "Gardevoir",
        "id": 282,
        "types": ["에스퍼", "페어리"],
        "features": "소중한 사람을 지키려는 마음이 강한 포켓몬.",
        "reason": "다른 사람의 마음을 세심하게 살피는 모습이 닮았어요. "
                  "의미 있는 관계를 소중히 여기고 자신이 믿는 가치를 지키는 성격과 잘 어울려요.",
        "mate": "ENTP",
        "mate_reason": "깊이 있는 생각과 새로운 발상이 만나 색다른 관점을 발견할 수 있어요."
    },
    "INFP": {
        "ko": "이브이",
        "en": "Eevee",
        "id": 133,
        "types": ["노말"],
        "features": "다양한 환경에 따라 여러 모습으로 진화할 수 있는 포켓몬.",
        "reason": "풍부한 상상력과 특별한 가능성을 지닌 모습이 닮았어요. "
                  "자신만의 가치관을 소중히 여기고 여러 방향으로 성장하는 모습이 잘 어울려요.",
        "mate": "ENFJ",
        "mate_reason": "섬세한 감성과 따뜻한 응원이 만나 서로를 이해하는 데 도움이 될 수 있어요."
    },
    "ENFJ": {
        "ko": "푸린",
        "en": "Jigglypuff",
        "id": 39,
        "types": ["노말", "페어리"],
        "features": "노래를 부르는 것을 좋아하는 동글동글한 포켓몬.",
        "reason": "사람들에게 즐거움을 전하고 함께하는 분위기를 소중히 여기는 모습이 닮았어요. "
                  "주변 사람을 격려하는 따뜻한 매력과 잘 어울려요.",
        "mate": "INFP",
        "mate_reason": "따뜻하게 이끄는 힘과 진솔한 감성이 만나 좋은 조화를 이룰 수 있어요."
    },
    "ENFP": {
        "ko": "피카츄",
        "en": "Pikachu",
        "id": 25,
        "types": ["전기"],
        "features": "볼의 전기 주머니에 전기를 모으는 활기찬 포켓몬.",
        "reason": "밝은 에너지와 호기심으로 주변을 즐겁게 만드는 모습이 닮았어요. "
                  "새로운 경험을 좋아하고 친구들과 추억을 나누는 성격과 잘 어울려요.",
        "mate": "INTJ",
        "mate_reason": "자유로운 상상력과 차분한 계획이 만나 아이디어를 발전시킬 수 있어요."
    },
    "ISTJ": {
        "ko": "꼬부기",
        "en": "Squirtle",
        "id": 7,
        "types": ["물"],
        "features": "등껍질을 이용해 몸을 보호하는 침착한 포켓몬.",
        "reason": "차근차근 자신의 일을 해내는 믿음직한 모습이 닮았어요. "
                  "책임감을 가지고 꾸준히 노력하는 성격과 잘 어울려요.",
        "mate": "ESFP",
        "mate_reason": "안정적인 계획과 즐거운 즉흥성이 만나 일상에 균형을 더할 수 있어요."
    },
    "ISFJ": {
        "ko": "해피너스",
        "en": "Blissey",
        "id": 242,
        "types": ["노말"],
        "features": "상냥한 마음으로 아픈 포켓몬을 돌보는 포켓몬.",
        "reason": "주변을 세심하게 살피고 소중한 사람을 챙기는 모습이 닮았어요. "
                  "다른 사람에게 편안함을 주는 따뜻한 성격과 잘 어울려요.",
        "mate": "ESFP",
        "mate_reason": "세심한 배려와 밝은 에너지가 즐거운 시간을 만드는 데 도움이 될 수 있어요."
    },
    "ESTJ": {
        "ko": "윈디",
        "en": "Arcanine",
        "id": 59,
        "types": ["불꽃"],
        "features": "용맹하고 빠르게 달리는 늠름한 포켓몬.",
        "reason": "책임감이 강하고 든든하게 주변을 이끄는 모습이 닮았어요. "
                  "목표를 정하고 계획적으로 실행하는 성격과 잘 어울려요.",
        "mate": "ISFP",
        "mate_reason": "추진력과 유연한 감성이 만나 서로의 장점을 배울 수 있어요."
    },
    "ESFJ": {
        "ko": "파치리스",
        "en": "Pachirisu",
        "id": 417,
        "types": ["전기"],
        "features": "볼에 전기를 모으는 다람쥐를 닮은 포켓몬.",
        "reason": "친근한 매력으로 주변 사람들과 잘 어울리는 모습이 닮았어요. "
                  "서로 챙겨 주고 함께 즐거움을 나누는 성격과 잘 어울려요.",
        "mate": "ISFP",
        "mate_reason": "다정한 소통과 섬세한 감각이 편안한 관계를 만드는 데 도움이 될 수 있어요."
    },
    "ISTP": {
        "ko": "메타그로스",
        "en": "Metagross",
        "id": 376,
        "types": ["강철", "에스퍼"],
        "features": "네 개의 다리와 뛰어난 계산 능력을 지닌 포켓몬.",
        "reason": "복잡한 문제를 침착하게 분석하는 모습이 닮았어요. "
                  "직접 원인을 찾아 해결하려는 실용적인 성격과 잘 어울려요.",
        "mate": "ESTP",
        "mate_reason": "차분한 문제 해결 능력과 과감한 행동력이 좋은 팀이 될 수 있어요."
    },
    "ISFP": {
        "ko": "치코리타",
        "en": "Chikorita",
        "id": 152,
        "types": ["풀"],
        "features": "머리의 잎으로 주변의 따뜻한 기운을 느끼는 포켓몬.",
        "reason": "부드럽고 자연스러운 매력으로 주변을 편안하게 하는 모습이 닮았어요. "
                  "자신만의 취향과 감성을 소중히 여기는 성격과 잘 어울려요.",
        "mate": "ESFJ",
        "mate_reason": "자유로운 감성과 다정한 관심이 편안한 관계를 만드는 데 도움이 될 수 있어요."
    },
    "ESTP": {
        "ko": "개굴닌자",
        "en": "Greninja",
        "id": 658,
        "types": ["물", "악"],
        "features": "민첩한 움직임으로 상대를 교란하는 닌자 포켓몬.",
        "reason": "빠르게 상황을 파악하고 행동으로 옮기는 모습이 닮았어요. "
                  "직접 경험하며 배우고 도전을 즐기는 성격과 잘 어울려요.",
        "mate": "ISTP",
        "mate_reason": "빠른 실행력과 침착한 문제 해결 능력이 함께 도전하는 데 도움이 될 수 있어요."
    },
    "ESFP": {
        "ko": "마릴",
        "en": "Marill",
        "id": 183,
        "types": ["물", "페어리"],
        "features": "물에 뜨는 꼬리를 이용해 헤엄치는 귀여운 포켓몬.",
        "reason": "밝고 친근한 에너지로 즐거움을 전하는 모습이 닮았어요. "
                  "친구들과 지금 이 순간을 즐기며 추억을 만드는 성격과 잘 어울려요.",
        "mate": "ISTJ",
        "mate_reason": "즐거움을 찾아 나서는 에너지와 든든한 안정감이 서로를 보완할 수 있어요."
    },
}

# ==========================================
# 4. 세션 상태
# ==========================================
if "selected_mbti" not in st.session_state:
    st.session_state.selected_mbti = None

if "just_found" not in st.session_state:
    st.session_state.just_found = False

# ==========================================
# 5. 제목
# ==========================================
st.markdown("""
<div class="hero">
    <div class="hero-badge">🌼 나만의 포켓몬 찾기</div>
    <div class="hero-title">내 MBTI의<br>단짝 포켓몬은 누구?</div>
    <div class="hero-subtitle">
        내 성격과 닮은 포켓몬을 만나 보세요! ✨
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="section-heading">🎯 나의 MBTI를 골라 주세요</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="section-caption">16가지 유형 중 하나를 선택하면 결과가 나타나요.</div>',
    unsafe_allow_html=True,
)

# ==========================================
# 6. 16가지 MBTI 버튼
# ==========================================
mbti_types = [
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP",
]

columns = st.columns(4)

for index, mbti in enumerate(mbti_types):
    with columns[index % 4]:
        if st.button(
            mbti,
            key=f"mbti_{mbti}",
            use_container_width=True,
        ):
            st.session_state.selected_mbti = mbti
            st.session_state.just_found = True

# ==========================================
# 7. 결과 화면과 축하 효과
# ==========================================
selected = st.session_state.selected_mbti

if selected:
    pokemon = POKEMON[selected]

    # 새로운 결과를 찾았을 때만 축하 효과 재생
    if st.session_state.just_found:
        st.balloons()
        st.session_state.just_found = False

    st.markdown("""
    <div class="celebration">
        🎉 짝짝짝! 단짝 포켓몬을 찾았어요! 🎉
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        f'<div class="result-card">'
        f'<div class="result-label">✨ 나의 MBTI · {selected}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # 온라인 이미지 주소. 앱이 실행될 때 이미지를 불러옵니다.
    image_url = (
        "https://raw.githubusercontent.com/"
        "PokeAPI/sprites/master/sprites/pokemon/"
        f"{pokemon['id']}.png"
    )

    # 이미지를 표시하고, 실패하면 안내 메시지를 보여 줍니다.
    try:
        st.image(
            image_url,
            width=250,
            caption="포켓몬 스프라이트 · PokeAPI",
        )
    except Exception:
        st.info("이미지를 불러오지 못했어요. 인터넷 연결을 확인해 주세요.")

    st.markdown(
        f'<div style="text-align:center;">'
        f'<div class="pokemon-name">{html.escape(pokemon["ko"])}</div>'
        f'<div class="pokemon-en">({html.escape(pokemon["en"])})</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    type_html = "".join(
        f'<span class="type-pill">{html.escape(t)} 타입</span>'
        for t in pokemon["types"]
    )
    st.markdown(
        f'<div style="text-align:center;margin-bottom:15px;">'
        f'{type_html}</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div class="info-card">'
        f'<div class="info-title">📖 포켓몬 특징</div>'
        f'<p class="info-text">{html.escape(pokemon["features"])}</p>'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div class="info-card">'
        f'<div class="info-title">💛 너와 닮은 이유</div>'
        f'<p class="info-text">{html.escape(pokemon["reason"])}</p>'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div class="info-card match-card">'
        f'<div class="info-title">🤝 단짝이 되기 좋은 MBTI</div>'
        f'<div class="match-type">{html.escape(pokemon["mate"])}</div>'
        f'<p class="info-text">{html.escape(pokemon["mate_reason"])}</p>'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.write("")

    if st.button("🔄 다른 MBTI 다시 고르기", use_container_width=True):
        st.session_state.selected_mbti = None
        st.session_state.just_found = False
        st.rerun()

else:
    st.markdown("""
    <div class="info-card" style="text-align:center;margin-top:20px;">
        <div style="font-size:38px;">🥚</div>
        <div class="info-title">어떤 포켓몬이 기다리고 있을까요?</div>
        <p class="info-text">
            위에서 나의 MBTI를 선택해 보세요.<br>
            나만의 단짝 포켓몬이 나타날 거예요!
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="footer">
    🌟 포켓몬과 MBTI의 조합은 재미를 위한 창작 설정입니다.<br>
    이미지 출처: PokeAPI 공개 스프라이트 저장소<br>
    이미지가 표시되려면 인터넷 연결이 필요합니다.
</div>
""", unsafe_allow_html=True)
