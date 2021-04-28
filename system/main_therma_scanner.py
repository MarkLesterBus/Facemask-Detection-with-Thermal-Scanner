import module.VideoStream_opencv as vs
import sqlalchemy as db
import datetime
import cv2

engine = db.create_engine('sqlite:///db/database.sqlite')
connection = engine.connect()
metadata = db.MetaData()
persons = db.Table('Persons', metadata, autoload=True, autoload_with=engine)
attendance = db.Table('Attendance', metadata, autoload=True, autoload_with=engine)

scan = vs.VideoStream(0).start()

if __name__ == '__main__':
    while True:
        # grab the frame from the threaded video stream and resize it
        # to have a maximum width of 400 pixels
        tstamp = datetime.datetime.now()
        scan_frame = scan.frame
        pid = scan.detect_qr()
        if pid != "":
            scan.tts.say("Checking ID.")
            scan.tts.runAndWait()

            query = db.select([persons]).where(persons.columns.pid == pid)
            rp = connection.execute(query)
            rs = rp.fetchall()
            if rs != []:
                scan.tts.say("ID check completed.")
                scan.tts.runAndWait()

                scan.tts.say("Checking temperature.")
                scan.tts.runAndWait()

                temp = scan.detect_temp()

                scan.tts.say("Temperature check completed.")
                scan.tts.runAndWait()

                if float(temp) <= 37.00:
                    scan.tts.say("Your temperature is {} degree celcius,".format(temp))
                    scan.tts.say("temperature level is normal.")
                    scan.tts.runAndWait()

                    try:
                        query = attendance.insert().values(
                            pid=pid,
                            temp=temp,
                            time=tstamp.strftime("%I:%M %p"),
                            date=tstamp.strftime("%Y-%m-%d"),
                        )
                        connection.execute(query)
                        scan.tts.say("Welcome {}".format(rs[0].fname))
                        scan.tts.runAndWait()
                    except Exception as e:
                        print(e)
                else:
                    scan.tts.say("Your temperature is {} degree celcius,".format(temp))
                    scan.tts.say("Your health is at risk, please seek medical attention.")
                    scan.tts.runAndWait()
                    try:
                        query = attendance.insert().values(
                            pid=pid,
                            temp=temp,
                            time=tstamp.strftime("%I:%M %p"),
                            date=tstamp.strftime("%Y-%m-%d"),
                        )
                        connection.execute(query)
                        scan.tts.say("You cannot enter {}".format(rs[0].fname))
                        scan.tts.runAndWait()
                    except Exception as e:
                        print(e)

            else:
                scan.tts.say("Invalid ID.")
                scan.tts.runAndWait()

        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break

    cv2.destroyAllWindows()
    scan.stop()
