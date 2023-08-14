import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

system_prompt_1 = """
このスレッドでは以下ルールを厳格に守ってください。
あなたはお店のホームページにある文章をもとに、不芳なお店かを判断するシステムです
不芳の観点は以下です。以下である確率をパーセントで答えてください。
"""

system_prompt_2 = """

回答は以下のフォーマットにしてください。
【確率】

【根拠】

"""

system_prompt = "".join([system_prompt_1, system_prompt_2])

# # st.session_stateを使いメッセージのやりとりを保存

st.session_state["messages"] = [
    {"role": "system", "content": system_prompt}
    ]

# チャットボットとやりとりする関数
def communicate():

    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
        ]

    #追加観点のプロンプトに追加
    
    if aspect_input != "":
        system_prompt_1_added = "\n・".join([system_prompt_1, aspect_input])
        system_prompt_added = "".join([system_prompt_1_added, system_prompt_2])
        st.session_state["messages"] = [
            {"role": "system", "content": system_prompt_added}
            ]

    messages = st.session_state["messages"]
    
    user_message = {"role": "user", "content": st.session_state["user_input"]}
    st.session_state["messages"].append(user_message)

    # response = openai.ChatCompletion.create(
    #     model="gpt-3.5-turbo",
    #     messages=st.session_state["messages"]
    # )  

    response = openai.ChatCompletion.create(
        model= option,
        temperature = selected_value,
        messages=st.session_state["messages"]
    )  

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去

# ユーザーインターフェイスの構築
st.title("不芳サイトか判定します")
st.write("サイトの文章を入力してください")
#st.write("概要、雰囲気、人気メニュー、接客態度の観点で要約します")
st.write("指定された観点の不芳サイトか判定します")

# ユーザーからの観点指定入力
aspect_input = st.text_input("観点を入力してください（例：アダルト、違法ドラッグ、マルチ商法）", key="aspect_input")

if "user_input" not in st.session_state:
    st.session_state["user_input"] = ""
    
# ユーザーからの口コミ入力
review_input = st.text_area("サイトの文章", key="review_input")

option = st.radio(
    'GPTのバージョン', #ラベルを空に
    ('gpt-3.5-turbo', 'gpt-4'),
    index=0 # デフォルトで左側のボタンを選択状態にする
)

options_tmp = [i/10 for i in range(21)]
selected_value = st.selectbox('temperature',options_tmp, index=10)

if st.button("判定開始"):
    
    st.session_state["user_input"] = review_input  # 追加する行
    #st.session_state["user_input"] = st.text_area("レストランの口コミ", key="user_input")  # ここに移動
    
    communicate()

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "＜サイトの文章＞"
        if message["role"]=="assistant":
            speaker="＜判定結果＞"

        # st.write(speaker + ": " + message["content"])
        st.write("-----------------------------------------------------------------------------------------------")
        st.write(speaker)
        st.write(message["content"])
