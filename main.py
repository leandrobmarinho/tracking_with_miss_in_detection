import argparse
import multiprocessing as mp
import cv2
import dlib


if __name__ == '__main__':
    history = list(dict())

    # TODO para cada frame guardar historico dos n elementos
    history.append({'coords': [(7, 211), (269, 580)], 'feature': [1, 1, 1]})
    history.append({'coords': [(437, 350), (690, 590)], 'feature': [2, 2, 2]})



    VIDEO_PATH = 'elevador.mp4'
    WIN_NAME = 'window'
    WIN_WIDTH = 800
    WIN_HEIGHT = 600

    skip_frames = 0
    pause_frames = False


    cv2.namedWindow(WIN_NAME)
    # cv2.setMouseCallback(WIN_NAME, drag_and_select)
    vs = cv2.VideoCapture(VIDEO_PATH)

    while True:
        if not pause_frames:
            skip_frames -= 1
            (ret, frame) = vs.read()

            if frame is None:
                break
            # if skip_frames > 0:
            #     continue

            frame = cv2.resize(frame, (WIN_WIDTH, WIN_HEIGHT), cv2.INTER_AREA)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            draw_frame = frame.copy()

            # if tracking:
            #     for iQ in inputQueues:
            #         iQ.put(rgb)
            #
            #     for oQ in outputQueues:
            #         (objNum, (x1, y1, x2, y2)) = oQ.get()
            #         draw_box(draw_frame, x1, y1, x2, y2, objNum)
            #
            #         # update the box's coordinates
            #         boxes[objNum] = (x1, y1, x2, y2)

        # if dragging is True:
        #     # draw the bounding box if dragging
        #     draw_frame = frame.copy()
        #
        #     # draw all previous boxes
        #     for i, (x1, y1, x2, y2) in enumerate(boxes):
        #         draw_box(draw_frame, x1, y1, x2, y2, i)
        #
        #     # draw the current box that is being dragged
        #     cv2.rectangle(draw_frame, (startX, startY), (endX, endY), (0,255,0), 2)
        #     cv2.putText(draw_frame, 'object', (startX, startY - 15),
        #                 cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)

        # cv2.putText(draw_frame, 'Tracking: ' + str(tracking), (10, WIN_HEIGHT - 25),
        #             cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)
        cv2.imshow(WIN_NAME, draw_frame)

        # handle keys
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        if key == ord('s'):
            skip_frames = 100
        if key == ord('p'):
            # toggle pause
            if pause_frames is True:
                pause_frames = False
            else:
                pause_frames = True
        # if key == ord('t'):
        #     # toggle tracking
        #     if tracking is False:
        #         tracking = True
        #         if inputQueues or len(boxes) > last_queue_length:
        #             for i, box in enumerate(boxes[last_queue_length:]):
        #                 i = last_queue_length + i
        #                 iQ = mp.Queue()
        #                 oQ = mp.Queue()
        #                 inputQueues.append(iQ)
        #                 outputQueues.append(oQ)
        #
        #                 p = mp.Process(target=tracker_callback, args=(box, rgb, i, iQ, oQ))
        #                 p.daemon = True
        #                 p.start()
        #
        #         last_queue_length = len(inputQueues)

            # elif tracking is True:
            #     tracking = False

    cv2.destroyAllWindows()
    vs.release()
