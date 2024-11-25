from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
import os
from dotenv import load_dotenv
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging

# 设置日志级别
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
# 修改CORS配置
CORS(app, supports_credentials=True)

# GLM-4 API配置
API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
API_KEY = os.getenv('GLM_API_KEY')

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/ping', methods=['GET', 'OPTIONS'])
def ping():
    """健康检查端点"""
    return jsonify({'status': 'ok', 'message': 'Server is running'})

@app.route('/api/chat', methods=['POST', 'OPTIONS'])
@limiter.limit("20 per minute")
def chat():
    if request.method == 'OPTIONS':
        return '', 204
        
    try:
        logger.debug(f"收到请求头: {request.headers}")
        logger.debug(f"收到请求数据: {request.get_data()}")
        
        # 验证请求数据
        if not request.is_json:
            logger.error("请求不是JSON格式")
            return jsonify({
                'success': False,
                'error': '请求必须是JSON格式'
            }), 400

        data = request.get_json()
        if 'message' not in data:
            logger.error("缺少message字段")
            return jsonify({
                'success': False,
                'error': '缺少message字段'
            }), 400

        user_message = data['message']
        logger.info(f"收到用户消息: {user_message}")
        
        # 准备请求数据
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
        
        payload = {
            "model": "glm-4",
            "messages": [
                {
                    "role": "system",
                    "content": "你是冉岩岩的AI助手，你会以专业、友好的方式回答问题。你的回答应该简洁、准确、有帮助。"
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            "temperature": 0.7,
            "max_tokens": 2048,
            "stream": False
        }
        
        # 调用GLM-4 API
        try:
            logger.info("正在调用GLM-4 API...")
            response = requests.post(API_URL, headers=headers, json=payload)
            logger.info(f"API响应状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"API响应内容: {result}")
                
                if "choices" in result and len(result["choices"]) > 0:
                    ai_response = result["choices"][0]["message"]["content"]
                    return jsonify({
                        'success': True,
                        'response': ai_response
                    })
                else:
                    raise Exception("API返回的数据格式不正确")
            else:
                raise Exception(f"API请求失败: {response.text}")
            
        except Exception as e:
            logger.error(f"API调用失败: {str(e)}")
            raise e

    except Exception as e:
        error_msg = str(e)
        logger.error(f"发生错误: {error_msg}")
        return jsonify({
            'success': False,
            'error': error_msg
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)