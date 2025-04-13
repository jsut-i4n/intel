import time

from flask import Flask, render_template, request , url_for

from templates import template, chat_template, detail_ask_template
from utils import llm_server
app = Flask(__name__)


# 主页 - 时间选择
@app.route('/')
def index():
    gif_url = url_for('static', filename='gif.gif')
    return render_template('time_selection.html', gif_url=gif_url)

# 主题选择页面
@app.route('/select-themes')
def select_themes():
    selected_time = request.args.get('time')
    gif_url = url_for('static', filename='gif.gif')
    return render_template('theme_selection.html', time=selected_time,gif_url=gif_url)

# 生成历史内容
@app.route('/generate-content', methods=['POST'])
def generate_content():
    data = request.json
    selected_time = data['time']
    selected_themes = data['themes']

    content = template.format(
        user_selected_time=selected_time,
        user_selected_themes=selected_themes
    )
    res = llm_server(content)
    return res

@app.route('/get-event-details', methods=['POST'])
def get_event_details():
    data = request.json
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    detail_event = data['event']
    content = detail_ask_template.format(
        current_time=current_time,
        detail_event=detail_event
    )
    res = llm_server(content)
    return res

@app.route('/chat', methods=['POST'])
def chat_with_content():
    data = request.json
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    user_chat_history = data['history_content']
    user_question = data['message']
    content = chat_template.format(current_time=current_time, user_chat_history=user_chat_history, user_question=user_question)
    res = llm_server(content)
    return res


if __name__ == '__main__':
    app.run(debug=True)
