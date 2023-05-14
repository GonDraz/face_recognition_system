from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from datetime import datetime

import tensorflow as tf
from imutils.video import VideoStream

import argparse
import include.facenet
import imutils
import os
import csv
import json
import pickle
import include.align.detect_face
import numpy as np
import cv2
import collections
from sklearn.svm import SVC

from tkinter import *
from tkinter import messagebox, ttk

from PIL import Image, ImageTk

from pyfirmata import Arduino, util, STRING_DATA
from time import strftime

from store.path import Path
# port='COM7'
# board=Arduino(port)


def mark_attendance_by_id(id):
    pathname = Path.Data.info + f"{id}.json"

    try:
        with open(pathname, "r", encoding="utf-8") as f:
            json_data = json.load(f)
            name = json_data["name"]
            dep = json_data["dep"]
            div = json_data["div"]

            now = datetime.now()
            n = now.strftime("%d_%m_%Y")

            path = "attendance"

            if not os.path.exists(path):
                os.makedirs(path)

            path = path + "/" + n + ".csv"

            if not os.path.exists(path):
                f = open(path, "x")
                f.write('\ufeff')

            with open(path, "r+", newline='', encoding='utf-8') as f:
                myDataList = f.readlines()
                name_list = []

                for line in myDataList:
                    entry = line.split((","))
                    name_list.append(entry[1])

                if (id not in name_list):
                    now = datetime.now()
                    dtString = now.strftime("%H:%M:%S")
                    writer = csv.writer(f)
                    writer.writerows([(dtString, id, name, dep, div)])
                    student_table.insert(
                        "", END, values=[dtString, id, name, dep, div])
    except Exception as es:
        print(str(es))


def face_rec_cam(lmain):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--path', help='Path of the video you want to test on.', default=0)
    args = parser.parse_args()

    MINSIZE = 20
    THRESHOLD = [0.6, 0.7, 0.7]
    FACTOR = 0.709
    IMAGE_SIZE = 182
    INPUT_IMAGE_SIZE = 160
    CLASSIFIER_PATH = Path.Include.faceModel
    VIDEO_PATH = args.path
    FACENET_MODEL_PATH = Path.Include.pb

    # Load The Custom Classifier
    with open(CLASSIFIER_PATH, 'rb') as file:
        model, class_names = pickle.load(file)
    print("Custom Classifier, Successfully loaded")

    with tf.Graph().as_default():

        gpu_options = tf.compat.v1.GPUOptions(
            per_process_gpu_memory_fraction=0.333)
        sess = tf.compat.v1.Session(config=tf.compat.v1.ConfigProto(
            gpu_options=gpu_options, log_device_placement=False))

        with sess.as_default():

            # Load the model
            print('Loading feature extraction model')
            include.facenet.load_model(FACENET_MODEL_PATH)

            # Get input and output tensors
            images_placeholder = tf.compat.v1.get_default_graph().get_tensor_by_name("input:0")
            embeddings = tf.compat.v1.get_default_graph().get_tensor_by_name("embeddings:0")
            phase_train_placeholder = tf.compat.v1.get_default_graph(
            ).get_tensor_by_name("phase_train:0")
            embedding_size = embeddings.get_shape()[1]

            pnet, rnet, onet = include.align.detect_face.create_mtcnn(
                sess, Path.Include.align)

            people_detected = set()
            person_detected = collections.Counter()

            global cap
            cap = VideoStream(src=0).start()

            def video_streaming():
                frame = cap.read()
                frame = imutils.resize(frame, width=730, height=740)
                frame = cv2.flip(frame, 1)

                bounding_boxes, _ = include.align.detect_face.detect_face(
                    frame, MINSIZE, pnet, rnet, onet, THRESHOLD, FACTOR)

                faces_found = bounding_boxes.shape[0]
                try:
                    if faces_found > 1:
                        cv2.putText(frame, "Only one face", (0, 100), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                                    1, (255, 255, 255), thickness=1, lineType=2)
                    elif faces_found > 0:
                        det = bounding_boxes[:, 0:4]
                        bb = np.zeros((faces_found, 4), dtype=np.int32)
                        for i in range(faces_found):
                            bb[i][0] = det[i][0]
                            bb[i][1] = det[i][1]
                            bb[i][2] = det[i][2]
                            bb[i][3] = det[i][3]
                            # print(bb[i][3]-bb[i][1])
                            # print(frame.shape[0])
                            # print((bb[i][3]-bb[i][1])/frame.shape[0])
                            if (bb[i][3]-bb[i][1])/frame.shape[0] > 0.25:
                                cropped = frame[bb[i][1]:bb[i]
                                                [3], bb[i][0]:bb[i][2], :]
                                scaled = cv2.resize(cropped, (INPUT_IMAGE_SIZE, INPUT_IMAGE_SIZE),
                                                    interpolation=cv2.INTER_CUBIC)
                                scaled = include.facenet.prewhiten(scaled)
                                scaled_reshape = scaled.reshape(
                                    -1, INPUT_IMAGE_SIZE, INPUT_IMAGE_SIZE, 3)
                                feed_dict = {
                                    images_placeholder: scaled_reshape, phase_train_placeholder: False}
                                emb_array = sess.run(
                                    embeddings, feed_dict=feed_dict)

                                predictions = model.predict_proba(emb_array)
                                best_class_indices = np.argmax(
                                    predictions, axis=1)
                                best_class_probabilities = predictions[
                                    np.arange(len(best_class_indices)), best_class_indices]
                                best_name = class_names[best_class_indices[0]]
                                # print("Name: {}, Probability: {}".format(best_name, best_class_probabilities))

                                if best_class_probabilities > 0.8:
                                    cv2.rectangle(
                                        frame, (bb[i][0], bb[i][1]), (bb[i][2], bb[i][3]), (0, 255, 0), 2)
                                    text_x = bb[i][0]
                                    text_y = bb[i][3] + 20

                                    name = class_names[best_class_indices[0]]
                                    # code cho adruino
                                    # board.send_sysex(STRING_DATA, util.str_to_two_byte_iter(name))
                                    # string = strftime('%H:%M:%S %p')
                                    # board.send_sysex(STRING_DATA, util.str_to_two_byte_iter(string))

                                    cv2.putText(frame, name, (text_x, text_y), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                                                1, (255, 255, 255), thickness=1, lineType=2)
                                    cv2.putText(frame, str(round(best_class_probabilities[0], 3)), (text_x, text_y + 17),
                                                cv2.FONT_HERSHEY_COMPLEX_SMALL,
                                                1, (255, 255, 255), thickness=1, lineType=2)
                                    person_detected[best_name] += 1

                                    mark_attendance_by_id(name)
                                else:
                                    name = "Unknown"
                                    cv2.putText(frame, name, (text_x, text_y), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                                                1, (255, 255, 255), thickness=1, lineType=2)

                except:
                    pass

                # cv2.imshow('Face Recognition', frame)
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
                img = Image.fromarray(cv2image)
                imgtk = ImageTk.PhotoImage(image=img)
                lmain.imgtk = imgtk
                lmain.configure(image=imgtk)
                global replay
                replay = lmain.after(1, video_streaming)

        video_streaming()


