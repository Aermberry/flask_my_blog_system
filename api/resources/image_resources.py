import datetime
import os

from flask import request, jsonify, current_app, send_from_directory
from flask_restful import Resource
from werkzeug.utils import secure_filename


class ImageListResources(Resource):
    def get(self):
        # 创建一个空数组用于存储文件信息的字典
        file_info_list = []
        file_list = os.listdir(current_app.config["UPLOAD_FOLDER"])

        for file in file_list:
            file_obj = {}
            # 获取文件的完整路径
            file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], file)
            file_obj['file_name'] = file
            if os.path.isfile(file_path):
                file_size = os.path.getsize(file_path)

                # 将字节数转换为更友好的格式（例如，KB、MB、GB等）
                if file_size < 1024:
                    size_str = f"{file_size} bytes"
                elif 1024 <= file_size < 1048576:
                    size_str = f"{file_size / 1024:.2f} KB"
                elif 1048576 <= file_size < 1073741824:
                    size_str = f"{file_size / 1048576:.2f} MB"
                else:
                    size_str = f"{file_size / 1073741824:.2f} GB"

                file_obj['file_size'] = size_str

            file_info_list.append(file_obj)

        return jsonify(file_info_list)

    def post(self):
        try:
            upload_file = request.files['image']
            if upload_file.filename != '':
                timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                filename = timestamp + '_' + secure_filename(upload_file.filename)
                upload_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

                base_url = request.url_root
                image_url = base_url + 'uploads/' + filename

                return {
                    'message': 'Image uploaded successfully',
                    'image_url': image_url
                }
            else:
                return {'message': 'No file selected'}
        except Exception as e:
            return {'message': 'Error: ' + str(e)}

    def put(self):
        try:
            # 获取 JSON 数据
            data = request.json

            # 从 JSON 数据中获取旧文件名和新文件名
            old_file_name = data.get('origin_name')
            new_file_name = data.get('rename')

            # 拼接旧文件路径和新文件路径
            old_file_path = os.path.join('uploads', old_file_name)
            new_file_path = os.path.join('uploads', new_file_name)

            # 检查旧文件是否存在
            if not os.path.exists(old_file_path):
                return jsonify({'error': 'Old file not found', 'origin_name': old_file_path}), 404

            # 执行文件重命名操作
            os.rename(old_file_path, new_file_path)

            # return jsonify({'message': 'File renamed successfully'}), 200
            return jsonify({"message": "File renamed successfully"})

        except Exception as e:
            return jsonify({'error': str(e)}), 500


class ImageResources(Resource):

    def delete(self, image_name):
        try:
            # 构建要删除的文件的完整路径
            file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], image_name)

            # 检查文件是否存在
            if os.path.exists(file_path):
                # 如果文件存在，执行删除操作
                os.remove(file_path)
                return jsonify({'message': 'Delete success', 'file': file_path})
            else:
                # 如果文件不存在，返回错误响应
                return jsonify({"error": "File not found", "file": file_path}), 404

        except Exception as e:
            # 处理异常情况
            return jsonify({'error': str(e)}), 500

    def get(self, image_name):

        # image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image_name)
        # print(f"UPLOAD_FOLDER:{image_path}")
        # print(f"image_name:{image_name}")
        # print(f"url:{current_app.config['UPLOAD_FOLDER']}")
        # return send_file(image_path)

        return send_from_directory(current_app.config['UPLOAD_FOLDER'], image_name)
