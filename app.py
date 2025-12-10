import streamlit as st
import google.generativeai as genai
import json

# --- ページ設定 ---
st.set_page_config(
    page_title="Visual English",
    page_icon="🌏",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Wise風デザインの適用 (Custom CSS) ---
st.markdown("""
<style>
    /* 全体の背景色 */
    .stApp {
        background-color: #F2F5F7; /* Wiseのような薄いグレー背景 */
        font-family: 'Inter', sans-serif;
    }
    
    /* ヘッダーエリア（装飾用） */
    .header-bg {
        background-color: #163354; /* Wiseの深いネイビー */
        height: 250px;
        width: 100%;
        position: absolute;
        top: 0;
        left: 0;
        z-index: 0;
    }

    /* メインコンテナの調整 */
    .block-container {
        padding-top: 3rem;
        z-index: 1;
        position: relative;
    }

    /* 入力用カード（Wise風の白い浮きカード） */
    .input-card {
        background-color: white;
        padding: 40px;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin-bottom: 2rem;
    }

    /* タイトルテキスト */
    .main-title {
        color: white;
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        text-align: center;
    }
    .sub-title {
        color: #A8B4C2;
        text-align: center;
        margin-bottom: 2rem;
        font-size: 1.1rem;
    }

    /* ボタンのスタイル (Wise Green) */
    div.stButton > button {
        background-color: #2ED06E; /* Wiseのグリーン */
        color: white;
        border: none;
        padding: 12px 24px;
        font-size: 18px;
        font-weight: bold;
        border-radius: 8px;
        width: 100%;
        transition: background-color 0.3s;
    }
    div.stButton > button:hover {
        background-color: #26B05D; /* ホバー時の少し濃い緑 */
        color: white;
        border: none;
    }

    /* 結果表示エリアのスタイル */
    .result-section {
        background-color: white;
        padding: 30px;
        border-radius: 16px;
        margin-top: 20px;
    }

    /* ブロック（単語カード）のデザイン */
    .block-item {
        padding: 15px 10px;
        border-radius: 8px;
        text-align: center;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        transition: transform 0.2s;
    }
    .block-item:hover { transform: translateY(-3px); }
    .block-en { font-size: 1.2rem; font-weight: 700; color: #163354; margin-bottom: 4px; }
    .block-ja { font-size: 0.9rem; color: #5D6B75; }
    .block-role { 
        font-size: 0.75rem; 
        font-weight: bold; 
        color: #76808F; 
        background-color: rgba(255,255,255,0.7); 
        border-radius: 4px; 
        padding: 2px 6px; 
        margin-top: 8px;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# --- 背景要素の配置 ---
st.markdown('<div class="header-bg"></div>', unsafe_allow_html=True)

# --- メインレイアウト ---
# 中央寄せにするためのカラム設定
col_spacer1, col_main, col_spacer2 = st.columns([1, 2, 1])

with col_main:
    st.markdown('<div class="main-title">英文構造を、一瞬でクリアに。</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Visual English Converter</div>', unsafe_allow_html=True)

    # --- 入力カードエリア ---
    with st.container():
        st.markdown('<div class="input-card">', unsafe_allow_html=True)
        
        # APIキー入力（本来は環境変数などが良いですが、デモ用にここに配置）
        # 目立たないようにexpanderに入れるか、シンプルに置く
        with st.expander("🔑 API Key Settings", expanded=False):
            api_key = st.text_input("Gemini API Key", type="password")

        st.markdown("##### 解析したい英文を入力")
        input_text = st.text_area(
            label="hidden_label", # ラベルはCSSで隠すか、直書きで見せる
            placeholder="例: It feels like a lifetime since Joe Biden was in the Oval Office.",
            height=120,
            label_visibility="collapsed"
        )
        
        st.write("") # スペース
        analyze_btn = st.button("構造を解析する", type="primary")
        
        st.markdown('</div>', unsafe_allow_html=True) # End input-card

# --- 解析ロジック & 結果表示 ---
if analyze_btn and input_text:
    if not api_key:
        st.warning("まずはAPIキーを設定してください 🔑")
    else:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')

        # プログレス表示もWise風にシンプルにしたいところですが、標準スピナーを使用
        with st.spinner("Analyzing structure..."):
            try:
                # プロンプト（前回と同じくJSON構造化データを要求）
                prompt = f"""
                あなたは英語のプロです。以下の英文を解析し、UI表示用のJSONデータを作成してください。
                
                対象: "{input_text}"
                
                【出力JSON形式】
                {{
                    "translation": "自然な日本語訳",
                    "point": "文法や構造のポイントを一言で（例：倒置による強調）",
                    "blocks": [
                        {{
                            "text": "英語のチャンク",
                            "meaning": "意味",
                            "role": "S/V/O/C/Mなどの役割",
                            "bg_color": "#E3F2FD" (役割に応じた淡いパステルカラー)
                        }}
                    ],
                    "dot_code": "Graphviz DOTコード（ノードは日本語ラベル、横向きレイアウト rankdir=LR）"
                }}
                
                配色は以下を参考にしてください:
                - 主語(S): #E3F2FD (Blue)
                - 動詞(V): #FBE9E7 (Red/Orange)
                - 目的語/補語: #E8F5E9 (Green)
                - 修飾/その他: #FFF3E0 (Yellow/Orange)
                Markdownなし、JSONのみ出力。
                """
                
                response = model.generate_content(prompt)
                cleaned_text = response.text.replace("```json", "").replace("```", "").strip()
                data = json.loads(cleaned_text)

                # --- 結果エリア（カードの下に表示） ---
                st.markdown("---")
                
                # 日本語訳セクション
                st.markdown(f"""
                <div class="result-section" style="border-left: 5px solid #2ED06E;">
                    <h3 style="color: #163354; margin:0;">{data['translation']}</h3>
                    <p style="color: #5D6B75; margin-top: 10px;">💡 Point: {data['point']}</p>
                </div>
                """, unsafe_allow_html=True)

                # ブロックセクション
                st.markdown("### 🧱 Structure Blocks")
                
                blocks = data['blocks']
                # グリッド表示のための行計算
                rows = [blocks[i:i + 4] for i in range(0, len(blocks), 4)]
                
                for row in rows:
                    cols = st.columns(4)
                    for i, block in enumerate(row):
                        with cols[i]:
                            st.markdown(f"""
                            <div class="block-item" style="background-color: {block['bg_color']};">
                                <div class="block-en">{block['text']}</div>
                                <div class="block-ja">{block['meaning']}</div>
                                <div class="block-role">{block['role']}</div>
                            </div>
                            """, unsafe_allow_html=True)
                    st.write("") # 行間

                # ツリー図セクション
                st.markdown("### 🌳 Syntax Tree")
                with st.expander("ツリー図で詳細を見る", expanded=True):
                    st.graphviz_chart(data['dot_code'])

            except Exception as e:
                st.error(f"解析エラー: {e}")
