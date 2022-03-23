def main():


    from googleapiclient.http import MediaFileUpload
    from Google import Create_Service
    import qrcode
    from tkinter.filedialog import askopenfilename
    import pandas as pd
    from os.path import exists


    CLIENT_SECRET_FILE = "client_secret.json"
    API_NAME="drive"
    API_VERSION="v3"
    SCOPES=["https://www.googleapis.com/auth/drive"]

    
    folder_id="18C4heZLU1LbUTBuY-cxwoACVIJ7xx_CP"
    csv_id="1GYIS3sqK1IiTcLJMGKaJoCEWhLfhGQ3a" 

    name=input("Enter Name: ")
    roll_no=input("Enter Roll Number: ")
    email_id=input("Enter Email ID: ")

    def give_qr(folder_id,csv_id,name,roll_no,email_id):
        
        service=Create_Service(CLIENT_SECRET_FILE,API_NAME,API_VERSION,SCOPES)

        pic_name=name+"_"+roll_no
        pic_path=pic_path=askopenfilename()

        pic_metadata={
            'name':pic_name,
            'parents':[folder_id]
        }

        pic_media = MediaFileUpload(pic_path, mimetype="image/jpeg")

        pic_id = service.files().create(
            body=pic_metadata,
            media_body=pic_media,
            fields="id"
        ).execute().get('id')


        request_body = {
            'role': 'reader',
            'type': 'anyone'
        }

        service.permissions().create(
            fileId=pic_id,
            body=request_body
        ).execute()

        link = service.files().get(
            fileId=pic_id,
            fields='webViewLink'
        ).execute().get('webViewLink')


        if exists("Details.csv"):
            df=pd.read_csv("Details.csv")
        else:
            df=pd.DataFrame(columns=["Name","Roll Number","Email ID","Id Link"])
        temp={"Name":name,"Roll Number":roll_no,"Email ID":email_id,"Id Link":link}
        df=df.concat(temp,ignore_index=True,axis=0)
        df.to_csv("Details.csv",index=None)


        
        csv_media=MediaFileUpload("Details.csv",mimetype="text/csv")
        service.files().update(
            fileId=csv_id,
            media_body=csv_media
        ).execute()


        qr=qrcode.make(link)
        qr.save(pic_name+".png")


    give_qr(folder_id,csv_id,name,roll_no,email_id)

      
       
if __name__ == "__main__":
    main()