class FaceRecCamView:
    def __init__(self, root, controller):
        self.controller = controller
        self.root = root

        title__lbl = Label(self.root, text="ĐIỂM DANH", font=(
            "Arial", 25, "bold"), bg="red", fg="white")
        title__lbl.place(x=0, y=0, width=1530, height=30)

        # button
        b1_1 = Button(self.root, text="Bắt đầu quét", command=self.face_recog,
                      cursor="hand2", font=("Arial", 15, "bold"), bg="darkblue", fg="white")
        b1_1.place(x=200, y=608, width=153, height=60)

        self.stop_btn = Button(self.root, text="Dừng quét", command=self.stop_face_recog,
                               cursor="hand2", font=("Arial", 15, "bold"), bg="darkblue", fg="white")
        self.stop_btn.place(x=370, y=608, width=153, height=60)

        # create a frame
        frame = Frame(root, bg="white")
        frame.grid()
        frame.place(x=10, y=40)
        # create a label in the frame
        self.lmain = Label(frame)
        self.lmain.grid()
        # =======================
        self.var_std_id = StringVar()
        self.var_std_name = StringVar()
        self.var_note = StringVar()

        self.attendances = []
        self.times = {}

        self.date_var = StringVar()
        self.from_date_var = StringVar()
        self.to_date_var = StringVar()

        self.right_frame = LabelFrame(
            self.root, bd=2, bg="white", relief=RIDGE, text="Thông tin điểm danh", font=("Arial", 12, "bold"))
        self.right_frame.place(x=755, y=50, width=590, height=610)

        self.table_frame = Frame(
            self.right_frame, bd=2, bg="white", relief=RIDGE)
        self.table_frame.place(x=5, y=5, width=590, height=580)

        Scroll_y = ttk.Scrollbar(self.table_frame, orient=VERTICAL)
        global student_table
        student_table = ttk.Treeview(
            self.table_frame, column=("Atd", "id", "name", "dep", "div"))
        Scroll_y.pack(side=RIGHT, fill=Y)
        Scroll_y.config(command=student_table.yview)

        student_table.heading("Atd", text="Thời gian")
        student_table.heading("id", text="MSSV")
        student_table.heading("name", text="Tên")
        student_table.heading("dep", text="Ngành")
        student_table.heading("div", text="Lớp")

        student_table["show"] = "headings"

        student_table.column("Atd", width=100)
        student_table.column("id", width=100)
        student_table.column("name", width=100)
        student_table.column("dep", width=100)
        student_table.column("div", width=100)

        student_table.pack(fill=BOTH, expand=1)

        # ====================== Face recognition ==================

    def face_recog(self):
        face_rec_cam(self.lmain)

    def stop_face_recog(self):
        self.stop_btn.after_cancel(replay)
        cap.stream.release()
