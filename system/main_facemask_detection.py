import module.VideoStream_opencv as vs
import cv2


cctv = vs.VideoStream(1, "http://10.0.0.20:8081").start()

if __name__ == '__main__':
    while True:
        # grab the frame from the threaded video stream and resize it
        # to have a maximum width of 400 pixels
        cctv_frame = cctv.process()
        # rs = cctv.detect_mask()
        # if "No Mask" in rs:
        #     cctv.tts.say("Someone is not wearing a face mask.")
        #     cctv.tts.runAndWait()
        cv2.imshow("CCTV", cctv_frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    cv2.destroyAllWindows()
    cctv.stop()

