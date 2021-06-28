import time
import glob
import cv2
import numpy as np


class YoloTest(object):
        def __init__(self):
                self.CONFIDENCE_THRESHOLD = 0.5
                self.NMS_THRESHOLD = 0.4

        def YoloImage(self,cfg,weights,imagepath,labellist,clr):
                CONFIDENCE_THRESHOLD = 0.5
                NMS_THRESHOLD = 0.4
                cfg=cfg
                weights=weights
                lbls =labellist
                COLORS =clr
                net = cv2.dnn.readNetFromDarknet(cfg, weights)
                net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
                net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
                
                layer = net.getLayerNames()
                layer = [layer[i[0] - 1] for i in net.getUnconnectedOutLayers()]
                image=cv2.imread(imagepath)
                (H_ORI, W_ORI)=image.shape[:2]
                image=cv2.resize(image,(512,512))
                (H, W) = image.shape[:2]
                
                blob = cv2.dnn.blobFromImage(image, 1/255, (512, 512), swapRB=True, crop=False)
                net.setInput(blob)
                
                start_time = time.time()
                layer_outs = net.forward(layer)
                end_time = time.time()
                boxes = list()
                centerboxes=list()
                confidences = list()
                class_ids = list()
                result=list()
                for output in layer_outs:
                        for detection in output:
                                scores = detection[5:]
                                class_id = np.argmax(scores)
                                confidence = scores[class_id]
                                if confidence > CONFIDENCE_THRESHOLD:
                                        box = detection[0:4] * np.array([W, H, W, H])
                                        (center_x, center_y, width, height) = box.astype("int")

                                        x = int(center_x - (width / 2))
                                        y = int(center_y - (height / 2))

                                        boxes.append([x, y, int(width), int(height),int(center_x),int(center_y)])
                                        confidences.append(float(confidence))
                                        class_ids.append(class_id)
                idxs = cv2.dnn.NMSBoxes(boxes, confidences, CONFIDENCE_THRESHOLD, NMS_THRESHOLD )
                if len(idxs) > 0:
                        for i in idxs.flatten():
                                (x, y) = (boxes[i][0], boxes[i][1])
                                (w, h) = (boxes[i][2], boxes[i][3])
                                color = [int(c) for c in COLORS[class_ids[i]]]
                                cv2.rectangle(image, (x, y), (x+w, y+h), color, 2)
                                text = "{}: {:.4f}".format(lbls[class_ids[i]], confidences[i])
                                result.append({'score': confidences[i],'id': str(lbls[class_ids[i]])})
                                centerboxes.append([int(((boxes[i][4]/W)*W_ORI)),int(((boxes[i][5]/H)*H_ORI))])
                                cv2.putText(image, text, (x, y -5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                                label = "Inference Time: {:.2f} ms".format(end_time - start_time)
                                cv2.putText(image, label, (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)

                return result,image,centerboxes
                                

