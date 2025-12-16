# 1. 必要なライブラリをインポート
import streamlit as st
# LangChainから必要な3つをインポート
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
# 環境変数を読み込むための道具
from dotenv import load_dotenv

# 2. 環境変数の読み込み
# ここで .env ファイルを読み込みます
load_dotenv()

# 3. Webアプリの画面作り
st.title("専門家AIチャットアプリ")
st.write("質問を入力して、回答してほしい専門家を選んでください。")

# 【課題要件】ラジオボタンで専門家の種類を選択させる
# ヒント: st.radio("ラベル", ("選択肢1", "選択肢2"...))
role_option = st.radio(
    "回答する専門家を選んでください:",
    ("熱血なプログラミング講師", "冷静な科学者", "関西弁のコメディアン")
)

# 【課題要件】入力フォームを作る
# ヒント: st.text_input("ラベル")
input_text = st.text_input("質問を入力してください")

# 4. LLMとのやり取りを行う関数
def get_llm_response(query, role):
    
    # (1) モデルの準備 (GPT-3.5など)
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
    
    # (2) 選ばれた役割(role)に応じてシステムメッセージを切り替える
    if role == "熱血なプログラミング講師":
        system_message = "あなたは情熱的で励まし上手なプログラミング講師です。初心者にもわかりやすく解説してください。"
    elif role == "冷静な科学者":
        system_message = "あなたは論理的で冷静な科学者です。事実に基づき簡潔に回答してください。"
    elif role == "関西弁のコメディアン":
        system_message = "あなたは面白い関西弁のコメディアンです。ボケとツッコミを交えて回答してください。"
    else:
        system_message = "あなたは親切なアシスタントです。"

    # (3) プロンプト（指示書）の作成
    # system_message と ユーザーの入力 {input} を組み合わせる
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("user", "{input}")
    ])
    
    # (4) チェーンをつなぐ (Prompt -> LLM -> OutputParser)
    chain = prompt | llm | StrOutputParser()
    
    # (5) AIに実行させて結果を返す
    return chain.invoke({"input": query})


# 5. ボタンが押されたときの動作
if st.button("回答を生成"):
    # テキストが入力されていれば実行
    if input_text:
        with st.spinner("AIが回答を生成中..."):
            # 上で作った関数を呼び出す
            response = get_llm_response(input_text, role_option)
            
            # 結果を表示する
            st.divider()
            st.markdown(f"### 【{role_option}】からの回答")
            st.write(response)
            
    else:
        st.warning("質問内容を入力してください。")
        