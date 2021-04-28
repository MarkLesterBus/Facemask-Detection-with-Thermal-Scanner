# from flask import (Blueprint, flash, g, redirect, render_template, Response, request, session, url_for, jsonify)
# from .AuthController import login_required
# from ..module.VideoStream_opencv import VideoStream
# import cv2
# from ..model.schema import db, Camera
#
# detections = Blueprint('detections', __name__, url_prefix='/detections', template_folder='templates')
# global camera
#
# @detections.route('/<camera_id>')
# @login_required
# def index(camera_id):
#     camera = getById(camera_id)
#     return render_template('detections/index.html', camera=camera)
#
# @detections.route('/source/<url>')
# def source(url):
#     return Response(get_stream(get_stream(url)),mimetype='multipart/x-mixed-replace; boundary=frame',)
#
# def get_stream(url):
#     camera = VideoStream(2, url).start()
#     while True:
#         frame = camera.process()
#         ret, frame = cv2.imencode('.png', frame)
#
#         if frame is not None:
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n\r\n')
#         else:
#             break
#
# # @detections.route('/capture', methods=['GET'])
# # @login_required
# # def capture():
# #     camera = VideoStream(0)
# #     camera.capture()
# #     return "Captured"
#
# def createRecord(name):
#     db.session.add(name)
#     db.session.commit()
#
#
# def deleteRecord(name):
#     db.session.delete(name)
#     db.session.commit()
#
#
# def getByName(name):
#     rs = Camera.query.filter_by(name=name).first()
#     return rs
#
# def getById(id):
#     rs = Camera.query.filter_by(id=id).first()
#     return rs
#
# def getAll():
#     rs = Camera.query.order_by(Camera.name).all()
#     return rs
#
#
# def flashHandler(message):
#     (value, category) = message
#     if category == 'success':
#         flash(value, category)
#     elif category == 'info':
#         flash(value, category)
#     elif category == 'warning':
#         flash(value, category)
#     elif category == 'danger':
#         flash(value, category)
#     else:
#         flash(value, 'default')
